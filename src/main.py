import openpyxl
import os
import requests
from openpyxl.drawing.image import Image
import urllib.request
from openpyxl.styles import Alignment
import re
from openpyxl.styles import Font
from openpyxl.cell.cell import get_column_letter
import time
from openpyxl.utils.units import pixels_to_EMU
from openpyxl.utils.units import cm_to_EMU
from openpyxl.drawing.xdr import XDRPoint2D, XDRPositiveSize2D
from openpyxl.drawing.spreadsheet_drawing import AbsoluteAnchor, OneCellAnchor, AnchorMarker
import copy

TEMPLETE_PATH = r".\resource\templete\templete.xlsx" # 最终订单模板路径

RESOUCE_PATH = r".\resource"
OUTPUT_PATH = r".\out"


def main():
    print("start making orders!!!!!")

    start_time = time.time()

    # 遍历 RESOUCE_PATH 文件夹下所有文件，找出xlsx文件，并打印不带后缀文件名
    for file in os.listdir(RESOUCE_PATH):
        if file.endswith(".xlsx"):
            file_name = file[:-5]
            filePath = os.path.join(RESOUCE_PATH, file)
            print("=======开始===：", filePath)

            # 读取店小秘导出订单表格
            workbookDianXiaoMi = openpyxl.load_workbook(filePath)
            worksheetDianXiaoMi = workbookDianXiaoMi["order_"]

            # 店小秘表头
            sheetHead = []
            for cell in worksheetDianXiaoMi[1]:
                sheetHead.append(cell.value)

            # 遍历店小秘中的订单
            rawData = []
            skuColor = {}
            for row in worksheetDianXiaoMi.iter_rows(min_row=2):
                if all(cell.value is None for cell in row):
                    continue # 空行跳过
                
                productSpecifications = row[sheetHead.index("产品规格")].value

                # 支持的尺码配置
                sizePart = re.findall(r'Size:(?:xs|s|m|l|xl|xxl|xxxl|xxxxl|2xl|3xl|4xl|5xl)?', productSpecifications, re.IGNORECASE)[0]
                # size转换为同一格式，大写，XXXL改成3XL
                size = sizePart.split(":")[1].upper()
                num_x = len(re.findall(r'X', size))
                if num_x > 1:
                    size = size.replace('X' * num_x, str(num_x) + "X")

                colorPart = productSpecifications.replace(sizePart, "")
                color = colorPart.split(":")[1].replace(" ", "_") # color 的空格转换成_,key不能有空格

                goodsId = row[sheetHead.index("产品ID")].value
                rawDataItem = {}

                goodsNum = row[sheetHead.index("产品数量")].value
                if goodsId + color in skuColor:
                    rawDataItem = rawData[skuColor[goodsId+color]]
                    if size in rawDataItem["sizeNum"]:
                        rawDataItem["sizeNum"][size] = rawDataItem["sizeNum"][size] + goodsNum
                    else:
                        rawDataItem["sizeNum"][size] = goodsNum
                else:
                    rawDataItem = {
                        "goodsName": row[sheetHead.index("产品名称")].value,
                        "sizeNum": {size: goodsNum},
                        "imgUrl": row[sheetHead.index("图片网址")].value,
                        "sku": goodsId,
                        "color": color,
                    }
                    skuColor[goodsId + color] = len(rawData)
                    rawData.append(rawDataItem)

            genfinalOrder(rawData, file_name)

    end_time = time.time()
    elapsed_time = end_time - start_time
    print("脚本总用时: {} 分 {} 秒".format(int(elapsed_time/60), int(elapsed_time%60)))
    print("输出文件在 out 这个文件夹里")



