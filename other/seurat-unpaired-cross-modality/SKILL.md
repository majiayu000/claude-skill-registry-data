---
name: seurat-unpaired-cross-modality
description: "Seurat unpaired RNA-ATAC integration via gene-activity anchoring — CCA-based FindTransferAnchors, TransferData label transfer, and exploratory expression imputation for ATAC cells. Use with separate scRNA and scATAC experiments (NOT true multiome) and no bridge dataset. For the Python equivalent use scglue-unpaired-multiomics-integration."
license: MIT
---

# Seurat Unpaired Cross-Modality Integration

## Overview

When you have **separate** scRNA-seq and scATAC-seq experiments from the
same biological system (but not the same cells), Seurat can transfer
labels between them by treating the gene-activity matrix from ATAC as a
proxy for RNA. CCA is used to find shared structure in this synthetic
shared feature space.

**When to reach for this skill:**
- No paired multiome data, no bridge dataset.
- Gene-activity matrix already computed in the ATAC object (via
  `Signac::GeneActivity()`).
- You want cell-type labels transferred from an RNA reference onto the
  ATAC cells, or RNA expression imputed for the ATAC cells.

**When NOT to reach for this skill:**
- Paired multiome — use `signac-chromatin-analysis` (WNN is strictly
  better when both modalities are on the same cell).
- A multiome bridge dataset is available — use
  `seurat-bridge-integration`.
- The Python ecosystem is preferred — use
  `scglue-unpaired-multiomics-integration`.

---

## Part 1 — Find CCA transfer anchors

```r
# Gene activity must already exist in atac_obj's "RNA" slot
# (i.e. assigned via atac_obj[["RNA"]] <- GeneActivity-based assay)

DefaultAssay(rna_ref) <- "RNA"
DefaultAssay(atac_obj) <- "RNA"   # gene activity scores

rna_ref <- FindVariableFeatures(rna_ref, nfeatures = 3000)

transfer.anchors <- FindTransferAnchors(
  reference        = rna_ref,
  query            = atac_obj,
  features         = VariableFeatures(rna_ref),
  reference.assay  = "RNA",
  query.assay      = "RNA",       # gene-activity scores
  reduction        = "cca",       # CCA for cross-modality (NOT rpca)
  dims             = 1:30,
)
```

**Critical:** use `reduction = "cca"`. `rpca` does not handle the
modality gap and gives near-random anchors.

---

## Part 2 — Transfer labels

```r
predictions <- TransferData(
  anchorset         = transfer.anchors,
  refdata           = rna_ref$cell_annotations,
  weight.reduction  = atac_obj[["lsi"]],
  dims              = 2:30,       # skip LSI 1 (depth-correlated)
)

atac_obj <- AddMetaData(atac_obj, predictions)

# QC: well-anchored cells have prediction.score.max > 0.5
sum(atac_obj$prediction.score.max > 0.5) / ncol(atac_obj)
```

The `weight.reduction = atac_obj[["lsi"]]` argument tells Seurat to use
the ATAC native embedding (not gene activity) when weighting anchors —
this preserves ATAC-resolved structure.

---

## Part 3 — Expression imputation (exploratory)

```r
refdata <- GetAssayData(rna_ref, assay = "RNA", layer = "data")[
              VariableFeatures(rna_ref), ]

imputation <- TransferData(
  anchorset         = transfer.anchors,
  refdata           = refdata,
  weight.reduction  = atac_obj[["lsi"]],
  dims              = 2:30,
)

atac_obj[["imputed_RNA"]] <- imputation
```

Imputed expression is suitable for **population-level** TF-gene
hypotheses, not single-cell regulatory dynamics.

---

## Part 4 — Quality and limitations

| What works well | What does NOT |
|---|---|
| Label transfer (~90 % accuracy on Ma et al. benchmark) | Single-cell-resolution regulatory inference |
| Co-embedding in a shared UMAP | Rare cell states (too few anchors) |
| Population-level gene signatures | Enhancer-driven expression (gene activity misses distal regulation) |
| Validation layer for ChromVAR TF activity | Dynamic range — variance is compressed |

**For GRN inference:** Imputed expression is suitable for
population-level TF-gene relationships but NOT single-cell regulatory
dynamics. For publication-quality GRN, use the SCENIC+ metacell approach
(`scenic-grn-inference`). Seurat imputation can serve as a validation
layer for SCENIC+ eRegulons.

**Benchmark reference:** Ma et al., Genome Biology 2023 — Seurat and
scGLUE were the top two methods for unpaired RNA+ATAC integration.

---

## Common pitfalls

| Pitfall | Resolution |
|---|---|
| Random-looking label transfer | Confirm `reduction = "cca"`, not `"rpca"`. |
| All `prediction.score.max` near 0 | Variable features in reference not present in gene-activity matrix; recompute gene activity with a matching annotation. |
| Imputed expression is smooth-looking | Expected — gene activity is already smoothed; do not over-interpret single-cell patterns. |
| LSI component 1 sneaks back in | Always pass `dims = 2:30` to `TransferData` when using `weight.reduction = atac_obj[["lsi"]]`. |

---

## API quick reference

```r
# Anchor finding
FindTransferAnchors(reference, query, features, reduction = "cca",
                    reference.assay, query.assay, dims = 1:30)

# Label / expression transfer
TransferData(anchorset, refdata, weight.reduction = obj[["lsi"]],
             dims = 2:30)
```

---

## Resources

- Cross-modality integration vignette:
  https://satijalab.org/seurat/articles/atacseq_integration_vignette
- Ma et al., Genome Biology 2023 (benchmark).
- Stuart et al., Cell 2019 (CCA anchoring methodology).

---

## When not to use

- Do not use for paired multiome data — use signac-chromatin-analysis.
- Do not use for single-cell-resolution GRN inference — gene-activity smoothing is too coarse; use scenic-grn-inference.

---

## See also

- `signac-chromatin-analysis`
- `seurat-bridge-integration`
- `scglue-unpaired-multiomics-integration`
- `scenic-grn-inference`
