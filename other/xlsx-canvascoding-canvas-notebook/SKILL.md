---
name: xlsx
description: "Use this Canvas-owned clean-room skill when a spreadsheet file is the primary input or output. Trigger for `.xlsx`, `.xls`, `.xlsm`, `.csv`, `.tsv`, workbooks, templates, trackers, models, dashboards, charts, formulas, data cleaning, formatting, validation, recalculation, and Google Sheets-targeted handoff."
license: "Canvas Notebook Sustainable Use License"
---

# XLSX Spreadsheets

This skill covers spreadsheet creation, editing, analysis, visualization, and
verification in Canvas Notebook. It is a clean-room Canvas skill; do not copy
vendor skill material, hidden prompts, or proprietary helper code into this
folder.

## Core Contract

- Use `CANVAS_AGENT_TEMP_DIR` for scripts, working copies, recalculation output,
  exports, and render previews. Promote only the requested final workbook to the
  workspace with `copy_path` or `move_path`.
- Preserve existing workbook conventions for targeted edits.
- For new workbooks, design the workbook structure first: summary/dashboard,
  inputs, assumptions, source data, calculations, checks, and outputs as needed.
- Keep formulas auditable and user-editable. Prefer formulas over hardcoded
  derived numbers when the workbook is meant to be reused.
- Avoid hidden scratch state in the final workbook unless the user asks for it.
- Return only the final spreadsheet unless the user asks for intermediate CSV,
  render, or validation files.

## Recommended Tools

- `openpyxl` for XLSX creation, formatting, formulas, charts, validation, and
  structural inspection.
- `pandas` for data cleaning, joins, grouping, and statistical preparation.
- LibreOffice `soffice` for formula recalculation and export checks. Before
  invoking it, read
  [references/headless-libreoffice.md](references/headless-libreoffice.md).
- CSV/TSV readers from the Python standard library for malformed lightweight
  tabular files when pandas would hide parsing issues.

## Workflow

1. Classify the task: create, edit, analyze, clean, model, dashboard, chart,
   convert, or inspect.
2. For existing workbooks, inspect sheet names, dimensions, formulas, tables,
   charts, defined names, validations, merged cells, freeze panes, and styles.
3. Make edits in the narrowest reliable scope. Extend formulas, tables,
   validations, and conditional formatting when adding rows or columns.
4. For new analytical workbooks, separate raw inputs from calculations and
   presentation sheets. Add checks when correctness depends on linked formulas.
5. If LibreOffice recalculation is needed, write its result to scratch with a
   unique headless profile, then reopen that result with `openpyxl` and verify
   formulas, cached values where available, dimensions, styles, frozen panes,
   filters, charts, and visible sheet order.

## Spreadsheet Quality Rules

- Use clear sheet names and freeze panes for large tables.
- Format dates, currency, percentages, and units explicitly.
- Keep column widths readable without excessive whitespace.
- Use consistent header, input, formula, and output styling.
- Add source notes for externally sourced hardcoded values.
- For financial or operational models, include checks for balance, totals,
  missing inputs, and formula error cells.

## Google Sheets Target

For a new Google Sheets deliverable, create a clean `.xlsx` first and verify it.
Then use the available import or upload workflow in the host app. Avoid Excel
features that import poorly unless the user specifically needs them.

## Final Checks

- Workbook opens without repair warnings.
- No unintended formula errors remain.
- Charts and tables point to the intended ranges.
- Filters, freeze panes, widths, formats, and sheet order are intentional.
- Any recalculation or render limitation is clearly reported.
