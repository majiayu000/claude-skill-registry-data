---
name: pymc-fundamentals
description: Foundational knowledge for writing PyMC 5 models including syntax, distributions, sampling, and ArviZ diagnostics. Use when creating or reviewing PyMC models.
---

# PyMC 5 Fundamentals

## When to Use This Skill

- Writing new PyMC models in Python
- Understanding PyMC syntax and API
- Converting models from Stan/JAGS to PyMC
- Diagnosing sampling issues with ArviZ

## Model Structure

```python
import pymc as pm
import numpy as np
import arviz as az

with pm.Model() as model:
    # 1. Priors
    mu = pm.Normal("mu", mu=0, sigma=10)
    sigma = pm.HalfNormal("sigma", sigma=1)

    # 2. Likelihood
    y_obs = pm.Normal("y_obs", mu=mu, sigma=sigma, observed=y_data)

    # 3. Sample
    trace = pm.sample(1000, tune=1000, return_inferencedata=True)

# 4. Diagnostics
az.summary(trace)
```

## CRITICAL: SD Parameterization

**PyMC uses SD (like Stan), NOT precision (like BUGS):**

```python
# PyMC (SD)
pm.Normal("x", mu=0, sigma=1)      # sigma is SD

# BUGS equivalent would be tau = 1/sigma² = 1
```

## Distribution Quick Reference

### Continuous
```python
pm.Normal("x", mu=0, sigma=1)           # Normal
pm.HalfNormal("x", sigma=1)             # Half-normal (>0)
pm.HalfCauchy("x", beta=2.5)            # Half-Cauchy (>0)
pm.Exponential("x", lam=1)              # Exponential
pm.Uniform("x", lower=0, upper=1)       # Uniform
pm.Beta("x", alpha=1, beta=1)           # Beta
pm.Gamma("x", alpha=2, beta=1)          # Gamma
pm.StudentT("x", nu=3, mu=0, sigma=1)   # Student-t
pm.LogNormal("x", mu=0, sigma=1)        # Log-normal
pm.TruncatedNormal("x", mu=0, sigma=1, lower=0)  # Truncated
```

### Discrete
```python
pm.Bernoulli("x", p=0.5)                # Bernoulli
pm.Binomial("x", n=10, p=0.5)           # Binomial
pm.Poisson("x", mu=5)                   # Poisson
pm.NegativeBinomial("x", mu=5, alpha=1) # Negative binomial
pm.Categorical("x", p=[0.3, 0.5, 0.2])  # Categorical
```

### Multivariate
```python
pm.MvNormal("x", mu=np.zeros(K), cov=np.eye(K))
pm.Dirichlet("x", a=np.ones(K))
pm.LKJCholeskyCov("chol", n=K, eta=2, sd_dist=pm.Exponential.dist(1))
```

## Sampling

```python
# Standard NUTS
trace = pm.sample(
    draws=1000,          # Samples per chain
    tune=1000,           # Warmup
    chains=4,
    cores=4,
    target_accept=0.8,   # Increase for divergences
    random_seed=42,
    return_inferencedata=True
)

# Variational inference (fast)
approx = pm.fit(n=30000, method="advi")
trace = approx.sample(1000)

# Predictive sampling
prior_pred = pm.sample_prior_predictive(500)
post_pred = pm.sample_posterior_predictive(trace)
```

## Bayesian Workflow (Statistical Rethinking)

### 1. Prior Predictive Check
```python
with model:
    prior_pred = pm.sample_prior_predictive(500, random_seed=42)
az.plot_ppc(prior_pred, group="prior")
```

### 2. Fit Model
```python
with model:
    trace = pm.sample(1000, tune=1000, target_accept=0.9,
                      return_inferencedata=True)
```

### 3. Diagnostics
```python
az.summary(trace, hdi_prob=0.89)
az.plot_trace(trace)
az.plot_rank_hist(trace)  # Ranked histograms (preferred)
```

### 4. Posterior Predictive Check
```python
with model:
    post_pred = pm.sample_posterior_predictive(trace)
az.plot_ppc(post_pred, num_pp_samples=100)
```

### 5. Model Comparison
```python
loo1 = az.loo(trace1)
loo2 = az.loo(trace2)
az.compare({"m1": trace1, "m2": trace2})
az.plot_khat(loo1)  # k > 0.7 is problematic
```

