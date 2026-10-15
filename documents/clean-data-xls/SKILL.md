---
name: clean-data-xls
description: Clean up messy spreadsheet data — trim whitespace, fix inconsistent casing, convert numbers-stored-as-text, standardize dates, remove duplicates, and flag mixed-type columns. Use when data is messy, inconsistent, or needs prep before analysis. Triggers on "clean this data", "clean up this sheet", "normalize this data", "fix formatting", "dedupe", "standardize this column", "this data is messy", "데이터 정리해줘", "엑셀 정리", "이상한 데이터 찾아줘", "중복 제거", "데이터 클리닝", "형식 맞춰줘", "공백 제거".
---

# Clean Data

Clean messy data in the active sheet or a specified range.

## Preflight: Dependency Check

Before starting, verify required libraries are installed and install any that are missing.

```bash
python3 -c "import openpyxl" 2>/dev/null || python3 -m pip install openpyxl
```

**Important**: Do not skip this step — the workflow below will fail without these libraries.

## Environment

- **If running inside Excel (Office Add-in / Office JS):** Use Office JS directly. Read via `range.values`, write helper-column formulas via `range.formulas = [["=TRIM(A2)"]]`. The in-place vs helper-column decision still applies.
- **If operating on a standalone `.xlsx` file:** Use Python and `openpyxl`.

## Workflow

### Step 1: Scope

- If a range is given, such as `A1:F200`, use it.
- Otherwise use the full used range of the active sheet.
- Profile each column: detect its dominant type, text vs number vs date, and identify outliers.

### Step 2: Detect issues

| Issue | What to look for |
|---|---|
| Whitespace | Leading/trailing spaces, double spaces |
| Casing | Inconsistent casing in categorical columns like `usa`, `USA`, `Usa` |
| Number-as-text | Numeric values stored as text; stray `$`, `,`, `%` in number cells |
| Dates | Mixed formats in the same column like `3/8/26`, `2026-03-08`, `March 8 2026` |
| Duplicates | Exact-duplicate rows and near-duplicates caused by case or whitespace differences |
| Blanks | Empty cells in otherwise-populated columns |
| Mixed types | A column that is mostly numbers but has a few text entries |
| Encoding | Mojibake, non-printing characters |
| Errors | `#REF!`, `#N/A`, `#VALUE!`, `#DIV/0!` |

### Step 3: Propose fixes

Show a summary table before changing anything:

| Column | Issue | Count | Proposed Fix |
|---|---|---|---|

### Step 4: Apply

- Prefer formulas over hardcoded cleaned values. Where the cleaned output can be expressed as a formula, such as `=TRIM(A2)`, `=VALUE(SUBSTITUTE(B2,"$",""))`, `=UPPER(C2)`, or `=DATEVALUE(D2)`, write the formula in an adjacent helper column rather than computing the result in Python and overwriting the original.
- Only overwrite in place with computed values when the user explicitly asks for it, or when no sensible formula equivalent exists, such as encoding or mojibake repair.
- For destructive operations like removing duplicates, filling blanks, or overwriting originals, confirm with the user first.
- After each category of fix, whitespace, casing, number conversion, dates, dedup, show a sample of what changed and get confirmation before moving to the next category.
- Report a before/after summary of what changed.
