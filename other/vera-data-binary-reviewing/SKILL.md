---
name: vera-data-binary-reviewing
description: >-
  Runs class balance diagnostics and primary association tests for binary
  outcome variables (0/1, yes/no, survived/died, pass/fail). Produces
  proportion tables, class balance check with rare-event warning,
  descriptives by outcome level, chi-square test of independence with
  Cramer's V, Fisher's exact test when cell counts are small, odds ratio
  with 95% CI, and a mosaic or grouped bar chart. Outputs .R and .py scripts with 2 publication-quality plots.
  Triggered when user has a binary/dichotomous outcome and says "binary
  outcome," "survived or died," "yes or no," "pass or fail,"
  "0/1," "classification," "binary DV," or names a binary variable like
  survived, admitted, defaulted, churned, diagnosed. Does not handle
  continuous, count, survival time, ordinal, repeated measures, or SEM.
allowed-tools: Read, Bash, Write, Edit
---

# Binary Outcome --- Class Balance Diagnostics & Association Testing

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
- The outcome is a single binary endpoint and the first need is a defensible descriptive / inferential baseline.
- The main question is a cross-sectional association or simple group comparison, not a full prediction workflow.

Do not use this skill when:
- The design is paired, matched, or otherwise within-subject; use `vera-data-repeated-reviewing`.
- The target is ordinal, nominal, count, survival, or time-to-event rather than binary.

## Workflow

Read each step file in `workflow/` before executing that step.

| Step | Responsibility | Executor | Document | Input | Output |
|---|---|---|---|---|---|
| Collect | Collect Inputs | Main Agent | `workflow/step01-collect-inputs.md` | User input | Structured input summary |
| Diagnose | Check Distribution | Main Agent | `workflow/step02-check-distribution.md` | Prior step output | PART 1 code block |
| Test | Run Primary Test | Main Agent | `workflow/step03-run-primary-test.md` | Prior step output | PART 2-3 code blocks |

## Decision Tree

```
1. CHECK CLASS BALANCE
   ├── Balanced (minority ≥ 10%) → standard tests
   └── Imbalanced (minority < 10%) → rare event warning, note power limits

2. PRIMARY ASSOCIATION TEST
   ├── All cells ≥ 5 → Chi-square + Cramer's V + OR
   └── Any cell < 5 → Fisher's exact + OR
```

## Required Inputs

| Role | What to collect |
|---|---|
| **Outcome (Y)** | Variable name, what 0/1 represents |
| **Primary group variable** | What defines groups, how many levels |
| **Predictors** | For recommendation block (not executed) |
| **Covariates** | For recommendation block (not executed) |

## Code Structure

```
PART 0: Setup & Data Loading
PART 1: Class Balance Diagnostics  → plot_01_class_balance.png
PART 2: Primary Association Test   → plot_02_mosaic_[var].png
PART 3: Recommendation Block       → text listing additional analyses available
```

## Reporting Standards

1. p-values: "< .001" not "0.000"; exact to 3 decimals otherwise
2. Effect sizes: Cramer's V (chi-square), odds ratio with 95% CI
3. Odds ratios: always as "OR = X.XX, 95% CI [X.XX, X.XX]"
4. Proportions: report as percentages with 1 decimal
5. Chi-square: chi-sq(df) = X.XX, p = .XXX, Cramer's V = .XXX
6. Degrees of freedom: always with chi-square statistic
7. Sample size: final analytic N
8. Decimal places: 1 for proportions, 2 for OR, 3 for p and effect sizes
9. Non-significance: "not statistically significant at alpha = .05" --- never "no association"

## Hypothesis Tests

| Scenario | Expected cells all >= 5 | Any expected cell < 5 |
|---|---|---|
| 2x2 or 2xK | Chi-square + Cramer's V | Fisher's exact test |

Paired/matched binary designs -> `vera-data-repeated-reviewing` (handles within-subject comparisons including paired binary data via McNemar's test).

## Example Dataset

R built-in `Titanic` (convert to data frame): outcome = Survived (0/1), predictors = Class, Sex, Age.
Python: `sm.datasets.get_rdataset("Titanic").data` or reconstruct from counts (offline fallback uses base R `Titanic` dataset).

## Method Status

| Status | Methods |
|---|---|
| Implemented in this skill | Class-balance diagnostics, chi-square / Fisher's exact testing, Cramer's V, odds ratio with 95% CI |
| Implemented downstream in `vera-data-binary-generating` | Additional association tests, stratified odds ratios, logistic regression, ROC/AUC summaries, exploratory tree-based models |
| Out of scope in this open-source baseline | Matched binary workflows, causal estimands, and any binary method not named above |

## Minimal Smoke Test

- Smoke-test prompt: "Run `vera-data-binary-reviewing` on `Titanic`, treating `Survived` as the outcome and `Sex` as the primary grouping variable. Produce the standard baseline artifacts."

## Cross-Skill Interface

```
Output:
├── code_r      → .R script
├── code_python → .py script
├── figures/    → 2 PNGs (class balance + mosaic/grouped bar)
└── recommendations → text block (additional analyses available)
```

Next step: Invoke `vera-data-binary-generating` from this skillset to run the full pipeline (additional tests, subgroup analysis, modeling, manuscript generation). See `../../CROSS-SKILL-INTERFACE.md` for the shared handoff contract.
