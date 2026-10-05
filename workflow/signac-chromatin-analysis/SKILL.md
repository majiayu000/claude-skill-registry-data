---
name: signac-chromatin-analysis
description: "Signac (R) for chromatin accessibility — 10x Multiome RNA+ATAC processing, TF-IDF+LSI, WNN joint embedding, gene activity, ChromVAR motif enrichment, peak-gene linkage, and coverage plots. Use when analysing 10x Multiome in R with Seurat+Signac. For the Python path see snapatac2-atac-preprocessing."
license: MIT
---

# Signac Chromatin Analysis

## Overview

Signac is Seurat's companion package for scATAC-seq and 10x Multiome. It
adds a `ChromatinAssay` class, TF-IDF + LSI dimensionality reduction
(`RunTFIDF` / `RunSVD`), gene-activity scoring, ChromVAR motif
enrichment, and locus-level coverage plots — all interoperable with the
rest of Seurat.

**Pre-reqs:**
```r
install.packages(c("Seurat", "Signac"))
BiocManager::install(c("EnsDb.Hsapiens.v86", "BSgenome.Hsapiens.UCSC.hg38",
                       "JASPAR2020", "TFBSTools", "chromVAR", "motifmatchr"))
```

---

## Part 1 — Load 10x Multiome data

```r
library(Seurat)
library(Signac)
library(EnsDb.Hsapiens.v86)        # or EnsDb.Mmusculus.v79 for mouse

counts   <- Read10X_h5("filtered_feature_bc_matrix.h5")
fragpath <- "atac_fragments.tsv.gz"

# Gene annotations for the ChromatinAssay
annotations <- GetGRangesFromEnsDb(ensdb = EnsDb.Hsapiens.v86)
seqlevelsStyle(annotations) <- "UCSC"

seurat_obj <- CreateSeuratObject(counts = counts$`Gene Expression`, assay = "RNA")

seurat_obj[["ATAC"]] <- CreateChromatinAssay(
  counts      = counts$Peaks,
  sep         = c(":", "-"),
  fragments   = fragpath,
  annotation  = annotations,
)
```

---

## Part 2 — Multiome QC

```r
DefaultAssay(seurat_obj) <- "RNA"
seurat_obj <- PercentageFeatureSet(seurat_obj, pattern = "^MT-",
                                   col.name = "percent.mt")

DefaultAssay(seurat_obj) <- "ATAC"
seurat_obj <- NucleosomeSignal(seurat_obj)
seurat_obj <- TSSEnrichment(seurat_obj)

VlnPlot(seurat_obj,
        features = c("nCount_RNA", "nFeature_RNA", "percent.mt",
                     "nCount_ATAC", "TSS.enrichment", "nucleosome_signal"),
        ncol = 3, pt.size = 0)

seurat_obj <- subset(seurat_obj,
  nCount_ATAC < 100000 & nCount_RNA < 25000 &
  nCount_ATAC > 1000   & nCount_RNA > 1000   &
  nucleosome_signal < 2 & TSS.enrichment > 1
)
```

---

## Part 3 — Process each modality

### RNA: SCTransform + PCA

```r
DefaultAssay(seurat_obj) <- "RNA"
seurat_obj <- SCTransform(seurat_obj, verbose = FALSE)
seurat_obj <- RunPCA(seurat_obj, verbose = FALSE)
```

### ATAC: TF-IDF + LSI

```r
DefaultAssay(seurat_obj) <- "ATAC"
seurat_obj <- RunTFIDF(seurat_obj)
seurat_obj <- FindTopFeatures(seurat_obj, min.cutoff = "q0")
seurat_obj <- RunSVD(seurat_obj)        # = LSI

# CRITICAL: LSI component 1 often correlates with sequencing depth.
DepthCor(seurat_obj)
# If yes, exclude component 1 from `dims.list` below.
```

---

## Part 4 — WNN integration (RNA + ATAC)

The WNN chassis (`FindMultiModalNeighbors` → `RunUMAP(nn.name="weighted.nn")` → `FindClusters(graph.name="wsnn", algorithm=3)`) is identical to the CITE-seq workflow — see `seurat-citeseq-wnn` for the full pattern. ATAC-specific tweaks:

- `reduction.list = list("pca", "lsi")` (LSI replaces APCA)
- `dims.list = list(1:50, 2:40)` — skip LSI 1 if `DepthCor()` shows it correlates with sequencing depth

---

## Part 5 — Gene activity scores

```r
DefaultAssay(seurat_obj) <- "ATAC"
gene.activities <- GeneActivity(seurat_obj)

seurat_obj[["GeneActivity"]] <- CreateAssay5Object(counts = gene.activities)
seurat_obj <- NormalizeData(seurat_obj, assay = "GeneActivity",
                            normalization.method = "LogNormalize")

# Compare RNA vs gene-activity on the WNN UMAP
DefaultAssay(seurat_obj) <- "SCT"
p1 <- FeaturePlot(seurat_obj, features = "MS4A1", reduction = "wnn.umap") +
        ggtitle("MS4A1 RNA")

DefaultAssay(seurat_obj) <- "GeneActivity"
p2 <- FeaturePlot(seurat_obj, features = "MS4A1", reduction = "wnn.umap") +
        ggtitle("MS4A1 Activity")
p1 | p2
```

