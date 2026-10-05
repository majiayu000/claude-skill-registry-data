---
name: scvi-multivi
description: "MultiVI jointly integrates paired and unpaired single-cell RNA and ATAC via scvi-tools, producing a shared latent embedding with cross-modality imputation. Use when combining 10x Multiome with RNA-only or ATAC-only datasets, or running DE plus DA on joint embeddings. For ATAC-only use scvi-peakvi."
license: MIT
---

# MultiVI: RNA + ATAC Multimodal Integration

**Foundation:** inherits shared patterns from `scvi-framework`. Jump to:
- `scvi-framework/references/setup-anndata.md` — concatenated RNA+ATAC feature registration
- `scvi-framework/references/training-and-gpu.md`
- `scvi-framework/references/common-outputs.md`
- `scvi-framework/references/interop-matrix.md` — MultiVI ↔ PeakVI transitions
- `scvi-framework/references/gotchas.md`, `scvi-framework/checks/pre-train-checklist.md`

This file covers only the parts that differ for MultiVI (joint RNA+ATAC).

## When to Use MultiVI

- Integrating multiome (paired RNA+ATAC) with unimodal data
- Joint embedding of RNA-only, ATAC-only, and paired cells
- Cross-modality imputation
- Differential expression + accessibility testing

**Requirements:** Features must be ordered: genes first, then peaks. Shared peak set across datasets (requires re-calling peaks on merged fragments).

---

## Quick Start

```python
import scvi
import anndata

# Prepare: concatenate [genes | peaks] in feature axis
# adata.var has 'modality' column: "Gene Expression" or "Peaks"

scvi.model.MULTIVI.setup_anndata(
    adata,
    layer="counts",
    batch_key="batch",
    modality_key="modality",  # Distinguishes genes from peaks
)

model = scvi.model.MULTIVI(adata, n_latent=20)
model.train()

adata.obsm["X_MultiVI"] = model.get_latent_representation()
```

---

## Data Preparation

```python
import anndata

# RNA data: genes as features
rna_adata = sc.read_h5ad("rna.h5ad")
rna_adata.var["modality"] = "Gene Expression"

# ATAC data: peaks as features
atac_adata = sc.read_h5ad("atac.h5ad")
atac_adata.var["modality"] = "Peaks"

# Paired multiome: already has both
paired_adata = sc.read_h5ad("multiome.h5ad")
paired_adata.var["modality"] = ["Gene Expression"] * n_genes + ["Peaks"] * n_peaks

# Concatenate cells, union of features
# CRITICAL: genes must come before peaks in var_names
adata = anndata.concat([rna_adata, atac_adata, paired_adata], join="outer")
adata.layers["counts"] = adata.X.copy()
```

---

## Key Model Parameters

```python
model = scvi.model.MULTIVI(
    adata,
    n_hidden=128,
    n_latent=20,             # Latent dimensions
    region_factors=True,     # Learn region-specific scaling (recommended)
    fully_paired=False,      # Set True if ALL cells have both modalities
    n_layers_encoder=2,
    n_layers_decoder=2,
)

model.train(
    max_epochs=500,
    early_stopping=True,
    batch_size=256,
)
```

---

## Outputs

```python
# Joint latent representation
latent = model.get_latent_representation()

# Normalized gene expression (denoised)
norm_expr = model.get_normalized_expression()

# Accessibility probability per peak
accessibility = model.get_accessibility_estimates()

# Impute missing modality
# For RNA-only cells: impute ATAC
# For ATAC-only cells: impute RNA
imputed_rna = model.get_normalized_expression(
    adata=atac_only_adata,
    imputation=True
)
```

---

## Differential Analysis

```python
# Differential expression (genes)
de = model.differential_expression(
    groupby="cell_type",
    group1="cDC1A",
    group2="cDC1B",
    mode="change"
)

# Differential accessibility (peaks)
da = model.differential_accessibility(
    groupby="cell_type",
    group1="cDC1A",
    group2="cDC1B",
    mode="change"
)
```

---

## Critical Gotchas

| Issue | Solution |
|-------|----------|
| Feature order wrong | Genes MUST come before peaks in `var_names` |
| Peaks don't match | Re-call peaks on merged fragment files |
| Missing modality indicator | Each cell needs `modality_key` in `obs` or inferred from data |
| OOM errors | Reduce features; use `fully_paired=True` if applicable |

---

## Resources

- **Docs:** https://docs.scvi-tools.org/en/stable/user_guide/models/multivi.html
- **Tutorial:** https://docs.scvi-tools.org/en/stable/tutorials/notebooks/multimodal/MultiVI_tutorial.html
- **Paper:** https://www.biorxiv.org/content/10.1101/2021.08.11.455920

---

## When not to use

- Do not use for ATAC-only datasets. Use scvi-peakvi instead.
- Do not use for unpaired multi-omics where cells are not shared. Use scglue-unpaired-multiomics-integration.

---

## See also

- `scvi-framework`
- `scvi-peakvi`
- `scglue-unpaired-multiomics-integration`
- `cellranger-arc-multiome`
- `muon-multimodal-analysis` — for loading, storing, and manipulating the paired RNA+ATAC `MuData` object that MultiVI's inputs and outputs are typically organized around
