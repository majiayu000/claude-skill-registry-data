---
name: ads-test
description: "Design and evaluate paid-ad experiments with hypotheses, randomization units, sample-size and duration assumptions, guardrails, platform experiment tools, analysis, and decision rules. Use for A/B test, split test, experiment design, hypothesis, statistical significance, sample size, test duration, or experiment readout."
---

# Paid Media Experiment

1. State the decision, causal hypothesis, treatment, control, randomization unit,
   population, primary metric, guardrails, minimum effect, and stopping rule.
2. Check platform constraints, overlapping experiments, conversion lag, seasonality,
   interference, and measurement quality.
3. Calculate sample and duration from declared assumptions; disclose approximations.
4. Change one decision surface unless the design explicitly estimates interactions.
5. Pre-register exclusions, quality checks, analysis, and decision thresholds.
6. For readout, verify assignment integrity and data completeness before estimating
   effect and uncertainty.
7. Return setup or readout in versioned JSON with a plain-language decision.

Do not repeatedly peek and stop on a favorable result, call underpowered noise a
winner, or generalize beyond the tested population.

