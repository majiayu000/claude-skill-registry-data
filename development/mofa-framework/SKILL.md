---
name: mofa-framework
description: "MOFA family router — Multi-Omics Factor Analysis, a Bayesian group factor model with per-view likelihoods, ARD sparsity, and a shared latent Z. Use first when choosing among the four MOFA implementations, or when a cross-cutting concern applies (counts vs log-normalised, R-squared semantics, sign ambiguity, GPU/SVI, the no-biplot caveat)."
license: MIT
---

# MOFA Framework and Router

## Overview

MOFA (Multi-Omics Factor Analysis) is a **Bayesian group factor model**: per-view likelihoods (gaussian / bernoulli / poisson), ARD-driven sparsity, a single latent matrix Z shared across views, one independent W per view, and a coordinate-ascent variational inference loop monitoring an ELBO. The math lives in `mofapy2` (Python); `MOFA2` is an R interface plus plotting that calls the Python engine via reticulate/basilisk; `MOFAcellulaR` is a single-cell pseudo-bulk + tissue-association layer on top of `MOFA2`; `mofax` is a Python downstream / visualisation reader for the trained HDF5.

This skill is the **router** for the `mofa-*` cluster. Every child skill (mofa-mofapy2, mofa-r, mofa-cellular, mofa-mofax) inherits the patterns documented here. Concerns shared across implementations live in `references/*.md` rather than in any one child. For the *super-family* (non-MOFA alternatives like FAMD/MFA, scITD, sciRED, mixOmics/DIABLO), route up to `factor-analysis-framework`.

**Citation:** cite the MOFA+ paper (Argelaguet et al., *Genome Biology* 2020) and, if you used the donor pseudo-bulk variant, the MOFAcellulaR paper (Ramirez Flores et al., *Cell Reports Methods* 2023). MEFISTO smooth-covariate users cite Velten et al., *Nature Methods* 2022.

---

## Installation

### Python (engine + downstream)

```bash
pip install mofapy2 mofax
# Optional GPU acceleration via CuPy:
pip install cupy-cuda12x          # match your CUDA version
```

### R (bindings + single-cell variant)

```r
# Core bindings — this also pulls mofapy2 into a managed conda env via basilisk
BiocManager::install("MOFA2")
# Single-cell pseudo-bulk variant
remotes::install_github("saezlab/MOFAcellulaR")
```

`MOFA2` (R) does not reimplement the math. It calls `mofapy2` (Python) under the hood via `reticulate` / `basilisk` (see `MOFA2/R/run_mofa.R`, `MOFA2/R/basilisk.R`). The two environments must agree on `mofapy2` version.

---

## Model-selection decision tree

```
Need to fit a multi-view factor model with mixed likelihoods?
│
├─ Working language?
│   │
│   ├─ Python
│   │   ├─ Fitting only (define model, train, save HDF5)         → mofa-mofapy2
│   │   ├─ Downstream on a trained HDF5 (load, plot, associate)  → mofa-mofax
│   │   └─ Both                                                   → mofa-mofapy2 → mofa-mofax
│   │
│   └─ R
│       ├─ Grain: cells (or any per-row observations)             → mofa-r
│       └─ Grain: donor pseudo-bulk, cell-type-as-view
│           (single-cell → donor aggregation + associations)      → mofa-cellular
│
└─ Don't need MOFA specifically?
    ├─ Want a Benzécri-style biplot with categorical levels       → factor-analysis-framework (FAMD/MFA)
    └─ Want a single-omic linear embedding                        → scanpy (PCA) or scvi-linearscvi
```

---

## The MOFA family at a glance

| Skill | Layer | Primary use | Language |
|---|---|---|---|
| `mofa-mofapy2` | engine | Define model, fit, save HDF5 (`set_data_matrix`, `build`, `run`, `save`) | Python |
| `mofa-r` | bindings + plotting | `create_mofa`, `run_mofa`, `plot_factors`, `plot_weights`, `correlate_factors_with_covariates` | R |
| `mofa-cellular` | preprocessing + associations | Donor pseudo-bulk → views, MOFA fit, ANOVA/regression downstream | R |
| `mofa-mofax` | downstream | Load trained HDF5, `get_factors`, `get_weights`, basic plots in Python | Python |

