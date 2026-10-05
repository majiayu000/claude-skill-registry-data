---
name: mofa-cellular
description: "MOFAcellulaR — pseudo-bulk preprocessing and downstream-association layer on top of MOFA2. Use for cross-condition single-cell atlases where donors are rows and cell types become MOFA views (donor x cell-type grain, not cell grain). Wraps filtering, TMM/log-CPM, per-view centring, MOFA fitting, and ANOVA of factors against donor metadata."
license: MIT
---

# MOFAcellulaR: Donor Pseudo-Bulk × Cell-Type Views

**Foundation:** `mofa-framework` is the router and holds all shared MOFA patterns. Jump directly to:
- `mofa-framework/references/mofa-architecture.md` — Markov blanket (Y/Z/W/Tau), ARD pruning, ELBO trace
- `mofa-framework/references/view-likelihoods.md` — gaussian / bernoulli / poisson per view (MOFAcellulaR uses gaussian on log-CPM)
- `mofa-framework/references/variance-explained.md` — per-factor R² is not an inertia partition
- `mofa-framework/references/geometric-caveats.md` — no biplot, sign / order indeterminacy, no shared Σ
- `mofa-framework/references/supplementary-projection-on-z.md` — supplementary covariate / level projection onto Z
- `mofa-framework/checks/pre-fit-checklist.md` — pre-flight before `create_mofa()` / `run_mofa()`

This file covers only the parts that differ for MOFAcellulaR (single-cell pseudo-bulk preprocessing and downstream donor-level associations).

---

## When to Use MOFAcellulaR

- Cross-condition single-cell atlases (multiple donors × multiple cell types).
- You want to find *multicellular* programs that link cell types via shared donor variation.
- Donor-level metadata (condition, age, sex, biopsy site) is your primary regressor.
- You explicitly want pseudo-bulk grain (donor scores, not cell scores).

**Use other skills when:**
- You want a per-cell MOFA fit → use `mofa-r` (R) or `mofa-mofapy2` (Python).
- You want Python-side downstream viz on a trained HDF5 → use `mofa-mofax`.
- You want non-MOFA multi-view factor analysis → route up to `factor-analysis-framework`.

---

## The grain shift — what makes this different from mofa-r

In a per-cell MOFA fit (`mofa-r` / `mofa-mofapy2`) each **cell** is a row of Z, each **modality** (RNA, ATAC, methylation, …) is a view, and N is on the order of 10⁴–10⁶. In MOFAcellulaR each **donor** is a row of Z, each **cell type** is a view, and N drops to 10–100. `pb_dat2MOFA` (`MOFAcellulaR/R/create_init_exp.R:79-99`) pivots the per-cell-type pseudobulks into MOFA2's multiview long-format with `sample_column = "donor_id"`; from there the engine is the same shared-Z / per-view-W bilinear Gaussian model, but the geometry now reads donor × multicellular-program.

Two consequences from `mofa.md` §4:
1. The n≪p regime becomes acute. The latent-lens stability gate (Tucker congruence < 0.85 = unstable; resampling required) bites hard at donor grain.
2. Donor metadata is the *only* signal worth supplementary-projecting onto Z. The Benzécri Level-1 patch is *more* useful here than at single-cell grain.

---

## Installation

```r
# MOFAcellulaR — pulls MOFA2 (R bindings) and via basilisk a managed mofapy2 (Python)
remotes::install_github("saezlab/MOFAcellulaR")
# Hard dependencies
BiocManager::install(c("MOFA2", "SummarizedExperiment", "edgeR"))
install.packages(c("tibble", "dplyr"))
```

`MOFAcellulaR` calls `MOFA2` for the fit, which in turn calls `mofapy2` via reticulate / basilisk. See `mofa-framework` for environment pinning.

---

## Quick Start — the canonical pipeline

The intended sequential call order from the official vignette (`vignette("MOFAcellulaR")`):

