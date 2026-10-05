---
name: cross-validation-strategies
description: "Cross-validation only estimates generalization if the split mimics the gap between"
---

# Cross Validation Strategies (Verbose)

## Core Patterns

### Choosing a Splitter

Cross-validation only estimates generalization if the split mimics the gap between
training data and deployment data. Pick the splitter from the structure of the data,
not from habit.

| Splitter | Use when | Key parameters |
|---|---|---|
| `KFold` | Rows are exchangeable | `n_splits`, `shuffle`, `random_state` |
| `StratifiedKFold` | Classification, uneven classes | `n_splits`, `shuffle` |
| `GroupKFold` | Repeated measures per entity | `n_splits`, `groups=` at split time |
| `StratifiedGroupKFold` | Both of the above | `n_splits`, `shuffle` |
| `TimeSeriesSplit` | Temporal ordering matters | `n_splits`, `test_size`, `gap`, `max_train_size` |
| `RepeatedStratifiedKFold` | Small n, noisy estimates | `n_splits`, `n_repeats` |

`cross_val_score` and `GridSearchCV` default to `StratifiedKFold` for classifiers and
`KFold` for everything else, with `shuffle=False`. Two consequences bite regularly:
data sorted by label gets pathological unshuffled folds, and time series get shuffled
the moment someone passes `cv=KFold(shuffle=True)`.

### Preventing Preprocessing Leakage

Leakage is the dominant cause of a CV score that fails to reproduce in production.
Any transformation that estimates parameters from data — mean, variance, category
frequencies, target statistics, principal components, selected feature indices — must
be fitted on the training fold alone.

```python
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.feature_selection import SelectKBest, f_classif
from sklearn.ensemble import HistGradientBoostingClassifier

numeric = Pipeline([
    ("impute", SimpleImputer(strategy="median")),   # median from the fold
    ("scale", StandardScaler()),
])
categorical = OneHotEncoder(handle_unknown="ignore")

pre = ColumnTransformer([
    ("num", numeric, num_cols),
    ("cat", categorical, cat_cols),
])

model = Pipeline([
    ("pre", pre),
    ("select", SelectKBest(f_classif, k=50)),
    ("clf", HistGradientBoostingClassifier()),
])
```

Feature selection is the sneakiest case. Ranking all features by correlation with the
target on the full dataset, then cross-validating the surviving 50, produces strong
scores on pure noise: with 10,000 random columns some will correlate with `y` by
chance, and the selection step already saw the validation rows. Inside the pipeline,
each fold re-selects and the illusion disappears.

### Time Series Validation

```python
from sklearn.model_selection import TimeSeriesSplit

tscv = TimeSeriesSplit(n_splits=5, test_size=90, gap=14)
for train_idx, test_idx in tscv.split(X):
    # train_idx is always strictly earlier than test_idx
    ...
```

Expanding window (the default) grows the training set each fold; it suits models that
benefit from more history. A rolling window — `max_train_size=365` — holds the training
length fixed and better reflects deployment when the process drifts.

`gap` handles label lag. If the target is "churned within 30 days", a row dated
day *t* is not observable until day *t+30*; without a 30-day gap the model trains on
outcomes that had not yet occurred at the boundary. The same applies to rolling
features: a 7-day moving average at the first test timestamp is computed partly from
training-period values, so it straddles the split.

Purged and embargoed k-fold, standard in quantitative finance, generalizes this:
remove training samples whose label window overlaps the test window, then embargo a
further stretch after it.

### Group-Aware Splitting

```python
from sklearn.model_selection import StratifiedGroupKFold, cross_val_score

cv = StratifiedGroupKFold(n_splits=5, shuffle=True, random_state=0)
scores = cross_val_score(model, X, y, groups=patient_id, cv=cv, scoring="roc_auc")
```

When one patient contributes 40 records, a random split puts some in train and some in
test. The model memorizes the patient, not the disease, and the score measures
recall of individuals rather than generalization to new individuals. The tell is a
large drop when you switch from `KFold` to `GroupKFold` on the same data — that drop
is the true difficulty of the problem.

`GroupKFold` cannot honour equal fold sizes when groups are very uneven; folds will
differ in size. That is expected, not a bug.

### Nested Cross-Validation

```python
from sklearn.model_selection import GridSearchCV, StratifiedKFold, cross_val_score

grid = {"clf__learning_rate": [0.03, 0.1, 0.3], "clf__max_leaf_nodes": [15, 31, 63]}

inner = GridSearchCV(model, grid, cv=StratifiedKFold(5), scoring="roc_auc", n_jobs=-1)
outer = cross_val_score(inner, X, y, cv=StratifiedKFold(5), scoring="roc_auc")
print(f"{outer.mean():.3f} ± {outer.std():.3f}")
```

Reporting `GridSearchCV.best_score_` as the expected performance is optimistic by
construction: it is the maximum over a search, and the maximum of noisy estimates
exceeds their mean. With a large grid and small data the inflation can exceed 5 points
of AUC. Nested CV separates model selection from evaluation at the cost of
`n_outer × n_inner × |grid|` fits.

### Reading the Variance

Report the fold standard deviation, always. If model A scores 0.842 ± 0.031 and model B
scores 0.850 ± 0.028 over five folds, the difference is noise. Use paired folds — the
same `random_state` and splitter for both — and compare per-fold differences, which
removes fold difficulty as a confounder.

## Common Anti-Patterns

❌ **Scaling, imputing, or encoding before `train_test_split`.**
✅ Put every fitted transformer in a `Pipeline` and pass the pipeline to `cross_val_score`.

❌ **`KFold(shuffle=True)` on a time-indexed dataset** — trains on the future, scores
near-perfect on autocorrelated targets, collapses in production.
✅ `TimeSeriesSplit` with a `gap` sized to the label lag.

❌ **Oversampling (SMOTE, random duplication) before splitting** — synthetic points
interpolated from a validation row make it partly memorized.
✅ Resample inside the fold with `imblearn.pipeline.Pipeline`, which applies samplers
on `fit` only.

❌ **Selecting features on the full dataset, then cross-validating the survivors.**
✅ `SelectKBest` as a pipeline step, re-fit per fold.

❌ **Reporting `best_score_` from `GridSearchCV` as expected performance.**
✅ Nested CV, or a genuinely untouched holdout set.

❌ **Ignoring group structure** — same user, session, image patch, or device on both
sides of the split.
✅ `GroupKFold` / `StratifiedGroupKFold` with the entity id as `groups`.

❌ **Comparing models on different fold assignments.**
✅ Fix `random_state` and reuse the identical splits across candidates.

❌ **Tuning against the final test set** by iterating until it looks good.
✅ Touch the holdout once, at the end.

## Cross-Validation Checklist

- [ ] Splitter chosen from data structure (temporal / grouped / stratified)
- [ ] Every fitted transformer lives inside a `Pipeline`
- [ ] Resampling applied via `imblearn.pipeline.Pipeline`, never before the split
- [ ] Feature selection re-fit per fold
- [ ] `groups=` passed when entities repeat across rows
- [ ] `gap` set to the label lag for time series
- [ ] Scoring metric matches the decision the model supports
- [ ] Hyperparameter search wrapped in an outer loop or judged on a separate holdout
- [ ] Mean **and** standard deviation reported across folds
- [ ] Same `random_state` and splitter used for every candidate model
- [ ] CV estimate sanity-checked against a chronologically later holdout
- [ ] Final holdout evaluated exactly once
