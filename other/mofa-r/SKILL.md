---
name: mofa-r
description: "MOFA2 — R bindings and plotting for Multi-Omics Factor Analysis. Use to fit MOFA from R (it calls the mofapy2 engine via reticulate/basilisk) and to run the standard downstream methods: get_factors, get_weights, plot_factors, correlate_factors_with_covariates, calculate_variance_explained. For Python-side fitting use mofa-mofapy2."
license: MIT
---

# MOFA2: R Bindings and Plotting

**Foundation:** `mofa-framework` is the router and holds all shared patterns. Jump directly to:
- `mofa-framework/references/mofa-architecture.md` — Markov blanket, bilinear `Y ≈ ZW^T`, ARD, VI loop
- `mofa-framework/references/view-likelihoods.md` — gaussian / bernoulli / poisson per view
- `mofa-framework/references/variance-explained.md` — why per-(view, factor) R² is NOT a partition
- `mofa-framework/references/geometric-caveats.md` — duality absent, no biplot, sign/order ambiguity
- `mofa-framework/references/supplementary-projection-on-z.md` — the L1 patch (arrows + level points on Z)
- `mofa-framework/checks/pre-fit-checklist.md` — pre-flight before `run_mofa()`

This file covers only the parts that differ for MOFA2 (R bindings + plotting).

---

## When to Use MOFA2 (R)

- R/Bioconductor workflows where the rest of the pipeline (DE, GSEA, annotation) is already in R.
- `SingleCellExperiment` / `SummarizedExperiment` / `MultiAssayExperiment` inputs — there are dedicated constructors.
- Downstream associations (covariate correlation, ANOVA-style summaries) need to be done in R.
- `ggplot2` / `cowplot` / `patchwork` composability matters — the returned plot objects are real `ggplot` objects.
- You want the Python engine but prefer to script and orchestrate from R.

**Limitations:** requires a working Python install (basilisk-managed conda env or user-supplied reticulate env); no biplot; sign and factor order are non-canonical across runs.

---

## Installation

```r
# Core bindings — basilisk will lazily provision a conda env with mofapy2 the
# first time you call run_mofa(). See MOFA2/R/basilisk.R for the env spec.
BiocManager::install("MOFA2")
```

Manual Python env (skip basilisk):

```r
# Point reticulate at a Python that already has mofapy2 installed.
reticulate::use_python("/opt/conda/envs/mofa/bin/python", required = TRUE)
library(MOFA2)
# Verify
reticulate::py_module_available("mofapy2")
```

The basilisk env spec lives in `MOFA2/R/basilisk.R`. The Python engine version is pinned there; if you upgrade `mofapy2` in your own env, make sure it matches what `MOFA2` expects, or stick to basilisk.

---

## Quick Start

```r
library(MOFA2)

# views_list is a NAMED list of feature x sample matrices, one per view
mofa <- create_mofa(views_list)

data_opts  <- get_default_data_options(mofa)
model_opts <- get_default_model_options(mofa)
model_opts$num_factors <- 10
train_opts <- get_default_training_options(mofa)
train_opts$seed             <- 42
train_opts$convergence_mode <- "medium"

mofa <- prepare_mofa(
  mofa,
  data_options     = data_opts,
  model_options    = model_opts,
  training_options = train_opts
)

mofa <- run_mofa(mofa, outfile = "mofa_fit.hdf5")  # calls Python under the hood

# Downstream
Z  <- get_factors(mofa)
r2 <- calculate_variance_explained(mofa)
plot_factors(mofa, factors = 1:2, color_by = "condition")
```

**Verify it worked:**

```r
stopifnot(inherits(mofa, "MOFA"))
stopifnot(is.list(Z) || is.matrix(Z))           # Z is a list-per-group or a single matrix
stopifnot(length(get_weights(mofa)) == length(views_list))   # one W per view
```

---

## Key API surfaces

Constructors:

- `create_mofa(data)` — generic dispatch on a named list of matrices, a long data.frame, a `MultiAssayExperiment`, or a Seurat object. Returns an untrained `MOFA` S4 object. (`MOFA2/R/create_mofa.R`)
- `create_mofa_from_matrix(data, groups = NULL)` — list of feature x sample matrices.
- `create_mofa_from_MultiAssayExperiment(mae)` — pulls assays as views.
- `create_mofa_from_df(df)` — long format with columns `feature`, `view`, `sample`, `value` (and optional `group`).

Configuration and fitting:

