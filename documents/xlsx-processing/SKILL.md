---
name: xlsx-processing
description: >
  Create, parse, format, and audit Microsoft Excel (.xlsx) workbooks programmatically
  using openpyxl. Use when generating financial spreadsheets with calculated
  formulas, applying cell styles and number formats, managing multiple worksheets,
  building structured tables and charts, handling large files in read-only or
  write-only mode, or preventing formula injection from untrusted data. Do not use for
  legacy .xls, Google Sheets API work, pivot-table authoring, or when recalculated
  values are required without a spreadsheet engine (openpyxl cannot calculate).
compatibility: >
  Agent Skills-compatible coding agents operating with openpyxl (3.1.x checked in
  October 2026; Python 3.8+). LibreOffice is optional for recalculating formulas
  headlessly. XlsxWriter is an alternative for write-only generation.
metadata:
  author: michaelweissdev
  version: "1.1.0"
  tags: "xlsx, excel, openpyxl, spreadsheets, formulas, financial-modeling, office"
  topics: "office, documentation, devtools"
---

# Programmatic Microsoft Excel (.xlsx) Processing

Excel workbooks (`.xlsx`) represent structured tabular data, multi-sheet workbooks, formula calculation trees, cell styling, and data formatting. Building production-grade Excel files requires disciplined separation of raw numeric data from display formatting, precise formula syntax, and validation of cell coordinates.

Detailed reference guides:
- [openpyxl Patterns, Formulas & Formatting Guide](references/openpyxl-guide.md)

---

## The 6-Step Spreadsheet Engineering Workflow

1. **Inspect Requirements**: Determine required sheets, data schemas, formula relationships (`SUM`, `AVERAGE`, `VLOOKUP`), and number formatting (currency, percentages, dates).
2. **Select Tooling**: Use `openpyxl` for Python `.xlsx` generation and modification.
3. **Draft / Update Workbook**: Write raw typed data (integers, floats, dates, strings) into cells—never format numbers as pre-rendered text strings like `"$1,200.00"`.
4. **Apply Number Formatting & Styles**: Set explicit `number_format`, font weights, header fills, column widths, and cell borders.
5. **Validate Calculation Formulas**: Confirm formula syntax uses uppercase names, valid coordinate ranges, and produces no `#VALUE!` or `#REF!` errors.
6. **Save & Distribute Clean Artifact**: Save to a genuine `.xlsx` file and verify readability.

---

## 1. Creating a Styled Financial Model with `openpyxl`