def get_absolute(worksheet, row, col):
    """
    获取单元格的右下方绝对位置（单位：像素），及单元格的宽高
    """
    x = 0
    y = 0
    # get_column_letter(int)把整数转换为Excel中的列索引
    col_letter = get_column_letter(col)
    # 获取每列的列宽
    width = worksheet.column_dimensions[col_letter].width
    # 计算第一列到目标列的总宽
    for i in range(col):
        col_letter = get_column_letter(i + 1)
        fcw = worksheet.column_dimensions[col_letter].width
        x += fcw
    # 如果Excel中高为默认值时，openpyxl却没有值为NoneValue，这一点我很奇怪。
    if not worksheet.row_dimensions[col].height:
        worksheet.row_dimensions[col].height = 13.5
        height = 13.5  # Excel默认列宽为13.5
    else:
        height = worksheet.row_dimensions[col].height
    # 计算第一行到目标行的总高
    for j in range(row):
        if not worksheet.row_dimensions[j + 1].height:
            worksheet.row_dimensions[j + 1].height = 13.5
            fch = 13.5
        else:
            fch = worksheet.row_dimensions[j + 1].height
        y += fch 
    # 把高单位转换为像素
    height = (height * 18) // 13.5  # 一个单元格高为13.5，像素为18
    # 把宽单位转换为像素
    width = (width * 72) // 9  # 一个单元格为宽为9，像素为72
    x = (x * 72) // 9
    y = (y * 18) // 13.5
    return x, y, width, height

def inster_image(worksheet, start_row, start_col, hieght, image_url, image_size=None):

    img = Image(image_url)
    img.height, img.width = image_size
    col_letter = get_column_letter(start_col)
    width = worksheet.column_dimensions[col_letter].width
    c2e = cm_to_EMU
    p2e = pixels_to_EMU
    size = XDRPositiveSize2D(p2e(img.height), p2e(img.width))
    image_cell, mod = divmod(img.height, 20)
    image_cell = image_cell+1 if mod != 0 else image_cell
    if (hieght - image_cell) % 2 == 0:
        start = start_row + (hieght - image_cell) // 2
        rowOff = c2e((0.6 * 49.77) / 99)
    else:
        start = start_row + (hieght - image_cell) // 2 + 1
        rowOff = c2e((0.4 * 49.77) / 99)
    colOff = (c2e(width + 1) - c2e(img.width / 72 * 13)) / 9
    marker = AnchorMarker(col=start_col - 1, colOff=colOff, row=start - 1, rowOff=rowOff)
    img.anchor = OneCellAnchor(_from=marker, ext=size)
    worksheet.add_image(img)




