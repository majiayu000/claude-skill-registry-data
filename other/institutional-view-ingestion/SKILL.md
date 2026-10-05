---
name: institutional-view-ingestion
description: Use this skill to ingest user-authorized institutional views, consensus exports, target-price summaries, or licensed research notes into structured cross-checks. Trigger when the user provides broker research, FactSet/Bloomberg/Refinitiv/Wind exports, or local institutional-view files.
---

# Institutional View Ingestion Skill

## Purpose

Ingest user-provided or publicly available institutional views into structured, auditable fields for investment analysis cross-checks.

This skill is designed for:

- Consensus estimate exports
- Rating / target price summaries
- User-provided subscription exports
- Public institutional summaries
- Short notes created by the user from licensed research

It is not designed to reproduce paid research reports.

## Safety and Copyright Rules

1. Use only user-provided files, user-authorized subscription exports, public summaries, or licensed APIs the user is allowed to use.
2. Do not bypass paywalls, scrape restricted pages, share credentials, or store API keys in the repository.
3. Do not output long excerpts from paid reports. Summarize and structure instead.
4. Do not commit raw subscription files, PDFs, spreadsheets, or licensed exports. Store them under ignored local paths such as `data/`, `institutional_reports/`, or `licensed_data/`.
5. Preserve source metadata: provider, date, ticker, document path, license scope, and user-provided status.
6. Treat institutional views as cross-checks, not as primary truth.
7. If license scope is unclear, mark the institutional view as `restricted` or `blocked`.

## Inputs

- Ticker / company
- Optional local file or folder path
- Provider or institution
- Source path or public URL
- Date / as-of date
- Rating / recommendation
- Target price
- Forecast fields, if exported
- Key assumptions
- Bull case / bear case
- Model used
- License scope

## Outputs

- Structured institutional view records
- Consensus / disagreement summary
- Differences versus our assumptions
- Source confidence
- License / copyright status
- Missing or blocked fields

## Workflow

1. Confirm source is user-provided, public, or licensed for the user.
2. If the user provides a folder, recursively discover local files and automatically select supported structured exports (`.json`, `.csv`) that match the target ticker or company.
3. Treat PDFs, Word files, spreadsheets, text dumps, and markdown notes as reference-only unless the user or an authorized export has converted them into structured fields.
4. Read only the provided local file or structured export.
5. Extract structured fields into `schemas/institutional_view.schema.json`.
6. Summarize assumptions without reproducing long copyrighted text.
7. Compare institutional assumptions against the skill's own structured assumptions.
8. Add `Institutional View Cross-check` to analysis as an optional appendix or evidence item.

## Pre-analysis Prompt

Before a current stock analysis, ask once whether institutional or licensed local files should be included. If the user gives a folder path, use:

```bash
python -m scripts.connectors.institutional_view_parser <file-or-folder> <ticker-or-company>
```

Use only the returned structured records and summary in the analysis. Mention blocked, unsupported, or reference-only files in data provenance when they are material.

## Blocking Rules

Block or downgrade use when:

- Source license is unclear.
- Raw paid report text is pasted without permission context.
- Required provider/date/ticker metadata is missing.
- The only available content is a target price with no assumptions.
- The user asks to reproduce or redistribute a paid report.
