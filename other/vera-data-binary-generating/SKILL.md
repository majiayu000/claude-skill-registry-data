---
name: vera-data-binary-generating
description: >-
  Server-side extension that completes the full analysis pipeline for binary
  outcome variables after vera-data-binary-reviewing has run. Adds remaining
  association tests (chi-square/Fisher's for additional predictors, point-
  biserial for continuous predictors), stratified odds ratio analysis with
  Breslow-Day test and forest plot, full modeling (logistic regression with OR
  and 95% CI, Hosmer-Lemeshow GOF, pseudo-R2, ROC curve with AUC, classification
  table, tree-based classification with CART/RF/GBM), and cross-method variable
  importance comparison on a 0-100 unified scale. Generates manuscript-ready
  methods.md and results.md with formatted tables, publication-quality figures,
  and references.bib. Applies output variation and code style variation for
  natural, non-repetitive output. Triggered after vera-data-binary-reviewing
  completes and its PART 0–2 artifacts (code.R, code.
allowed-tools: Read, Bash, Write, Edit, Grep, Glob
---

# Binary Outcome --- Full Analysis & Manuscript Generation

Open-source skill. Read `reference/specs/output-variation-protocol.md`
before every generation --- apply all variation layers.

## Workflow

Continues from where vera-data-binary-reviewing stopped (PART 0-2 done).

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

Same as vera-data-binary-reviewing, plus:
- Logistic coefficients: report OR (not raw B) in results text; raw B with SE in supplementary table
- Pseudo-R2: report McFadden and Nagelkerke; say "the model accounted for" --- never "explained"
- AUC: report with 95% CI; note "in-sample" if no cross-validation performed
- Classification: report sensitivity, specificity, and threshold used
- Tree-based with small N: frame as "exploratory"; never claim predictive validity
- Hosmer-Lemeshow: report chi-sq, df, p; non-significant = adequate fit. HL is known to have low power with large N — when N > 1000, supplement with a calibration plot (predicted vs observed, loess-smoothed) and report Brier score.
- **Rare events or quasi-separation** (minority < 10% OR any model coefficient |β| > 5 with very wide SE): switch to **Firth's penalized likelihood** (`logistf` in R; `statsmodels` with `method='bfgs'` + bias-reduction, or the `firthlogist` package in Python). Report Firth-penalized OR with profile-likelihood 95% CI. Flag in the manuscript that standard ML estimates were unstable and Firth was used.

## Classification Threshold

Default threshold is 0.5 (balanced misclassification cost). Adjust only when justified:
- **Youden's J** (maximizes sensitivity + specificity − 1): use when sens and spec are equally important.
- **Cost-optimal threshold** (minimizes expected loss given cost ratio): use when FP and FN have documented asymmetric costs (e.g., medical screening, fraud detection).
- Always report the threshold used and, when non-default, state the objective (Youden, cost ratio C_FP:C_FN).

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

Invoked directly after `vera-data-binary-reviewing` or orchestrated by `vera-data-application-pipelining`.
