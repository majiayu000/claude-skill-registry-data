---
name: seurat-multimodal-analysis
description: "Orchestrator for R/Seurat multimodal single-cell analysis — chains CITE-seq WNN, Signac chromatin analysis, bridge integration, and unpaired RNA+ATAC anchoring across four leaf skills. Use as the entry point when the project is R-based and must stay in Seurat. For the Python scverse use muon-multimodal-analysis."
license: MIT
---

# Seurat Multimodal Analysis — Orchestrator

## Overview

This skill is the **entry point** for R-side multimodal scRNA-seq
analysis. It does not duplicate per-tool tutorial content — that lives
in the leaf skills listed below. Its job is to choreograph
the workflow: when to use CITE-seq WNN vs Signac multiome, when to add
a bridge dataset, and when unpaired anchoring is the right tool.

**The leaves (mounted flat alongside this skill; load each on demand):**

| Leaf | Role in the workflow |
|---|---|
| `seurat-citeseq-wnn` | CITE-seq RNA + ADT, WNN joint embedding |
| `signac-chromatin-analysis` | 10x Multiome RNA + ATAC, ChromVAR, peak-gene links |
| `seurat-bridge-integration` | Azimuth + bridge-integration label transfer |
| `seurat-unpaired-cross-modality` | CCA anchoring on gene activity (no bridge) |
| `harmonypy-batch-integration` | Per-modality batch correction for multi-sample workflows |
| `anndatar-seurat-scanpy-conversion` | Seurat ↔ AnnData (h5ad) conversion |
| `louper-seurat-conversion` | Loupe Browser ↔ Seurat conversion |

---

## Decision tree — which leaf do I need?

```
Modalities?
├── RNA + protein (CITE-seq)
│   └── seurat-citeseq-wnn
├── RNA + ATAC, paired (10x Multiome)
│   └── signac-chromatin-analysis
├── RNA-only query against an annotated reference
│   └── seurat-bridge-integration  (Azimuth path)
├── ATAC-only query, multiome bridge available
│   └── seurat-bridge-integration  (bridge path)
└── ATAC-only query, NO bridge
    └── seurat-unpaired-cross-modality  (CCA on gene activity)

Multiple samples / batches?
└── harmonypy-batch-integration on each modality's reduction
    (use `harmony` R package via SeuratWrappers, or run harmonypy
     through reticulate — same algorithm, same expected result)

Need to export to Python downstream?
└── anndatar-seurat-scanpy-conversion (h5ad)
    or louper-seurat-conversion (Loupe Browser)
```

---

## Canonical workflow — CITE-seq

See `seurat-citeseq-wnn` for full code. High-level chassis:

```r
library(Seurat)
seu <- CreateSeuratObject(counts$`Gene Expression`)
seu[["ADT"]] <- CreateAssay5Object(counts$`Antibody Capture`)

DefaultAssay(seu) <- "RNA"; seu <- SCTransform(seu)
DefaultAssay(seu) <- "ADT"; seu <- NormalizeData(seu, "CLR", margin = 2)

DefaultAssay(seu) <- "SCT"; seu <- RunPCA(seu)
DefaultAssay(seu) <- "ADT"; seu <- RunPCA(seu, reduction.name = "apca")

seu <- FindMultiModalNeighbors(seu,
         reduction.list = list("pca", "apca"),
         dims.list      = list(1:30, 1:18))
seu <- RunUMAP(seu, nn.name = "weighted.nn", reduction.name = "wnn.umap")
seu <- FindClusters(seu, graph.name = "wsnn", algorithm = 3)
```

## Canonical workflow — 10x Multiome

See `signac-chromatin-analysis`. Chassis:

```r
counts   <- Read10X_h5("filtered_feature_bc_matrix.h5")
seu      <- CreateSeuratObject(counts$`Gene Expression`, assay = "RNA")
seu[["ATAC"]] <- CreateChromatinAssay(
                   counts = counts$Peaks, sep = c(":", "-"),
                   fragments = "atac_fragments.tsv.gz",
                   annotation = GetGRangesFromEnsDb(EnsDb.Hsapiens.v86))

# QC: TSSEnrichment, NucleosomeSignal
# RNA: SCTransform + RunPCA
# ATAC: RunTFIDF + FindTopFeatures + RunSVD
# WNN: FindMultiModalNeighbors(dims.list = list(1:50, 2:40))
# Downstream: GeneActivity, AddMotifs + RunChromVAR, LinkPeaks, CoveragePlot
```