## pm.Deterministic for Tracking

**Always track mu for plotting:**

```python
# Inside model
mu = pm.Deterministic("mu", alpha + pm.math.dot(X, beta))

# Access later
trace.posterior["mu"]  # All samples of mu
```

## Data Extraction Patterns

```python
# Extract to DataFrame
trace_df = az.extract_dataset(trace).to_dataframe()

# Access specific parameters
post = az.extract_dataset(trace["posterior"])
mu_samples = post["mu"].values

# Get numpy arrays
alpha_values = trace.posterior["alpha"].values  # (chains, draws)
```

## HDI Visualization

```python
# Compute mu at new x values
x_seq = np.linspace(x.min(), x.max(), 100)
mu_pred = post["alpha"] + post["beta"] * x_seq[:, None]

# Plot HDI bands
az.plot_hdi(x_seq, mu_pred.T, hdi_prob=0.89)
plt.scatter(x, y)
```

## ArviZ Diagnostics

```python
import arviz as az

# Configure defaults
az.rcParams["stats.hdi_prob"] = 0.89

# Summary table
summary = az.summary(trace, hdi_prob=0.89)

# Key metrics
max_rhat = summary["r_hat"].max()       # Should be < 1.01
min_ess = summary["ess_bulk"].min()     # Should be > 400

# Plots
az.plot_trace(trace)                    # Trace plots
az.plot_rank_hist(trace)                # Ranked histograms (preferred!)
az.plot_posterior(trace)                # Posteriors
az.plot_forest(trace)                   # Forest plot
az.plot_pair(trace)                     # Pairs plot

# Model comparison
az.loo(trace)                           # LOO-CV
az.waic(trace)                          # WAIC
az.compare({"m1": trace1, "m2": trace2})
```

## Diagnostic Checklist

- [ ] Rhat < 1.01 for all parameters
- [ ] ESS_bulk > 400
- [ ] ESS_tail > 400
- [ ] Prior predictive produces sensible values
- [ ] Posterior predictive matches data pattern
- [ ] Pareto k < 0.7 for LOO

## Non-Centered Parameterization

For hierarchical models:

```python
# Centered (may have divergences)
theta = pm.Normal("theta", mu=mu, sigma=tau, shape=J)

# Non-centered (recommended)
theta_raw = pm.Normal("theta_raw", mu=0, sigma=1, shape=J)
theta = pm.Deterministic("theta", mu + tau * theta_raw)
```

## PyTensor Math Operations

Inside `with pm.Model()`, use `pm.math` not `np`:

```python
# Correct
mu = pm.math.dot(X, beta)
p = pm.math.sigmoid(eta)
log_x = pm.math.log(x)

# Wrong (will fail)
mu = np.dot(X, beta)  # Don't use numpy inside model
```

## Common Priors

```python
# Intercept
alpha = pm.Normal("alpha", mu=0, sigma=10)

# Coefficients
beta = pm.Normal("beta", mu=0, sigma=2.5, shape=K)

# Scale (SD)
sigma = pm.HalfNormal("sigma", sigma=1)
sigma = pm.HalfCauchy("sigma", beta=2.5)
sigma = pm.Exponential("sigma", lam=1)

# Hierarchical SD
tau = pm.HalfCauchy("tau", beta=2.5)

# Correlation matrix
chol, corr, stds = pm.LKJCholeskyCov("chol", n=K, eta=2,
                                      sd_dist=pm.Exponential.dist(1))
```

## Key Differences from Stan

| Feature | PyMC | Stan |
|---------|------|------|
| Syntax | Python | DSL |
| Arrays | `shape=K` | `array[K]` |
| Math | `pm.math.dot()` | `*` operator |
| Blocks | Single context | 7 blocks |
| Output | InferenceData | CmdStanMCMC |

## Troubleshooting

| Issue | Solution |
|-------|----------|
| Divergences | Increase `target_accept` to 0.9-0.99 |
| Low ESS | Run longer chains, reparameterize |
| Shape errors | Check `shape=` parameter |
| Slow | Use ADVI for quick approximation |
| Memory | Reduce chains or use mini-batch |
