---
name: coresh-signature-search
description: "CoReSh signature search with bulkiRNA. Ranks ~86,000 public GEO datasets by how strongly a 10-200 gene Entrez query is coregulated in each (pct_var, optional GESECA p-value), finds hits shared across queries, and turns top hits into a gene-set database for GSEA. For canonical pathways use bulk-rnaseq-gsea."
license: MIT
---

# CoReSh signature search

CoReSh (Sukhov et al., *NAR* 2025) scores one gene set against every dataset in a preprocessed
GEO compendium: 44,253 human and 42,224 mouse series. The score is GESECA's: the variance the
query genes carry along their own summed profile, as a percentage of the dataset's total
variance. It needs no contrast, so one query sweeps datasets of any design. Use it to find
public contexts where a signature moves together, then derive context-specific gene sets.

bulkiRNA implements the method. Load it and call the exports; `skills/bulkirna` holds the
general recipe and the rules for every bulk stage.

```r
library(bulkiRNA)
coresh_validate(species = "human")   # preflight: packages, chunk tree, first chunk
?coresh_search                       # each export documents its contract
```

## Rules this skill imposes

1. **Smoke-test on the web UI first.** Run the signature at
   <https://alserglab.wustl.edu/coresh>, then locally, and compare top accessions.
2. **Queries are named lists of integer Entrez vectors.** Build them with `gene_to_entrez()`.
   Each needs at least three unique IDs. Keep the exact IDs in project config: provenance
   records query names and sizes only.
3. **Query the compendium of the query's species.** `species = "mouse"` reads `mmu/`. A human
   query on mouse chunks scores near-zero `size` with no error.
4. **Keep `(gse, gpl)` together.** A GSE accession alone is not unique in the compendium.
5. **Report the `p_value` ranking unadjusted.** One seed is reset for every dataset, so the
   p-values are not independent. `p.adjust()` on a compendium sweep is invalid.
6. **Keep the seed at `1L`.** It matches upstream CoReSh. `bulkirna_stochastic()` lists it.
7. **Read the top 20 before building sets.** Follow `references/interpretation-protocol.md`.

## Task → export

| Task | Export |
|---|---|
| Preflight packages, chunk tree, first chunk | `coresh_validate(chunk_dir, species)` |
| Symbols → integer Entrez, alias fallback | `gene_to_entrez(symbols, species)` |
| Strip ribosomal, mito, haemoglobin, cell-cycle, sex genes | `filter_confounder_genes(symbols, drop)` |
| Score every dataset for named queries | `coresh_search(queries, chunk_dir, species, n_cores, pvalues, sample_size, seed, eps)` |
| Score one dataset object | `coresh_match(obj, query, pvalues, sample_size, seed, eps)` |
| Datasets in the top hits of several queries | `coresh_convergence(ranking, top_n, min_queries)` |
| GSE → chunk file index | `coresh_chunks(chunk_dir, species, cache)` |
| Gene loadings on the query direction, one hit | `coresh_loadings(chunk_path, gse_id, query, top_n, gpl)` |
| Gene sets from a filtered hit table | `coresh_sets(top_hits, queries, chunk_dir, species, top_n, min_size, max_size, jaccard_threshold, verbose)` |
| Search and build sets in one call | `gsdb_coresh(queries, chunk_dir, species, top_hits, top_n, min_size, max_size, jaccard_threshold, n_cores, seed)` |
| Axis labels from accession, platform, size, pct_var | `coresh_labels(x, titles, style, title_width)` |
| Coregulation of sets in your own expression matrix | `gs_coregulation()`, `bulkirna` skill |

## Chunk tree

| Item | Value |
|---|---|
| Host path | `/data2/users/shared/refcache/coresh/current/preprocessed_chunks/{hsa,mmu}` |
| Snapshot | `current` → `syn66227307_20260721`; 89 `hsa` + 85 `mmu` chunk files, ~21 GB |
| Resolution | `chunk_dir = NULL` reads `$REFCACHE_ROOT/coresh/current/...`; pass `chunk_dir` for a local copy |
| Container | mount the refcache at `/refcache` and set `REFCACHE_ROOT=/refcache` |
| Check | `coresh_validate()` prints every check and the resolved path |
| Record | `attr(hits, "provenance")$snapshot` |

`coresh_validate()` also reports `qs2`, `BiocParallel` and `org.*.eg.db`. Install any it marks
missing. The upstream `coresh` package carries no R functions and is not required. To fetch a new
snapshot, the user runs the Synapse download in `references/synapse-data-setup.md`.

## Recipe: query to ranked datasets

