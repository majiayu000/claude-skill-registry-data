---
name: genenmf-metaprogram-discovery
description: "Runs PER-SAMPLE NMF then consensus-clusters the programs into recurrent meta-programs across donors or tumors, via R GeneNMF plus UCell scoring. Use to find transcriptional states shared across MULTIPLE samples without batch correction (Gavish-style meta-programs). For one joint model on one dataset use scvi-lda."
license: MIT
---

# GeneNMF Skill

## Purpose

Discover recurrent gene programs (meta-programs) across multiple single-cell samples using non-negative matrix factorization (NMF). Bypasses batch correction by learning programs per-sample then finding consensus signatures.

## Biology Problem

```
PCA/SVD:        [sequential transforms that can cancel out]  → Hard to interpret individual factors
NMF:            [additive decomposition into parts]          → Each factor = interpretable gene program

Cancer cells:   Patient A [programs 1,3,5]  →  Meta-programs across patients
                Patient B [programs 2,3,4]  →  MP3 = consensus of program 3 variants
                Patient C [programs 1,3,6]
```

**Key advantage:** Per-sample NMF + meta-program consensus bypasses need for batch effect correction.

## Installation

```r
# From CRAN
install.packages("GeneNMF")

# Or from GitHub (latest)
library(remotes)
remotes::install_github("carmonalab/GeneNMF")

# Dependencies
library(GeneNMF)
library(Seurat)
library(UCell)        # For signature scoring
library(fgsea)        # For GSEA interpretation (optional)
library(msigdbr)      # For MSigDB signatures (optional)
```

## Quick Start

```r
library(GeneNMF)
library(Seurat)

# 1. Split by sample
seu.list <- SplitObject(seu, split.by = "sample_id")

# 2. Multi-sample NMF (tests k=4 to 9 components)
geneNMF.programs <- multiNMF(seu.list, k=4:9, assay="RNA", nfeatures=2000)

# 3. Cluster into meta-programs
geneNMF.metaprograms <- getMetaPrograms(geneNMF.programs, nMP=10)

# 4. Get gene sets
geneNMF.metaprograms$metaprograms.genes     # Gene lists per MP
geneNMF.metaprograms$metaprograms.metrics   # Quality metrics
```

---

## Core Workflow

### Step 1: NMF for Dimensionality Reduction (Single Dataset)

```r
# Find variable features first
seu <- FindVariableFeatures(seu, nfeatures=1000)

# Run NMF (similar to RunPCA)
ndim <- 15
seu <- runNMF(seu, k=ndim, assay="SCT")  # or "RNA"

# UMAP on NMF embedding
seu <- RunUMAP(seu, reduction="NMF", dims=1:ndim,
               reduction.name="NMF_UMAP", reduction.key="nmfUMAP_")

DimPlot(seu, reduction="NMF_UMAP", group.by="celltype")
```

### Step 2: Multi-Sample Meta-Program Discovery

```r
# Split Seurat object by sample/patient
seu.list <- SplitObject(seu, split.by="donor")

# Run NMF across samples and k values
geneNMF.programs <- multiNMF(
  seu.list,
  assay = "RNA",       # or "SCT"
  slot = "data",       # normalized data
  k = 4:9,             # range of components to test
  nfeatures = 2000,    # top variable genes
  min.exp = 0.05       # min expression filter (for noisy data)
)
```

### Step 3: Extract Meta-Programs

```r
geneNMF.metaprograms <- getMetaPrograms(
  geneNMF.programs,
  nMP = 10,                    # target number of meta-programs
  weight.explained = 0.7,      # cumulative weight threshold for gene inclusion
  min.confidence = 0.5,        # fraction of programs where gene appears
  specificity.weight = 5,      # sparsity enforcement (lower = more overlap allowed)
  metric = "cosine",           # similarity metric
  max.genes = 100              # cap genes per MP
)

# Visualize program clustering
plotMetaPrograms(geneNMF.metaprograms, similarity.cutoff=c(0.1, 1))
```

### Step 4: Evaluate Meta-Program Quality

```r
# Quality metrics
geneNMF.metaprograms$metaprograms.metrics
```

