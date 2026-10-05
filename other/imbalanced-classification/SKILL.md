---
name: imbalanced-classification
description: "Imbalance is not itself a problem — it is a symptom that the default loss and the"
---

# Imbalanced Classification (Verbose)

## Core Patterns

### Diagnose Before You Treat

Imbalance is not itself a problem — it is a symptom that the default loss and the
default threshold are misaligned with the cost structure. Establish three numbers
before touching a sampler:

1. **Prevalence.** 1:10 rarely needs intervention. 1:1000 changes the whole approach.
2. **Absolute positive count.** 500 positives out of 500,000 is workable; 20 positives
   out of 20,000 is a problem of data volume, not of balance, and no resampler fixes it.
3. **Relative cost.** A missed fraud costing $400 against a review costing $5 gives an
   80:1 ratio that directly implies the operating threshold.

```python
import numpy as np
counts = np.bincount(y)
print(counts, counts[1] / counts.sum())   # e.g. [99000  1000] 0.01
```

### Metric Selection

```python
from sklearn.metrics import (average_precision_score, roc_auc_score,
                             precision_recall_curve, confusion_matrix)

p = model.predict_proba(X_test)[:, 1]
print("PR-AUC ", average_precision_score(y_test, p))   # baseline = prevalence
print("ROC-AUC", roc_auc_score(y_test, p))             # baseline = 0.5
```

The baselines differ in a way that matters. A random classifier scores 0.5 ROC-AUC but
only 0.01 PR-AUC at 1% prevalence, so a PR-AUC of 0.25 — unimpressive-looking — is a
25× lift over chance. Report PR-AUC against prevalence, not against 0.5.

| Situation | Primary metric |
|---|---|
| Ranking for a fixed-capacity review queue | Precision@k, PR-AUC |
| Screening where misses are dangerous | Recall at a precision floor |
| Costs known in currency | Expected cost at the tuned threshold |
| Comparing across datasets of differing prevalence | ROC-AUC (prevalence-invariant) |
| Model selection under strong imbalance | PR-AUC |

Always print the confusion matrix at the deployed threshold. Aggregate scores hide
whether the model produces 40 false positives or 4,000.

### Cost-Sensitive Learning

The cheapest effective intervention is reweighting the loss, which leaves the data
untouched and therefore cannot leak.

```python
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
import xgboost as xgb

LogisticRegression(class_weight="balanced", max_iter=1000)
RandomForestClassifier(class_weight="balanced_subsample")
xgb.XGBClassifier(scale_pos_weight=(y == 0).sum() / (y == 1).sum())
```

`"balanced"` sets `w_c = n_samples / (n_classes * n_c)`. For explicit control pass a
dict — `class_weight={0: 1, 1: 80}` — derived from the actual cost ratio rather than
from the frequency ratio. Those two ratios are different quantities and are only
accidentally equal.

### Resampling

| Method | Mechanism | Cost | Notes |
|---|---|---|---|
| `RandomUnderSampler` | Drop majority rows | Cheap, fast | Discards signal; good at huge n |
| `RandomOverSampler` | Duplicate minority rows | Cheap | Trees can overfit exact duplicates |
| `SMOTE` | Interpolate k-NN minority pairs | Moderate | Needs meaningful distances |
| `BorderlineSMOTE` | Interpolate near the boundary | Moderate | Often better than plain SMOTE |
| `SMOTENC` | SMOTE with categorical columns | Moderate | Required for mixed dtypes |
| `SMOTEENN` | Oversample, then clean noise | Expensive | Aggressive; verify it helps |

SMOTE assumes Euclidean neighbourhoods are meaningful. On one-hot encoded
high-cardinality categoricals, on unscaled features, or in more than ~50 dimensions,
interpolation produces points that lie off the data manifold — synthetic records that
no real process could generate. Scale first, or use `SMOTENC`, or skip it.

```python
from imblearn.pipeline import Pipeline
from imblearn.over_sampling import SMOTE
from imblearn.under_sampling import RandomUnderSampler
from sklearn.model_selection import cross_val_score, StratifiedKFold

pipe = Pipeline([
    ("over", SMOTE(sampling_strategy=0.1, random_state=0)),   # minority to 10% of majority
    ("under", RandomUnderSampler(sampling_strategy=0.5, random_state=0)),
    ("clf", RandomForestClassifier(n_estimators=300, n_jobs=-1)),
])
scores = cross_val_score(pipe, X, y, cv=StratifiedKFold(5), scoring="average_precision")
```

