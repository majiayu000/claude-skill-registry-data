---
name: bambi-python
description: Use for writing, reviewing, debugging, testing, or diagnosing Bayesian regression and hierarchical models built with Bambi formulas, Model, Family/Likelihood/Link, Prior, fit, prior predictive, and predict. Trigger on common versus group-specific terms, categorical coding, family/link choice, automatic prior scaling, missing rows, PyMC backend settings, and InferenceData predictions. Do not use for hand-built PyMC graphs, NumPyro programs, ArviZ-only analysis of existing draws, frequentist statsmodels formulas, or generic pandas work.
argument-hint: "[Bambi formula, family, priors, fit, hierarchy, or prediction]"
---

# Bambi Python

Translate a statistical estimand into an explicit formula, likelihood family,
link, contrast/group structure, and prior contract; inspect the built model;
then validate inference and predictions rather than treating `.fit()` as done.

## Boundary

Use Bambi when formula-driven Bayesian regression or multilevel modeling is the
primary job. Use PyMC for a custom probability graph that cannot be expressed
cleanly through Bambi, and ArviZ for analysis that starts from an existing
`InferenceData`. Bambi uses a PyMC backend, but backend implementation details
must not silently replace the formula-level contract.

## Know the objects

| Object | Meaning | Use it for |
|---|---|---|
| Formula | Response plus common and group-specific linear predictor terms; optional additional formulas target other distribution parameters. | Declaring estimands and hierarchical structure. |
| Term | A transformed predictor, interaction, intercept, or group-specific coefficient produced by formula parsing. | Understanding the actual design matrix and coefficient interpretation. |
| `Family` | Likelihood plus link(s) connecting distribution parameters to predictors. | Matching outcome support and data-generating process. |
| `Prior` | Distribution specification for a term or auxiliary parameter, optionally nested/hierarchical. | Encoding domain scale and regularization. |
| `Model` | Formula, data, family, priors, design matrices, settings, and compiled PyMC backend. | Building, fitting, and predicting one coherent regression. |
| Backend model | The generated PyMC model after `build()`. | Low-level inspection and supported sampler/backend configuration. |
| `InferenceData` | Labeled posterior, sample statistics, log likelihood, observed data, and predictive groups returned/extended by fitting and prediction. | Diagnostics, persistence, and ArviZ handoff. |

Common effects estimate population-level coefficients. Group-specific terms such
as `(1 + x | group)` estimate varying intercepts/slopes with partial pooling; the
vertical bar is not a bitwise operation or ordinary interaction. Read [the
formula and model contract](references/object-model.md) before changing term
syntax, coding, or hierarchy.

## Ordered workflow

1. State the outcome support, observation unit, estimand, likelihood, link,
   exposure/trials, repeated/group structure, missing-data policy, and prediction
   population.
2. Validate the pandas data before model construction: response support,
   category levels/order, group IDs, numeric units, missing rows, and one row per
   declared observation unit.
3. Write the smallest formula that represents the estimand. Add interactions,
   splines/transforms, offsets, and group-specific terms only under explicit
   scientific meaning.
4. Choose `Family` and link from the sampling process, not from the outcome's
   Python dtype. Include auxiliary/distributional formulas when dispersion or
   another parameter genuinely varies.
5. Inspect the printed/built model, design terms, family/link, observations
   retained, categorical reference levels, priors, and parameter names.
6. Replace consequential automatic priors with explicit domain-scale priors.
   Run prior predictive simulation before fitting.
7. Fit with recorded backend, chains, warmup, draws, seed, and sampler settings.
   Diagnose the returned `InferenceData` using PyMC/ArviZ evidence.
8. Run posterior predictive checks. For new data, preserve formula columns,
   factor levels, transforms, and group policy; store predictions separately.

## Decision map

