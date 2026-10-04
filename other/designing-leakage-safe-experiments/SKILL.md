---
name: designing-leakage-safe-experiments
description: Design leakage-safe machine learning experiments that mirror real deployment and support fair model comparisons. Use when defining prediction timing, feature eligibility, train-validation-test splits, baselines, metrics, or controlled model iterations; not for auditing whether raw labels are trustworthy.
---

# Design Leakage-Safe Experiments

Create an experiment whose result would remain credible when the model meets new data in its intended operating environment. Leakage prevention starts with time and causality, not with a random split parameter.

## Define the prediction event

Write down:

- entity and prediction grain;
- decision made from the prediction;
- prediction timestamp and feature cutoff;
- outcome definition and maturity window;
- eligible population at prediction time;
- deployment cadence, horizon, and retraining policy;
- operational cost of each error type.

Build an availability ledger for candidate features: source event, observation time, recording delay, correction or backfill behavior, earliest production availability, and whether the value depends on the outcome. Exclude or reconstruct features that would not exist in the same form at prediction time.

Read [references/leakage-threats-and-splits.md](references/leakage-threats-and-splits.md) when choosing a split or investigating a suspected leakage path.

## Lock the comparison protocol

1. Choose a split that matches deployment: temporal for future generalization, grouped for repeated entities, spatial or site holdout for new locations, or a justified combination.
2. Reserve the final test set before feature selection or tuning. Repeated test inspection turns it into validation data.
3. Fit preprocessing, imputation, encoding, scaling, selection, and resampling only on the training portion of each fold.
4. Fit a calibrator from a separate calibration split or from out-of-fold predictions that did not train the base prediction for those records.
5. Choose the operating threshold or decision policy from validation or calibration evidence. Keep the final test untouched until the model, calibrator, and policy are locked.
6. Define primary and guardrail metrics before seeing candidate results.
7. Establish a transparent baseline: prevalence, naive forecast, rule, or simple regularized model as appropriate.
8. Hold data, split, metric implementation, and compute budget constant while comparing one material change at a time.
9. Record every run, including failures and negative results. Complexity earns adoption only through a repeatable, decision-relevant improvement.

## Challenge the design

Test for duplicate or near-duplicate rows across folds; entity, household, device, site, or document overlap; target proxies; post-outcome updates; full-dataset preprocessing; retrospective cohort filters; label-window overlap; and repeated tuning against the holdout.

Where risk is material, run a temporal backtest, group holdout, label or feature permutation check, suspicious-feature ablation, and slice stability analysis. A surprisingly strong result is a reason to investigate, not a reason to relax scrutiny.

Ask for approval when a choice changes the business target, acceptable error tradeoff, evaluation population, or deployment assumptions. Make routine technical choices within the agreed protocol and document them.

## Produce the protocol

Use [assets/leakage-safe-experiment-plan.md](assets/leakage-safe-experiment-plan.md) before implementation. The finished protocol must let a reviewer determine:

- what was knowable at prediction time;
- why no entity or future information crosses folds;
- how the baseline and candidates receive an equal comparison;
- which set controls tuning and which set supports the final claim;
- what improvement would justify added complexity;
- which observed failures remain unresolved.
