---
name: mofa-mofapy2
description: "mofapy2 — the Python core engine for Multi-Omics Factor Analysis (MOFA+). Use to fit a MOFA model from Python on multi-view data (gaussian/bernoulli/poisson per view), with optional spike-and-slab sparsity, SVI minibatching, and GPU acceleration. Emits HDF5 readable by mofax or MOFA2. For R-side fitting use mofa-r."
license: MIT
---

# mofapy2: Python Core Engine for MOFA+

**Foundation:** `mofa-framework` is the router and holds all shared MOFA patterns. Jump directly to:
- `mofa-framework/references/mofa-architecture.md` — Markov blanket (Y/Z/W/Tau), ARD pruning, ELBO trace
- `mofa-framework/references/view-likelihoods.md` — when to use gaussian / bernoulli / poisson per view
- `mofa-framework/references/variance-explained.md` — per-factor R² is not an inertia partition
- `mofa-framework/references/geometric-caveats.md` — no biplot, sign / order indeterminacy, no shared Σ
- `mofa-framework/checks/pre-fit-checklist.md` — pre-flight before `build()` / `run()`

This file covers only the parts that differ for mofapy2 (the Python engine itself).

---

## When to Use mofapy2

- Python pipelines that need to fit a MOFA model end-to-end without round-tripping to R
- Full programmatic control of the `build()` / `run()` / `save_model()` lifecycle
- GPU acceleration via CuPy, or SVI minibatching for N > 10⁵ samples
- Embedding MOFA inside a larger Python workflow (snakemake, nextflow, AnnData-centric pipelines)
- Producing the canonical HDF5 file that mofax and MOFA2 (R) both read

**Use other skills when:**
- You want the R API or R-side plotting → use `mofa-r` (which calls mofapy2 under the hood via reticulate)
- You start from single-cell counts and need donor-pseudo-bulk preprocessing → use `mofa-cellular`
- You already have a trained `.hdf5` and only want to plot / interrogate it → use `mofa-mofax`

---

## Installation

```bash
pip install mofapy2

# Optional GPU acceleration — match your CUDA major version
pip install cupy-cuda12x   # CUDA 12
# pip install cupy-cuda11x # CUDA 11
```

Verify:

```bash
python -c "from mofapy2.run.entry_point import entry_point; print('ok')"
```

---

## Quick Start

End-to-end fit. The `data` argument is a *nested list*: outer list is groups (use a single-element list when you have no group structure), inner list is views.

```python
import numpy as np
from mofapy2.run.entry_point import entry_point

# views: each is a feature × sample numpy array (NaN-aware for missingness)
# view1: RNA log-CPM       (genes × samples)
# view2: ATAC raw counts   (peaks × samples)
sample_ids = [f"s{i}" for i in range(view1.shape[1])]

ent = entry_point()
ent.set_data_matrix(
    data=[[view1, view2]],                       # [group][view]
    likelihoods=["gaussian", "poisson"],
    views_names=["rna_logcpm", "atac_counts"],
    samples_names=[sample_ids],                   # [group][sample]
)
ent.set_model_options(
    factors=10,                # initial K; ARD will prune unused factors
    spikeslab_weights=True,    # sparse loadings (recommended for omics)
    ard_weights=True,          # per-view ARD precision on W
    ard_factors=True,          # per-group ARD precision on Z
)
ent.set_train_options(
    seed=42,
    convergence_mode="medium", # fast | medium | slow
    gpu_mode=False,
    freqELBO=5,
)
ent.build()
ent.run()
ent.save_model("mofa_fit.hdf5")
```

The output HDF5 is read by `mofax.mofa_model("mofa_fit.hdf5")` in Python or `MOFA2::load_model("mofa_fit.hdf5")` in R.

---

## Key API Surfaces

### Input contracts

Three input entry points, picked by your data shape:

| API | Input shape | When to use |
|---|---|---|
| `set_data_matrix` (`entry_point.py:201`) | nested list of numpy arrays `[group][view]`, each `features × samples` | Programmatic / from scratch |
| `set_data_df` (`entry_point.py:389`) | tidy long-format pandas DataFrame (`sample`, `feature`, `view`, `group`, `value`) | When upstream code already produced a long table |
| `set_data_from_anndata` (`entry_point.py:550`) | one AnnData per view (or one AnnData with a layer per view) | AnnData-native workflows |