# 输入从店小秘导出的订单中原始数据，生成最终表格
def genfinalOrder(rawData, file_name):
    print("start gen Order-------------")

    # 读取最终订单模板
    workbookDianTemplete = openpyxl.load_workbook(TEMPLETE_PATH)
    worksheetTemplete = workbookDianTemplete["Sheet1"]

    goodsStartRowNum =11 # 商品开始的行数，每2行为一个产品

    # 遍历原始数据，写入到模板表格
    # 模板表格产品表头
    goodsTableHead = []
    for cell in worksheetTemplete[7]:
        goodsTableHead.append(cell.value)
    
    for i in range(len(rawData) + 200): # 加两百个空空格 
        goodsRaw = goodsStartRowNum + i * 2

        # 居中对齐
        for cells in worksheetTemplete.iter_cols(0, 12, goodsRaw, goodsRaw + 1):
            for cell in cells:
                cell.alignment = Alignment(horizontal='center', vertical='center')

        # 设置两行的总高度为100
        worksheetTemplete.row_dimensions[goodsRaw].height = 30
        worksheetTemplete.row_dimensions[goodsRaw + 1].height = 30


        if i < len(rawData): # 有数据的表格
            rawDataItem = rawData[i] # 每个订单的原始数据

            # 产品序号
            worksheetTemplete["A{}".format(goodsRaw)] = i + 1

            # 从url获取产品图片
            print("sku：", rawDataItem["sku"], "||color：", rawDataItem["color"], "||图片地址：", rawDataItem["imgUrl"])
            opener = urllib.request.build_opener()
            opener.addheaders = [('User-agent', 'Mozilla/5.0')]
            response = opener.open(rawDataItem["imgUrl"])
            # 暂存图片
            with open("./temp/tempImg{}.jpg".format(i), "wb") as f:
                f.write(response.read())
            # 设置产品图片
            inster_image(worksheetTemplete, goodsRaw + 1, 2, 0, "./temp/tempImg{}.jpg".format(i), image_size=(60, 60))

            # 各尺码数量
            sizeNum = rawDataItem["sizeNum"]
            totalNum = 0 # 当前商品的总数
            for eachSize in sizeNum:
                totalNum += sizeNum[eachSize]
                if eachSize == "XS":
                    worksheetTemplete.cell(goodsRaw + 1, goodsTableHead.index("S") + 1, "XS:" + str(sizeNum[eachSize]))
                elif eachSize == "4XL":
                    worksheetTemplete.cell(goodsRaw + 1, goodsTableHead.index("2XL") + 1, "4XL:" + str(sizeNum[eachSize]))
                elif eachSize == "5XL":
                    worksheetTemplete.cell(goodsRaw + 1, goodsTableHead.index("3XL") + 1, "5XL:" + str(sizeNum[eachSize]))
                else:
                    worksheetTemplete.cell(goodsRaw, goodsTableHead.index(eachSize) + 1, str(sizeNum[eachSize]))
            worksheetTemplete.cell(goodsRaw, goodsTableHead.index("合计") + 1, int(totalNum))

        # 产品名称（暂时先复制上面的模板）
        worksheetTemplete["C{}".format(goodsRaw)].number_format = worksheetTemplete["C9"].number_format
        # worksheetTemplete["C{}".format(goodsRaw)].font = worksheetTemplete["C9"].font.copy()
        # worksheetTemplete["C{}".format(goodsRaw)].alignment = worksheetTemplete["C9"].alignment.copy()
        # worksheetTemplete["C{}".format(goodsRaw)].border = worksheetTemplete["C9"].border.copy()
        # worksheetTemplete["C{}".format(goodsRaw)].fill = worksheetTemplete["C9"].fill.copy()
        # worksheetTemplete["C{}".format(goodsRaw)].protection = worksheetTemplete["C9"].protection.copy()
        worksheetTemplete["C{}".format(goodsRaw)].font = copy.copy(worksheetTemplete["C9"].font)
        worksheetTemplete["C{}".format(goodsRaw)].alignment = copy.copy(worksheetTemplete["C9"].alignment)
        worksheetTemplete["C{}".format(goodsRaw)].border = copy.copy(worksheetTemplete["C9"].border)
        worksheetTemplete["C{}".format(goodsRaw)].fill = copy.copy(worksheetTemplete["C9"].fill)
        worksheetTemplete["C{}".format(goodsRaw)].protection = copy.copy(worksheetTemplete["C9"].protection)



        # 合并单元格
        worksheetTemplete.merge_cells(f'B{goodsRaw}:B{goodsRaw + 1}')
        worksheetTemplete.merge_cells('K{}:K{}'.format(goodsRaw, goodsRaw + 1))
        worksheetTemplete.merge_cells('A{}:A{}'.format(goodsRaw, goodsRaw + 1))
        worksheetTemplete.merge_cells(f'C{goodsRaw}:C{goodsRaw + 1}')


        # 填写尺码中的商品数量
        # goodsNum =



        # 设置边框
        from openpyxl.styles.borders import Border, Side
        thin_border = Border(left=Side(style='thin'), 
                            right=Side(style='thin'), 
                            top=Side(style='thin'), 
                            bottom=Side(style='thin'))
        for col in range(1, 13):
            for row in range(goodsRaw, goodsRaw + 2):
                cell = worksheetTemplete.cell(row=row, column=col)
                cell.border = thin_border

    # 没有 OUTPUT_PATH 这个文件夹则创建这个文件夹
    if not os.path.exists(OUTPUT_PATH):
        os.mkdir(OUTPUT_PATH)

    workbookDianTemplete.save(os.path.join(OUTPUT_PATH, f'{file_name}_result.xlsx'))



main()