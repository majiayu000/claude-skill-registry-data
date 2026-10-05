---
name: xlsx-generation
description: Excel spreadsheet generation and manipulation expertise for creating, reading, and automating XLSX files programmatically. Use when building report.
---

# XLSX Generation

Structured guidance for generating, reading, and manipulating Excel XLSX files programmatically. Covers library selection, cell formatting, formulas, charts, advanced workbook features, and data pipeline integration across Python, JavaScript, and Java ecosystems.

## When to Use This Skill

Use this skill for:

- Building automated report generators that output styled Excel workbooks
- Creating data export pipelines that produce XLSX files from databases or APIs
- Generating financial models, budgets, or forecasts as spreadsheets
- Formatting business dashboards with conditional formatting, charts, and pivot-ready data
- Converting DataFrame analysis results into multi-sheet Excel deliverables
- Integrating spreadsheet output into ETL or CI/CD workflows
- Reading and transforming existing Excel files (extract data, update cells, merge workbooks)
- Producing Excel templates with data validation, dropdowns, and protected ranges

**Trigger phrases**: "xlsx", "Excel generation", "spreadsheet", "openpyxl", "xlsxwriter", "ExcelJS", "Apache POI", "Excel report", "data export", "Excel automation", "workbook", "worksheet", "cell formatting", "Excel chart", "pivot table", "Excel formula", "DataFrame to Excel", "spreadsheet pipeline"

## What This Skill Does

Provides Excel generation patterns including:

- **Library Selection**: Decision matrix for openpyxl, xlsxwriter, ExcelJS, Apache POI, and Pandas wrappers
- **Cell Formatting**: Fonts, fills, borders, alignment, number formats, merged cells, rich text
- **Formulas**: Cell references, named ranges, array formulas, cross-sheet formulas, formula auditing
- **Charts**: Bar, line, pie, scatter, combo charts with programmatic configuration and positioning
- **Data Validation**: Dropdown lists, numeric ranges, date constraints, custom formula validators
- **Advanced Features**: Autofilters, freeze panes, print setup, protection, VBA preservation, images
- **Pandas Integration**: DataFrame export, multi-sheet workbooks, Styler formatting, read/transform/write
- **Performance**: Streaming writes for large datasets, memory optimization, batch operations

## Instructions

### Step 1: Library Selection

Choosing the right library depends on whether you need read/write access, write-only performance, language ecosystem, and specific feature requirements.

**Decision Matrix**:

| Feature | openpyxl (Python) | xlsxwriter (Python) | ExcelJS (Node.js) | Apache POI (Java) | Pandas to_excel |
|---------|-------------------|---------------------|--------------------|--------------------|-----------------|
| Read XLSX | Yes | No | Yes | Yes | Yes (via openpyxl) |
| Write XLSX | Yes | Yes | Yes | Yes | Yes (via openpyxl/xlsxwriter) |
| Modify existing | Yes | No | Yes | Yes | No |
| Streaming write | Yes (write-only mode) | Yes (default) | Yes | Yes (SXSSF) | No |
| Formulas | Yes | Yes | Yes | Yes | Limited |
| Charts | Yes | Yes | Yes | Yes | No |
| Conditional formatting | Yes | Yes | Yes | Yes | Via Styler |
| VBA macro support | Yes (preserve) | Yes (xlsm) | No | Yes | No |
| Images | Yes | Yes | Yes | Yes | No |
| Memory efficiency | Moderate | High | Moderate | Low (HSSF) / High (SXSSF) | Low |
| Max rows | 1,048,576 | 1,048,576 | 1,048,576 | 1,048,576 | 1,048,576 |
| Install | `pip install openpyxl` | `pip install xlsxwriter` | `npm i exceljs` | Maven/Gradle | `pip install pandas openpyxl` |

**When to Use Each Library**:

- **openpyxl**: Default choice for Python when you need both read and write, or must modify existing files. Best for template-based report generation where you load a template and fill in data
- **xlsxwriter**: Best for Python write-only scenarios requiring maximum performance and feature richness (conditional formatting, sparklines, data validation). Cannot read or modify existing files
- **ExcelJS**: The standard choice for Node.js/TypeScript projects. Supports read, write, and streaming. Good feature coverage for most business requirements
- **Apache POI**: The Java ecosystem standard. Use XSSF for full-featured access or SXSSF for streaming large datasets. Heaviest memory footprint but most mature library
- **Pandas to_excel**: Best when your data is already in DataFrames. Not a standalone Excel library; delegates to openpyxl or xlsxwriter under the hood. Use for quick exports; switch to the underlying library when you need formatting control

**Installation and Setup**:

```python
# Python: openpyxl (read/write)
pip install openpyxl

# Python: xlsxwriter (write-only, high performance)
pip install xlsxwriter

# Python: Pandas with Excel support
pip install pandas openpyxl  # or pandas xlsxwriter
```

```bash
# Node.js: ExcelJS
npm install exceljs
```

```xml
<!-- Java: Apache POI (Maven) -->
<dependency>
    <groupId>org.apache.poi</groupId>
    <artifactId>poi-ooxml</artifactId>
    <version>5.2.5</version>
</dependency>
```

**Choosing Based on Use Case**:

```
Need to read existing XLSX?
  ├─ Yes → openpyxl (Python), ExcelJS (Node), POI (Java)
  └─ No → Write-only?
       ├─ Yes, large dataset → xlsxwriter (Python), SXSSF (Java)
       ├─ Yes, data already in DataFrame → pandas.to_excel
       └─ Yes, Node.js project → ExcelJS

Need to preserve VBA macros?
  ├─ Yes → openpyxl (keep_vba=True), POI
  └─ No → Any library

Need charts + conditional formatting + data validation?
  ├─ Yes → xlsxwriter (Python), POI (Java), ExcelJS (Node)
  └─ Basic formatting only → Any library
```

### Step 2: Python openpyxl Fundamentals

openpyxl is the most versatile Python library for Excel manipulation. It supports reading, writing, and modifying XLSX files with full formatting control.

**Workbook and Worksheet Basics**:

```python
from openpyxl import Workbook, load_workbook
from openpyxl.utils import get_column_letter

# Create a new workbook
wb = Workbook()
ws = wb.active  # Get the default sheet
ws.title = "Sales Report"

# Add additional sheets
ws2 = wb.create_sheet("Summary")
ws3 = wb.create_sheet("Raw Data", 0)  # Insert at position 0

# Write data to cells
ws["A1"] = "Product"
ws["B1"] = "Revenue"
ws["C1"] = "Quarter"

# Write by row and column index (1-based)
ws.cell(row=2, column=1, value="Widget A")
ws.cell(row=2, column=2, value=15000.50)
ws.cell(row=2, column=3, value="Q1 2026")

# Write rows in bulk
data = [
    ["Widget B", 22000.75, "Q1 2026"],
    ["Widget C", 8500.00, "Q1 2026"],
    ["Widget D", 31200.25, "Q1 2026"],
]
for row in data:
    ws.append(row)

# Set column widths
ws.column_dimensions["A"].width = 20
ws.column_dimensions["B"].width = 15
ws.column_dimensions["C"].width = 12

# Set row height
ws.row_dimensions[1].height = 25

# Save the workbook
wb.save("sales_report.xlsx")
```

**Cell Data Types and Number Formats**:

```python
from openpyxl import Workbook
from openpyxl.utils import get_column_letter
from datetime import datetime, date
from decimal import Decimal

wb = Workbook()
ws = wb.active

# String values
ws["A1"] = "Revenue Report"

# Numeric values (integers and floats)
ws["A2"] = 42
ws["B2"] = 3.14159
ws["C2"] = Decimal("15000.50")  # Converted to float internally

# Date and datetime values
ws["A3"] = date(2026, 3, 15)
ws["A3"].number_format = "YYYY-MM-DD"

ws["B3"] = datetime(2026, 3, 15, 14, 30, 0)
ws["B3"].number_format = "YYYY-MM-DD HH:MM:SS"

# Currency formatting
ws["A4"] = 15000.50
ws["A4"].number_format = '"$"#,##0.00'

# Percentage formatting
ws["B4"] = 0.1575
ws["B4"].number_format = "0.00%"

# Accounting format (negative in parentheses)
ws["C4"] = -5000.00
ws["C4"].number_format = '_("$"* #,##0.00_);_("$"* (#,##0.00);_("$"* "-"??_);_(@_)'

# Custom number formats
ws["A5"] = 1234567
ws["A5"].number_format = "#,##0"  # Thousands separator

ws["B5"] = 0.5
ws["B5"].number_format = "0.0%"

# Boolean values
ws["A6"] = True  # Displays as TRUE in Excel

wb.save("data_types.xlsx")
```