Note `sampling_strategy=0.1` rather than full balance. Resampling all the way to 1:1 is
a habit, not a requirement; moderate rebalancing frequently outperforms it and distorts
probabilities less. Treat the ratio as a hyperparameter.

### Threshold Optimization

```python
import numpy as np
from sklearn.metrics import precision_recall_curve

prec, rec, thr = precision_recall_curve(y_val, p_val)

# Highest recall subject to precision >= 0.30
ok = prec[:-1] >= 0.30
threshold = thr[ok][np.argmax(rec[:-1][ok])]
```

Or optimize expected cost directly, which is the honest version when the numbers exist:

```python
def expected_cost(t, cost_fn=400, cost_fp=5):
    pred = (p_val >= t).astype(int)
    fn = ((pred == 0) & (y_val == 1)).sum()
    fp = ((pred == 1) & (y_val == 0)).sum()
    return fn * cost_fn + fp * cost_fp

grid = np.linspace(0.01, 0.99, 99)
best = grid[np.argmin([expected_cost(t) for t in grid])]
```

Choose the threshold on validation data and freeze it. Selecting it on the test set is
the same leakage as tuning any other hyperparameter there.

### Calibration

Resampling and class weighting shift the predicted probability distribution: a model
trained on artificially balanced data outputs values near a 50% base rate rather than
the true 1%. Ranking is preserved, so AUC is unaffected — but any downstream expected-value
calculation is now wrong.

```python
from sklearn.calibration import CalibratedClassifierCV

clf = CalibratedClassifierCV(base_model, method="isotonic", cv=5)
clf.fit(X_train, y_train)     # fit on the real, unresampled distribution
```

Use `method="sigmoid"` (Platt scaling) when calibration data is scarce — isotonic needs
roughly 1,000+ samples and will overfit below that.

## Common Anti-Patterns

❌ **Reporting accuracy on 99:1 data.** The trivial constant classifier wins.
✅ PR-AUC, plus precision/recall at the deployed threshold.

❌ **`X_res, y_res = SMOTE().fit_resample(X, y)` before splitting** — synthetic points
interpolated from validation rows land in training.
✅ `imblearn.pipeline.Pipeline`, which resamples only during `fit`.

❌ **Resampling the test set** to "make evaluation fair" — the test set must reflect
production prevalence or precision is meaningless.
✅ Resample training only; evaluate at the real base rate.

❌ **Shipping the 0.5 threshold** because `predict()` uses it.
✅ Tune the threshold on validation against the cost structure.

❌ **Optimizing ROC-AUC at 1:1000** and being surprised that 96% of alerts are false.
✅ Optimize PR-AUC or precision@k, which react to false positives.

❌ **Always resampling to exactly 1:1.**
✅ Sweep `sampling_strategy`; compare against plain `class_weight="balanced"` first.

❌ **SMOTE on one-hot categoricals or unscaled features** — interpolation invents
impossible records.
✅ `SMOTENC` for mixed types, scaling before any distance-based sampler.

❌ **Treating 20 positives as an imbalance problem.**
✅ It is a data-collection problem — gather more labels, or use anomaly detection.

## Imbalanced Classification Checklist

- [ ] Prevalence, absolute positive count, and cost ratio all measured
- [ ] Primary metric is PR-AUC / precision@k, never accuracy
- [ ] PR-AUC compared against the prevalence baseline
- [ ] Class weighting tried before any resampler
- [ ] Resamplers live inside `imblearn.pipeline.Pipeline`
- [ ] Validation and test sets left at production prevalence
- [ ] `sampling_strategy` tuned, not fixed at 1:1
- [ ] `SMOTENC` used when categorical features are present
- [ ] Decision threshold chosen on validation from the cost structure
- [ ] Confusion matrix at the deployed threshold reviewed
- [ ] Probabilities calibrated if consumed as probabilities
- [ ] Stratified splits used throughout
- [ ] Alert volume checked against downstream review capacity
