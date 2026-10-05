---
name: bulk-rnaseq-gsea
description: "GSEA for bulk RNA-seq with bulkiRNA: which MSigDB and custom databases to run, rank metric, size bounds 10/500, per-database figures and the master table. Use for preranked GSEA, fgsea, Hallmark, KEGG, Reactome, GO, MitoPathways, TransportDB, GMT or GMX sets, dotplots, running-sum plots. For the HTML explorer use bulk-rnaseq-pathway-explorer."
license: MIT
---

# Bulk RNA-seq GSEA

This skill sets the house GSEA stage: databases, parameters, figures and the master table. The
package does the mechanics. Read `bulkirna` first for the DE recipe that produces the input, then
`?gs_test`, `?gsdb_msigdb`, `?gs_plot_dot` and `?gs_to_master` for each contract.

## Rules this skill imposes

1. **Rank on the moderated t.** `gs_ranks(de, metric = "t", genes = "Symbol", collapse = "max_abs")`.
2. **Bound set size at 10 and 500 on `gs_test()`.** Pass both explicitly. Leave the provider
   bounds at `NULL`: `gsdb_*(min_size = )` filters raw sets, before intersection with the ranked
   genes, and changes which pathways are tested.
3. **Keep every tested set.** `gs_test()` returns all of them. Select for display with `gs_top()`
   and the renderers' `top_n`; mark significance with `highlight`.
4. **Name each provider with the project's database key.** The names of the list passed as `db`
   become the `database` column. Figures, tables and master rows join on it.
5. **Seed from config.** fgsea's default is `123L`; `bulkirna_stochastic()` lists it.
6. **One stage computes, one renders.** The compute stage ends at `gs_write()`. The viz stage
   starts at `gs_read()`.

## Databases

House set for a mouse project. Human MSigDB is mapped to mouse orthologs (`db_species = "HS"`,
the default).

| Key | Call | Why |
|---|---|---|
| `Hallmark` | `gsdb_msigdb(sp, collection = "H")` | 50 curated programs; first read of any contrast |
| `KEGG` | `gsdb_msigdb(sp, "C2", "CP:KEGG_LEGACY")` | metabolic and signalling maps |
| `Reactome` | `gsdb_msigdb(sp, "C2", "CP:REACTOME")` | fine-grained mechanism |
| `WikiPathways` | `gsdb_msigdb(sp, "C2", "CP:WIKIPATHWAYS")` | community pathways |
| `TF_Targets` | `gsdb_msigdb(sp, "C3", "TFT:GTRD")` | TF target sets |
| `GO_BP`, `GO_MF`, `GO_CC` | `gsdb_msigdb(sp, "C5", "GO:BP")` and so on | broad coverage; slowest |
| `MitoPathways` | `gsdb_load("mitopathways", species = sp)` | mitochondrial hierarchy (MitoCarta 3.0) |
| `MitoXplorer` | `gsdb_load("mitoxplorer", species = sp)` | mitochondrial processes |
| `TransportDB` | `gsdb_load("transportdb", species = sp)` | transporter families |

Pass a subcollection for C2, C3 and C5; `NULL` loads the whole collection. Subcollection names
follow the installed msigdbr: list them with `msigdbr::msigdbr_collections()`. `gsdb_list()` lists
the bundled databases; `mito_unified` merges the two mito sources. Project GMT, GMX, TSV and
GATOM-module sets: [references/custom-databases.md](references/custom-databases.md).

## Parameters

| Setting | House value | Where |
|---|---|---|
| Rank metric | moderated t from limma-trend | `gs_ranks(metric = "t")` |
| Set size | 10 to 500 genes tested | `gs_test(min_size = 10, max_size = 500)` |
| p-value floor | none, `eps = 0` (the default) | `gs_test(eps = )` |
| Permutations | `n_perm_simple = 100000` (the default) | `gs_test(n_perm_simple = )` |
| Seed | `123L` from config | `gs_test(seed = )` |
| Significance | FDR < 0.05 | renderer `highlight = 0.05` |
| Display | top 20 per database; top 10 per database pooled | renderer `top_n` |

## Compute

