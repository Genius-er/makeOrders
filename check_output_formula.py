import openpyxl

# 加载输出文件
wb = openpyxl.load_workbook('工具输出工厂单/order_20260519111437332_2279079_result.xlsx')
ws = wb['Sheet1']

print('=== L列公式检查 ===')
for row in range(1, 20):
    cell = ws.cell(row=row, column=12)  # L列是第12列
    print(f'L{row}: value={repr(cell.value)}')