| Metric | Interpretation |
|--------|----------------|
| `sampleCoverage` | Fraction of samples where MP detected (>0.5 good) |
| `silhouette` | Internal consistency vs other MPs (>0.3 good, <0 drop) |
| `meanSimilarity` | Average similarity within MP cluster |
| `numberGenes` | Genes in MP signature |
| `numberPrograms` | Individual programs contributing to MP |

```r
# Drop low-quality meta-programs
geneNMF.metaprograms <- dropMetaPrograms(
  geneNMF.metaprograms,
  dropMP = c("MP4", "MP8")  # e.g., negative silhouette
)
```

### Step 5: Interpret Gene Programs via GSEA

```r
library(msigdbr)
library(fgsea)

top_pathways <- lapply(geneNMF.metaprograms$metaprograms.genes, function(program) {
  runGSEA(program, universe=rownames(seu), category="C8")  # Cell type signatures
  # Or: category="H" for Hallmarks, "C5" subcategory="GO:BP" for biological process
})

# Inspect top enrichments for each MP
head(top_pathways$MP1)
```

### Step 6: Score Cells by Meta-Programs

```r
library(UCell)

# Get MP signature scores (0-1 per cell)
mp.genes <- geneNMF.metaprograms$metaprograms.genes
seu <- AddModuleScore_UCell(seu, features=mp.genes, assay="SCT", ncores=4, name="")

# Visualize by cell type
VlnPlot(seu, features=names(mp.genes), group.by="celltype.l1", pt.size=0, ncol=5)
```

### Step 7: Integrated Space from MP Scores

```r
# Create new dimensionality reduction from MP scores
matrix <- seu@meta.data[, names(mp.genes)]
dimred <- as.matrix(matrix)
colnames(dimred) <- paste0("MP_", seq_len(ncol(dimred)))

seu@reductions[["MPsignatures"]] <- new("DimReduc",
  cell.embeddings = dimred,
  assay.used = "RNA",
  key = "MP_",
  global = FALSE
)

# UMAP on MP signature space
seu <- RunUMAP(seu, reduction="MPsignatures",
               dims=1:length(seu@reductions[["MPsignatures"]]),
               metric="euclidean", reduction.name="umap_MP")

DimPlot(seu, reduction="umap_MP", group.by="patient")  # Samples should mix!
```

---

## Key Parameters

### multiNMF()

| Parameter | Default | Description |
|-----------|---------|-------------|
| `k` | 4:9 | Range of NMF components to test |
| `nfeatures` | 2000 | Top variable genes |
| `assay` | "RNA" | Seurat assay slot |
| `slot` | "data" | Layer (counts/data/scale.data) |
| `min.exp` | 0.05 | Minimum expression filter |
| `center` | FALSE | Center data (v0.6+ default FALSE) |
| `scale` | FALSE | Scale data (v0.6+ default FALSE) |

### getMetaPrograms()

| Parameter | Default | Description |
|-----------|---------|-------------|
| `nMP` | 10 | Target number of meta-programs |
| `weight.explained` | 0.5 | Cumulative weight threshold for genes |
| `min.confidence` | 0.5 | Min fraction of programs with gene |
| `specificity.weight` | 5 | Sparsity (lower=more overlap) |
| `max.genes` | 200 | Cap genes per MP |
| `metric` | "cosine" | Similarity metric (cosine/jaccard) |

---

## Cancer Cell Heterogeneity Workflow

For tumor samples where batch correction fails:

```r
# 1. Extract cancer cells only
cancer_seu <- subset(seu, subset = cell_type == "Cancer")
cancer.list <- SplitObject(cancer_seu, split.by = "patient")

# 2. Multi-sample NMF
programs <- multiNMF(cancer.list, assay="RNA", k=4:9, nfeatures=2000)

# 3. Strict meta-program extraction
mps <- getMetaPrograms(
  programs,
  nMP = 10,
  min.confidence = 0.7,      # High consistency required
  weight.explained = 0.5,    # Focused gene sets
  specificity.weight = 8     # Enforce sparse, distinct programs
)

# 4. Filter by quality
mps$metaprograms.metrics
mps <- dropMetaPrograms(mps, dropMP = c("MP4"))  # Drop poor quality

# 5. Score all cells (including non-cancer) by cancer programs
seu <- AddModuleScore_UCell(seu, features=mps$metaprograms.genes, ncores=4)
```

