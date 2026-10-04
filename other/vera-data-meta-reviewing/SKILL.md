---
name: vera-data-meta-reviewing
description: >-
  Runs study-level diagnostics and primary pooled estimation for
  meta-analysis of summary statistics across multiple studies. Produces
  forest plot, heterogeneity assessment (Q, I-squared, tau-squared),
  pooled estimates under both fixed-effects and random-effects models,
  and prediction interval. Ends with a recommendation block listing
  Outputs .R and .py
  scripts with 1 publication-quality forest plot. Triggered when user
  says "meta-analysis," "systematic review," "pooled estimate," "combine
  studies," "forest plot," "heterogeneity," "I-squared," "effect size
  synthesis," or "aggregate results across studies." Does not handle
  network meta-analysis or individual participant data.
allowed-tools: Read, Bash, Write, Edit
---

# Meta-Analysis — Diagnostics & Primary Pooled Estimation

## Table of Contents

- [Scope Boundary](#scope-boundary)
- [Workflow](#workflow)
- [Decision Tree](#decision-tree)
- [Required Inputs](#required-inputs)
- [Code Structure](#code-structure)
- [Reporting Standards](#reporting-standards)
- [Example Dataset](#example-dataset)
- [Method Status](#method-status)
- [Minimal Smoke Test](#minimal-smoke-test)
- [Cross-Skill Interface](#cross-skill-interface)


Open-source skill.

## Scope Boundary

Use this skill when:
- The inputs are study-level summary statistics and the first need is a transparent pooled estimate with heterogeneity diagnostics.
- A one-effect-size-at-a-time meta-analysis is appropriate before moderator, bias, or multilevel extensions.

Do not use this skill when:
- The project is network meta-analysis, IPD meta-analysis, or evidence synthesis without extractable study-level effects.
- The primary need is publication-bias modeling or meta-regression from the start.

## Workflow

Read each step file in `workflow/` before executing that step.

| Step | Responsibility | Executor | Document | Input | Output |
|---|---|---|---|---|---|
| Collect | Collect Inputs | Main Agent | `workflow/step01-collect-inputs.md` | User input | Structured input summary |
| Diagnose | Check Distribution | Main Agent | `workflow/step02-check-distribution.md` | Prior step output | PART 1 code block |
| Test | Run Primary Test | Main Agent | `workflow/step03-run-primary-test.md` | Prior step output | PART 2-3 code blocks |

## Decision Tree

```
1. EFFECT SIZE TYPE
   ├── Continuous (SMD, MD) → escalc(measure="SMD") or "MD"
   ├── Binary (OR, RR, RD) → escalc(measure="OR") or "RR"/"RD"
   └── Correlation (r) → escalc(measure="ZCOR") Fisher z transform

2. HETEROGENEITY ASSESSMENT
   ├── I² < 25% → low heterogeneity (fixed-effects may suffice)
   ├── 25% ≤ I² ≤ 75% → moderate (random-effects preferred)
   └── I² > 75% → high (random-effects + moderator analysis needed)
```

## Required Inputs

| Role | What to collect |
|---|---|
| **Study data** | Study ID, effect size, SE (or CI, or N per group + means/SDs) |
| **Effect type** | SMD, MD, OR, RR, RD, or r |
| **Moderators** | Study-level variables (year, quality, setting) — for recommendation |
| **Model preference** | Fixed vs random (or let data decide) |

## Code Structure

```
PART 0: Setup & Data Loading
PART 1: Study Table + Forest Plot + Heterogeneity → plot_01_forest.png
PART 2: Pooled Estimates (fixed + random) + Prediction Interval
PART 3: Recommendation Block → text listing additional analyses available
```

## Reporting Standards

1. Pooled effect: "pooled ES = X.XX, 95% CI [X.XX, X.XX], z = X.XX, p"
2. Heterogeneity: "Q(df) = X.XX, p = .XXX; I² = XX.X%; tau² = X.XX"
3. Prediction interval: always alongside CI
4. p-values: "< .001" not "0.000"; exact to 3 decimals otherwise
5. Weights: report study weights in forest plot
6. Degrees of freedom: always with test statistics
7. Sample size: report total N across studies and k (number of studies)
8. Decimal places: 2 for effect sizes, 3 for p-values, 1 for I²

## Example Dataset

Constructed example: 10 studies comparing treatment vs control on a
continuous outcome (standardized mean difference). NOT a built-in R
dataset — create a data frame with study_id, n_treatment, n_control,
mean_treatment, mean_control, sd_treatment, sd_control.

R: `metafor` package. Python: `statsmodels` or custom inverse-variance.

## Method Status

| Status | Methods |
|---|---|
| Implemented in this skill | Effect-size construction, fixed/random pooled estimates, forest plot, heterogeneity metrics, prediction interval |
| Implemented downstream in `vera-data-meta-generating` | Publication-bias checks, sensitivity analysis, subgroup analysis, meta-regression, Bayesian and three-level extensions |
| Out of scope in this open-source baseline | Network meta-analysis, IPD meta-analysis, and evidence-synthesis families not named above |

## Minimal Smoke Test

- Smoke-test prompt: "Run `vera-data-meta-reviewing` on a 10-study continuous-outcome example with study IDs, group means, SDs, and sample sizes. Produce the standard baseline artifacts."

## Cross-Skill Interface

```
Output:
├── code_r      → .R script
├── code_python → .py script
├── figures/    → 1 PNG (forest plot)
└── recommendations → text block (additional analyses available)
```

Next step: Invoke `vera-data-meta-generating` from this skillset to run the full pipeline (additional tests, subgroup analysis, modeling, manuscript generation). See `../../CROSS-SKILL-INTERFACE.md` for the shared handoff contract.
