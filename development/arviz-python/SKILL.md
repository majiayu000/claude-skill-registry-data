---
name: arviz-python
description: Use for writing, reviewing, debugging, or testing Python analysis of Bayesian inference results with ArviZ, including 1.x DataTree groups, legacy InferenceData inputs, xarray dimensions and coordinates, conversion, summaries, R-hat/ESS/MCSE diagnostics, posterior predictive checks, PSIS-LOO, Pareto-k, and model comparison. Trigger on chain/draw shape errors, mislabeled groups, flattened samples, missing log likelihood, or misleading diagnostic claims. Do not use to construct or sample PyMC, NumPyro, or Bambi models, for generic plotting, or for deterministic statistics without Bayesian draws.
argument-hint: "[ArviZ DataTree/InferenceData, diagnostics, predictive check, or comparison]"
---

# ArviZ Python

Turn posterior artifacts into correctly labeled inference data, preserve chain
and draw structure, diagnose sampling and prediction, and compare only models
whose observations and log-likelihood semantics are compatible.

## Boundary

Use this skill when the input is completed or partially completed Bayesian
draws and the code directly uses ArviZ. Use the modeling framework's skill to
build or sample a model. A plot request alone does not trigger this skill unless
the plot represents posterior, diagnostic, predictive, or comparison results.

## Know the objects

| Object | Meaning | Use it for |
|---|---|---|
| ArviZ 1.x `DataTree` / accepted idata-like container | Named inference groups, each holding labeled xarray variables. Legacy integrations may still call the artifact `InferenceData`. | The durable boundary for posterior analysis. |
| Group | A semantic dataset such as `posterior`, `sample_stats`, `log_likelihood`, `posterior_predictive`, `predictions`, `observed_data`, or `constant_data`. | Keeping quantities with different meaning separate. |
| Variable | A named tensor with dimensions and coordinates. | One parameter, statistic, observation, or prediction. |
| `chain` | Independent MCMC run dimension. | Between-chain convergence diagnostics. |
| `draw` | Iteration within a chain. | Within-chain sample sequence. |
| Model-comparison result | Pointwise predictive score summaries, uncertainty, diagnostics, and weights. | Comparing compatible predictive models, not proving truth. |

Dimension names determine semantics; axis order is secondary. Sample dimensions
must not be confused with event/data dimensions. `observed_data` has no chain or
draw axis; posterior predictive values normally have both plus observation
dimensions. Read [the inference-data contract](references/object-model.md) before
converting arrays, concatenating results, or selecting coordinates.

## Ordered workflow

1. Establish provenance: model, sampler/guide, package versions, warmup policy,
   number of chains/draws, seed, observation identity, and log-likelihood target.
2. Inspect available groups, variables, dimensions, coordinates, dtypes, and
   missing values before computing a statistic. On ArviZ 1.x, treat the
   `DataTree` children as the group registry instead of assuming 0.x
   `InferenceData` attribute behavior.
3. Convert raw arrays with explicit group, variable, dims, and coords mappings.
   Preserve chain and draw separately; reject ambiguous flattened samples.
4. Select variables/coordinates intentionally. Exclude warmup or transformed
   helper variables only under a recorded policy.
5. Diagnose sampling using multiple complementary measures and plots. Report
   problematic variables and coordinates, not only a global maximum.
6. Check posterior predictive adequacy with discrepancies tied to the modeling
   objective and distinguish in-sample replicated data from out-of-sample
   predictions.
7. For model comparison, verify identical observations, likelihood target, data
   preprocessing, and pointwise `log_likelihood`; inspect Pareto diagnostics and
   score uncertainty before ranking.
8. Persist the labeled artifact and provenance when results must be reproducible.

## Decision map

