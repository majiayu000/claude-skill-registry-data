---
name: review-04-search-execution
description: Execute or document literature searches and create a reproducible search log. Use when running database searches, exporting records, recording hit counts, and preparing deduplication inputs.
---

# Review 04 Search Execution

## Purpose

Record exactly what was searched so the review can be reproduced and defended during peer review.

## Required Inputs

- `02_search_strategy/search_strategy.md`.
- Database access status.
- Export format preference: RIS, BibTeX, CSV, NBIB, or Zotero collection.

## Output

Create or update:

- `03_search_records/search_log.csv`.
- `03_search_records/export_manifest.md`.
- Raw export files if provided by the user.

## Completion Gate

Pass only when each database has search date, exact search string, date range, filters, result count, export filename, and operator notes.

## Stop Rules

Do not fabricate result counts. If a database cannot be searched, record it as unavailable with reason.
