---
name: anndata
description: AnnData — foundation for the scverse ecosystem. Use for format operations (.h5ad read/write, subsetting, concatenating), data-slot structure, and shape/index debugging. For analysis workflows use scanpy; for probabilistic models use scvi-framework (scvi-tools); for population-scale queries use cellxgene-census-annotation.
license: MIT
---

# AnnData: The scverse Data Container

## Overview

AnnData is the shared data container for the scverse ecosystem (scanpy, scvi-tools, scvelo, cellrank, squidpy, muon). Understanding its structure is prerequisite knowledge for all single-cell Python work. Every tool in this skill library reads and writes AnnData objects.

**When to use this skill:**
- Reading / writing `.h5ad` files, 10X MTX, loom, zarr
- Subsetting, filtering, or concatenating datasets
- Debugging index alignment errors, shape mismatches
- Memory-efficient access to large files (backed mode)
- Understanding where a tool stored its output (which slot)
- Converting between sparse/dense, strings/categoricals

**When NOT to use this skill alone:**
- For full scRNA-seq analysis → `scanpy.md`
- For deep learning models → `scvi-framework.md`
- For R↔Python format conversion → `anndatar-seurat-scanpy-conversion.md`
- For multi-assay containers (RNA + protein/ATAC) → `multimodal-anndata-mudata.md`

---

## AnnData Structure

```
AnnData object:  n_obs × n_vars  (cells × genes)
│
├─ .X              — expression matrix (n_obs × n_vars); sparse or dense
├─ .obs            — cell metadata DataFrame (n_obs rows); cluster, sample, QC metrics
├─ .var            — gene metadata DataFrame (n_vars rows); highly_variable, mean, std
├─ .uns            — unstructured dict; neighbors graph params, color palettes, DE results
│
├─ .obsm            — multi-dim cell arrays; 'X_pca', 'X_umap', 'X_scVI' (n_obs × k)
├─ .varm            — multi-dim gene arrays; 'PCs' loadings (n_vars × k)
├─ .obsp            — pairwise cell matrices; 'connectivities', 'distances' (n_obs × n_obs)
│
├─ .layers          — alternative expression matrices (same shape as X); 'counts', 'spliced'
│                     Use layers to store raw counts after normalization
└─ .raw             — snapshot of (X, var) before filtering; accessed with adata.raw.X
```

**Mental model**: Think of `.obs` as your cell-level metadata spreadsheet, `.var` as your gene metadata spreadsheet, `.X` as the expression matrix that links them, and everything else as additional matrices that hang off cells (`.obsm`) or genes (`.varm`) or pairs-of-cells (`.obsp`).

**var_names convention:** During build, keep Ensembl IDs as var_names (no duplicates, stable
for gene-set tools). At the deliverable milestone, switch to gene symbols — preserve Ensembl in
var['gene_id'] for a one-line switch-back:

```python
adata.var["gene_id"] = adata.var_names.copy()    # preserve before switch
adata.var_names = adata.var["gene_name"].values   # symbols become active
adata.var_names_make_unique(join="-")             # Symbol-1 for any duplicate
# Switch back any time: adata.var_names = adata.var['gene_id']
```

See `scrna-pipeline-conventions/references/gene-identifier-packaging.md` for the
milestone contract and verification.

### Where tools store their outputs

| Tool | Output | Location |
|------|--------|----------|
| `sc.tl.pca()` | PCA coordinates | `adata.obsm['X_pca']` |
| `sc.tl.umap()` | UMAP coordinates | `adata.obsm['X_umap']` |
| multiple UMAP sources (unsupervised + integration) | `X_umap_unsupervised`, `X_umap_integrated` | `adata.obsm` |
| `scvi_model.get_latent_representation()` | scVI embedding | `adata.obsm['X_scVI']` |
| `sc.pp.neighbors()` | kNN graph | `adata.obsp['connectivities']`, `adata.uns['neighbors']` |
| `sc.tl.leiden()` | Cluster labels | `adata.obs['leiden']` |
| `sc.tl.rank_genes_groups()` | DE results | `adata.uns['rank_genes_groups']` |
| `sc.tl.score_genes()` | Cell scores | `adata.obs['<score_name>']` |
| `scv.tl.velocity()` | Velocity vectors | `adata.layers['velocity']` |
| `scv.tl.latent_time()` | Pseudotime | `adata.obs['latent_time']` |