```r
library(MOFAcellulaR)
library(MOFA2)

# Inputs:
#   counts   — gene × cell raw integer count matrix
#   coldata  — data.frame with at minimum: donor_id, cell_type, condition
#              (one row per cell; row order matches columns of counts)

# 1. Wrap as SummarizedExperiment, split by cell type into pseudo-bulks
se <- create_init_exp(counts = counts, coldata = coldata)

# 2. Drop (donor × cell_type) pseudo-bulks backed by too few cells
se <- filt_profiles(se, min_cells = 10, ncells = "cells")

# 3. Drop low-expression genes per view (edgeR::filterByExpr)
se <- filt_gex_byexpr(se, min_count = 5, min_prop = 0.25)

# 4. TMM normalisation → log-CPM (stored in assay "logcounts")
se <- tmm_trns(se)

# 5. Per-view feature centring (scale = FALSE) — leaves variance untouched
se <- center_views(se)

# 6. Pivot to MOFA2 long-format: feature, view, sample, value
mofa_input <- pb_dat2MOFA(se, sample_column = "donor_id")

# 7. Standard MOFA2 fit (gaussian on log-CPM)
mofa <- create_mofa(mofa_input)
mofa <- prepare_mofa(mofa,
                    data_options       = get_default_data_options(mofa),
                    model_options      = get_default_model_options(mofa),
                    training_options   = get_default_training_options(mofa))
mofa <- run_mofa(mofa, outfile = "mofa_model.hdf5", use_basilisk = TRUE)

# 8. Downstream — tidy join + ANOVA against donor metadata
tidy  <- get_tidy_factors(mofa, factor = "all", metadata = coldata)
assoc <- get_associations(mofa,
                         metadata          = coldata,
                         sample_id_column  = "donor_id",
                         test_variable     = "condition")
```

**Verify it worked:**

```r
stopifnot(MOFA2::get_dimensions(mofa)$N == length(unique(coldata$donor_id)))
stopifnot("Factor1" %in% colnames(MOFA2::get_factors(mofa)[[1]]))
stopifnot(nrow(assoc) >= 1)  # at least one factor tested
```

---

## Key API surfaces

| Function | File:line | Role |
|---|---|---|
| `create_init_exp()` | `MOFAcellulaR/R/create_init_exp.R:26-32` | Wrap `counts` + `coldata` into a `SummarizedExperiment`; one column per (donor, cell_type) pseudo-bulk. |
| `filt_profiles()` | `MOFAcellulaR/R/filtering_basic.R` | Drop pseudo-bulks backed by fewer than `min_cells` cells. Defaults to `ncells = "cells"` column in coldata; review per dataset. |
| `filt_gex_byexpr()` | `MOFAcellulaR/R/filtering_basic.R` | Per-view gene filter wrapping `edgeR::filterByExpr` (`min_count`, `min_prop`). Applied independently per cell-type view. |
| `tmm_trns()` | `MOFAcellulaR/R/normalization.R` | TMM normalisation + `cpm(log = TRUE)`. Output stored in `assay(se, "logcounts")`. |
| `center_views()` | `MOFAcellulaR/R/create_init_exp.R:144-160` | Per-view feature centring `scale(dat, scale = FALSE)` (line 150). Centres, does **not** scale to unit variance — MOFA2's own `process_data` handles per-view scaling. |
| `pb_dat2MOFA()` | `MOFAcellulaR/R/create_init_exp.R:79-99` | Pivot to MOFA2 multiview long-format (`feature`, `view`, `sample`, `value`). `sample_column = "donor_id"` (line 79) sets the row axis; each cell type becomes a view. |
| `get_tidy_factors()` | `MOFAcellulaR/R/get_tidy_factors.R` | Join `MOFA2::get_factors()` with `coldata` into a long tibble (`sample`, `factor`, `value`, metadata columns). |
| `get_associations()` | `MOFAcellulaR/R/get_associations.R:49-115` | Per-factor `aov(value ~ test_variable)` (parametric) or Kruskal–Wallis; BH-adjusted. `mode = "regression"` for continuous outcomes. Returns one row per factor. |
| `plot_MOFA_hmap()` | `MOFAcellulaR/R/plot_MOFA_hmap.R` | Factor-score heatmap (donors × factors) with `ComplexHeatmap` metadata annotation tracks. |
| `plot_sample_2D()` | `MOFAcellulaR/R/plot_sample_2D.R:41-113` | **Warning surface.** Defaults to `uwot::umap()` on Z at line 89 (or MDS at line 64). Discards the linearity of Z. Prefer `MOFA2::plot_factors()` (linear F_α × F_β scatter) — see Caveats below. |
| `project_data()` | `MOFAcellulaR/R/project_data.R:50-90` | Out-of-sample projection: `Z_new = X_new · MASS::ginv(W)` (Moore–Penrose pseudoinverse, line 63). Valid only when noise precision Tau is high and prior precision Alpha is low; otherwise drifts from the trained posterior Z. |

