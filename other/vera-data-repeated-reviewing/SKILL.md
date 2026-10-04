---
name: vera-data-repeated-reviewing
description: >-
  Trajectory diagnostics and primary hypothesis tests for repeated measures /
  longitudinal designs with a continuous outcome. Produces spaghetti plots with
  group mean ribbons, ICC, descriptives per time point, attrition check, and
  one interpreted test: paired t-test for 2 time points, repeated measures
  ANOVA for 3+ time points in one group, or mixed ANOVA (time x group) for 3+
  time points with 2+ groups, including Mauchly sphericity and Greenhouse-Geisser
  correction. Ends with a recommendation block. Outputs .R and .py scripts with
  publication-quality plots. Trigger when user has a continuous outcome measured
  on the same subjects over time and says "repeated measures," "longitudinal,"
  "within-subjects," "pre-post," "paired," "panel data," "growth curve,"
  "multilevel," "mixed model," or "correlated observations." Does not handle
  binary, count, survival, ordinal, or cross-sectional outcomes.
allowed-tools: Read, Bash, Write, Edit
---

# Repeated Measures Outcome — Trajectory Diagnostics & Hypothesis Testing

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
- The same continuous outcome is measured repeatedly on the same units over a small number of waves.
- A paired-test / RM-ANOVA / mixed-ANOVA baseline is needed before mixed-model extensions.

Do not use this skill when:
- The data are a long univariate calendar-time series; use `vera-data-timeseries-reviewing`.
- The primary need is a richer mixed-model, GEE, or growth-curve analysis from the start.

## Workflow

Read each step file in `workflow/` before executing that step.

| Step | Responsibility | Executor | Document | Input | Output |
|---|---|---|---|---|---|
| Collect | Collect Inputs | Main Agent | `workflow/step01-collect-inputs.md` | User input | Structured input summary |
| Diagnose | Check Distribution | Main Agent | `workflow/step02-check-distribution.md` | Prior step output | PART 1 code block |
| Test | Run Primary Test | Main Agent | `workflow/step03-run-primary-test.md` | Prior step output | PART 2-3 code blocks |

## Decision Tree

```
1. DATA FORMAT CHECK
   ├── Wide → reshape to long before proceeding
   └── Long → continue

2. TIME POINTS
   ├── Exactly 2 → paired comparisons path
   └── 3+ → repeated measures ANOVA / mixed ANOVA path

3. GROUP STRUCTURE
   ├── No between-subjects factor → one-way RM-ANOVA (within-subjects only)
   └── Between-subjects factor → mixed ANOVA (time × group)

4. SPHERICITY (if 3+ time points)
   ├── Mauchly p ≥ .05 → uncorrected F
   └── Mauchly p < .05 → Greenhouse-Geisser / Huynh-Feldt correction
```

## Required Inputs

| Role | What to collect |
|---|---|
| **Outcome (Y)** | Variable name, units, what it measures (continuous) |
| **Time variable** | Measurement occasions, how many, equally spaced? |
| **Subject/ID variable** | What identifies the same individual across time |
| **Group variable** | Between-subjects factor (treatment, condition, etc.) |
| **Covariates** | Time-varying? Time-invariant? |
| **Data format** | Long (one row per obs) or wide (one row per subject) |

## Code Structure

```
PART 0: Setup & Data Loading (+ reshape if wide)
PART 1: Trajectory Diagnostics → plot_01_trajectories.png
PART 2: Primary Hypothesis Test → plot_02_interaction.png
PART 3: Recommendation Block   → text listing additional analyses available
```

## Reporting Standards

1. p-values: "< .001" not "0.000"; exact to 3 decimals otherwise
2. Effect sizes: Cohen's d (paired t-test), partial eta-squared (RM-ANOVA/mixed ANOVA)
3. 95% CIs: always for mean differences
4. Degrees of freedom: always with t and F statistics
5. Sphericity: Mauchly's W, p; if violated, GG epsilon and corrected p
6. ICC: **always name the specific form**, not just "ICC". Use Shrout & Fleiss (1979) notation: ICC(1,1) one-way random, single measure; ICC(2,1) two-way random, single measure, absolute agreement; ICC(3,1) two-way mixed, single measure, consistency; and the corresponding (*,k) forms for averaged measures. For repeated-measures designs with the same rater/instrument across time on the same subjects, **default to ICC(3,1) consistency** (or ICC(3,k) if reporting the averaged score). For multiple independent raters of the same targets, use ICC(2,1) agreement. Report value + 95% CI + form + interpretation (Koo & Li 2016 bands: < 0.50 poor, 0.50–0.75 moderate, 0.75–0.90 good, > 0.90 excellent).
7. Sample size: final analytic N (subjects) and total observations
8. Decimal places: 2 for M/SD, 3 for p and effect sizes
9. Non-significance: "not statistically significant at alpha = .05" — never "no effect"

## Hypothesis Tests

| Scenario | Normal | Non-Normal |
|---|---|---|
| 2 time points (paired) | Paired t-test | Wilcoxon signed-rank |
| 3+ time points, 1 group | One-way RM-ANOVA + sphericity | Friedman test |
| 3+ time points, 2+ groups | Mixed ANOVA (time x group) | — |

Cross-sectional group comparisons → `vera-data-continuous-reviewing`.

## Example Dataset

R built-in `ChickWeight`: outcome = weight, time = Time (0, 2, 4, ..., 21 days),
subject = Chick, group = Diet (1, 2, 3, 4).
Python: `sm.datasets.get_rdataset("ChickWeight").data` (with offline fallback to bundled `examples/chickweight.csv`).

## Method Status

| Status | Methods |
|---|---|
| Implemented in this skill | ICC reporting, paired tests, RM-ANOVA / mixed-ANOVA branching, sphericity corrections, trajectory diagnostics |
| Implemented downstream in `vera-data-repeated-generating` | Linear mixed models, GEE, growth-curve extensions, subgroup interactions, exploratory trees |
| Out of scope in this open-source baseline | Binary/count repeated-outcome families and high-frequency time-series forecasting workflows |

## Minimal Smoke Test

- Smoke-test prompt: "Run `vera-data-repeated-reviewing` on `ChickWeight`, using `weight` as the outcome, `Time` as the repeated factor, `Chick` as the subject ID, and `Diet` as the grouping variable. Produce the standard baseline artifacts."

## Cross-Skill Interface

```
Output:
├── code_r      → .R script
├── code_python → .py script
├── figures/    → 2 PNGs (trajectories + interaction)
└── recommendations → text block (additional analyses available)
```

Next step: Invoke `vera-data-repeated-generating` from this skillset to run the full pipeline (additional tests, subgroup analysis, modeling, manuscript generation). See `../../CROSS-SKILL-INTERFACE.md` for the shared handoff contract.
