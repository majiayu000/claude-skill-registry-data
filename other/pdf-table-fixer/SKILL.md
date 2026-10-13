---
name: pdf-table-fixer
description: "Use when the user has a tagged PDF whose tables fail accessibility checks or read badly in a screen reader (for example 'fix the table headers in this PDF', 'my PDF tables fail PDF/UA', 'repair the table tags')."
---

# PDF Table Fixer

## Overview

Repairs the table structure of a PDF that is already tagged: header cells and their scope, row and column spans, header links, and the order of rows and cells. It does not tag untagged PDFs, write alt text or fix anything outside tables. Scripts read and write the PDF and do all checking; you read their evidence and write a small plan. Nothing is written until the user has seen the diff and said yes, and the original file is never changed.

## The scripts

In this skill's `scripts/` folder. They need Python 3 and `pikepdf` (`python -m pip install pikepdf`); validation also needs Java and veraPDF. If `pikepdf` is missing a script says so and exits 2; tell the user how to install it and stop. Use `python3`, or `python` / `py -3`, whichever works.

- `tables.py inspect IN.pdf [--json]`: read-only. Lists each table (`t1`, `t2`, ...) with its rows, cells (type, text, scope, spans, ids) and the problems it can prove from the file.
- `tables.py plan-diff IN.pdf --plan PLAN.json`: checks the plan against the file and prints what would change. Writes nothing.
- `tables.py apply IN.pdf --plan PLAN.json --out OUT.pdf`: applies the plan to a new file. Refuses to overwrite the input. Exit 2 means a refusal or a bad plan (nothing written); exit 3 means the output failed its own check (nothing written).
- `verapdf_check.py FILE.pdf [--against BEFORE.pdf]`: runs veraPDF with the PDF/UA-1 profile and compares before and after.

## The plan file

JSON, one entry per table id from `inspect`. Every index is the one `inspect` printed. Allowed keys per table, nothing else:

- `expect`: `{"rows": N, "cells": M}`, copied from `inspect --json` (`rows_count`, `cells_count`). Required: a plan without it is refused, because it is what stops a plan from being applied to the wrong file.
- `header_rows`, `header_cols`: how many rows at the top and columns at the left are headers. If you give either, you are declaring every header in the table; any other cell becomes a plain data cell.
- `spans`: `[{"row": r, "cell": i, "rowspan": n, "colspan": m}]`.
- `row_order`: the old row numbers in their new order (rows stay in their THead/TBody/TFoot section). `cell_order`: `{"<old row>": [old cell numbers in new order]}`.
- `headers`: `{"<row>.<cell>": ["<row>.<cell>", ...]}`, a data cell mapped to the header cells it falls under, for tables whose headers need more than a scope (two or more header levels, irregular spans). An empty list clears a cell's existing Headers (needed when a cell it pointed at stops being a header).

Example:

```json
{"tables": {"t1": {"expect": {"rows": 3, "cells": 6}, "header_rows": 1, "header_cols": 1}}}
```

## Process

1. **Inspect.** Run `tables.py inspect IN.pdf`. If it says untagged, encrypted or signed, say so and stop; this skill cannot help with that file. If it finds no tables, say so and stop.
2. **Read the evidence.** For each table look at the problem list and the cells' text. A problem is something the file proves (a span past the grid, no header cells, a TH with no scope, rows or cells drawn out of order). Which cells are headers is your judgment from the text; where the text does not settle it, ask the user one question instead of guessing. Never quote document text beyond what you need to identify a table or cell.
3. **Write the plan** to a file next to the PDF's output, with `expect` for every table.
4. **Show the diff.** Run `plan-diff`, show the changes per table, and wait for the user's yes. If it prints errors, fix the plan; do not argue with the check.
5. **Apply.** Run `apply` with a new `--out` path (for example `NAME-tables-fixed.pdf`).
6. **Validate.** Run `verapdf_check.py OUT.pdf --against IN.pdf`. Report the table-related failures before and after, anything fixed, and any regression (a rule that fails now and did not before) even if the total went down. If it prints `not validated`, say so plainly; never call the file compliant.

## What to tell the user

- The checks prove the structure is consistent, not that the headers are the semantically right ones; that rests on your reading and their review of the diff.
- veraPDF's PDF/UA-1 rules are the only judge here. PAC may disagree on some rules; this skill makes no claim about PAC.
- The text of a cell is read from the page's fonts; if a font gives no readable text, `inspect` flags `text_unreadable` and you should ask the user what the cell says.
- Row and cell order evidence comes from where the text is drawn; it is approximate.
- Saving rewrites the whole file, so a digital signature would break; signed files are refused.

## Common mistakes

| Mistake | Fix |
| --- | --- |
| Declaring `header_rows` for a table that has a header column too | Give `header_cols` as well, or the left column becomes plain data cells |
| Using new row numbers in `spans` or `headers` after a `row_order` | All indices are the original ones from `inspect` |
| Skipping `expect` | It is required; copy `rows_count` and `cells_count` from `inspect --json` |
| Calling the result accessible after a veraPDF pass | Say what was checked: veraPDF PDF/UA-1 only |
