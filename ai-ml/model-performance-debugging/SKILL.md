---
name: model-performance-debugging
description: "Run this before anything else."
---

# Model Performance Debugging (Verbose)

## Core Patterns

### The Overfit-a-Tiny-Subset Test

Run this before anything else. It is the cheapest experiment in machine learning
and it partitions the space of causes in one shot.

```python
tiny = slice(0, 50)
model.fit(X[tiny], y[tiny])
print(model.score(X[tiny], y[tiny]))   # should approach 1.0 / near-zero loss
```

Fifty examples, no regularization, no early stopping, as many epochs as it takes —
any model with adequate capacity should memorize them.

| Result | What it rules out | Where to look |
|---|---|---|
| Cannot reach ~1.0 | Data volume, regularization, distribution shift | Pipeline bug, loss/label mismatch, learning rate, capacity |
| Reaches ~1.0, generalizes badly | Optimization, capacity, wiring | Leakage, feature quality, regularization, shift |

Failing this test means more data will not help, and neither will hyperparameter
search. The usual causes: labels misaligned with features by a shuffle or a join;
a learning rate orders of magnitude off; features all NaN or all constant after a
preprocessing step; a loss that does not match the label encoding (cross-entropy
against one-hot vs integer labels); or a frozen layer meant to be trainable. Teams
routinely spend a week tuning a pipeline whose labels were shifted by one row.

### Learning Curves and the Bias/Variance Read

```python
from sklearn.model_selection import learning_curve

sizes, train_scores, val_scores = learning_curve(
    model, X, y, cv=5, scoring="neg_log_loss",
    train_sizes=np.linspace(0.1, 1.0, 8), n_jobs=-1,
)
```

| Shape | Diagnosis | Effective action | Wasted effort |
|---|---|---|---|
| Train low, val high, gap flat | High variance | Regularize, prune features, simplify | More capacity |
| Train high, val high, converged | High bias | More capacity, better features | More data |
| Gap narrowing at the largest size | Data-limited | Collect more data | Model changes |
| Both high, flat from the start | Bug | The tiny-subset test | Everything else |

The practical value is in the *slope at the right edge*. If validation is still
improving when you run out of data, more data pays; if it went flat at 30% of the
dataset, another 100,000 rows will not move it and the constraint is features or
model class. A validation curve sitting *above* the training curve means the
validation split is easier — a stratification failure, a duplicated easy segment,
or dropout active during training scoring only.

### Baselines and Metric Choice

```python
from sklearn.dummy import DummyClassifier, DummyRegressor

DummyClassifier(strategy="most_frequent").fit(X_tr, y_tr).score(X_te, y_te)
DummyRegressor(strategy="mean").fit(X_tr, y_tr).score(X_te, y_te)
```

No score means anything without the baseline beside it. "94% accuracy" on a 93%
majority class is a model that learned the prior. For forecasting the baseline is
the naive last-value (or seasonal-naive) forecast — harder to beat than expected.

| Situation | Use | Avoid |
|---|---|---|
| Imbalanced (< 10% positive) | PR-AUC, precision@k | Accuracy, ROC-AUC |
| Ranking matters | NDCG, MAP | Accuracy |
| Probabilities consumed downstream | Log loss, Brier, reliability curve | Accuracy |
| Asymmetric error costs | Expected cost at the threshold | Any symmetric metric |

If probabilities feed a decision rule, calibration is a first-class requirement. A
model can rank perfectly and still emit probabilities systematically 3× too high;
boosted trees and SVMs are both notorious for it. Check with a reliability curve,
fix with `CalibratedClassifierCV(method="isotonic")` — isotonic wants a few
thousand calibration samples, `method="sigmoid"` is the choice below that.

### Leakage Investigation

Results that are too good are the most common serious bug, and the least often
reported as one.

```python
imp = pd.Series(model.feature_importances_, index=X.columns).sort_values()
fit_and_score(X.drop(columns=[imp.index[-1]]), y)   # drop the top feature, refit

for col in X.columns[:20]:
    print(col, fit_and_score(X[[col]], y))   # any single column near-perfect = leak
```

The recurring shapes:

- **Target-derived features** — `total_amount` when predicting `is_refunded`, or a
  status column updated after the outcome.
- **Preprocessing fitted before the split** — scalers, imputers, target encoders,
  PCA, feature selection. A `Pipeline` fixes this structurally.
- **Duplicate or near-duplicate rows** on both sides of the split.
- **Group leakage** — the same patient, user, or device in train and test; the
  model memorizes the entity. Use `GroupKFold`.
