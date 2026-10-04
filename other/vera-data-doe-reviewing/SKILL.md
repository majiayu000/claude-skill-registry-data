---
name: vera-data-doe-reviewing
description: >-
  Runs distribution diagnostics and primary analysis for designed experiments
  (DOE) with controlled factors. Produces cell descriptives, balance check,
  residual normality, Levene's test, full factorial ANOVA (Type III SS) with
  partial eta-squared, interaction plots, and Tukey HSD / simple effects
  post-hoc. Outputs .R and .py scripts with 2
  publication-quality plots. Triggered when user mentions "experimental
  design," "DOE," "factorial design," "treatment effects," "blocking,"
  "randomized experiment," "split-plot," "response surface," "2^k factorial,"
  "main effects and interactions," "Latin square," "fractional factorial,"
  "CRD," "RCBD," or describes manipulated factors. Fractional factorial
  and RSM are identified and flagged; full design-resolution analysis
  delegated to vera-data-doe-generating. Does not handle observational
  studies, repeated measures, or SEM outcomes.
allowed-tools: Read, Bash, Write, Edit
---

# Design of Experiments — Diagnostics & Primary Analysis

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
- The data come from a designed experiment with controlled factors and a clear error structure.
- A baseline factorial ANOVA-style analysis is the right first check before optimization or alias-structure work.

Do not use this skill when:
- The study is observational rather than experimental.
- The main need is repeated-measures, longitudinal, or SEM modeling rather than DOE analysis.

## Workflow

Read each step file in `workflow/` before executing that step.

| Step | Responsibility | Executor | Document | Input | Output |
|---|---|---|---|---|---|
| Collect | Collect Inputs | Main Agent | `workflow/step01-collect-inputs.md` | User input | Structured input summary |
| Diagnose | Check Distribution | Main Agent | `workflow/step02-check-distribution.md` | Prior step output | PART 1 code block |
| Test | Run Primary Test | Main Agent | `workflow/step03-run-primary-test.md` | Prior step output | PART 2-3 code blocks |

## Decision Tree

```
1. CHECK DESIGN
   ├── Balanced (equal N per cell) → standard ANOVA
   └── Unbalanced → Type III SS mandatory

2. CHECK RESIDUALS
   ├── Normal residuals + equal variances → factorial ANOVA
   └── Non-normal / heteroscedastic → flag, proceed with caution + recommend transformations

3. FACTORIAL ANOVA
   ├── Significant main effects → Tukey HSD post-hoc
   └── Significant interactions → simple effects analysis
```

## Required Inputs

| Role | What to collect |
|---|---|
| **Response (Y)** | Variable name, units, what it measures |
| **Factors** | Names, levels, type (fixed/random) |
| **Design type** | CRD, RCBD, factorial, fractional, **split-plot**, Latin square — if split-plot, identify the whole-plot factor and sub-plot factor explicitly, because the design requires **two separate error terms** (whole-plot error and sub-plot error); analyzing them against a single pooled error inflates Type I error on the whole-plot factor and deflates it on the sub-plot factor. Generated code MUST specify `Error(whole_plot_id / sub_plot_factor)` in R's `aov()` or `random = ~1 | whole_plot_id` in `lme()`. |
| **Blocking variable** | If RCBD or similar |
| **Replication info** | Replicates per cell, total N |

## Code Structure

```
PART 0: Setup & Data Loading
PART 1: Design Diagnostics        → plot_01_interaction.png
PART 2: Factorial ANOVA + Post-hoc → plot_02_effects.png
PART 3: Recommendation Block       → text listing additional analyses available
```

## Reporting Standards

1. p-values: "< .001" not "0.000"; exact to 3 decimals otherwise
2. Effect sizes: partial eta-squared always alongside F-tests
3. SS Type III always for unbalanced designs
4. F(df1, df2) = X.XX, p, partial eta-squared
5. Effect estimates with SE
6. Degrees of freedom: always with F statistics
7. Sample size: final analytic N and cell sizes
8. Decimal places: 2 for M/SD, 3 for p and effect sizes
9. Non-significance: "not statistically significant at alpha = .05" -- never "no effect"
10. Design resolution for fractional factorial (in recommendation)

## Hypothesis Tests

| Scenario | Method |
|---|---|
| Main effects | F-test from factorial ANOVA |
| Interactions | F-test for each interaction term |
| Post-hoc (main effects) | Tukey HSD (all pairwise) |
| Post-hoc (interactions) | Simple effects (effect of A at each level of B) |
| Variance homogeneity | Levene's test |
| Residual normality | Shapiro-Wilk on residuals |

## Example Dataset

R built-in `npk`: 24 observations, N/P/K fertilizer treatments (2^3 factorial)
on pea yield, blocked by block. Classic agricultural DOE.
Python: `sm.datasets.get_rdataset("npk").data` (with offline fallback to bundled `examples/npk.csv`).

Alternative: `warpbreaks` -- wool x tension factorial on breaks.

## Method Status

| Status | Methods |
|---|---|
| Implemented in this skill | Design-balance checks, residual diagnostics, factorial ANOVA, Tukey HSD, and simple-effects escalation triggers |
| Implemented downstream in `vera-data-doe-generating` | RSM, fractional-factorial alias analysis, split-plot handling, desirability optimization, and exploratory trees |
| Out of scope in this open-source baseline | Observational causal modeling and experimental workflows not grounded in a named DOE design |

## Minimal Smoke Test

- Smoke-test prompt: "Run `vera-data-doe-reviewing` on `npk`, treating `yield` as the response and `N`, `P`, and `K` as the factorial treatments. Produce the standard baseline artifacts."

## Cross-Skill Interface

```
Output:
├── code_r      → .R script
├── code_python → .py script
├── figures/    → 2 PNGs (interaction plot + effects plot)
└── recommendations → text block (additional analyses available)
```

Next step: Invoke `vera-data-doe-generating` from this skillset to run the full pipeline (additional tests, subgroup analysis, modeling, manuscript generation). See `../../CROSS-SKILL-INTERFACE.md` for the shared handoff contract.
