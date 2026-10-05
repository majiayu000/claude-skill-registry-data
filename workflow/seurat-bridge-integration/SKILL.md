---
name: seurat-bridge-integration
description: "Seurat bridge integration — map an ATAC-only query onto an RNA-only reference via a multiome bridge dataset, plus Azimuth reference mapping for paired or RNA-only queries. Use when an scATAC query needs labels transferred from a well-annotated scRNA reference. For unpaired integration without a bridge use seurat-unpaired-cross-modality."
license: MIT
---

# Seurat Bridge Integration & Azimuth Mapping

## Overview

Two related workflows for transferring annotations from a well-curated
reference onto a query dataset:

| Workflow | Use when |
|---|---|
| Azimuth (`RunAzimuth`) | Query is RNA-only (or has been WNN-integrated) and matches a SeuratData reference. |
| Bridge integration (`FindBridgeTransferAnchors`) | Query is ATAC-only, no matched RNA; a multiome bridge dataset connects ATAC space → RNA space. |

**Pre-reqs:**
```r
install.packages(c("Seurat", "Signac"))
install.packages("SeuratData")
install.packages("Azimuth")
```

---

## Part 1 — Azimuth: RNA query → RNA reference

```r
library(Azimuth)
library(SeuratData)

# InstallData("pbmcref")
reference <- LoadData("pbmcref")

# Map a query Seurat object (RNA assay must be present)
query <- RunAzimuth(query = seurat_obj, reference = "pbmcref")

head(query$predicted.celltype.l2)
head(query$predicted.celltype.l2.score)

DimPlot(query, group.by = "predicted.celltype.l2", reduction = "wnn.umap")
```

Azimuth runs an internal SCTransform on the query, finds anchors against
the reference's pre-computed PCA, and transfers both labels and the
reference UMAP coordinates.

**Quality check:**
- `predicted.celltype.l2.score > 0.5` is a conventional minimum for
  "well-anchored" cells.
- `mapping.score > 0.5` likewise — Azimuth provides two distinct scores.

---

## Part 2 — Bridge integration: ATAC query → RNA reference

The bridge is a **paired multiome dataset** (RNA + ATAC on the same
cells) that shares cell types with both the ATAC query and the RNA
reference. Anchors are found by projecting the ATAC query into the
bridge's LSI, then finding nearest neighbours in the bridge's RNA space.

```r
library(Seurat); library(Signac); library(SeuratData)

# Load the three datasets
atac_query <- LoadData("pbmc_multiome_atac")
bridge     <- LoadData("pbmc_multiome")        # has RNA + ATAC
reference  <- LoadData("pbmcref")              # RNA only

# Preprocess the bridge — must process BOTH modalities
DefaultAssay(bridge) <- "RNA"
bridge <- SCTransform(bridge, verbose = FALSE)
bridge <- RunPCA(bridge, verbose = FALSE)

DefaultAssay(bridge) <- "ATAC"
bridge <- RunTFIDF(bridge)
bridge <- FindTopFeatures(bridge, min.cutoff = "q0")
bridge <- RunSVD(bridge)

# Find anchors via the bridge
anchors <- FindBridgeTransferAnchors(
  reference  = reference,
  bridge     = bridge,
  query      = atac_query,
  reduction  = "lsiproject",   # project ATAC query into bridge LSI space
  dims       = 2:30,            # skip LSI 1
)

# Transfer labels (and project query onto reference UMAP)
atac_query <- MapQuery(
  anchorset       = anchors,
  reference       = reference,
  query           = atac_query,
  refdata         = list(l1 = "celltype.l1", l2 = "celltype.l2"),
  reduction.model = "wnn.umap",
)

DimPlot(atac_query, group.by = "predicted.l2")
```

---

## Part 3 — Bridge prerequisites

The bridge must:

1. **Share cell types** with both the query (ATAC) and the reference (RNA).
   A bridge of PBMC multiome cannot annotate a brain ATAC dataset.
2. **Span the same protocol / batch domain** as the query when possible.
   Strong batch effects between bridge and query degrade anchor quality.
3. **Be preprocessed in both modalities** — RNA through SCTransform + PCA,
   ATAC through RunTFIDF + RunSVD.

---

## Common pitfalls

| Pitfall | Resolution |
|---|---|
| Low mapping scores | Check that bridge cell types overlap query AND reference. |
| Missing features after `RunTFIDF` | Ensure peak set is consistent between bridge and query (or harmonise to a common peak set first). |
| Azimuth refuses to run | Confirm the reference name (`pbmcref`, `tonsilref`, `lungref`, ...) and that `SeuratData::AvailableData()` lists it. |
| Memory blow-up on bridge | The bridge can be downsampled — 10-20 k cells often suffices. |

---

## API quick reference

```r
# Azimuth
RunAzimuth(query, reference)

# Bridge integration
FindBridgeTransferAnchors(reference, bridge, query,
                          reduction = "lsiproject", dims = 2:30)
MapQuery(anchorset, reference, query,
         refdata = list(...), reduction.model = "wnn.umap")
```

---

## Resources

- Bridge integration tutorial: https://satijalab.org/seurat/articles/seurat5_integration_bridge
- Azimuth: https://azimuth.hubmapconsortium.org/
- Hao et al., Cell 2021 — Azimuth + reference-mapping paper.

---

## When not to use

- Do not use without a multiome bridge dataset — see seurat-unpaired-cross-modality.
- Do not use for hierarchical label transfer with deep tree priors — see treearches-hierarchy-learning.

---

## See also

- `seurat-unpaired-cross-modality`
- `signac-chromatin-analysis`
- `seurat-multimodal-analysis`
- `treearches-hierarchy-learning`
