---
name: model-evaluation
description: "Every metric encodes an opinion about which mistake hurts."
---

# Model Evaluation (Verbose)

## Core Patterns

### Choosing the Metric

Every metric encodes an opinion about which mistake hurts. Start from the
decision the model drives, then pick the metric that penalizes the costly error.

| Task | Default metric | Reach for instead when |
|---|---|---|
| Balanced binary | ROC-AUC, accuracy | — |
| Rare-positive binary (fraud, disease, churn) | Average precision (PR-AUC) | ROC-AUC hides false-positive volume |
| Multi-class, uneven support | Macro-F1 | Micro-F1 if you want per-sample weighting |
| Probabilistic output consumed downstream | Log loss, Brier score | Ranking metrics ignore calibration |
| Regression, outliers matter | RMSE | MAE when outliers are noise, not signal |
| Regression, relative error matters | MAPE / sMAPE | Never when actuals approach zero |
| Ranking / retrieval | NDCG@k, MRR | Accuracy is meaningless here |

#### Why ROC-AUC Flatters on Imbalanced Data

The ROC curve plots TPR against FPR. FPR is `FP / (FP + TN)`. When negatives
outnumber positives 200:1, `TN` dominates the denominator and a large absolute
number of false positives produces a tiny FPR movement. The precision-recall
curve plots precision, `TP / (TP + FP)`, which has no `TN` term and therefore no
cushion.

```python
from sklearn.metrics import roc_auc_score, average_precision_score

# 10,000 rows, 50 positives (0.5% prevalence)
roc_auc_score(y_test, scores)            # 0.94  -- looks excellent
average_precision_score(y_test, scores)  # 0.21  -- the honest picture
```

PR-AUC's baseline is the positive rate itself (0.005 here), so 0.21 is real
lift — but it says that at any recall worth having, most flagged cases are
wrong. That is the number the review team lives with. The corollary: PR-AUC is
not comparable across datasets with different base rates, because its floor
moves with prevalence.

### Splitting Honestly

```python
from sklearn.model_selection import GroupKFold, TimeSeriesSplit

# Repeated entities: the same patient must not appear on both sides
cv = GroupKFold(n_splits=5)
for tr, te in cv.split(X, y, groups=patient_id):
    ...

# Temporal data: never train on the future
cv = TimeSeriesSplit(n_splits=5, gap=7)   # gap skips rows between fold edges
```

Leakage is the dominant cause of models that look great offline and die in
production. Three shapes recur:

1. **Preprocessing before splitting.** Fitting a scaler, imputer, or target
   encoder on the full dataset lets test statistics reach the training rows.
2. **Grouped rows split randomly.** Multiple rows per user, session, or image
   patch put near-duplicates on both sides; scores inflate by several points.
3. **Features computed with hindsight.** A `customer_lifetime_value` column
   computed today, joined onto a two-year-old event, encodes the label.

```python
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression

pipe = make_pipeline(StandardScaler(), LogisticRegression(max_iter=1000))
cross_val_score(pipe, X, y, cv=cv)   # scaler refit inside every fold
```

### Uncertainty on the Estimate

A single train/test number is one draw from a distribution. Quantify the spread
before you claim an improvement.

```python
import numpy as np
from sklearn.model_selection import RepeatedStratifiedKFold, cross_val_score

cv = RepeatedStratifiedKFold(n_splits=5, n_repeats=4, random_state=0)
s = cross_val_score(model, X, y, cv=cv, scoring="average_precision")
lo, hi = np.percentile(s, [2.5, 97.5])
print(f"AP {s.mean():.3f}  95% range [{lo:.3f}, {hi:.3f}]  n={len(s)}")
```

For a fixed test set, bootstrap the *test set* instead: resample indices with
replacement, recompute the metric, take percentiles. Rough guide — on a
1,000-row test set with 100 positives, the 95% interval on AUC spans roughly
±0.03. Deltas smaller than that are not results.

To compare two models, run them on the *same* folds and look at the paired
per-fold differences, not at two independent means.

### Thresholds and Costs

```python
from sklearn.metrics import precision_recall_curve
import numpy as np

prec, rec, thr = precision_recall_curve(y_val, val_scores)
# Highest recall subject to precision >= 0.60. Note thr is one shorter than prec/rec.
ok = prec[:-1] >= 0.60
best = thr[ok][np.argmax(rec[:-1][ok])]
```

Choose the threshold on validation data, then evaluate it once on test. Choosing
it on test and reporting the same number is optimistic by construction.

When costs are known, skip the curve: with per-error costs `C_fp` and `C_fn`,
the expected-cost-minimizing threshold on a calibrated probability is
`C_fp / (C_fp + C_fn)`. At a 10:1 FN:FP cost ratio that is 0.09, not 0.5.

### Calibration

```python
from sklearn.calibration import CalibratedClassifierCV, calibration_curve

prob_true, prob_pred = calibration_curve(y_val, val_scores, n_bins=10)
# Boosted trees typically bow away from the diagonal: 0.80 predicted, 0.60 observed

cal = CalibratedClassifierCV(base_model, method="isotonic", cv=5)
```

Calibration and discrimination are independent properties. Any monotone
transform of the scores leaves ROC-AUC untouched while changing log loss
completely — which is exactly why a model can rank well and still be badly
calibrated. Use `method="isotonic"` with ample data and `"sigmoid"` (Platt) when
the calibration set is small, since isotonic overfits below a few thousand rows.

### Beyond the Aggregate Number

Slice every metric by segment — region, device, tenure, protected attribute. A
model at 0.88 overall can sit at 0.61 on the newest 10% of users, which is the
cohort that matters most. Aggregate metrics average away exactly the failures
worth finding. Pair slicing with error inspection; see the model-interpretability
skill for attributing *why* a slice fails.

## Common Anti-Patterns

❌ **Reporting accuracy on imbalanced data** — 99% accuracy at 1% prevalence is
what always predicting "no" achieves.
✅ Average precision, plus recall at a stated precision floor.

❌ **A single test-set number with no interval.** The delta being celebrated is
usually inside the noise band.
✅ Repeated CV or a bootstrap interval, with paired fold-wise comparisons.

❌ **Fitting the scaler, imputer, or encoder before splitting.**
✅ Every transform inside a `Pipeline`, refit per fold.

❌ **Random splits on grouped or time-ordered data.**
✅ `GroupKFold` for repeated entities, `TimeSeriesSplit` for temporal order.

❌ **Tuning on the test set, then reporting the test set.** Every peek turns it
into a validation set; after fifty experiments it is fully optimized against.
✅ Train / validation / test, with test opened once at the end.

❌ **Shipping on the offline metric alone.** Offline gains routinely fail to
transfer when the deployment distribution shifts or the metric was a proxy.
✅ Confirm with an online experiment against the business metric.

❌ **Treating 0.5 as the threshold.**
✅ Derive it from explicit costs or the validation PR curve.

## Model Evaluation Checklist

- [ ] Metric chosen from the decision, not from habit
- [ ] PR-AUC rather than ROC-AUC reported when positives are rare
- [ ] Split strategy matches the data structure (group / time / random)
- [ ] All preprocessing inside a `Pipeline`
- [ ] Confidence interval or fold spread reported with every number
- [ ] Model comparisons paired across identical folds
- [ ] Test set untouched until the final evaluation
- [ ] Decision threshold tuned on validation, from explicit costs
- [ ] Calibration checked whenever probabilities are consumed downstream
- [ ] Metrics broken out by meaningful segments, not just aggregate
- [ ] Compared against `DummyClassifier` or a naive baseline
- [ ] Random seeds fixed and recorded so results reproduce
