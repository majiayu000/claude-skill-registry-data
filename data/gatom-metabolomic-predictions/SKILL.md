---
name: gatom-metabolomic-predictions
description: "GATOM metabolic modules via bulkiRNA: finds the maximally regulated metabolic subnetwork from DE results using atom-transition graphs and BUM-scored SGMWCS. Use to read transcriptomic or metabolomic DE through KEGG or Rhea reaction structure. Needs raw p-values. Load library(bulkiRNA). For pathway enrichment use bulk-rnaseq-gsea."
license: MIT
---

# GATOM: active metabolic modules

GATOM scores a metabolic graph with a BUM model and solves for the maximum-weight connected
subgraph. The module is a scored optimum; it carries no permutation p-value. bulkiRNA wraps the
pipeline in six exports. Read `skills/bulkirna` for the general recipe and the DE fit.

```r
library(bulkiRNA)
?gatom_module
```

## Rules this skill imposes

1. **Feed raw p-values.** BUM is fitted to the raw p-value distribution. `gatom_de()` rejects an
   adjusted-looking column name and values outside `[0, 1]`.
2. **Give `baseMean` on the linear scale.** For limma output use `2^AveExpr`. `gatom_de()` warns
   on a log-scale column.
3. **Start from the unfiltered DE table.** The BUM fit needs the whole p-value distribution.
4. **Read genes from edges.** In atom topology, vertices are metabolite atoms and edges are
   enzyme reactions. `gatom_genes()` reads the edges.
5. **Run the k sensitivity branches.** `k_gene` sets the gene threshold at the k-th smallest
   p-value, capped at FDR 0.1: a larger k grows the module. Run 25, 50 and 75, and report the
   module size per k and the shared core.
6. **Keep `seed = 42`.** It reproduces the historical GATOM results. `bulkirna_stochastic()` records it.
7. **Record the inputs beside the module.** Save the DE table and `refs$files` with the output.

## Task → export

| Task | Export |
|---|---|
| Fetch network, `met.db`, annotation, gene2reaction TSVs | `gatom_download_refs(dir, species, networks, overwrite)` |
| Load the three reference objects | `gatom_refs(species, dir, download, network)` |
| Build and validate the gene DE input | `gatom_de(x, id, pval, log2FC, baseMean)` |
| Build, score and solve the module | `gatom_module(de, refs, k_gene, k_met, met_de, seed, solver, verbose, gene2reaction_extra)` |
| Module genes | `gatom_genes(m)` |
| Interactive HTML | `gatom_save_html(m, path, name)` |

## Recipe

```r
refs_dir <- "00_data/references/gatom"
gatom_download_refs(dir = refs_dir, species = "Mus musculus",
                    networks = c("kegg", "combined"))         # one-time, networked
refs <- gatom_refs(species = "Mus musculus", dir = refs_dir, network = "kegg")

de <- gatom_de(tt, id = Symbol, pval = P.Value, log2FC = logFC,
               baseMean = 2^AveExpr)                           # dedups on ID, lowest p wins
m  <- gatom_module(de, refs, k_gene = 50, seed = 42, verbose = TRUE)
gatom_genes(m)

gatom_save_html(m, "03_results/<stage>/plots/GATOM/kegg_module.html",
                name = "<contrast>: KEGG module")
igraph::write_graph(m, "03_results/<stage>/tables/kegg_module.graphml",
                    format = "graphml")                        # Cytoscape
```

`gatom_refs()` searches `dir`, then `/opt/gatom-refs`, then `00_data/references/gatom`. Pass
`dir` explicitly. `print(refs)` shows which files were loaded.

## k sensitivity

```r
mods <- lapply(c(25, 50, 75), function(k) gatom_module(de, refs, k_gene = k, seed = 42))
sapply(mods, attr, "n_edges")                  # module size per k
core <- Reduce(intersect, lapply(mods, gatom_genes))
```

Interpret the `core` genes first. Treat a gene present at only one k as a size effect until
shown otherwise.

## Networks

| `network` | Files `gatom_refs()` loads | Extra input |
|---|---|---|
| `"kegg"` | `network.kegg.rds`, `met.kegg.db.rds`, `org.<sp>.eg.gatom.anno.rds` | none |
| `"combined"` | `network.combined.rds`, `met.combined.db.rds`, annotation | `gene2reaction_extra` |

For `"combined"`, read the downloaded `gene2reaction.combined.<sp>.eg.tsv` with
`data.table::fread()` and pass it as `gene2reaction_extra`. The table needs `gene` and
`reaction` columns. Without it, Rhea reactions carry no genes.

## Metabolite DE (`met_de`)

Pass a metabolite table as `met_de` with columns `ID`, `pval` (raw) and `log2FC`. It needs no
`baseMean`. Set `k_met` only when `met_de` is supplied.

`met_de$ID` is matched against the `met.db` base ID or any `met.db$mapFrom` ID type:

| Network | Base ID | Accepted `met_de$ID` |
|---|---|---|
| KEGG | KEGG compound | KEGG, HMDB, ChEBI |
| Combined | KEGG + ChEBI | KEGG or ChEBI |

ID formats drift between `met.db` builds. HMDB exists as 5-digit (`HMDB00634`) and 7-digit
(`HMDB0000008`) accessions. Before solving, compare a handful of `refs$met_db$mapFrom[[<type>]]`
IDs against your own `met_de$ID` by eye. A mismatch yields a sparse graph and no error.

## Reading a module

- Colour and read **edges** by `log2FC`. Vertices carry metabolite scores and no fold change.
- State network, species, `k_gene` and `seed` with every module figure and table.

## Pitfalls

| Symptom | Cause and fix |
|---|---|
| Graph has no scored edges | Gene IDs do not match `refs$org_anno`. Read GATOM's `Found DE table for genes with <type> IDs` message and use symbols or Entrez for the species. |
| `met_de` matches few metabolites | ID-format mismatch. Inspect `refs$met_db` IDs. |
| Combined module has only KEGG reactions | `gene2reaction_extra` is missing. |
| `gatom_save_html()` fails on pandoc | Install pandoc or set `RSTUDIO_PANDOC`; the error names the fix. |

## Stage layout

Compute in `2.x_gatom.R`; render in `3.x_gatom_viz.R`. Rendering reads the saved module and
never recomputes it.

## See also

- `bulkirna` — DE fit and the general recipe
- `bulk-rnaseq-gsea` — pathway enrichment statistics
- `genenmf-metaprogram-discovery`

Upstream data: http://artyomovlab.wustl.edu/publications/supp_materials/GATOM/
