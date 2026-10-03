---
name: data-cleaning
description: Use when preparing raw data for modeling — handling missing values, duplicates, inconsistent types, outliers, and bad categorical values. Emphasizes fitting all imputation on train-only to avoid leakage.
---

# Data Cleaning

## Overview

Cleaning turns raw data into a consistent, model-ready table without leaking information from the future or the test set. The golden rule: **every statistic used to clean (means, medians, modes, bounds, category maps) must be learned from the training split only**, then applied to validation/test.

## When to use

- Raw data has nulls, duplicates, mixed types, or junk categories.
- Before feature-engineering and modeling.
- After EDA flagged specific quality issues.

## Workflow

1. **Deduplicate** — exact and key-based duplicates. Decide which to keep (latest timestamp, highest completeness).
2. **Fix types** — parse dates, cast numerics stored as strings, normalize booleans.
3. **Standardize categoricals** — trim whitespace, unify case, map synonyms ("US"/"USA"/"United States").
4. **Handle missing values** — choose per-column strategy (see below).
5. **Treat outliers** — cap/winsorize or flag; never blindly delete.
6. **Validate** — assert schema, ranges, and row counts after each step.

## Missing-value strategy

| Situation | Strategy |
|-----------|----------|
| Numeric, MCAR, small % | Median impute (robust to skew) |
| Numeric, informative missingness | Impute + add `was_missing` indicator |
| Categorical | Impute with `"Missing"` as its own category |
| Time series | Forward/backward fill within group |
| >50% missing | Consider dropping the column |

## Reference snippet (leakage-safe)

```python
from sklearn.model_selection import train_test_split
from sklearn.impute import SimpleImputer

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)

# Fit imputers on TRAIN ONLY
num_imputer = SimpleImputer(strategy="median").fit(X_train[num_cols])
X_train[num_cols] = num_imputer.transform(X_train[num_cols])
X_test[num_cols]  = num_imputer.transform(X_test[num_cols])  # reuse train stats
```

Prefer doing this inside a `Pipeline`/`ColumnTransformer` (see the `sklearn-pipelines` skill) so leakage is impossible by construction.

## Outlier handling

```python
# Winsorize numeric columns to train-derived 1st/99th percentiles
lo = X_train[col].quantile(0.01)
hi = X_train[col].quantile(0.99)
X_train[col] = X_train[col].clip(lo, hi)
X_test[col]  = X_test[col].clip(lo, hi)
```

## Pitfalls

- **`df.fillna(df.mean())` on the whole dataset** — classic leakage. Compute stats on train only.
- **`dropna()` on rows** silently shrinks and biases the dataset; prefer imputation + indicators.
- **Deleting outliers** that are real signal (fraud, rare events) — investigate before removing.
- **Cleaning before splitting** — split first, then clean using train statistics.

## Hand-off

Produce a clean, typed dataframe plus a documented list of decisions (what was imputed/capped/dropped and why) so feature-engineering and reproducible-ml can rely on it.
