---
name: arc-xlsx
description: Create and edit Excel XLSX workbooks with formulas, readable tables, data checks, and explicit formula recalculation and cache verification.
---

# Excel workbooks

Use this skill for actual `.xlsx` files. For a connected Google Sheet or Microsoft Excel workbook, discover and use that authorized App's tools instead of exporting and replacing the workbook without reason. Inspect existing sheets, formulas, named ranges, units, and formatting before editing. Preserve macros with an appropriate macro-capable editor; do not turn `.xlsm` into `.xlsx` and claim macros were retained.

## Build from checked data

Check for Python and `openpyxl` on an authorized computer; install missing dependencies in a task-local environment if necessary. Obtain [scripts/inspect_xlsx.py](scripts/inspect_xlsx.py) through the resource tools. Reuse a supplied template. Separate user-entered assumptions from calculations. Store real numbers and dates rather than display strings, label currencies and units, use formulas for derived figures, and validate totals independently against the source data. Do not fill absent data with invented zeros.

Use `openpyxl.load_workbook(path)` for an existing file or `Workbook()` for a new one. Give sheets meaningful names, freeze header rows, set useful number formats and widths, and use actual tables or filters. Avoid merged cells inside sortable data. Prefix externally supplied text that begins with a formula marker when it should remain literal text; do not turn untrusted CSV fields into formulas.

## Recalculate and verify

`openpyxl` writes formulas but does not calculate them. Setting automatic calculation flags does not create cached results. Run `python scripts/inspect_xlsx.py OUTPUT.xlsx` to identify formula cells, stored errors, and missing cached values. Independently check important arithmetic with Python. When a local Excel or LibreOffice engine is available, recalculate a copy, save it, and rerun the inspector to verify cached results and errors. Preserve the original when conversion might discard unsupported features.

The helper reports structure and stored values; it does not prove formulas are correct, references are current, or a chart is readable. Inspect representative sheets and charts visually when a renderer is available. If recalculation is unavailable, clearly identify uncached formulas rather than claiming a fully calculated workbook. Return the actual saved file path and any remaining verification limit.

Reference: https://openpyxl.readthedocs.io/en/stable/
