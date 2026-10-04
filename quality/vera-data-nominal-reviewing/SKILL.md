---
name: vera-data-nominal-reviewing
description: >-
  Runs class distribution diagnostics and primary association tests for
  nominal (unordered multi-class) outcome variables. Produces class
  frequency table, proportions, rare-class warnings, bar chart, and one
  interpreted association test (Chi-square/Cramer's V for categorical
  predictors, or ANOVA/Kruskal-Wallis for continuous predictors) with
  effect sizes. Outputs .R and .py scripts with 2 publication-quality
  plots. Triggered when user has a nominal outcome with 3+ unordered
  levels and says "nominal outcome," "multi-class," "unordered categories,"
  "multinomial," or names a variable like species, diagnosis type, region.
  Does NOT handle binary (2-level), ordinal, continuous, count, survival,
  or SEM outcomes.
allowed-tools: Read, Bash, Write, Edit
---

# Nominal Outcome — Class Distribution Diagnostics & Primary Association Test

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
- The outcome has 3 or more unordered classes and the first task is a baseline association test plus class-distribution check.
- A descriptive / inferential starting point is needed before multinomial or classifier-style modeling.

Do not use this skill when:
- The outcome has only 2 classes or has a meaningful order.
- The main need is repeated-measures, survival, or multilevel nominal modeling.

## Workflow

Read each step file in `workflow/` before executing that step.

| Step | Responsibility | Executor | Document | Input | Output |
|---|---|---|---|---|---|
| Collect | Collect Inputs | Main Agent | `workflow/step01-collect-inputs.md` | User input | Structured input summary |
| Diagnose | Check Distribution | Main Agent | `workflow/step02-check-distribution.md` | Prior step output | PART 1 code block |
| Test | Run Primary Test | Main Agent | `workflow/step03-run-primary-test.md` | Prior step output | PART 2-3 code blocks |

## Decision Tree

```
1. VALIDATE OUTCOME TYPE
   ├── Only 2 levels → redirect to vera-data-binary-reviewing
   ├── Ordered levels → redirect to vera-data-ordinal-reviewing
   └── 3+ unordered levels → proceed

2. PRIMARY ASSOCIATION TEST
   ├── Primary predictor is categorical → Chi-square + Cramér's V
   └── Primary predictor is continuous → One-way ANOVA (predictor ~ outcome) or Kruskal-Wallis
```

## Required Inputs

| Role | What to collect |
|---|---|
| **Outcome (Y)** | Variable name, what categories represent, confirm NO ordering |
| **Number of levels** | Confirm 3+ unordered categories |
| **Primary predictor** | Variable name, type (categorical or continuous) |
| **Predictors** | For recommendation block (not executed) |
| **Covariates** | For recommendation block (not executed) |

## Code Structure

```
PART 0: Setup & Data Loading
PART 1: Class Distribution Diagnostics → plot_01_class_distribution.png
PART 2: Primary Association Test       → plot_02_association_[var].png
PART 3: Recommendation Block           → text listing additional analyses available
```

## Reporting Standards

1. p-values: "< .001" not "0.000"; exact to 3 decimals otherwise
2. Effect sizes: Cramer's V (Chi-square), eta-squared (ANOVA) — always alongside p
3. 95% CIs: always for effect sizes when available
4. Degrees of freedom: always with Chi-square and F statistics
5. Sample size: final analytic N
6. Decimal places: 2 for frequencies/proportions, 3 for p and effect sizes
7. Non-significance: "not statistically significant at alpha = .05" — never "no association"
8. Chi-square: report observed vs expected when informative
9. Always state which category is the reference (for later multinomial modeling)

## Hypothesis Tests

| Predictor Type | Primary Test | Confirmation |
|---|---|---|
| Categorical predictor | Chi-square + Cramer's V | Fisher's exact (if any cell < 5) |
| Continuous predictor | One-way ANOVA (predictor ~ outcome as factor) | Kruskal-Wallis |

## Example Dataset

R built-in `iris`: outcome = Species (setosa/versicolor/virginica, 3 unordered classes).
Predictors: Sepal.Length, Sepal.Width, Petal.Length, Petal.Width.
Python: `from sklearn.datasets import load_iris` (preferred — fully offline) or `sm.datasets.get_rdataset("iris")`.

## Method Status

| Status | Methods |
|---|---|
| Implemented in this skill | Class-distribution diagnostics, chi-square / ANOVA-style association testing, rare-class warnings |
| Implemented downstream in `vera-data-nominal-generating` | Multinomial logistic regression, LDA, CART/RF/LightGBM, subgroup analysis, and IIA diagnostics |
| Out of scope in this open-source baseline | Binary, ordinal, nested-choice, or multilevel nominal workflows not named above |

## Minimal Smoke Test

- Smoke-test prompt: "Run `vera-data-nominal-reviewing` on `iris`, treating `Species` as the outcome and `Petal.Length` as the primary predictor. Produce the standard baseline artifacts."

## Cross-Skill Interface

```
Output:
├── code_r      → .R script
├── code_python → .py script
├── figures/    → 2 PNGs (class distribution + association plot)
└── recommendations → text block (additional analyses available)
```

Next step: Invoke `vera-data-nominal-generating` from this skillset to run the full pipeline (additional tests, subgroup analysis, modeling, manuscript generation). See `../../CROSS-SKILL-INTERFACE.md` for the shared handoff contract.
