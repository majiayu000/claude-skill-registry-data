---
name: harmonypy-batch-integration
description: "harmonypy — multi-sample batch correction on PCA / LSI / spectral embeddings via scanpy.external.harmony_integrate. Use when you have a per-cell embedding and need to remove batch effects before clustering or label transfer. For deep-learning batch correction use scvi-basic; for cross-modality alignment use scglue-unpaired-multiomics-integration."
license: MIT
---

# Harmony Batch Integration (Python)

## Overview

`harmonypy` is the Python port of the Harmony algorithm; it iteratively
re-centres clusters in a chosen embedding so that batch labels become
uninformative. The integration is purely on the embedding — it does NOT
touch `.X` — which means it composes cleanly with both RNA (PCA) and ATAC
(LSI, spectral) preprocessing.

**When to reach for this skill:**
- Multiple samples / donors processed independently, now combined in one
  AnnData / MuData.
- Visible batch structure on a UMAP before integration.
- You want a CPU-only, fast, deterministic correction (vs. scVI which is
  slower and stochastic).

**Pre-reqs:**
- `pip install harmonypy scanpy`
- An embedding already computed (`X_pca`, `X_lsi`, `X_spectral`, ...)
- A batch key on `adata.obs` (e.g. `sample`, `donor`, `batch`)

---

## Part 1 — RNA: Harmony on PCA

```python
import scanpy as sc
import scanpy.external as sce

# Standard RNA preprocessing
sc.pp.normalize_total(rna, target_sum=1e4)
sc.pp.log1p(rna)
sc.pp.highly_variable_genes(rna, n_top_genes=3000)
rna.raw = rna
sc.pp.scale(rna, max_value=10)
sc.pp.pca(rna, n_comps=50)

# Harmony integration
sce.pp.harmony_integrate(
    rna,
    key="sample",                  # batch / donor key
    basis="X_pca",                 # input embedding
    adjusted_basis="X_pca_harmony" # output embedding (NEW slot)
)

# Use the integrated embedding for all downstream steps
sc.pp.neighbors(rna, use_rep="X_pca_harmony")
sc.tl.umap(rna)
sc.tl.leiden(rna)

# Always check integration quality
sc.pl.umap(rna, color=["sample", "leiden"])
```

---

## Part 2 — ATAC: Harmony on spectral / LSI

```python
import snapatac2 as snap
import scanpy.external as sce

# Spectral embedding
snap.pp.select_features(atac, n_features=50000)
snap.pp.spectral(atac, n_comps=50)

# Harmony on the spectral embedding
sce.pp.harmony_integrate(
    atac,
    key="sample",
    basis="X_spectral",
    adjusted_basis="X_spectral_harmony",
)

# Downstream uses the integrated embedding
snap.pp.umap(atac, use_rep="X_spectral_harmony")
snap.pp.knn(atac, use_rep="X_spectral_harmony")
snap.tl.leiden(atac)
```

For LSI-based ATAC, the same pattern applies but with `basis="X_lsi"`.
Remember to drop LSI component 1 first if it correlates with depth (see
`snapatac2-atac-preprocessing`).

---

## Part 3 — Joint RNA+ATAC integration

```python
import muon as mu
import numpy as np

# Method A: simple concatenation of per-modality embeddings
rna = mdata.mod["rna"]
atac = mdata.mod["atac"]

common_cells = list(set(rna.obs_names) & set(atac.obs_names))
rna_sub = rna[common_cells].copy()
atac_sub = atac[common_cells].copy()

joint = np.concatenate([
    rna_sub.obsm["X_pca_harmony"][:, :30],
    atac_sub.obsm["X_spectral_harmony"][:, 1:31],
], axis=1)

rna_sub.obsm["X_joint"] = joint
sc.pp.neighbors(rna_sub, use_rep="X_joint")
sc.tl.umap(rna_sub)

# Method B: muon's WNN implementation operates per-modality and combines
mu.pp.neighbors(mdata, key_added="wnn")
mu.tl.umap(mdata, neighbors_key="wnn")
```

---

## Tuning

| Knob | Effect | Default |
|---|---|---|
| `theta` (passed via `harmony_kwargs`) | Higher = more aggressive batch removal | 2 |
| Number of components in input embedding | More components = more granular structure preserved | 30-50 |
| Clustering resolution after Harmony | Affects whether sub-types collapse together | 0.5 |

---

## Common pitfalls

| Pitfall | Resolution |
|---|---|
| Harmony over-corrects (cell types mixing) | Lower `theta`; verify batch key is correct. |
| Poor batch mixing | Raise number of input PCs/LSI components; raise `theta`. |
| Confused which embedding to use | `adjusted_basis` is the integrated one — pass it to every downstream `neighbors()`. |
| Memory blows up | Pass `max_iter_harmony=10` (lower iterations); ensure embedding is float32. |

---

## API quick reference

```python
sce.pp.harmony_integrate(
    adata,
    key="sample",
    basis="X_pca",
    adjusted_basis="X_pca_harmony",
    max_iter_harmony=10,
    # any other arg goes to harmonypy.run_harmony()
)
```

---

## Resources

- harmonypy: https://github.com/slowkow/harmonypy
- Original Harmony paper: Korsunsky et al., Nature Methods 2019.
- scanpy.external: https://scanpy.readthedocs.io/en/stable/external.html

---

## When not to use

- Do not use if you need a generative model (use scvi-basic / scvi-scanvi).
- Do not use for unpaired cross-modality (use scglue-unpaired-multiomics-integration).

---

## See also

- `scanpy`
- `snapatac2-atac-preprocessing`
- `muon-multimodal-analysis`
- `seurat-multimodal-analysis`