---

## Multi-sample integration (Part 5 of the original monolith)

For multi-sample paired-modality workflows, the **per-modality** pattern
applies: integrate each modality's reduction with Harmony before
constructing the WNN graph. The integration logic itself lives in
`harmonypy-batch-integration` — the same algorithm is invoked from R via
the `harmony` package (`SeuratWrappers::RunHarmony` wraps it) or by
calling `harmonypy` through `reticulate`. The choice is purely
operational; results match.

```r
# Sketch — see harmonypy-batch-integration for the conceptual contract
library(harmony)

DefaultAssay(merged) <- "SCT"
merged <- RunHarmony(merged, group.by.vars = "sample",
                     reduction = "pca",
                     reduction.save = "pca.harmony")

DefaultAssay(merged) <- "ATAC"
merged <- RunHarmony(merged, group.by.vars = "sample",
                     reduction = "lsi", dims.use = 2:30,
                     reduction.save = "lsi.harmony")

# Then WNN on the harmonised reductions
merged <- FindMultiModalNeighbors(merged,
            reduction.list = list("pca.harmony", "lsi.harmony"),
            dims.list      = list(1:30, 2:30))
```

---

## Conversion to / from Python

The toolkit ships two leaves for this:

- `anndatar-seurat-scanpy-conversion` — bidirectional h5ad ↔ Seurat
  conversion via `anndataR` (preferred for losslessness).
- `louper-seurat-conversion` — Seurat ↔ Loupe Browser `.cloupe` files.

The orchestrator itself does NOT cover conversion details — defer to
those leaves.

---

## Cross-cutting pitfalls

### Data preparation
| Pitfall | Resolution |
|---|---|
| ADT row names have prefixes | Strip prefixes before analysis. |
| Fragment file not indexed | `tabix -p bed atac_fragments.tsv.gz`. |
| Wrong genome annotation version | Match EnsDb version to your Cell Ranger reference. |
| Missing peaks for some cells | Check Cell Ranger QC; consider re-running with looser thresholds. |

### WNN integration
| Pitfall | Resolution |
|---|---|
| One modality dominates | Inspect `RNA.weight`; rebalance via `dims.list`. |
| LSI component 1 correlates with depth | Always exclude (use `2:30`, never `1:30`). |
| Poor WNN clustering | Check each modality's own UMAP first — WNN cannot fix a broken modality. |

### Reference mapping
| Pitfall | Resolution |
|---|---|
| Low Azimuth mapping scores | Confirm the right reference; check `predicted.celltype.l2.score`. |
| Bridge integration anchors weak | Bridge must share cell types with both query and reference. |

---

## API quick reference

```r
# Multi-assay basics
DefaultAssay(obj) <- "RNA"
obj[["NewAssay"]] <- CreateAssay5Object(counts = ...)
GetAssayData(obj, assay = "RNA", layer = "counts")

# WNN
FindMultiModalNeighbors(reduction.list = ..., dims.list = ...)
RunUMAP(nn.name = "weighted.nn", reduction.name = "wnn.umap")
FindClusters(graph.name = "wsnn", algorithm = 3)
```

Per-leaf API surfaces are documented in their respective SKILL.md
files.

---

## Resources

- Seurat v5:          https://satijalab.org/seurat/
- Signac:             https://stuartlab.org/signac/
- WNN tutorial:       https://satijalab.org/seurat/articles/weighted_nearest_neighbor_analysis
- Multiome tutorial:  https://satijalab.org/seurat/articles/seurat5_multimodal_vignette
- Bridge integration: https://satijalab.org/seurat/articles/seurat5_integration_bridge
- ChromVAR:           https://greenleaflab.github.io/chromVAR/
- JASPAR:             https://jaspar.genereg.net/


---

## When not to use

- Do not use for Python/scverse workflows. Use muon-multimodal-analysis instead.
- Do not use to convert Seurat objects to AnnData/MuData. Use multimodal-anndata-mudata.

---

## See also

- `muon-multimodal-analysis`
- `scglue-unpaired-multiomics-integration`