---

## Gene Weight Inspection

```r
# View gene contributions to a meta-program
geneNMF.metaprograms$metaprograms.genes.weights$MP1

# Example output:
#   TOP2A    CENPF   NUSAP1   PCLAF   MAD2L1
#   0.195    0.149    0.093    0.081    0.063
```

Higher weights = stronger contribution to the meta-program.

---

## Visualization

### Meta-Program Heatmap

```r
library(RColorBrewer)

anno_colors <- brewer.pal(n=10, name="Paired")
names(anno_colors) <- names(geneNMF.metaprograms$metaprograms.genes)

plotMetaPrograms(geneNMF.metaprograms,
                 annotation_colors = anno_colors,
                 similarity.cutoff = c(0.1, 1))
```

### MP Scores on UMAP

```r
library(viridis)

FeaturePlot(seu, features=names(mp.genes), reduction="umap_MP", ncol=4) &
  scale_color_viridis(option="B") &
  theme(aspect.ratio=1, axis.text=element_blank(), axis.ticks=element_blank())
```

### Compare MPs Across Conditions

```r
VlnPlot(seu, features=names(mp.genes), group.by="patient", pt.size=0, ncol=5)
```

---

## Version 0.6+ Changes

| Change | Old Behavior | New Behavior (v0.6+) |
|--------|--------------|----------------------|
| MP calculation | Jaccard on gene sets | Cosine on weight vectors |
| Consensus weights | Majority voting | Average of program weights |
| `specificity.weight` | New | Enforces sparse decomposition |
| `weight.explained` | N/A | Cumulative threshold for gene inclusion |
| `min.confidence` | Different | Fraction of programs containing gene |
| `scale`/`center` | TRUE | FALSE (default) |

---

## Troubleshooting

| Issue | Solution |
|-------|----------|
| No meta-programs found | Increase `nMP`, lower `min.confidence` |
| MPs too similar | Increase `specificity.weight` (e.g., 8) |
| Poor silhouette scores | Drop MPs with negative silhouette |
| Low sample coverage | Check sample sizes; need ≥50-100 cells/sample |
| Too few genes per MP | Increase `weight.explained` (e.g., 0.8) |
| Too many genes per MP | Decrease `weight.explained`, increase `min.confidence` |
| Memory issues | Reduce `nfeatures`, process in batches |
| Different k values give different MPs | This is expected; consensus resolves it |

---

## Comparison with Other Methods

| Method | Approach | Batch Handling | Interpretability |
|--------|----------|----------------|------------------|
| **GeneNMF** | Per-sample NMF → consensus | Bypasses correction | High (additive parts) |
| PCA | Variance axes | Requires correction | Low (cancellation) |
| scVI | VAE latent | Learns batch | Medium |
| Harmony | Integration | Explicit correction | Low |
| NMF (single run) | All samples together | None | High but batch-confounded |

---

## Quick Reference

```r
# Minimal workflow
library(GeneNMF)
library(Seurat)
library(UCell)

seu.list <- SplitObject(seu, split.by = "sample")
programs <- multiNMF(seu.list, k=4:9, nfeatures=2000)
mps <- getMetaPrograms(programs, nMP=10)
seu <- AddModuleScore_UCell(seu, features=mps$metaprograms.genes)
```

---

## API Reference

- GitHub: https://github.com/carmonalab/GeneNMF
- CRAN: https://cran.r-project.org/package=GeneNMF
- Demo (PBMC): https://carmonalab.github.io/GeneNMF.demo/PBMC_demo.html
- Demo (Cancer): https://carmonalab.github.io/GeneNMF.demo/BCC_demo.html
- RcppML (fast NMF): https://github.com/zdebruine/RcppML

## Citation

```
Wounding triggers invasive progression in human basal cell carcinoma.
Yerly, Andreatta et al. bioRxiv 2024. doi:10.1101/2024.05.31.596823
```

---

## When not to use

- Do not use for batch correction of integrated embeddings. Use scvi-framework or scvi-scanvi for that.
- Do not use on single samples — the method needs multiple donors/samples for meta-program consensus.

---

## See also

- `scvi-framework`
- `anndatar-seurat-scanpy-conversion`