**Cell Styling (Fonts, Fills, Borders, Alignment)**:

```python
from openpyxl import Workbook
from openpyxl.styles import (
    Font, PatternFill, Border, Side, Alignment, NamedStyle
)

wb = Workbook()
ws = wb.active

# Font styling
header_font = Font(
    name="Calibri",
    size=14,
    bold=True,
    italic=False,
    color="FFFFFF",  # White text
)

body_font = Font(name="Calibri", size=11, color="333333")

# Fill (background color)
header_fill = PatternFill(
    start_color="2F5496",  # Dark blue
    end_color="2F5496",
    fill_type="solid",
)

alternating_fill = PatternFill(
    start_color="D6E4F0",  # Light blue
    end_color="D6E4F0",
    fill_type="solid",
)

# Borders
thin_border = Border(
    left=Side(style="thin", color="999999"),
    right=Side(style="thin", color="999999"),
    top=Side(style="thin", color="999999"),
    bottom=Side(style="thin", color="999999"),
)

header_border = Border(
    bottom=Side(style="medium", color="2F5496"),
)

# Alignment
center_align = Alignment(
    horizontal="center",
    vertical="center",
    wrap_text=True,
)

# Apply styles to header row
headers = ["Product", "Revenue", "Cost", "Profit", "Margin"]
for col_idx, header in enumerate(headers, 1):
    cell = ws.cell(row=1, column=col_idx, value=header)
    cell.font = header_font
    cell.fill = header_fill
    cell.border = thin_border
    cell.alignment = center_align

# Apply alternating row colors
data_rows = [
    ["Widget A", 15000, 8000, 7000, 0.4667],
    ["Widget B", 22000, 12000, 10000, 0.4545],
    ["Widget C", 8500, 5000, 3500, 0.4118],
    ["Widget D", 31200, 18000, 13200, 0.4231],
]

for row_idx, row_data in enumerate(data_rows, 2):
    for col_idx, value in enumerate(row_data, 1):
        cell = ws.cell(row=row_idx, column=col_idx, value=value)
        cell.font = body_font
        cell.border = thin_border
        if row_idx % 2 == 0:
            cell.fill = alternating_fill
        # Format currency columns
        if col_idx in (2, 3, 4):
            cell.number_format = '"$"#,##0'
        # Format percentage column
        if col_idx == 5:
            cell.number_format = "0.0%"

wb.save("styled_report.xlsx")
```

**Named Styles for Reuse**:

```python
from openpyxl import Workbook
from openpyxl.styles import NamedStyle, Font, PatternFill, Border, Side, Alignment

wb = Workbook()

# Define reusable named styles
header_style = NamedStyle(name="header_style")
header_style.font = Font(bold=True, size=12, color="FFFFFF")
header_style.fill = PatternFill(start_color="2F5496", fill_type="solid")
header_style.alignment = Alignment(horizontal="center", vertical="center")
header_style.border = Border(
    bottom=Side(style="medium", color="1F3864")
)
wb.add_named_style(header_style)

currency_style = NamedStyle(name="currency_style")
currency_style.number_format = '"$"#,##0.00'
currency_style.font = Font(size=11)
currency_style.alignment = Alignment(horizontal="right")
wb.add_named_style(currency_style)

# Apply named styles by name
ws = wb.active
ws["A1"].style = "header_style"
ws["A1"].value = "Amount"
ws["A2"].style = "currency_style"
ws["A2"].value = 15000.50

wb.save("named_styles.xlsx")
```

**Merged Cells**:

```python
from openpyxl import Workbook
from openpyxl.styles import Font, Alignment

wb = Workbook()
ws = wb.active

# Merge cells for a title row
ws.merge_cells("A1:E1")
ws["A1"] = "Quarterly Sales Report - Q1 2026"
ws["A1"].font = Font(size=16, bold=True)
ws["A1"].alignment = Alignment(horizontal="center")

# Merge cells for section headers
ws.merge_cells("A3:B3")
ws["A3"] = "Product Details"
ws["A3"].font = Font(bold=True)

ws.merge_cells("C3:E3")
ws["C3"] = "Financial Metrics"
ws["C3"].font = Font(bold=True)

# Unmerge if needed
# ws.unmerge_cells("A1:E1")

wb.save("merged_cells.xlsx")
```

**Loading and Modifying Existing Files**:

```python
from openpyxl import load_workbook

# Load an existing workbook
wb = load_workbook("template.xlsx")
ws = wb.active

# Read cell values
value = ws["A1"].value
print(f"Cell A1: {value}")

# Iterate over rows
for row in ws.iter_rows(min_row=2, max_col=5, values_only=True):
    product, revenue, cost, profit, margin = row
    print(f"{product}: ${revenue}")

# Modify cells
ws["F1"] = "Status"
for row_idx in range(2, ws.max_row + 1):
    profit = ws.cell(row=row_idx, column=4).value
    if profit and profit > 10000:
        ws.cell(row=row_idx, column=6, value="High")
    else:
        ws.cell(row=row_idx, column=6, value="Standard")

# Load with data_only to get calculated values instead of formulas
wb_values = load_workbook("report_with_formulas.xlsx", data_only=True)
# Note: data_only returns the cached value from the last Excel save,
# not a recalculated value. If the file was never opened in Excel,
# formula cells will return None.

wb.save("template_updated.xlsx")
```

### Step 3: Python xlsxwriter

xlsxwriter is a write-only library optimized for performance and feature richness. It produces XLSX files without needing to read existing ones, making it ideal for report generation pipelines.

**Basic Setup and Formatting**:

```python
import xlsxwriter

wb = xlsxwriter.Workbook("report.xlsx")
ws = wb.add_worksheet("Sales")

# Define reusable formats
header_fmt = wb.add_format({
    "bold": True,
    "font_size": 12,
    "font_color": "#FFFFFF",
    "bg_color": "#2F5496",
    "border": 1,
    "align": "center",
    "valign": "vcenter",
    "text_wrap": True,
})

currency_fmt = wb.add_format({
    "num_format": "$#,##0.00",
    "font_size": 11,
    "border": 1,
})

percent_fmt = wb.add_format({
    "num_format": "0.0%",
    "font_size": 11,
    "border": 1,
})

date_fmt = wb.add_format({
    "num_format": "yyyy-mm-dd",
    "border": 1,
})

# Write header row
headers = ["Product", "Revenue", "Cost", "Profit", "Margin", "Date"]
for col, header in enumerate(headers):
    ws.write(0, col, header, header_fmt)

# Write data rows
data = [
    ["Widget A", 15000.50, 8000, 7000.50, 0.4667, "2026-03-15"],
    ["Widget B", 22000.75, 12000, 10000.75, 0.4545, "2026-03-16"],
    ["Widget C", 8500.00, 5000, 3500.00, 0.4118, "2026-03-17"],
]

for row_idx, row_data in enumerate(data, 1):
    ws.write(row_idx, 0, row_data[0])             # String
    ws.write(row_idx, 1, row_data[1], currency_fmt) # Currency
    ws.write(row_idx, 2, row_data[2], currency_fmt) # Currency
    ws.write(row_idx, 3, row_data[3], currency_fmt) # Currency
    ws.write(row_idx, 4, row_data[4], percent_fmt)  # Percentage
    ws.write(row_idx, 5, row_data[5], date_fmt)     # Date

# Set column widths
ws.set_column("A:A", 20)
ws.set_column("B:D", 15)
ws.set_column("E:E", 10)
ws.set_column("F:F", 14)

# Set row heights
ws.set_row(0, 25)

wb.close()  # xlsxwriter uses close(), not save()
```

**Conditional Formatting**:

