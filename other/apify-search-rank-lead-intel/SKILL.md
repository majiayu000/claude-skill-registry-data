---
name: apify-search-rank-lead-intel
description: Reverse-engineer local search rankings for any industry with Apify, preserve input query/location/rank metadata, classify fit, roll up companies by place ID, and prepare accepted businesses for enrichment. Use when building ranked lead lists, competitor maps, or niche reseller/operator discovery workflows.
---

# Apify Search Rank Lead Intel

Use this workflow to discover which companies appear for target local searches and where they rank.

## Procedure

1. Configure search terms, include terms, exclude terms, and rank buckets.
2. Prepare a city/county/state location grid.
3. Run `src/rank_discovery.py --dry-run`.
4. Run one paid batch with `--max-batches 1`.
5. Inspect raw JSON, parsed rank CSVs, and confidence classifications.
6. Run `src/rollup_rankings.py` to dedupe companies while keeping all query/rank appearances.
7. Send accepted rows to website/contact/email enrichment.

## Guardrails

- Preserve `input_query`, `query_location`, and `result_rank` before dedupe.
- Dedupe company records by `place_id`, but keep a separate rank-appearances table.
- Exclude off-audience rows before paid enrichment.
- Keep API tokens only in `.env` or runtime environment variables.

