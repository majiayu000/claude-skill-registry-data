---
name: feature-importance-analysis
description: "\"Feature importance\" is ambiguous."
---

# Feature Importance Analysis (Verbose)

## Core Patterns

### The Four Methods Answer Four Questions

"Feature importance" is ambiguous. Name the question before picking the tool.

| Method | Question it answers | Data used | Cost | Known bias |
|---|---|---|---|---|
| Impurity / gain | Where did the trees split? | Train | Free | High-cardinality inflation, overfit-friendly |
| Permutation | How much does this fitted model rely on the column? | Test | k × n_repeats predictions | Breaks under correlation; extrapolates |
| Drop-column | What is lost if the feature does not exist? | CV | One refit per feature | Expensive; correlated substitutes mask loss |
| SHAP mean-abs | How large is this feature's typical contribution? | Any | Cheap for trees | Magnitude, not accuracy value |

They routinely disagree, and disagreement is information, not error. A feature
high on impurity but flat on permutation was split on often without improving
generalization — a classic overfitting signature.

### Why Impurity Importance Is Biased

A tree chooses splits by scanning candidate thresholds. A continuous feature
with 10,000 distinct values offers 9,999 candidate thresholds; a binary flag
offers one. More candidates means more chances that one splits the noise
favorably, so the high-cardinality feature accrues impurity reduction it did not
earn. The same mechanism promotes free-text hashes, timestamps, and IDs.

```python
import numpy as np
# Control column: pure noise, high cardinality
X_train["_noise"] = np.random.default_rng(0).normal(size=len(X_train))
model.fit(X_train, y_train)

rank = np.argsort(model.feature_importances_)[::-1]
# Anything ranked below "_noise" is not distinguishable from random
```

This one line reframes every importance table you produce. It is also computed
on training data, so a feature that memorizes the training set is rewarded.

### Permutation Importance Done Properly

```python
from sklearn.inspection import permutation_importance
import pandas as pd

r = permutation_importance(
    model, X_test, y_test,
    n_repeats=30,
    random_state=0,
    scoring="average_precision",   # match your real evaluation metric
    n_jobs=-1,
)

pd.DataFrame({
    "mean": r.importances_mean,
    "std": r.importances_std,
}, index=X_test.columns).sort_values("mean", ascending=False)
```

Three rules:

1. **Held-out data.** Permuting on the training set measures memorization. The
   sklearn docs are explicit about this; run it on test or in CV.
2. **The metric matters.** Permutation importance under accuracy and under
   average precision produce different rankings on imbalanced data — for the
   same reason those metrics disagree (see model-evaluation).
3. **Report the spread.** `importances_std` over `n_repeats` tells you whether a
   gap is real. A mean of 0.004 with std 0.006 is zero.

### The Correlation Problem

This is the failure senior practitioners watch for. Suppose `height_cm` and
`height_in` are both present. The model uses whichever it prefers; permuting one
leaves the information intact via the other, so *both* score near zero. A naive
reading concludes height does not matter and drops both — destroying a real
signal.

There is a second, subtler defect: permutation destroys the joint distribution.
Shuffling `income` independently of `loan_amount` produces rows with a $20k
income and a $2M mortgage. Those rows never existed in training, the model's
behavior there is unconstrained extrapolation, and the resulting score drop
measures fantasy as much as reliance.

Mitigations, in order of preference:

```python
from scipy.cluster import hierarchy
from scipy.stats import spearmanr
from collections import defaultdict

corr = spearmanr(X_train).correlation
corr = (corr + corr.T) / 2                       # enforce symmetry
np.fill_diagonal(corr, 1)
dist = 1 - np.abs(corr)
links = hierarchy.ward(hierarchy.distance.squareform(dist, checks=False))
cluster_ids = hierarchy.fcluster(links, 0.5, criterion="distance")

groups = defaultdict(list)
for idx, cid in enumerate(cluster_ids):
    groups[cid].append(X_train.columns[idx])
# Permute each group as a unit, or keep one representative per cluster
```

Alternatives: conditional permutation (permute within strata of the correlated
partner), or grouped drop-column, where you refit without the whole cluster.

### Drop-Column for Removal Decisions

Permutation answers "does this model use it." If your actual decision is "can we
retire this upstream pipeline," only refitting answers that.

```python
from sklearn.model_selection import cross_val_score

base = cross_val_score(pipe, X, y, cv=cv, scoring="average_precision")
for col in candidates:
    without = cross_val_score(pipe, X.drop(columns=[col]), y, cv=cv,
                              scoring="average_precision")
    delta = base.mean() - without.mean()
    se = np.sqrt(base.std()**2 + without.std()**2) / np.sqrt(len(base))
    print(f"{col:<24} delta {delta:+.4f}  se {se:.4f}")
```

Compare the delta against the interval. Most single-feature removals land inside
the noise band, which is itself the answer: the feature is not carrying weight.

### Importance Is Not Causation, and Not Fairness Clearance

A high-importance feature may be a proxy. A model that leans on `zip_code` is
often leaning on a correlate of race or income; removing the column does not
remove the effect, because the remaining features reconstruct it. Conversely, a
protected attribute with low importance does not certify a fair model. Importance
ranks model reliance, nothing more. For attribution of individual predictions and
its caveats, see the model-interpretability skill.

## Common Anti-Patterns

❌ **Shipping `feature_importances_` as the answer.** Biased toward
high-cardinality columns and computed on training data.
✅ Permutation importance on held-out data, with a noise-column control.

❌ **Permutation importance on the training set.** Measures memorization.
✅ `X_test` / `y_test`, or importance computed within CV folds.

❌ **A ranking with no uncertainty.** "0.012 beats 0.009" across 30 shuffles with
std 0.008 is not an ordering.
✅ Report `importances_mean ± importances_std` and treat overlaps as ties.

❌ **Pruning correlated features one at a time.** Each looks droppable while its
twin is present; drop both and lose the signal.
✅ Cluster on rank correlation, evaluate and prune per cluster.

❌ **Ignoring an ID-like column at the top of the list.** That is a leakage
alarm, not a discovery.
✅ Investigate provenance — such a feature almost always encodes the label.

❌ **Selecting features on the full dataset, then cross-validating.** Selection
saw the test folds; scores are optimistic.
✅ Put selection inside the `Pipeline` so it refits per fold.

❌ **Treating low importance for a protected attribute as a fairness result.**
✅ Measure outcome disparities directly; proxies survive column removal.

## Feature Importance Checklist

- [ ] Question named: model reliance vs removal value vs contribution size
- [ ] Noise control column added and its rank position noted
- [ ] Permutation importance computed on held-out data
- [ ] `scoring` matches the metric the model is actually judged on
- [ ] Means reported with standard deviations; overlaps treated as ties
- [ ] Correlated features clustered and handled as groups
- [ ] Impurity results cross-checked against permutation before use
- [ ] Removal decisions confirmed by a refit, not by ranking alone
- [ ] Top-ranked features audited for leakage and hindsight
- [ ] Rankings verified stable across seeds, folds, and bootstrap resamples
- [ ] Feature selection nested inside cross-validation, not applied before it
- [ ] No causal or fairness claims drawn from importance alone
