---
name: xlsx-toolkit
description: >
  Full spreadsheet automation inside AI. Create, edit, analyze, and visualize Excel files, Google Sheets, and CSVs — formulas, formatting, recalculation, charts, pivots, and data insights. Trigger when working with any spreadsheet file (.xlsx, .xlsm, .csv, .tsv), doing spreadsheet automation, data analysis, formula creation, formatting, charting, pivots, or Google Sheets operations.
  Purpose: Comprehensive in-chat spreadsheet work — no external tools or manual file
  juggling, from raw CSV reads to formatted workbooks with formulas, pivot tables,
  and charts. When to trigger: (1) Any spreadsheet operation: "read Excel", "parse CSV",
  "edit spreadsheet", "workbook". (2) Formula work: "add SUM", "create VLOOKUP", "build
  a formula". (3) Formatting: "style cells", "bold headers", "freeze panes". (4) Data
  analysis: "analyze data", "pivot table", "filter", "sort". (5) Visualization: "add
  chart", "create graph", "sparkline". (6) Google Sheets: "export to Sheets". (7) Data
  ops: "merge files", "split data", "clean data". Key capabilities: Excel functions
  (SUM, VLOOKUP, INDEX/MATCH, IF/IFS, SUMIF, COUNTIF). Array formulas, conditional
  formatting, charts (bar, line, pie, scatter). Pivot tables, named ranges, cross-sheet
  refs. Data profiling (nulls, duplicates, outliers). Also for: Data export pipelines,
  recurring reports, CSV-to-XLSX converters. Ideal for: Analysts and developers who
  need spreadsheet automation without leaving their AI workflow.
---

# XLSX Toolkit Skill

## Overview

This skill provides comprehensive spreadsheet automation capabilities for working with Excel files (.xlsx, .xlsm), CSV/TSV files, and Google Sheets. It handles creation, editing, analysis, visualization, formulas, formatting, and data insights.

## Trigger Conditions

**ALWAYS USE THIS SKILL when user mentions:**
- Any spreadsheet file operation: "read Excel", "parse CSV", "edit spreadsheet"
- Formula work: "add formula", "create SUM", "Excel functions"
- Formatting: "style cells", "bold headers", "freeze panes"
- Analysis: "analyze data", "pivot table", "filter data", "sort"
- Visualization: "add chart", "create graph", "pivot chart"
- Data operations: "merge files", "split data", "clean data"
- Google Sheets: "Google Sheets", "Sheets export", "import to Sheets"
- Any of: xlsx, xlsm, csv, tsv, spreadsheet, workbook, worksheet, cell, range, column, row

## Core Capabilities

### 1. File Operations
- **Read**: Open and parse .xlsx, .xlsm, .csv, .tsv files
- **Create**: Generate new workbooks from scratch
- **Edit**: Modify existing cells, sheets, formatting
- **Save**: Export to any supported format
- **Convert**: Transform between Excel, CSV, JSON, HTML

### 2. Data Operations
- Read/write cell values and ranges
- Insert/delete rows and columns
- Merge/split cells
- Find and replace
- Data validation (dropdowns, rules)
- Auto-filter and advanced filtering
- Sort by single or multiple columns
- Remove duplicates
- Fill down/series

### 3. Formula Engine
- All Excel functions: SUM, AVERAGE, COUNT, VLOOKUP, HLOOKUP, INDEX, MATCH, IF, IFS, SUMIF, COUNTIF, etc.
- Array formulas and dynamic arrays
- Formula auditing (trace precedents/dependents)
- Circular reference detection
- Custom named ranges

### 4. Formatting
- Cell styles: font, size, color, bold, italic, underline
- Fill colors and gradients
- Borders (all styles)
- Number formats (currency, date, percentage, custom)
- Alignment (horizontal, vertical, wrap text, merge)
- Conditional formatting rules
- Cell protection/lock

### 5. Visualization
- Charts: Column, Bar, Line, Pie, Area, Scatter, Stock, Radar
- Sparklines
- Pivot tables
- Pivot charts
- Chart formatting and styling

### 6. Multi-Sheet Operations
- Create/rename/delete sheets
- Copy/move sheets
- Sheet protection
- Cross-sheet references
- Consolidate data from multiple sheets

### 7. Data Analysis
- Statistical analysis (sum, average, median, std dev, etc.)
- Data profiling (nulls, duplicates, outliers)
- Correlation and basic analysis
- Grouping and subtotals
- What-if analysis support

### 8. Google Sheets Integration
- Export to Google Sheets format
- Handle Google Sheets-specific functions
- Preserve sharing permissions note

## Implementation Patterns

