---
name: pymc-python
description: Use for writing, reviewing, debugging, testing, or diagnosing Python Bayesian models built directly with PyMC, including Model, coords/dims, Data, random variables, potentials, posterior sampling, prior/posterior predictive checks, and InferenceData output. Trigger on model geometry, shape errors, divergences, sampler choice, mutable prediction data, and probabilistic validation. Do not use for Bambi formula models, NumPyro/JAX programs, ArviZ-only analysis of existing draws, deterministic optimization, or general statistics without PyMC code.
argument-hint: "[PyMC model, inference, prediction, diagnostic, or error]"
---

# PyMC Python

Build an identifiable generative model with named dimensions, test it against
simulated observations, sample reproducibly, and treat diagnostics and
predictive adequacy as part of correctness.

## Boundary

Use this skill when code directly constructs or samples a `pymc.Model`. Use
Bambi for formula-driven regression, NumPyro for a native JAX probabilistic
program, and ArviZ when the job starts from completed inference results. Do not
translate between frameworks unless the user requests it.

## Know the objects

| Object | Runtime meaning | Use it for |
|---|---|---|
| `Model` | A named probabilistic graph plus coordinates, data containers, random variables, deterministics, and potentials. | Owning one coherent generative model and its namespace. |
| Coordinate / `dims` | Semantic labels for tensor axes. | Making observations, parameters, and predictions align by meaning rather than position. |
| `Data` | A named model input whose value can be replaced for prediction when shape/coordinates remain compatible. | Covariates, indices, offsets, and other conditioned inputs. |
| Random variable | A named distribution node; observed RVs define the likelihood and unobserved RVs are inferred. | Priors, latent states, and observations. |
| `Deterministic` | A named graph expression derived from model variables. | Interpretable quantities needed in results; not an independent random site. |
| `Potential` | A registered, named arbitrary contribution to the model joint log-probability; it is not a random variable. | A mathematically justified density factor, not a substitute for an observed likelihood. |
| `InferenceData` | Grouped, labeled posterior, sample statistics, observed/constant data, and predictive draws. | The durable inference artifact and ArviZ boundary. |

Distribution batch/support shape, named dimensions, and observed-data shape must
agree. A dimension label does not broadcast or transpose values for you. Read
[the model and shape contract](references/object-model.md) before repairing a
shape error, indexing hierarchical effects, or updating prediction data.

## Ordered workflow

1. State the estimand, observation unit, likelihood, link, censoring/truncation,
   missing-data policy, grouping structure, and prediction target.
2. Build coordinates from stable domain identifiers. Give every non-scalar
   variable meaningful `dims`; check data and coordinate lengths before sampling.
3. Choose likelihood from the data-generating process, not from a convenient
   distribution name. Encode exposure, trials, bounds, or measurement error.
4. Choose proper priors on the scale where they are interpretable. Simulate the
   prior predictive and reject impossible or implausible outcomes.
5. Run a small sampled-data recovery test. If known parameters cannot be
   recovered, repair the model before increasing draws.
6. Select inference from variable support and geometry. Use automatic sampling
   as a starting point, not proof that NUTS is valid for every site.
7. Sample multiple independent chains with a recorded seed, warmup, draws, and
   sampler settings; retain `InferenceData` and sample statistics.
8. Diagnose convergence and geometry, then run posterior predictive checks on
   domain-relevant discrepancies. Fix causes rather than hiding warnings.
9. For new data, update `Data` and matching coordinates under the same model
   contract; store out-of-sample draws as predictions, separate from in-sample
   posterior predictive checks.

## Decision map