```python
import xlsxwriter

wb = xlsxwriter.Workbook("conditional.xlsx")
ws = wb.add_worksheet()

# Write sample data
headers = ["Product", "Revenue", "Target", "Variance"]
for col, h in enumerate(headers):
    ws.write(0, col, h)

data = [
    ["Widget A", 15000, 12000, 3000],
    ["Widget B", 8000, 12000, -4000],
    ["Widget C", 22000, 12000, 10000],
    ["Widget D", 11000, 12000, -1000],
]
for r, row in enumerate(data, 1):
    for c, val in enumerate(row):
        ws.write(r, c, val)

# Color scale: green (high) to red (low) on revenue column
ws.conditional_format("B2:B5", {
    "type": "3_color_scale",
    "min_color": "#F8696B",   # Red
    "mid_color": "#FFEB84",   # Yellow
    "max_color": "#63BE7B",   # Green
})

# Data bar on revenue column
ws.conditional_format("B2:B5", {
    "type": "data_bar",
    "bar_color": "#2F5496",
})

# Icon set on variance column
ws.conditional_format("D2:D5", {
    "type": "icon_set",
    "icon_style": "3_traffic_lights",
    "icons": [
        {"criteria": ">=", "type": "number", "value": 5000},
        {"criteria": ">=", "type": "number", "value": 0},
        {"criteria": "<",  "type": "number", "value": 0},
    ],
})

# Cell-based conditional format: highlight negative variance in red
red_fmt = wb.add_format({"bg_color": "#FFC7CE", "font_color": "#9C0006"})
ws.conditional_format("D2:D5", {
    "type": "cell",
    "criteria": "<",
    "value": 0,
    "format": red_fmt,
})

# Highlight cells above average
green_fmt = wb.add_format({"bg_color": "#C6EFCE", "font_color": "#006100"})
ws.conditional_format("B2:B5", {
    "type": "average",
    "criteria": "above",
    "format": green_fmt,
})

# Formula-based: highlight entire row where variance is negative
row_red_fmt = wb.add_format({"bg_color": "#FFC7CE"})
ws.conditional_format("A2:D5", {
    "type": "formula",
    "criteria": "=$D2<0",
    "format": row_red_fmt,
})

wb.close()
```

**Data Validation**:

```python
import xlsxwriter

wb = xlsxwriter.Workbook("validation.xlsx")
ws = wb.add_worksheet()

# Dropdown list validation
ws.write("A1", "Status")
ws.data_validation("A2:A100", {
    "validate": "list",
    "source": ["Active", "Inactive", "Pending", "Archived"],
    "input_title": "Select Status",
    "input_message": "Choose a status from the dropdown.",
    "error_title": "Invalid Status",
    "error_message": "Please select a valid status from the list.",
})

# Numeric range validation
ws.write("B1", "Quantity")
ws.data_validation("B2:B100", {
    "validate": "integer",
    "criteria": "between",
    "minimum": 1,
    "maximum": 10000,
    "input_title": "Enter Quantity",
    "input_message": "Quantity must be between 1 and 10,000.",
    "error_type": "stop",
})

# Date range validation
ws.write("C1", "Due Date")
ws.data_validation("C2:C100", {
    "validate": "date",
    "criteria": ">=",
    "value": "2026-01-01",
    "input_title": "Enter Date",
    "input_message": "Date must be on or after 2026-01-01.",
})

# Custom formula validation (value must be unique in column)
ws.write("D1", "Code")
ws.data_validation("D2:D100", {
    "validate": "custom",
    "value": "=COUNTIF($D:$D,D2)<=1",
    "input_title": "Unique Code",
    "input_message": "Enter a unique product code.",
    "error_title": "Duplicate",
    "error_message": "This code already exists in the column.",
})

wb.close()
```

**Sparklines**:

```python
import xlsxwriter

wb = xlsxwriter.Workbook("sparklines.xlsx")
ws = wb.add_worksheet()

# Monthly revenue data
ws.write_row("A1", ["Product", "Jan", "Feb", "Mar", "Apr", "May", "Jun", "Trend"])
ws.write_row("A2", ["Widget A", 100, 120, 115, 140, 155, 170])
ws.write_row("A3", ["Widget B", 200, 190, 210, 195, 220, 240])
ws.write_row("A4", ["Widget C", 50, 60, 55, 70, 65, 80])

# Add sparklines in the Trend column
ws.add_sparkline("H2", {
    "range": "B2:G2",
    "type": "line",
    "markers": True,
    "high_point": True,
    "low_point": True,
})

ws.add_sparkline("H3", {
    "range": "B3:G3",
    "type": "column",
    "high_point": True,
})

ws.add_sparkline("H4", {
    "range": "B4:G4",
    "type": "win_loss",
})

ws.set_column("H:H", 20)
wb.close()
```

**Memory-Optimized Writing for Large Datasets**:

```python
import xlsxwriter

# Enable constant_memory mode for large datasets
# Rows are flushed to disk and cannot be revisited
wb = xlsxwriter.Workbook("large_dataset.xlsx", {"constant_memory": True})
ws = wb.add_worksheet()

header_fmt = wb.add_format({"bold": True, "bg_color": "#2F5496", "font_color": "#FFFFFF"})

headers = ["ID", "Name", "Value", "Category", "Timestamp"]
for col, h in enumerate(headers):
    ws.write(0, col, h, header_fmt)

# Write 1 million rows efficiently
for row in range(1, 1_000_001):
    ws.write_number(row, 0, row)
    ws.write_string(row, 1, f"Item {row}")
    ws.write_number(row, 2, row * 1.5)
    ws.write_string(row, 3, f"Cat-{row % 10}")
    ws.write_string(row, 4, "2026-03-15T10:30:00")

wb.close()
```

### Step 4: JavaScript ExcelJS

ExcelJS is the standard library for Excel generation in Node.js and TypeScript projects. It supports reading, writing, and streaming with comprehensive formatting options.

**Basic Workbook Creation**:

```javascript
const ExcelJS = require("exceljs");

async function createReport() {
  const wb = new ExcelJS.Workbook();
  wb.creator = "Report Generator";
  wb.created = new Date();

  const ws = wb.addWorksheet("Sales Report", {
    properties: { tabColor: { argb: "2F5496" } },
    pageSetup: {
      paperSize: 9, // A4
      orientation: "landscape",
      fitToPage: true,
    },
  });

  // Define columns with headers, keys, and widths
  ws.columns = [
    { header: "Product", key: "product", width: 25 },
    { header: "Revenue", key: "revenue", width: 15, style: { numFmt: "$#,##0.00" } },
    { header: "Cost", key: "cost", width: 15, style: { numFmt: "$#,##0.00" } },
    { header: "Profit", key: "profit", width: 15, style: { numFmt: "$#,##0.00" } },
    { header: "Margin", key: "margin", width: 12, style: { numFmt: "0.0%" } },
  ];

  // Add rows using key-value objects
  ws.addRow({ product: "Widget A", revenue: 15000.50, cost: 8000, profit: 7000.50, margin: 0.4667 });
  ws.addRow({ product: "Widget B", revenue: 22000.75, cost: 12000, profit: 10000.75, margin: 0.4545 });
  ws.addRow({ product: "Widget C", revenue: 8500.00, cost: 5000, profit: 3500.00, margin: 0.4118 });

  // Style the header row
  const headerRow = ws.getRow(1);
  headerRow.eachCell((cell) => {
    cell.font = { bold: true, size: 12, color: { argb: "FFFFFFFF" } };
    cell.fill = {
      type: "pattern",
      pattern: "solid",
      fgColor: { argb: "FF2F5496" },
    };
    cell.alignment = { horizontal: "center", vertical: "middle" };
    cell.border = {
      bottom: { style: "medium", color: { argb: "FF1F3864" } },
    };
  });
  headerRow.height = 25;

  await wb.xlsx.writeFile("sales_report.xlsx");
}

createReport();
```

**Cell Styling and Rich Text**:

