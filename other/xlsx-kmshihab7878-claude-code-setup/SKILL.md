---
name: xlsx
description: "Use this skill any time a spreadsheet file is the primary input or output. This means any task where the user wants to: open, read, edit, or fix an existing .xlsx, .xlsm, .csv, or .tsv file (e.g., adding columns, computing formulas, formatting, charting, cleaning messy data); create a new spreadsheet from scratch or from other data sources; or convert between tabular file formats. Trigger especially when the user references a spreadsheet file by name or path — even casually (like \"the xlsx in my downloads\") — and wants something done to it or produced from it. Also trigger for cleaning or restructuring messy tabular data files (malformed rows, misplaced headers, junk data) into proper spreadsheets. The deliverable must be a spreadsheet file. Do NOT trigger when the primary deliverable is a Word document, HTML report, standalone Python script, database pipeline, or Google Sheets API integration, even if tabular data is involved."
license: Proprietary. LICENSE.txt has complete terms
---

# XLSX Creation, Editing, And Validation

Use this skill when the deliverable is an `.xlsx`, `.xlsm`, `.csv`, or `.tsv` file, or when an existing spreadsheet file must be read, fixed, edited, formatted, charted, cleaned, converted, or validated.

Do not use it when the primary deliverable is a Word document, HTML report, standalone Python script, database pipeline, or Google Sheets API integration.

## Required Inputs

Ask for or infer:

- Source file or source data, including sheet names and expected output path.
- Desired deliverable: new workbook, edited workbook, cleaned table, model, chart, template update, or format conversion.
- Required sheets, columns, formulas, charts, filters, pivots, tables, styling, and accessibility needs.
- Existing template conventions that must be preserved.
- Calculation expectations, formula dependencies, assumptions, and validation criteria.
- Whether formulas must remain live and recalculable.

Do not invent source data, validation output, financial assumptions, or formula results.

## Core Workflow

1. Inspect the workbook or tabular data before modifying it.
2. Choose the tool: `pandas` for data analysis and bulk reshaping; `openpyxl` for formulas, formatting, charts, workbook editing, and template preservation.
3. Preserve existing templates, sheet names, formulas, styles, and conventions unless the user asks for a redesign.
4. Build or edit sheets, tables, formulas, charts, and formatting.
5. Save the workbook.
6. If formulas were added or changed, recalculate with `python skills/xlsx/scripts/recalc.py <excel_file> [timeout_seconds]`.
7. Fix every formula error and rerun recalculation until the workbook is clean.
8. Report file path, major changes, validation results, and any limitations.

## Decision-Critical Routing

- Use `pandas` for reading, profiling, cleaning, joining, filtering, grouping, and writing simple tabular outputs.
- Use `openpyxl` for preserving formulas, modifying existing workbooks, adding Excel formulas, applying formats, creating charts, and managing multiple sheets.
- Use Excel formulas for calculated workbook values instead of hardcoding Python-calculated results.
- Use `load_workbook(..., data_only=False)` when editing formula workbooks. Saving a workbook opened with `data_only=True` can replace formulas with values.
- Preserve existing workbook conventions over these defaults.
- Use formulas, tables, named sheets, units in headers, and source notes when the workbook needs to remain auditable.

## Data Integrity And Formula Safety

- Deliver Excel workbooks with zero formula errors: `#REF!`, `#DIV/0!`, `#VALUE!`, `#N/A`, `#NAME?`, `#NULL!`, and `#NUM!`.
- Put assumptions such as growth rates, margins, multiples, and thresholds in separate cells.
- Use cell references instead of formula hardcodes.
- Verify ranges, row offsets, cross-sheet references, far-right columns, and denominator safety.
- Test formulas on a few cells before filling large regions.
- Include edge cases: zero values, negative values, blanks, and large values.
- Document hardcoded inputs with source notes where appropriate.

## Styling And Accessibility

- Use a consistent professional font unless the user or template says otherwise.
- Match existing formatting exactly when updating templates.
- Use clear headers, frozen panes, filters, sensible widths, and readable number formats.
- Include units in headers such as `Revenue ($mm)`.
- Do not rely on color alone to communicate meaning.
- For financial models, default to standard conventions unless the template overrides them:
  - Blue text: user-editable hardcoded inputs.
  - Black text: formulas and calculations.
  - Green text: links to other worksheets in the same workbook.
  - Red text: external file links.
  - Yellow fill: key assumptions or cells requiring attention.

## Validation Gates

- Workbook opens successfully.
- Sheet names, row counts, column counts, and key headers match expectations.
- Formulas are live where calculations are required.
- Recalculation reports zero formula errors when formulas exist.
- Template styles and formulas are preserved when editing existing files.
- Formatting is readable and consistent.
- Source notes, assumptions, and units are present where required.
- No secrets, credentials, private context, local paths, or personal identifiers are added.

## Output Expectations

Return:

- Output workbook path.
- Summary of sheets, tables, formulas, charts, and formatting changed.
- Validation commands run and result summary.
- Formula error status and recalc result when applicable.
- Any assumptions, skipped validation, or user follow-ups.

## Minimal Examples

Formula-first calculation:

```python
sheet["B10"] = "=SUM(B2:B9)"
sheet["C5"] = "=(C4-C2)/C2"
```

Recalculate formulas:

```bash
python skills/xlsx/scripts/recalc.py output.xlsx 30
```

## Reference Map

- [Workbook workflow](references/workbook-workflow.md)
- [Formatting and layout](references/formatting-and-layout.md)
- [Formulas, charts, and tables](references/formulas-charts-and-tables.md)
- [Validation, troubleshooting, and anti-patterns](references/validation-troubleshooting-and-antipatterns.md)
- [Examples and templates](references/examples.md)