The fit produced by any of the four is the same Bayesian model. The HDF5 written by `mofapy2/build_model/save_model.py` is the lingua franca — every other tool reads from it. See `references/interop-matrix.md`.

---

## Shared contract (all children inherit)

All children expect the same input shape and produce the same output shape.

**Input:** a list of M view matrices, each of shape `D_m × N` (features × samples). One likelihood per view. Missing values are `NaN` (Python) or `NA` (R) — they are **integrated out** of the ELBO, not imputed (`mofapy2/core/nodes/Y_nodes.py:46-50` masks `self.value[mask] = 0.0` while keeping the mask for the likelihood term).

**Output:** Z (`N × K`), per-view W (`D_m × K` × M), per-(group, view, factor) R², per-(view, factor) ARD precisions, plus the noise precision Tau.

### Python lifecycle

```python
from mofapy2.run.entry_point import entry_point

ent = entry_point()
ent.set_data_matrix(
    data=[Y_rna, Y_atac_binary, Y_counts],     # list of M (D_m × N) matrices
    likelihoods=["gaussian", "bernoulli", "poisson"],
    views_names=["rna", "atac", "counts"],
)
ent.set_model_options(
    factors=10,
    spikeslab_weights=True,                    # ARD + spike-and-slab on W
    spikeslab_factors=False,
)
ent.set_train_options(
    seed=42,
    gpu_mode=True,                             # requires CuPy
    convergence_mode="medium",                 # fast / medium / slow
    stochastic=False,                          # set True for SVI
    drop_factor_threshold=0.01,                # prune factors with total R² < threshold
)
ent.build()
ent.run()
ent.save("model.hdf5")
```

### R lifecycle

```r
library(MOFA2)

mofa <- create_mofa(views_list)                              # views_list: named list of D_m × N matrices
mofa <- prepare_mofa(
  mofa,
  model_options = list(num_factors = 10,
                       likelihoods = c(rna = "gaussian",
                                       atac = "bernoulli")),
  training_options = list(seed = 42, convergence_mode = "medium")
)
mofa <- run_mofa(mofa, outfile = "model.hdf5")               # calls mofapy2 via basilisk
```

**Contract rules** (every child enforces these):

1. Per-view matrices are **features × samples**, not samples × features.
2. One likelihood per view. The auto-detector (`mofapy2/build_model/utils.py:99-115`) infers gaussian / bernoulli / poisson from data values; override explicitly when in doubt.
3. Missing values stay as `NaN` / `NA`. Do **not** zero-impute count views — zero is real signal.
4. Sample / group structure (donor, batch) is declared via `set_group` (or the R equivalent) **before** `build()`.
5. The seed is the single most important reproducibility lever — Bayesian VI is sensitive to it (`mofapy2/run/entry_point.py:1017`).

---

## Cross-cutting references (load on demand)

| Topic | File |
|---|---|
| Architecture (Markov blanket, bilinear Y≈ZW^T, ARD, VI loop) | `references/mofa-architecture.md` |
| Per-view likelihood selection (gaussian / bernoulli / poisson) | `references/view-likelihoods.md` |
| R² semantics — what it is NOT (not a partition, factor ordering) | `references/variance-explained.md` |
| Geometric caveats — duality absent, no biplot, sign / order ambiguity | `references/geometric-caveats.md` |
| The L1 supplementary-projection patch (when MOFA is the upstream) | `references/supplementary-projection-on-z.md` |
| Implementation transitions (mofapy2 ↔ R ↔ mofax ↔ MOFAcellulaR) | `references/interop-matrix.md` |
| Failure modes (ELBO non-monotone, OOM, sign flips, ...) | `references/troubleshooting.md` |

Child skills link directly into these — do **not** copy-paste their content into a child SKILL.md. If a child needs a different treatment of a shared concern, override locally and cite the difference back here.

---

## Verification and self-evolution

