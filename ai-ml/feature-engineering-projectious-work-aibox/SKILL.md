---
name: feature-engineering
description: |
  Feature engineering for ML — encoding, imputation, scaling, selection, time-series features. Use when preparing data for an ML model, encoding categoricals, handling missing data, building time-series features, or selecting features from a wide table.
metadata:
  processkit:
    apiVersion: processkit.projectious.work/v2
    id: SKILL-feature-engineering
    version: "1.1.0"
    created: 2026-04-06T00:00:00Z
    category: data-ai
---

# Feature Engineering

## Intro

Good features beat clever models. Encode categoricals by cardinality,
impute missing data with mechanism in mind, scale only when the model
needs it, and wrap everything in a sklearn Pipeline so you cannot leak
the test set.

## Overview

### Encoding categoricals

- **One-hot** for nominal categories with < 15 unique values; use
  `drop_first=True` to avoid multicollinearity.
- **Ordinal** for natural order (low/medium/high). Map explicitly —
  never rely on alphabetical sort.
- **Target encoding** for high-cardinality nominals (city, zip).
  Replace with mean target value, always with cross-validated
  encoding to prevent leakage.
- **Frequency encoding** when category count or proportion is itself
  predictive (popular products).
- **Never label-encode nominals** — it implies false ordinal
  relationships.

### Handling missing data

Understand the mechanism first: MCAR, MAR, or MNAR. Numerical
imputation: median (robust to outliers) or mean (preserves
distribution mean), with a binary `_is_missing` indicator if
missingness may be informative. Categorical imputation: mode for
low-cardinality, or treat missing as its own `"unknown"` category.
Advanced: KNN or iterative (MICE) imputation when features are
correlated. Drop rows only when < 5% are affected and missingness is
MCAR. Always fit imputers on training data only.

### Feature scaling

- **StandardScaler** (z-score) — linear regression, SVM, PCA
- **MinMaxScaler** (0–1) — neural networks, bounded range
  requirements; sensitive to outliers
- **RobustScaler** (IQR-based) — when outliers are present
- **No scaling needed** for tree-based models (Random Forest,
  XGBoost)

Always fit on training data only and apply the same transform to
test data.

### Feature selection

Filter methods (correlation, mutual information, chi-square) are
fast but ignore interactions. Wrapper methods (RFE, forward/backward)
consider combinations but are expensive. Embedded methods (Lasso,
tree importance, permutation importance) are the best
speed/accuracy balance. Remove zero-variance features first. Drop
one of each highly correlated pair (r > 0.9). Use domain knowledge
as the first filter before data-driven methods.

### Time-series features

- **Lag features** — `value_lag_1`, `value_lag_7`, `value_lag_30`
  chosen by domain seasonality
- **Rolling statistics** — `value_rolling_mean_7d`, std, min, max
  over windows matching the pattern
- **Seasonal features** — `hour_of_day`, `day_of_week`, `month`,
  `is_weekend`, `is_holiday`; encode cyclical features as
  `sin(2*pi*hour/24)` and matching cosine
- **Difference features** — period-over-period change, percent change
- **Expanding statistics** — cumulative mean, sum, count

Respect temporal ordering — never use future values as features.

### Avoiding data leakage

Never compute features using information from the test set. Fit all
transformers (scaler, imputer, encoder) on training data only. For
time series, features must use only data available at prediction
time. Target encoding must use cross-validation folds, never the
full training set. Wrap preprocessing in `sklearn.pipeline.Pipeline`
to enforce ordering.

## Gotchas

Agent-specific failure modes — provider-neutral pause-and-self-check items:

- **Fitting transformers on the full dataset before splitting.** Fitting a scaler, imputer, or target encoder on train + test leaks test-set statistics into the model. Fit all transformers on training data only, then transform test data with the training-fitted transformer.
- **Target encoding without cross-validation.** Replacing a categorical with its mean target value on the same fold creates direct leakage: the model learns to associate the target with... the target. Use cross-validated target encoding where each fold is encoded using only the other folds' statistics.
- **Label-encoding nominal categories.** Label encoding implies an ordinal relationship (e.g., `Red=0, Blue=1, Green=2` implies `Green > Blue > Red`). Linear models and neural networks will learn a false ordering. Use one-hot or target encoding for nominals with no natural order.
- **Time-series features that peek at future data.** A lag-3 feature computed from row `t` includes data from rows `t+1`, `t+2`, `t+3` if the DataFrame is sorted descending. Verify temporal direction and always use only data available at prediction time.
- **Applying MinMaxScaler when the test set contains values outside the training range.** MinMaxScaler clips values to `[0, 1]` based on training min/max. Out-of-range test values produce values outside `[0, 1]` or are clipped, corrupting the distribution. Use RobustScaler or StandardScaler for data with outliers or uncertain ranges.
- **Polynomial feature expansion on all features "to be safe".** Degree-2 expansion on 100 features produces ~5,000 features. Most of these will be noise, increasing training time and overfitting risk dramatically. Use polynomial features only for specific known non-linear relationships.
- **Feature selection before splitting.** Running mutual information or correlation-based selection on the full dataset lets test-set information guide which features are retained. Select features using only training data, ideally inside a sklearn Pipeline.

## Full reference

### Text features

- **TF-IDF** — baseline text representation; use `max_features` to
  cap dimensionality. Strong with traditional ML classifiers.
- **Count vectorizer** — simpler than TF-IDF when raw frequency is
  enough.
- **Embeddings** — pre-trained sentence-transformers for semantic
  similarity; superior for nuance, more expensive.
- **Extracted features** — text length, word count, punctuation
  count, sentiment score, readability. Often more interpretable
  than bag-of-words.

Combine TF-IDF + extracted features for a strong baseline before
reaching for embeddings.

### Interaction and derived features

- Interaction terms for known relationships (`price * quantity =
  revenue`)
- Ratio features (`clicks / impressions`, `revenue / users`)
- Polynomial features sparingly (degree 2 max), only for known
  non-linear relationships
- Binning continuous → categorical when the relationship is
  step-wise (age groups, income brackets); use domain-driven bins,
  not arbitrary quantiles
- Log transform right-skewed features (income, prices, counts)

### Worked examples

- **user_id, city, purchase_amount, timestamp:** Cross-validated
  target encoding on city; extract day_of_week, hour, is_weekend
  from timestamp; lag features per user; rolling 7- and 30-day
  purchase means; days_since_last_purchase. Wrap in a sklearn
  Pipeline.
- **200 features, poor performance:** Drop zero-variance and
  near-constant columns, drop one of each correlated pair (r > 0.9),
  rank with permutation importance on the baseline, retrain on top
  30–50, compare. Audit remaining features for leakage.
- **40% missing income:** Investigate MAR via correlation with
  other features. Add `income_is_missing` indicator. Impute median
  from the training set (robust to skew). Compare model performance
  to KNN imputation as an alternative.

### Anti-patterns

- Fitting a scaler or encoder on the full dataset before splitting
- Target encoding without cross-validation (silent leakage)
- Label-encoding nominal categories
- Imputing nulls with column mean computed across train + test
- Time-series features that peek at future timestamps
- Polynomial expansion of every feature "to be safe"