- **Temporal leakage** — any non-causal feature; see time-series-preprocessing.
- **Identifier leakage** — auto-increment IDs correlate with time, which correlates
  with the label, so the model learns collection order.

The diagnostic: drop the suspect column and refit. A large drop means the column
carried real signal *or* the leak — then ask the operational question, will this
value be known, with this content, at the moment of prediction? That question, not
the importance score, settles it.

### Error Slicing and Manual Inspection

```python
# Build the frame from the evaluation rows themselves, so the slice columns
# and the predictions share one index — assembling it from bare arrays and
# grouping by an outside frame silently misaligns whenever the indices differ.
err = X_test.copy()
err["y"], err["p"], err["prob"] = y_true, y_pred, y_prob
err["wrong"] = err.y != err.p

for col in ["region", "channel", "device", "signup_cohort"]:
    print(err.groupby(col)["wrong"].agg(["mean", "size"]).sort_values("mean"))

# The highest-confidence mistakes are the most informative.
err[err.wrong].nlargest(30, "prob")
```

Aggregate metrics average away exactly the failures that matter. A model at 92%
overall may be at 55% on new users — the segment the product exists to grow. Slice
by class, cohort, data source, time period, input length, and feature-missingness.

Then read thirty actual misclassified examples, highest-confidence errors first.
This step gets skipped constantly and it is where the cause usually surfaces:
mislabeled ground truth, a preprocessing step mangling a category, an encoding
problem, or an ambiguous boundary no model will fix. High-confidence errors
concentrated in one pattern are almost always a data bug, not a capacity limit.

### Train/Serve Skew

Offline metrics are fine, production is worse. In order of frequency:

1. **Feature computation differs** — two implementations of the same logic, in the
   training job and the serving path, that drifted apart.
2. **Feature availability differs** — a value present in the warehouse at training
   time has not landed at scoring time and arrives as NaN or a stale default.
3. **Distribution shift** — compare training and live feature distributions with a
   PSI or KS test per feature before assuming the model degraded.
4. **The training set was filtered** in a way live traffic is not — completed
   transactions only, or bot traffic removed offline but not online.

The structural fix is one shared implementation of feature computation, plus
logging the exact feature vector at scoring time so you can replay it offline and
confirm the model produces the same output.

## Common Anti-Patterns

❌ **Tuning hyperparameters before checking the model can overfit 50 examples** —
optimizing a pipeline that has a wiring bug.
✅ Run the tiny-subset test first; it takes seconds.

❌ **Reporting a score with no baseline.** 94% is meaningless at 93% base rate.
✅ Always print `DummyClassifier` / naive-forecast alongside.

❌ **Adding capacity to fix a train/validation gap** — a gap is variance, and more
capacity widens it.
✅ Regularize, cut features, or get more data — the learning curve decides which.

❌ **Adding data to fix high training error.** Underfitting ignores volume.
✅ More capacity, better features, or longer training.

❌ **Celebrating a 0.99 AUC.** On most real problems that is a leak.
✅ Investigate before shipping; near-perfect is a bug report.

❌ **Preprocessing fitted outside the CV loop.**
✅ Everything fitted goes inside a `Pipeline`.

❌ **Retraining to fix bad precision when ranking is already good.**
✅ Move the threshold and calibrate; retraining changes nothing about the cutoff.

❌ **Trusting aggregate accuracy across heterogeneous segments, and never reading
a misclassified example.**
✅ Slice by business value, then read thirty errors, highest-confidence first.

❌ **Assuming a production drop is model decay.** Usually it is skew.
✅ Log live feature vectors, replay them offline, compare distributions first.

## Model Debugging Checklist

- [ ] Model demonstrated able to overfit 50 examples
- [ ] Baseline (dummy / naive forecast) computed and reported alongside
- [ ] Metric appropriate to class balance and downstream decision
- [ ] Learning curve plotted; bias vs variance identified from its shape
- [ ] Slope at the largest training size checked before collecting more data
- [ ] Leakage checklist walked: target-derived, preprocessing, duplicates, groups, time, IDs
- [ ] All fitted transforms inside a `Pipeline`
- [ ] Split strategy matches data structure (stratified / grouped / temporal)
- [ ] Errors sliced by segment, cohort, source, and time
- [ ] Thirty misclassified examples read, high-confidence errors first
- [ ] Ranking quality and threshold treated as separate problems
- [ ] Probability calibration checked if probabilities are consumed downstream
- [ ] Training and serving feature computation verified identical
- [ ] Live feature vectors logged for offline replay and distribution comparison
