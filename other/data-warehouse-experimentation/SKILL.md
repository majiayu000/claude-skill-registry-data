---
name: "data-warehouse-experimentation"
description: "Running experiments out of the data warehouse instead of via dedicated experiment platforms. SQL-based assignment, exposure logging discipline, metric definitions in dbt models, statistical analysis in SQL or Python, variance reduction with CUPED, sequential testing, and the operational tradeoffs vs platforms like Statsig and Optimizely. Triggers on warehouse-native experimentation, run experiments in BigQuery, run experiments in Snowflake, dbt experiments, SQL t-test, CUPED variance reduction, exposure log, sample ratio mismatch, sequential testing, mSPRT, doubly robust estimation, build vs buy experimentation. Also triggers when the team is choosing between platform and warehouse, building warehouse-native experiment infrastructure, auditing one, or running an experiment with a custom metric the platform cannot handle."
---

# Data Warehouse Experimentation

A senior data scientist's playbook for running experiments natively out of BigQuery, Snowflake, or any modern data warehouse, with metric definitions in dbt and statistical analysis in SQL or Python.

Most companies that run experiments at scale use a dedicated platform. Statsig, Optimizely, LaunchDarkly with experimentation, PostHog, Amplitude Experiment. The platforms are good. They handle assignment, instrumentation, and analysis in one product, and the SQL-savvy data team does not have to reinvent the variance reduction wheel.

There is a different operational model that mature data teams increasingly choose: warehouse-native experimentation. Assignment happens in code or via feature flags. Exposure events fire to the warehouse like any other event. Metrics are defined as dbt models. Statistical analysis runs as SQL or in a Python notebook against warehouse data. The "experiment platform" is just your existing data stack.

This skill covers when warehouse-native is the right call, the architecture, and the specific techniques that make it work: assignment patterns, exposure logging discipline, metric definitions in dbt, t-tests and CUPED in SQL, sequential testing, and the pitfalls that take down homegrown setups.

When to use this skill: deciding between platform vs warehouse-native, building a warehouse-native experiment infrastructure, auditing an existing one, or running a specific experiment when the platform of record cannot handle a custom metric or segmentation.

---

## What this skill is for

This skill spans the operational execution model for warehouse-native experimentation. It does not replace the methodology and interpretation skills; it composes with them.

- `experiment-design` covers methodology: hypotheses, sample size, randomization unit, primary metric. Tool-agnostic. Read it first to design the experiment correctly regardless of where it runs.
- `experimentation-analytics` covers interpretation: confidence intervals, p-values, effect size, decision frameworks. Tool-agnostic. Read it when results land.
- `experimentation-platform-orchestrator` covers the platform-vs-warehouse decision in detail. Read it to decide whether to use a platform or this skill.
- `feature-flagging` covers assignment infrastructure when not running through a platform. Read it for the flag-management discipline that this skill assumes.
- This skill (`data-warehouse-experimentation`) covers the operational execution: SQL-based assignment, exposure logging, metric definitions in dbt, statistical analysis in SQL or Python, variance reduction, sequential testing.

The distinction is between "what to do" (the methodology and interpretation skills) and "how to do it without a vendor platform" (this skill). Read this skill after you have decided warehouse-native is the right call. If you are still deciding, start with `experimentation-platform-orchestrator`.

---

## If required data is unavailable

This skill's output depends on data, measurements, or tool results it cannot generate on its own. When a required input, tool, or data source is unavailable or unverifiable, the sanctioned output is the deliverable with the gap stated: what was needed, what was actually obtained or verified, and which parts of the output are affected. Fabricating, estimating, or interpolating a required number to complete the deliverable is never sanctioned. A stated gap is a complete answer.

---

## Reference files

- [`references/warehouse-vs-platform-decision.md`](references/warehouse-vs-platform-decision.md) - When each operational model is the right call. Cost considerations at different scales. Hybrid patterns. Migration patterns.
- [`references/assignment-and-exposure-patterns.md`](references/assignment-and-exposure-patterns.md) - Hash assignment SQL templates for BigQuery and Snowflake. Salt naming conventions. Exposure event schema. SRM check SQL.
- [`references/metric-definitions-in-dbt.md`](references/metric-definitions-in-dbt.md) - dbt model patterns for experiment metrics. Reusing fct models. The exp_metrics namespace. Versioning.
- [`references/statistical-analysis-templates.md`](references/statistical-analysis-templates.md) - SQL and Python templates for Welch's t-test, proportions test, Mann-Whitney, bootstrap. Notebook structure.
- [`references/variance-reduction-techniques.md`](references/variance-reduction-techniques.md) - CUPED math and Python implementation with worked example. Stratification. Regression adjustment. Doubly robust estimation primer.
- [`references/power-analysis-calculations.md`](references/power-analysis-calculations.md) - MDE math. Sample size calculations. Calibrating effect-size assumptions from historical experiments.
- [`references/sequential-testing-patterns.md`](references/sequential-testing-patterns.md) - mSPRT, confidence sequences, group sequential designs. Honest framing on when to peek.
- [`references/common-pitfalls.md`](references/common-pitfalls.md) - Eleven failure patterns with diagnoses and fixes.

---


## Conditional methods

Before applying a method below, read its linked section. For a narrow task select only relevant methods; for a full audit/design use the framework and relevant failure patterns. Existing references remain available for deeper details.

- When warehouse-native is the right call: [method](references/domain-guide.md#when-warehouse-native-is-the-right-call).
- The architecture: [method](references/domain-guide.md#the-architecture).
- Assignment patterns: [method](references/domain-guide.md#assignment-patterns).
- The exposure log: [method](references/domain-guide.md#the-exposure-log).
- Metric definitions in dbt models: [method](references/domain-guide.md#metric-definitions-in-dbt-models).
- Statistical analysis in SQL: [method](references/domain-guide.md#statistical-analysis-in-sql).
- Statistical analysis in Python: [method](references/domain-guide.md#statistical-analysis-in-python).
- Variance reduction: CUPED and beyond: [method](references/domain-guide.md#variance-reduction-cuped-and-beyond).
- Pre-experiment power analysis: [method](references/domain-guide.md#pre-experiment-power-analysis).
- Sequential testing patterns: [method](references/domain-guide.md#sequential-testing-patterns).
- Common pitfalls: [method](references/domain-guide.md#common-pitfalls).
- The framework: 12 considerations for warehouse-native experimentation: [method](references/domain-guide.md#the-framework-12-considerations-for-warehouse-native-experimentation).
- Closing: the build-vs-buy decision is real: [method](references/domain-guide.md#closing-the-build-vs-buy-decision-is-real).
