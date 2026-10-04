---
name: ensembl-gene-lookup
description: Use this skill to resolve a gene symbol to Ensembl IDs and fetch a canonical Ensembl gene record. Do not use it for full transcript annotation pipelines or offline work.
---

## Purpose
Resolve a gene symbol through Ensembl REST and return the corresponding gene lookup payload.

## When to use
- You need a quick official Ensembl gene identifier lookup.
- You want lightweight gene metadata before a larger genomics workflow.

## When not to use
- You need transcript-level or large-batch annotation.
- You need local-only execution.

## Inputs
- Gene symbol
- Optional species and output path

## Outputs
- JSON payload containing the xref candidates and the selected lookup record

## Requirements
- Python 3.13+
- Network access to `rest.ensembl.org`
- Example asset fallback exists for the curated `BRCA1` and `BRCA2` examples if the live API is temporarily unavailable.

## Procedure
1. Run `python3 skills/genomics/ensembl-gene-lookup/scripts/lookup_gene.py --symbol BRCA1 --out skills/genomics/ensembl-gene-lookup/assets/brca1_lookup.json`.
2. Inspect `xrefs` to confirm the chosen gene ID.
3. Use the `lookup` block for coordinates and display name.

## Validation
- Command exits successfully.
- At least one xref is returned for a known symbol.
- Lookup block includes `id`, `display_name`, and coordinates.

## Failure modes and fixes
- No hits: confirm species and capitalization.
- Multiple matches: filter by `type == gene` and inspect the candidates.
- Official API timeout: rerun once; the curated BRCA example assets can still support deterministic example execution.

## Safety and limits
- Metadata lookup only.
- Large-scale annotation should use more specialized batch tooling.

## Examples
- `python3 .../lookup_gene.py --symbol TP53 --species homo_sapiens`

## Provenance
- Ensembl REST API: https://rest.ensembl.org/
- Ensembl lookup documentation: https://rest.ensembl.org/documentation/info/lookup

## Related skills
- `scanpy-qc-starter`
