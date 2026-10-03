---
name: xlsx
description: Create, read, edit, and analyse Excel spreadsheet files (.xlsx, .xlsm, .xltx, .csv, .tsv). Use whenever a spreadsheet file is the primary input or output — adding columns, computing formulas, formatting cells, building financial models, cleaning messy data, extracting tables, creating charts, or converting between tabular formats. Trigger when the user mentions an .xlsx file, "spreadsheet", "Excel", "budget", "data export", or any tabular data that belongs in a file rather than in chat.
---

# Excel / XLSX Spreadsheets

A `.xlsx` file is a ZIP archive of XML. Work with it programmatically using `openpyxl` (formulas + formatting) or `pandas` (bulk data). Choose the right tool for the job and apply it precisely.

| Task | Tool |
|---|---|
| Create or edit with formulas and formatting | `openpyxl` |
| Bulk data in/out, pivot analysis | `pandas` (`read_excel`, `to_excel`) |
| Quick read of content | `markitdown file.xlsx` |
| Reading both formulas AND cached values | Two `load_workbook` passes — see gotchas |

> `openpyxl`, `pandas`, and `markitdown` are typically pre-installed. Import directly. Only run `pip install` if an import fails.

---

## Non-Negotiable Standards

Every spreadsheet delivered must meet these standards:

- **Professional font throughout.** Arial or Calibri for data, Times New Roman for formal reports. No default Calibri 11 unless that is the existing convention.
- **Zero formula errors.** Never ship while `recalc` shows errors. A `#DIV/0!`, `#REF!`, or `#NAME?` in a delivered file is a failure.
- **Use formulas, not hardcoded results.** Write `=SUM(B2:B9)`, not the Python-computed value. The sheet must recalculate when inputs change.
- **Follow the user's spec literally.** Exact tab names, exact column headers, exact formula logic. Never redesign what was asked.
- **Document every assumption.** Hardcoded numbers need a cell comment or adjacent label with the source. "Source: Company 10-K, FY2024, Page 45" is correct. Unexplained magic numbers are not.
- **Input cells need a legend.** If you create a template for someone to fill in, add a legend naming which cells to edit and include one example row showing expected format.
- **Editing existing files: match conventions exactly.** Find the designated input cells (usually distinguished by font color or fill). Write only there. Leave all existing formulas untouched.

---

## Reading a Spreadsheet

```python
import subprocess

# Quick content read (no cell coordinates — use for overview only)
result = subprocess.run(["markitdown", "file.xlsx"], capture_output=True, text=True)
print(result.stdout)

# Read into pandas (values only, no formulas)
import pandas as pd
df = pd.read_excel("file.xlsx", sheet_name="Sheet1")
print(df.head())
print(df.dtypes)

# Read formulas (openpyxl — formulas as strings, no cached values)
import openpyxl
wb = openpyxl.load_workbook("file.xlsx")
ws = wb["Sheet1"]
print(ws["B10"].value)  # prints the formula string e.g. "=SUM(B2:B9)"

# Read cached values (openpyxl data_only — values only, no formulas)
# WARNING: data_only=True is destructive if you save — loses all formulas
wb_vals = openpyxl.load_workbook("file.xlsx", data_only=True)
ws_vals = wb_vals["Sheet1"]
print(ws_vals["B10"].value)  # prints the last-saved calculated value
```

### Reading Both Formulas and Values (Two-Pass)

```python
# CORRECT: two separate loads
wb_formulas = openpyxl.load_workbook("file.xlsx")                # formulas
wb_values   = openpyxl.load_workbook("file.xlsx", data_only=True) # cached values

ws_f = wb_formulas["Sheet1"]
ws_v = wb_values["Sheet1"]

for row in ws_f.iter_rows(min_row=2, values_only=False):
    for cell in row:
        formula = cell.value
        value   = wb_values["Sheet1"].cell(cell.row, cell.column).value
        if formula and str(formula).startswith("="):
            print(f"{cell.coordinate}: formula={formula}, value={value}")
```

---

## Creating a Spreadsheet

### Basic Creation with openpyxl

