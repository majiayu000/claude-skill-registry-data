---
name: stan-coding
description: Best practices for writing efficient, clean Stan programs
---

# Stan Coding Guidelines

Use this skill when writing or modifying Stan programs to ensure clean, efficient code.

## Program Structure

Use canonical block order: `functions`, `data`, `transformed data`, `parameters`, `transformed parameters`, `model`, `generated quantities`.

Follow Stan style:
- Two-space indents, no tabs, ≤80 character lines
- Opening braces at end of line: `for (n in 1:N) {`
- Spaces around operators and after commas
- Variable names: lowercase with underscores (`sigma_y`, `mu_group`)
- Dimension constants: single uppercase letters (`N`, `K`, `J`)
- Declare locals close to use; scalars inside loops, reused containers outside

## Types and Containers

Use appropriate types:
- Linear algebra: `matrix`, `vector`, `row_vector` with matrix operations (`x * beta`)
- Indexing/containers: `array[N] real y` (not legacy `real y[N]`)
- Repeated row access: `array[M] row_vector[N] x` over `matrix[M, N]`
- Heterogeneous returns: `tuple(...)` for multiple values
- Sum-to-zero: `sum_to_zero_vector`, `sum_to_zero_matrix` instead of manual constraints

Memory layout: matrices are column-major, arrays are row-major.

## Distributions and Vectorization

Always use log form:
- Write `y ~ normal(mu, sigma)` or `target += normal_lpdf(y | mu, sigma)`
- Vectorize: `y ~ normal(mu, sigma)` for arrays, not loops
- Use GLM functions: `bernoulli_logit_glm`, `poisson_log_glm`, `normal_id_glm`
- Precompute shared expressions: compute `mu = X * beta` once, reuse
- Finite mixtures: use `log_sum_exp` on log scale

## Parameterization

Use constrained types over manual checks:
- `<lower=0>`, `<upper=...>`, `ordered`, `positive_ordered`, `simplex`, `unit_vector`
- Covariance (K≥3): `cholesky_factor_corr[K] L_Omega` with `multi_normal_cholesky`
- Sum-to-zero: use built-in types, not "last element = minus sum"

For custom transforms, use built-in `*_constrain`, `*_unconstrain`, `*_jacobian` functions.

## Parallelization

For large-N models with independent terms, use `reduce_sum`:
- Write partial sum function that takes data slice and returns log-density contribution
- Keep partial sum vectorized internally
- No side effects (no printing, no mutation)

## Functions

Modularize complex logic in `functions` block:
- Reused operations, complex math, custom likelihoods
- Signature: data arguments first, then parameters, then tuning constants
- Use `tuple` returns for multiple heterogeneous outputs

## Preventing Crashes

Both compilation and sampling can crash or OOM.

**Defensive Stan patterns:**
- Always use tight bounds: `int<lower=1, upper=K> id[N]`
- Guard math: check parameters before `log`, `sqrt`, division
- Add explicit bounds for dispersion: `real<lower=0.01> phi` (never exactly 0)

**Execution:**
- Wrap `CmdStanModel()` and `model.sample()` in try-except
- Probe with short runs before full sampling

**On crash/OOM:**
- Reduce `parallel_chains` (4 → 2 → 1)
- Reduce `max_treedepth` (10 → 8)
- Subsample data or simplify model

## ArviZ Integration

Design Stan programs for downstream ArviZ workflow:

**Generated quantities:**
- Always include pointwise log-likelihood: `vector[N] log_lik` - required for model comparison and downstream workflow
- Always include posterior predictive draws: `vector[N] y_rep` - required for all predictive checks
- For multiple observed variables, use one vector per variable: `log_lik_y1`, `log_lik_y2`
- This will incur modest overhead, but might be worth workflow simplicity

**Transformed parameters:**
- Put reusable intermediate quantities here (e.g., `vector[N] mu = alpha + X * beta`)
- Avoids recomputation in Python and makes them available in posterior samples

**Extending without refitting:**
- To add new derived quantities, use `generate_quantities` mode with original posterior draws
- Write new Stan file with same data/parameters/transformed parameters but extended generated quantities
- Call `model.generate_quantities(data=data, mcmc_sample=fit)` - orders of magnitude faster than refitting

**Save and cache:**
- Convert to InferenceData: `az.from_cmdstanpy(fit, log_likelihood="log_lik", posterior_predictive=["y_rep"])`
- Save as NetCDF: `idata.to_netcdf("posterior.nc")` - makes all downstream analysis instant
- Use consistent coords/dims for all models in the workflow

## Known Issues

- **CmdStanPy `diagnose()` OOMs** on large data (N > 10K). Use `check_convergence()` from `shared_utils` instead.
- **ArviZ column names** are lowercase (`r_hat`, `ess_bulk`). CmdStanPy uses uppercase (`R_hat`, `ESS_bulk`).
- **Stan CSV columns** use dots: `beta.1` not `beta[1]`.

## References

If stuck on Stan patterns or ArviZ usage, search these resources:
- Stan case studies: https://mc-stan.org/learn-stan/case-studies.html
- ArviZ API documentation: https://python.arviz.org/en/latest/api/index.html

Use WebSearch or WebFetch to find specific examples.
