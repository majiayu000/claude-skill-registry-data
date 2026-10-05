---
name: scanpy
description: "Standard scanpy scRNA-seq pipeline: normalization, HVG selection, PCA/UMAP/t-SNE, Leiden clustering, rank_genes_groups markers, score_genes, and scverse plots. Use for exploratory analysis once cells are QC'd — its own QC is fixed-threshold only, so for MAD-based QC or doublet detection use single-cell-rna-qc; for batch correction use scvi-basic."
license: MIT
---

# Scanpy: Standard scRNA-seq Analysis

## Overview

Scanpy is the standard Python toolkit for single-cell RNA-seq analysis, built on AnnData. It covers the complete standard workflow: quality control → normalization → feature selection → dimensionality reduction → clustering → marker identification → visualization. All outputs are stored back in the AnnData object, making it interoperable with the entire scverse ecosystem.

**When to use scanpy:**
- Standard scRNA-seq workflows (QC through annotation)
- UMAP, t-SNE, or PCA visualization
- Clustering (Leiden / Louvain) and marker gene identification
- Condition-vs-condition DE with `rank_genes_groups`
- Gene set scoring (`sc.tl.score_genes`)
- Publication-quality plots (dotplot, heatmap, violin, UMAP)

**When NOT to use scanpy:**
- Multi-sample probabilistic batch correction → use `scvi-basic.md` (scVI)
- Semi-supervised annotation transfer → use `scvi-scanvi.md` (scANVI)
- Joint RNA + ATAC modeling → use `scvi-multivi.md`
- RNA velocity / trajectory direction → use `rna-velocity-trajectory.md`
- Multi-assay containers (CITE-seq, multiome) → use `multimodal-anndata-mudata.md`
- AnnData format operations alone → use `anndata.md`

---

## Tool Decision: Scanpy vs scvi-tools vs Seurat

```
New scRNA-seq dataset?
│
├─ Standard workflow, single modality, publication plots?
│   └─ scanpy (this skill)
│
├─ Need probabilistic batch correction or DE?
│   └─ scvi-basic → then scanpy for downstream clustering/viz
│
├─ Need annotation transfer from reference?
│   └─ scvi-scanvi → scanpy for visualization
│
├─ In R, working with Seurat objects?
│   └─ seurat-multimodal-analysis.md
│
└─ All of the above + deep learning?
    └─ scvi-framework.md as foundation, scanpy for downstream
```

After scVI/scANVI, you almost always use scanpy for `neighbors → umap → leiden → rank_genes_groups`. The two tools are complementary, not alternatives.

---

## Quick Start

```python
import scanpy as sc
import numpy as np

# Settings
sc.settings.verbosity = 2
sc.settings.set_figure_params(dpi=80, facecolor='white')

# Load data
adata = sc.read_h5ad('data.h5ad')
# or: adata = sc.read_10x_mtx('path/to/10x/')
# or: adata = sc.read_10x_h5('data.h5')
print(adata)  # Always check shape first
```

---

## Standard Workflow

### 1. Quality Control

```python
# Flag mitochondrial genes (human: "MT-", mouse: "mt-")
adata.var['mt'] = adata.var_names.str.startswith('MT-')

# Calculate QC metrics
sc.pp.calculate_qc_metrics(
    adata,
    qc_vars=['mt'],
    percent_top=None,
    log1p=False,
    inplace=True
)
# Adds to adata.obs: n_genes_by_counts, total_counts, pct_counts_mt

# Visualize before filtering
sc.pl.violin(
    adata,
    ['n_genes_by_counts', 'total_counts', 'pct_counts_mt'],
    jitter=0.4, multi_panel=True
)
sc.pl.scatter(adata, x='total_counts', y='n_genes_by_counts', color='pct_counts_mt')
```

**Setting thresholds:**
- Fixed thresholds (e.g., `pct_counts_mt < 20`) are common but dataset-dependent
- **MAD-based thresholds** are more principled (see `single-cell-rna-qc.md`):
  ```python
  import numpy as np
  median = np.median(adata.obs['n_genes_by_counts'])
  mad = np.median(np.abs(adata.obs['n_genes_by_counts'] - median))
  lower = median - 3 * mad
  upper = median + 3 * mad
  ```
- Typical starting points: `min_genes=200`, `pct_counts_mt < 20`, inspect scatter plot for doublets (upper-right outliers)