All three converge on the same internal `Y_Node` representation. Missingness encoded as `NaN` is preserved as a mask and integrated over the ELBO — do not impute.

### Likelihoods

Pass likelihoods as a per-view list via the `likelihoods=` kwarg on `set_data_matrix` / `set_data_df` / `set_data_from_anndata`; the value must be a subset of `{gaussian, bernoulli, poisson}`. The validator lives inline in `set_data_matrix` (`entry_point.py:371-382`) — there is no standalone `set_likelihoods` method. Auto-detection is provided by `guess_likelihoods` (`build_model/utils.py:99-115`): all 0/1 → bernoulli; all-integer → poisson; else gaussian. Always pass explicitly — auto-detect can misclassify pre-normalised data as gaussian even when it should not be a MOFA view at all.

See `mofa-framework/references/view-likelihoods.md` for the per-omic recommendation table (RNA log-CPM → gaussian, ATAC peaks → poisson or bernoulli, methylation β → gaussian after logit, etc.).

### Model options

```python
ent.set_model_options(
    factors=10,             # initial K; final K ≤ this after ARD pruning
    spikeslab_weights=True, # SW_Node on W: Bernoulli × Gaussian, recommended
    spikeslab_factors=False,# SZ_Node on Z: rarely useful
    ard_weights=True,       # AlphaW per view × factor — drives factor selection
    ard_factors=True,       # AlphaZ per group × factor
)
```

ARD shrinkage on W is the mechanism that prunes redundant factors during training (Gamma precision update in `Alpha_nodes.py:60`). Keep `ard_weights=True` unless you have a specific reason.

### Train options

`set_train_options` (`entry_point.py:857-1031`) controls the VI loop:

```python
ent.set_train_options(
    maxiter=1000,
    tolerance=0.0001,
    convergence_mode="medium",  # fast | medium | slow — sets tolerance presets
    seed=42,
    gpu_mode=False,
    weight_views=False,         # rescale views by inverse feature count
    freqELBO=5,                 # ELBO trace stride
    dropR2=None,                # if a float in (0, 1): drop factors with R² below this threshold
)
```

`dropR2` (the Python kwarg; surfaces as `drop_factor_threshold` / `drop.min_r2` in the R wrapper) lives at `entry_point.py:867` with the drop logic at `:932-948`. It drops a factor mid-training if its R² falls below the threshold across all views. Useful for auto-K; aggressive thresholds (≳0.02) can collapse K to 1 — start conservative (`dropR2=0.01`) or leave `None` to disable.

### Stochastic VI (SVI)

For N > 10⁵ samples, enable minibatching:

```python
ent.set_stochastic_options(
    batch_size=0.1,        # FRACTION in (0, 1], not a count
    learning_rate=0.5,
    forgetting_rate=0.25,
    start_stochastic=1,
)
```

`set_stochastic_options` lives at `entry_point.py:1033-1064`. The natural-gradient step enters `W_node` (`W_nodes.py:64-95`) and `Z_node` (`Z_nodes.py:49-100`) via the `ro` argument and per-minibatch index. Two hard incompatibilities baked into the codebase:

- **SVI ⊥ MEFISTO smooth covariates** (`entry_point.py:1037-1042`) — using `set_smooth_options` aborts the run if stochastic is on.
- **SVI disables auto factor-dropping** (`entry_point.py:1049-1051`) — pick your K up front when running SVI.

### MEFISTO (smooth covariates)

`set_covariates` (`entry_point.py:81`) declares the continuous covariate (time, space) per sample; `set_smooth_options` (`entry_point.py:1066`) then turns on the Gaussian-process prior on Z. Order matters: covariates must be set first (`entry_point.py:1103-1112` asserts this). Out of scope here — see the MEFISTO tutorial at https://biofam.github.io/MOFA2/MEFISTO.html and the parent `mofa-framework` skill.

### Lifecycle

`build()` constructs the Markov blanket from `Y / Z / W / Tau` nodes (`build_model/build_model.py:175-178`), then `run()` executes coordinate-ascent VI, then `save_model(path)` serialises the posterior to HDF5 (`build_model/save_model.py:115-119`). Call in that order; `run()` without `build()` errors.

---

## GPU Mode

