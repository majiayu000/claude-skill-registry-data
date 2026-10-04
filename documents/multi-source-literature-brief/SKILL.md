---
name: multi-source-literature-brief
description: Use this skill to query OpenAlex, Europe PMC, Crossref, and PubMed for the same topic and build a normalized literature brief. Do not use it as a full systematic-review workflow or citation-analysis engine.
---

## Purpose
Build a compact cross-source literature brief for a query by aggregating multiple official scholarly APIs into one normalized JSON report.

## When to use
- You want a quick cross-check of literature coverage across general and biomedical indexes.
- You need a reusable JSON brief before deeper paper triage or ranking.
- You want a small overlap view by DOI or title across sources.

## When not to use
- You need exhaustive retrieval for a systematic review.
- You need full-text mining, citation graphs, or advanced deduplication.
- You need offline-only execution.

## Inputs
- Query string
- Per-source result limit
- Optional output path
- Optional NCBI/OpenAlex etiquette fields such as `--email` or `--mailto`

## Outputs
- JSON report with per-source counts, normalized top results, and cross-source overlap candidates

## Requirements
- Python 3.10+
- Network access to OpenAlex, Europe PMC, Crossref, and NCBI E-utilities

## Procedure
1. Run `python3 skills/scientific-knowledge/multi-source-literature-brief/scripts/build_literature_brief.py --query "single-cell RNA-seq" --limit 2 --out skills/scientific-knowledge/multi-source-literature-brief/assets/single_cell_literature_brief.json`.
2. Inspect the `sources` section to compare the top normalized results from each API.
3. Review `overlap_summary` to see which DOI or title candidates appear in more than one source.

## Validation
- The command exits successfully.
- All four source blocks are present.
- Each source returns at least one normalized result for a known query.

## Failure modes and fixes
- NCBI rate limiting: rerun after a short pause or pass `--email`; the wrapper already retries transient `429` responses.
- Sparse Crossref hits: keep the query phrase concise because Crossref is title-oriented here.
- Query drift across sources: use quoted phrases or a more specific biomedical term.

## Safety and limits
- This skill aggregates public bibliographic metadata only.
- It does not infer scientific truth or replace manual review.

## Example
- `python3 skills/scientific-knowledge/multi-source-literature-brief/scripts/build_literature_brief.py --query "CRISPR screen melanoma" --limit 1`

## Provenance
- OpenAlex API: https://docs.openalex.org/how-to-use-the-api/api-overview
- Europe PMC RESTful Web Service: https://europepmc.org/RestfulWebService
- Crossref REST API: https://www.crossref.org/documentation/retrieve-metadata/rest-api/
- NCBI E-utilities: https://www.ncbi.nlm.nih.gov/books/NBK25501/

## Related skills
- `openalex-literature-search`
- `europepmc-method-triage`
- `crossref-metadata-search`
- `ncbi-pubmed-search`
