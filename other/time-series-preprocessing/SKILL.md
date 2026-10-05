---
name: time-series-preprocessing
description: "Almost every downstream bug traces back to an index that was assumed regular and"
---

# Time Series Preprocessing (Verbose)

## Core Patterns

### Establishing a Regular Index

Almost every downstream bug traces back to an index that was assumed regular and
was not. Make the grid explicit before anything else.

```python
df = (df.drop_duplicates(subset="ts", keep="last")
        .set_index("ts")
        .sort_index()
        .asfreq("h"))          # absent hours become rows of NaN, not silent gaps
```

`asfreq` is the load-bearing call. Without it, `shift(1)` means "the previous
row", which may be an hour ago or a week ago depending on what the source system
happened to emit. With it, `shift(1)` means "one hour ago" — which is what every
lag feature actually assumes.

Store timestamps in UTC. A series in local time gains a duplicated hour each
autumn and loses one each spring; `asfreq` will either raise on the duplicate or
silently produce a NaN row, and seasonal features built on local hour-of-day drift
by one for half the year. Convert to local time only for calendar features
(`is_weekend`, `hour_of_day`), and derive those from the localized view rather
than storing the whole series that way.

### Causal Feature Engineering

The governing rule: a feature for time `t` may use only data timestamped strictly
before `t`, *and* available before `t` in the production system. Those are two
different constraints and both bite.

```python
g = df.groupby("store_id")["sales"]

df["lag_1"]   = g.shift(1)
df["lag_7"]   = g.shift(7)
df["lag_364"] = g.shift(364)                      # same weekday last year

# Rolling windows: shift first, then roll.
df["ma_7"]    = g.shift(1).rolling(7,  min_periods=7).mean()
df["ma_28"]   = g.shift(1).rolling(28, min_periods=28).mean()
df["std_28"]  = g.shift(1).rolling(28, min_periods=28).std()

# Ratio features generalize better than levels across stores of different sizes.
df["ma_ratio"] = df["ma_7"] / df["ma_28"]
```

pandas `rolling` is right-aligned: at row `t` the window covers `t-6 .. t`
inclusive. So an unshifted `rolling(7).mean()` contains `y[t]` — one seventh of the
target is literally inside the predictor. This produces beautiful validation
curves and a model that collapses the moment it runs on data where `y[t]` is not
yet known. The `.shift(1)` before `.rolling()` is not stylistic; it is the whole
correctness argument.

`min_periods` equal to the window prevents a second, subtler issue: partially
filled early windows have different variance than full ones, so the model learns a
spurious relationship between series age and noise level.

The availability constraint is the one that survives code review and then fails in
production. A daily sales total for day `t-1` may not land in the warehouse until
06:00 on day `t`; if you score at 02:00, `lag_1` is not there. Lag features to what
is *available at scoring time*, not to what is *timestamped before now*.

### Resampling and Target Definition

```python
agg = df.resample("D").agg(
    sales_total=("sales", "sum"),
    sales_peak=("sales", "max"),
    price_close=("price", "last"),
    n_obs=("sales", "size"),        # keep the count — it exposes partial periods
)
```

| Source → target | Aggregation | Why |
|---|---|---|
| Counts/volume | `sum` | Additive quantity |
| Prices, levels, gauges | `last` | Endpoint is the state |
| Rates, utilization | `mean` | Time-weighted average |
| Capacity planning | `max` / `quantile(0.95)` | Peaks drive the decision |
| Presence | `size` | Detects incomplete periods |

Downsampling is not a neutral cleanup step — it changes the question. Predicting
hourly demand and predicting daily demand are different problems with different
noise floors, different seasonality, and different naive baselines. Recompute the
baseline after resampling; a model that beat the hourly naive forecast may lose to
the daily one, because aggregation removed exactly the noise the model was
exploiting.

Always carry `n_obs`. The final period of a resampled series is almost always
partial — the day is not over — and a partial sum looks like a dramatic drop. Drop
or mask incomplete periods rather than letting the model learn a phantom
end-of-series collapse.

### Missing Data