- `prepare_mofa(mofa, data_options, model_options, training_options)` (`MOFA2/R/prepare_mofa.R`) — sets the three option blocks; called once before `run_mofa()`. Use `get_default_data_options()`, `get_default_model_options()`, `get_default_training_options()` as starting templates and mutate.
- `run_mofa(mofa, outfile, use_basilisk = TRUE)` (`MOFA2/R/run_mofa.R`) — invokes the Python engine via `basilisk::basiliskRun()` (or, if `use_basilisk = FALSE`, directly via `reticulate`). Writes HDF5 to `outfile` and returns the trained `MOFA` S4 object.
- `load_model(file)` (`MOFA2/R/load_model.R`) — deserialises an HDF5 produced elsewhere (mofapy2 directly, another R session, or a colleague). Round-trip: `run_mofa(...)` -> HDF5 -> `load_model(HDF5)` produces the same downstream interface.

Accessors:

- `get_factors(model, factors = "all", groups = "all", scale = FALSE, as.data.frame = FALSE)` (`MOFA2/R/get_methods.R:192-214`) — returns Z. With `scale = TRUE`, divides Z by `max(abs(Z))` (line 209). This scaling is **independent** of anything done to W.
- `get_weights(model, views = "all", factors = "all", scale = FALSE, as.data.frame = FALSE)` (`MOFA2/R/get_methods.R:248-272`) — returns W as a **list over views**; each element is a `D_m x K` matrix. With `scale = TRUE`, divides each view's W by `max(abs(W))` (line 266). **Independent** of Z scaling.
- `get_expectations(model, variable, ...)` (`MOFA2/R/get_methods.R:494+`) — generic accessor over the node graph (Z, W, Tau, Alpha, ...).
- `samples_metadata(mofa) <- df` — attach sample metadata used by every plot/correlate function downstream. The row order of `df` must match `samples_names(mofa)`.

---

## Plotting

What MOFA2 ships (`R/plot_*.R`, 25 `plot_*` man pages). Each returns a `ggplot` object you can `+` onto.

- `plot_factors(model, factors = c(1, 2), color_by = NULL, shape_by = NULL)` (`MOFA2/R/plot_factors.R:290-379`) — sample scatter on `F_alpha x F_beta`. Categorical metadata enters as `color_by` / `shape_by` aesthetics (lines 322-323, 356) — **not** as a coordinate. Levels do not get points on the map.
- `plot_factor(model, factor, color_by = NULL, ...)` — single-factor beeswarm of Z values.
- `plot_weights_scatter(model, view, factors = c(1, 2))` (`MOFA2/R/plot_weights.R:97-191`) — feature scatter of W on `F_alpha x F_beta`. **Different axes** from `plot_factors`; axes are scaled independently (lines 147-150). The two are not in a shared metric — see Foundation/geometric-caveats.
- `plot_weights(model, view, factor, ...)` (`MOFA2/R/plot_weights.R:249+`) — single-factor loading vector as a horizontal bar chart.
- `plot_top_weights(model, view, factor, nfeatures = 10)` (`MOFA2/R/plot_weights.R:456+`) — top-N features by `|W|` on one factor.
- `plot_data_heatmap(model, factor, view, features)` / `plot_data_scatter(model, factor, view, features)` — show the raw data behind a factor.
- `plot_factor_cor(model)` — correlation matrix of Z columns. Docs at `MOFA2/R/plot_factors.R:471` warn that "the model encourages the factors to be uncorrelated, so this function usually yields a diagonal correlation matrix" — *usually*, not exactly. Always run this once after a fit.
- `plot_variance_explained(model)` — heatmap of the R² returned by `calculate_variance_explained()`.

**No biplot.** `ls MOFA2/man/ | grep -i biplot` returns empty; `grep -rn "biplot" MOFA2/` returns empty. There is no MOFA2 function that co-projects Z and W on shared axes — the architecture does not support it (no shared singular values). When you need a biplot-style co-plot, follow the L1 supplementary-projection patch documented in `mofa-framework/references/supplementary-projection-on-z.md`; the numeric machinery (`correlate_factors_with_covariates`, `summarise_factors`) already exists.

---

## Associations and downstream

