---
name: bulkirna
description: "bulkiRNA — the installed R package for bulk and pseudo-bulk RNA-seq. Use for any bulk count matrix, gene annotation, DGEList, filterByExpr, TMM, limma or edgeR DE, PCA, volcano, GSEA, ORA, MSigDB, CoReSh or GATOM step. Load it with library(bulkiRNA) and call its exports. For TE counts use te-geneset-gsea; for single-cell use single-cell-rna-qc."
license: MIT
---

# bulkiRNA

bulkiRNA is the house library for bulk RNA-seq. It ships in every `scdock-r-dev` image from
`v0.5.15` and replaces the retired `RNAseq-toolkit` scripts. Load it and call it:

```r
library(bulkiRNA)
packageVersion("bulkiRNA")   # 1.1.0 in v0.5.19
bulkirna_api()               # every export: layer, lifecycle, stochastic flag
?build_dge                   # each export documents its contract
```

## Rules this skill imposes

1. **Call the export.** Reading counts, annotating genes, building a DGEList, ranking genes,
   loading gene sets, testing them and drawing DE or gene-set figures are package functions.
   Check `bulkirna_api()` and the help page before writing any helper.
2. **Wrap a gap, then name it.** When an export falls short, keep it in the call path, add the
   smallest project helper around it, and state the missing behaviour in your summary.
3. **Treat `RNAseq-toolkit` as retired.** An instruction to `source()` a script from
   `01_modules/RNAseq-toolkit/` is stale; the export of the same name replaces it.
4. **Annotate before filtering.** Ensembl IDs dropped by a filter cannot be recovered.
5. **Fit with limma-trend or edgeR QL. Rank on the moderated t.**
6. **Carry `contrast` as a string.** It is the join key across DE, gene-set and master tables.
7. **Compute writes tables; viz writes figures.** `gs_save()` writes `.pdf`, `.png` and the
   same-stem `.tsv` from one plot object.
8. **Pass seeds and size bounds from config.** `bulkirna_stochastic()` lists every stochastic
   export with its seed argument and default. `gs_test()` has no size default: set
   `min_size = 10, max_size = 500` explicitly.

## Task → export

| Task | Export |
|---|---|
| Read featureCounts, Salmon or generic counts | `read_counts_matrix()` |
| Read a sample sheet (`.csv`, `.tsv`, `.xlsx`) | `read_metadata()` |
| Ensembl → symbol, Entrez, biotype | `annotate_genes()` |
| Symbol ↔ Entrez | `gene_to_entrez()`, `entrez_to_gene()` |
| Drop ribosomal, mito, haemoglobin, cell-cycle, sex genes | `filter_confounder_genes()` |
| DGEList with order checks and TMM | `build_dge()` |
| Provenance (genome, resolved Ensembl release, RNG, `sessionInfo()`) | `write_session_provenance()` |
| PCA, 3-D PCA | `de_pca()`, `de_pca_3d()` |
| Volcano, volcano row, MD, B-vs-FC | `de_volcano()`, `de_volcano_grid()`, `de_md_plot()`, `de_bfc_plot()` |
| Rank vector from a DE table | `gs_ranks()` |
| Gene-set databases | `gsdb_msigdb()`, `gsdb_load()`, `gsdb_from_file()`, `gsdb_coresh()`, `gsdb_list()` |
| GSEA, ORA, score-matrix limma | `gs_test()` — method follows the class of `x` |
| Per-sample scores (GSVA, ssGSEA, z-score, PLAGE) | `gs_score()` |
| Coregulation (GESECA) | `gs_coregulation()` |
| Top sets, leading edge, filter, split | `gs_top()`, `gs_leading_edge()`, `gs_filter()`, `gs_split()` |
| Write and read results | `gs_write()`, `gs_read()` |
| Master table | `gs_to_master()`, `gs_validate_master()`, `gs_master_columns()` |
| Gene-set figures | `gs_plot_dot()`, `gs_plot_bar()`, `gs_plot_heatmap()`, `gs_plot_running()`, `gs_plot_size()` |
| Save a figure and its table | `gs_save()` |
| CoReSh signature search | `coresh_search()`, `coresh_sets()`, `coresh_labels()` — skill `coresh-signature-search` |
| GATOM metabolic modules | `gatom_refs()`, `gatom_de()`, `gatom_module()` — skill `gatom-metabolomic-predictions` |

