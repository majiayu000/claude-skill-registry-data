---
name: diagnosing-ml-failures
description: Isolate the root cause of ML performance drops, inconsistent evaluations, prediction errors, and training-serving mismatches across data, labels, splits, pipelines, models, metrics, and runtime behavior. Use when investigating a reproducible failure or regression, not routine model selection or general performance validation.
---

# Diagnosing ML Failures

Turn a vague failure into a minimal, testable discrepancy and isolate the first layer where expected and observed behavior diverge. Do not begin with hyperparameter tuning: it can hide the fault while destroying causal evidence.

## Define the symptom

Capture one concrete failing example or comparison:

- expected versus observed behavior;
- first known bad and last known good run, version, or time window;
- affected population and unaffected control population;
- metric implementation, threshold, and aggregation level;
- exact input, artifact, code revision, configuration, and environment when available.

Reproduce the symptom through the smallest stable entry point. If it is intermittent, estimate frequency and identify what varies between runs before changing the system.

## Isolate the first broken layer

Trace the same records through boundaries in causal order:

1. **Source and semantics:** extraction window, identifiers, units, timestamps, schema, missingness, duplicates, and joins.
2. **Ground truth:** label definition, observation window, reviewer process, label delay, drift, and adjudication.
3. **Split and sampling:** entity overlap, temporal leakage, cohort shift, weighting, and deduplication.
4. **Feature pipeline:** availability time, fit/transform state, ordering, encoding, defaults, and training-serving parity.
5. **Model artifact:** weights, feature contract, class order, preprocessing bundle, and artifact version.
6. **Metric and decision logic:** denominator, grouping, threshold, calibration, exclusions, and business-cost mapping.
7. **Runtime and delivery:** dependency versions, hardware nondeterminism, caching, serialization, concurrency, and response postprocessing.

Compare invariants at each boundary - row counts, key uniqueness, hashes, distributions, schemas, representative record traces - and stop at the earliest divergence. Downstream differences may be consequences, not causes.

## Test competing hypotheses

Maintain multiple plausible hypotheses until evidence distinguishes them. For each hypothesis, define a discriminating test whose outcomes differ between explanations. Prefer controlled swaps and minimal counterfactuals:

- old data with new code versus new data with old code;
- frozen artifact through offline and online pipelines;
- known-good records before and after one transformation;
- recomputed metric from raw predictions versus reported metric;
- independently adjudicated error sample versus existing labels.

Change one explanatory variable at a time where practical. Preserve all failed tests and negative results in a rejected-hypothesis log; they prevent repeated work and constrain future explanations.

## Treat ground truth as a suspect, not an oracle

When apparent model failures may be annotation errors or ambiguous cases, sample errors without cherry-picking. Obtain independent human review only when an authorized reviewer and an approved data-sharing path are available; otherwise specify the review needed without transmitting records. Keep original labels, reviewer decisions, disagreements, and adjudication separate. A corrected label may explain an example without proving the model is correct for the population.

## Close with proof, not plausibility

A diagnosis is complete only when the proposed cause predicts the symptom and an authorized, isolated, reversible intervention removes it without breaking an appropriate control. Verify at the same scope as the original failure: fixing one example does not prove a population regression is resolved. Diagnose and propose a fix by default; modify or deploy the real system only when the user requested that additional action.

Use [assets/failure-investigation-log.md](assets/failure-investigation-log.md) to preserve observations, experiments, rejected hypotheses, root-cause evidence, and regression coverage. For detailed layer probes and controlled isolation patterns, read [references/failure-isolation.md](references/failure-isolation.md).

If several layers remain plausible, report the narrowed boundary, remaining hypotheses, and next discriminating test. Do not label the most intuitive explanation as root cause.
