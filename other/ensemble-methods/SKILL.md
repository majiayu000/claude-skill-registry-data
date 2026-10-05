---
name: ensemble-methods
description: "Expected error decomposes into bias, variance, and irreducible noise."
---

# Ensemble Methods (Verbose)

## Core Patterns

### Match the Ensemble to the Error

Expected error decomposes into bias, variance, and irreducible noise. Each family
of ensemble attacks a different term, so diagnosing first saves you from
combining models in a way that cannot help.

| Family | Base learners | Attacks | Trained | Typical base model |
|---|---|---|---|---|
| Bagging | Independent, parallel | Variance | Bootstrap samples | Deep, unpruned tree |
| Boosting | Sequential, dependent | Bias | Residuals of the current ensemble | Shallow tree (depth 3-8) |
| Voting / averaging | Independent, heterogeneous | Both, mildly | Same data | Any |
| Stacking | Heterogeneous + meta-learner | Both | Out-of-fold predictions | Any |

The base learner is not interchangeable across families. Bagging wants
high-variance, low-bias learners — averaging is what removes the variance, so
start deep. Boosting wants weak, high-bias learners — the sequence supplies the
capacity, so a depth-20 tree as a boosting base overfits within a few rounds.

### Bagging and Random Forests

```python
from sklearn.ensemble import RandomForestClassifier

rf = RandomForestClassifier(
    n_estimators=500,
    max_features="sqrt",    # decorrelates trees -- the load-bearing parameter
    min_samples_leaf=1,
    n_jobs=-1,
    random_state=0,
)
```

The variance of an average of `n` estimators each with variance `s^2` and
pairwise correlation `rho` is `rho*s^2 + (1-rho)*s^2/n`. The second term vanishes
as `n` grows; the first does not. This explains two observations practitioners
hit constantly:

- Returns on `n_estimators` flatten hard — 500 trees is rarely meaningfully
  better than 200, and never worse (forests do not overfit with more trees).
- `max_features` is the parameter that moves the needle, because it lowers
  `rho`. Bagged trees using all features are highly correlated and pool little.

Random forests give you a free validation estimate:

```python
rf = RandomForestClassifier(n_estimators=500, oob_score=True, bootstrap=True)
rf.fit(X_train, y_train)
rf.oob_score_    # scored on the ~37% of rows each tree did not see
```

Useful for a quick read, but it is a single number without an interval — for a
decision, still use repeated CV (see model-evaluation).

### Boosting

```python
from sklearn.ensemble import HistGradientBoostingClassifier

hgb = HistGradientBoostingClassifier(
    learning_rate=0.05,
    max_iter=2000,
    early_stopping=True,
    validation_fraction=0.1,
    n_iter_no_change=30,
    l2_regularization=1.0,
    random_state=0,
)
```

`learning_rate` and iteration count trade off directly: halving the rate roughly
doubles the iterations needed. Rather than tuning both, fix a small rate
(0.03-0.1) and let early stopping choose the count. `HistGradientBoosting` bins
features and handles NaNs natively, making it fast on large tabular data and a
reasonable stand-in for LightGBM inside the sklearn API.

Boosting overfits in a way bagging does not: it will keep driving training loss
down past the point of generalization. Early stopping is not optional.

### Stacking, and the Leak That Ruins It

Stacking trains a meta-learner on base-model predictions. The correctness
condition is that those predictions must be **out-of-fold**.

```python
from sklearn.ensemble import StackingClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import StratifiedKFold

stack = StackingClassifier(
    estimators=[("rf", rf), ("hgb", hgb), ("lr", lr_pipeline), ("knn", knn_pipeline)],
    final_estimator=LogisticRegression(C=1.0, max_iter=1000),
    cv=StratifiedKFold(5, shuffle=True, random_state=0),
    stack_method="predict_proba",
    passthrough=False,
    n_jobs=-1,
)
```

Why in-sample base predictions are fatal: a random forest predicting on its own
training rows is near-perfect — it has effectively memorized them. The
meta-learner sees a column that matches the label almost exactly and assigns it
overwhelming weight. At inference time that column is an ordinary,
error-prone prediction, and the ensemble underperforms its own base models. The
symptom is a stack with a spectacular training score and test performance below
the best single component.