```javascript
const ExcelJS = require("exceljs");

async function styledWorkbook() {
  const wb = new ExcelJS.Workbook();
  const ws = wb.addWorksheet("Styled");

  // Rich text in a single cell
  ws.getCell("A1").value = {
    richText: [
      { font: { bold: true, size: 14, color: { argb: "FF2F5496" } }, text: "Q1 2026 " },
      { font: { italic: true, size: 14, color: { argb: "FF666666" } }, text: "Sales Report" },
    ],
  };

  // Conditional fill based on value
  const data = [
    { name: "Widget A", value: 15000 },
    { name: "Widget B", value: -3000 },
    { name: "Widget C", value: 22000 },
  ];

  data.forEach((item, idx) => {
    const row = idx + 3;
    ws.getCell(`A${row}`).value = item.name;
    const valueCell = ws.getCell(`B${row}`);
    valueCell.value = item.value;
    valueCell.numFmt = "$#,##0.00";

    if (item.value < 0) {
      valueCell.font = { color: { argb: "FF9C0006" } };
      valueCell.fill = {
        type: "pattern",
        pattern: "solid",
        fgColor: { argb: "FFFFC7CE" },
      };
    } else {
      valueCell.font = { color: { argb: "FF006100" } };
      valueCell.fill = {
        type: "pattern",
        pattern: "solid",
        fgColor: { argb: "FFC6EFCE" },
      };
    }
  });

  // Data validation dropdown
  ws.getCell("C3").dataValidation = {
    type: "list",
    allowBlank: true,
    formulae: ['"Active,Inactive,Pending"'],
    showErrorMessage: true,
    errorTitle: "Invalid",
    error: "Select a valid status.",
  };

  await wb.xlsx.writeFile("styled.xlsx");
}

styledWorkbook();
```

**Streaming Writes for Large Datasets**:

```javascript
const ExcelJS = require("exceljs");
const fs = require("fs");

async function streamLargeDataset() {
  const options = {
    filename: "large_dataset.xlsx",
    useStyles: true,
    useSharedStrings: false, // Disable for better performance
  };

  const wb = new ExcelJS.stream.xlsx.WorkbookWriter(options);
  const ws = wb.addWorksheet("Data");

  // Define columns
  ws.columns = [
    { header: "ID", key: "id", width: 10 },
    { header: "Name", key: "name", width: 25 },
    { header: "Value", key: "value", width: 15 },
    { header: "Category", key: "category", width: 15 },
  ];

  // Stream 500,000 rows without holding them all in memory
  for (let i = 1; i <= 500_000; i++) {
    ws.addRow({
      id: i,
      name: `Item ${i}`,
      value: Math.round(Math.random() * 10000) / 100,
      category: `Cat-${i % 10}`,
    }).commit(); // Flush row to disk immediately
  }

  ws.commit();
  await wb.commit();
}

streamLargeDataset();
```

**Adding Images**:

```javascript
const ExcelJS = require("exceljs");

async function addImages() {
  const wb = new ExcelJS.Workbook();
  const ws = wb.addWorksheet("With Image");

  // Add image from file
  const logoId = wb.addImage({
    filename: "logo.png",
    extension: "png",
  });

  // Position image over a cell range
  ws.addImage(logoId, {
    tl: { col: 0, row: 0 },       // Top-left anchor
    br: { col: 3, row: 4 },       // Bottom-right anchor
    editAs: "oneCell",             // Resize behavior
  });

  // Add image from buffer
  const imageBuffer = fs.readFileSync("chart_screenshot.png");
  const chartId = wb.addImage({
    buffer: imageBuffer,
    extension: "png",
  });

  ws.addImage(chartId, "E1:K15");  // Shorthand range notation

  await wb.xlsx.writeFile("with_images.xlsx");
}
```

### Step 5: Formulas and Calculations

All major XLSX libraries support embedding Excel formulas in cells. Formulas are stored as text and evaluated by Excel when the file is opened.

**Cell Formulas in openpyxl**:

```python
from openpyxl import Workbook

wb = Workbook()
ws = wb.active

# Simple formulas
ws["A1"] = "Revenue"
ws["A2"] = 15000
ws["A3"] = 22000
ws["A4"] = 8500
ws["A5"] = "=SUM(A2:A4)"            # Sum
ws["A6"] = "=AVERAGE(A2:A4)"        # Average
ws["A7"] = "=MAX(A2:A4)"            # Maximum
ws["A8"] = '=IF(A5>40000,"High","Low")'  # Conditional

# Cross-cell references
ws["B2"] = 8000   # Cost for row 2
ws["C2"] = "=A2-B2"  # Profit = Revenue - Cost
ws["D2"] = "=C2/A2"  # Margin = Profit / Revenue

# Fill formulas down a range
for row in range(2, 5):
    ws.cell(row=row, column=3).value = f"=A{row}-B{row}"
    ws.cell(row=row, column=4).value = f"=C{row}/A{row}"

# VLOOKUP and INDEX/MATCH
ws2 = wb.create_sheet("Lookup")
ws2["A1"] = "Product"
ws2["B1"] = "Category"
ws2["A2"] = "Widget A"
ws2["B2"] = "Electronics"
ws2["A3"] = "Widget B"
ws2["B3"] = "Hardware"

# Reference lookup from main sheet
ws["E2"] = "=VLOOKUP(A2,Lookup!A:B,2,FALSE)"
# Modern alternative: XLOOKUP (Excel 365+)
ws["F2"] = "=XLOOKUP(A2,Lookup!A:A,Lookup!B:B)"

wb.save("formulas.xlsx")
```

**Named Ranges**:

```python
from openpyxl import Workbook
from openpyxl.workbook.defined_name import DefinedName

wb = Workbook()
ws = wb.active
ws.title = "Data"

# Write data
ws["A1"] = "Revenue"
for row, val in enumerate([15000, 22000, 8500, 31200], 2):
    ws.cell(row=row, column=1, value=val)

# Create a named range
revenue_range = DefinedName("RevenueData", attr_text="Data!$A$2:$A$5")
wb.defined_names.add(revenue_range)

# Use the named range in formulas
ws["C1"] = "Total Revenue"
ws["C2"] = "=SUM(RevenueData)"
ws["C3"] = "Average Revenue"
ws["C4"] = "=AVERAGE(RevenueData)"

# Named range scoped to a specific sheet
local_range = DefinedName(
    "LocalTotal",
    attr_text="Data!$C$2",
    localSheetId=0,  # Sheet index
)
wb.defined_names.add(local_range)

# Print area as a named range
ws.print_area = "A1:C10"

# Print titles (repeat rows at top of each printed page)
ws.print_title_rows = "1:1"

wb.save("named_ranges.xlsx")
```

**Array Formulas and Dynamic Arrays**:

```python
from openpyxl import Workbook
from openpyxl.worksheet.formula import ArrayFormula

wb = Workbook()
ws = wb.active

# Data
ws["A1"] = "Price"
ws["B1"] = "Quantity"
ws["C1"] = "Total"
for row, (price, qty) in enumerate([(10, 5), (20, 3), (15, 8)], 2):
    ws.cell(row=row, column=1, value=price)
    ws.cell(row=row, column=2, value=qty)

# Legacy CSE array formula (Ctrl+Shift+Enter)
# Computes sum of element-wise multiplication
ws["D1"] = "Sum of Products"
ws["D2"] = ArrayFormula("D2", "=SUM(A2:A4*B2:B4)")

# Individual cell formulas (non-array, but referencing ranges)
ws["C2"] = "=A2*B2"
ws["C3"] = "=A3*B3"
ws["C4"] = "=A4*B4"

# Dynamic array formulas (Excel 365+, spill into adjacent cells)
# These work when opened in Excel; the library writes the formula to the anchor cell
ws2 = wb.create_sheet("Dynamic")
ws2["A1"] = "=SORT(Data!A2:A4)"            # Spills sorted values
ws2["C1"] = "=UNIQUE(Data!A2:A10)"          # Spills unique values
ws2["E1"] = "=FILTER(Data!A2:C4,Data!C2:C4>50)"  # Filtered results

wb.save("array_formulas.xlsx")
```

**Cross-Sheet References**:

