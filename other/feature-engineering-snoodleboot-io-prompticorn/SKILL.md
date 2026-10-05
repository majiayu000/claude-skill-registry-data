---
name: feature-engineering
description: "Cardinality and model family jointly determine the encoding."
---

# Feature Engineering (Verbose)

## Core Patterns

### Categorical Encoding

Cardinality and model family jointly determine the encoding. There is no default that
survives both a 3-level column and a 200,000-level user id.

| Encoding | Best for | Failure mode |
|---|---|---|
| One-hot | Low cardinality, linear models | Dimension blowup; sparse, weak splits in trees |
| Ordinal | Genuinely ordered levels | Imposes false order on nominal data |
| Target / mean | High cardinality with signal | Leaks the label unless cross-fitted |
| Count / frequency | High cardinality, popularity matters | Collides distinct categories at equal counts |
| Hashing | Streaming, unbounded vocabulary | Collisions, no inverse mapping |
| Native categorical | LightGBM, CatBoost, `HistGradientBoosting*` | Library-specific |

```python
from sklearn.preprocessing import OneHotEncoder, OrdinalEncoder, TargetEncoder

OneHotEncoder(handle_unknown="ignore", min_frequency=0.01)   # rare levels pooled
OrdinalEncoder(categories=[["low", "medium", "high"]])       # order stated explicitly
TargetEncoder(smooth="auto", cv=5)                           # cross-fitted internally
```

`min_frequency` folds long-tail levels into an `infrequent` bucket, which both bounds
the column count and prevents a level seen twice in training from acquiring its own
weight.

### Target Encoding Without Leakage

Naive target encoding is the most common self-inflicted leak in tabular work:

```python
# ❌ each row's own label feeds its own feature value
df["city_te"] = df.groupby("city")["target"].transform("mean")
```

For a city appearing once, that feature *is* the label. Cross-validation scores climb,
production performance does not. The fix is out-of-fold computation plus shrinkage:

```python
from sklearn.preprocessing import TargetEncoder
from sklearn.pipeline import Pipeline

model = Pipeline([
    ("te", TargetEncoder(target_type="binary", smooth="auto", cv=5)),
    ("clf", HistGradientBoostingClassifier()),
])
```

Smoothing blends the category mean toward the global mean in proportion to the
category's sample count: a level with n=2 lands near the prior, a level with n=5,000
near its own mean. Without it, rare categories become high-variance near-perfect
predictors on the training set alone.

### Numeric Transformation

```python
from sklearn.preprocessing import (StandardScaler, RobustScaler,
                                   QuantileTransformer, KBinsDiscretizer)
import numpy as np

StandardScaler()                                   # (x - μ) / σ; assumes roughly symmetric
RobustScaler()                                     # median/IQR; outlier-tolerant
QuantileTransformer(output_distribution="normal")  # forces normality, rank-preserving
np.log1p(x)                                        # right-skewed counts, prices
KBinsDiscretizer(n_bins=10, encode="ordinal", strategy="quantile")
```

Which models need it:

| Model | Scaling required | Reason |
|---|---|---|
| Linear / logistic with penalty | Yes | The penalty is scale-dependent |
| SVM, k-NN, k-means | Yes | Distances dominated by large-range features |
| Neural networks | Yes | Gradient conditioning |
| PCA and friends | Yes | Variance is the objective — see dimensionality-reduction |
| Decision tree, RF, GBM | No | Splits are invariant to monotone transforms |

`log1p` is the right choice over `log` whenever zeros occur, which for counts and
monetary amounts is nearly always.

### Temporal Features

```python
ts = pd.to_datetime(df["event_time"])

df["hour"]        = ts.dt.hour
df["dayofweek"]   = ts.dt.dayofweek
df["is_weekend"]  = (ts.dt.dayofweek >= 5).astype(int)
df["days_since"]  = (reference_time - ts).dt.days

# cyclical: 23:00 and 00:00 should be neighbours
df["hour_sin"] = np.sin(2 * np.pi * df["hour"] / 24)
df["hour_cos"] = np.cos(2 * np.pi * df["hour"] / 24)
```