```python
# Filter
n_before = adata.n_obs
sc.pp.filter_cells(adata, min_genes=200)
sc.pp.filter_genes(adata, min_cells=3)
adata = adata[adata.obs.pct_counts_mt < 20]
print(f"Filtered: {n_before} → {adata.n_obs} cells")
```

### 2. Normalization and Preprocessing

```python
# Save raw counts before any normalization
adata.raw = adata  # Preserves X as-is; used later for gene expression plots

# Normalize to median total counts (or 1e4)
sc.pp.normalize_total(adata, target_sum=1e4)

# Log-transform: log(x + 1)
sc.pp.log1p(adata)

# Identify highly variable genes
sc.pp.highly_variable_genes(
    adata,
    min_mean=0.0125, max_mean=3,
    min_disp=0.5,
    # Or: n_top_genes=2000
    # Or: flavor='seurat_v3' for count-based HVG
)
sc.pl.highly_variable_genes(adata)
print(f"HVGs: {adata.var.highly_variable.sum()}")

# Subset to HVGs for PCA (keep all genes in adata for later)
adata_hvg = adata[:, adata.var.highly_variable].copy()

# Optionally: scale to unit variance and zero mean
sc.pp.scale(adata_hvg, max_value=10)
```

**Note:** If integrating with scVI after this, scVI needs raw counts. Don't normalize before passing to scVI.

### 3. Dimensionality Reduction

```python
# PCA
sc.tl.pca(adata_hvg, svd_solver='arpack', n_comps=50)
sc.pl.pca_variance_ratio(adata_hvg, log=True, n_pcs=50)  # Look for elbow

# Neighborhood graph (needed for UMAP and Leiden)
# Use n_pcs from elbow (typically 20-40)
sc.pp.neighbors(adata_hvg, n_neighbors=15, n_pcs=30)

# UMAP
sc.tl.umap(adata_hvg)
sc.pl.umap(adata_hvg, color='sample')  # Quick check for batch effects
```

**If you used scVI for batch correction:**
```python
# Use scVI latent representation instead of PCA
sc.pp.neighbors(adata, use_rep='X_scVI', n_neighbors=15)
sc.tl.umap(adata)
# Do NOT run sc.tl.pca before this
```

### 4. Clustering

```python
# Leiden (recommended over Louvain — faster, better quality)
# Resolution controls granularity: higher = more clusters
sc.tl.leiden(adata_hvg, resolution=0.5)

# Explore multiple resolutions
for res in [0.3, 0.5, 0.8, 1.0, 1.5]:
    sc.tl.leiden(adata_hvg, resolution=res, key_added=f'leiden_{res}')

sc.pl.umap(adata_hvg,
           color=['leiden_0.3', 'leiden_0.5', 'leiden_0.8', 'leiden_1.0'],
           ncols=2)
```

### 5. Marker Gene Identification

```python
# Find markers for each cluster (all vs rest)
sc.tl.rank_genes_groups(
    adata_hvg,
    groupby='leiden',
    method='wilcoxon',  # Wilcoxon is more robust than t-test for single-cell
    use_raw=True        # Use raw counts for DE
)

# Visualize
sc.pl.rank_genes_groups(adata_hvg, n_genes=15, sharey=False)
sc.pl.rank_genes_groups_dotplot(adata_hvg, n_genes=5)

# Get results as DataFrame
import pandas as pd
markers_df = sc.get.rank_genes_groups_df(adata_hvg, group='0')
print(markers_df.head(10))
```

**Condition vs condition DE within a cell type:**
```python
subset = adata[adata.obs['cell_type'] == 'DC']
sc.tl.rank_genes_groups(
    subset,
    groupby='condition',
    groups=['treated'],
    reference='control',
    method='wilcoxon'
)
```

### 6. Visualization

```python
# Gene expression on UMAP (use raw counts)
marker_genes = ['CD14', 'CD3D', 'MS4A1', 'FCGR3A']
sc.pl.umap(adata_hvg, color=marker_genes, use_raw=True, ncols=2)

# Dotplot (canonical for cell type marker confirmation)
sc.pl.dotplot(
    adata_hvg,
    var_names=marker_genes,
    groupby='leiden',
    use_raw=True
)

# Heatmap
sc.pl.heatmap(
    adata_hvg,
    var_names=marker_genes,
    groupby='leiden',
    swap_axes=True,
    show_gene_labels=True
)

# Stacked violin
sc.pl.stacked_violin(adata_hvg, var_names=marker_genes, groupby='leiden')
```

