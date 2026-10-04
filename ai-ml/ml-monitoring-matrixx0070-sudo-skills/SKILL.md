---
name: ml-monitoring
version: 1.0.0
description: Monitor a live model for data quality, input and prediction drift, performance decay, and fire retraining triggers.
author: matrixx0070
tags: [ml, monitoring, drift, decay, retraining]
capabilities: []
---

## When to use

Use this once a model serves real traffic, to detect when reality diverges from training — broken inputs, shifted distributions, decayed accuracy — and to define the concrete conditions that trigger retraining or rollback.

**Not for:** monitoring LLM output quality, hallucination, or token cost (see `ai-guardrails`, `ai-cost-latency`). Not for BI freshness/pipeline SLAs or data-quality tests at rest (see `de-data-quality`).

## Method

1. Establish the training reference: save the training feature distributions, prediction distribution, and headline metric as the comparison baseline.
2. Monitor data quality first: nulls, out-of-range values, schema changes, unexpected categories. Most incidents are broken data, not clever drift.
3. Track input (feature) drift. Decision point: numeric → PSI or KS test; categorical → PSI / chi-square. Alert on sustained shift, not single-batch noise.
4. Track prediction drift: the score distribution moving is an early warning available before labels arrive.
5. Track true performance once labels land. Decision point: labels delayed → rely on proxy/drift signals in the gap; labels fast → monitor the live primary metric on a rolling window.
6. Segment monitoring by the cohorts that mattered in error analysis — aggregate health can hide a decayed segment.
7. Define retraining triggers as explicit thresholds (metric below X, PSI above Y, or a fixed cadence), plus a rollback trigger for hard failures.
8. Route alerts to an owner with a runbook; every alert names its likely cause and first action.

## Example

Loan-default model, labels arrive ~60 days late. Daily job compares live features to the training reference: `income` PSI jumps to 0.28 (>0.2 threshold) after an upstream unit change dollars→cents — a data-quality bug, caught before any label. Prediction drift confirms the shift. Trigger fires: page the owner, roll back to v2, patch the pipeline. Standing rule: retrain when rolling AUC < 0.68 OR any feature PSI > 0.2 for 3 consecutive days OR quarterly, whichever first.

## Pitfalls

- **Drift-only, no data-quality checks.** Chasing subtle distribution shifts while a null flood corrupts inputs. Check quality first.
- **Waiting for labels.** Doing nothing until ground truth arrives. Use input/prediction drift as leading signals.
- **Alerting on single batches.** Noisy one-off spikes cause fatigue. Require sustained breaches.
- **Vague triggers.** "Retrain when it gets worse" never fires. Set numeric thresholds and a cadence.

## Output format

```
# Monitoring: <name>
REFERENCE: training feature + prediction dists + <metric baseline>
DATA QUALITY: nulls | ranges | schema | new categories
INPUT DRIFT: <PSI|KS> per feature | alert=<threshold, sustained N>
PREDICTION DRIFT: score dist | alert=<threshold>
PERFORMANCE: <metric> on <window> | label delay=<t>
SEGMENTS: <cohort: watched>
RETRAIN TRIGGER: <metric<X | PSI>Y for Nd | cadence>
ROLLBACK TRIGGER: <hard-failure condition> -> <last-good>
ALERTING: owner + runbook
```
