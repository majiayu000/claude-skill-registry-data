---
name: office-xlsx
description: 制作和修改 Excel 工作簿，维护公式、图表和格式，重算并生成 PDF 或工作表预览。
---

# Excel 工作簿

先调用 `load_workspace_dependencies`。读取与修改使用 `openpyxl`，新建复杂格式报表也可使用 `XlsxWriter`。使用返回的 Python 绝对路径执行工作目录脚本。

## 制作和修改

区分原始数据、计算和报告区域；设置清晰的列名、单位、日期和数值格式，冻结表头、配置筛选与打印范围。计算使用公式而不是硬编码结果。保留用户现有工作表和公式，修改默认另存为新文件。

```python
from openpyxl import Workbook, load_workbook
from openpyxl.styles import Font, PatternFill
from openpyxl.chart import BarChart, Reference

book = Workbook()
sheet = book.active
sheet.title = '月度统计'
sheet.append(['月份', '收入', '成本', '结余'])
sheet.append(['一月', 1200, 800, '=B2-C2'])
sheet.append(['二月', 1500, 950, '=B3-C3'])
sheet.freeze_panes = 'A2'
sheet.auto_filter.ref = sheet.dimensions
for row in sheet:
    for cell in row:
        cell.font = Font(name='Noto Sans CJK SC', bold=cell.row == 1)
for name in ['A', 'B', 'C', 'D']:
    sheet.column_dimensions[name].width = 18
sheet.print_area = 'A1:D3'
chart = BarChart()
chart.add_data(Reference(sheet, min_col=2, max_col=3, min_row=1, max_row=3), titles_from_data=True)
chart.set_categories(Reference(sheet, min_col=1, min_row=2, max_row=3))
sheet.add_chart(chart, 'F2')
book.save(output_path)
```

## 公式重算与验证

`openpyxl` 不计算公式。需要缓存计算结果时通过 `run_command` 执行 `[node, libreoffice, 'recalculate', '--input', workbook, '--output', fresh_xlsx]`。命令在工作目录执行，输出路径须全新；验证重算后实际数值，不能把存在公式等同于计算正确。

用 `checkOffice` 检查实际文件的工作表、公式数量和关键文字；用 `openpyxl.load_workbook(..., data_only=True)` 检查重算后的结果。导出 PDF 使用 `render_document`；PNG 预览指定准确 `sheet` 名称，可加 `range: 'A1:H20'`。

最终 XLSX 使用 `register_artifact` 登记。可识图模型检查预览的列宽、数值格式、图表和打印布局。结构检查不评估业务数据正确性。