### Reading a File
```python
from openpyxl import load_workbook
import pandas as pd

# Method 1: Using openpyxl for exact cell control
wb = load_workbook('file.xlsx')
ws = wb.active
value = ws['A1'].value

# Method 2: Using pandas for data analysis
df = pd.read_excel('file.xlsx', sheet_name='Sheet1')
df = pd.read_csv('file.csv')
```

### Writing/Editing
```python
from openpyxl import Workbook, load_workbook

# Create new file
wb = Workbook()
ws = wb.active
ws['A1'] = 'Hello'
wb.save('new.xlsx')

# Edit existing
wb = load_workbook('file.xlsx')
ws = wb.active
ws['A1'] = 'Updated'
wb.save('file.xlsx')
```

### Formulas
```python
ws['A3'] = '=SUM(A1:A2)'
ws['B1'] = '=VLOOKUP(D1, Sheet2!A:B, 2, FALSE)'
# Force recalculation on open
wb.calculation.calcMode = 'auto'
```

### Formatting
```python
from openpyxl.styles import Font, PatternFill, Alignment, Border
from openpyxl.styles.numbers import FORMAT_NUMBER_COMMA_SEPARATED1

# Style a header row
header_font = Font(bold=True, color='FFFFFF')
header_fill = PatternFill(start_color='366092', end_color='366092', fill_type='solid')
for cell in ws[1]:
    cell.font = header_font
    cell.fill = header_fill
    cell.alignment = Alignment(horizontal='center')

# Number format
ws['A1'].number_format = FORMAT_NUMBER_COMMA_SEPARATED1
ws['B1'].number_format = 'YYYY-MM-DD'
```

### Charts
```python
from openpyxl.chart import BarChart, Reference

chart = BarChart()
data = Reference(ws, min_col=2, min_row=1, max_row=10, max_col=3)
cats = Reference(ws, min_col=1, min_row=2, max_row=10)
chart.add_data(data, titles_from_data=True)
chart.set_categories(cats)
ws.add_chart(chart, 'E1')
```

### Conditional Formatting
```python
from openpyxl.formatting.rule import ColorScaleRule, FormulaRule

# Color scale
ws.conditional_formatting.add('A1:A10',
    ColorScaleRule(start_type='min', start_color='F8696B',
                   mid_type='percentile', mid_value=50, mid_color='FFEB84',
                   end_type='max', end_color='63BE7B'))

# Formula-based
ws.conditional_formatting.add('B2:B100',
    FormulaRule(formula=['$B2>1000'], fill=PatternFill(start_color='FFC7CE', fill_type='solid')))
```

### Pivot Tables
```python
from openpyxl.pivot import PivotTable, PivotField

# Note: openpyxl has limited pivot support
# For complex pivots, consider using xlsxwriter or pandas
```

## Libraries to Use

| Task | Library | Install |
|------|---------|---------|
| Excel read/write | `openpyxl` | `pip install openpyxl` |
| Advanced Excel | `xlsxwriter` | `pip install xlsxwriter` |
| Data analysis | `pandas` | `pip install pandas` |
| CSV/TSV | `csv` (stdlib) | - |
| Google Sheets | `gspread`, `pygsheets` | `pip install gspread` |
| PDF exports | `reportlab`, `fpdf` | `pip install reportlab` |

## Quality Standards

- **Always verify**: After any write operation, re-open and confirm data
- **Preserve formatting**: Never lose existing styling when editing
- **Handle errors gracefully**: Missing sheets, invalid formulas, encoding issues
- **Large files**: Use iter_chunks() for files >100MB
- **Backup**: Always create backup before major modifications

## Common Patterns

### Error Handling
```python
try:
    wb = load_workbook('file.xlsx')
except FileNotFoundError:
    # Handle missing file
    pass
except Exception as e:
    # Log error, provide fallback
    pass
```

### Safe Cell Access
```python
value = ws.cell(row=1, column=1).value  # Safer than ws['A1']
if value is None:
    value = ''  # or default
```

### Performance
```python
# Disable calculation temporarily
wb.calculation.calcMode = 'manual'
# ... make changes ...
wb.calculation.calcMode = 'auto'
```

## User Communication

When working with spreadsheets:
1. Always confirm the file path and format
2. Report what was changed (cells, sheets, formulas)
3. Show preview of data when relevant
4. Warn about any data loss or formatting changes
5. Offer to save in multiple formats if useful

## Example Commands to Handle

- "Create an Excel file with sales data"
- "Add a SUM formula to column E"
- "Make row 1 bold with blue background"
- "Create a bar chart from this data"
- "Read the CSV and show me the columns"
- "Add conditional formatting to highlight duplicates"
- "Create a pivot table from this sheet"
- "Freeze the first row"
- "Export this to CSV"
- "Add data validation dropdown to cell B2"