Toggle via `set_train_options(..., gpu_mode=True)` (`entry_point.py:929`). The dispatch lives in `mofapy2/core/gpu_utils.py:1-12`: when `gpu_mode=True` it imports `cupy as cp` and the hot loops in `Z_nodes.py:122-144` and `W_nodes.py:75-84` route arrays through `gpu_utils.array` / `gpu_utils.dot` / `gpu_utils.asnumpy`.

Practical notes:

- The first call after import pays a one-time CuPy / CUDA warm-up (seconds, not minutes). Time the second run when benchmarking.
- Memory pressure scales with `K × N × p_total`. If you OOM, drop to SVI (`set_stochastic_options(batch_size=0.1, ...)`) or reduce `factors`.
- GPU mode is independent of stochastic mode. You can run dense GPU on moderate data, or SVI + GPU on very large data.

---

## Outputs

`save_model("mofa_fit.hdf5")` writes a single HDF5 with this layout:

| Path | Contents |
|---|---|
| `expectations/Z` | Posterior mean of factor scores, `N × K` per group |
| `expectations/W/<view>` | Posterior mean of loadings, `D_m × K` per view |
| `expectations/Tau/<view>` | Posterior noise precision (Gaussian views) |
| `variance_explained/r2_total/<group>` | Per-view total R², `views × 1` |
| `variance_explained/r2_per_factor/<group>` | Per-view per-factor R², `views × K` |
| `model_options` | Spikeslab / ARD flags, K |
| `training_options` | Maxiter, tolerance, seed, gpu_mode, convergence_mode |
| `intercepts/<view>` | Per-feature centering term |
| `data/<view>/<group>` | Original input matrix (centered for Gaussian views) |

Factors in the HDF5 are sorted descending by total R² across groups and views (`save_model.py:115-119`) — mimics PCA's eigenvalue order but is *not* the same thing; see `mofa-framework/references/variance-explained.md`.

For Python-side reading and plotting, pair with `mofa-mofax` (`mofax.mofa_model(path)`).

---

## Common Issues

| Issue | Solution |
|---|---|
| ELBO not monotone / oscillating | Set `convergence_mode="slow"`; increase `maxiter`; check for raw counts passed as gaussian |
| Factor count collapses to 1 (or 0 useful) | `dropR2` too aggressive — lower to `0.01` or set to `None` (disable). Also check for one view dwarfing others; enable `weight_views=True` |
| NaN in Z / W after fit | Likelihood mismatch — most commonly `poisson` on log-normalised data, or `gaussian` on highly skewed raw counts. Re-check the `likelihoods=` argument on `set_data_matrix` / `set_data_df` / `set_data_from_anndata` |
| GPU out-of-memory | Switch to SVI (`set_stochastic_options(batch_size=0.1)`); reduce initial `factors`; or fall back to CPU dense |
| Sign / factor order changes between runs | Expected — bilinear Bayesian models are sign-flip and permutation equivariant. Codebase orders by R² but does not fix sign. Impose a canonical sign downstream (e.g. force largest absolute loading positive per factor) |
| `set_data_matrix` rejects input | Most often a shape error — each view must be `features × samples`, and `data` must be a nested list `[group][view]` even with one group |
| MEFISTO + SVI raises at run | They are mutually exclusive by design (`entry_point.py:1037-1042`). Drop one |

---

## Resources

- **Upstream docs:** https://biofam.github.io/MOFA2/
- **Repository:** https://github.com/bioFAM/mofapy2
- **PyPI:** https://pypi.org/project/mofapy2/
- **MOFA+ paper (multi-group, sparse priors):** https://genomebiology.biomedcentral.com/articles/10.1186/s13059-020-02015-1
- **MOFA original paper:** https://www.embopress.org/doi/full/10.15252/msb.20178124

---

## When not to use

- Do not pass log-normalised data with `likelihoods=["poisson"]`. Poisson assumes raw integer counts.
- Do not pass row-wise (sample × feature) matrices; mofapy2 takes feature × sample per view inside the views list.
- Do not impute missing values before fit. mofapy2 integrates NaN over the ELBO; imputation biases the posterior.
- Do not enable stochastic SVI together with MEFISTO smooth covariates; the codebase forbids it.

---

## See also

- `mofa-framework`
- `mofa-mofax`
- `anndata`
