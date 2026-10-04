---
name: event-study-cars
description: >-
  Complete methodology for computing publication-quality cumulative abnormal returns with
  proper event-study test statistics, matching the robustness of Kaspereit's eventstudy2 for
  Stata. Covers dateline construction, event-date mapping, estimation and event windows,
  thin-trading adjustment, OLS with Theil prediction error correction, abnormal return
  computation, CAR/CAAR/AAR accumulation, boundary contamination guards, and common tests such
  as Patell, BMP, Kolari-Pynnonen, generalized sign, Wilcoxon, and GRANK-T. Use when the user
  mentions abnormal returns, event windows, market-model regressions, CARs, CAAR, AAR,
  eventstudy2, thin trading, trade-to-trade returns, or event-study test statistics.
---

# Event Study: Cumulative Abnormal Returns (CARs)

A complete methodology reference for computing publication-quality CARs with
robust test statistics, matching the rigor of Kaspereit's eventstudy2 (v3.2b)
for Stata. This skill is **generic** — applicable to any market, asset class,
or event type.

## Use the shipped engine first (do not rewrite it)

`scripts/eventstudy.py` is a complete, runnable Python replication of
eventstudy2, validated against the Stata package to floating-point precision
(AR ~1e-8, CAR ~6e-8, CAAR and the implemented test statistics ~1e-7) on a
generic CRSP sample across all four models (FM, COMEAN, MA, RAW). It is generic —
all column names, the model, windows, thin-trading, and log handling are CLI
flags. When a user wants CARs computed, **run this engine**; do not author a new
pipeline.

```bash
python scripts/eventstudy.py --selftest          # synthetic self-check, no inputs
python scripts/eventstudy.py \
    --returns returns.csv --market market.csv --events events.csv \
    --id-col permno --ret-col ret --event-date-col event_date --mkt-col vwretd \
    --model FM --car-windows "-1,1;-5,5;-10,10" \
    --eswlb -250 --eswub -30 --evwlb -10 --evwub 10 --out-dir out/
```

Inputs are CSV/Parquet: returns (`id, date, ret`), market/factors
(`date, mkt[, factors]`), events (`id, event_date`). Outputs: `ar_panel.csv`,
`car_panel.csv`, `test_statistics.csv`. Requires numpy/pandas/scipy. Run
`--help` for all flags (`--factor-cols smb,hml`, `--model MA`,
`--no-thin-trading`, ...). The sections below document the methodology the engine
implements; read them to audit, extend, or port it.

## Methodology Overview: The 8-Step Pipeline

### Step 1: Build Trading Calendar (Dateline)

Construct a master list of valid trading dates from the security returns file.

1. Collect all unique dates on which at least one security has a non-missing
   return (or, if using a factor model, dates where market/factor returns exist).
2. Count the number of securities with valid returns on each date.
3. Optionally drop weekends (`delweekend`).
4. Apply `dateline_threshold`: drop dates where the count of return
   observations falls below `threshold × mean(daily_count)`. A threshold of
   0.2 works well for international samples with heterogeneous holidays.
5. The resulting date vector is the **dateline** — all downstream windows are
   defined in dateline time (relative trading days), not calendar time.

### Step 2: Map Event Dates to Nearest Valid Trading Day

For each event:
1. Find the nearest dateline date **on or after** the event date.
2. If the shift exceeds `max_shift` calendar days (default: 3), **exclude**
   the event entirely — do not silently map it to a distant trading day.
3. Events with missing dates, or dates outside the dateline range, are also
   excluded and logged with the reason.

### Step 3: Construct Estimation and Event Windows

For each firm-event pair, define windows in **relative trading time** (offsets
from the event day on the dateline):

- **Estimation window**: `[esw_lb, esw_ub]` — default `[-250, -30]`.
- **Event window**: `[evw_lb, evw_ub]` — determined by the widest CAR window
  requested.
- Enforce a **gap** between the estimation and event windows to prevent event
  contamination of the benchmark model.

**Exclusion checks** (per firm-event):
- Insufficient estimation-window observations (fewer than `min_esw_obs`,
  default 120).
- Insufficient event-window observations.
- **IPO/delisting guard**: if the stock's first observed return date falls
  after `evw_lb` or last observed return date falls before `evw_ub`, exclude
  the firm-event. These are survivorship-biased observations.

