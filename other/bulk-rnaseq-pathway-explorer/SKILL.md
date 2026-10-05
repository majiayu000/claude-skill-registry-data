---
name: bulk-rnaseq-pathway-explorer
description: "pathway-explorer builds standalone interactive HTML dashboards from a master_unified.csv of GSEA, TF and PROGENy results: gene-set UMAP, Jaccard neighbour edges, running sums, database filters. Build the table with bulkiRNA gs_to_master() and gs_validate_master(). For running GSEA use bulk-rnaseq-gsea."
license: MIT
---

# Pathway Explorer: interactive pathway dashboards

`pathway-explorer` (Python module `pathway_explorer`, v2.0.0) turns a master table into a
self-contained HTML dashboard. Pathways sit on a 2-D embedding of their leading-edge genes,
with database and entity filters, FDR/NES sliders, neighbour edges, a gene table and a
per-pathway running sum. bulkiRNA produces the input table; the CSV schema is the only bridge.
Read `skills/bulkirna` for the DE and gene-set recipe.

## Rules this skill imposes

1. **Build master rows with `gs_to_master()`.** It emits the schema the loader reads.
2. **Validate the assembled table with `gs_validate_master()`** before writing it.
3. **Set the provider's database key to the dashboard name** (`Hallmark`, `KEGG`, `Reactome`,
   `GO_BP`, `MitoPathways`, `MitoXplorer`, `CollecTRI`, `PROGENy`, `TE_Class`, `TE_Family`,
   `TransportDB`, `GATOM`). `DB_COLORS` keys on it.
4. **Pass `entity_type`** (`Pathway`, `TF`, `PROGENy`, `TE`) on every row.
5. **Keep `core_enrichment` populated.** It seeds the similarity matrix.

## Build the input in R

At the master-table stage, where `res`, `db` and `ranks` are in scope:

```r
db <- gsdb_msigdb(species = "Mus musculus", collection = "H")
attr(db, "database") <- "Hallmark"                       # before gs_test()
res <- gs_test(ranks, db, contrast = contrast, min_size = 10, max_size = 500)
pw  <- gs_to_master(res, db = db, universe = names(ranks), entity_type = "Pathway")
```

From a viz stage, read the stored result back. `genes_full_set` is `NA` without `db`; the
dashboard does not read it.

```r
res <- gs_read("03_results/<stage>/tables", name = "gsea")
pw  <- gs_to_master(res, entity_type = "Pathway")
```

Assemble, validate and write:

```r
unified <- rbind(pw, tf_rows, progeny_rows)              # TF/PROGENy rows built by hand
gs_validate_master(unified)
utils::write.csv(unified, "03_results/tables/master_unified.csv", row.names = FALSE)
```

bulkiRNA has no TF-activity or PROGENy export. Build those rows in the column order of
`gs_master_columns(optional = TRUE)`; `gs_validate_master()` checks them.

Load MitoCarta and mitoXplorer as separate providers (`gsdb_load("mitopathways")`,
`gsdb_load("mitoxplorer")`) labelled `MitoPathways` and `MitoXplorer`, so each gets its colour.

Pre-filter a large result before `gs_to_master()`:

```r
res <- gs_filter(res, padj = 0.25)
res <- gs_top(res, n = 100, by = "padj", per = c("database", "contrast"))
```

### Running-sum input

The running-sum panel reads `03_results/tables/master_de_table.csv` with columns
`gene_symbol, t, logFC, adj.P.Val`. bulkiRNA has no writer for it. Write it from the limma
table, one file for all contrasts.

## Columns the loader reads

