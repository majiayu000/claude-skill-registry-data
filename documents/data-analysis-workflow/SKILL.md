---
name: data-analysis-workflow
description: Use this skill when the task is open-ended analysis of local files or mixed data sources in this repository, especially CSV, XLSX, PDF, DOCX, PPTX, JSON, text, HTML, XML, or folders of related evidence. It provides the default workflow, helper scripts, and output conventions for reproducible data exploration in Codex.
---

# Data Analysis Workflow

Use this skill for exploratory analysis, document review, dataset triage, metric investigation, or mixed-source fact finding inside this repo.

Default source rule: if the user does not name a path, start from `workspace/input/`.

## Default Workflow

1. Inventory the input files.
2. Run `scripts/file_profile.py` on the likely inputs.
3. Split the work by source type:
   - Tabular: CSV, TSV, XLSX, JSON, parquet-like exports
   - Document: PDF, DOCX, PPTX, TXT, MD, HTML, XML
   - Mixed folders: create a short source map first
4. Create reproducible analysis:
   - SQL in `workspace/sql/`
   - Notes in `workspace/notes/`
   - Charts and exports in `workspace/artifacts/`
5. End with findings, caveats, and suggested next drills.

## Scripts

- `scripts/file_profile.py`
  Use first for profiling a file or folder. It prints a compact summary of structure, schema, sample content, and likely analysis directions.
- `scripts/query_tabular.py`
  Use for SQL over one or more tabular files. It registers files as DuckDB tables and returns markdown, CSV, or JSON output.
- `scripts/chart_from_query.py`
  Use when a chart should be produced from a repeatable SQL query rather than one-off notebook code.

## Source-Type Guidance

- For CSV/XLSX/JSON tabular data, prefer SQL or pandas over manual reading.
- For PDFs and DOCX files, extract text first, then summarize sections and search for anchors before making claims.
- For PPTX files, treat slide titles and bullets as the first-pass structure.
- For unknown formats, inspect metadata and fall back to raw text or binary summary rather than guessing.

## Reporting Standard

Every substantial analysis should leave behind at least one durable artifact:

- a note with the question, method, caveats, and findings
- a SQL file or Python snippet if the analysis is likely to be reused
- a chart or export when it materially helps interpretation

## References

Read these only when needed:

- `references/workflow-recipes.md` for concrete investigation patterns
- `references/output-conventions.md` for where to store results and how to name them