### Step 4: Apply Thin-Trading Adjustment

For markets with non-trivially thin trading (most markets outside US
mega-caps), apply the Maynes-Rumsey (1993) trade-to-trade transformation
**by default**.

> Read `references/thin_trading.md` for the complete transformation, including
> the `cum_periods` construction, the regression specification with `nocons`,
> and the boundary contamination guard.

**Summary**: Non-trading days accumulate into the next trading day's return.
All variables (returns, factors, intercept) are divided by `sqrt(cum_periods)`.
OLS is run with `nocons` because the intercept regressor `1/sqrt(d)` replaces
the standard constant. This is a GLS correction for the heteroscedasticity
introduced by multi-period returns.

### Step 5: Run OLS and Compute STDF

For each firm-event pair, estimate the benchmark model over the estimation
window and compute the **standard deviation of forecast** (STDF) for every
observation (estimation + event window).

> Read `references/estimation_models.md` for model specifications (RAW,
> COMEAN, MA, FM, BHAR).

**STDF** (Theil 1971 prediction error correction):

For each observation t, the forecast standard deviation is:

    STDF_it = sigma_hat_i * sqrt(1 + x'_t (X'X)^{-1} x_t)

where `x_t` is the regressor vector at time t, `X` is the estimation-window
design matrix, and `sigma_hat_i = sqrt(SSR / (T_i - 2 - df))` is the OLS
residual standard deviation. `df` is the number of additional factors beyond
the market (0 for market model, 2 for FF3, etc.).

The STDF accounts for both the inherent noise in returns (sigma) and the
estimation uncertainty in the model coefficients (which grows when event-window
factor values are far from estimation-window means).

**Python**: after `numpy.linalg.lstsq`, compute the hat matrix
`H = X @ inv(X'X) @ X'` and `h_t = x'_t @ inv(X'X) @ x_t` for each
event-window observation. Then `STDF_t = sigma_hat * sqrt(1 + h_t)`.

### Step 6: Compute Abnormal Returns

    AR_it = R_it - predicted_it

where `predicted_it` comes from the estimated benchmark model applied to
event-window factor values.

**Critical rule**: do NOT zero-fill missing event-window returns. A missing
return means the stock did not trade — setting it to zero biases CARs toward
zero for illiquid stocks. Leave it as NaN and let the accumulation step handle
the count of valid ARs.

### Step 7: Accumulate CARs

For each requested CAR window `[lb, ub]` and each firm-event:

    CAR_i = sum of AR_it for t in [lb, ub] where AR_it is not NaN

**Boundary contamination guard** (from eventstudy2):
- If the **first** day of the CAR window has `cum_periods > 1`, the return on
  that day spans back before the window start. Set CAR = NaN.
- If the **last** day of the CAR window has a missing AR, the firm-event
  lacks coverage at the window boundary. Set CAR = NaN.
- For AAR (day-by-day) output: any day with `cum_periods > 1` has its AR set
  to NaN (the multi-period return cannot be attributed to a single day).

Track `n_valid_ar` per CAR: the count of non-NaN ARs in the window. A valid
CAR should have `n_valid_ar == window_length`. CARs with fewer valid days
should be flagged or excluded depending on the analysis.

### Step 8: Compute Test Statistics

Compute at minimum: **Patell (1976)**, **BMP (Boehmer et al. 1991)**,
**Kolari-Pynnonen adjusted BMP**, and the **generalized sign test (Cowan
1992)**. For maximum rigor, compute all 13 tests.

> Read `references/test_statistics.md` for exact formulas, null hypotheses,
> distributions, and Python implementation notes for all 13 tests.

> Read `references/kolari_pynnonen.md` for the cross-correlation adjustment
> procedure (ADJ factor) and the GRANK-T test.

Test statistics are reported at two levels:
- **AAR level**: one test statistic per event day (tests whether the average
  AR across firms is significantly different from zero on that day).
- **CAAR level**: one test statistic per CAR window (tests whether the
  cumulative average AR is significantly different from zero over the window).

---

## Model Selection

> Read `references/estimation_models.md` for full mathematical specifications.