```python
df["gap_len"] = df["value"].isna().groupby(df["value"].notna().cumsum()).transform("size")
df["was_imputed"] = df["value"].isna()
df["value"] = df["value"].ffill(limit=3)      # causal, bounded
df = df[df["gap_len"] <= 24]                  # drop windows built over long outages
```

| Method | Causal | Use when |
|---|---|---|
| `ffill(limit=n)` | Yes | Slowly varying state; short sensor dropouts |
| Rolling median of the past | Yes | Noisy series where the last value is unreliable |
| Seasonal lag (`shift(168)`) | Yes | Strong weekly cycle, gaps under a week |
| `interpolate()` | **No** | Offline visualization and reporting only |
| `bfill()` | **No** | Never in a training set |
| Leave NaN | Yes | LightGBM/XGBoost handle it natively — often best |

Leaving NaN is underrated. Gradient boosting learns a default direction for
missing values, which lets the model treat "sensor was down" as the signal it
frequently is. Imputation manufactures a plausible value and destroys that signal.

### Validation Splits

```python
from sklearn.model_selection import TimeSeriesSplit

tscv = TimeSeriesSplit(n_splits=5, test_size=30, gap=7)
for tr, te in tscv.split(X):
    ...   # tr always precedes te; 7 rows discarded between them
```

`gap` must be at least the forecast horizon. Predicting seven days ahead with
`gap=0` means the last training row's target window overlaps the first validation
row's — the model sees part of the answer.

Expanding-window splits (the sklearn default, where the training set grows) match
production retraining. Sliding-window splits, where training length is fixed,
better estimate performance under regime change and are the honest choice when the
data-generating process is known to drift. Pick one deliberately and say which.

Group by entity when panel data has one series per store, device, or user: leakage
across time within an entity is the obvious risk, but a random split also puts the
same store on both sides, which inflates scores for anything the model can memorize
per entity.

## Common Anti-Patterns

❌ **`df["ma"] = df["y"].rolling(7).mean()`** — the window includes `y[t]`.
✅ `df["y"].shift(1).rolling(7).mean()`.

❌ **`interpolate()` or `bfill()` before splitting.** Future values are dragged
backwards into training rows.
✅ Forward fill with a limit, a seasonal lag, or leave NaN.

❌ **`train_test_split(X, y, shuffle=True)`.** Trains on the future to predict the
past.
✅ `TimeSeriesSplit`, or a fixed date cutoff.

❌ **Scaler, target encoder, or PCA fitted on the full series.** Test-period
statistics leak into every training row.
✅ Fit inside a `Pipeline` so each fold refits on its own training portion.

❌ **Lagging to what is timestamped before now, ignoring ingestion delay.** Passes
backtest, fails at 02:00 when yesterday's batch has not landed.
✅ Lag to what is *available* at scoring time; verify against the actual SLA.

❌ **Reporting the last, partial period.** A half-finished day reads as a crash.
✅ Track `n_obs` per period and mask incomplete ones.

❌ **Feeding a trending series to gradient boosting undifferenced.** Trees cannot
extrapolate; forecasts saturate at the training maximum.
✅ Difference, detrend, or model the ratio to a rolling baseline.

❌ **Naive outlier clipping before the split.** Quantile thresholds computed over
all data encode future extremes.
✅ Compute clipping bounds on training data only — and see
anomaly-detection-techniques before deciding an extreme value is noise.

## Time Series Preprocessing Checklist

- [ ] Timestamps stored in UTC; duplicates resolved; index sorted
- [ ] `asfreq` applied so gaps are explicit NaN rows
- [ ] Every rolling / expanding / `ewm` feature preceded by `.shift(1)`
- [ ] `min_periods` set equal to the window length
- [ ] Lags reflect ingestion delay, not just timestamp order
- [ ] Aggregation function chosen from the downstream decision, not by default
- [ ] Naive baseline recomputed after any resampling
- [ ] Incomplete final period masked or dropped
- [ ] Imputation is causal and bounded; `was_imputed` flag retained
- [ ] Split is time-ordered with `gap` ≥ forecast horizon
- [ ] Expanding vs sliding window chosen deliberately and documented
- [ ] All fitted transforms inside a per-fold `Pipeline`
- [ ] Stationarity checked before using an ARIMA-family model
- [ ] Trending series differenced before tree-based models