**Multiple UMAPs tip:** If the pipeline produces both an unsupervised UMAP (PCA-based) and an
integrated UMAP (scANVI/Harmony-based), do not overwrite the single `X_umap` key — rename both
with a purpose suffix at packaging so collaborators select the right one by name. Document each
in `uns['embeddings']`. See
`scrna-pipeline-conventions/references/embedding-deliverables.md`.

---

## Installation

```bash
pip install anndata        # Core package
# Usually installed as a dependency of scanpy or scvi-tools
```

---

## Reading and Writing

```python
import anndata as ad

# Read h5ad (standard format)
adata = ad.read_h5ad('data.h5ad')

# Read with backed mode (large files — X stays on disk)
adata = ad.read_h5ad('large_data.h5ad', backed='r')
# Must call .to_memory() before operations that need X in RAM

# Read 10X formats
adata = sc.read_10x_mtx('path/to/10x_output/')  # via scanpy
adata = ad.read_10x_h5('filtered_feature_bc_matrix.h5')

# Write
adata.write_h5ad('output.h5ad')
adata.write_h5ad('output.h5ad', compression='gzip')  # Smaller file, slower write

# Write zarr (cloud-friendly, chunked)
adata.write_zarr('output.zarr')
```

---

## Subsetting

```python
# Boolean mask on obs (cells)
t_cells = adata[adata.obs['cell_type'] == 'T cell']

# Multiple conditions
filtered = adata[
    (adata.obs['n_genes'] > 200) &
    (adata.obs['pct_mt'] < 20)
]

# By var (genes)
hvg_only = adata[:, adata.var['highly_variable']]

# By name
genes_of_interest = adata[:, ['CD14', 'CD3D', 'MS4A1']]

# Combined
subset = adata[
    adata.obs['leiden'] == '3',
    adata.var['highly_variable']
]
```

**CRITICAL: View vs Copy**

```python
# Subsetting creates a VIEW — modifying it may modify the original
view = adata[adata.obs['cell_type'] == 'T cell']

# Make a copy to get an independent object
copy = adata[adata.obs['cell_type'] == 'T cell'].copy()

# Rule of thumb: always .copy() if you're going to modify the subset
# Otherwise you'll see "ImplicitlyConvertedView" warnings
```

---

## Concatenation

```python
import anndata as ad

# Concatenate along cells (add more cells — common for batch integration)
adata = ad.concat(
    [adata1, adata2, adata3],
    axis=0,
    join='inner',           # 'inner' = shared genes only; 'outer' = all genes, fill NaN
    label='batch',          # Adds a 'batch' column to obs
    keys=['batch1', 'batch2', 'batch3']
)
print(adata)  # Check shape

# Concatenate along genes (rare; add modalities)
combined = ad.concat([adata_rna, adata_protein], axis=1)
```

**Common issue:** After concatenation, `obs_names` may have duplicates.
```python
# Check
print(adata.obs_names.is_unique)  # Should be True

# Fix if needed
adata.obs_names_make_unique()
```

---

## Working with Layers

Layers store alternative expression matrices (same shape as X). Use them to preserve raw counts alongside normalized data.

```python
# Store raw counts before normalization
adata.layers['counts'] = adata.X.copy()

# Normalize
sc.pp.normalize_total(adata, target_sum=1e4)
sc.pp.log1p(adata)
# Now adata.X is log-normalized, adata.layers['counts'] is raw

# scVI needs raw counts:
scvi.model.SCVI.setup_anndata(adata, layer='counts')

# scvelo needs spliced/unspliced:
adata.layers['spliced']   # from velocyto or STARsolo
adata.layers['unspliced'] # from velocyto or STARsolo
```

---

## Raw Slot

```python
# Save a snapshot of X before HVG filtering (for gene expression plots)
adata.raw = adata  # Freezes current X and var

# Later: plot gene expression using raw (even for genes filtered out by HVG)
sc.pl.umap(adata, color='SOME_GENE', use_raw=True)

# Access raw data directly
raw_X = adata.raw.X      # Expression matrix (n_obs × all genes)
raw_var = adata.raw.var  # All genes (not just HVGs)

# Restore raw to X (if you need to go back to full gene set)
adata = adata.raw.to_adata()
```