| Model | When to Use |
|-------|-------------|
| **RAW** | Baseline/diagnostic only. No benchmark subtracted. |
| **COMEAN** | Simplest parametric benchmark (constant mean return). |
| **MA** (market-adjusted) | When factor data is unavailable. Subtracts market return directly. |
| **FM** (factor model) | Standard choice for short-window event studies. Market model (1 factor) or FF3/FF5/Carhart (multi-factor). |
| **BHAR** | Long-horizon event studies (months/years). Requires skewness-adjusted bootstrap (Lyon et al. 1999). |

Default: **FM with market model** (1 factor) for short-window studies.

---

## Critical Rules

1. **NEVER** replace missing event-window returns with zero. This biases CARs
   toward zero for illiquid stocks. The only exception is BHAR models, which
   assume continuous holding.

2. **NEVER** compute CARs when the stock's first/last trading date falls
   inside the event window (IPO/delisting bias).

3. **NEVER** sum CARs when a boundary day has `cum_periods > 1` — the return
   spans outside the intended window.

4. **NEVER** run OLS with a standard constant when using the trade-to-trade
   transformation. Use `nocons` with `1/sqrt(cum_periods)` as the intercept
   regressor.

5. **NEVER** report CARs without at least one parametric and one
   non-parametric test statistic.

6. **NEVER** mix log and simple returns between the LHS and RHS of the market
   model. If stock returns are in logs, factor returns must also be in logs
   (or convert both via `ln(1+R)` before estimation). Jensen's inequality
   creates bias otherwise.

---

## Output Contract

A valid CAR output dataset must contain:

**Identifiers** (column names vary by project):
- `firm_id`, `event_id`, `event_date`

**Estimation diagnostics** (per firm-event, per model):
- `alpha`, `beta` (per factor), `nobs`, `r2`, `sigma_hat`

**Per CAR window per model**:
- `car_value` — NaN if invalid
- `n_valid_ar` — count of non-NaN ARs in the window

**Exclusion reason** (per firm-event):
- `insufficient_est_obs`, `insufficient_evt_obs`, `ipo_in_window`,
  `delisting_in_window`, `event_off_dateline`, `boundary_contamination`

**Test statistics** (separate output):
- AAR-level and CAAR-level tests, each with test statistic value and p-value
- Minimum: Patell, BMP, Kolari-Pynnonen adjusted BMP, generalized sign test

---

## Sensible Defaults

These can be overridden by the user:

| Parameter | Default | Notes |
|-----------|---------|-------|
| Estimation window | `[-250, -30]` | ~1 year of trading days |
| Min estimation obs | 120 | Conservative; eventstudy2 defaults to 30 |
| Event window | Widest CAR window | Determined by user's CAR windows |
| Max event-date shift | 3 calendar days | Beyond this, exclude the event |
| Dateline threshold | 0.0 | Include all trading days (set ~0.2 for international samples) |
| Thin-trading adjustment | ON | Disable only for extremely liquid markets |
| Log returns | Convert via `ln(1+R)` | Unless input is already in logs |
| Min event-window obs | 1 | Per eventstudy2 default |
| Kolari-Pynnonen ADJ | Computed | Skip only if N > 500 firms (O(N^2) cost) |

---

## Reference Files

Read these for detailed formulas and implementation guidance:

| File | Contents | When to Read |
|------|----------|--------------|
| `references/estimation_models.md` | RAW, COMEAN, MA, FM, BHAR model specs | When choosing or implementing a benchmark model |
| `references/thin_trading.md` | Maynes-Rumsey (1993) transformation with Python code | When implementing the trade-to-trade adjustment |
| `references/test_statistics.md` | All 13 test statistics with formulas | When implementing or debugging test statistics |
| `references/kolari_pynnonen.md` | Cross-correlation adjustment (2010) and GRANK-T (2011) | When implementing Kolari-Pynnonen tests |
| `references/implementation_checklist.md` | 10 most common mistakes in naive implementations | When auditing or upgrading an existing CAR pipeline |

## Validation Script

After computing CARs, run `scripts/validate_cars.py` to check output
integrity:

```bash
python scripts/validate_cars.py --car-file output.parquet \
    --firm-col firm_id --event-col event_id \
    --car-cols CAR_m1_p1,CAR_m5_p5 \
    --exclusion-col exclusion_reason \
    --nar-cols n_ar_m1_p1,n_ar_m5_p5 \
    --window-lengths 3,11
```

The script checks: no CARs where exclusion reasons exist, valid AR counts
match window lengths, required columns are present, and test statistic files
exist alongside the CAR panel.
