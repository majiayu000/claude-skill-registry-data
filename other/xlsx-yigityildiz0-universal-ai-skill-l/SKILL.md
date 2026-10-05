---
name: xlsx
description: Read, create, edit, clean, calculate, chart, and validate XLSX/XLSM workbooks while preserving formulas, styles, names, links, macros, and user conventions. Use when a spreadsheet is the primary input or deliverable; never claim formulas were recalculated unless a real calculation engine verified them.
license: MIT
---

# Spreadsheet Workflow

## Inspect before editing

Inventory workbook type, sheets/visibility, used ranges, tables, names, formulas, cached results, charts, pivots, validation, conditional formats, external links, protection, macros, and file size. Load untrusted workbooks without executing macros or external links.

Choose tooling already available:

- dataframe tools for data cleaning/analysis;
- workbook libraries for formulas, formatting, charts, validations, and OOXML preservation;
- a real spreadsheet engine for recalculation/rendering when required.

Do not install packages or office software implicitly.

## Editing rules

1. Preserve the original and write to a new output unless replacement is explicit.
2. Follow the workbook's existing styles, units, locale, date system, formula separators, and sheet organization.
3. Make narrow changes; avoid recreating the workbook when editing would preserve more features.
4. Preserve VBA with a macro-aware mode when required, but never execute it. Warn that some libraries cannot safely round-trip every macro, pivot, slicer, signature, or embedded object.
5. Escape CSV cells that could trigger spreadsheet formula injection when exporting untrusted text.
6. Keep source inputs, formulas, assumptions, and outputs visually and structurally distinguishable without relying on color alone.
7. Use formulas for auditable derived values; avoid hard-coded totals. Add divide-by-zero, missing-data, and boundary handling intentionally.
8. Do not refresh external data connections or upload workbook data without authorization.

## Creation quality

Use descriptive sheet/table names, frozen headers where useful, filters, consistent number formats, realistic column widths, documented units, and a concise assumptions/readme sheet for complex models. Charts need a stated insight, labeled axes/units, readable legends, and source ranges that expand correctly.

## Validation

- reopen the output with an independent reader;
- compare sheet names, dimensions, formulas, styles, names, links, and macro presence with the source;
- scan formulas/cached results for `#REF!`, `#DIV/0!`, `#VALUE!`, `#NAME?`, and unintended blanks;
- recalculate with an installed spreadsheet engine when outputs depend on formulas, then reopen and verify cached values;
- inspect rendered sheets/charts at practical zoom levels;
- test a few edge-case inputs and totals independently.

Report output path, rows/sheets changed, calculation engine used or not used, preserved/unsupported features, and validation results.
