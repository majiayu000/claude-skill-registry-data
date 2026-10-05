---
name: seurat
description: Single-cell RNA-seq analysis in R with Seurat v5 — QC, normalization (LogNormalize or SCTransform), dimensionality reduction, clustering, marker detection, integration of multiple samples, and interconversion with AnnData/scanpy. Use when single-cell work must stay in R/Bioconductor, when collaborators expect a Seurat object, or when following an R-based tutorial. For Python single-cell workflows use scanpy/anndata instead.
---

# Seurat (R) — single-cell RNA-seq

## Overview

Seurat (Satija lab) is the dominant **R** toolkit for single-cell/spatial analysis. Use it
when the analysis must live in R (Bioconductor downstream, R-based collaborators, lab
convention) — otherwise [[scanpy]]/[[anndata]] in Python is the equivalent and is already
well covered in this vault. Seurat v5 introduced the layered `Assay5` object and a
`BPCells`-backed on-disk path for very large datasets.

## When to use vs scanpy

- **Seurat** — R/tidyverse/Bioconductor downstream, integration with `DESeq2`/`edgeR`
  pseudobulk, `SingleR` annotation, established lab pipelines.
- **scanpy** — Python ecosystem, scVI/deep models ([[scvi-tools]]), very large atlases,
  AnnData-native tooling.

Convert between them rather than re-running: use `sceasy`, `zellkonverter`
(`SingleCellExperiment` ↔ AnnData), or `SeuratDisk` (`.h5Seurat` ↔ `.h5ad`).

## Standard workflow

```r
library(Seurat)

# 1. Load (10x output) and create object with basic gene/cell filters
counts <- Read10X(data.dir = "filtered_feature_bc_matrix/")
obj <- CreateSeuratObject(counts, min.cells = 3, min.features = 200)

# 2. QC: mitochondrial fraction, then filter
obj[["percent.mt"]] <- PercentageFeatureSet(obj, pattern = "^MT-")  # "^mt-" for mouse
VlnPlot(obj, c("nFeature_RNA", "nCount_RNA", "percent.mt"), ncol = 3)
obj <- subset(obj, nFeature_RNA > 200 & nFeature_RNA < 6000 & percent.mt < 15)

# 3a. Standard normalization path
obj <- NormalizeData(obj)
obj <- FindVariableFeatures(obj, nfeatures = 2000)
obj <- ScaleData(obj)

# 3b. OR SCTransform (preferred; replaces NormalizeData+FindVariableFeatures+ScaleData)
# obj <- SCTransform(obj, vars.to.regress = "percent.mt")

# 4. Linear + non-linear dim reduction, graph clustering
obj <- RunPCA(obj)
ElbowPlot(obj)                       # choose #PCs
obj <- FindNeighbors(obj, dims = 1:30)
obj <- FindClusters(obj, resolution = 0.5)   # higher res -> more clusters
obj <- RunUMAP(obj, dims = 1:30)
DimPlot(obj, reduction = "umap", label = TRUE)

# 5. Marker genes
markers <- FindAllMarkers(obj, only.pos = TRUE, min.pct = 0.25, logfc.threshold = 0.25)
FeaturePlot(obj, c("CD3D", "MS4A1", "LYZ"))

saveRDS(obj, "obj.rds")
```

## Integration (multiple samples / batch correction)

Seurat v5 unifies integration under `IntegrateLayers`. Split layers by batch first:

```r
obj[["RNA"]] <- split(obj[["RNA"]], f = obj$sample)
obj <- NormalizeData(obj) |> FindVariableFeatures() |> ScaleData() |> RunPCA()
obj <- IntegrateLayers(obj, method = CCAIntegration,        # or HarmonyIntegration,
                       orig.reduction = "pca",              #    RPCAIntegration,
                       new.reduction = "integrated.cca")    #    scVIIntegration
obj <- FindNeighbors(obj, reduction = "integrated.cca", dims = 1:30)
obj <- FindClusters(obj); obj <- RunUMAP(obj, reduction = "integrated.cca", dims = 1:30)
obj <- JoinLayers(obj)   # re-join before DE / pseudobulk
```

`HarmonyIntegration` mirrors [[harmonypy]]; `RPCA` is faster/more conservative than `CCA`
for large or weakly-overlapping datasets.

## Gotchas

- **v5 layers:** counts/data/scale.data are now *layers*. After integration, call
  `JoinLayers()` before differential expression or pseudobulk, or you'll operate per-batch.
- **SCTransform + markers:** run `PrepSCTFindMarkers()` before `FindMarkers` on SCT data.
- **Species mito pattern:** `^MT-` (human) vs `^mt-` (mouse); a wrong pattern silently
  yields `percent.mt == 0` and bad QC.
- **Pseudobulk DE** beats single-cell Wilcoxon for condition contrasts: aggregate with
  `AggregateExpression()`/`Seurat::PseudobulkExpression()` then hand off to [[pydeseq2]] or
  edgeR. See [[de-summary]] for interpreting results.
- **Memory:** for >500k cells use the `BPCells` on-disk backend or switch to [[scanpy]].

## Related

R counterpart to [[scanpy]]/[[anndata]]; integrate with [[harmonypy]], [[scvi-tools]]
(via `scVIIntegration`), [[bioconductor-bridge]], and pseudobulk DE via [[pydeseq2]].