```python
from openpyxl import Workbook

wb = Workbook()

# Create multiple sheets with data
regions = {
    "North": [10000, 12000, 15000],
    "South": [8000, 9000, 11000],
    "East": [14000, 13000, 16000],
    "West": [7000, 8500, 9500],
}

for region, values in regions.items():
    ws = wb.create_sheet(region)
    ws["A1"] = "Q1"
    ws["B1"] = "Q2"
    ws["C1"] = "Q3"
    for col, val in enumerate(values, 1):
        ws.cell(row=2, column=col, value=val)
    ws["D1"] = "Total"
    ws["D2"] = "=SUM(A2:C2)"

# Summary sheet with cross-sheet references
summary = wb.create_sheet("Summary", 0)
summary["A1"] = "Region"
summary["B1"] = "Q1"
summary["C1"] = "Q2"
summary["D1"] = "Q3"
summary["E1"] = "Total"

for row, region in enumerate(regions.keys(), 2):
    summary.cell(row=row, column=1, value=region)
    summary.cell(row=row, column=2).value = f"='{region}'!A2"
    summary.cell(row=row, column=3).value = f"='{region}'!B2"
    summary.cell(row=row, column=4).value = f"='{region}'!C2"
    summary.cell(row=row, column=5).value = f"='{region}'!D2"

# Grand total row
total_row = len(regions) + 2
summary.cell(row=total_row, column=1, value="Grand Total")
for col in range(2, 6):
    col_letter = chr(64 + col)  # B, C, D, E
    summary.cell(row=total_row, column=col).value = (
        f"=SUM({col_letter}2:{col_letter}{total_row - 1})"
    )

# Remove the default sheet
del wb["Sheet"]

wb.save("cross_sheet.xlsx")
```

**Formula Auditing and Validation**:

```python
from openpyxl import load_workbook
from openpyxl.utils import get_column_letter
import re

def audit_formulas(filepath: str) -> list[dict]:
    """Scan a workbook and report all formula cells with their references."""
    wb = load_workbook(filepath)
    findings = []

    for ws in wb.worksheets:
        for row in ws.iter_rows():
            for cell in row:
                if isinstance(cell.value, str) and cell.value.startswith("="):
                    formula = cell.value
                    # Extract cell references from the formula
                    refs = re.findall(
                        r"(?:'[^']+'\!)?\$?[A-Z]{1,3}\$?\d+(?::\$?[A-Z]{1,3}\$?\d+)?",
                        formula,
                    )
                    findings.append({
                        "sheet": ws.title,
                        "cell": cell.coordinate,
                        "formula": formula,
                        "references": refs,
                    })

    return findings

# Usage
# results = audit_formulas("complex_report.xlsx")
# for f in results:
#     print(f"{f['sheet']}!{f['cell']}: {f['formula']} -> refs: {f['references']}")
```

### Step 6: Charts and Visualization

Both openpyxl and xlsxwriter support creating Excel-native charts. Charts are embedded in the worksheet and update dynamically when the underlying data changes.

**openpyxl Charts**:

```python
from openpyxl import Workbook
from openpyxl.chart import (
    BarChart, LineChart, PieChart, ScatterChart, Reference
)
from openpyxl.chart.series import SeriesLabel
from openpyxl.chart.label import DataLabelList
from openpyxl.utils import get_column_letter

wb = Workbook()
ws = wb.active
ws.title = "Chart Data"

# Write data
headers = ["Month", "Revenue", "Cost", "Profit"]
data = [
    ["Jan", 15000, 8000, 7000],
    ["Feb", 18000, 9500, 8500],
    ["Mar", 22000, 11000, 11000],
    ["Apr", 19000, 10000, 9000],
    ["May", 25000, 12500, 12500],
    ["Jun", 28000, 14000, 14000],
]

ws.append(headers)
for row in data:
    ws.append(row)

# --- Bar Chart ---
bar_chart = BarChart()
bar_chart.type = "col"  # "col" for vertical, "bar" for horizontal
bar_chart.title = "Monthly Revenue and Cost"
bar_chart.x_axis.title = "Month"
bar_chart.y_axis.title = "Amount ($)"
bar_chart.style = 10
bar_chart.width = 20
bar_chart.height = 12

# Data references (min_col/max_col are 1-based)
categories = Reference(ws, min_col=1, min_row=2, max_row=7)  # Month labels
revenue_data = Reference(ws, min_col=2, min_row=1, max_row=7)  # Include header
cost_data = Reference(ws, min_col=3, min_row=1, max_row=7)

bar_chart.add_data(revenue_data, titles_from_data=True)
bar_chart.add_data(cost_data, titles_from_data=True)
bar_chart.set_categories(categories)

# Customize series colors
bar_chart.series[0].graphicalProperties.solidFill = "2F5496"  # Blue
bar_chart.series[1].graphicalProperties.solidFill = "C00000"  # Red

ws.add_chart(bar_chart, "F2")

# --- Line Chart ---
line_chart = LineChart()
line_chart.title = "Profit Trend"
line_chart.x_axis.title = "Month"
line_chart.y_axis.title = "Profit ($)"
line_chart.style = 10
line_chart.width = 20
line_chart.height = 12

profit_data = Reference(ws, min_col=4, min_row=1, max_row=7)
line_chart.add_data(profit_data, titles_from_data=True)
line_chart.set_categories(categories)

# Add data labels
line_chart.series[0].graphicalProperties.line.width = 25000  # EMUs
line_chart.series[0].dLbls = DataLabelList()
line_chart.series[0].dLbls.showVal = True

ws.add_chart(line_chart, "F18")

# --- Pie Chart ---
pie_ws = wb.create_sheet("Pie Chart")
pie_ws["A1"] = "Category"
pie_ws["B1"] = "Amount"
pie_data_rows = [
    ["Electronics", 45000],
    ["Hardware", 30000],
    ["Software", 25000],
    ["Services", 15000],
]
for row in pie_data_rows:
    pie_ws.append(row)

pie_chart = PieChart()
pie_chart.title = "Revenue by Category"
pie_chart.width = 18
pie_chart.height = 14

pie_labels = Reference(pie_ws, min_col=1, min_row=2, max_row=5)
pie_values = Reference(pie_ws, min_col=2, min_row=1, max_row=5)
pie_chart.add_data(pie_values, titles_from_data=True)
pie_chart.set_categories(pie_labels)

# Show percentage labels
pie_chart.series[0].dLbls = DataLabelList()
pie_chart.series[0].dLbls.showPercent = True
pie_chart.series[0].dLbls.showCatName = True
pie_chart.series[0].dLbls.showVal = False

pie_ws.add_chart(pie_chart, "D2")

# --- Scatter Chart ---
scatter_ws = wb.create_sheet("Scatter")
scatter_ws.append(["Ad Spend", "Revenue"])
scatter_data_rows = [
    [1000, 12000], [2000, 18000], [3000, 22000],
    [4000, 28000], [5000, 32000], [6000, 35000],
]
for row in scatter_data_rows:
    scatter_ws.append(row)

scatter_chart = ScatterChart()
scatter_chart.title = "Ad Spend vs Revenue"
scatter_chart.x_axis.title = "Ad Spend ($)"
scatter_chart.y_axis.title = "Revenue ($)"
scatter_chart.width = 18
scatter_chart.height = 14

x_values = Reference(scatter_ws, min_col=1, min_row=2, max_row=7)
y_values = Reference(scatter_ws, min_col=2, min_row=2, max_row=7)
series = scatter_chart.series
from openpyxl.chart import Series
s = Series(y_values, x_values, title="Revenue")
scatter_chart.series.append(s)

# Add trendline
from openpyxl.chart.trendline import Trendline
s.trendline = Trendline(trendlineType="linear", dispRSqr=True, dispEq=True)

scatter_ws.add_chart(scatter_chart, "D2")

wb.save("charts.xlsx")
```

**xlsxwriter Charts**:

