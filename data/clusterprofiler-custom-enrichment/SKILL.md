---
name: clusterprofiler-custom-enrichment
description: Use this skill to run deterministic local custom enrichment with Bioconductor clusterProfiler and user-supplied TERM2GENE tables. Do not use it for remote annotation downloads or organism database lookups.
---

## Purpose
Run a compact over-representation analysis with local query genes, local `TERM2GENE`, and local `TERM2NAME` tables through Bioconductor `clusterProfiler`.

## When to use
- You want a deterministic enrichment example without online annotation services.
- You already have a short gene list and local term mappings.

## When not to use
- You need GO, KEGG, Reactome, or remote annotation queries.
- You need large production enrichment workflows with plotting/reporting layers.

## Inputs
- Query gene file with one gene per line
- `TERM2GENE` TSV with columns `term` and `gene`
- `TERM2NAME` TSV with columns `term` and `name`
- Optional local R library path and `--install-missing`

## Outputs
- Compact JSON summary of enrichment results with p-values, adjusted p-values, gene ratios, and matched genes

## Requirements
- `Rscript`
- `jsonlite`
- Bioconductor `clusterProfiler` for package-backed execution

## Procedure
1. Inspect the toy files in `examples/toy_query_genes.txt`, `examples/toy_term2gene.tsv`, and `examples/toy_term2name.tsv`.
2. Optionally prepare a temp Bioconductor library, then run `Rscript skills/systems-biology/clusterprofiler-custom-enrichment/scripts/run_clusterprofiler_custom_enrichment.R --lib-dir /tmp/bioc-skill-lib --install-missing --out clusterprofiler_summary.json`.
3. Review `results` for `term`, `description`, `gene_ratio`, `p_adjust`, and `gene_ids`.

## Validation
- `--describe-toy` returns the expected toy gene and term counts.
- A package-backed run returns at least one enriched term for the bundled toy example.

## Failure modes and fixes
- Missing `clusterProfiler`: rerun with `--install-missing --lib-dir <path>`.
- `gdtools` or `ggiraph` build failures: install Cairo and FreeType development headers before retrying the Bioconductor stack.
- Empty results: inspect the overlap between the query genes and `TERM2GENE`.
- Wrong term labels: confirm the `TERM2NAME` table keys match the `TERM2GENE` term IDs exactly.

## Safety and limits
- Uses only local custom term mappings.
- Does not fetch remote annotations or make claims beyond the supplied toy or local input data.

## Example
- `Rscript skills/systems-biology/clusterprofiler-custom-enrichment/scripts/run_clusterprofiler_custom_enrichment.R --describe-toy`

## Provenance
- Bioconductor clusterProfiler package page: https://bioconductor.org/packages/clusterProfiler
- clusterProfiler manual: https://bioconductor.org/packages/release/bioc/manuals/clusterProfiler/man/clusterProfiler.pdf

## Related skills
- `fgsea-preranked-enrichment`
- `reactome-identifiers-enrichment`
