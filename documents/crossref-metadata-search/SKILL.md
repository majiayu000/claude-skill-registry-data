---
name: crossref-metadata-search
description: Use this skill to search Crossref metadata when you need DOI-oriented citation records from the official REST API. Do not use it when you need full text or publisher-specific access controls.
---

## Purpose
Search Crossref works metadata and save a structured JSON result set for citation discovery and DOI lookup.

## When to use
- You need DOI-rich bibliographic metadata.
- You want a publisher-agnostic metadata pass to complement OpenAlex or PubMed.

## When not to use
- You need article full text.
- You need biomedical indexing fields unique to PubMed or Europe PMC.

## Inputs
- Title or topic query
- Optional `--rows` and `--out`

## Outputs
- Crossref `work-list` JSON payload

## Requirements
- Python 3.13+
- Network access to `api.crossref.org`

## Procedure
1. Run `python3 skills/scientific-knowledge/crossref-metadata-search/scripts/search_crossref.py --query-title "single-cell RNA-seq" --rows 3 --out skills/scientific-knowledge/crossref-metadata-search/assets/crossref_single_cell.json`.
2. Inspect `message.total-results` and `message.items`.
3. Use returned DOIs as anchors for follow-up literature or provenance work.

## Validation
- Command exits successfully.
- Output JSON contains `message-type` equal to `work-list`.
- At least one item is returned for a common topic.

## Failure modes and fixes
- Empty results: simplify the title query.
- Rate or service issues: retry with smaller `--rows` and a descriptive user agent.

## Safety and limits
- Metadata only; access to full content depends on publishers.
- Respect Crossref polite-use expectations.

## Examples
- `python3 .../search_crossref.py --query-title "spatial transcriptomics" --rows 2`

## Provenance
- Crossref REST API docs: https://www.crossref.org/documentation/retrieve-metadata/rest-api/

## Related skills
- `openalex-literature-search`
- `ncbi-pubmed-search`
