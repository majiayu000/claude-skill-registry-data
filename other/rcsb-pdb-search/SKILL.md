---
name: rcsb-pdb-search
description: Use this skill to search the Protein Data Bank through the official RCSB Search API when you need structure identifiers from a free-text query. Do not use it when you need structure download or coordinate parsing.
---

## Purpose
Run lightweight RCSB PDB entry searches and save the result set as JSON.

## When to use
- You need a quick structure search from a protein, ligand, or concept keyword.
- You want PDB entry IDs for downstream structural analysis.

## When not to use
- You need mmCIF/PDB coordinate files.
- You need local structural parsing rather than remote search.

## Inputs
- Query string
- Optional `--rows` and `--out`

## Outputs
- Search API JSON containing PDB entry identifiers

## Requirements
- Python 3.13+
- Network access to `search.rcsb.org`

## Procedure
1. Run `python3 skills/structural-biology/rcsb-pdb-search/scripts/search_rcsb.py --query hemoglobin --rows 3 --out skills/structural-biology/rcsb-pdb-search/assets/hemoglobin_results.json`.
2. Review `total_count` and `result_set`.

## Validation
- Command exits successfully.
- Output JSON contains `result_set`.
- At least one structure ID is returned for a common query.

## Failure modes and fixes
- Empty results: broaden the text query.
- HTTP errors: retry later or reduce result count.

## Safety and limits
- This is a metadata search skill, not a molecular modeling workflow.

## Examples
- `python3 .../search_rcsb.py --query "p53" --rows 2`

## Provenance
- RCSB Search API docs: https://search.rcsb.org/

## Related skills
- `ensembl-gene-lookup`