```python
from datetime import date
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter

def generate_financial_model(output_path: str):
    wb = Workbook()
    ws = wb.active
    ws.title = "Q4 Financials"

    # Styling Palettes
    header_font = Font(name="Calibri", size=11, bold=True, color="FFFFFF")
    header_fill = PatternFill(start_color="1F4E79", end_color="1F4E79", fill_type="solid")
    total_font = Font(name="Calibri", size=11, bold=True)
    border_thin = Side(border_style="thin", color="D9D9D9")
    cell_border = Border(top=border_thin, left=border_thin, right=border_thin, bottom=border_thin)
    double_bottom = Border(bottom=Side(border_style="double", color="000000"), top=border_thin)

    # 1. Document Title
    ws["A1"] = "Acme Corp - Q4 Performance Summary"
    ws["A1"].font = Font(name="Calibri", size=16, bold=True)
    ws["A2"] = f"Report Date: {date.today().isoformat()}"
    ws["A2"].font = Font(name="Calibri", size=10, italic=True)

    # 2. Table Headers
    headers = ["Department", "Budget", "Actual Spend", "Variance", "% Utilized"]
    for col_idx, h in enumerate(headers, start=1):
        cell = ws.cell(row=4, column=col_idx, value=h)
        cell.font = header_font
        cell.fill = header_fill
        cell.alignment = Alignment(horizontal="center" if col_idx > 1 else "left")

    # 3. Data Rows
    departments = [
        ("Engineering", 250000, 241200),
        ("Product & Design", 80000, 78500),
        ("Sales & Marketing", 140000, 149300),
        ("Operations & HR", 65000, 61000),
    ]

    start_row = 5
    for i, (dept, budget, actual) in enumerate(departments):
        r = start_row + i
        ws.cell(row=r, column=1, value=dept).border = cell_border

        # Numeric values stored as raw numbers (NOT strings)
        c_budget = ws.cell(row=r, column=2, value=budget)
        c_budget.number_format = "$#,##0"
        c_budget.border = cell_border

        c_actual = ws.cell(row=r, column=3, value=actual)
        c_actual.number_format = "$#,##0"
        c_actual.border = cell_border

        # Formula: Budget - Actual
        c_var = ws.cell(row=r, column=4, value=f"=B{r}-C{r}")
        c_var.number_format = "$#,##0"
        c_var.border = cell_border

        # Formula: Actual / Budget
        c_pct = ws.cell(row=r, column=5, value=f"=C{r}/B{r}")
        c_pct.number_format = "0.0%"
        c_pct.border = cell_border

    # 4. Total Summary Row
    total_row = start_row + len(departments)
    ws.cell(row=total_row, column=1, value="Total").font = total_font
    ws.cell(row=total_row, column=1).border = double_bottom

    c_tot_b = ws.cell(row=total_row, column=2, value=f"=SUM(B{start_row}:B{total_row-1})")
    c_tot_b.font = total_font
    c_tot_b.number_format = "$#,##0"
    c_tot_b.border = double_bottom

    c_tot_a = ws.cell(row=total_row, column=3, value=f"=SUM(C{start_row}:C{total_row-1})")
    c_tot_a.font = total_font
    c_tot_a.number_format = "$#,##0"
    c_tot_a.border = double_bottom

    c_tot_v = ws.cell(row=total_row, column=4, value=f"=B{total_row}-C{total_row}")
    c_tot_v.font = total_font
    c_tot_v.number_format = "$#,##0"
    c_tot_v.border = double_bottom

    c_tot_p = ws.cell(row=total_row, column=5, value=f"=C{total_row}/B{total_row}")
    c_tot_p.font = total_font
    c_tot_p.number_format = "0.0%"
    c_tot_p.border = double_bottom

    # 5. Auto-fit Column Widths with comfortable padding
    for col in ws.columns:
        max_len = max(len(str(cell.value or "")) for cell in col)
        col_letter = get_column_letter(col[0].column)
        ws.column_dimensions[col_letter].width = max(max_len + 4, 12)

    wb.save(output_path)
    print(f"Spreadsheet successfully generated: {output_path}")

if __name__ == "__main__":
    generate_financial_model("q4_financials.xlsx")
```

---

## 2. Reading Formulas vs Cached Values

When opening workbooks created by third parties:
- `load_workbook(filename)`: Reads the **formula text** (`=SUM(A1:A10)`).
- `load_workbook(filename, data_only=True)`: Reads the **cached evaluated value** (`150.0`).
*(Note: If a formula was generated by a script and never opened in Excel, `data_only=True` will return `None` because openpyxl does not evaluate formula engines.)*

```python
from openpyxl import load_workbook

# Read formula text
wb_formulas = load_workbook("q4_financials.xlsx", data_only=False)
print("Formula:", wb_formulas["Q4 Financials"]["B9"].value) # Output: =SUM(B5:B8)

# Read evaluated values
wb_values = load_workbook("q4_financials.xlsx", data_only=True)
print("Cached Value:", wb_values["Q4 Financials"]["B9"].value)
```

---

## 3. Common Mistakes and Anti-Patterns

