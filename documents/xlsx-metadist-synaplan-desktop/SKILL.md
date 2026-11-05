---
name: xlsx
description: Write a real Excel workbook (.xlsx) from JSON or CSV — several sheets, styled header, numbers, formulas, a SUM total row — or read an existing .xlsx back to JSON/CSV. Standard library only, no Excel needed.
license: Apache-2.0
compatibility:
  python: true
---

# xlsx

Create a `.xlsx` that opens in Excel, LibreOffice Calc and Google Sheets, or
read one so its numbers can be analysed, merged or re-shaped. No extra
packages: the script builds the OOXML package itself.

## When to use

- The user wants a spreadsheet: a summary table, merged data from several
  workbooks, a list with totals.
- The user has `.xlsx` files in an allowed folder and wants to combine or
  analyse them — **read** each one first, then **write** the result.

## How to run

Read (JSON contains every sheet; CSV takes the first sheet):

```
python3 <skill_dir>/run.py read <input.xlsx> <output.json>
```

Write: first save the spec with `write_file` into the out-box, then

```
python3 <skill_dir>/run.py write <spec.json> <output.xlsx>
python3 <skill_dir>/run.py write <input.csv> <output.xlsx>
```

- `<output.xlsx>` / `<output.json>` — paths **inside the out-box**.
- `<input.xlsx>` — a workbook in an allowed folder or in the out-box.

## Spec for write

```json
{
  "sheets": [
    {
      "name": "Summary",
      "columns": ["Region", "Units", "Revenue"],
      "rows": [["North", 120, 15400.5], ["South", 90, 10200]],
      "totals": true
    }
  ]
}
```

- Numbers stay numbers; a string starting with `=` is written as a formula
  (`"=C2*1.19"`). `"totals": true` adds a `SUM` row under numeric columns.
- The header row is bold and frozen, with a filter. Sheet names are trimmed
  to Excel's 31 characters.

Standard library only. After the script exits 0, tell the user the full path.
