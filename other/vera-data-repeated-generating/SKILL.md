---
name: vera-data-repeated-generating
description: >-
  Server-side extension that completes the full analysis pipeline for repeated
  measures / longitudinal designs with a continuous outcome after vera-data-
  repeated-reviewing has run. Adds pairwise comparisons at each time point and
  within each group, simple effects analysis, subgroup three-way interactions,
  linear mixed models (random intercept, random slope, growth curve), GEE with
  multiple correlation structures, tree-based exploratory analysis on subject-
  level features, and model comparison with unified variable importance (0-100).
  Generates manuscript-ready methods.md and results.md with formatted tables,
  publication-quality figures, and references.bib. Applies output variation and
  code style variation for natural, non-repetitive output. Triggered after vera-
  data-repeated-reviewing completes and its PART 0–2 artifacts are present (see
  ../../CROSS-SKILL-INTERFACE.md).
allowed-tools: Read, Bash, Write, Edit, Grep, Glob
---

# Repeated Measures Outcome — Full Analysis & Manuscript Generation

Open-source skill. Read `reference/specs/output-variation-protocol.md`
before every generation — apply all variation layers.

## Workflow

Continues from where vera-data-repeated-reviewing stopped (PART 0-2 done).

| Step | Responsibility | Executor | Document | Input | Output |
|---|---|---|---|---|---|
| Additional tests | Run Additional Tests | Main Agent | `workflow/step04-run-additional-tests.md` | Prior step output | PART 3 code + prose |
| Subgroup | Analyze Subgroups | Main Agent | `workflow/step05-analyze-subgroups.md` | Prior step output | PART 4 code + prose |
| Modeling | Fit Models | Main Agent | `workflow/step06-fit-models.md` | Prior step output | PART 5 code + prose |
| Comparison | Compare Models | Main Agent | `workflow/step07-compare-models.md` | Prior step output | PART 6 code + prose |
| Manuscript | Generate Manuscript | Main Agent | `workflow/step08-generate-manuscript.md` | Prior step output | methods.md + results.md |

## Additional Inputs

Collect if not already provided:
- Target discipline (for reporting conventions)
- Target journal or style (APA 7th, STROBE, etc.)
- Research question / hypothesis
- Subgroup variable (if subgroup analysis desired)

## Output Structure

```
output/
├── methods.md
├── results.md
├── tables/             ← Markdown + CSV per table
├── figures/            ← PNGs, 300 DPI
├── references.bib
├── code.R              ← Style-varied
└── code.py             ← Style-varied
```

## Key References (read before generation)

| File | Purpose |
|---|---|
| `reference/specs/output-variation-protocol.md` | Output quality variation layers |
| `reference/specs/code-style-variation.md` | Seven-dimension code style diversity |
| `reference/patterns/sentence-bank.md` | 4-6 phrasings per result type |
| `reference/rules/reporting-standards.md` | Hard rules for statistical reporting |

## Reporting Standards

Same as vera-data-repeated-reviewing, plus:
- Fixed effects (LMM): B, SE, 95% CI, df (Satterthwaite or Kenward-Roger), t, p
- Random effects: variance components with SD, correlation if random slope
- ICC: report with interpretation
- GEE: report working correlation structure, robust SE, population-averaged coefficients
- AIC/BIC: for model comparison within LMM family (not across model types)
- Missing data: report attrition pattern, state MAR assumption if using LMM
- Tree-based with small N: frame as "exploratory"; never claim predictive validity
- Coefficients: unstandardized B with SE always; add standardized when predictors on different scales

## Cross-Skill Interface

```
Method Unit Contract:
├── code_r           → .R script (style-varied)
├── code_python      → .py script (style-varied)
├── methods_md       → methods.md (varied structure)
├── results_md       → results.md (varied phrasing)
├── tables/          → Markdown + CSV
├── figures/         → PNGs 300 DPI (varied layout)
├── references_bib   → .bib with cited references
└── comparison       → cross-method narrative (in results.md)
```

Invoked directly after `vera-data-repeated-reviewing` or orchestrated by `vera-data-application-pipelining`.