- `correlate_factors_with_covariates(model, covariates, plot = "log_pval", ...)` (`MOFA2/R/correlate_covariates.R:23-95`) — Pearson correlation of each Z column against each metadata column; renders as a `corrplot` heatmap (line 78) or BH-adjusted `-log10(p)` heatmap (line 89). This **is** the Benzécri supplementary-continuous-variable formula `g_alpha = cor(v, F_alpha)` — the data plumbing exists, the geometric overlay does not.
- `summarise_factors(model, group_by)` (`MOFA2/R/correlate_covariates.R:114-171`) — per-level median of Z within each level of a discrete grouping; renders as a `geom_tile` heatmap (line 150). This **is** the Benzécri level-barycenter computation — same amputation as above (right number, wrong rendering).
- `calculate_variance_explained(model, factors = "all", groups = "all", views = "all")` (`MOFA2/R/calculate_variance_explained.R:31-107`) — returns a `(group x view x factor)` array of `1 - SSE/SST` per cell. **NOT a partition.** See `mofa-framework/references/variance-explained.md` for the four reasons (denominator is full Y, no orthogonality enforced, factors ordered post-hoc by total R², no `cos²/ctr` semantics). The `max(0, .)` floor at lines 73-76, 94-97 is the tell.
- `predict(model, views = "all", factors = "all")` (`MOFA2/R/predict.R:29-78`) — reconstructs `Y_hat = Z W^T + intercept` (lines 61, 68). Useful for missing-value imputation; not for inertia accounting.

---

## Common Issues

| Issue | Cause | Fix |
|---|---|---|
| `Error: mofapy2 not found` on `run_mofa()` | basilisk env not provisioned, or reticulate is pointed at a Python without `mofapy2` | Either let basilisk handle it (`run_mofa(use_basilisk = TRUE)`, first call is slow), or set `reticulate::use_python(...)` to a Python where `mofapy2` is installed **before** `library(MOFA2)`. |
| `"Likelihood mismatch"` warning at `prepare_mofa()` | The auto-detector inferred the wrong likelihood (e.g. log-counts looked Gaussian but you wanted Poisson on raw counts) | Set `model_opts$likelihoods <- c(rna = "gaussian", atac = "bernoulli", counts = "poisson")` explicitly. See `mofa-framework/references/view-likelihoods.md`. |
| `plot_factors` and `plot_weights_scatter` produce mismatched scales | Expected. Z and W are scaled independently (`get_methods.R:209` vs `get_methods.R:266`) and have no shared singular value | Don't overlay them directly. Use the L1 patch from `mofa-framework/references/supplementary-projection-on-z.md`. |
| Sign or factor-order flips between runs | Expected. Bilinear `Y ≈ ZW^T` is sign-flip equivariant per factor; `save_model.py:115-119` sorts factors by total R² but does not fix sign | If cross-run comparison matters, impose a canonical sign downstream (e.g. flip so the largest absolute loading is positive). |
| `samples_metadata(mofa) <- df` complains about row order, or aesthetics map to the wrong cells | `df` must be in the same order as `samples_names(mofa)` (concatenation of per-group sample names) | `df <- df[match(samples_names(mofa), df$sample), ]` before assignment. |
| `Σ_k r2[m, k]` does not equal `r2_total[m]` | Expected. Per-factor R² is computed against the full Y, not against the residual after k-1 factors (`calculate_variance_explained.R:80-84`) | Use R² as a per-factor diagnostic, not as a budget. See `mofa-framework/references/variance-explained.md`. |
| First `run_mofa()` is very slow / appears to hang | basilisk is provisioning the conda env in the background; one-time cost | Wait it out, or pre-provision: `BiocManager::install("MOFA2")` followed by `MOFA2:::.MOFA2_dependencies` setup, or supply your own Python via `reticulate::use_python()` and `run_mofa(use_basilisk = FALSE)`. |

---

## Resources

- **MOFA2 Bioconductor:** https://bioconductor.org/packages/release/bioc/html/MOFA2.html
- **GitHub:** https://github.com/bioFAM/MOFA2
- **Vignettes (in-source):** `vignettes/getting_started_R.Rmd`, `vignettes/downstream_analysis.Rmd`, `vignettes/MEFISTO_temporal.Rmd`
- **Website:** https://biofam.github.io/MOFA2/
- **MOFA+ paper:** https://genomebiology.biomedcentral.com/articles/10.1186/s13059-020-02015-1

---

## When not to use

- Do not use without a working Python install. MOFA2 R calls mofapy2 under the hood via reticulate/basilisk; the conda env is required.
- Do not expect a biplot. MOFA2 has 25 `plot_*` man pages and none of them co-projects Z and W; use the L1 supplementary-projection patch from mofa-framework/references/supplementary-projection-on-z.md.
- Do not pass `get_factors(scale=TRUE)` and `get_weights(scale=TRUE)` outputs into the same coordinate system; the two scalers are independent `max(|.|)` normalisations, not the two halves of a shared SVD.

---

## See also

- `mofa-framework`
- `mofa-cellular`
- `muon-multimodal-analysis`
