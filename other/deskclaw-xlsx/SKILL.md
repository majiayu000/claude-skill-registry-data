---
slug: deskclaw-xlsx
version: 3.0.0
displayName: Excel 表格工具（DeskClaw XLSX）
summary: "DeskClaw 自研 Excel 全能工具。基于 openpyxl 与 LibreOffice 公式引擎，支持创建、读取、编辑、公式重算与校验、unpack/pack 高级编辑、列行插入、pandas 数据分析与财务建模规范。"
tags: office, xlsx, excel, spreadsheet, formulas, pandas, openpyxl, libreoffice, financial-modeling
name: deskclaw-xlsx
description: "专业 Excel 文件（.xlsx）创建、读取、编辑、公式验证和格式化。覆盖数据表、财务模型、报表、统计分析等场景。当用户要求创建、编辑、分析任何 Excel 表格时使用此技能。"
setup: bootstrap.py
---

# DeskClaw XLSX v3.0

创建、读取、编辑和验证 Excel 表格。

## 第零步：Bootstrap

```python
python bootstrap.py
```

幂等，已装跳过。检查：`python -c "import openpyxl; print('READY')"`

## 命令速查表（Agent 必读）

| 任务 | 方法 |
|------|------|
| 创建新表格 | `from openpyxl import Workbook; wb = Workbook()` → 添加数据/公式/格式 → `wb.save()` |
| 读取分析 | `python scripts/xlsx_reader.py file.xlsx` 或 pandas |
| 编辑已有文件 | `from openpyxl import load_workbook; wb = load_workbook('file.xlsx')` |
| 添加列（带公式） | `python scripts/xlsx_add_column.py` |
| 插入行 | `python scripts/xlsx_insert_row.py` |
| 公式重算 | `python scripts/recalc.py output.xlsx`（**创建后必须执行**） |
| 公式验证 | `python scripts/formula_check.py file.xlsx --json` |
| 保存路径 | `wb.save(os.path.expanduser('~/Desktop/output.xlsx'))` |

## 创建新表格

```python
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
import os

wb = Workbook()
ws = wb.active
ws.title = "数据表"

# 表头
headers = ["姓名", "部门", "销售额", "占比"]
header_font = Font(bold=True, color="FFFFFF", name="Microsoft YaHei")
header_fill = PatternFill("solid", fgColor="4472C4")
for col, h in enumerate(headers, 1):
    cell = ws.cell(row=1, column=col, value=h)
    cell.font = header_font
    cell.fill = header_fill
    cell.alignment = Alignment(horizontal="center")

# 数据
data = [["张三", "销售部", 85000], ["李四", "市场部", 72000]]
for r, row_data in enumerate(data, 2):
    for c, val in enumerate(row_data, 1):
        ws.cell(row=r, column=c, value=val)

# 公式（绝对不要硬编码计算结果！）
ws['C4'] = '=SUM(C2:C3)'
ws['C4'].font = Font(bold=True)
for r in range(2, 4):
    ws.cell(row=r, column=4, value=f'=C{r}/C$4')
    ws.cell(row=r, column=4).number_format = '0.0%'

# 列宽
for col in ["A", "B", "C", "D"]:
    ws.column_dimensions[col].width = 15

wb.save(os.path.expanduser("~/Desktop/output.xlsx"))
```

创建后**必须**执行公式重算：
```bash
python scripts/recalc.py ~/Desktop/output.xlsx
```

## 核心规则

### 1. 公式优先（最重要）

```python
# ❌ 错误
total = sum([85000, 72000])
ws['C4'] = total  # 硬编码

# ✅ 正确
ws['C4'] = '=SUM(C2:C3)'
```

**每个计算值都必须用 Excel 公式。** 硬编码的数字无法在 Excel 中更新。

### 2. 公式重算（必须）

openpyxl 写入的公式只是字符串，保存后必须执行 `scripts/recalc.py` 让值生效。如果有公式错误（#REF!、#DIV/0!），recalc 会返回详细位置。

### 3. 编辑完整性

- **创建**：`Workbook()` 新建
- **编辑已有文件**：**必须** `load_workbook('existing.xlsx')`，绝对不要 `Workbook()` 新建
- 输出必须保留原有所有 sheet 和数据
- 保存后用 `xlsx_reader.py` 验证

### 4. 财务配色

| 角色 | 颜色 | 用法 |
|------|------|------|
| 输入/假设 | 蓝色 `Font(color="0000FF")` | 用户会改的数字 |
| 公式结果 | 黑色 `Font(color="000000")` | 所有计算值 |
| 跨 Sheet 引用 | 绿色 `Font(color="00B050")` | `='Sheet2'!A1` 类公式 |

### 5. 数字格式

```python
cell.number_format = '¥#,##0'      # 货币
cell.number_format = '0.0%'         # 百分比
cell.number_format = '@'            # 文本（年份用这个，避免 2026 变 2,026）
cell.number_format = '#,##0;(#,##0);"-"'  # 负数括号，零用横线
```

## 任务路由

```
用户任务
├─ 读取/分析 → xlsx_reader.py + pandas
├─ 从零创建 → openpyxl Workbook() → save → recalc.py
├─ 编辑已有文件
│   ├─ 简单修改 → openpyxl load_workbook()
│   └─ 添加列/插入行 → scripts/xlsx_add_column.py, xlsx_insert_row.py
├─ 修复公式 → XML unpack → 修 <f> 节点 → pack
└─ 验证公式 → formula_check.py（静态）+ recalc.py（动态）
```

## 编辑已有文件的工具脚本

### 添加列（带公式、样式自动复制）
```bash
python scripts/xlsx_unpack.py input.xlsx /tmp/xlsx_work/
python scripts/xlsx_add_column.py /tmp/xlsx_work/ --col G \
    --sheet "Sheet1" --header "占比" \
    --formula '=F{row}/$F$10' --formula-rows 2:9 \
    --total-row 10 --total-formula '=SUM(G2:G9)' --numfmt '0.0%'
python scripts/xlsx_pack.py /tmp/xlsx_work/ output.xlsx
```

### 插入行（自动移位、更新 SUM 公式）
```bash
python scripts/xlsx_unpack.py input.xlsx /tmp/xlsx_work/
python scripts/xlsx_insert_row.py /tmp/xlsx_work/ --at 5 \
    --sheet "Sheet1" --text A=新项目 \
    --values B=3000 C=3000 --formula 'D=SUM(B{row}:C{row})'
python scripts/xlsx_pack.py /tmp/xlsx_work/ output.xlsx
```

## 参考文档索引

| 需求 | 文件 |
|------|------|
| 读取分析数据 | [read-analyze.md](references/read-analyze.md) |
| 编辑 SOP | [edit_sop.md](references/edit_sop.md) |
| 编辑 XML 模式 | [edit_patterns.md](references/edit_patterns.md) |
| 编辑高级操作 | [edit_advanced.md](references/edit_advanced.md) |
| 编辑规则 | [edit_rules.md](references/edit_rules.md) |
| 修复公式 | [fix.md](references/fix.md) |
| 财务格式标准 | [format_standards.md](references/format_standards.md) |
| styles.xml 操作 | [format_styles.md](references/format_styles.md) |
| 公式验证架构 | [validate.md](references/validate.md) |
| 验证检查详情 | [validate_checks.md](references/validate_checks.md) |
