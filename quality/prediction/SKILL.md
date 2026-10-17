---
name: prediction
description: Predict with models honestly — baselines, leakage-free validation, calibration, drift awareness.
version: 1
triggers: prediction model, predictive model, calibration, leakage, forecast with a model
category: Thinking & decisions
blurb: Predict with models honestly — baselines, leakage-free validation and calibration.
archetype: knowledge
example: Check my prediction model for leakage and overconfidence.
---

# Prediction (Predictive Modeling)

A prediction is a claim with an error bar. Beat the baseline, validate without leakage, report calibration — or don't deploy it.

## When to use
- Building or using predictive models (churn, demand, risk scores, failure prediction).
- Reviewing any "the model says" claim before relying on it.
- Setting thresholds for automated decisions.

## Method
1. **Target & decision**: what is predicted, at what horizon, driving which decision? Choose the metric from the decision's costs — false positives vs false negatives rarely cost the same.
2. **Baseline first**: naive rule / historical mean / current heuristic — computed and reported; a model that doesn't beat the baseline doesn't ship.
3. **Validation without leakage**: time-based splits for temporal data (never random if time matters — that's leakage); no peeking at validation; cross-validation where appropriate; holdout for the final read.
4. **Model ladder**: simple first (regression, rules, seasonal means); complexity must earn its keep in accuracy, explainability, and maintenance cost.
5. **Probabilities, not fortune-telling**: output probabilities; set action thresholds from decision costs; **check calibration** (when it says 70%, it should be right ~70%) — not just ranking ability.
6. **Evaluate for purpose**: magnitude metrics (MAE/MAPE), ranking metrics (AUC, precision-recall) as appropriate; segment errors — the worst cohort is the story.
7. **Drift & loops**: monitor input drift and live performance; identify feedback loops (predictions change behavior change data); define retraining policy.
8. **Deploy carefully**: versioned model + card, rollout with monitoring, rollback path — plumbing via `data-ml-pipelines`.

## Quality gates
- [ ] Baseline computed; improvement demonstrated on untouched holdout.
- [ ] Split strategy documented; temporal leakage explicitly checked.
- [ ] Calibration + segment errors reported, not just aggregate.
- [ ] Drift monitoring + retrain policy in place before relying on it.

## Red lines
- No random splits for time-series reality; no metric-chosen-to-flatter; no silent model updates in production.

## Related
`forecasting` · `data-ml-pipelines` · `quant-research` (validation discipline).
