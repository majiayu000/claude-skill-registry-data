---
name: scvi-basic
description: scVI — probabilistic deep generative model for scRNA-seq integration and batch correction. Use for unsupervised integration across batches or samples, building a latent space for downstream analysis, or as a preprocessing step before scANVI. Requires raw counts. For semi-supervised annotation use scvi-scanvi; for multiome use scvi-multivi.
license: MIT
---

# scVI: Basic Integration and Batch Correction

**Foundation:** `scvi-framework` is the router and holds all shared patterns. Jump directly to:
- `scvi-framework/references/setup-anndata.md` — batch/covariate registration, raw-count rule
- `scvi-framework/references/training-and-gpu.md` — train call and GPU settings
- `scvi-framework/references/common-outputs.md` — latent, normalized expression, Bayesian DE
- `scvi-framework/references/count-distributions.md` — ZINB vs NB for scRNA
- `scvi-framework/references/gotchas.md` — shared symptom/cause/fix table
- `scvi-framework/checks/pre-train-checklist.md` — pre-flight before `.train()`

This file covers only the parts that differ for scVI.

## When to Use scVI

- Unsupervised integration (no cell type labels)
- As a preprocessing step before scANVI
- Differential expression between conditions
- Building a latent space for downstream analysis

**Limitations:** Requires GPU for speed; latent space not directly interpretable.

---

## Quick Start

```python
import scvi
import scanpy as sc

scvi.settings.seed = 42

# Prep (raw counts required)
adata.layers["counts"] = adata.X.copy()
sc.pp.highly_variable_genes(adata, n_top_genes=2000, flavor="seurat_v3",
                            layer="counts", batch_key="batch", subset=True)

# Train
scvi.model.SCVI.setup_anndata(adata, layer="counts", batch_key="batch")
model = scvi.model.SCVI(adata, n_latent=30, n_layers=2, gene_likelihood="nb")
model.train()

# Use
adata.obsm["X_scVI"] = model.get_latent_representation()
sc.pp.neighbors(adata, use_rep="X_scVI")
sc.tl.umap(adata)
```

---

## Key Model Parameters

```python
model = scvi.model.SCVI(
    adata,
    n_hidden=128,          # Hidden layer size
    n_latent=30,           # Latent dimensions (10-50 typical)
    n_layers=2,            # Hidden layers
    dropout_rate=0.1,
    gene_likelihood="nb",  # "zinb" (default) or "nb" (often better for integration)
    dispersion="gene",     # "gene", "gene-batch", or "gene-label"
)
```

**Gene likelihood tip:** Try `"nb"` if integration looks poor with default `"zinb"`.

---

## Library Size Handling

```python
# Default: observed library size (recommended)
model = scvi.model.SCVI(adata, use_observed_lib_size=True)

# Model library size as latent (rare cases)
model = scvi.model.SCVI(adata, use_observed_lib_size=False)

# Manual size factors
adata.obs["size_factor"] = your_factors
scvi.model.SCVI.setup_anndata(adata, size_factor_key="size_factor")
```

---

## Outputs

```python
# Latent representation (posterior mean)
latent = model.get_latent_representation()

# Sample from posterior (uncertainty quantification)
latent_sample = model.get_latent_representation(give_mean=False)

# Denoised, batch-corrected expression
norm = model.get_normalized_expression(library_size=1e4)

# Counterfactual: expression as if in different batch
norm_batch1 = model.get_normalized_expression(transform_batch="batch1")
```

---

## Differential Expression

scVI provides Bayesian DE with uncertainty quantification:

```python
# 1-vs-1 comparison
de = model.differential_expression(
    groupby="cell_type",
    group1="T_cells",
    group2="B_cells",
    mode="change",      # Recommended: tests if LFC > delta
    delta=0.25,
    batch_correction=True
)

# 1-vs-all for marker genes
de_all = model.differential_expression(groupby="cell_type", mode="change")

# Filter results
markers = de[(de["lfc_mean"] > 0) & (de["bayes_factor"] > 3)]
```

**Key columns:** `proba_de`, `bayes_factor`, `lfc_mean`, `is_de_fdr_0.05`

---

## Transitioning to scANVI

Always initialize scANVI from trained scVI:

```python
scvi_model = scvi.model.SCVI(adata, n_layers=2, n_latent=30)
scvi_model.train()

scanvi_model = scvi.model.SCANVI.from_scvi_model(
    scvi_model,
    labels_key="cell_type",
    unlabeled_category="Unknown"
)
scanvi_model.train(max_epochs=20)
```

See `scvi-scanvi.md` for full workflows.

---

## Common Issues

| Issue | Solution |
|-------|----------|
| Poor integration | Try `gene_likelihood="nb"`, increase `n_latent` |
| Overclustering | Reduce Leiden resolution, increase `n_latent` |
| OOM errors | Reduce `batch_size`, set `scvi.settings.dl_num_workers=0` |
| Batch key errors | Must be categorical strings |

---

## Resources

- **Docs:** https://docs.scvi-tools.org/en/stable/user_guide/models/scvi.html
- **DE Tutorial:** https://docs.scvi-tools.org/en/stable/tutorials/notebooks/scrna/scVI_DE_worm.html
- **Paper:** https://www.nature.com/articles/s41592-018-0229-2

---

## When not to use

- Do not use on normalized / log-transformed data. scVI needs raw integer counts.
- Do not use for multiome (RNA+ATAC). Use scvi-multivi.
- Do not use for scATAC-seq alone. Use scvi-peakvi.
- Do not use for cross-species integration without careful gene orthology handling.

---

## See also

- `scvi-framework`
- `anndata`
- `single-cell-rna-qc`
- `scvi-scanvi`
- `scvi-scarches-reference-mapping`
- `scanpy`