```r
h <- gsdb_msigdb(species = "Homo sapiens", collection = "H")
syms <- filter_confounder_genes(de_top_symbols)       # e.g. top 50 by moderated t
queries <- list(
  hypoxia_ctrl = gene_to_entrez(h[["HALLMARK_HYPOXIA"]], species = "human"),
  my_signature = gene_to_entrez(syms, species = "human")
)

hits <- coresh_search(queries, species = "human", n_cores = 4L)          # pct_var screen
hits_p <- coresh_search(queries, species = "human", n_cores = 4L,
                        pvalues = TRUE)                                  # p_value ranking
nrow(attr(hits, "skipped"))                                              # report it
conv <- coresh_convergence(hits_p, top_n = 10L, min_queries = 2L)
```

Screen with `pct_var` (seconds). Rank with `p_value` for anything reported: upstream calls it
the more specific ranking. Columns: `query_name`, `gse`, `gpl`, `pct_var`, `p_value`, `log2err`,
`size`, `rank`. Report `log2err`; `Inf` means past the estimator's resolution.

## Recipe: hits to a gene-set database

```r
top <- hits_p[hits_p$rank <= 5L, ]
db  <- coresh_sets(top, queries, species = "human")                 # from p-value hits
# or: db <- gsdb_coresh(queries, species = "human", top_hits = 5L)  # pct_var hits, one call

gsdb_info(db)$provenance
attr(db, "set_provenance")      # set_name, query_name, gse, gpl, chunk_path, rank_in_coresh
res <- gs_test(ranks, db, contrast = cfg$contrasts$name, min_size = 15, max_size = 500)
```

`gsdb_coresh()` ranks by `pct_var` only. Use `coresh_search(pvalues = TRUE)` plus
`coresh_sets()` to build sets from p-value hits. Derived sets are unsigned: the sign of the
query direction is arbitrary. The full bridge, with checks, is
`references/coresh-to-gsea-bridge.md`.

## Verification checklist

- [ ] Web UI and local top 20 share accessions for the same query.
- [ ] `HALLMARK_HYPOXIA` ranks hypoxia, HIF and tumour-hypoxia series in its top 20.
- [ ] `size` on top hits is near `length(query)`. Low `size` means wrong species or poor
      platform coverage.
- [ ] A housekeeping control (`ACTB`, `GAPDH`, `B2M`, `HPRT1`, `TBP`, `PPIA`) ranks different
      datasets from the real query.
- [ ] At least 5 of the top 10 hits are expected or adjacent biology.
- [ ] Related queries share at least one top-10 dataset in `coresh_convergence()`.

## Traps

| Symptom | Cause | Action |
|---|---|---|
| `size` near 0 everywhere | Human query on `mmu/`, or the reverse | Map orthologs, query the matching species |
| Top hits all cancer cell lines | Proliferation-adjacent signal | Drop cell-cycle genes; rank by `p_value` |
| One GSE tops every query at very high `pct_var` | Outlier-driven dataset | Inspect it on GEO before use |
| Derived sets look alike across queries | Housekeeping-heavy query | Filter the query and rerun |
| Mapping drops genes | Retired symbols, readthroughs, `LOC` loci | Read the `gene_to_entrez()` warning; readthroughs stay unmapped |
| Labels show set ids | Titles are not in the snapshot | Pass a GEO title lookup to `coresh_labels(titles = )` |

## References (load on demand)

- `references/query-design.md`: size regime, signature sources, confounder filtering
- `references/interpretation-protocol.md`: expected categories, top-20 protocol, controls, red flags, write-up
- `references/coresh-to-gsea-bridge.md`: hits to sets to GSEA, provenance, failure modes
- `references/algorithm.md`: what `pct_var` measures, chunk object fields, p-value cost
- `references/synapse-data-setup.md`: fetching a new snapshot into the refcache

## Resources

- Paper: Sukhov V et al. *Nucleic Acids Res.* 2025;53(W1):W187-W192. doi:10.1093/nar/gkaf372
- Method precedent: Mehrotra P et al. *Nature* 631, 207-215 (2024). doi:10.1038/s41586-024-07585-9
- Web UI: <https://alserglab.wustl.edu/coresh>
- Upstream vignette: <https://rpubs.com/asergushichev/coresh-local>

## See also

- `bulkirna`: counts to DE to ranks, the general recipe
- `bulk-rnaseq-gsea`: canonical-pathway interpretation, and GSEA on CoReSh-derived sets
- `bulk-rnaseq-pathway-explorer`: reading the resulting gene-set result
- `gatom-metabolomic-predictions`: metabolic modules from DE
