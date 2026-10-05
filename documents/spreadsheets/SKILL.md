---
name: spreadsheets
description: Use when creating, reading, or fixing spreadsheets (.xlsx, .csv). Covers formulas, formatting, charts, data cleaning, and handling the messy real-world files that are not actually tabular.
metadata:
  category: documents
  version: 1.0.0
  tags: [xlsx, excel, csv, data-cleaning, formulas]
---

# Spreadsheets

## Purpose

Build and repair spreadsheets, including the ones that arrive with headers on row 7, merged cells, and three tables on one sheet. Most spreadsheet work is cleaning, not computing.

## When to Use

- Creating a spreadsheet from data.
- Reading or extracting data from an existing workbook.
- Cleaning a messy file into something a machine can read.
- Adding formulas, formatting, or charts.
- Converting between tabular formats.

## Capabilities

- Workbook generation: sheets, formulas, formatting, conditional formatting, charts.
- Reading, including files whose structure is not a clean table.
- Data cleaning: header detection, type coercion, deduplication.
- Formula construction, including cross-sheet references.
- Format conversion.

## Inputs

- The data, or the source workbook.
- The intended audience: a human reading it, or a machine parsing it.
- Any formatting or template requirements.

## Outputs

- A workbook with correct formulas and readable formatting.
- Or clean, typed, tabular data extracted from a messy source.

## Workflow

1. **Inspect before parsing** — Read the first thirty rows raw. Real spreadsheets have title rows, blank rows, merged headers, and notes in the margins. Assuming `header=0` is how you end up with a DataFrame whose columns are `Unnamed: 0`.
2. **Find the actual header row** — The first row where every cell is non-empty and the row below it has consistent types.
3. **Coerce the types explicitly** — Excel stores dates as numbers, numbers as text, and empty cells as several different things. Nothing is what it appears.
4. **Clean before computing** — Trim whitespace, unify the null representations, drop the total row that got read as data.
5. **When writing for humans, format** — Column widths, number formats, a frozen header row. An unformatted spreadsheet with a column of `1234567.891` is not usable.
6. **Verify the formulas calculate** — A written formula is a string until a spreadsheet application evaluates it. Open the file and check.

## Best Practices

- The most common cause of a wrong spreadsheet analysis is a total row read as a data row, silently doubling the sum.
- Excel dates are days since 1900 (with a deliberate leap-year bug). A date column read as a number is a date; convert it rather than treating it as an integer.
- Merged cells produce a value in the top-left and `None` everywhere else. Forward-fill after unmerging, or the grouping column will be 80% empty.
- Trailing whitespace in a key column silently breaks every join. Strip on read, always.
- Do not write formulas that reference an entire column (`SUM(A:A)`) in a large workbook — it forces a full-column calculation on every change.
- If the output is going to be read by a program, write CSV or Parquet. `.xlsx` is a presentation format.

## Examples

**Reading a real-world messy file:**

```python
import pandas as pd

# Never trust the structure. Look first.
raw = pd.read_excel("sales.xlsx", sheet_name="Q2", header=None, nrows=30)

# Row 0: "ACME Corp — Confidential"      <- a title
# Row 1: (blank)
# Row 2: "Q2 2026 Sales by Region"       <- a subtitle
# Row 3: (blank)
# Row 4: Region | Rep | Units | Revenue  <- the actual header, on row 4
# ...
# Row 47: "TOTAL" | | 8,412 | 1,204,880  <- a total row that must not be data

def find_header_row(raw: pd.DataFrame, max_scan: int = 20) -> int:
    for i in range(max_scan):
        row = raw.iloc[i]
        if row.notna().all() and raw.iloc[i + 1].notna().sum() >= len(row) - 1:
            return i
    raise ValueError("no header row found in the first 20 rows")

header_row = find_header_row(raw)

df = pd.read_excel("sales.xlsx", sheet_name="Q2", header=header_row)

# Drop the total row — it is the single most common source of a doubled sum.
df = df[~df["Region"].astype(str).str.strip().str.upper().isin({"TOTAL", "SUM", "GRAND TOTAL"})]

# Clean the keys: trailing whitespace silently breaks every join downstream.
df["Region"] = df["Region"].str.strip()
df["Rep"] = df["Rep"].str.strip()

# Excel stores numbers as text more often than anyone expects.
df["Revenue"] = pd.to_numeric(
    df["Revenue"].astype(str).str.replace(r"[$,]", "", regex=True),
    errors="coerce",
)

assert df["Revenue"].notna().all(), "some revenue values failed to parse"
```

**Writing a workbook a human can read:**

```python
from openpyxl.styles import Font, PatternFill, Alignment
from openpyxl.utils import get_column_letter

with pd.ExcelWriter("output/summary.xlsx", engine="openpyxl") as writer:
    summary.to_excel(writer, sheet_name="Summary", index=False, startrow=0)
    ws = writer.sheets["Summary"]

    header_fill = PatternFill("solid", fgColor="1F2937")
    for cell in ws[1]:
        cell.font = Font(bold=True, color="FFFFFF")
        cell.fill = header_fill
        cell.alignment = Alignment(horizontal="center")

    ws.freeze_panes = "A2"                       # header stays visible when scrolling
    ws.auto_filter.ref = ws.dimensions

    for i, column in enumerate(summary.columns, start=1):
        letter = get_column_letter(i)
        width = max(summary[column].astype(str).str.len().max(), len(column)) + 3
        ws.column_dimensions[letter].width = min(width, 50)

        if "revenue" in column.lower() or "cents" in column.lower():
            for cell in ws[letter][1:]:
                cell.number_format = '#,##0.00'   # 1234567.891 is not a readable number
```

## Notes

- The total-row problem is worth checking for every single time. It produces an answer that is exactly double, which is large enough to be wrong and plausible enough to be believed.
- `openpyxl` reads formulas as strings by default. To read computed values instead, open with `data_only=True` — but note that this returns `None` if the file has never been opened and calculated by Excel.
- For anything above a few hundred thousand rows, `.xlsx` becomes slow and fragile. Use CSV or Parquet and reserve the spreadsheet for the summary.
