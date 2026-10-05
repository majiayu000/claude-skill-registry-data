---
name: mofa-mofax
description: "mofax — the Python read-side helper for trained MOFA+ models. Use to load an HDF5 model from mofapy2 or MOFA2 and access expectations (Z, W), variance explained, MEFISTO covariates, metadata, and a small library of factor and weight plots. Read-only; it cannot fit. For fitting use mofa-mofapy2 or mofa-r."
license: MIT
---

# mofax: Python Read-Side Helper for Trained MOFA Models

**Foundation:** all architectural and statistical context lives in `mofa-framework`. Jump to:
- `mofa-framework/references/mofa-architecture.md` — what is stored in the HDF5 (Z, W per view, R², AlphaW, Tau, group/sample metadata)
- `mofa-framework/references/variance-explained.md` — R² is per-factor × view × group, NOT an additive partition of total inertia
- `mofa-framework/references/geometric-caveats.md` — no biplot; Z and W have independent scalings and do not share a metric
- `mofa-framework/references/supplementary-projection-on-z.md` — how to overlay categorical/continuous metadata onto a Z scatter without inventing a co-projection

This file covers only the read-side ergonomics in Python.

---

## When to Use mofax

- You have a trained `model.hdf5` from mofapy2 (Python) or MOFA2 (R) and want to inspect it from Python.
- You need DataFrame accessors over Z, W, R², metadata: `.get_factors(df=True)`, `.get_weights(df=True)`, `.get_r2()`, `.metadata`.
- You want quick seaborn-based factor / weight / variance plots without re-implementing the MOFA2 R plot family.
- You are working with a MEFISTO model and need access to `.covariates`, `.interpolated_factors`, or the smoothness/scale per factor.

mofax cannot fit a model. For that use `mofa-mofapy2` (Python) or `mofa-r` (R).

---

## Installation

```bash
pip install mofax
```

Lightweight — depends only on `h5py`, `numpy`, `pandas`, `seaborn`, `matplotlib`. No GPU, no PyTorch.

---

## Quick Start

```python
import mofax as mfx

model = mfx.mofa_model("trained_mofa.hdf5")   # readonly HDF5 handle
print(model.shape)                            # (n_samples, n_features_total)
print(model.views_names, model.groups_names)

z = model.get_factors(df=True)                # DataFrame: rows = samples, cols = Factor1..K
w_dict = model.get_weights(df=True)           # dict view_name -> DataFrame (features × factors)
r2 = model.get_r2()                           # long DataFrame: Factor, View, Group, R2
meta = model.metadata                         # samples_metadata as DataFrame (may be empty)

mfx.plot_factors(model, x="Factor1", y="Factor2", color="condition")
mfx.plot_weights(model, factor="Factor1", view=model.views_names[0], n_features=20)

model.close()                                 # always close the HDF5 handle
```

---

## Key API Surfaces

The `mofa_model` class wraps the HDF5 file in readonly mode (`core.py:28`, `core.py:211`).

| Property / method | Returns | Notes |
|---|---|---|
| `model.shape` | `(N, D_total)` tuple | Attribute set in `__init__` (`core.py:67-75`); `model.get_shape(group=…, view=…)` (`core.py:216`) for grouped/viewed slices |
| `model.samples_names`, `model.features_names`, `model.views_names`, `model.groups_names` | lists | Names per axis |
| `model.metadata` | DataFrame | Shorthand for `samples_metadata`; getter at `core.py:192`, setter at `core.py:196` |
| `model.features_metadata` | DataFrame | Per-feature metadata when stored |
| `model.covariates_names`, `model.covariates` | list, DataFrame | MEFISTO only |
| `model.get_cells(groups=None)` / `model.get_samples()` / `model.get_features(views=None)` | DataFrame | `core.py:235, 256, 269` |
| `model.get_factors(factors=None, df=False, scale=False)` | ndarray or DataFrame | Z; `core.py:399` |
| `model.get_weights(factors=None, views=None, df=False, scale=False)` | ndarray, dict, or DataFrame | W; one entry per view when `df=True`; `core.py:611` |
| `model.get_r2(factors=None, groups=None, views=None)` | long DataFrame | Variance explained per factor × view × group; `core.py:1167` |
| `model.get_variance_explained(...)` | nested dict | Same info, raw form; `core.py:1104` |
| `model.get_top_features(factor, view, n_features=…)` | DataFrame | `core.py:301` |
| `model.get_interpolated_factors(df_long=True)` | DataFrame | MEFISTO interpolation grid; `core.py:456` |
| `model.get_group_kernel()` | ndarray | MEFISTO group kernel; `core.py:590` |
| `model.project_data(new_data, ...)` | ndarray | Pseudoinverse projection `Z_new = X_new · W⁺`; `core.py:1373`. See `mofa-framework/references/supplementary-projection-on-z.md` for caveats. |
| `model.fetch_values(variables)` | DataFrame | Pull any combination of factors / metadata columns into one frame; `core.py:782` |
| `model.run_umap(...)` | ndarray | UMAP on Z; convenience only — see geometric caveats |
| `model.close()` | None | Release the HDF5 handle |

