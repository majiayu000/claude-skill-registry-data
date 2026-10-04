---
name: vera-data-timeseries-reviewing
description: >-
  Runs time series diagnostics and primary ARIMA modeling for temporal data.
  Produces time plot, ACF/PACF, seasonal decomposition, stationarity tests
  (ADF + KPSS), and one fully interpreted ARIMA model with forecast and
  prediction intervals. Identifies trend, seasonality, and non-stationarity;
  fits ARIMA/SARIMA as baseline. Advanced methods (Prophet, state-space, VAR)
  delegated to vera-data-timeseries-generating. Outputs .R and .py scripts
  with 2 publication-quality plots. Triggered when user has temporal/time
  series data and says "time series," "temporal data," "forecast," "ARIMA,"
  "seasonal," "trend," "autocorrelation," "monthly data," "daily data,"
  "quarterly," "stationarity," or names a time-indexed variable like
  sales over time, temperature, stock price, monthly passengers. Does not
  handle panel/longitudinal data (redirect to vera-data-repeated-reviewing,
  or vera-data-repeated-generating for growth-curve / mixed-model extensions),
  cross-sectional data, or spatial time series.
allowed-tools: Read, Bash, Write, Edit
---

# Time Series — Diagnostics & Primary Modeling

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
- The data are a univariate series indexed by calendar time and the first need is a classical ARIMA-style baseline.
- Trend, seasonality, stationarity, and short-horizon forecasting are the immediate priorities.

Do not use this skill when:
- The data are panel / longitudinal across subjects with few waves; use `vera-data-repeated-reviewing` or `vera-data-repeated-generating`.
- The task is multivariate cross-series modeling, regime switching, or advanced forecasting from the start.

## Workflow

Read each step file in `workflow/` before executing that step.

| Step | Responsibility | Executor | Document | Input | Output |
|---|---|---|---|---|---|
| Collect | Collect Inputs | Main Agent | `workflow/step01-collect-inputs.md` | User input | Structured input summary |
| Diagnose | Check Distribution | Main Agent | `workflow/step02-check-distribution.md` | Prior step output | PART 1 code block |
| Model | Run Primary Test | Main Agent | `workflow/step03-run-primary-test.md` | Prior step output | PART 2-3 code blocks |

## Decision Tree

```
1. STATIONARITY CHECK
   ├── Stationary (ADF p < .05 AND KPSS p ≥ .05) → fit ARIMA(p,0,q)
   ├── Non-stationary → difference, retest, fit ARIMA(p,d,q)
   └── Seasonal pattern detected → recommend SARIMA

2. MODEL SELECTION
   ├── ACF/PACF inspection → candidate ARIMA(p,d,q) orders
   ├── Auto-ARIMA for automated selection (AIC minimization)
   └── Ljung-Box residual diagnostics → confirm adequacy
```

## Required Inputs

| Role | What to collect |
|---|---|
| **Time series (Y)** | Variable name, units, what it measures |
| **Frequency** | Daily, weekly, monthly, quarterly, annual |
| **Date/time index** | Column name or implicit ordering |
| **Exogenous (optional)** | Any external predictors (for recommendation) |

## Code Structure

```
PART 0: Setup & Data Loading
PART 1: Time Series Diagnostics   → plot_01_ts_diagnostics.png
PART 2: Primary ARIMA Model       → plot_02_forecast.png
PART 3: Recommendation Block      → text listing additional analyses available
```

## Reporting Standards

1. p-values: "< .001" not "0.000"; exact to 3 decimals otherwise
2. ADF test: report test statistic + p-value + number of lags used
3. KPSS test: report test statistic + p-value + bandwidth
4. Model notation: ARIMA(p,d,q) or ARIMA(p,d,q)(P,D,Q)[s]
5. Information criteria: AIC and BIC
6. Ljung-Box: Q statistic + lag + p-value. Use **adaptive lag** = min(⌊T/5⌋, 20) where T is series length — the fixed (5, 10, 15) scheme can underdetect misspecification in short series and overtest in long ones. Report the chosen lag explicitly.
7. Forecast intervals: 80% and 95% prediction intervals
8. Accuracy metrics: RMSE, MAE, MAPE on training data
9. Decimal places: 2 for coefficients, 3 for p-values
10. Non-significance: "not statistically significant at alpha = .05" — never "no effect"

## Hypothesis Tests

| Test | Null Hypothesis | Stationary if |
|---|---|---|
| ADF (Augmented Dickey-Fuller) | Unit root present (non-stationary) | p < .05 (reject null) |
| KPSS | Series is stationary | p >= .05 (fail to reject null) |

Conflicting results → note ambiguity, proceed with differencing as conservative choice.

## Example Dataset

R built-in `AirPassengers`: monthly airline passengers 1949-1960.
Python: `sm.datasets.get_rdataset("AirPassengers")` (with offline fallback to bundled `examples/airpassengers.csv`).

## Method Status

| Status | Methods |
|---|---|
| Implemented in this skill | ADF/KPSS diagnostics, ACF/PACF-based ARIMA triage, baseline ARIMA/SARIMA fit, forecast intervals, residual checks |
| Implemented downstream in `vera-data-timeseries-generating` | ETS, GARCH, VAR, spectral analysis, regression with ARIMA errors, ML forecasting on lagged features |
| Out of scope in this open-source baseline | Panel time series, spatial time series, and forecasting families not explicitly named above |

## Minimal Smoke Test

- Smoke-test prompt: "Run `vera-data-timeseries-reviewing` on `AirPassengers`, using the passenger count as the series and monthly frequency. Produce the standard baseline artifacts."

## Cross-Skill Interface

```
Output:
├── code_r      → .R script
├── code_python → .py script
├── figures/    → 2 PNGs (diagnostics + forecast)
└── recommendations → text block (additional analyses available)
```

Next step: Invoke `vera-data-timeseries-generating` from this skillset to run the full pipeline (additional tests, subgroup analysis, modeling, manuscript generation). See `../../CROSS-SKILL-INTERFACE.md` for the shared handoff contract.