| Condition | Action |
|---|---|
| Continuous approximately symmetric outcome | Gaussian may be a candidate; verify tails, bounds, and variance behavior. |
| Binary outcome | Bernoulli family with a justified link; validate values and event unit. |
| Counts | Poisson only if mean/variance and zero behavior fit; otherwise test overdispersion/zero structure with a supported family/model. |
| Binomial successes out of trials | Supply the binomial trial contract; do not model counts as unconstrained Poisson by habit. |
| Repeated observations by group | Add group-specific intercept/slopes required by dependence and estimand. |
| Few observations per group or funnel diagnostics | Prefer/test non-centered group effects; do not eliminate pooling. |
| Prior scale has domain meaning | Set explicit `Prior`; do not rely on automatic scaling invisibly. |
| New data contains unseen group levels | Apply an explicit supported new-group policy and uncertainty interpretation; never silently map to an existing group. |
| Custom latent graph exceeds formula/family system | Drop to a hand-built PyMC model and use that skill. |

Read [families, priors, and inference](references/inference-priors.md) before
accepting defaults or changing the backend.

## Canonical hierarchical anchor

```python
import arviz as az
import bambi as bmb
import pandas as pd


def fit_reaction(data: pd.DataFrame, seed: int):
    required = {"reaction", "days", "subject"}
    if missing := required.difference(data.columns):
        raise ValueError(f"missing columns: {sorted(missing)}")
    if data[list(required)].isna().any().any():
        raise ValueError("missing model values require an explicit policy")

    priors = {
        "days": bmb.Prior("Normal", mu=0, sigma=5),
        "1|subject": bmb.Prior("Normal", mu=0, sigma=bmb.Prior("HalfNormal", sigma=10)),
    }
    model = bmb.Model(
        "reaction ~ 1 + days + (1 + days | subject)",
        data,
        family="gaussian",
        priors=priors,
        dropna=False,
    )
    model.build()
    prior = model.prior_predictive(random_seed=seed)
    idata = model.fit(chains=4, random_seed=seed)
    summary = az.summary(idata)
    return model, prior, idata, summary
```

Prior names and signatures drift; inspect the built model in the installed
Bambi version. The chosen numeric scales are examples, not domain defaults.

## Non-negotiable rules

- Do not let Bambi drop rows silently. Reject missing model columns or opt into
  listwise deletion and report the exact retained observation set.
- Formula syntax does not validate causal identification. Confounding,
  post-treatment variables, selection, and measurement error require a model
  justified outside the formula parser.
- Inspect intercept inclusion, categorical reference levels, interactions, and
  group terms. Coefficient meaning changes with coding and predictor centering.
- Automatic prior scaling is a convenience, not a domain prior. Record whether
  `auto_scale` and predictor centering are active and inspect resulting priors.
- A group-specific term requires a meaningful population of groups. Do not use
  fixed dummy effects merely to avoid partial pooling, and do not add random
  slopes unsupported by data without diagnosing geometry.
- `.fit()` returning is not acceptance. Inspect divergences, R-hat, ESS, MCSE,
  traces, prior/posterior predictive checks, and parameterization.
- Predictions on new data must reuse training transforms and category coding.
  State whether they include observation noise and group-specific effects.
- Model comparison requires compatible observations and pointwise log
  likelihood; use ArviZ and inspect Pareto diagnostics.

Use [testing and version grounding](references/testing-version.md) to inspect
the installed formula, fit, predict, and backend contracts.

## Completion gate

Do not declare completion until the formula matches the estimand; response
family/link and auxiliary parameters match support; retained rows and category/
group encodings are explicit; built terms and priors are inspected; prior
predictive and simulated recovery checks pass; inference has no unresolved
critical diagnostics; posterior predictive checks target domain behavior; new-
data prediction semantics and unseen groups are tested; `InferenceData` groups
and coordinates are correct; and skipped checks or version uncertainty are
reported.

## References

- [Formula and model contract](references/object-model.md)
- [Families, priors, and inference](references/inference-priors.md)
- [Testing and version grounding](references/testing-version.md)