| Anti-Pattern | Bug / Risk | Correct Practice |
| :--- | :--- | :--- |
| Writing numbers formatted as strings: `"$500"` | Breaks Excel mathematical formulas (`#VALUE!`) | Store raw number `500`, set `number_format = "$#,##0"` |
| Lowercase or localized formula names: `=sum(a1:a5)`, `=SOMME(...)` | Stored text is not guaranteed to parse; localized names fail in the file format | Write English, uppercase function names with comma argument separators: `=SUM(A1:A5)` |
| Writing untrusted strings that start with `=`, `+`, `-`, `@` | openpyxl stores a string beginning with `=` as a formula (formula injection); exported CSV is risky too | Force text: `cell.value = text; cell.data_type = "s"`, or validate/escape input |
| Load, edit, save a workbook with charts, images, or pivots | openpyxl does not preserve everything (charts, pivots, some shapes and conditional-format features can be lost) | Test on a copy, diff visually, or edit the XML/use a different tool |
| `load_workbook(data_only=True)` then `save()` | Formulas are replaced by cached values permanently | Keep a separate formulas workbook; never save a data_only copy over the source |
| Opening `.xlsm` without `keep_vba=True` then saving | Macros dropped | `load_workbook(path, keep_vba=True)` and save as `.xlsm`; never run macros |
| Floating-point money in cells | Rounding surprises (Excel keeps about 15 significant digits) | Store cents as integers or use `ROUND` in formulas |
| Dates as strings | Sorting and arithmetic break | Write `datetime.date`/`datetime` objects and set `number_format` |
| Overwriting open workbooks | File lock crash on Windows (`PermissionError`) | Save to new file or ensure workbook is closed |
| Relying on `data_only=True` for newly created files | Returns `None` because openpyxl has no calculation engine | Open in Excel/LibreOffice to calculate caches |

---

## 4. Large Files, Recalculation, and Untrusted Workbooks

- **Large files**: `load_workbook(path, read_only=True)` streams rows (close the workbook; no random cell access, formatting limited). `Workbook(write_only=True)` plus `ws.append(row)` writes with low memory but cannot revisit cells. Both fit exports of tens of thousands of rows or more.
- **Recalculation**: openpyxl never computes formulas, so a script-written workbook has no cached values until a spreadsheet engine opens and saves it. If a downstream reader needs values, recalculate with LibreOffice headless (for example `soffice --headless --convert-to xlsx --outdir out_dir in.xlsx`) and inspect `data_only=True` output; or compute values in Python and write them as numbers when formulas are not required. Verify results independently, because engine differences exist.
- **Error values**: after recalculation, scan for `#REF!`, `#NAME?`, `#DIV/0!`, `#VALUE!`, `#N/A` in cached values.
- **Untrusted workbooks**: `.xlsx` is a ZIP of XML. Cap size, avoid external links (`xl/externalLinks`) and data connections, never enable macros (`.xlsm`), and consider installing `defusedxml` so openpyxl parses XML defensively. openpyxl does not execute formulas or macros, but Excel will when a person opens the file.
- **Sharing**: remove hidden sheets, comments, and personal properties (`wb.properties`) you do not intend to disclose.

## 5. Troubleshooting

| Symptom | Cause | Action |
| :--- | :--- | :--- |
| Cell shows formula text instead of result | Cell stored as text, or number format `@` | Remove text format; ensure value starts with `=` and is not forced to string |
| `#NAME?` in Excel | Misspelled or non-English function name, or a function the app lacks | Use English names; avoid newer functions if recipients use older Excel |
| `data_only=True` returns `None` | No cached value (never calculated) | Recalculate via a spreadsheet engine |
| `InvalidFileException` | Wrong extension or format | Use `.xlsx`/`.xlsm`/`.xltx`; convert `.xls` first |
| Memory blow-up | Full load of a huge file | Use `read_only=True` / `write_only=True` |
| Column shows `####` | Column too narrow for number or date | Increase width or shorten format |

## 6. Verification Checklist

- [ ] All numeric and financial cells contain raw numeric types (not pre-formatted strings).
- [ ] Number formats explicitly set (`$#,##0`, `0.0%`, `YYYY-MM-DD`).
- [ ] Formula names in uppercase (`SUM`, `AVERAGE`, `IF`, `VLOOKUP`).
- [ ] Column widths adjusted to prevent `###` overflow truncation.
- [ ] File verified with `zipfile.is_zipfile(path)` and opens without error.
