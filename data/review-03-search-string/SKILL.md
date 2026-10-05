---
name: review-03-search-string
description: Build reproducible search strategies for PubMed, Web of Science, Embase, Cochrane, Scopus, CNKI, and preprint databases. Use when preparing medical review search strings from a locked question.
---

# Review 03 Search String

## Purpose

Generate transparent, database-specific search strings that can be copied into each database and audited later.

## Required Inputs

- `question_lock.md`.
- Date range, language restrictions, article types, and required databases.
- Whether the review is systematic or narrative.

## Output

Create `02_search_strategy/search_strategy.md` with:

- Concept blocks and synonyms.
- PubMed search string with MeSH and Title/Abstract terms when appropriate.
- Web of Science Topic search.
- Embase Emtree strategy if Embase is available.
- Cochrane strategy for intervention reviews.
- Search notes for Chinese databases if needed.
- Pilot-search adjustment log.

## Completion Gate

Pass only when every search string has database name, date prepared, fields, Boolean logic, and planned filters.

## Stop Rules

Do not silently add restrictive filters that could bias the search. Mark optional filters separately.