Plot wrappers (all seaborn-backed, re-exported at the top level via `mofax/plot.py`):

- Z views (`plot_factors.py`): `mfx.plot_factors_scatter` (line 24), `mfx.plot_factors_violin` (line 303), `mfx.plot_factors_umap` (line 472), `mfx.plot_factors_matrix` (line 598), `mfx.plot_factors_dotplot` (line 663), `mfx.plot_factors_correlation` (line 788), `mfx.plot_factors_covariates_correlation` (line 908), `mfx.plot_projection` (line 936). A convenience alias `mfx.plot_factors` is also exposed.
- W views (`plot_weights.py`): `mfx.plot_weights` (line 24), `mfx.plot_weights_ranked` (line 231), `mfx.plot_weights_scaled` (line 354), `mfx.plot_weights_heatmap` (line 441), `mfx.plot_weights_dotplot` (line 560), `mfx.plot_weights_scatter` (line 746), `mfx.plot_weights_correlation` (line 821).
- Data behind a factor (`plot_data.py`): `mfx.plot_data_overview` (line 12).
- R² / variance (`plot_variance.py`): `mfx.plot_r2` (line 24), `mfx.plot_r2_pvalues` (line 137), `mfx.plot_r2_barplot` (line 199).
- MEFISTO (`plot_mefisto.py`): `mfx.plot_interpolated_factors` (line 17), `mfx.plot_group_kernel` (line 220), `mfx.plot_sharedness` (line 300), `mfx.plot_smoothness` (line 345).

Utility:

- `mfx.calculate_r2(Z, W, Y)` (`utils.py:229`) — re-derive R² from raw arrays. Takes the three matrices, not a `mofa_model`.

---

## Common Issues

| Issue | Fix |
|---|---|
| Stale HDF5 cache / "OSError: Unable to open file (file is already open for write)" | Call `model.close()` then re-open; ensure no other process holds the file. |
| `model.metadata` is empty | mofapy2 does not always serialise samples_metadata into the HDF5. Build the DataFrame yourself and assign: `model.metadata = my_df` (`core.py:196`). |
| `get_weights(df=True)` returns a dict, not a DataFrame | Expected. One DataFrame per view (W is per-view). Concatenate with `pd.concat(w_dict, names=["view", "feature"])` if needed. |
| `get_factors(scale=True)` and `get_weights(scale=True)` produce non-commensurable axes | Expected. The two scalings divide independently by `max(|Z|)` and `max(|W|)`. They are cosmetic — do not interpret Z- and W-coordinates as living in the same space. See `mofa-framework/references/geometric-caveats.md`. |
| Sign-flipped factors compared to a previous run | Expected — Bayesian bilinear models are sign-invariant per factor. Impose a canonical sign downstream (e.g. fix the sign of the largest-magnitude loading). |
| `plot_factors(..., color="x")` errors with `KeyError` | The column must exist in `model.metadata` OR be a Factor name. Use `model.fetch_values([...])` to assemble a combined frame first. |
| MEFISTO methods (`covariates`, `interpolated_factors`) return `None` | Model was not trained with MEFISTO covariates. Re-train with `set_covariates(...)` if needed (see `mofa-mofapy2`). |

---

## Resources

- **GitHub:** https://github.com/gtca/mofax
- **PyPI:** https://pypi.org/project/mofax/
- **In-source notebooks:** `notebooks/getting_started_pbmc10k.ipynb`, `notebooks/training_pbmc10k.ipynb`
- **MOFA+ paper:** https://genomebiology.biomedcentral.com/articles/10.1186/s13059-020-02015-1
- **MOFA2 site (training side):** https://biofam.github.io/MOFA2/

---

## When not to use

- Do not use to fit a model. mofax is read-only; use mofa-mofapy2 or mofa-r.
- Do not expect a biplot. mofax mirrors MOFA2's plot family — no co-projection of Z and W on shared axes (see mofa-framework/references/geometric-caveats.md).
- Do not forget to close the HDF5 handle (`model.close()`) at end of session; mofax holds a readonly file handle.

---

## See also

- `mofa-framework`
- `mofa-mofapy2`
- `anndata`