---

## Memory Efficiency

```python
# Backed mode: X stays on disk, obs/var in RAM
adata = ad.read_h5ad('50GB_atlas.h5ad', backed='r')

# Filter on metadata without loading X
filtered = adata[adata.obs['tissue'] == 'lung']

# Load only the filtered subset into memory
adata_lung = filtered.to_memory()

# Process in chunks (for very large files)
chunk_size = 5000
for i in range(0, adata.n_obs, chunk_size):
    chunk = adata[i:i+chunk_size].to_memory()
    # process chunk

# Use sparse matrices (most expression matrices are >95% zeros)
from scipy.sparse import csr_matrix, issparse
if not issparse(adata.X):
    adata.X = csr_matrix(adata.X)

# Convert string columns to categorical (saves memory, speeds up groupby)
adata.strings_to_categoricals()
```

---

## Common Gotchas

### Index alignment when adding external data

```python
# WRONG — index positions may not match
adata.obs['new_col'] = external_series.values

# RIGHT — align on index
adata.obs['new_col'] = external_df.loc[adata.obs_names, 'value']
```

### obs_names must be unique

```python
# Check
assert adata.obs_names.is_unique, "Cell barcodes are not unique!"

# Fix
adata.obs_names_make_unique()
```

### Modifying X after subsetting

```python
# This may raise a warning about modifying a view
subset = adata[adata.obs['batch'] == '1']
subset.X = ...  # Warning!

# Fix: make a copy first
subset = adata[adata.obs['batch'] == '1'].copy()
subset.X = ...  # No warning
```

### var_names must match between datasets for scVI / scArches

```python
# Check before concat or scArches mapping
assert set(query.var_names) == set(ref.var_names), "Gene sets don't match"
# Or: subset to intersection
common_genes = query.var_names.intersection(ref.var_names)
query = query[:, common_genes].copy()
ref = ref[:, common_genes].copy()
```

---

## Inspecting an Unknown AnnData Object

```python
# Start here when handed an unfamiliar .h5ad
print(adata)                          # Shape, layers, obsm keys
print(adata.obs.columns.tolist())     # What cell metadata exists
print(adata.var.columns.tolist())     # What gene metadata exists
print(list(adata.obsm.keys()))        # What embeddings exist
print(list(adata.layers.keys()))      # What count matrices exist
print(adata.obs.dtypes)               # Check for unexpected types
print(adata.obs['cell_type'].value_counts())  # Check category distributions
print(adata.X.min(), adata.X.max())   # Normalized or raw? (raw: integers, norm: floats)
```

---

## Integration Map: Which Skill Uses Which Slots

| Skill | Reads | Writes |
|-------|-------|--------|
| `scanpy.md` | `.X` (normalized), `.raw` | `.obs` (leiden, scores), `.obsm` (X_pca, X_umap), `.uns` (neighbors, DE) |
| `scvi-basic.md` | `.layers['counts']` (raw) | `.obsm['X_scVI']` |
| `scvi-scanvi.md` | `.obsm['X_scVI']`, `.obs['cell_type']` | `.obs['scanvi_pred', 'scanvi_prob']` |
| `rna-velocity-trajectory.md` | `.layers['spliced', 'unspliced']`, `.obsm['X_umap']` | `.layers['velocity']`, `.obs['latent_time']`, `.obsm['velocity_umap']` |
| `multimodal-anndata-mudata.md` | Multiple AnnData | `MuData` container |

---

## Resources

- Documentation: https://anndata.readthedocs.io/
- GitHub: https://github.com/scverse/anndata
- scverse ecosystem: https://scverse.org/

---

## When not to use

- Do not use alone for full scRNA-seq analysis. Pair with scanpy.
- Do not use for multi-assay containers (CITE-seq, multiome). Use multimodal-anndata-mudata.

---

## See also

- `scanpy`
- `anndatar-seurat-scanpy-conversion`
- `scvi-framework`