```r
library(bulkiRNA)
sp  <- cfg$project$species                          # "Mus musculus"
dbs <- list(
  Hallmark     = gsdb_msigdb(sp, collection = "H"),
  Reactome     = gsdb_msigdb(sp, "C2", "CP:REACTOME"),
  GO_BP        = gsdb_msigdb(sp, "C5", "GO:BP"),
  MitoPathways = gsdb_load("mitopathways", species = sp)
)
ranks <- lapply(de_tables, gs_ranks, metric = "t", genes = "Symbol", collapse = "max_abs")
res <- do.call(rbind, lapply(names(ranks), function(ct)
  gs_test(ranks[[ct]], dbs, contrast = ct, min_size = 10, max_size = 500,
          seed = cfg$gsea$seed)))

gs_write(res, file.path(stage_dir, "tables"), name = "gsea", prune = TRUE)
saveRDS(list(dbs = dbs, ranks = ranks), file.path(stage_dir, "gsea_inputs.rds"))
```

`de_tables` is a named list of full `limma::topTable(n = Inf, sort.by = "none")` tables keyed by
the contrast string. `prune = TRUE` makes a re-run replace the stage's tables. The viz and master
stages read set membership and ranks from `gsea_inputs.rds`.

## Figure set

Per contrast and database, from `x <- gs_filter(res, contrast = ct, database = key)`. Size each
canvas with `gs_plot_size(type, key)` and write with `gs_save()`, which emits `.pdf`, `.png` and
the same-stem `.tsv`.

| Stem | Call |
|---|---|
| `<key>_dot` | `gs_plot_dot(x, top_n = 20, highlight = 0.05)` |
| `<key>_up_dot`, `<key>_down_dot` | `gs_plot_dot(x, top_n = 20, direction = "up")`, `"down"` |
| `<key>_nes_bar` | `gs_plot_bar(x, top_n = 20, highlight = 0.05)` |
| `<key>_running` | `gs_plot_running(x, ranks = ranks[[ct]], db = dbs[[key]], top_n = 5, metric_label = "t statistic")` |
| `running/<pathway_id>` | `gs_plot_running(x, ranks = ranks[[ct]], db = dbs[[key]], pathways = id)` for each id in `gs_top(x, n = 10)$pathway_id` |

Across databases, per contrast, under `_overview/`:

| Stem | Call |
|---|---|
| `pooled_<contrast>` | `gs_plot_dot(gs_filter(res, contrast = ct), top_n = 10, facet = "database")` |
| `focused_top5_<contrast>` | the same over the key databases, `top_n = 5` |
| `<key>_contrasts_heatmap` | `gs_plot_heatmap(gs_filter(res, database = key), top_n = 20, by = "contrast")` |

Pass one shared `limits` to every figure meant for side-by-side comparison; the default derives
limits from each figure's own data.

## Master table

`gs_to_master()` serialises a result to the versioned master schema; `gs_validate_master()` checks
it. Assembly across stages and non-GSEA rows: [references/master-table.md](references/master-table.md).

## Reading the result

- `stat` is NES. Its sign follows the contrast string: positive means enriched in the first term.
- `padj` is adjusted within one database and one contrast.
- `log2err = Inf` marks a p-value past the estimator's resolution. Report it as below that floor.
- `gs_leading_edge()` shows which sets share driving genes and which are independent.

## Checks before reporting

```r
setequal(unique(res$database), names(dbs))         # every database returned tested sets
table(res$database, res$contrast)                  # every cell non-empty
summary(res)                                       # tested sets and hits per database
sum(names(ranks[[1]]) %in% unlist(dbs$Hallmark))   # thousands of shared symbols
```

A database with no tested sets means Ensembl IDs or human symbols in the ranks. Fix the ranks.

## Traps

- `gsdb_msigdb()` keys itself `msigdb_C2_CP_REACTOME`; the list name overrides it, and
  `gs_plot_size()` recognises project keys such as `Hallmark`, `KEGG`, `GO_BP`.
- `db_species = "MM"` selects mouse-native sets: a different collection with different set ids.
- `gs_plot_running()` needs `db`: a `gs_result` carries no set membership.
- Shape-21 points in a hand-built figure use `color = "transparent"` under ggplot2 4.0+.

## See also

- `bulkirna`: DE recipe, task-to-export table, general traps
- `bulk-rnaseq-pathway-explorer`: interactive HTML from the master table
- `bulk-rnaseq-activity-inference`: TF and PROGENy activities
- `gatom-metabolomic-predictions`: metabolic modules; their genes enter as a custom database
- `coresh-signature-search`: signature search across GEO datasets
- `te-geneset-gsea`: TE family and class sets
