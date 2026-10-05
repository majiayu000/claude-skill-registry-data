---
name: seurat-citeseq-wnn
description: "Seurat CITE-seq workflow — multi-assay RNA + ADT object creation, per-modality normalisation (SCTransform for RNA, CLR for ADT), and Weighted Nearest Neighbors joint embedding. Use when analysing 10x CITE-seq in R and you need joint RNA+protein clustering. For ATAC + RNA WNN use signac-chromatin-analysis."
license: MIT
---

# Seurat CITE-seq + WNN

## Overview

CITE-seq pairs scRNA-seq with antibody-derived tags (ADT) on the same
cells. This skill covers the Seurat side: building the multi-assay
object, normalising each modality with its appropriate transform
(SCTransform for RNA, CLR for ADT), and joining them via Weighted
Nearest Neighbors (WNN).

**Pre-reqs:**
- `Seurat` v5+ installed
- 10x Cell Ranger CITE-seq output (Gene Expression + Antibody Capture
  matrices) or an existing multi-assay Seurat object

---

## Part 1 — Create the multimodal Seurat object

### From an existing dataset

```r
library(Seurat)
library(SeuratData)

# InstallData("bmcite")
bm <- LoadData(ds = "bmcite")

Assays(bm)                  # [1] "RNA" "ADT"
DefaultAssay(bm) <- "RNA"   # Switch active assay
```

### From raw 10x Cell Ranger output

```r
counts <- Read10X("filtered_feature_bc_matrix/")
# Returns a list: Gene Expression + Antibody Capture

seurat_obj <- CreateSeuratObject(
  counts        = counts$`Gene Expression`,
  project       = "CITE-seq",
  min.cells     = 3,
  min.features  = 200
)

seurat_obj[["ADT"]] <- CreateAssay5Object(counts = counts$`Antibody Capture`)
```

---

## Part 2 — QC and per-modality normalisation

```r
DefaultAssay(bm) <- "RNA"
bm <- PercentageFeatureSet(bm, pattern = "^MT-", col.name = "percent.mt")

# QC subset
bm <- subset(bm,
  nFeature_RNA > 200 &
  nFeature_RNA < 5000 &
  percent.mt < 10
)

# RNA: SCTransform (preferred over LogNormalize for CITE-seq)
DefaultAssay(bm) <- "RNA"
bm <- SCTransform(bm, verbose = FALSE)

# ADT: CLR normalisation along columns (margin = 2)
DefaultAssay(bm) <- "ADT"
bm <- NormalizeData(bm, normalization.method = "CLR", margin = 2)

# For ADT, typically use ALL antibodies (not HVG selection)
VariableFeatures(bm) <- rownames(bm[["ADT"]])
bm <- ScaleData(bm)
```

---

## Part 3 — Per-modality dimensionality reduction

```r
# RNA: PCA on SCT
DefaultAssay(bm) <- "SCT"
bm <- RunPCA(bm, verbose = FALSE)

# ADT: PCA on protein space (separate reduction slot)
DefaultAssay(bm) <- "ADT"
bm <- RunPCA(bm, reduction.name = "apca", verbose = FALSE)
```

---

## Part 4 — Weighted Nearest Neighbors (WNN)

```r
bm <- FindMultiModalNeighbors(
  bm,
  reduction.list        = list("pca", "apca"),
  dims.list             = list(1:30, 1:18),   # per-modality dims
  modality.weight.name  = "RNA.weight",
)

# WNN UMAP — joint embedding
bm <- RunUMAP(
  bm,
  nn.name        = "weighted.nn",
  reduction.name = "wnn.umap",
  reduction.key  = "wnnUMAP_",
)

# WNN clustering on the shared NN graph
bm <- FindClusters(
  bm,
  graph.name = "wsnn",
  algorithm  = 3,      # SLM
  resolution = 0.5,
  verbose    = FALSE,
)

DimPlot(bm, reduction = "wnn.umap", label = TRUE)
```

---

## Part 5 — Modality-weight interpretation

```r
# How much each modality contributes per cell
VlnPlot(bm, features = "RNA.weight", group.by = "celltype", pt.size = 0)
```

- High `RNA.weight` → RNA more informative for that cell type.
- High `1 - RNA.weight` → protein more informative (often myeloid /
  cell-surface-defined types).

---

## Part 6 — Protein marker visualisation

```r
DefaultAssay(bm) <- "ADT"
FeaturePlot(
  bm,
  features  = c("CD4", "CD8", "CD14", "CD19"),
  reduction = "wnn.umap",
  cols      = c("lightgrey", "darkgreen"),
  ncol      = 2,
)

# Compare RNA vs protein with side-by-side DotPlots
DefaultAssay(bm) <- "ADT"
p1 <- DotPlot(bm, features = rownames(bm), group.by = "celltype") +
        RotatedAxis() + ggtitle("Protein")

DefaultAssay(bm) <- "SCT"
p2 <- DotPlot(bm, features = c("CD4", "CD8A", "CD14", "CD19"),
              group.by = "celltype") +
        RotatedAxis() + ggtitle("RNA")
p1 | p2
```

---

## Common pitfalls

| Pitfall | Resolution |
|---|---|
| ADT row names have prefixes (`CD4_TotalSeqB`) | Strip prefixes with `rownames(bm[["ADT"]]) <- gsub(...)`. |
| ADT signal dominated by isotype controls | Remove isotype rows before normalisation. |
| WNN gives one-modality-dominant clusters | Inspect `RNA.weight` first — extreme bimodal distribution suggests one modality is uninformative for some cell types. |
| Wrong `margin` in CLR | `margin = 2` for CITE-seq (CLR along cells); `margin = 1` is a different operation. |

---

## API quick reference

```r
# Assay management
DefaultAssay(obj) <- "RNA"
obj[["ADT"]] <- CreateAssay5Object(counts = ...)

# WNN
FindMultiModalNeighbors(reduction.list = ..., dims.list = ...)
RunUMAP(nn.name = "weighted.nn", reduction.name = "wnn.umap")
FindClusters(graph.name = "wsnn", algorithm = 3)
```

---

## Resources

- WNN tutorial: https://satijalab.org/seurat/articles/weighted_nearest_neighbor_analysis
- Seurat v5 docs: https://satijalab.org/seurat/
- Stoeckius et al., Nature Methods 2017 (CITE-seq paper).

---

## When not to use

- Do not use for ATAC + RNA WNN — use signac-chromatin-analysis.
- Do not use to convert Seurat to AnnData — use anndatar-seurat-scanpy-conversion.

---

## See also

- `signac-chromatin-analysis`
- `seurat-multimodal-analysis`
- `anndatar-seurat-scanpy-conversion`
