---
name: vera-data-count-generating
description: >-
  Server-side extension that completes the full analysis pipeline for
  count outcome variables after vera-data-count-reviewing has run. Adds
  remaining hypothesis tests (additional group comparisons, continuous
  predictor correlations), subgroup analysis with stratified rate ratios
  and interaction tests, full modeling (Poisson, Negative Binomial,
  Zero-Inflated Poisson, Zero-Inflated Negative Binomial, Hurdle,
  tree-based exploratory), and model comparison with unified variable
  importance. Generates manuscript-ready methods.md and results.md with
  formatted tables, publication-quality figures, and references.bib.
  Applies output variation and code style variation for natural, non-repetitive output. Triggered after
  vera-data-count-reviewing completes and its PART 0–2 artifacts are present
  (see ../../CROSS-SKILL-INTERFACE.md). If invoked directly without those artifacts, halts and prompts
  the user to run testing first or supply equivalent PART 0–2 code.
allowed-tools: Read, Bash, Write, Edit, Grep, Glob
---

# Count Outcome — Full Analysis & Manuscript Generation

Open-source skill. Read `reference/specs/output-variation-protocol.md`
before every generation — apply all variation layers.

## Workflow

Continues from where vera-data-count-reviewing stopped (PART 0-2 done).

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

Same as vera-data-count-reviewing, plus:
- IRR: always with 95% CI, "IRR = X.XX, 95% CI [X.XX, X.XX]"
- Rate: "X.XX events per [unit] of exposure"
- Overdispersion: report deviance/df ratio
- Poisson vs NB: LR test chi-sq(1), p
- ZIP/ZINB: Vuong test statistic, p
- Hurdle: AIC comparison + conceptual justification
- Count means: report with SD (not SE unless explicitly comparing)
- Coefficients: log-scale B with SE always; exponentiate to IRR for interpretation
- Tree-based with small N: frame as "exploratory"; never claim predictive validity
- Model selection: frame as "which distributional assumption fits the data" not "which model wins"

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

Invoked directly after `vera-data-count-reviewing` or orchestrated by `vera-data-application-pipelining`.