```python
import xlsxwriter

wb = xlsxwriter.Workbook("xlsxwriter_charts.xlsx")
ws = wb.add_worksheet("Data")

# Write data
headers = ["Month", "Revenue", "Cost", "Profit"]
data = [
    ["Jan", 15000, 8000, 7000],
    ["Feb", 18000, 9500, 8500],
    ["Mar", 22000, 11000, 11000],
    ["Apr", 19000, 10000, 9000],
    ["May", 25000, 12500, 12500],
    ["Jun", 28000, 14000, 14000],
]

bold = wb.add_format({"bold": True})
for col, h in enumerate(headers):
    ws.write(0, col, h, bold)
for r, row in enumerate(data, 1):
    for c, val in enumerate(row):
        ws.write(r, c, val)

# --- Clustered Bar Chart ---
bar_chart = wb.add_chart({"type": "column"})

bar_chart.add_series({
    "name": "=Data!$B$1",
    "categories": "=Data!$A$2:$A$7",
    "values": "=Data!$B$2:$B$7",
    "fill": {"color": "#2F5496"},
    "gap": 150,
})
bar_chart.add_series({
    "name": "=Data!$C$1",
    "values": "=Data!$C$2:$C$7",
    "fill": {"color": "#C00000"},
})

bar_chart.set_title({"name": "Monthly Revenue and Cost"})
bar_chart.set_x_axis({"name": "Month"})
bar_chart.set_y_axis({"name": "Amount ($)", "num_format": "$#,##0"})
bar_chart.set_size({"width": 720, "height": 400})
bar_chart.set_legend({"position": "bottom"})

ws.insert_chart("F2", bar_chart)

# --- Combo Chart (Bar + Line) ---
combo_chart = wb.add_chart({"type": "column"})

combo_chart.add_series({
    "name": "Revenue",
    "categories": "=Data!$A$2:$A$7",
    "values": "=Data!$B$2:$B$7",
    "fill": {"color": "#2F5496"},
})

# Add a line series on a secondary axis
line_series = wb.add_chart({"type": "line"})
line_series.add_series({
    "name": "Profit",
    "categories": "=Data!$A$2:$A$7",
    "values": "=Data!$D$2:$D$7",
    "line": {"color": "#00B050", "width": 2.5},
    "marker": {"type": "circle", "size": 6},
    "y2_axis": True,
})

combo_chart.combine(line_series)
combo_chart.set_title({"name": "Revenue (Bars) vs Profit (Line)"})
combo_chart.set_y_axis({"name": "Revenue ($)"})
combo_chart.set_y2_axis({"name": "Profit ($)"})
combo_chart.set_size({"width": 720, "height": 400})

ws.insert_chart("F22", combo_chart)

# --- Stacked Area Chart ---
area_chart = wb.add_chart({"type": "area", "subtype": "stacked"})
area_chart.add_series({
    "name": "Cost",
    "categories": "=Data!$A$2:$A$7",
    "values": "=Data!$C$2:$C$7",
    "fill": {"color": "#FFC000"},
})
area_chart.add_series({
    "name": "Profit",
    "values": "=Data!$D$2:$D$7",
    "fill": {"color": "#00B050"},
})
area_chart.set_title({"name": "Revenue Composition"})
area_chart.set_size({"width": 720, "height": 400})

ws.insert_chart("F42", area_chart)

wb.close()
```

**Data-Driven Chart Generation Helper**:

```python
from openpyxl import Workbook
from openpyxl.chart import BarChart, LineChart, PieChart, Reference


def add_chart_from_data(
    wb: Workbook,
    sheet_name: str,
    chart_type: str,
    title: str,
    data_range: tuple[int, int, int, int],
    category_col: int,
    anchor_cell: str = "A1",
    width: int = 18,
    height: int = 12,
) -> None:
    """Add a chart to a worksheet from a data range.

    Args:
        wb: The workbook containing the data.
        sheet_name: Name of the sheet with data.
        chart_type: One of "bar", "line", "pie".
        title: Chart title.
        data_range: Tuple of (min_col, min_row, max_col, max_row) for data series.
        category_col: Column number for category labels.
        anchor_cell: Cell where the chart top-left corner is placed.
        width: Chart width in cm.
        height: Chart height in cm.
    """
    ws = wb[sheet_name]
    min_col, min_row, max_col, max_row = data_range

    chart_classes = {
        "bar": BarChart,
        "line": LineChart,
        "pie": PieChart,
    }

    chart_cls = chart_classes.get(chart_type)
    if chart_cls is None:
        raise ValueError(f"Unsupported chart type: {chart_type}. Use: {list(chart_classes.keys())}")

    chart = chart_cls()
    chart.title = title
    chart.width = width
    chart.height = height

    data_ref = Reference(ws, min_col=min_col, min_row=min_row, max_col=max_col, max_row=max_row)
    categories = Reference(ws, min_col=category_col, min_row=min_row + 1, max_row=max_row)

    chart.add_data(data_ref, titles_from_data=True)
    chart.set_categories(categories)

    target_ws = ws
    target_ws.add_chart(chart, anchor_cell)


# Usage:
# wb = Workbook()
# ws = wb.active
# ws.append(["Month", "Revenue", "Cost"])
# for row in [["Jan", 15000, 8000], ["Feb", 18000, 9500]]:
#     ws.append(row)
# add_chart_from_data(wb, ws.title, "bar", "Revenue vs Cost", (2, 1, 3, 3), 1, "E2")
# wb.save("dynamic_chart.xlsx")
```

### Step 7: Advanced Features

Production Excel files often require features beyond basic data and formatting: autofilters for interactive exploration, freeze panes for navigation, print configuration for physical output, protection for controlled access, and VBA macro preservation for existing automation.

**Autofilters**:

```python
from openpyxl import Workbook

wb = Workbook()
ws = wb.active

headers = ["Product", "Category", "Revenue", "Region", "Status"]
ws.append(headers)

data = [
    ["Widget A", "Electronics", 15000, "North", "Active"],
    ["Widget B", "Hardware", 22000, "South", "Active"],
    ["Widget C", "Software", 8500, "East", "Inactive"],
    ["Widget D", "Electronics", 31200, "West", "Active"],
    ["Widget E", "Hardware", 12000, "North", "Pending"],
]
for row in data:
    ws.append(row)

# Enable autofilter on the data range
ws.auto_filter.ref = f"A1:E{len(data) + 1}"

# Pre-apply a filter (visible when file is opened)
# Note: openpyxl sets the filter definition but Excel applies it on open
ws.auto_filter.add_filter_column(4, ["Active"])  # Column E (0-indexed: 4)
ws.auto_filter.add_sort_condition("C2:C6")       # Sort by Revenue

wb.save("autofilter.xlsx")
```

**Freeze Panes**:

```python
from openpyxl import Workbook

wb = Workbook()
ws = wb.active

# Freeze the top row (header) and first column
ws.freeze_panes = "B2"
# "B2" means: freeze everything above row 2 and left of column B
# Result: row 1 and column A stay visible when scrolling

# Other common freeze configurations:
# ws.freeze_panes = "A2"   # Freeze top row only
# ws.freeze_panes = "B1"   # Freeze first column only
# ws.freeze_panes = "C3"   # Freeze rows 1-2 and columns A-B
# ws.freeze_panes = None    # Remove freeze panes

# Write headers and data
ws.append(["ID", "Name", "Revenue", "Cost", "Profit"])
for i in range(1, 101):
    ws.append([i, f"Product {i}", i * 100, i * 60, i * 40])

wb.save("freeze_panes.xlsx")
```

**Print Setup and Page Layout**:

```python
from openpyxl import Workbook
from openpyxl.worksheet.page import PageMargins

wb = Workbook()
ws = wb.active

# Page setup
ws.page_setup.paperSize = ws.PAPERSIZE_A4
ws.page_setup.orientation = ws.ORIENTATION_LANDSCAPE
ws.page_setup.fitToWidth = 1   # Fit all columns on one page width
ws.page_setup.fitToHeight = 0  # Allow multiple pages vertically
ws.page_setup.scale = 85       # 85% scale (ignored if fitTo is set)

# Margins (in inches)
ws.page_margins = PageMargins(
    left=0.5, right=0.5,
    top=0.75, bottom=0.75,
    header=0.3, footer=0.3,
)

# Header and footer
ws.oddHeader.center.text = "Quarterly Sales Report"
ws.oddHeader.right.text = "&D"   # Current date
ws.oddFooter.center.text = "Page &P of &N"  # Page X of Y
ws.oddFooter.left.text = "Confidential"

# Print titles: repeat row 1 on every printed page
ws.print_title_rows = "1:1"
# Repeat columns A-B on every page
ws.print_title_cols = "A:B"

# Print area: only print a specific range
ws.print_area = "A1:F50"

# Page breaks
ws.page_breaks.append(openpyxl.worksheet.pagebreak.Break(id=25))  # After row 25

# Gridlines and headings
ws.sheet_properties.pageSetUpPr.fitToPage = True
ws.print_options.gridLines = True       # Print gridlines
ws.print_options.horizontalCentered = True  # Center on page

wb.save("print_setup.xlsx")
```