| Condition | Action |
|---|---|
| Continuous differentiable latent variables with workable geometry | Start with NUTS; inspect divergences, tree depth, energy, R-hat, ESS, and traces. |
| Discrete unobserved sites | Use a compatible discrete or compound method, or marginalize/reformulate; do not force gradient-based NUTS. |
| Hierarchical scale/funnel causes divergences | Standardize predictors and test a non-centered parameterization; do not only raise `target_accept`. |
| Prior predictive is unrealistic | Repair likelihood, scale, link, or priors before posterior sampling. |
| Prediction rows differ from training rows | Update `Data` and coordinates together; preserve coefficient/category semantics. |
| Need in-sample replicated observations | Posterior predictive group. |
| Need out-of-sample predictions | Prediction data plus `predictions=True` or installed equivalent; keep a distinct predictions group. |
| Model comparison is required | Ensure pointwise log likelihood and use ArviZ with compatibility and Pareto diagnostics. |

Read [inference and predictive diagnostics](references/inference-diagnostics.md)
before changing sampler settings or claiming a fitted model is valid.

## Canonical model flow

```python
import numpy as np
import pymc as pm


def fit_logistic(x: np.ndarray, y: np.ndarray, seed: int):
    coords = {"observation": np.arange(y.size), "feature": np.arange(x.shape[1])}
    with pm.Model(coords=coords) as model:
        x_data = pm.Data("x", x, dims=("observation", "feature"))
        intercept = pm.Normal("intercept", 0, 1.5)
        beta = pm.Normal("beta", 0, 1, dims="feature")
        logit_p = pm.Deterministic("logit_p", intercept + x_data @ beta, dims="observation")
        pm.Bernoulli("outcome", logit_p=logit_p, observed=y, dims="observation")

        prior = pm.sample_prior_predictive(random_seed=seed)
        idata = pm.sample(chains=4, random_seed=seed)
        pm.sample_posterior_predictive(idata, random_seed=seed, extend_inferencedata=True)
    return model, prior, idata
```

The seed makes the run reproducible, not deterministic across every backend and
hardware combination. Keep observed binary values and predictor dimensions
validated outside the model; PyMC graph construction is not input sanitation.

## Non-negotiable rules

- Never infer axis meaning from length alone. Assert coordinates, dtypes, index
  arrays, and category coding at ingress and prediction time.
- Do not use posterior data twice: choose priors before inspecting the target
  outcomes, and evaluate on held-out or explicitly in-sample predictive tasks.
- Do not declare convergence from one chain, a trace plot alone, or R-hat alone.
  Inspect rank-normalized R-hat, bulk/tail ESS, MCSE, divergences, energy/BFMI,
  tree depth, and parameter-specific traces as applicable.
- Increasing draws reduces Monte Carlo error but does not repair divergences,
  non-identifiability, a bad likelihood, or prior-data conflict.
- A posterior predictive distribution is conditional on the fitted model; it
  does not prove causal identification or out-of-sample calibration.
- Do not use `Potential` to hide a likelihood term needed for predictive
  simulation. Potentials affect log-probability sampling but are ignored by
  prior and posterior forward sampling. If one is necessary, document its
  density and predictive consequences and test the intended behavior.
- Preserve chain and draw dimensions in `InferenceData`; never flatten chains
  before convergence diagnostics.
- Inspect the installed major before using experimental dims APIs or changing
  posterior-predictive volatility arguments.

Inspect the installed version, then use [testing and version
grounding](references/testing-version.md) for the
smallest falsifiers and installed-API checks.

## Completion gate

Do not declare completion until the likelihood and priors match the stated
generative assumptions; coordinates/dims and data shapes are asserted; prior
predictive and simulated recovery checks pass; multiple-chain diagnostics show
no unresolved critical warnings; posterior predictive checks target meaningful
features; prediction data preserves feature/category coordinates; the final
`InferenceData` contains required groups and sample statistics; and every
skipped diagnostic, backend limitation, or version uncertainty is reported.

## References

- [Model construction recipes](references/recipes-models.md)
- [Inference and prediction recipes](references/recipes-inference.md)
- [Model and shape contract](references/object-model.md)
- [Inference and predictive diagnostics](references/inference-diagnostics.md)
- [Testing and version grounding](references/testing-version.md)
