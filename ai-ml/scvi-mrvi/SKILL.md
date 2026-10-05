---
name: scvi-mrvi
description: "MrVI from scvi-tools — multi-resolution variational inference for multi-donor scRNA-seq, modeling sample identity as biological rather than nuisance variation. Use for cohort studies needing cell-type-specific sample-to-sample distances and covariate-linked DE at single-cell resolution. sample_key is distinct from batch_key."
license: MIT
---

# MrVI: Multi-Sample Analysis

**Foundation:** inherits shared patterns from `scvi-framework`. Jump to:
- `scvi-framework/references/setup-anndata.md` — **critical**: `sample_key` (biological) vs `batch_key` (technical)
- `scvi-framework/references/training-and-gpu.md`
- `scvi-framework/references/common-outputs.md`
- `scvi-framework/references/gotchas.md`, `scvi-framework/checks/pre-train-checklist.md`

This file covers only the parts that differ for MrVI (multi-donor cohort modeling).

## When to Use MrVI

- Multi-donor/multi-sample studies (COVID severity, aging, treatment response)
- Sample-level comparisons at single-cell resolution (not pseudobulk)
- Covariate-linked differential expression
- Cell-type-specific sample distances

**Key difference from scVI:**
- scVI: `batch_key` = technical variation to remove
- MrVI: `sample_key` = biological variation to study

---

## Quick Start

```python
from scvi.external import MRVI

# Setup with sample as the biological key
MRVI.setup_anndata(
    adata,
    layer="counts",
    sample_key="sample_id",       # Biological samples (REQUIRED)
    batch_key="sequencing_run",   # Technical batches (optional, nuisance)
)

model = MRVI(adata, n_latent=30)
model.train()

# Dual latent spaces
adata.obsm["X_u"] = model.get_latent_representation(give_z=False)  # Sample-invariant
adata.obsm["X_z"] = model.get_latent_representation(give_z=True)   # Sample-aware
```

---

## Dual Latent Representations

MrVI learns two complementary embeddings:

| Representation | Access | Use |
|---------------|--------|-----|
| `u` (sample-invariant) | `get_latent_representation(give_z=False)` | Cell type identification, UMAP |
| `z` (sample-aware) | `get_latent_representation(give_z=True)` | Sample effects, heterogeneity |

```python
# Use u for cell type clustering
adata.obsm["X_MrVI_u"] = model.get_latent_representation(give_z=False)
sc.pp.neighbors(adata, use_rep="X_MrVI_u")
sc.tl.umap(adata)
sc.tl.leiden(adata)
```

---

## Sample Distances

Compute cell-type-specific sample-to-sample distances:

```python
# Cell-type-specific sample distances
distance_df = model.get_local_sample_representation(
    keep_cell=False,  # Aggregate per cell type
)

# Returns DataFrame: samples × samples × cell_types
# Use for hierarchical clustering of samples within each cell type
```

---

## Covariate-Linked DE

Attribute expression changes to specific sample covariates:

```python
# Associate sample covariates
adata.obs["severity"] = adata.obs["sample_id"].map(sample_to_severity)
adata.obs["age"] = adata.obs["sample_id"].map(sample_to_age)

# Get DE effects linked to covariates
de_results = model.differential_expression(
    sample_cov_keys=["severity", "age"],  # Covariates to test
    store_lfc=True,
)

# Returns per-gene effects attributable to each covariate
```

---

## Differential Abundance

Test covariate-linked changes in cell composition:

```python
da_results = model.differential_abundance(
    sample_cov_keys=["severity"],
    cell_type_key="cell_type",
)

# Which cell types change abundance with severity?
```

---

## Key Model Parameters

```python
model = MRVI(
    adata,
    n_latent=30,               # Latent dimensions
    n_latent_u=10,             # u-space dimensions (sample-invariant)
    n_hidden=128,
    n_layers=2,
)

model.train(
    max_epochs=400,
    early_stopping=True,
    batch_size=256,
)
```

---

## Data Requirements

| Requirement | Details |
|-------------|---------|
| Multiple samples | ≥10 samples recommended per condition |
| Sample key | Biological replicates (donors, subjects) |
| Comparable cells | Similar cell types across samples |
| Raw counts | As with all scvi-tools models |

---

## Critical Gotchas

| Issue | Solution |
|-------|----------|
| `sample_key` vs `batch_key` confusion | `sample_key` = what you study; `batch_key` = technical noise |
| Few samples per condition | MrVI needs sufficient samples for covariate effects |
| Imbalanced cell types | Some cell types may be absent in some samples |
| JAX errors | Ensure compatible JAX/CUDA versions |

---

## Resources

- **Docs:** https://docs.scvi-tools.org/en/stable/user_guide/models/mrvi.html
- **Tutorial:** https://docs.scvi-tools.org/en/stable/tutorials/notebooks/scrna/MrVI_tutorial.html
- **Paper:** https://www.biorxiv.org/content/10.1101/2022.10.04.510898

---

## When not to use

- Do not use on normalized / log-transformed data. Raw counts required.
- Do not confuse sample_key with batch_key. Sample is the biological variable; batch is technical nuisance.
- Do not use for single-sample or small-cohort datasets. MrVI shines with many samples.

---

## See also

- `scvi-framework`
- `scvi-basic`
- `scvi-scanvi`
- `anndata`
- `scanpy`
