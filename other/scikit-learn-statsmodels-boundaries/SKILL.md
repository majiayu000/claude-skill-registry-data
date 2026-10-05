---
name: scikit-learn-statsmodels-boundaries
description: >-
  Use when choosing between or composing scikit-learn predictive workflows and
  statsmodels inferential models: estimand versus prediction target, preprocessing,
  leakage, design matrices, validation, uncertainty, and result handoff. Do not use
  for work entirely inside one library.
---

# scikit-learn and statsmodels boundaries

Choose the library from the question, not from API familiarity. scikit-learn owns
out-of-sample prediction workflows; statsmodels owns model-based estimation and
inference when its assumptions match the design. Using both does not make a result
automatically predictive or inferential.

## Decide the objective

| Need | Primary path |
|---|---|
| estimate a defined parameter with standard errors or tests | statsmodels |
| predict new observations and compare pipelines out of sample | scikit-learn |
| exploratory prediction followed by confirmatory inference | separate discovery and inference datasets or label the second stage exploratory |
| deploy a predictor but inspect coefficients | scikit-learn pipeline; coefficients are not automatically causal or valid inferential estimates |

Read [estimands.md](references/estimands.md),
[design-matrices.md](references/design-matrices.md), and
[validation.md](references/validation.md).

## Workflow

1. Define observation unit, target/estimand, prediction time, available features,
   dependence structure, and intended population.
2. Split by the real deployment boundary before learning preprocessing. Use group or
   time-aware splits when rows are not exchangeable.
3. For scikit-learn, put every learned transformation inside a `Pipeline` or
   `ColumnTransformer`. Tune only within the training resampling procedure.
4. For statsmodels, construct the design deliberately: intercept, reference levels,
   interactions, weights, missing-data policy, and covariance estimator are modeling
   choices.
5. Never reuse a fitted sklearn transformer on a statsmodels model without freezing
   and recording its column order and meaning. Formula encoders and sklearn encoders
   are not interchangeable contracts.
6. Validate the artifact according to its purpose: held-out performance and
   calibration for prediction; assumptions, estimand, uncertainty, and sensitivity for
   inference.
7. Keep outputs separate: predictions with evaluation provenance; estimates with model
   specification, covariance choice, interval, and population scope.

## Boundary rules

- Do not preprocess the full dataset before splitting. This leaks information even
  when the transformation does not use the label.
- Do not select features on all data and then report ordinary statsmodels p-values as
  confirmatory inference.
- Do not compare in-sample fit statistics with cross-validated predictive scores as if
  they measured the same quantity.
- If repeated observations or clusters exist, use grouped validation and an inferential
  covariance/model that represents that dependence.
- If categorical levels can appear at prediction time, define unknown-category
  behavior and verify identical feature ordering.

## Completion checks

- The split matches deployment or sampling structure and no learned operation sees the
  test fold.
- Feature names/order are inspectable after preprocessing.
- Prediction metrics include a baseline and uncertainty or repeated-resampling context.
- Inferential claims identify estimand, assumptions, covariance choice, effect size,
  and interval—not just p-values.
- A handoff between libraries has a tested shape/schema contract and preserves row IDs.
