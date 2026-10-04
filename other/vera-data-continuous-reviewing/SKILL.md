---
name: vera-data-continuous-reviewing
description: >-
  Runs distribution diagnostics and primary hypothesis tests for continuous
  outcome variables. Produces Shapiro-Wilk normality check, skewness,
  kurtosis, Q-Q plot, and one fully interpreted group comparison (Welch's t
  for 2 groups or ANOVA with Tukey HSD for 3+ groups) with effect sizes and
  nonparametric confirmation. Ends with a recommendation block listing
  Outputs .R and .py scripts
  with 2 publication-quality plots. Triggered when user has a
  continuous/numeric outcome and says "analyze continuous outcome," "my DV is
  numeric," "compare group means," or names a continuous variable like
  weight, score, income, time, cost, mpg, blood pressure. Does not handle
  binary, count, survival, ordinal, repeated measures, or SEM outcomes.
allowed-tools: Read, Bash, Write, Edit
---

# Continuous Outcome — Distribution Diagnostics & Hypothesis Testing

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
- The outcome is a single continuous variable and the first need is a transparent baseline comparison across groups.
- A primary t-test / ANOVA-style analysis is appropriate before regression or nonlinear exploratory work.

Do not use this skill when:
- The design is repeated / paired, multivariate, or time-indexed.
- The outcome is binary, count, survival, ordinal, or SEM-based rather than continuous.

## Workflow

Read each step file in `workflow/` before executing that step.

| Step | Responsibility | Executor | Document | Input | Output |
|---|---|---|---|---|---|
| Collect | Collect Inputs | Main Agent | `workflow/step01-collect-inputs.md` | User input | Structured input summary |
| Diagnose | Check Distribution | Main Agent | `workflow/step02-check-distribution.md` | Prior step output | PART 1 code block |
| Test | Run Primary Test | Main Agent | `workflow/step03-run-primary-test.md` | Prior step output | PART 2-3 code blocks |

## Decision Tree

```
1. CHECK DISTRIBUTION
   ├── Normal (Shapiro-Wilk p ≥ .05, |skewness| < 1) → parametric primary
   └── Non-normal → nonparametric primary + recommend QR/trees

2. GROUP COMPARISON
   ├── 2 groups → Welch's t + Cohen's d + Mann-Whitney U
   └── 3+ groups → ANOVA + η² + Tukey HSD + Kruskal-Wallis
```

## Required Inputs

| Role | What to collect |
|---|---|
| **Outcome (Y)** | Variable name, units, what it measures |
| **Group variable** | What defines groups, how many levels |
| **Predictors** | For recommendation block (not executed) |
| **Covariates** | For recommendation block (not executed) |

## Code Structure

```
PART 0: Setup & Data Loading
PART 1: Distribution Diagnostics → plot_01_distribution.png
PART 2: Primary Hypothesis Test  → plot_02_boxplot_[var].png
PART 3: Recommendation Block     → text listing additional analyses available
```

## Reporting Standards

1. p-values: "< .001" not "0.000"; exact to 3 decimals otherwise
2. Effect sizes: Cohen's d (t-test), η² (ANOVA) — always alongside p
3. 95% CIs: always for mean differences
4. Degrees of freedom: always with t and F statistics
5. Sample size: final analytic N
6. Decimal places: 2 for M/SD, 3 for p and effect sizes
7. Non-significance: "not statistically significant at α = .05" — never "no effect"
8. Normality check: Shapiro–Wilk W, p on **residuals** (not Y directly) for t-test and ANOVA; also report skewness and kurtosis. With large samples (N > 200), Shapiro–Wilk is over-sensitive — trivial deviations from normality reach significance. When N > 200, rely primarily on visual inspection (Q–Q plot) and skewness/kurtosis magnitudes; treat Shapiro–Wilk p as a supporting diagnostic, not a gatekeeper.
9. Variance homogeneity: **Levene's test** (F, p) before choosing Student's t vs Welch's t or pooled ANOVA vs Welch ANOVA. Default to Welch's t (robust to unequal variances) unless Levene p ≥ .05 and sample sizes are balanced.

## Hypothesis Tests

| Scenario | Normal (equal var) | Normal (unequal var) | Non-Normal |
|---|---|---|---|
| 2 independent groups | Student's t + Tukey HSD (optional) | Welch's t (default) | Mann-Whitney U |
| 3+ independent groups | ANOVA + Tukey HSD | **Welch ANOVA + Games-Howell** post-hoc | Kruskal-Wallis + Dunn's |

When Levene's test indicates heterogeneous variances across 3+ groups, use Welch ANOVA for the omnibus test and **Games-Howell** for pairwise comparisons — Tukey HSD assumes equal variances and inflates Type I error when variances differ. Report which post-hoc was used and why.

Paired/repeated designs → `vera-data-repeated-reviewing`.

## Example Dataset

R built-in `mtcars`: outcome = mpg, 2-group = am, 3+ group = cyl.
Python: `sm.datasets.get_rdataset("mtcars").data` (with offline fallback to bundled `examples/mtcars.csv`).

## Method Status

| Status | Methods |
|---|---|
| Implemented in this skill | Residual normality diagnostics, Levene-informed Welch / ANOVA branching, post-hoc tests, and nonparametric confirmation |
| Implemented downstream in `vera-data-continuous-generating` | Extended group comparisons, OLS, quantile regression, subgroup analysis, and exploratory tree-based models |
| Out of scope in this open-source baseline | Repeated-measures, mixed-effects, and any continuous-outcome workflow that depends on a different data structure |

## Minimal Smoke Test

- Smoke-test prompt: "Run `vera-data-continuous-reviewing` on `mtcars`, using `mpg` as the outcome and `am` as the primary grouping variable. Produce the standard baseline artifacts."

## Cross-Skill Interface

```
Output:
├── code_r      → .R script
├── code_python → .py script
├── figures/    → 2 PNGs (distribution + boxplot)
└── recommendations → text block (additional analyses available)
```

Next step: Invoke `vera-data-continuous-generating` from this skillset to run the full pipeline (additional tests, subgroup analysis, modeling, manuscript generation). See `../../CROSS-SKILL-INTERFACE.md` for the shared handoff contract.
