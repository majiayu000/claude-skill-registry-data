---
name: visual-predictive-checks
description: Guidelines for visual predictive checks following Säilynoja et al. recommendations using ArviZ
---

# Visual Predictive Checks

Use this skill when running prior or posterior predictive checks to validate Bayesian models. These checks compare simulated data from the model to observed data (or plausible ranges for prior predictive checks).

## ArviZ Workflow

1. Fit model with CmdStanPy, generating predictive quantities in `generated quantities` block (e.g., `y_rep` for posterior predictive, `y_prior_pred` for prior predictive)
2. Convert to ArviZ DataTree using `arviz_base.from_cmdstanpy`, specifying predictive groups
3. Create visual checks using `arviz_plots` functions

## Visual Checks by Data Type

### Continuous Data
- **Distribution**: `plot_ppc_dist` with `kind="ecdf"` and `kind="kde"`
- **PIT ECDF**: `plot_ppc_pit` - shows calibration with simultaneous bands
- **Coverage**: `plot_ppc_pit(coverage=True)` - equal-tailed interval coverage
- **Summary statistics**: `plot_ppc_tstat` for median, MAD, IQR combined with `combine_plots`
- **LOO-PIT**: `plot_loo_pit` - avoids double-dipping by using leave-one-out

### Count Data
- **Rootogram**: `plot_ppc_rootogram` - emphasizes discreteness and dispersion
- **Histogram**: `plot_ppc_dist(kind="hist")`
- **PIT ECDF** and **coverage**: Same as continuous

### Binary/Categorical/Ordinal Data
- **Calibration**: `plot_ppc_pava` - PAV-adjusted calibration curves
- **Intervals**: `plot_ppc_interval` - posterior predictive intervals with observed overlay
- **PIT ECDF** and **coverage**: Same as continuous

### Censored/Survival Data
- **Survival curves**: `plot_ppc_censored` - Kaplan-Meier style PPC
- **PIT ECDF** and **coverage**: Same as continuous

## Key Principles

Use multiple complementary views rather than relying on a single plot. For example, for continuous outcomes, combine ECDF (shows full distribution) with PIT ECDF (shows calibration) and t-stat PPCs (shows specific features like central tendency and spread).

LOO-PIT is preferred over regular PIT for posterior checks as it approximates leave-one-out predictive distribution and avoids overfitting concerns.

Name plots descriptively: `prior_predictive_ecdf.png`, `loo_pit_calibration.png`, `posterior_rootogram.png`.
