---
name: scvi-contrastivevi
description: "contrastiveVI from scvi-tools — a contrastive deep generative model that splits scRNA-seq variation into salient (target-specific) and background (shared) latent spaces. Use for Perturb-seq, drug-vs-control, or disease-vs-healthy comparisons where confounding variation masks the effect. Needs a clear target-vs-background split and raw counts."
license: MIT
---

# contrastiveVI: Perturbation Analysis

**Foundation:** inherits shared patterns from `scvi-framework`. Jump to:
- `scvi-framework/references/setup-anndata.md` — plus the target-vs-background split specific to contrastiveVI
- `scvi-framework/references/training-and-gpu.md`
- `scvi-framework/references/common-outputs.md`
- `scvi-framework/references/gotchas.md`, `scvi-framework/checks/pre-train-checklist.md`

This file covers only the parts that differ for contrastiveVI (salient vs background latent).

## When to Use contrastiveVI

- Perturb-seq analysis (isolating CRISPR effects)
- Drug treatment studies
- Disease vs healthy comparisons
- Any target vs background comparison with confounding variation

**Key insight:** Separates **salient** (target-specific) from **background** (shared) variation.

---

## Quick Start

```python
from scvi.external import ContrastiveVI

# Identify target (perturbed) and background (control) cells
adata.obs["is_target"] = adata.obs["condition"] != "control"

# Setup
ContrastiveVI.setup_anndata(
    adata,
    layer="counts",
    batch_key="batch",
)

# Train
model = ContrastiveVI(
    adata,
    n_latent=10,         # Background latent dimensions
    n_salient=10,        # Salient (target-specific) dimensions
)
model.train()
```

---

## Dual Latent Spaces

| Space | Access | Contains |
|-------|--------|----------|
| Background (`z`) | `get_latent_representation(give_z=True)` | Shared variation (cell cycle, baseline) |
| Salient (`s`) | `get_latent_representation(give_z=False)` | Target-specific variation (perturbation effect) |

```python
# For visualization: use salient space for target cells
target_idx = adata.obs["is_target"]
adata.obsm["X_salient"] = model.get_latent_representation(give_z=False)
adata.obsm["X_background"] = model.get_latent_representation(give_z=True)

# UMAP on salient shows perturbation effects
sc.pp.neighbors(adata[target_idx], use_rep="X_salient")
sc.tl.umap(adata[target_idx])
```

---

## Key Model Parameters

```python
model = ContrastiveVI(
    adata,
    n_hidden=128,
    n_latent=10,            # Background dimensions (shared variation)
    n_salient=10,           # Salient dimensions (target-specific)
    n_layers=2,
    wasserstein_penalty=0,  # >0 encourages orthogonal spaces
)

model.train(
    max_epochs=400,
    early_stopping=True,
    batch_size=128,
    # Specify which cells are target vs background
    indices_to_study=target_idx,  # Target cell indices
)
```

---

## Differential Expression

Get perturbation-specific DE:

```python
# DE focused on salient (perturbation) effects
de = model.differential_expression(
    groupby="perturbation",
    group1="gene_knockout",
    group2="control",
    mode="change",
)
```

---

## Typical Workflow

```python
from scvi.external import ContrastiveVI

# 1. Prep data
adata.layers["counts"] = adata.X.copy()
target_mask = adata.obs["condition"] == "treated"

# 2. Setup
ContrastiveVI.setup_anndata(adata, layer="counts", batch_key="batch")

# 3. Train
model = ContrastiveVI(adata, n_latent=10, n_salient=10)
model.train()

# 4. Extract representations
adata.obsm["X_bg"] = model.get_latent_representation(give_z=True)
adata.obsm["X_salient"] = model.get_latent_representation(give_z=False)

# 5. Visualize perturbation effects (salient space, target cells only)
target_adata = adata[target_mask]
sc.pp.neighbors(target_adata, use_rep="X_salient")
sc.tl.umap(target_adata)
sc.pl.umap(target_adata, color=["perturbation"])
```

---

## Critical Gotchas

| Issue | Solution |
|-------|----------|
| Salient space empty | Increase `n_salient`; check target/background distinction |
| Background dominates | Use `wasserstein_penalty > 0` to separate spaces |
| Poor separation | Ensure sufficient target/background cells |
| Wrong target cells | Verify `is_target` or indices correctly identify perturbed cells |

---

## Resources

- **Docs:** https://docs.scvi-tools.org/en/stable/user_guide/models/contrastive_vi.html
- **Tutorial:** https://docs.scvi-tools.org/en/stable/tutorials/notebooks/scrna/contrastiveVI.html
- **Paper:** https://www.nature.com/articles/s41592-023-01955-3

---

## When not to use

- Do not use on normalized / log-transformed data. Raw counts required.
- Do not use without a target / background split. contrastiveVI needs both groups.
- Do not use for unconfounded case-control (where scVI / scANVI already suffice).

---

## See also

- `scvi-framework`
- `scvi-basic`
- `scvi-mrvi`
- `anndata`
- `scanpy`

Upstream docs: https://docs.scvi-tools.org/en/stable/user_guide/models/contrastivevi.html
