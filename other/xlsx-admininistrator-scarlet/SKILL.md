---
name: xlsx
description: Create Excel spreadsheets (.xlsx) — tables, formulas, number formats, several sheets, charts. Use when the user asks for an Excel file or a downloadable spreadsheet.
license: Same as the Scarlet repository
metadata:
  default_enabled: "true"
  display_name: Excel (.xlsx)
---

# xlsx — Excel spreadsheets

Written by Scarlet for its sandbox. `openpyxl` and `pandas` are available —
no LibreOffice, no `pip install`, no network.

## How to make a file

Call `run_code` with `skill="xlsx"`. The helper `make_xlsx.py` sits next to
your code:

```python
from make_xlsx import build_xlsx

rows = [["Khoản", "Tháng 1", "Tháng 2", "Tổng"],
        ["Thuê nhà", 5000000, 5000000, "=SUM(B2:C2)"],
        ["Ăn uống", 3200000, 2900000, "=SUM(B3:C3)"],
        ["Cộng", "=SUM(B2:B3)", "=SUM(C2:C3)", "=SUM(D2:D3)"]]
build_xlsx("chi-tieu.xlsx", {"Chi tiêu": rows},
           number_formats={"Chi tiêu": {"B": "#,##0", "C": "#,##0", "D": "#,##0"}})
print("ok")
```

- One key per sheet (name ≤ 31 chars, no `[]:*?/\`). Row 0 is the header:
  bold, frozen, with a filter. Columns are auto-sized.
- A string starting with `=` is a formula. **Prefer formulas over values you
  computed in Python** so the sheet stays live when the user edits it.
  Formulas are not evaluated in the sandbox — Excel computes them on open.
- Numbers must be numbers (`5000000`, not `"5.000.000"`); show separators with
  `number_formats` (`"#,##0"`, `"0.0%"`, `"dd/mm/yyyy"`).

### Chart

`build_xlsx` returns the workbook; add a chart and save again:

```python
from openpyxl.chart import BarChart, Reference
wb = build_xlsx("sales.xlsx", {"Data": rows})
ws = wb["Data"]
chart = BarChart()
chart.title = "Doanh thu"
chart.add_data(Reference(ws, min_col=2, min_row=1, max_row=ws.max_row), titles_from_data=True)
chart.set_categories(Reference(ws, min_col=1, min_row=2, max_row=ws.max_row))
ws.add_chart(chart, "F2")
wb.save("sales.xlsx")
```

With `pandas`: `df.to_excel("x.xlsx", index=False)` works too (engine
`openpyxl`), but loses the header styling above.

## Rules

- Save with a **relative** file name (current folder). Every file left there
  is sent to the user as a download — write exactly one `.xlsx`; helper files
  must start with a dot (`.tmp.csv`).
- The user's uploaded files are **not** in the sandbox — build from the
  conversation text.
- A traceback in `stderr` means fix the code and call `run_code` again.
- After success, tell the user the file is ready to download in the panel.
