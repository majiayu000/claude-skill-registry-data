---
name: vera-data-count-reviewing
description: >-
  Runs distribution diagnostics and primary hypothesis tests for count
  outcome variables (non-negative integers with no upper bound). Produces
  frequency table, overdispersion assessment, bar chart of count
  distribution with Poisson overlay, and one fully interpreted group
  comparison (Poisson/NB rate test or regression with LR test) with
  incidence rate ratios. Detects zero-inflation and overdispersion, flags
  for zero-inflated models in full analysis. Outputs .R and .py scripts
  with 2 publication-quality plots. Triggered when user has a
  count/frequency outcome and says "count outcome," "number of events,"
  "Poisson," "incidents," "rate," "per capita." Does not handle binary,
  continuous, survival, ordinal, repeated measures, or SEM outcomes.
allowed-tools: Read, Bash, Write, Edit
---

# Count Outcome — Distribution Diagnostics & Hypothesis Testing

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
- The outcome is a non-negative count or rate and the first task is distributional triage plus one primary group comparison.
- Exposure / offset handling can be represented as a simple baseline choice between count and rate formulations.

Do not use this skill when:
- The outcome is bounded binary, continuous, ordered categorical, survival time, or repeated within subject.
- The question already requires zero-inflated, hurdle, or multivariable count modeling as the primary analysis.

## Workflow

Read each step file in `workflow/` before executing that step.

| Step | Responsibility | Executor | Document | Input | Output |
|---|---|---|---|---|---|
| Collect | Collect Inputs | Main Agent | `workflow/step01-collect-inputs.md` | User input | Structured input summary |
| Diagnose | Check Distribution | Main Agent | `workflow/step02-check-distribution.md` | Prior step output | PART 1 code block |
| Test | Run Primary Test | Main Agent | `workflow/step03-run-primary-test.md` | Prior step output | PART 2-3 code blocks |

## Decision Tree

```
1. CHECK COUNT TYPE
   ├── Exposure variable exists → rate model path (offset = log(exposure))
   └── No exposure variable → count model path

2. CHECK DISTRIBUTION
   ├── Variance ≈ Mean (ratio < 1.5) → Poisson
   ├── Variance >> Mean (ratio ≥ 1.5) → Negative Binomial
   └── Excess zeros (>20%) → flag for Zero-Inflated models
   # 1.5 dispersion threshold: common rule of thumb; equivalent to a Pearson-chi²/df ≈ 1.5
   # cutoff. Some sources use 1.2; others use a test-based decision (overdispersion LR test).
   # 1.5 is chosen here as a conservative trigger that flags the full analysis skill.
   # 20% zero threshold: empirical convention — below this, Poisson/NB handle zeros adequately;
   # above this, zero-inflation is often driven by a distinct generating process and warrants ZIP/ZINB.

3. GROUP COMPARISON
   ├── 2 groups → Poisson/NB rate test + IRR + Mann-Whitney U
   └── 3+ groups → Poisson/NB regression with group factor + LR test + Kruskal-Wallis
```

## Required Inputs

| Role | What to collect |
|---|---|
| **Outcome (Y)** | Variable name, what it counts, units |
| **Group variable** | What defines groups, how many levels |
| **Exposure/offset** | Time at risk, population, area — or none |
| **Predictors** | For recommendation block (not executed) |
| **Covariates** | For recommendation block (not executed) |

## Code Structure

```
PART 0: Setup & Data Loading
PART 1: Distribution Diagnostics → plot_01_count_distribution.png
PART 2: Primary Hypothesis Test  → plot_02_mean_counts_[var].png
PART 3: Recommendation Block     → text listing additional analyses available
```

## Reporting Standards

1. p-values: "< .001" not "0.000"; exact to 3 decimals otherwise
2. Effect sizes: incidence rate ratio (IRR) with 95% CI — always alongside p
3. Overdispersion: report variance/mean ratio with interpretation
4. Rate: "X.XX events per [unit] of exposure" when applicable
5. Degrees of freedom: always with chi-square and LR test statistics
6. Sample size: final analytic N
7. Decimal places: 2 for means/SDs, 3 for p and IRR, 2 for rate ratios
8. Non-significance: "not statistically significant at α = .05" — never "no effect"

## Hypothesis Tests

| Scenario | Equidispersed | Overdispersed |
|---|---|---|
| 2 independent groups | Poisson rate test | Negative binomial test |
| 3+ independent groups | Poisson regression + LR test | NB regression + LR test |

Nonparametric confirmation: Mann-Whitney U (2 groups) or Kruskal-Wallis (3+).

Paired/repeated designs → `vera-data-repeated-reviewing`.

## Example Dataset

R built-in `warpbreaks`: outcome = breaks (count), predictors: wool (A/B), tension (L/M/H).
Python: `sm.datasets.get_rdataset("warpbreaks").data` (with offline fallback to bundled `examples/warpbreaks.csv`).

## Method Status

| Status | Methods |
|---|---|
| Implemented in this skill | Overdispersion and zero-inflation triage, Poisson / negative-binomial primary testing, incidence-rate-ratio reporting |
| Implemented downstream in `vera-data-count-generating` | ZIP, ZINB, hurdle models, subgroup rate-ratio analysis, and exploratory tree-based count comparisons |
| Out of scope in this open-source baseline | Longitudinal count models, causal count estimands, and count families not explicitly named here |

## Minimal Smoke Test

- Smoke-test prompt: "Run `vera-data-count-reviewing` on `warpbreaks`, using `breaks` as the outcome and `wool` as the primary grouping variable. Produce the standard baseline artifacts."

## Cross-Skill Interface

```
Output:
├── code_r      → .R script
├── code_python → .py script
├── figures/    → 2 PNGs (count distribution + mean counts bar chart)
└── recommendations → text block (additional analyses available)
```

Next step: Invoke `vera-data-count-generating` from this skillset to run the full pipeline (additional tests, subgroup analysis, modeling, manuscript generation). See `../../CROSS-SKILL-INTERFACE.md` for the shared handoff contract.
