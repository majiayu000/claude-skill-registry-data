---
name: fgsea-preranked-enrichment
description: Use this skill to run deterministic toy or local custom preranked gene-set enrichment with Bioconductor fgsea. Do not use it for remote annotation lookups or large cohort-scale pathway workflows.
---

## Purpose
Run preranked enrichment with a local ranked-statistics table and local pathway definitions through Bioconductor `fgsea`.

## When to use
- You already have a ranked gene statistics vector from a differential expression or scoring workflow.
- You want a deterministic enrichment example that depends only on local pathway definitions.

## When not to use
- You need remote MSigDB, Reactome, or annotation downloads.
- You need large production enrichment workflows with reporting layers.

## Inputs
- Ranked stats TSV with columns `gene` and `score`
- Pathway membership TSV with columns `pathway` and `gene`
- Optional local R library path and `--install-missing`

## Outputs
- Compact JSON summary of fgsea results with ES, NES, p-values, adjusted p-values, and leading-edge genes

## Requirements
- `Rscript`
- `jsonlite`
- Bioconductor `fgsea` for package-backed execution

## Procedure
1. Inspect the toy files in `examples/toy_ranked_stats.tsv` and `examples/toy_pathways.tsv`.
2. Optionally prepare a temp Bioconductor library, then run `Rscript skills/systems-biology/fgsea-preranked-enrichment/scripts/run_fgsea_preranked.R --lib-dir /tmp/bioc-skill-lib --install-missing --out fgsea_summary.json`.
3. Review `results` for `pathway`, `NES`, `padj`, and `leadingEdge`.

## Validation
- `--describe-toy` returns the expected toy gene and pathway counts.
- A package-backed run returns at least one enriched pathway for the bundled toy example.

## Failure modes and fixes
- Missing `fgsea`: rerun with `--install-missing --lib-dir <path>`.
- Empty results: lower `--min-size` or inspect the ranked-statistics directionality.
- Non-deterministic values: keep the input files fixed and set `--seed`.

## Safety and limits
- Uses only local custom pathways and local ranked statistics.
- Does not fetch or infer biological annotations from remote services.

## Example
- `Rscript skills/systems-biology/fgsea-preranked-enrichment/scripts/run_fgsea_preranked.R --describe-toy`

## Provenance
- Bioconductor fgsea package page: https://bioconductor.org/packages/fgsea
- fgsea tutorial: https://bioconductor.org/packages/release/bioc/vignettes/fgsea/inst/doc/fgsea-tutorial.html

## Related skills
- `reactome-identifiers-enrichment`
- `clusterprofiler-custom-enrichment`
