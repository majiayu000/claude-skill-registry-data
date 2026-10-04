---
name: vera-data-timeseries-generating
description: >-
  Server-side extension that completes the full analysis pipeline for
  time series data after vera-data-timeseries-reviewing has run. Adds
  SARIMA, exponential smoothing (ETS/Holt-Winters), structural break
  tests, Granger causality, subseries and rolling window analysis,
  regime detection, full classical model suite (ARIMA, SARIMA, ETS,
  GARCH, VAR, spectral, regression with ARIMA errors), ML-based
  forecasting (RF + LightGBM on lagged features), and cross-method
  forecast comparison. Generates manuscript-ready methods.md and
  results.md with formatted tables, publication-quality figures, and
  references.bib. Applies output variation and code style variation for natural, non-repetitive output. Triggered after
  vera-data-timeseries-reviewing completes and its PART 0–2 artifacts are present
  (see ../../CROSS-SKILL-INTERFACE.md). If invoked directly without those artifacts, halts and prompts
  the user to run testing first or supply equivalent PART 0–2 code.
allowed-tools: Read, Bash, Write, Edit, Grep, Glob
---

# Time Series — Full Analysis & Manuscript Generation

## Table of Contents

- [Workflow](#workflow)
- [Additional Inputs](#additional-inputs)
- [Output Structure](#output-structure)
- [Key References (read before generation)](#key-references-read-before-generation)
- [Reporting Standards](#reporting-standards)
- [Cross-Validation for Time Series (Mandatory)](#cross-validation-for-time-series-mandatory)
- [Cross-Skill Interface](#cross-skill-interface)


Open-source skill. Read `reference/specs/output-variation-protocol.md`
before every generation — apply all variation layers.

## Workflow

Continues from where vera-data-timeseries-reviewing stopped (PART 0-2 done).

| Step | Responsibility | Executor | Document | Input | Output |
|---|---|---|---|---|---|
| Additional tests | Run Additional Tests | Main Agent | `workflow/step04-run-additional-tests.md` | Prior step output | PART 3 code + prose |
| Subseries | Analyze Subgroups | Main Agent | `workflow/step05-analyze-subgroups.md` | Prior step output | PART 4 code + prose |
| Modeling | Fit Models | Main Agent | `workflow/step06-fit-models.md` | Prior step output | PART 5 code + prose |
| Comparison | Compare Models | Main Agent | `workflow/step07-compare-models.md` | Prior step output | PART 6 code + prose |
| Manuscript | Generate Manuscript | Main Agent | `workflow/step08-generate-manuscript.md` | Prior step output | methods.md + results.md |

## Additional Inputs

Collect if not already provided:
- Target discipline (for reporting conventions)
- Target journal or style (APA 7th, STROBE, etc.)
- Research question / hypothesis
- Forecast horizon (if not set in initial testing)
- Whether volatility modeling is relevant
- Whether cross-series relationships exist

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

Same as vera-data-timeseries-reviewing, plus:
- Model order notation: always ARIMA(p,d,q)(P,D,Q)[s] for seasonal models
- AIC/BIC: report for all fitted models for comparability
- Ljung-Box: report on residuals for every fitted model
- GARCH: report ARCH-LM test before fitting, conditional variance equation
- VAR: report lag selection criteria (AIC, BIC, HQ), Granger causality p-values
- Spectral: report dominant frequency, corresponding period, and power
- Forecast accuracy: RMSE, MAE, MAPE on hold-out set — frame as "which assumptions fit" not "which model wins"
- Tree-based with time series: frame as "exploratory"; never claim superiority over statistical models

## Cross-Validation for Time Series (Mandatory)

Standard k-fold CV **leaks future into past** and MUST NOT be used on temporal data. All validation and hyperparameter tuning for this skill uses one of:

1. **Rolling-origin (fixed-size) forecast evaluation**: at each split, fit on `data[t−w : t]` (fixed window w) and forecast `data[t+1 : t+h]`; slide t forward. Recommended when the underlying process is approximately stationary.
2. **Expanding-window forecast evaluation**: fit on `data[0 : t]` (growing) and forecast `data[t+1 : t+h]`. Recommended when more history helps the model.

Implementations: `sklearn.model_selection.TimeSeriesSplit` (Python), `tscv::rolling_origin` or `tsibble::stretch_tsibble` (R). Report the scheme used, window size w, horizon h, and number of splits. Never shuffle time-indexed data prior to split.

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

Invoked directly after `vera-data-timeseries-reviewing` or orchestrated by `vera-data-application-pipelining`.