```python
import openpyxl
from openpyxl.styles import (
    Font, PatternFill, Alignment, Border, Side, numbers
)
from openpyxl.utils import get_column_letter

wb = openpyxl.Workbook()
ws = wb.active
ws.title = "Revenue Model"

# ── Header row ────────────────────────────────────────────────────────────
HEADER_FILL = PatternFill("solid", fgColor="1A1A2E")
HEADER_FONT = Font(name="Arial", bold=True, color="FFFFFF", size=11)

headers = ["Period", "Revenue ($k)", "COGS ($k)", "Gross Profit ($k)", "Margin %"]
for col, header in enumerate(headers, 1):
    cell = ws.cell(row=1, column=col, value=header)
    cell.font  = HEADER_FONT
    cell.fill  = HEADER_FILL
    cell.alignment = Alignment(horizontal="center")

# ── Data rows ─────────────────────────────────────────────────────────────
INPUT_FONT = Font(name="Arial", color="000080", size=11)  # blue = hardcoded input
FORMULA_FONT = Font(name="Arial", color="000000", size=11)  # black = formula

data = [
    ("Q1 2025", 1200, 480),
    ("Q2 2025", 1380, 552),
    ("Q3 2025", 1520, 608),
    ("Q4 2025", 1700, 680),
]

for row_idx, (period, revenue, cogs) in enumerate(data, 2):
    ws.cell(row=row_idx, column=1, value=period).font = Font(name="Arial", size=11)

    # Input values — blue font (hardcoded)
    rev_cell = ws.cell(row=row_idx, column=2, value=revenue)
    rev_cell.font = INPUT_FONT

    cogs_cell = ws.cell(row=row_idx, column=3, value=cogs)
    cogs_cell.font = INPUT_FONT

    # Formulas — black font
    gp_col  = get_column_letter(4)
    rev_col = get_column_letter(2)
    cog_col = get_column_letter(3)

    gp_cell = ws.cell(row=row_idx, column=4,
                       value=f"={rev_col}{row_idx}-{cog_col}{row_idx}")
    gp_cell.font = FORMULA_FONT

    margin_cell = ws.cell(row=row_idx, column=5,
                           value=f"=IFERROR({gp_col}{row_idx}/{rev_col}{row_idx},0)")
    margin_cell.font = FORMULA_FONT
    margin_cell.number_format = "0.0%"

# ── Number formats ────────────────────────────────────────────────────────
for row in ws.iter_rows(min_row=2, min_col=2, max_col=4):
    for cell in row:
        cell.number_format = '#,##0'  # thousands comma, no decimals

# ── Totals row ────────────────────────────────────────────────────────────
last_data_row = len(data) + 1
total_row = last_data_row + 1
ws.cell(row=total_row, column=1, value="TOTAL").font = Font(name="Arial", bold=True)

for col in range(2, 5):
    col_letter = get_column_letter(col)
    cell = ws.cell(row=total_row, column=col,
                   value=f"=SUM({col_letter}2:{col_letter}{last_data_row})")
    cell.font = Font(name="Arial", bold=True)
    cell.number_format = '#,##0'

# ── Column widths ─────────────────────────────────────────────────────────
ws.column_dimensions["A"].width = 12
for col in range(2, 6):
    ws.column_dimensions[get_column_letter(col)].width = 18

wb.save("revenue_model.xlsx")
print("Saved revenue_model.xlsx")
```

### Bulk Data with pandas

```python
import pandas as pd

# Create from dict
data = {
    "Name":       ["Alice", "Bob", "Carol"],
    "Department": ["Engineering", "Product", "Design"],
    "Salary":     [120000, 110000, 105000],
    "Start Date": pd.to_datetime(["2022-03-01", "2021-07-15", "2023-01-10"]),
}
df = pd.DataFrame(data)

# Write with formatting options
with pd.ExcelWriter("staff.xlsx", engine="openpyxl", datetime_format="YYYY-MM-DD") as writer:
    df.to_excel(writer, sheet_name="Staff", index=False)

    # Access workbook for formatting
    wb = writer.book
    ws = writer.sheets["Staff"]

    # Auto-size columns
    for col in ws.columns:
        max_len = max(len(str(cell.value or "")) for cell in col)
        ws.column_dimensions[col[0].column_letter].width = max_len + 4
```

---

## Formula Reference

### Preferred Formulas (work universally)

```excel
=SUM(B2:B9)                           — sum a range
=AVERAGE(B2:B9)                       — average
=COUNT(B2:B9)                         — count numbers
=COUNTA(A2:A9)                        — count non-empty
=IFERROR(B2/C2, 0)                   — guard divide by zero
=IF(B2>100, "High", "Low")           — conditional
=SUMIFS(D2:D9, A2:A9, "Q1")         — conditional sum
=COUNTIFS(A2:A9, ">0", B2:B9, "<100") — conditional count
=INDEX(A2:A9, MATCH("Alice", B2:B9, 0)) — flexible lookup
=VLOOKUP(A2, Sheet2!A:C, 2, FALSE)   — vertical lookup
=CONCATENATE(A2, " ", B2)            — join text (legacy safe)
```

### Functions Requiring `_xlfn.` Prefix in openpyxl

```python
# These must have _xlfn. prefix when written via openpyxl
ws["A1"] = "=_xlfn.TEXTJOIN(\", \", TRUE, A2:A10)"
ws["B1"] = "=_xlfn.IFS(A1>90,\"A\",A1>80,\"B\",TRUE,\"C\")"
ws["C1"] = "=_xlfn.MAXIFS(B2:B10, A2:A10, \"Q1\")"
```

### Never Use (breaks in LibreOffice recalc)

```
XLOOKUP, XMATCH, SORT, FILTER, UNIQUE, SEQUENCE
→ Use INDEX/MATCH for lookups
→ Sort and filter in Python before writing
```

---

## Financial Model Conventions

