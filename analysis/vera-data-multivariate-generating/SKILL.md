---
name: vera-data-multivariate-generating
description: >-
  Server-side extension that completes the full analysis pipeline for multiple
  continuous outcome variables after vera-data-multivariate-reviewing has run.
  Adds follow-up univariate ANOVAs with Bonferroni-corrected pairwise
  comparisons, full discriminant function analysis with classification accuracy,
  MANCOVA and two-way MANOVA, profile analysis (parallelism, equal levels,
  flatness), canonical correlation analysis, PCA for dimension reduction,
  multivariate multiple regression, and tree-based importance comparison across
  DVs. Synthesizes insights across methods and generates manuscript-ready
  methods.md and results.md with formatted tables, publication-quality figures,
  and references.bib. Applies output variation and code style variation for
  natural, non-repetitive output. Triggered after vera-data-multivariate-
  reviewing completes and its PART 0–2 artifacts are present (see ../../../..
allowed-tools: Read, Bash, Write, Edit, Grep, Glob
---

# Multivariate Outcome — Full Analysis & Manuscript Generation

Open-source skill. Read `reference/specs/output-variation-protocol.md`
before every generation — apply all variation layers.

## Workflow

Continues from where vera-data-multivariate-reviewing stopped (PART 0-2 done).

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
- Whether DVs are on same scale (for profile analysis)

## Output Structure

```
output/
├── methods.md
├── results.md
├── tables/             <- Markdown + CSV per table
├── figures/            <- PNGs, 300 DPI
├── references.bib
├── code.R              <- Style-varied
└── code.py             <- Style-varied
```

## Key References (read before generation)

| File | Purpose |
|---|---|
| `reference/specs/output-variation-protocol.md` | Output quality variation layers |
| `reference/specs/code-style-variation.md` | Seven-dimension code style diversity |
| `reference/patterns/sentence-bank.md` | 4-6 phrasings per result type |
| `reference/rules/reporting-standards.md` | Hard rules for statistical reporting |

## Reporting Standards

Same as vera-data-multivariate-reviewing, plus:
- Canonical correlations: report with Wilks' lambda significance test per dimension
- Discriminant loadings: report structure coefficients (correlations with function)
- Classification accuracy: overall and per-group hit rates
- Profile analysis: report parallelism F, equal levels F, flatness F with df and p
- PCA: report eigenvalues, proportion of variance, cumulative proportion
- Component loadings: report only loadings >= |.40| for interpretation
- Multivariate regression: Pillai's Trace for overall test, individual R-squared per DV
- Tree-based: frame as exploratory; compare importance rankings across DVs

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

Invoked directly after `vera-data-multivariate-reviewing` or orchestrated by `vera-data-application-pipelining`.
