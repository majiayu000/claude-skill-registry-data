---
name: vera-data-survival-reviewing
description: >-
  Runs survival diagnostics and primary hypothesis tests for right-censored
  time-to-event outcomes. Produces Kaplan-Meier curves with number-at-risk
  tables, log-rank test for group comparison, median survival, landmark
  survival rates, and HR preview from univariate Cox regression. Outputs
  .R and .py scripts with publication-quality plots. Triggered when user
  has a time-to-event outcome and says "survival outcome," "time to event,"
  "Kaplan-Meier," "hazard," "OS/PFS/DFS." Right-censored data only.
  Competing risks, recurrent events, and multi-state models are out of
  scope. Does not handle binary, count, continuous, ordinal, repeated
  measures, or SEM outcomes.
allowed-tools: Read, Bash, Write, Edit
---

# Survival Outcome — Diagnostics & Hypothesis Testing

## Table of Contents

- [Scope Boundary](#scope-boundary)
- [Workflow](#workflow)
- [Decision Tree](#decision-tree)
- [Required Inputs](#required-inputs)
- [Code Structure](#code-structure)
- [Reporting Standards](#reporting-standards)
- [Hypothesis Tests](#hypothesis-tests)
- [Example Dataset](#example-dataset)
- [Method Status](#method-status)
- [Minimal Smoke Test](#minimal-smoke-test)
- [Cross-Skill Interface](#cross-skill-interface)


Open-source skill.

## Scope Boundary

Use this skill when:
- The endpoint is standard right-censored time-to-event data and the first need is KM plus log-rank style inference.
- A univariate or simple grouped survival baseline is appropriate before multivariable hazard modeling.

Do not use this skill when:
- The data involve left/interval censoring, competing risks, or multi-state structures.
- The primary question already depends on recurrent-event or time-varying-covariate modeling.

## Workflow

Read each step file in `workflow/` before executing that step.

| Step | Responsibility | Executor | Document | Input | Output |
|---|---|---|---|---|---|
| Collect | Collect Inputs | Main Agent | `workflow/step01-collect-inputs.md` | User input | Structured input summary |
| Diagnose | Check Distribution | Main Agent | `workflow/step02-check-distribution.md` | Prior step output | PART 1 code block |
| Test | Run Primary Test | Main Agent | `workflow/step03-run-primary-test.md` | Prior step output | PART 2-3 code blocks |

## Decision Tree

```
1. CHECK FOLLOW-UP & CENSORING
   ├── Censoring rate > 80% → Warning: limited events, wide CIs expected
   ├── Censoring rate < 5% → Note: standard regression may suffice
   └── Otherwise → proceed normally

2. GROUP COMPARISON
   ├── 2 groups → Log-rank test + HR from univariate Cox
   └── 3+ groups → Log-rank test + pairwise log-rank (Bonferroni)
```

## Required Inputs

| Role | What to collect |
|---|---|
| **Time variable** | Continuous, ≥0, follow-up/survival time |
| **Event indicator** | Which value = event occurred, which = censored |
| **Group variable** | What defines groups, how many levels |
| **Predictors** | For recommendation block (not executed) |

## Code Structure

```
PART 0: Setup & Data Loading
PART 1: Follow-Up & Censoring Diagnostics → plot_01_km_overall.png, plot_01b_event_histogram.png
PART 2: Primary Hypothesis Test           → plot_02_km_groups.png
PART 3: Recommendation Block              → text listing additional analyses available
```

## Reporting Standards

1. p-values: "< .001" not "0.000"; exact to 3 decimals otherwise
2. Hazard ratio: HR with 95% CI, "HR = X.XX, 95% CI [X.XX, X.XX]"
3. Median survival: always with 95% CI
4. Survival rates at landmarks: with 95% CI
5. Censoring: always report % censored overall and by group
6. Log-rank: chi-sq(df) = X.XX, p = .XXX
7. Decimal places: 2 for median survival, 3 for p and HR
8. Non-significance: "not statistically significant at alpha = .05" — never "no effect"
9. Cox regression: when reported, include Schoenfeld-residual test for proportional hazards (global p-value + per-covariate). Flag any PH violation explicitly.

## Hypothesis Tests

| Scenario | Test |
|---|---|
| 2 independent groups | Log-rank + univariate Cox HR |
| 3+ independent groups | Log-rank + pairwise log-rank (Bonferroni) |

Paired/clustered designs are out of scope for this version.

## Example Dataset

R built-in `survival::lung`: outcome = time (survival time), status (1=censored, 2=dead).
Predictors: age, sex, ph.ecog, ph.karno, pat.karno, meal.cal, wt.loss.
Python: `from lifelines.datasets import load_lung` or reconstruct from R.

## Method Status

| Status | Methods |
|---|---|
| Implemented in this skill | Kaplan-Meier summaries, log-rank tests, median survival, landmark survival rates, univariate Cox preview |
| Implemented downstream in `vera-data-survival-generating` | Multivariable Cox, AFT, recurrent-event models, random survival forest, boosting survival methods |
| Out of scope in this open-source baseline | Competing-risks, multi-state, left-censored, and interval-censored survival families |

## Minimal Smoke Test

- Smoke-test prompt: "Run `vera-data-survival-reviewing` on `survival::lung`, using `time` as follow-up, `status` as the event indicator, and `sex` as the grouping variable. Produce the standard baseline artifacts."

## Cross-Skill Interface

```
Output:
├── code_r      → .R script
├── code_python → .py script
├── figures/    → 2 PNGs (KM overall + KM groups)
└── recommendations → text block (additional analyses available)
```

Next step: Invoke `vera-data-survival-generating` from this skillset to run the full pipeline (additional tests, subgroup analysis, modeling, manuscript generation). See `../../CROSS-SKILL-INTERFACE.md` for the shared handoff contract.