| Column | Source in `gs_to_master()` | Role |
|---|---|---|
| `entity_type` | `entity_type =` | Point shape (circle, diamond, square, triangle) |
| `pathway_id` | `res$pathway_id` | Neighbour key; repeats across contrasts |
| `pathway_name` | `res$pathway_name` | Label, Title Case, truncated to 60 chars |
| `database` | provider key | Colour |
| `contrast` | `res$contrast` | Required for `--contrast` and `--all` |
| `nes`, `pvalue`, `padj` | `stat`, `p_value`, `padj` | Colour scale, tooltip, FDR slider |
| `set_size`, `leading_edge_size` | tested size, leading edge | Size encoding |
| `core_enrichment` | `/`-joined leading edge | Similarity matrix |
| `direction` | `Up`, `Down`, `NS` | Direction filter |

## Run

```bash
pathway-explorer --contrast <contrast>          # one dashboard
pathway-explorer --all                          # one per contrast + index.html
python -m pathway_explorer --data <csv> --output <html> --contrast <contrast>
pathway-explorer --entity-types Pathway TF      # restrict entities
pathway-explorer --te-level class               # or family
```

The CLI walks up from the working directory to the first `03_results/tables/`. Output lands in
`03_results/interactive/pathway_explorer_<contrast>.html`. Install the `[full]` extra for UMAP:
`pip install -e "01_modules/pathway-explorer[full]"`.

## What the tool computes

1. `signed_sig = -log10(padj) * sign(nes)`, capped at ±50.
2. Similarity over leading edges: Jaccard within a type and for PROGENy–Pathway; overlap
   coefficient `|A∩B| / min(|A|,|B|)` for TF–Pathway and TF–PROGENy, because TF regulons are
   much larger than pathway sets.
3. Top-5 neighbours per pathway above `MIN_JACCARD_EDGE = 0.15`.
4. Embedding: UMAP, then PCA, then random projection.

Tunables in `config.py`: `MIN_JACCARD_EDGE`, `NES_MAX = 3.5`, `DEFAULT_FDR_SLIDER = 0.05`,
`MAX_PATHWAYS`, `DB_COLORS`, `ENTITY_SHAPES`. A new entity type goes in `ENTITY_TYPES` and
`ENTITY_SHAPES`; a new cross-type pair gets its own metric in `compute_hybrid_similarity`.

## Planned: one HTML for all contrasts

The next version embeds every contrast in one file with an in-place toggle. Keep the JSON
payload contrast-keyed: `{contrasts: {<name>: {pathways, metadata, neighbors}}, default_contrast}`.
Keep `--contrast` and `--all`; add a third mode such as `--all-in-one`. Make
`master_de_table.csv` contrast-keyed. Use `--all` until then.

## Verify

- [ ] The HTML is hundreds of KB.
- [ ] Sidebar counts show every entity type the table holds.
- [ ] The legend lists every database you labelled.
- [ ] Edges connect related pathways.
- [ ] Clicking a point fills the gene table and, with `master_de_table.csv`, the running sum.

## Pitfalls

| Symptom | Cause and fix |
|---|---|
| `No pathways found after filtering!` | `--contrast` matches no row. Run once unfiltered, read `Found N contrasts`, use the exact string. |
| `NES column not found` | A hand-built block uses a third column name. `gs_validate_master()` names it. |
| One tight blob | Empty `core_enrichment`, or no UMAP/sklearn (random fallback). |
| One colour for all databases | Providers kept bulkiRNA keys (`msigdb_H`). Relabel before `gs_test()`. |
| Empty running-sum panel | `master_de_table.csv` is missing. |
| HTML over 10 MB | Pre-filter with `gs_filter()` / `gs_top()`, or set `MAX_PATHWAYS`. |

## Static figures

For PDF/PNG use bulkiRNA: `gs_plot_running()`, `gs_plot_dot()`, then `gs_save()`. See
`bulk-rnaseq-gsea`.

## See also

- `bulkirna` — DE, gene-set testing and master-table exports
- `bulk-rnaseq-gsea` — running GSEA, database choice, static figures
- `gatom-metabolomic-predictions` — metabolic network modules
- Upstream: https://github.com/tony-zhelonkin/pathway-explorer
