---
name: vera-data-multivariate-reviewing
description: >-
  Multivariate diagnostics and primary hypothesis tests for multiple continuous
  outcomes analyzed simultaneously. Produces multivariate normality (Mardia,
  Henze-Zirkler), Box's M test, scatterplot matrix, correlation matrix, and one
  multivariate group comparison (Hotelling's T-squared for 2 groups or one-way
  MANOVA with all four test statistics for 3+ groups) with partial eta-squared
  per DV and univariate follow-up ANOVAs. Ends with a recommendation block.
  Outputs .R and .py scripts with publication-quality plots. Handles group-
  difference tests on 2+ continuous dependent variables (Hotelling's T², MANOVA,
  one-way MANOVA). Dimensionality-reduction methods (PCA, factor analysis) and
  canonical correlation are delegated to vera-data-multivariate-generating.
allowed-tools: Read, Bash, Write, Edit
---

# Multivariate Outcome — Distribution Diagnostics & Hypothesis Testing

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
- There are multiple continuous outcomes that should be tested jointly before decomposing into separate univariate models.
- A baseline Hotelling / MANOVA analysis is appropriate before dimension reduction or multivariate modeling.

Do not use this skill when:
- There is only one dependent variable.
- The data are repeated / longitudinal, SEM-based, or primarily exploratory dimension-reduction from the outset.

## Workflow

Read each step file in `workflow/` before executing that step.

| Step | Responsibility | Executor | Document | Input | Output |
|---|---|---|---|---|---|
| Collect | Collect Inputs | Main Agent | `workflow/step01-collect-inputs.md` | User input | Structured input summary |
| Diagnose | Check Distribution | Main Agent | `workflow/step02-check-distribution.md` | Prior step output | PART 1 code block |
| Test | Run Primary Test | Main Agent | `workflow/step03-run-primary-test.md` | Prior step output | PART 2-3 code blocks |

## Decision Tree

```
1. CHECK MULTIVARIATE DISTRIBUTION
   ├── Mardia skewness p >= .05 AND Mardia kurtosis p >= .05 → multivariate normal
   └── Either p < .05 → note violation, Pillai's Trace is robust

2. CHECK COVARIANCE EQUALITY
   ├── Box's M p >= .001 (strict alpha) → covariance matrices equal
   └── Box's M p < .001 → note violation, Pillai's Trace is robust

3. GROUP COMPARISON
   ├── 2 groups → Hotelling's T² + F approximation + individual ANOVAs
   └── 3+ groups → One-way MANOVA (all 4 statistics) + discriminant follow-up
```

## Required Inputs

| Role | What to collect |
|---|---|
| **Outcomes (Y₁..Yₖ)** | 2+ continuous variable names, what they measure |
| **Group variable** | What defines groups, how many levels |
| **Predictors** | For recommendation block (not executed) |
| **Covariates** | For recommendation block (not executed) |

## Code Structure

```
PART 0: Setup & Data Loading
PART 1: Multivariate Distribution Diagnostics → plot_01_scattermatrix.png
PART 2: Primary Multivariate Test             → plot_02_groupmeans.png
PART 3: Recommendation Block                  → text listing additional analyses available
```

## Reporting Standards

1. p-values: "< .001" not "0.000"; exact to 3 decimals otherwise
2. Effect sizes: partial eta-squared per DV in follow-up ANOVAs
3. 95% CIs: always for mean differences in univariate follow-ups
4. Degrees of freedom: always with F statistics
5. Sample size: final analytic N
6. Decimal places: 2 for M/SD, 3 for p and effect sizes
7. Non-significance: "not statistically significant at alpha = .05" — never "no effect"
8. MANOVA statistics: report all four (Pillai's V, Wilks' Lambda, Hotelling-Lawley T, Roy's theta) with F approximation and p
9. Box's M: report with F approximation and p, use strict alpha (.001). **Caveat:** Box's M is notoriously sensitive to deviations from multivariate normality — a significant result may reflect non-normality rather than true covariance heterogeneity. When Box's M rejects AND Mardia/Henze–Zirkler also indicate non-normality, do NOT conclude covariance heterogeneity on Box's M alone. Instead: (a) report Pillai's Trace as the primary MANOVA statistic (most robust to assumption violations), and (b) consider log/Box–Cox transformation or a robust MANOVA variant before interpreting Box's M as a substantive result.

## Hypothesis Tests

| Scenario | Test | Follow-Up |
|---|---|---|
| 2 independent groups | Hotelling's T² | Individual Welch's t per DV |
| 3+ independent groups | One-way MANOVA | Individual ANOVAs per DV |

Paired/repeated multivariate → `vera-data-repeated-reviewing`.
Single DV → `vera-data-continuous-reviewing`.

## Example Dataset

R built-in `iris`: outcomes = Sepal.Length, Sepal.Width, Petal.Length, Petal.Width; group = Species.
Python: `from sklearn.datasets import load_iris`.

## Method Status

| Status | Methods |
|---|---|
| Implemented in this skill | Multivariate normality / covariance checks, Hotelling's T-squared, one-way MANOVA, and univariate follow-up triggers |
| Implemented downstream in `vera-data-multivariate-generating` | MANCOVA, DFA, profile analysis, canonical correlation, PCA, multivariate regression, and exploratory trees |
| Out of scope in this open-source baseline | Repeated multivariate models and latent-variable multivariate frameworks |

## Minimal Smoke Test

- Smoke-test prompt: "Run `vera-data-multivariate-reviewing` on `iris`, using the four measurement columns as outcomes and `Species` as the grouping variable. Produce the standard baseline artifacts."

## Cross-Skill Interface

```
Output:
├── code_r      → .R script
├── code_python → .py script
├── figures/    → 2 PNGs (scattermatrix + group means)
└── recommendations → text block (additional analyses available)
```

Next step: Invoke `vera-data-multivariate-generating` from this skillset to run the full pipeline (additional tests, subgroup analysis, modeling, manuscript generation). See `../../CROSS-SKILL-INTERFACE.md` for the shared handoff contract.