When building financial models, apply these standards unless the existing file differs:

### Color Coding
```python
# Standard financial model color convention
COLORS = {
    "hardcoded_input": "0000FF",  # Blue — user enters this
    "formula":         "000000",  # Black — calculated
    "cross_sheet_link":"008000",  # Green — links another sheet
    "external_link":   "FF0000",  # Red — links external file
    "key_assumption":  "FFFF00",  # Yellow fill — critical input cell
}
```

### Number Formats
```python
FORMATS = {
    "currency":    '$#,##0;($#,##0);-',     # negatives in parentheses
    "currency_mm": '$#,##0.0;($#,##0.0);-', # millions with decimal
    "percentage":  '0.0%',                    # store as fraction (0.15 = 15%)
    "multiple":    '0.0x',                    # valuation multiples
    "integer":     '#,##0',                   # thousands separator
    "year":        '@',                        # text format — prevents comma
}
```

### Model Structure Rules
```
1. All assumptions in clearly labeled input section — never embedded in formulas
2. One row per time period, one column per variable — consistent structure
3. Formulas identical across all projection columns — no one-off edits
4. Denominator protection: =IFERROR(numerator/denominator, 0) on all divisions
5. Assumption cells referenced by name, not repeated values:
   CORRECT: =B5*(1+$B$6)   where $B$6 is the growth rate cell
   WRONG:   =B5*1.05       (what if growth rate changes?)
```

---

## Cleaning Messy Data

```python
import pandas as pd

df = pd.read_excel("messy.xlsx", header=None)

# Find the actual header row (sometimes row 3 or 4)
header_row = df[df.iloc[:, 0].astype(str).str.contains("Name|ID|Date", na=False)].index[0]
df.columns = df.iloc[header_row]
df = df.iloc[header_row + 1:].reset_index(drop=True)

# Drop entirely empty rows and columns
df = df.dropna(how="all").dropna(axis=1, how="all")

# Strip whitespace from string columns
str_cols = df.select_dtypes(include="object").columns
df[str_cols] = df[str_cols].apply(lambda col: col.str.strip())

# Standardize date column
df["Date"] = pd.to_datetime(df["Date"], errors="coerce")

# Remove duplicate rows
df = df.drop_duplicates()

# Save cleaned version
df.to_excel("clean.xlsx", index=False)
print(f"Cleaned: {len(df)} rows, {len(df.columns)} columns")
```

---

## openpyxl Critical Gotchas

| Gotcha | What happens | Fix |
|---|---|---|
| `data_only=True` then save | All formulas replaced with literal values permanently | Never save a `data_only` workbook |
| `data_only=True` on freshly-written file | Returns `None` for all formula cells | Run recalc first, then load `data_only` |
| Writing to merged cell body | `AttributeError` — only top-left anchor is writable | Write only to the top-left cell of the merge |
| `.xlsm` without `keep_vba=True` | All macros stripped on save | `load_workbook("file.xlsm", keep_vba=True)` |
| Sheet name with space in formula | `#VALUE!` error | Quote the name: `='My Sheet'!A1` |
| External link references | `[1]Sheet!A1` — breaks on recalc | Extract cached values before resaving |

---

## Recalculation (Required When File Has Formulas)

openpyxl writes formulas as strings with no cached values. Until recalculated, formula cells return `None` to anything reading the file.

```bash
# If recalc.py helper is available:
python scripts/recalc.py output.xlsx

# Manual LibreOffice recalc:
libreoffice --headless --calc \
  --infilter="Calc MS Excel 2007 XML" \
  --convert-to xlsx output.xlsx
```

After recalc, verify with:
```python
wb = openpyxl.load_workbook("output.xlsx", data_only=True)
ws = wb.active
# Spot-check key formula cells — they should now have numeric values, not None
print(ws["B10"].value)  # should be a number, not None
```

**A clean recalc proves formulas evaluate — not that they are correct.** Always spot-check 3–5 formula results against manually computed expected values.

---

## Definition of Done — XLSX

- [ ] Correct tool used: openpyxl for formulas/formatting, pandas for bulk data
- [ ] Professional font applied throughout (Arial or Calibri)
- [ ] All formulas use cell references — no hardcoded computed values
- [ ] All formulas use safe, universally-supported functions
- [ ] `_xlfn.` prefix applied to post-2007 functions (TEXTJOIN, IFS, MAXIFS, MINIFS)
- [ ] XLOOKUP, XMATCH, SORT, FILTER, UNIQUE, SEQUENCE NOT used
- [ ] Zero divide-by-zero errors — all divisions wrapped in IFERROR
- [ ] Recalculation run — zero errors reported
- [ ] Key formula cells spot-checked against expected values
- [ ] All hardcoded numbers documented with source or comment
- [ ] Financial models: color coding applied (blue=input, black=formula)
- [ ] Column widths set — no truncated content
- [ ] Header row formatted (bold, fill, centered)
- [ ] File opens without errors in Excel and LibreOffice
