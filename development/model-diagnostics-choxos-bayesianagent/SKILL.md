---
name: model-diagnostics
description: MCMC diagnostics for Bayesian models including convergence assessment, effective sample size, divergences, and posterior predictive checks.
---

# Model Diagnostics

## Key Convergence Metrics

| Metric | Good Value | Concern |
|--------|------------|---------|
| Rhat | < 1.01 | > 1.1 indicates non-convergence |
| ESS bulk | > 400 | < 100 unreliable estimates |
| ESS tail | > 400 | < 100 unreliable intervals |
| Divergences | 0 | Any indicates geometry issues |
| Max treedepth | 0 hits | Hitting limit = slow exploration |

## Stan Diagnostics (cmdstanr)

```r
library(cmdstanr)

fit <- mod$sample(data = stan_data, ...)

# Quick check
fit$cmdstan_diagnose()

# Summary with diagnostics
fit$summary()

# Detailed diagnostics
fit$diagnostic_summary()

# Extract specific metrics
draws <- fit$draws()
rhat <- posterior::rhat(draws)
ess_bulk <- posterior::ess_bulk(draws)
ess_tail <- posterior::ess_tail(draws)

# Divergences
np <- fit$sampler_diagnostics()
sum(np[,,"divergent__"])

# Treedepth
sum(np[,,"treedepth__"] == 10)  # Default max
```

## JAGS Diagnostics (R2jags)

```r
library(R2jags)
library(coda)

fit <- jags(...)

# Summary (includes Rhat, n.eff)
print(fit)
fit$BUGSoutput$summary

# Rhat
max(fit$BUGSoutput$summary[,"Rhat"])

# Effective sample size
min(fit$BUGSoutput$summary[,"n.eff"])

# Convert to coda
mcmc_obj <- as.mcmc(fit)

# Gelman-Rubin
gelman.diag(mcmc_obj)

# Autocorrelation
autocorr.diag(mcmc_obj)
autocorr.plot(mcmc_obj)

# Geweke diagnostic
geweke.diag(mcmc_obj)
```

## Visual Diagnostics

### Trace Plots
```r
# Stan (bayesplot)
library(bayesplot)
mcmc_trace(fit$draws(), pars = c("mu", "sigma"))

# JAGS
traceplot(fit)
```

### Rank Histograms
```r
# Should be uniform if chains mixed well
mcmc_rank_hist(fit$draws(), pars = "mu")
```

### Pairs Plot (Detect Correlations)
```r
mcmc_pairs(fit$draws(), pars = c("mu", "sigma", "tau"))
```

## Divergence Diagnosis (Stan)

```r
# Identify divergent transitions
np <- nuts_params(fit)
divergent <- np[np$Parameter == "divergent__" & np$Value == 1, ]

# Pairs plot highlighting divergences
mcmc_pairs(fit$draws(), np = np,
           pars = c("mu", "tau"),
           off_diag_args = list(size = 0.5))

# Common fixes:
# 1. Increase adapt_delta
fit <- mod$sample(data = stan_data, adapt_delta = 0.95)

# 2. Use non-centered parameterization
# 3. Reparameterize (use Cholesky for covariances)
```

## Effective Sample Size

```r
# Rule of thumb: ESS > 10 * num_chains for reliable Rhat
# ESS > 100 for reasonable posterior estimates
# ESS > 400 for reliable tail quantiles

# If low ESS:
# 1. Run longer chains
# 2. Thin the samples (last resort)
# 3. Improve parameterization
# 4. Use more informative priors
```

## Posterior Predictive Checks

### Stan (generated quantities)
```stan
generated quantities {
  array[N] real y_rep;
  for (n in 1:N)
    y_rep[n] = normal_rng(mu[n], sigma);
}
```

### R Visualization
```r
library(bayesplot)

# Density overlay
y_rep <- fit$draws("y_rep", format = "matrix")
ppc_dens_overlay(y, y_rep[1:50, ])

# Intervals
ppc_intervals(y, y_rep)

# Statistics
ppc_stat(y, y_rep, stat = "mean")
ppc_stat(y, y_rep, stat = "sd")
ppc_stat(y, y_rep, stat = function(x) max(x) - min(x))
```

## Model Comparison

### LOO-CV (Stan)
```r
library(loo)

# Add log_lik to generated quantities
loo1 <- fit1$loo()
loo2 <- fit2$loo()

# Compare
loo_compare(loo1, loo2)

# Check Pareto k diagnostics
plot(loo1)
```

### WAIC
```r
waic1 <- waic(log_lik1)
waic2 <- waic(log_lik2)
loo_compare(waic1, waic2)
```

### DIC (JAGS)
```r
fit$BUGSoutput$DIC
fit$BUGSoutput$pD  # Effective number of parameters
```

## Troubleshooting Guide

| Problem | Symptoms | Solutions |
|---------|----------|-----------|
| Non-convergence | Rhat > 1.1 | Longer warmup, better inits |
| Divergences | divergent__ > 0 | Non-centered param, higher adapt_delta |
| Low ESS | ESS < 100 | Longer chains, better param |
| Slow mixing | High autocorrelation | Reparameterize, QR decomposition |
| Hitting max_treedepth | treedepth == max | Increase max_treedepth |

## Quick Diagnostic Checklist

```r
check_diagnostics <- function(fit) {
  cat("=== MCMC Diagnostics ===\n")

  # For Stan
  if (inherits(fit, "CmdStanMCMC")) {
    summ <- fit$summary()
    diag <- fit$diagnostic_summary()

    cat("Max Rhat:", max(summ$rhat, na.rm=TRUE),
        ifelse(max(summ$rhat, na.rm=TRUE) < 1.01, "✓", "✗"), "\n")
    cat("Min ESS bulk:", min(summ$ess_bulk, na.rm=TRUE),
        ifelse(min(summ$ess_bulk, na.rm=TRUE) > 400, "✓", "✗"), "\n")
    cat("Divergences:", sum(diag$num_divergent),
        ifelse(sum(diag$num_divergent) == 0, "✓", "✗"), "\n")
    cat("Max treedepth:", sum(diag$num_max_treedepth),
        ifelse(sum(diag$num_max_treedepth) == 0, "✓", "✗"), "\n")
  }

  # For JAGS
  if (inherits(fit, "rjags")) {
    summ <- fit$BUGSoutput$summary
    cat("Max Rhat:", max(summ[,"Rhat"], na.rm=TRUE),
        ifelse(max(summ[,"Rhat"], na.rm=TRUE) < 1.1, "✓", "✗"), "\n")
    cat("Min n.eff:", min(summ[,"n.eff"], na.rm=TRUE),
        ifelse(min(summ[,"n.eff"], na.rm=TRUE) > 100, "✓", "✗"), "\n")
    cat("DIC:", fit$BUGSoutput$DIC, "\n")
  }
}
```
