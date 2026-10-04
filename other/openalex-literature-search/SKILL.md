---
name: openalex-literature-search
description: Use this skill to run fast literature triage against OpenAlex when you need public paper metadata, citation-linked context, and structured JSON output. Do not use it when you need full text, proprietary databases, or offline execution.
---

## Purpose
Search OpenAlex works metadata and save a reproducible JSON result set for paper triage.

## When to use
- You need a quick literature sweep for a topic or method.
- You want machine-readable metadata for downstream ranking or deduplication.

## When not to use
- You need full-text content or article annotations.
- You are working without network access.

## Inputs
- Search query string
- Optional `--per-page`, `--mailto`, and `--out`

## Outputs
- JSON payload from the OpenAlex works search endpoint

## Requirements
- Python 3.13+
- Network access to `api.openalex.org`

## Procedure
1. Run `python3 skills/scientific-knowledge/openalex-literature-search/scripts/search_openalex.py --query "single-cell RNA-seq" --per-page 5 --out skills/scientific-knowledge/openalex-literature-search/assets/openalex_single_cell.json`.
2. Inspect the `meta` block for `count` and pagination.
3. Use the first-pass results to rank or expand follow-up searches.

## Validation
- Command exits successfully.
- Output JSON contains `meta` and `results`.
- `results` is non-empty for a known topic.

## Failure modes and fixes
- HTTP 403 or throttling: provide `--mailto` and reduce request rate.
- Empty results: broaden the query or remove over-specific phrasing.

## Safety and limits
- This skill surfaces public metadata only.
- Respect API terms and do not turn literature discovery into unsafe experimental planning.

## Examples
- `python3 .../search_openalex.py --query "spatial transcriptomics benchmark" --per-page 3`

## Provenance
- OpenAlex API overview: https://docs.openalex.org/how-to-use-the-api/api-overview

## Related skills
- `europepmc-method-triage`