---

## Part 6 — Coverage plots

```r
DefaultAssay(seurat_obj) <- "ATAC"

CoveragePlot(
  seurat_obj,
  region            = "chr14-99700000-99760000",  # BCL11B
  features          = "BCL11B",
  assay             = "ATAC",
  extend.upstream   = 1000,
  extend.downstream = 1000,
)

# By group (one track per cluster)
CoveragePlot(seurat_obj, region = "MS4A1", group.by = "seurat_clusters")
```

---

## Part 7 — Differential accessibility

```r
DefaultAssay(seurat_obj) <- "ATAC"

da_peaks <- FindMarkers(
  seurat_obj,
  ident.1      = "0",
  ident.2      = "1",
  min.pct      = 0.05,
  test.use     = "LR",           # logistic regression: standard for ATAC
  latent.vars  = "nCount_ATAC",  # control for depth
)

# Annotate with nearest gene
closest_genes <- ClosestFeature(seurat_obj, regions = rownames(da_peaks))
da_peaks$gene <- closest_genes$gene_name
```

---

## Part 8 — Motif analysis (ChromVAR)

```r
library(JASPAR2020); library(TFBSTools); library(BSgenome.Hsapiens.UCSC.hg38)

DefaultAssay(seurat_obj) <- "ATAC"

pwm_set <- getMatrixSet(JASPAR2020,
  opts = list(collection = "CORE", tax_group = "vertebrates",
              all_versions = FALSE))

seurat_obj <- AddMotifs(seurat_obj, genome = BSgenome.Hsapiens.UCSC.hg38,
                        pfm = pwm_set)
seurat_obj <- RunChromVAR(seurat_obj, genome = BSgenome.Hsapiens.UCSC.hg38)

DefaultAssay(seurat_obj) <- "chromvar"

FeaturePlot(seurat_obj, features = "MA0139.1", reduction = "wnn.umap")  # CTCF

differential.activity <- FindMarkers(
  seurat_obj,
  ident.1   = "B_cells",
  ident.2   = "T_cells",
  only.pos  = TRUE,
  mean.fxn  = rowMeans,
  fc.name   = "avg_diff",
)

motif.names <- rownames(differential.activity) |>
  ConvertMotifID(object = seurat_obj)
```

---

## Part 9 — Peak-gene linkage

```r
DefaultAssay(seurat_obj) <- "ATAC"

seurat_obj <- RegionStats(seurat_obj, genome = BSgenome.Hsapiens.UCSC.hg38)
seurat_obj <- LinkPeaks(
  seurat_obj,
  peak.assay        = "ATAC",
  expression.assay  = "SCT",
  genes.use         = c("MS4A1", "CD3D", "CD8A"),
)

# Coverage plot with peak-gene links overlaid
CoveragePlot(seurat_obj, region = "MS4A1", features = "MS4A1",
             expression.assay = "SCT", links = TRUE)

links <- Links(seurat_obj)
```

---

## Common pitfalls

| Pitfall | Resolution |
|---|---|
| Fragment file not indexed | Run `tabix -p bed atac_fragments.tsv.gz`. |
| EnsDb version mismatches alignment | Match `EnsDb.Hsapiens.v86` etc. to the Cell Ranger reference. |
| LSI component 1 correlates with depth | Use `dims = 2:N` everywhere downstream. |
| `RunChromVAR` fails | Genome package style (`UCSC` vs `Ensembl`) must match `seqlevelsStyle(annotations)`. |
| WNN modality dominated by ATAC | Inspect `RNA.weight` distribution; tune `dims.list`. |

---

## API quick reference

```r
# Chromatin assay
CreateChromatinAssay(counts, sep, fragments, annotation)
RunTFIDF() / FindTopFeatures() / RunSVD()  # LSI pipeline
DepthCor()                                 # check LSI 1 vs depth

# Gene activity
GeneActivity()

# Motifs
AddMotifs(); RunChromVAR(); ConvertMotifID()

# Linkage / coverage
LinkPeaks(); RegionStats(); CoveragePlot()
ClosestFeature()                           # nearest gene to a peak

# WNN (same as seurat-citeseq-wnn)
FindMultiModalNeighbors(); FindClusters(graph.name = "wsnn")
```

---

## Resources

- Signac docs: https://stuartlab.org/signac/
- ChromVAR: https://greenleaflab.github.io/chromVAR/
- JASPAR: https://jaspar.genereg.net/
- Stuart et al., Nature Methods 2021 — Signac paper.

---

## When not to use

- Do not use for Python ATAC workflows — use snapatac2-atac-preprocessing.
- Do not use for protein + RNA CITE-seq — use seurat-citeseq-wnn.

---

## See also

- `seurat-citeseq-wnn`
- `seurat-multimodal-analysis`
- `chromvar-motif-accessibility`
- `snapatac2-atac-preprocessing`