**Password Protection**:

```python
from openpyxl import Workbook
from openpyxl.worksheet.protection import SheetProtection

wb = Workbook()
ws = wb.active

# Write data
ws.append(["Product", "Price", "Discount", "Final Price"])
ws.append(["Widget A", 100, 0.1, "=B2*(1-C2)"])
ws.append(["Widget B", 200, 0.15, "=B3*(1-C3)"])

# Protect the sheet with a password
ws.protection = SheetProtection(
    sheet=True,
    password=os.getenv("SHEET_PASSWORD", "changeme"),
    formatCells=False,      # Allow formatting
    formatColumns=False,    # Allow column width changes
    formatRows=False,       # Allow row height changes
    insertColumns=False,
    insertRows=False,
    insertHyperlinks=False,
    deleteColumns=True,     # Prevent column deletion
    deleteRows=True,        # Prevent row deletion
    selectLockedCells=False,
    sort=False,             # Allow sorting
    autoFilter=False,       # Allow filtering
    pivotTables=True,       # Prevent pivot table changes
    selectUnlockedCells=False,
)

# Unlock specific cells that users can edit (discount column)
from openpyxl.styles import Protection

unlocked = Protection(locked=False)
for row in range(2, 4):
    ws.cell(row=row, column=3).protection = unlocked

# Protect the workbook structure (prevent adding/removing sheets)
wb.security.workbookPassword = os.getenv("WORKBOOK_PASSWORD", "changeme")
wb.security.lockStructure = True

wb.save("protected.xlsx")
```

**VBA Macro Preservation**:

```python
from openpyxl import load_workbook

# Load a macro-enabled workbook (.xlsm) while preserving VBA
wb = load_workbook("template_with_macros.xlsm", keep_vba=True)
ws = wb.active

# Modify data without affecting macros
ws["A1"] = "Updated by automation"
ws["B1"] = 42

# Save as .xlsm to preserve macros
# IMPORTANT: Saving as .xlsx will strip all VBA code
wb.save("updated_with_macros.xlsm")
```

```python
# xlsxwriter: create a new .xlsm file with VBA from a binary
import xlsxwriter

wb = xlsxwriter.Workbook("new_macros.xlsm")
ws = wb.add_worksheet()

ws.write("A1", "Click the button to run the macro")

# Add VBA project from a .bin file extracted from an existing .xlsm
# Extract with: python -c "import zipfile; z=zipfile.ZipFile('source.xlsm'); z.extract('xl/vbaProject.bin')"
wb.add_vba_project("xl/vbaProject.bin")

# Optionally add a button that triggers a macro
# ws.insert_button("B3", {"macro": "MyMacro", "caption": "Run Report", "width": 128, "height": 30})

wb.close()
```

**Images and Embedded Objects**:

```python
from openpyxl import Workbook
from openpyxl.drawing.image import Image

wb = Workbook()
ws = wb.active

# Add an image
img = Image("company_logo.png")
img.width = 200   # Pixels
img.height = 80
ws.add_image(img, "A1")

# Add a second image positioned elsewhere
chart_img = Image("exported_chart.png")
chart_img.width = 600
chart_img.height = 400
ws.add_image(chart_img, "D5")

# Write data below the logo
ws["A6"] = "Report starts here"

wb.save("with_images.xlsx")
```

**Hyperlinks**:

```python
from openpyxl import Workbook

wb = Workbook()
ws = wb.active

# External URL
ws["A1"] = "Visit Website"
ws["A1"].hyperlink = "https://example.com"
ws["A1"].style = "Hyperlink"  # Built-in hyperlink style

# Link to another sheet in the same workbook
ws2 = wb.create_sheet("Details")
ws["A2"] = "Go to Details"
ws["A2"].hyperlink = "#Details!A1"
ws["A2"].style = "Hyperlink"

# Link to a file
ws["A3"] = "Open Document"
ws["A3"].hyperlink = "file:///C:/reports/summary.pdf"
ws["A3"].style = "Hyperlink"

# Email link
ws["A4"] = "Send Email"
ws["A4"].hyperlink = "mailto:reports@example.com?subject=Monthly%20Report"
ws["A4"].style = "Hyperlink"

wb.save("hyperlinks.xlsx")
```

### Step 8: Pandas Integration and Data Pipelines

Pandas provides the fastest path from data analysis to Excel output. The `DataFrame.to_excel()` method delegates to openpyxl or xlsxwriter under the hood, while `pd.read_excel()` handles ingestion.

**Basic DataFrame to Excel**:

```python
import pandas as pd

# Create sample data
df = pd.DataFrame({
    "Product": ["Widget A", "Widget B", "Widget C", "Widget D"],
    "Revenue": [15000.50, 22000.75, 8500.00, 31200.25],
    "Cost": [8000, 12000, 5000, 18000],
    "Units Sold": [150, 220, 85, 312],
    "Date": pd.to_datetime(["2026-01-15", "2026-02-01", "2026-02-15", "2026-03-01"]),
})
df["Profit"] = df["Revenue"] - df["Cost"]
df["Margin"] = df["Profit"] / df["Revenue"]

# Simple export
df.to_excel("basic_export.xlsx", index=False, sheet_name="Sales")

# Export with xlsxwriter engine for better formatting control
df.to_excel(
    "formatted_export.xlsx",
    index=False,
    sheet_name="Sales",
    engine="xlsxwriter",
    float_format="%.2f",
)
```

**Multi-Sheet Export**:

```python
import pandas as pd

# Multiple DataFrames to separate sheets
sales_df = pd.DataFrame({
    "Product": ["Widget A", "Widget B"],
    "Revenue": [15000, 22000],
})

inventory_df = pd.DataFrame({
    "Product": ["Widget A", "Widget B"],
    "Stock": [500, 300],
    "Reorder Point": [100, 50],
})

summary_df = pd.DataFrame({
    "Metric": ["Total Revenue", "Total Stock", "Products"],
    "Value": [37000, 800, 2],
})

# Use ExcelWriter for multi-sheet output
with pd.ExcelWriter("multi_sheet.xlsx", engine="openpyxl") as writer:
    summary_df.to_excel(writer, sheet_name="Summary", index=False)
    sales_df.to_excel(writer, sheet_name="Sales", index=False)
    inventory_df.to_excel(writer, sheet_name="Inventory", index=False)
```

**Styled Export with xlsxwriter Engine**:

```python
import pandas as pd

df = pd.DataFrame({
    "Product": ["Widget A", "Widget B", "Widget C", "Widget D"],
    "Revenue": [15000, 22000, 8500, 31200],
    "Cost": [8000, 12000, 5000, 18000],
    "Margin": [0.4667, 0.4545, 0.4118, 0.4231],
})

with pd.ExcelWriter("styled_pandas.xlsx", engine="xlsxwriter") as writer:
    df.to_excel(writer, sheet_name="Report", index=False, startrow=1)

    wb = writer.book
    ws = writer.sheets["Report"]

    # Title row
    title_fmt = wb.add_format({
        "bold": True, "font_size": 16, "font_color": "#2F5496",
    })
    ws.write("A1", "Sales Performance Report", title_fmt)

    # Header formatting
    header_fmt = wb.add_format({
        "bold": True, "bg_color": "#2F5496", "font_color": "#FFFFFF",
        "border": 1, "align": "center",
    })
    for col_num, header in enumerate(df.columns):
        ws.write(1, col_num, header, header_fmt)

    # Column formats
    currency_fmt = wb.add_format({"num_format": "$#,##0", "border": 1})
    percent_fmt = wb.add_format({"num_format": "0.0%", "border": 1})

    ws.set_column("A:A", 20)
    ws.set_column("B:C", 15, currency_fmt)
    ws.set_column("D:D", 12, percent_fmt)

    # Conditional formatting on margin column
    red_fmt = wb.add_format({"bg_color": "#FFC7CE", "font_color": "#9C0006"})
    green_fmt = wb.add_format({"bg_color": "#C6EFCE", "font_color": "#006100"})

    ws.conditional_format("D3:D6", {
        "type": "cell", "criteria": "<", "value": 0.45, "format": red_fmt,
    })
    ws.conditional_format("D3:D6", {
        "type": "cell", "criteria": ">=", "value": 0.45, "format": green_fmt,
    })

    # Add a chart
    chart = wb.add_chart({"type": "column"})
    chart.add_series({
        "name": "Revenue",
        "categories": "=Report!$A$3:$A$6",
        "values": "=Report!$B$3:$B$6",
        "fill": {"color": "#2F5496"},
    })
    chart.set_title({"name": "Revenue by Product"})
    chart.set_size({"width": 500, "height": 300})
    ws.insert_chart("F3", chart)
```

