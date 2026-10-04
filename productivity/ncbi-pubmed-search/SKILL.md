---
name: ncbi-pubmed-search
description: Use this skill to search PubMed through NCBI E-utilities when you need official Entrez-backed literature discovery and summary metadata. Do not use it when you need full text or network-free execution.
---

## Purpose
Run a PubMed search through NCBI E-utilities and optionally fetch summary metadata for the returned PMIDs.

## When to use
- You need a canonical PubMed search path.
- You want lightweight official metadata for biomedical literature triage.

## When not to use
- Full text is required.
- A Europe PMC workflow already covers the task better.

## Inputs
- Search term
- Optional `--retmax`, `--email`, and `--out`

## Outputs
- Combined JSON payload with `search` and `summary` sections

## Requirements
- Python 3.13+
- Network access to `eutils.ncbi.nlm.nih.gov`

## Procedure
1. Run `python3 skills/scientific-knowledge/ncbi-pubmed-search/scripts/search_pubmed.py --term "single-cell RNA-seq" --retmax 3 --out skills/scientific-knowledge/ncbi-pubmed-search/assets/pubmed_single_cell.json`.
2. Inspect `search.esearchresult.idlist`.
3. Review `summary.result` for titles, journals, and dates.

## Validation
- Command exits successfully.
- Search returns at least one PMID for a common query.
- Summary payload includes the returned UID keys.

## Failure modes and fixes
- Empty results: broaden the term or use a synonym.
- Courtesy warnings: supply `--email` for traceable requests.

## Safety and limits
- Metadata discovery only.
- Respect NCBI usage guidance and avoid unnecessary high-rate polling.

## Examples
- `python3 .../search_pubmed.py --term "spatial transcriptomics benchmark" --retmax 2`

## Provenance
- NCBI E-utilities guide: https://www.ncbi.nlm.nih.gov/books/NBK25501/
- NCBI developer API landing page: https://www.ncbi.nlm.nih.gov/home/develop/api/

## Related skills
- `europepmc-method-triage`
- `crossref-metadata-search`
