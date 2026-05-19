import openpyxl

# 加载输出文件
wb = openpyxl.load_workbook('工具输出工厂单/order_20260519111437332_2279079_result.xlsx')
ws = wb['Sheet1']

print('=== 图片位置检查 ===')
for img in ws._images:
    anchor = img.anchor
    if hasattr(anchor, '_from'):
        print(f"图片: row={anchor._from.row + 1}, col={anchor._from.col + 1}")
    else:
        print(f"图片: anchor={anchor}")

print('\n=== B列数据检查 ===')
for row in range(8, 20):
    cell = ws.cell(row=row, column=2)
    has_img = any(img for img in ws._images if hasattr(img.anchor, '_from') and img.anchor._from.row + 1 == row)
    print(f'B{row}: has_image={has_img}')