---

## Outputs

- **`mofa`** — a standard MOFA2 S4 model object (HDF5-backed). Consumable by every `mofa-r` and `mofa-mofax` downstream function.
- **`tidy`** — long-format tibble joining Z with donor metadata. Drop-in for `ggplot2`.
- **`assoc`** — data.frame of (factor, statistic, p, p.adj). One row per factor for the chosen `test_variable`.

All three are compatible with the downstream patterns in `mofa-r` (factor plots, weights, gene-set enrichment, factor-score boxplots).

---

## Two structural caveats unique to MOFAcellulaR

Both are inherited from `mofa.md` §1.3 and apply on top of every caveat in `mofa-framework/references/geometric-caveats.md`.

1. **UMAP-on-Z compounds the duality loss.** MOFA's Z is already not a Benzécri biplot row-space — sample-points in Z and feature-points in W do not share a metric (no shared Σ; `mofa-framework/references/geometric-caveats.md`). `plot_sample_2D()` (`MOFAcellulaR/R/plot_sample_2D.R:89`) then runs `uwot::umap(factors)` on top of Z. The result is non-linear *and* non-dual: supplementary-projection arrows from `correlate_factors_with_covariates` cannot land on the rendered UMAP axes, and Euclidean distance between two donors on the UMAP has no factor-space meaning. Prefer the linear `MOFA2::plot_factors(mofa, factors = c(1, 2))` scatter; reserve the UMAP for cluster-presentation only.

2. **Donors-as-rows at n = 10–100 makes the n≪p regime acute.** Per-cell MOFA may have N ~ 10⁴–10⁶; MOFAcellulaR has N ~ 10–100 donors. At this scale neither MOFA nor any factor-analytic method is safe without resampling stability. Apply a latent-lens-style stability gate (e.g. Tucker congruence ≥ 0.85 across bootstrap re-fits) before trusting any biplot, association, or factor-rank interpretation. MOFAcellulaR does *not* provide this gate out of the box; wire it in yourself.

---

## Common Issues

| Issue | Solution |
|---|---|
| `filt_profiles` drops too many pseudo-bulks | Relax `min_cells`, or audit upstream cell-typing — rare cell types systematically lose donors. |
| `pb_dat2MOFA` produces `NaN` in long-format | Expected. Some (donor, cell_type) pseudo-bulks have zero cells and become missing views for that donor. mofapy2 integrates NaN over the ELBO; do not impute. |
| `get_associations` p-values all significant | Small n + many factors invites false positives. Filter to stability-passing factors first; consider `mode = "regression"` if the donor metadata is continuous. |
| Cell-type abundance varies wildly per donor | Consider MOFA2's `weight_views` option (rescales views by inverse feature count in the ELBO; `mofa-framework/references/variance-explained.md`). |
| Sign / order of factors changes across re-fits | MOFA does not enforce a canonical sign. Pin a sign convention post-fit (e.g. flip so the largest absolute loading is positive) before rendering biplots. |
| `project_data()` Z_new looks unrelated to training Z | The Moore–Penrose projection equals the posterior Z only at high Tau and low Alpha. Inspect `get_variance_explained()` and ARD precisions before trusting it. |

---

## Resources

- **GitHub:** https://github.com/saezlab/MOFAcellulaR
- **Vignette (in-source):** `MOFAcellulaR/vignettes/get-started.Rmd`
- **Paper (Ramirez-Flores et al., 2023):** https://www.biorxiv.org/content/10.1101/2023.02.23.529642v1
- **saezlab homepage:** https://saezlab.org/

---

## When not to use

- Do not use at per-cell grain. MOFAcellulaR's whole point is donor × cell-type pseudo-bulk; for per-cell use mofa-r or mofa-mofapy2.
- Do not interpret plot_sample_2D's UMAP as a factor scatter. It runs uwot::umap on Z (plot_sample_2D.R:89), discarding the linearity that makes Z interpretable in the first place.
- Do not run with n_donors << 30 without resampling stability. The n≪p regime is acute at donor grain; latent-lens stability gates apply.
- Do not use without removing the cell type with fewest cells/donors first; filt_profiles defaults need review per dataset.

---

## See also

- `mofa-framework`
- `mofa-r`
- `scrna-pipeline-conventions`

Upstream docs: https://saezlab.github.io/MOFAcellulaR/