`cv=5` inside `StackingClassifier` handles this: each fold's meta-features come
from base models that never saw those rows. If you build stacking by hand,
generate meta-features with `cross_val_predict`, never `fit` then `predict` on
the same data.

Further guidance:

- **Keep the meta-learner simple.** Logistic or ridge regression on 3-6 base
  columns. A gradient-boosted meta-learner on the same folds overfits the fold
  structure and adds variance with no gain.
- **`passthrough=True`** feeds the raw features alongside base predictions. It
  occasionally helps, and reliably increases overfitting risk; test it, do not
  assume it.
- **Correct nesting.** To estimate stack performance, wrap the whole
  `StackingClassifier` in an outer CV. Reusing the internal `cv` folds for
  evaluation is optimistic.

### Diversity Is the Real Ingredient

Ensembling helps in proportion to how uncorrelated the base errors are. Measure
it rather than assuming it:

```python
import numpy as np, pandas as pd
oof = pd.DataFrame({name: cross_val_predict(m, X, y, cv=cv, method="predict_proba")[:, 1]
                    for name, m in estimators})
oof.corr(method="spearman")
```

Correlations above ~0.95 mean the models are redundant — you are paying n-times
inference cost for a rounding error. Sources of genuine diversity: different
model families, different feature subsets or representations, different loss
functions, different resampling of the training data. Different random seeds on
one algorithm is the weakest form and typically buys a fraction of a point.

### When Not to Ensemble

Ensembles cost inference latency (roughly linear in members), memory, retraining
orchestration, and interpretability — attribution now describes a committee, and
the model-interpretability caveats compound. Before shipping one, confirm the CV
improvement exceeds the confidence interval, not merely the point estimate. A
0.3-point AUC gain inside a ±1.5-point interval is not an improvement, and the
operational cost is real.

## Common Anti-Patterns

❌ **Stacking on in-sample base predictions.** The meta-learner learns to trust
a memorizing base model; test performance falls below the best single model.
✅ `cv` inside `StackingClassifier`, or `cross_val_predict` when hand-rolling.

❌ **Ensembling five seeds of the same algorithm and calling it an ensemble.**
Errors are near-identical, so nothing cancels.
✅ Mix families — trees, boosting, linear, neighbors — and verify residual
correlation is well below 0.95.

❌ **Deep trees as boosting base learners.** Boosting supplies the capacity;
deep bases overfit within a handful of rounds.
✅ `max_depth` 3-8, small learning rate, early stopping on a validation split.

❌ **Tuning `learning_rate` and `n_estimators` jointly on a grid.** They trade
off directly; the grid mostly rediscovers that.
✅ Fix a small rate, let early stopping select the count.

❌ **A complex meta-learner.** Gradient boosting on four probability columns
overfits fold structure.
✅ Regularized logistic or ridge regression.

❌ **Evaluating the stack on the same folds its base models were fit through.**
✅ Nested CV: an outer loop that never touches the inner fold structure.

❌ **Shipping the ensemble for a gain inside the noise band.**
✅ Compare paired per-fold deltas against their interval; prefer the single model
when they overlap.

## Ensemble Methods Checklist

- [ ] Bias vs variance diagnosed before choosing an ensemble family
- [ ] Base learner depth matched to the family (deep for bagging, shallow for boosting)
- [ ] `max_features` tuned for forests, not just `n_estimators`
- [ ] Boosting uses early stopping with a held-out validation fraction
- [ ] Stacking meta-features are strictly out-of-fold
- [ ] Meta-learner kept simple and regularized
- [ ] Base-model residual correlation measured, not assumed
- [ ] All preprocessing inside per-model `Pipeline` objects
- [ ] Stack performance estimated with nested CV
- [ ] Improvement over the best single model exceeds its confidence interval
- [ ] Inference latency and memory cost measured against the gain
- [ ] Retraining and version pinning defined for every ensemble member