**Publication-quality settings:**
```python
sc.settings.set_figure_params(dpi=300, frameon=False, figsize=(6, 6))
sc.settings.file_format_figs = 'pdf'

sc.pl.umap(
    adata_hvg,
    color='cell_type',
    legend_loc='on data',
    legend_fontsize=10,
    legend_fontoutline=2,
    frameon=False,
    save='_cell_types.pdf'  # Saves to sc.settings.figdir
)
```

### 7. Gene Set Scoring

```python
# Score cells for a gene program
gene_program = ['FCGR1A', 'CD68', 'CSF1R', 'ITGAM']
sc.tl.score_genes(adata_hvg, gene_list=gene_program, score_name='myeloid_score')
sc.pl.umap(adata_hvg, color='myeloid_score', cmap='RdYlBu_r')

# Compare to scVI's built-in DE which is more principled for multi-sample data
# → see scvi-basic.md for differential_expression()
```

---

## Key Parameters Reference

| Step | Parameter | Typical Range | Effect |
|------|-----------|---------------|--------|
| QC | `min_genes` | 200–500 | Removes low-complexity cells |
| QC | `pct_counts_mt` | 5–25% | Dataset-dependent |
| HVG | `n_top_genes` | 1500–4000 | More = slower, more sensitive |
| PCA | `n_comps` | 30–50 | Check variance ratio elbow |
| Neighbors | `n_neighbors` | 10–30 | More = smoother UMAP |
| Neighbors | `n_pcs` | 15–40 | From elbow plot |
| UMAP | `min_dist` | 0.1–0.5 | Tighter vs spread |
| Leiden | `resolution` | 0.3–1.5 | Higher = more clusters |

---

## Common Pitfalls

1. **Using normalized data with scVI**: scVI requires raw integer counts. If you've run `normalize_total` + `log1p`, you need to access `adata.layers['counts']` or `adata.raw`.
2. **Forgetting `adata.raw = adata`**: Gene expression plots with `use_raw=True` fail if you didn't save raw before HVG filtering.
3. **Plotting filtered-out genes**: After HVG subset, genes not in `adata.var_names` cause errors. Use `adata.raw` or go back to the full object.
4. **Cluster-level annotation pitfall**: Assigning one label per Leiden cluster (e.g., via max-scoring marker) fails when clusters are heterogeneous. Consider cell-level scoring. See project's `04_annotate_v3.py` for an example of cell-level annotation with scANVI + marker rescue.
5. **Louvain vs Leiden**: Leiden is preferred; Louvain has convergence issues.
6. **Wilcoxon vs t-test for DE**: Wilcoxon is non-parametric and more robust for single-cell. Use `method='wilcoxon'`.

---

## Integration with Other Skills

- **Before scanpy** (if multi-sample): `scvi-basic.md` for batch correction → use `X_scVI` for neighbors
- **Annotation transfer**: `scvi-scanvi.md` — use scANVI predictions, then scanpy for visualization
- **Trajectory**: After clustering, use `rna-velocity-trajectory.md` for directional dynamics
- **AnnData operations** (format, I/O, subsetting): `anndata.md`
- **R↔Python conversion**: `anndatar-seurat-scanpy-conversion.md`
- **QC details** (MAD-based filtering): `single-cell-rna-qc.md`

---

## Resources

- Documentation: https://scanpy.readthedocs.io/
- Best practices: Luecken & Theis (2019) "Current best practices in scRNA-seq analysis"
- scverse ecosystem: https://scverse.org/
- Tutorial: https://scanpy.readthedocs.io/en/stable/tutorials/

---

## When not to use

- Do not use for dedicated quality control. For MAD-based outlier detection and doublet-aware filtering, use single-cell-rna-qc.
- Do not use for multi-sample probabilistic batch correction. Use scvi-basic.
- Do not use for semi-supervised label transfer. Use scvi-scanvi.
- Do not use for multi-assay containers. Use multimodal-anndata-mudata.
- Do not use for pathway or TF interpretation of pseudobulk differential expression. Use bulk-rnaseq-gsea or bulk-rnaseq-activity-inference.

---

## See also

- `anndata`
- `single-cell-rna-qc`
- `scvi-basic`
- `rna-velocity-trajectory`