- `checks/pre-fit-checklist.md` — 8-item checklist the agent walks before calling `ent.run()` / `run_mofa()`.
- `references/troubleshooting.md` — append-only log. Record new failure modes here instead of carving a new skill on first encounter.
- `references/cross-refs.yaml` — curated design record of the intended routing graph for this cluster, kept for reference when writing or auditing each child's `## See also` prose. There is no `metadata.complementary-skills` frontmatter anymore and no validator checks this file against the SKILL.md bodies — it is not enforced, so it can drift from the prose. Treat it as a curated starting point, not ground truth.

---

## The four-Benzécri caveat

MOFA is a Bayesian generative model, not a Benzécri-school SVD. Per the geometric audit at `docs/vision/latent/mofa.md` §2.1–2.4, MOFA fails all four Benzécri properties:

1. **Duality absent** — Z and W are two separate posterior expectations with no shared singular-value matrix. `get_factors(scale=TRUE)` (`MOFA2/R/get_methods.R:209`) and `get_weights(scale=TRUE)` (`get_methods.R:266`) divide by `max(|.|)` *independently*. No biplot function exists across mofapy2, MOFA2, or MOFAcellulaR (verified by `grep -rn biplot`).
2. **Inertia decomposition absent** — per-(view, group, factor) R² is computed against the full Y (`MOFA2/R/calculate_variance_explained.R:80-84`), so `Σ_k r2[m, k] ≠ r2_total[m]`. The `max(0, .)` floor (`calculate_variance_explained.R:73-76`) is the tell that this is not a budget.
3. **Categorical-level-as-barycenter absent at fit-time** — `summarise_factors` (`MOFA2/R/correlate_covariates.R:114-171`) and `correlate_factors_with_covariates` (`correlate_covariates.R:23-95`) compute the right numerics post-hoc but render as tile / corrplot heatmaps, not as labelled points on `plot_factors`.
4. **Distribution-free framing absent** — fully Bayesian VI; output depends on prior, init (`mofapy2/build_model/init_model.py:78`), and seed (`entry_point.py:1017`). The bilinear likelihood is sign-flip equivariant per factor and permutation equivariant across factors; `save_model.py:115-119` sorts factors by total R² (fixing order, not sign).

The natural mitigation is the **L1 supplementary-projection patch** documented in `references/supplementary-projection-on-z.md`: continuous variables become arrows via `cor(Z[, α], v)`, categorical levels become points via `colMeans(Z[labels == ℓ, ])`. The numeric machinery already lives in `correlate_factors_with_covariates` and `summarise_factors`; only the display layer is missing.

For the trade-off between "good model" (modelling fitness — MOFA wins) and "good map" (Benzécri reading — FAMD/MFA wins), and how an L1 overlay on Z gives you both, route up to `factor-analysis-framework`.

---

## Resources

- **MOFA+ docs:** https://biofam.github.io/MOFA2/
- **MOFA+ paper:** https://genomebiology.biomedcentral.com/articles/10.1186/s13059-020-02015-1
- **MOFAcellulaR paper / vignette:** https://www.cell.com/cell-reports-methods/fulltext/S2667-2375(23)00111-1 ; https://saezlab.github.io/MOFAcellulaR/
- **MEFISTO paper:** https://www.nature.com/articles/s41592-021-01343-9
- **mofapy2 GitHub:** https://github.com/bioFAM/mofapy2
- **MOFA2 GitHub:** https://github.com/bioFAM/MOFA2
- **MOFAcellulaR GitHub:** https://github.com/saezlab/MOFAcellulaR
- **mofax GitHub:** https://github.com/bioFAM/mofax

---

## When not to use

- Do not use this skill alone to run MOFA. Pair with the specific mofa-* implementation skill.
- Do not use for single-omic Gaussian PCA (use scanpy) or nonlinear viz (use UMAP/t-SNE).
- Do not use as a biplot generator out of the box. MOFA does not produce a Benzécri-style biplot; see references/geometric-caveats.md and references/supplementary-projection-on-z.md.

---

## See also

- `factor-analysis-framework`
- `mofa-mofapy2`
- `mofa-r`
- `mofa-cellular`
- `mofa-mofax`
- `muon-multimodal-analysis`
- `multimodal-anndata-mudata`
- `anndata`
