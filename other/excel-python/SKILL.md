---
name: excel-python
description: >-
  Use for writing, reviewing, debugging, or testing Python code that inspects,
  edits, extracts, validates, preserves, or generates Excel .xlsx or .xlsm
  workbooks. Trigger on workbook contracts, formulas and cached values, Excel
  Tables, defined names, OOXML parts, types and precision, macros, charts,
  hidden sheets, external links, and semantic workbook verification. Do not use
  for CSV-only work, dataframe computation with no workbook boundary, Excel UI
  automation, recalculation, connection refresh, or macro execution.
argument-hint: "[workbook task, preservation requirements, and output contract]"
---

# Excel Python

Engineer Excel files from an explicit workbook contract. Preserve package
semantics, distinguish stored artifacts from Excel-runtime behavior, mutate the
smallest supported region, and prove the result by independent reopening and a
semantic comparison.

## Boundary and ownership

| Required semantics | Owner | Rule |
|---|---|---|
| Workbook/package structure, formulas, Tables, names, styles, charts, preservation | `excel-python` | Inspect OOXML and use openpyxl or XlsxWriter deliberately. |
| Tabular extraction only | Polars `read_excel` with Calamine when installed | Use when workbook layout is merely an input boundary. |
| Joins, aggregation, dtypes, nulls, lazy plans, analytical computation | `polars-python` | Hand off dataframe decisions; return only for workbook delivery. |
| Recalculation, refresh, native PDF/rendering, authorized VBA, unsupported Excel objects | installed-Excel runtime workflow | Stop and escalate; this skill never simulates Excel. |

Inspect installed APIs before relying on drift-prone behavior. Run
`python scripts/inspect_excel_env.py` from the installed skill and read
[library selection](references/library-selection.md).

## Ordered workflow

1. Recover the workbook contract from the request, workbook, callers, and
   downstream consumers. State sheet roles, Tables and names, row grain, keys,
   units, input/output regions, formula-owned columns, editable areas,
   presentation areas, compatibility, preservation, calculation, and delivery
   requirements. Prefer `cell < range < defined name < Excel Table < workbook
   contract`; use bare addresses only when no stable interface exists. Read
   [workbook contracts](references/workbook-contracts.md).
2. Preserve the source. Resolve extension, output destination, trust boundary,
   workbook date system, macros, links, and features that must survive.
3. Before editing a valuable workbook, run `python
   scripts/inspect_workbook.py INPUT.xlsx`. Treat its JSON as preflight evidence,
   not proof that openpyxl can preserve every reported part. Unknown or
   unsupported OOXML plus a preservation requirement blocks a blind round-trip.
4. Choose the operation path: Polars/Calamine for table extraction, openpyxl
   for supported existing-workbook inspection or minimal mutation, and
   XlsxWriter or Polars `write_excel` for new workbooks. Read [ingestion](references/ingestion.md),
   [existing workbooks](references/existing-workbooks.md), or
   [generation](references/generation.md).
5. Apply explicit [type and precision](references/types-and-precision.md),
   [formula](references/formulas.md), and [untrusted text](references/security.md)
   policies before writing.
6. Write to a temporary sibling, close successfully, then reopen independently.
   For edits, run `python scripts/diff_workbooks.py BEFORE AFTER`; classify each
   difference as required, acceptable serialization variation, or unexpected.
7. Run contract assertions and relevant project tests. For stakeholder output,
   render or inspect representative sheets because valid OOXML can be unusable.
   Read [semantic validation](references/validation-testing.md).

## Workbook contract invariants

- A cell format changes display, not stored arithmetic. Identifiers that can
  exceed 15 significant digits are text. Exact rounding is a value operation,
  not a number format. Define blank, empty string, `NaN`, infinity, boolean,
  date, datetime, timezone, currency, percentage, and basis-point policy.
- Preserve the 1900/1904 date system. Do not transfer raw serials across date
  systems without conversion and verification.
- Formula text, cached value, and Excel-engine recalculation are three evidence
  states: `FORMULA_TEXT_CHECKED`, `CACHE_INSPECTED`, and `RECALCULATED`. Claim
  only states actually established.
- XlsxWriter stores formulas in US-English syntax. It does not calculate them;
  absent an explicit result it stores zero and requests recalculation on open.
- Externally sourced text is text. Do not allow leading `=` or URL-like data to
  become formulas or hyperlinks implicitly; use `write_string()` or disable
  `strings_to_formulas` and `strings_to_urls` for text-first exports.
- For `.xlsm`, use `keep_vba=True`, preserve the macro-enabled extension, never
  execute VBA, and compare the VBA project hash before and after.
- Never execute macros, refresh connections, claim remote link freshness, or
  claim Excel recalculation from an openpyxl/XlsxWriter save.

## Preservation and scale gates

Inspect ZIP parts and relationships for VBA, drawings/shapes, charts,
chartsheets, pivots and caches, slicers, external links, connections/Power
Query artifacts, custom XML, embeddings, ActiveX/forms, comments/threaded
comments, media, custom properties, and unknown relationships. If a required
feature is unsupported or preservation is unknown, do not save with openpyxl;
retain the original and require an authorized Excel-native path. Read
[OOXML preservation](references/ooxml-preservation.md).

Fail before exceeding 1,048,576 rows or 16,384 columns per worksheet. Prefer a
summarized Excel view with Parquet/DuckDB/Polars for oversized analytical data.
XlsxWriter `constant_memory` requires sequential rows and disables Tables and
merged ranges; choose features before memory mode. openpyxl read-only/write-only
modes also omit normal APIs. Read [performance and limits](references/performance.md).

## Generated workbook quality

Keep machine-readable raw data separate from presentation sheets. Use named
Tables, visible units, centralized number formats, filters, useful freeze panes,
clear input/formula/output styling, stable chart sources, labeled axes, sensible
widths, and no merged cells inside data regions. Use hidden sheets only when
their role is documented in the contract. Add an optional `_meta` or About
section when provenance matters: generator/schema version, generation and
as-of timestamps, source identifiers or hashes, parameters, and code revision.
Read [presentation](references/presentation.md).

## Completion

Do not declare completion until the source remains intact; preflight risks are
resolved; the output reopens; sheet/name/Table/formula/type/date/visibility and
selected style/value contracts pass; required VBA and high-risk package parts
are unchanged; the semantic diff contains no unexplained differences; visual
review ran when presentation is contractual; and recalculation/runtime evidence
is reported separately. Use [evaluated recipes](references/recipes-core.md) only
for their stated conditions.

## References

- [Library selection and adjacent-skill routing](references/library-selection.md)
- [Workbook contracts](references/workbook-contracts.md)
- [Tabular ingestion](references/ingestion.md)
- [Types and precision](references/types-and-precision.md)
- [Formula semantics](references/formulas.md)
- [Inspection](references/inspection.md)
- [OOXML preservation](references/ooxml-preservation.md)
- [Existing-workbook mutation](references/existing-workbooks.md)
- [Generation](references/generation.md)
- [Presentation and provenance](references/presentation.md)
- [Performance and Excel limits](references/performance.md)
- [Untrusted text and security](references/security.md)
- [Semantic validation and testing](references/validation-testing.md)
- [Evaluated core recipes](references/recipes-core.md)
