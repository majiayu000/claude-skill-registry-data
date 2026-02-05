---
name: convergence-diagnostics
description: MCMC convergence diagnostics using CmdStanPy and ArviZ
---

# Convergence Diagnostics

Use this skill when checking MCMC convergence after fitting Stan models. Convergence means chains mixed and explored the same target, and you have enough effective draws.

## CmdStanPy Diagnostics

After fitting with CmdStanPy, run:
- `fit.summary()`: Returns DataFrame with R-hat, ESS_bulk, ESS_tail, MCSE per parameter
- `fit.diagnose()`: Checks for divergences, max treedepth, low E-BFMI, low ESS, high R-hat

If `diagnose()` reports no problems, you still need visual checks via ArviZ.

## ArviZ Workflow

Convert to InferenceData:
```python
idata = az.from_cmdstanpy(
    fit,
    log_likelihood="log_lik",
    observed_data={"y": y_obs}
)
```

Run numerical diagnostics:
- `az.rhat(idata)`: Rank-normalized split R-hat
- `az.ess(idata)`: Bulk and tail effective sample size
- `az.bfmi(idata)`: Bayesian fraction of missing information
- `az.mcse(idata)`: Monte Carlo standard error
- `az.summary(idata)`: All diagnostics in one table

## Thresholds

Must achieve:
- **R̂ < 1.01** (all parameters) - measures chain agreement
- **ESS bulk and tail ≥ 400** per parameter - enough effective draws
- **BFMI ≥ 0.3** per chain - adequate energy exploration
- **MCSE << posterior SD** - Monte Carlo error small relative to uncertainty
- **No divergent transitions** after warmup

## Visual Diagnostics

**Chain mixing and stationarity:**
- `az.plot_trace()`: Should show "fat fuzzy caterpillars", no trends or stuck chains. Divergences shown as vertical lines.
- `az.plot_rank()`: Rank histograms should be uniform and similar across chains. U-shapes or skew indicate poor mixing.

**Autocorrelation and ESS:**
- `az.plot_autocorr()`: Slow decay indicates high correlation and low ESS
- `az.plot_ess(kind="evolution")`: ESS growth over draws - should keep climbing
- `az.plot_ess(kind="local")`: ESS in local windows/quantiles - checks tail exploration

**HMC-specific pathologies:**
- `az.plot_energy()`: Overlays energy transitions vs marginal energy. Low BFMI shows mismatch.
- `az.plot_pair(divergences=True)`: Localizes divergences in parameter space (funnels, tight correlations)
- `az.plot_parallel()`: Parallel coordinates showing divergent vs non-divergent draws

## Common Issues

- **Divergences + low BFMI**: Geometry problems (funnels, stiff regions). Reparameterize or increase adapt_delta.
- **High R̂, good visuals**: Chains haven't run long enough. Extend iterations.
- **Low ESS, good R̂**: High autocorrelation. Reparameterize or run longer.
- **Max treedepth warnings**: Strong correlations. Reparameterize or simplify model.
- **Multimodality in plot_posterior**: Identification problem or multiple modes.

Remember: You never prove convergence, only build a strong circumstantial case. The sampler tells you about your model - listen to it.
