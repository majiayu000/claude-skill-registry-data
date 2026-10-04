---
name: ncbi-gene-search
description: Use this skill to search NCBI Gene by symbol and organism, then fetch compact official Entrez Gene summaries. Do not use it for variant interpretation, transcript-level modeling, or bulk offline annotation.
---

## Purpose
Resolve a gene symbol through NCBI E-utilities and return concise Gene database summaries.

## When to use
- You need an official Entrez Gene identifier for a symbol and species.
- You want a quick NCBI summary before a larger genomics workflow.

## When not to use
- You need transcript-level coordinates or large-batch annotation.
- You need clinical interpretation or variant effect prediction.
- You need offline execution.

## Inputs
- Gene symbol
- Optional species, maximum result count, email, and output path

## Outputs
- JSON payload containing the query, matched Gene IDs, and compact gene summaries

## Requirements
- Python 3.10+
- Network access to `eutils.ncbi.nlm.nih.gov`

## Procedure
1. Run `python3 skills/genomics/ncbi-gene-search/scripts/search_ncbi_gene.py --symbol BRCA1 --species "homo sapiens" --retmax 1 --out skills/genomics/ncbi-gene-search/assets/brca1_gene_summary.json`.
2. Inspect the `genes` list for `gene_id`, `symbol`, `description`, `organism`, and `map_location`.
3. Use the NCBI gene ID in downstream lookup or literature workflows when needed.

## Validation
- Command exits successfully.
- `search.ids` contains at least one Gene ID for a known symbol.
- The first result has a non-empty `symbol` and `organism`.

## Failure modes and fixes
- No hits: confirm the symbol and organism spelling.
- Unexpected species: make the organism explicit with `--species`.
- Too many matches: lower `--retmax` and review the returned summaries.

## Safety and limits
- Metadata lookup only.
- This skill does not perform variant interpretation or clinical classification.

## Example
- `python3 skills/genomics/ncbi-gene-search/scripts/search_ncbi_gene.py --symbol TP53 --species "homo sapiens" --retmax 1`

## Provenance
- NCBI E-utilities: https://www.ncbi.nlm.nih.gov/books/NBK25501/
- NCBI Developer APIs: https://www.ncbi.nlm.nih.gov/home/develop/api/

## Related skills
- `ensembl-gene-lookup`
- `ncbi-pubmed-search`