Both sine and cosine are required — either alone maps two distinct times to the same
value. And `days_since` must be measured from a per-row reference (the prediction
timestamp), not from `datetime.now()`, or the feature drifts every time you retrain and
means something different in backtest than in production.

### Entity Aggregates With Point-in-Time Correctness

Aggregates over an entity's history usually carry more signal than any raw field:

```python
agg = (events[events.ts < cutoff]
       .groupby("user_id")
       .agg(txn_count=("amount", "size"),
            txn_mean=("amount", "mean"),
            txn_max=("amount", "max"),
            last_seen=("ts", "max")))
agg["recency_days"] = (cutoff - agg["last_seen"]).dt.days
```

The `ts < cutoff` filter is the whole game. Aggregating a user's full transaction
history to predict a fraud event that occurred midway through it means the mean already
includes the fraudulent transaction. The model learns to detect its own label. This
class of bug produces excellent offline metrics and a model that is useless live —
see cross-validation-strategies for the splitting side of the same discipline.

### Interactions and Ratios

Trees approximate interactions through repeated splits but represent ratios poorly.
Stating them explicitly often helps more than adding rows:

```python
df["price_per_sqft"]   = df["price"] / df["sqft"]
df["debt_to_income"]   = df["debt"] / df["income"].replace(0, np.nan)
df["util_ratio"]       = df["balance"] / df["credit_limit"]
```

Guard denominators. A silent `inf` propagates into the model and, for linear models,
into an immediate failure to converge.

### Feature Selection

```python
from sklearn.feature_selection import VarianceThreshold, SelectKBest, mutual_info_classif
from sklearn.inspection import permutation_importance

VarianceThreshold(0.0)                      # drop constants
SelectKBest(mutual_info_classif, k=50)      # captures non-linear dependence
permutation_importance(model, X_val, y_val, n_repeats=10)
```

Prefer permutation importance on a validation set over a tree's built-in
`feature_importances_`. The impurity-based version is biased toward high-cardinality
and continuous features — a random unique id can outrank a genuinely predictive binary
flag, purely because it offers more split points.

## Common Anti-Patterns

❌ **`df.groupby(cat)["target"].transform("mean")` as a feature.**
✅ `TargetEncoder` with cross-fitting and smoothing, inside the pipeline.

❌ **Fitting scalers or imputers on the full dataset before splitting.**
✅ Every stateful transform inside a `Pipeline`, refit per fold.

❌ **Aggregating an entity's entire history regardless of the label timestamp.**
✅ Point-in-time filters on every aggregate window.

❌ **One-hot encoding a high-cardinality id** — thousands of near-empty columns.
✅ Target/count encoding, hashing, or a model with native categorical support.

❌ **Feeding raw epoch timestamps to a tree.**
✅ Decompose into hour/dow/month plus cyclical pairs and elapsed-time features.

❌ **Dropping rows with nulls, or imputing without an indicator.**
✅ `SimpleImputer(add_indicator=True)` — missingness is frequently predictive.

❌ **Trusting `feature_importances_`** for feature choice.
✅ Permutation importance on held-out data.

❌ **Engineering a feature that cannot be computed at serve time** — a field populated
by a batch job that lands hours later.
✅ Check availability and latency of every input before building on it.

## Feature Engineering Checklist

- [ ] Every stateful transform lives inside a `Pipeline`
- [ ] `handle_unknown="ignore"` set on one-hot encoders
- [ ] Target encoding cross-fitted and smoothed
- [ ] Encoding chosen per column by cardinality
- [ ] Scaling applied where the model family requires it
- [ ] Skewed numerics log- or quantile-transformed
- [ ] Timestamps decomposed; cyclical features use sin **and** cos
- [ ] Every entity aggregate has a point-in-time cutoff
- [ ] Missingness indicators retained
- [ ] Denominators guarded against zero
- [ ] Suspiciously dominant features investigated for leakage
- [ ] Feature importance measured by permutation on validation data
- [ ] Every feature reproducible from data available at prediction time
- [ ] Transformation logic shared between training and serving, not reimplemented