| Need | Use | Guard |
|---|---|---|
| Describe marginal posterior | Summary/HDI plus MCSE and ESS | Do not report precision beyond Monte Carlo accuracy. |
| Diagnose MCMC convergence | Rank R-hat, bulk/tail ESS, MCSE, trace/rank/energy views, sampler stats | Keep chains separate and inspect parameter coordinates. |
| Diagnose one-chain output | ESS/MCSE and trace/autocorrelation evidence | R-hat cannot supply between-chain evidence; obtain more chains where possible. |
| Assess model fit | Posterior predictive checks | Choose domain-relevant discrepancy, not only overlapping histograms. |
| Compare predictive models | PSIS-LOO or justified alternative | Same observations/target and valid pointwise log likelihood; inspect Pareto-k. |
| Combine independent chains | Concatenate along `chain` only after schema/coordinate equality | Do not concatenate posterior draws along an observation dimension. |
| Combine different groups | Extend/merge by group under matching variables/coords | Do not overwrite an existing group silently. |

Read [diagnostics and comparison](references/diagnostics-comparison.md) before
turning any single number into a pass/fail conclusion.

## Canonical labeled conversion

```python
import arviz as az
import numpy as np


def make_idata(
    beta: np.ndarray,
    log_likelihood: np.ndarray,
    feature_names: list[str],
    observation_ids: list[str],
):
    if beta.ndim != 3 or log_likelihood.ndim != 3:
        raise ValueError("expected chain x draw x domain arrays")
    if beta.shape[:2] != log_likelihood.shape[:2]:
        raise ValueError("posterior and log likelihood sample axes differ")
    if beta.shape[2] != len(feature_names):
        raise ValueError("feature coordinate length differs")
    if log_likelihood.shape[2] != len(observation_ids):
        raise ValueError("observation coordinate length differs")
    if len(set(feature_names)) != len(feature_names):
        raise ValueError("feature coordinates must be unique")
    if len(set(observation_ids)) != len(observation_ids):
        raise ValueError("observation coordinates must be unique")
    return az.from_dict(
        {
            "posterior": {"beta": beta},
            "log_likelihood": {"outcome": log_likelihood},
        },
        coords={"feature": feature_names, "observation": observation_ids},
        dims={"beta": ["feature"], "outcome": ["observation"]},
    )
```

This assumes arrays arrive as chain × draw × domain. Inspect the installed
converter rather than applying that assumption to every backend. Assert
coordinate lengths and uniqueness before conversion.

## Diagnostic contract

- R-hat near one is necessary for many MCMC workflows but not sufficient. Use
  rank-normalized and folded variants as supported, plus trace behavior.
- Bulk ESS concerns central estimates; tail ESS concerns quantiles/tails. MCSE
  must be small relative to the precision needed for the reported estimand.
- Divergences, energy/BFMI, acceptance, and tree-depth fields live in
  `sample_stats` when the sampler records them. Absence is unknown, not zero.
- Do not average chains before diagnostics or reshape chain × draw to one axis
  and then recreate fake chains.
- Diagnostic thresholds are escalation rules, not proof of model validity.
  Predictive adequacy and model assumptions remain separate.

## Comparison contract

PSIS-LOO requires pointwise log likelihood for the same observation units. Do
not compare models fit to different filtered rows, likelihood factorizations,
response transformations, or weighting conventions without a justified mapping.
On ArviZ 1.x, call `loo(..., pointwise=True, var_name=...)` when the caller must
retain per-observation Pareto-k, then pass those ELPD results to `compare`.
`compare` no longer accepts the 0.x `ic="loo"` selector. Inspect Pareto-k and
uncertainty; address influential observations or use a more robust validation
plan rather than reporting weights mechanically. Comparison answers relative
predictive performance among candidates, not absolute fit, causality, or
scientific truth.

Use [testing and version grounding](references/testing-version.md) because
ArviZ 1.x packaging and stats/plot APIs differ from many 0.x examples.

## Completion gate

Do not declare completion until provenance is recorded; required groups exist;
each variable's dimensions and coordinates match semantic axes; chains and
draws remain separate; convergence reports combine R-hat, ESS, MCSE, traces,
and available sampler statistics; predictive checks target the stated use;
comparisons use identical observations and valid pointwise log likelihood;
Pareto and uncertainty warnings are surfaced; persisted output reloads with the
same groups/coords; and missing groups or skipped diagnostics are reported.

## References

- [Inference-data contract](references/object-model.md)
- [Diagnostics and comparison](references/diagnostics-comparison.md)
- [Testing and version grounding](references/testing-version.md)