**Pandas Styler for Conditional Formatting**:

```python
import pandas as pd

df = pd.DataFrame({
    "Product": ["Widget A", "Widget B", "Widget C", "Widget D"],
    "Revenue": [15000, 22000, 8500, 31200],
    "Cost": [8000, 12000, 5000, 18000],
    "Profit": [7000, 10000, 3500, 13200],
    "Margin": [0.4667, 0.4545, 0.4118, 0.4231],
})

def highlight_negative(val):
    """Highlight negative values in red."""
    color = "color: #9C0006; background-color: #FFC7CE" if val < 0 else ""
    return color

def highlight_high_margin(val):
    """Highlight margins above 45% in green."""
    if val > 0.45:
        return "color: #006100; background-color: #C6EFCE"
    return ""

# Apply styles
styled = (
    df.style
    .format({
        "Revenue": "${:,.0f}",
        "Cost": "${:,.0f}",
        "Profit": "${:,.0f}",
        "Margin": "{:.1%}",
    })
    .map(highlight_negative, subset=["Profit"])
    .map(highlight_high_margin, subset=["Margin"])
    .bar(subset=["Revenue"], color="#D6E4F0", vmin=0)
    .set_caption("Sales Performance Report")
    .set_table_styles([
        {"selector": "th", "props": [
            ("background-color", "#2F5496"),
            ("color", "white"),
            ("font-weight", "bold"),
        ]},
    ])
)

# Export to Excel (uses openpyxl engine)
styled.to_excel("styler_export.xlsx", engine="openpyxl", index=False)
```

**Read, Transform, Write Pipeline**:

```python
import pandas as pd
from pathlib import Path
from openpyxl import load_workbook
from openpyxl.styles import Font, PatternFill


def excel_etl_pipeline(
    input_path: str | Path,
    output_path: str | Path,
    transformations: dict | None = None,
) -> dict:
    """Read an Excel file, apply transformations, and write a formatted output.

    Args:
        input_path: Path to the source Excel file.
        output_path: Path for the output Excel file.
        transformations: Optional dict of column_name -> callable transforms.

    Returns:
        Dict with row counts and sheet names processed.
    """
    input_path = Path(input_path)
    output_path = Path(output_path)

    # Read all sheets
    all_sheets = pd.read_excel(input_path, sheet_name=None, engine="openpyxl")
    stats = {"sheets_processed": [], "total_rows": 0}

    with pd.ExcelWriter(output_path, engine="openpyxl") as writer:
        for sheet_name, df in all_sheets.items():
            # Apply transformations
            if transformations:
                for col, transform_fn in transformations.items():
                    if col in df.columns:
                        df[col] = df[col].apply(transform_fn)

            # Remove fully empty rows
            df = df.dropna(how="all")

            # Write to output
            df.to_excel(writer, sheet_name=sheet_name, index=False)
            stats["sheets_processed"].append(sheet_name)
            stats["total_rows"] += len(df)

    # Post-process: apply formatting with openpyxl
    wb = load_workbook(output_path)
    header_font = Font(bold=True, color="FFFFFF")
    header_fill = PatternFill(start_color="2F5496", fill_type="solid")

    for ws in wb.worksheets:
        # Style headers
        for cell in ws[1]:
            cell.font = header_font
            cell.fill = header_fill

        # Auto-adjust column widths
        for col in ws.columns:
            max_length = 0
            col_letter = col[0].column_letter
            for cell in col:
                if cell.value:
                    max_length = max(max_length, len(str(cell.value)))
            ws.column_dimensions[col_letter].width = min(max_length + 4, 50)

        # Freeze header row
        ws.freeze_panes = "A2"

        # Enable autofilter
        if ws.max_row > 1:
            ws.auto_filter.ref = ws.dimensions

    wb.save(output_path)
    return stats


# Usage:
# stats = excel_etl_pipeline(
#     "raw_data.xlsx",
#     "processed_report.xlsx",
#     transformations={
#         "revenue": lambda x: round(x, 2) if pd.notna(x) else 0,
#         "name": lambda x: str(x).strip().title() if pd.notna(x) else "",
#     },
# )
# print(f"Processed {stats['total_rows']} rows across {len(stats['sheets_processed'])} sheets")
```

**Batch Report Generation**:

```python
import pandas as pd
from pathlib import Path


def generate_regional_reports(
    data: pd.DataFrame,
    output_dir: str | Path,
    group_column: str = "Region",
) -> list[Path]:
    """Generate one Excel report per group (e.g., per region).

    Args:
        data: Source DataFrame with all regions.
        output_dir: Directory to write individual report files.
        group_column: Column name to group/split by.

    Returns:
        List of generated file paths.
    """
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    generated_files = []

    for group_name, group_df in data.groupby(group_column):
        safe_name = str(group_name).replace(" ", "_").lower()
        filepath = output_dir / f"report_{safe_name}.xlsx"

        with pd.ExcelWriter(filepath, engine="xlsxwriter") as writer:
            # Summary sheet
            summary = group_df.describe()
            summary.to_excel(writer, sheet_name="Summary")

            # Detail sheet
            group_df.to_excel(writer, sheet_name="Detail", index=False)

            # Format the detail sheet
            wb = writer.book
            ws = writer.sheets["Detail"]

            header_fmt = wb.add_format({
                "bold": True, "bg_color": "#2F5496",
                "font_color": "#FFFFFF", "border": 1,
            })

            for col_num, col_name in enumerate(group_df.columns):
                ws.write(0, col_num, col_name, header_fmt)
                # Auto-fit column width
                max_len = max(
                    group_df[col_name].astype(str).map(len).max(),
                    len(col_name),
                )
                ws.set_column(col_num, col_num, min(max_len + 2, 40))

        generated_files.append(filepath)

    return generated_files


# Usage:
# df = pd.DataFrame({
#     "Region": ["North", "North", "South", "South", "East", "East"],
#     "Product": ["A", "B", "A", "B", "A", "B"],
#     "Revenue": [15000, 22000, 18000, 12000, 25000, 19000],
# })
# files = generate_regional_reports(df, "output/regional_reports")
# for f in files:
#     print(f"Generated: {f}")
```

**Common Pitfalls and Best Practices**:

- **Floating-point precision**: Use `Decimal` for financial data in Python. openpyxl converts to float internally, so round before writing: `float(Decimal("15000.50").quantize(Decimal("0.01")))`
- **Date handling**: Always pass `datetime` or `date` objects, not strings. Set `number_format` explicitly to control display
- **Memory with large files**: Use xlsxwriter's `constant_memory` mode or ExcelJS streaming API for datasets over 100,000 rows
- **Formula evaluation**: XLSX libraries write formula text, not computed values. The formulas are evaluated only when the file is opened in Excel. If you need pre-computed values, calculate them in Python and write the results
- **data_only mode in openpyxl**: Returns the last cached value from when the file was saved by Excel. If the file was never opened in Excel, formula cells return `None`
- **String length limit**: Excel cells support a maximum of 32,767 characters. Truncate long strings before writing
- **Sheet name limits**: Sheet names cannot exceed 31 characters and cannot contain `\ / * ? : [ ]`
- **Column limit**: XLSX supports up to 16,384 columns (XFD). Validate wide DataFrames before export
- **File locking**: On Windows, Excel locks open files. Catch `PermissionError` and prompt users to close the file
- **Encoding**: XLSX is UTF-8 internally. Special characters, CJK text, and emoji work without extra configuration
