---
name: reactome-identifiers-enrichment
description: Use this skill to submit a short identifier list to Reactome Analysis Service and return compact pathway enrichment summaries. Do not use it for full downstream statistical analysis or unsupported identifier normalization.
---

## Purpose
Run a lightweight Reactome pathway over-representation query from a small list of identifiers and summarize the top enriched pathways.

## When to use
- You have a short list of genes or other supported identifiers and need quick pathway context.
- You want a compact Reactome enrichment snapshot before a larger systems-biology workflow.

## When not to use
- You need a complete enrichment pipeline with custom background models.
- You need offline execution.
- You need unsupported identifier conversion or pathway visualization.

## Inputs
- Identifier list via `--identifiers` or `--input-file`
- Optional page size, page number, and output path

## Outputs
- JSON payload with query metadata, top pathway summaries, species coverage, resource coverage, and not-found identifiers

## Requirements
- Python 3.10+
- Network access to `reactome.org`

## Procedure
1. Run `python3 skills/systems-biology/reactome-identifiers-enrichment/scripts/analyze_reactome_identifiers.py --identifiers BRCA1,TP53 --page-size 5 --out skills/systems-biology/reactome-identifiers-enrichment/assets/brca1_tp53_enrichment.json`.
2. Inspect `pathways` for `stable_id`, `name`, `species`, `entities_fdr`, `entities_p_value`, and `reactions_found`.
3. Review `identifiers_not_found` before using the results downstream.

## Validation
- Command exits successfully.
- `pathways` contains at least one Reactome stable ID for a known human gene list.
- The first pathway has non-empty `stable_id`, `name`, and numeric enrichment statistics.

## Failure modes and fixes
- No pathways returned: check the identifiers and reduce the list to supported gene symbols or IDs.
- Many missing identifiers: provide one symbol or accession per line or comma-separated item.
- HTTP errors: retry later and keep the identifier list small for smoke validation.

## Safety and limits
- Knowledge lookup only.
- This skill does not justify biological claims on its own and does not replace statistical study design.

## Example
- `python3 skills/systems-biology/reactome-identifiers-enrichment/scripts/analyze_reactome_identifiers.py --identifiers BRCA1,TP53 --page-size 3`

## Provenance
- Reactome Analysis Service docs: https://reactome.org/dev/analysis
- Reactome platform: https://reactome.org/

## Related skills
- `reactome-event-summary`
- `ncbi-gene-search`