TF activity, PROGENy and WGCNA have no export yet; write those stages by hand and validate their
master rows with `gs_validate_master()`.

## Recipe: counts to a filtered, normalised DGEList

Paths and parameters come from `analysis_config.yaml`.

```r
counts  <- read_counts_matrix(cfg$inputs$counts)          # versioned Ensembl rownames
samples <- as.data.frame(read_metadata(cfg$inputs$samples))
rownames(samples) <- samples$Sample_ID
counts  <- counts[, rownames(samples)]
samples$group <- factor(samples[[cfg$design$group_column]])

genes <- as.data.frame(annotate_genes(rownames(counts), species = "Mus musculus",
                                      input_gene_name = attr(counts, "input_gene_name")))
rownames(genes) <- rownames(counts)
dge <- build_dge(counts, samples, genes)                   # raw counts + TMM

design <- model.matrix(~ 0 + group, data = dge$samples)
colnames(design) <- levels(dge$samples$group)
keep <- edgeR::filterByExpr(dge, design = design)
dge  <- edgeR::calcNormFactors(dge[keep, , keep.lib.sizes = FALSE], method = "TMM")
write_session_provenance(file.path(out_dir, "provenance.txt"),
                         genome_build = cfg$project$genome_build)
```

In 1.1.0 `annotate_genes()` stores the quantifier's name in `input_gene_name` and leaves `Symbol`
equal to the Ensembl ID where org.db has no entry. Fill `Symbol` from `input_gene_name` there
when the project wants GENCODE names.

## Recipe: contrast to gene sets

```r
logcpm <- edgeR::cpm(dge, log = TRUE, prior.count = 2)
cm  <- limma::makeContrasts(contrasts = cfg$contrasts$expr, levels = design)
fit <- limma::eBayes(limma::contrasts.fit(limma::lmFit(logcpm, design), cm), trend = TRUE)
de  <- limma::topTable(fit, coef = 1, n = Inf, sort.by = "none", genelist = dge$genes)

ranks <- gs_ranks(de, metric = "t", genes = "Symbol", collapse = "max_abs")
db    <- gsdb_msigdb(species = "Mus musculus", collection = "H")
res   <- gs_test(ranks, db, contrast = cfg$contrasts$name, min_size = 10, max_size = 500)
gs_write(res, "03_results/<stage>/tables", name = "gsea")
```

```r
p <- gs_plot_dot(res, top_n = 10)          # viz stage reads the tables back with gs_read()
gs_save(p, "03_results/<stage>/figures/_overview/hallmark_dot", width = 8, height = 6)
```

`gs_result` is a tibble: `dplyr` verbs and `rbind()` work on it.

## Traps

- `gsdb_msigdb()` defaults to human sets mapped to mouse; pass `db_species = "MM"` for
  mouse-native collections.
- `gs_to_master(db = )` takes the `gs_db` object.
- A renamed provider keeps its join key: set `attr(db, "database")` or `gsdb_from_file(database = )`.
- `annotate_genes()` takes `"Mus musculus"`; `gene_to_entrez()` takes `"mouse"`. Both accept
  either alias.
- Seed defaults differ by design: fgsea `123L`, CoReSh `1L`, GATOM `42`. Keep them.

## See also

- `annotate-bulk-rnaseq-data` — the TE path and gene + TE matrices
- `bulk-rnaseq-gsea` — database choice, interpretation, figure set
- `bulk-rnaseq-pathway-explorer` — reading a gene-set result
- `coresh-signature-search`, `gatom-metabolomic-predictions` — those two analyses end to end
- `analysis-code-conventions` — stage layout and helpers
