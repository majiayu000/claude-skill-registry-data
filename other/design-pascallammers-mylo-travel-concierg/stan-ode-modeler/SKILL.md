---
name: stan-ode-modeler
description: Guidelines for Stan models with ODE-based dynamics using modern interfaces
---

# Stan ODE Modeler

Use this skill when writing Stan models where latent dynamics are defined by ODEs: epidemic models (SIR/SEIR), PK/PD compartment models, population dynamics, biochemical reactions, growth models.

Uses Stan 2.24+ modern ODE interface (`ode_rk45`, `ode_bdf`, `ode_adams`, adjoint solvers), not legacy `integrate_ode_*`.

## Workflow

1. **Extract generative model**: Identify state variables x(t), parameters θ, ODE system dx/dt = f(t,x,θ), observation model, data structure
2. **Choose solver** (see below)
3. **Write complete Stan program**: functions (ODE RHS), data, parameters, transformed parameters (solve ODE), model (priors + likelihood), generated quantities (predictions)
4. **Scale appropriately**: Non-dimensionalize time and states to O(1) scales, use log/logit transforms for constraints
5. **Use stan-coding skill** for general Stan structure, parameterization, and ArviZ integration

## Modern ODE Interface

**Function signature:**
```stan
functions {
  vector ode_rhs(real t, vector y, array[] real theta, array[] real x_r, array[] int x_i) {
    vector[N] dydt;
    // fill dydt based on y and theta
    return dydt;
  }
}
```

**Solver calls:**
- `ode_rk45(ode_rhs, y0, t0, ts, theta, x_r, x_i)` - non-stiff (default)
- `ode_bdf(ode_rhs, y0, t0, ts, theta, x_r, x_i)` - stiff systems
- `ode_adams(ode_rhs, y0, t0, ts, theta, x_r, x_i)` - smooth, long horizons
- `ode_adjoint_*` - many parameters relative to state dimension

Add `_tol` suffix for configurable tolerances: `ode_rk45_tol(..., rel_tol, abs_tol, max_num_steps, ...)`

Returns: `array[T] vector[N]` where T = length(ts), N = state dimension

## Program Structure

**Transformed parameters** (when ODE enters likelihood):
```stan
transformed parameters {
  array[T] vector[N] x_hat;
  array[] real theta = {beta, gamma};  // pack parameters
  x_hat = ode_rk45(ode_rhs, y0, t0, ts, theta, {}, {});
}
```

**Generated quantities** (predictions, forecasts):
Include y_rep and log_lik following stan-coding skill guidelines.

## Example: SIR Model

```stan
functions {
  vector sir_rhs(real t, vector y, array[] real theta, array[] real x_r, array[] int x_i) {
    vector[3] dydt;
    real beta = theta[1];
    real gamma = theta[2];
    real N_pop = x_r[1];

    dydt[1] = -beta * y[1] * y[2] / N_pop;  // dS/dt
    dydt[2] = beta * y[1] * y[2] / N_pop - gamma * y[2];  // dI/dt
    dydt[3] = gamma * y[2];  // dR/dt
    return dydt;
  }
}

transformed parameters {
  array[T] vector[3] x_hat;
  x_hat = ode_rk45(sir_rhs, y0, t0, ts, {beta, gamma}, {N_pop}, {});
}

model {
  beta ~ lognormal(0, 1);
  gamma ~ lognormal(0, 1);
  for (t in 1:T) {
    I_obs[t] ~ poisson(x_hat[t, 2]);  // observe infected count
  }
}
```

## Hierarchical ODE Models

For multiple subjects with subject-specific ODE parameters:
- Use population hyperparameters (mean, sd) in parameters block
- Draw subject-level parameters with non-centered parameterization
- Loop over subjects, solve ODE once per subject
- Use log-transforms for positive parameters: `r[n] = exp(mu_log_r + sigma_log_r * z_r[n])`

## Solver Selection

**Default**: `ode_rk45` with `rel_tol ≈ 1e-6`, `abs_tol ≈ (typical state scale) × 1e-6`, `max_num_steps ≈ 1e4-1e5`

**Switch to `ode_bdf` if**:
- "max_num_steps exceeded" warnings
- Fast/slow components (multi-compartment PK, stiff reactions)
- Rapid changes in some states while others change slowly

**Use `ode_adams` if**: Smooth, non-stiff systems over long time horizons

**Use `ode_adjoint_*` if**: Many parameters relative to state dimension (hierarchical models with per-subject parameters)

**Tolerances**: ODE error should be much smaller than observation noise. Rarely need `rel_tol < 1e-8`. Can relax slightly (1e-6 → 1e-5) if HMC is slow but stable.

## Debugging Common Issues

**Max steps exceeded**:
- Rescale time and states to O(1)
- Switch to `ode_bdf` if stiff
- Increase `max_num_steps` as last resort

**Divergences**:
- Use log-transforms for positive parameters
- Use convergence-diagnostics skill for HMC-specific issues
- Strengthen priors to avoid extreme parameter values

**Performance**:
- Use observation times only, not fine grids
- Consider `reduce_sum` parallelization for multi-subject models
- Ensure proper scaling (time and states near 1)

## References

For ODE model examples and patterns, search:
- Stan case studies: https://mc-stan.org/learn-stan/case-studies.html (search for PK/PD, epidemiology, ODE examples)
- Stan ODE documentation: https://mc-stan.org/docs/functions-reference/functions-ode-solver.html

Use WebSearch or WebFetch to find domain-specific ODE modeling examples.
