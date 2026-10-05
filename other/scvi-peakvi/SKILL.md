---
name: scvi-peakvi
description: "PeakVI is a deep generative model in scvi-tools for scATAC-seq, producing batch-corrected latent embeddings and region-level differential accessibility. Use for standard scATAC clustering, batch correction across experiments, and scaling past a million cells. For paired RNA+ATAC use scvi-multivi; for TF activity use chromvar-motif-accessibility."
license: MIT
---

# PeakVI: scATAC-seq Analysis

**Foundation:** inherits shared patterns from `scvi-framework`. Jump to:
- `scvi-framework/references/setup-anndata.md` — peaks-by-cells registration (no HVG step)
- `scvi-framework/references/count-distributions.md` — Bernoulli vs Poisson for ATAC
- `scvi-framework/references/training-and-gpu.md`
- `scvi-framework/references/interop-matrix.md` — PeakVI ↔ MultiVI
- `scvi-framework/references/gotchas.md`, `scvi-framework/checks/pre-train-checklist.md`

This file covers only the parts that differ for PeakVI (scATAC-only).

## When to Use PeakVI

- **Standard scATAC-seq clustering** and embedding
- **Differential accessibility** between cell populations
- **Batch correction** across scATAC experiments
- Scalable analysis for >1M cells

**Limitations:** Requires GPU for speed; latent space not directly interpretable; binary/count data only (not fragment-level).

**Decision Guide:**
| Scenario | Recommendation |
|----------|----------------|
| Standard scATAC clustering/DA | **PeakVI** |
| Quantitative fragment analysis | PoissonVI |
| RNA+ATAC integration | MultiVI (`scvi-multivi.md`) |
| Regulatory inference | scGLUE (`scglue-unpaired-multiomics-integration.md`) |

---

## Quick Start

```python
import scvi
import scanpy as sc

scvi.settings.seed = 42

# Load scATAC data (peaks x cells matrix)
adata = sc.read_h5ad("scatac_data.h5ad")

# Filter peaks and cells
sc.pp.filter_cells(adata, min_genes=500)
sc.pp.filter_genes(adata, min_cells=int(adata.n_obs * 0.01))

# Setup and train
scvi.model.PEAKVI.setup_anndata(adata, batch_key="batch")
model = scvi.model.PEAKVI(adata)
model.train()

# Extract latent and visualize
adata.obsm["X_peakvi"] = model.get_latent_representation()
sc.pp.neighbors(adata, use_rep="X_peakvi")
sc.tl.umap(adata, min_dist=0.2)
sc.tl.leiden(adata, key_added="clusters", resolution=0.3)
```

---

## Input Requirements

```python
# AnnData structure
adata.X           # (n_cells, n_peaks) - binary or counts, sparse CSR recommended
adata.var         # Peak annotations (chr, start, end)
adata.obs         # Cell metadata (batch_key for batch correction)
```

**Preprocessing:**
```python
import scipy.sparse

# Ensure sparse format
if not scipy.sparse.issparse(adata.X):
    adata.X = scipy.sparse.csr_matrix(adata.X)
```

---

## Model Parameters

```python
model = scvi.model.PEAKVI(
    adata,
    n_latent=10,           # Latent dimensions (auto by default)
    n_hidden=128,          # Hidden layer size
    n_layers=2,            # Hidden layers
    dropout_rate=0.1,
)

model.train(
    max_epochs=500,
    early_stopping=True,
    early_stopping_patience=50,
    batch_size=128,
    use_gpu=True
)
```

---

## Outputs

```python
# Latent representation
adata.obsm["X_peakvi"] = model.get_latent_representation()

# Accessibility probabilities
accessibility = model.get_normalized_accessibility()

# Counterfactual (accessibility in different batch)
accessibility_batch2 = model.get_normalized_accessibility(transform_batch="batch2")
```

---

## Differential Accessibility

```python
# One cluster vs all others
da_results = model.differential_accessibility(
    groupby="clusters",
    group1="3"
)

# Two-group comparison
da_results = model.differential_accessibility(
    groupby="clusters",
    group1="3",
    group2="0",
    test_mode="two"
)

# Multi-batch data (important!)
da_results = model.differential_accessibility(
    groupby="cell_type",
    group1="TypeA",
    group2="TypeB",
    batch_correction=True
)
```

**Key columns:**
| Column | Description |
|--------|-------------|
| `prob_da` | Probability of differential accessibility (0-1) |
| `is_da_fdr` | FDR-corrected binary call |
| `bayes_factor` | BF > 3 = strong evidence |
| `effect_size` | `est_prob2 - est_prob1` |

**Filtering:**
```python
sig_peaks = da_results[
    (da_results.prob_da > 0.9) &
    (da_results.bayes_factor > 3) &
    (abs(da_results.effect_size) > 0.1)
]
```

---

## Transfer Learning

```python
# Train on reference
scvi.model.PEAKVI.setup_anndata(reference_adata)
ref_model = scvi.model.PEAKVI(reference_adata)
ref_model.train()
ref_model.save("reference_model/")

# Map query (must have same peaks)
scvi.model.PEAKVI.setup_anndata(query_adata)
query_model = scvi.model.PEAKVI.load_query_data(query_adata, "reference_model/")
query_model.train(max_epochs=100)
query_adata.obsm["X_peakvi"] = query_model.get_latent_representation()
```

---

## Integration with ArchR/Signac

### From ArchR
```python
# After exporting from ArchR to AnnData
adata = ad.read_h5ad("archr_export.h5ad")
scvi.model.PEAKVI.setup_anndata(adata, batch_key="Sample")
```

### From Signac
```r
# In R: Export Seurat/Signac
library(SeuratDisk)
SaveH5Seurat(seurat_obj, filename = "signac_data.h5Seurat")
Convert("signac_data.h5Seurat", dest = "h5ad")
```

```python
# In Python: Load
adata = sc.read_h5ad("signac_data.h5ad")
```

---

## Common Issues

| Issue | Solution |
|-------|----------|
| Out of memory | Reduce `batch_size=64`, subsample for exploration |
| Slow training | Check `torch.cuda.is_available()`, use GPU |
| Poor clustering | Try `n_latent=20`, adjust Leiden resolution |
| Too many peaks | Filter to highly variable: `sc.pp.highly_variable_genes(adata, n_top_genes=50000)` |

---

## PeakVI vs Alternatives

| Feature | PeakVI | PoissonVI | LSI |
|---------|--------|-----------|-----|
| Data type | Binary/counts | Fragment counts | Binary/TF-IDF |
| Batch correction | Built-in | Built-in | Harmony post-hoc |
| DA analysis | Built-in | Better quantification | External tools |
| Interpretability | Low | Low | High (linear) |
| GPU requirement | Recommended | Recommended | Not needed |

---

## Resources

- **Docs:** https://docs.scvi-tools.org/en/stable/user_guide/models/peakvi.html
- **Tutorial:** https://docs.scvi-tools.org/en/stable/tutorials/notebooks/atac/PeakVI.html
- **Paper:** Ashuach et al. (2021), *PeakVI: A Deep Generative Model For Single Cell Chromatin Accessibility Analysis*

---

## When not to use

- Do not use for paired multiome (RNA+ATAC) integration. Use scvi-multivi instead.
- Do not use for TF motif deviation scoring. Use chromvar-motif-accessibility.

---

## See also

- `scvi-framework`
- `scvi-multivi`
- `chromvar-motif-accessibility`
- `iterative-peak-merging`
- `pycistopic-atac-topic-modeling` — for topic-model-based cCRE/regulon discovery as an alternative accessibility model when you want interpretable topics rather than a VAE latent space
