---
name: fairlearn-fairness
description: "Compute group fairness metrics (selection rate, demographic parity, equalized odds) per sensitive feature with `MetricFrame`, then mitigate disparities using Reductions algorithms (`ExponentiatedGradient` with constraint = `DemographicParity`/`EqualizedOdds`). Wire group-disaggregated assertions into the model-evaluation gate. Use when a model's decisions affect people and a stakeholder, auditor, or regulation (ECOA, GDPR Art. 22, EU AI Act high-risk) requires evidence of per-group outcomes, or when someone reports the model treats a specific group worse."
metadata:
  keywords: "fairlearn, fairness, demographic-parity, equalized-odds, bias-mitigation"
  version: "1.3.5"
---

# fairlearn-fairness

Fairlearn provides *"Metrics - Tools to assess which groups are
negatively impacted and compare models across fairness and accuracy
dimensions"* and *"Algorithms - Techniques to mitigate unfairness"*
per the [Fairlearn quickstart]. Two primitives: `MetricFrame` (group
disaggregation) + Reductions (`ExponentiatedGradient`,
`ThresholdOptimizer`).

## When to use

- Pre-deployment: assert per-group accuracy / selection rate
  disparities are within budget.
- Bias incident triage: a stakeholder reports the model is unfair to
  group X; produce evidence + a mitigated comparison.
- Compliance evidence (ECOA, GDPR Art. 22, EU AI Act high-risk
  systems): group-disaggregated metrics + mitigation provenance.

## Step 1 - Install

```bash
pip install fairlearn
# OR
conda install -c conda-forge fairlearn
```

Per the [Fairlearn quickstart].

## Step 2 - Compute disaggregated accuracy

```python
from fairlearn.metrics import MetricFrame
from sklearn.metrics import accuracy_score
from sklearn.tree import DecisionTreeClassifier

classifier = DecisionTreeClassifier(min_samples_leaf=10, max_depth=4)
classifier.fit(X, y_true)
y_pred = classifier.predict(X)

mf = MetricFrame(
    metrics=accuracy_score,
    y_true=y_true,
    y_pred=y_pred,
    sensitive_features=sex,
)
print(mf.by_group)
print(f"Disparity (max-min): {mf.difference()}")
```

Per the [Fairlearn quickstart]. `sensitive_features` can be a Series
or a 2-D array for intersectional analysis (sex × race).

## Step 3 - Compute selection-rate disparity

```python
from fairlearn.metrics import selection_rate

sr = MetricFrame(
    metrics=selection_rate,
    y_true=y_true,
    y_pred=y_pred,
    sensitive_features=sex,
)
print(sr.by_group)
# Demographic Parity Difference (DPD)
print(f"DPD: {sr.difference()}")
```

DPD = max group selection rate − min group selection rate. Industry
guidance often cites the **80% rule** (selection rate ratio ≥ 0.8
between groups) as a soft threshold; consult legal counsel for
binding thresholds in your jurisdiction.

## Step 4 - Equalized odds (TPR + FPR per group)

```python
from fairlearn.metrics import (
    true_positive_rate,
    false_positive_rate,
    MetricFrame,
)

mf = MetricFrame(
    metrics={
        "TPR": true_positive_rate,
        "FPR": false_positive_rate,
        "selection_rate": selection_rate,
    },
    y_true=y_true,
    y_pred=y_pred,
    sensitive_features=sex,
)
print(mf.by_group)
```

Equalized Odds requires *both* TPR and FPR to be equal across groups - stricter than Demographic Parity.

## Step 5 - Mitigation via Reductions

```python
from fairlearn.reductions import DemographicParity, ExponentiatedGradient

constraint = DemographicParity()
mitigator = ExponentiatedGradient(classifier, constraint)
mitigator.fit(X, y_true, sensitive_features=sex)
y_pred_mitigated = mitigator.predict(X)
```

Per the [Fairlearn quickstart]: this approach significantly reduces
selection-rate differences while maintaining accuracy. Other
constraints: `EqualizedOdds`, `TruePositiveRateParity`,
`FalsePositiveRateParity`.

## Step 6 - Threshold post-processing

```python
from fairlearn.postprocessing import ThresholdOptimizer

postprocess = ThresholdOptimizer(
    estimator=classifier,
    constraints="demographic_parity",
    prefit=True,
)
postprocess.fit(X, y_true, sensitive_features=sex)
y_pred_pp = postprocess.predict(X, sensitive_features=sex)
```

Per the [Fairlearn postprocessing] guide, Fairlearn currently supports
one postprocessing technique, `ThresholdOptimizer`. Cheaper than
retraining; trades model output for per-group threshold adjustment.

## Step 7 - CI assertion

```python
def assert_fairness(y_true, y_pred, sensitive, max_dpd=0.10):
    sr = MetricFrame(
        metrics=selection_rate,
        y_true=y_true,
        y_pred=y_pred,
        sensitive_features=sensitive,
    )
    dpd = sr.difference()
    if dpd > max_dpd:
        raise AssertionError(
            f"Demographic Parity Difference {dpd:.3f} exceeds budget {max_dpd}"
        )

assert_fairness(y_true, y_pred, sex, max_dpd=0.10)
```

## Anti-patterns

| Anti-pattern | Why it fails | Fix |
|---|---|---|
| Compute aggregate accuracy only | Hides group disparities | Always use `MetricFrame` (Step 2) |
| Choose Demographic Parity for all problems | DP can be inappropriate when base rates legitimately differ across groups | Match constraint to legal/ethical context: DP, EO, EOD, EOP |
| Mitigate via training data resampling alone | Doesn't generalize to new data; brittle | Use Reductions (Step 5) or post-processing (Step 6) |
| Single sensitive attribute (e.g., sex only) | Misses intersectional disparities (Black women) | Pass 2-D sensitive_features for intersection (Step 2) |
| Hard-code 80% rule globally | Not legally binding everywhere; not appropriate for all metrics | Tune `max_dpd` per use case + legal counsel; use waiver template if scope-exclusion needed |

## Limitations

- Fairlearn does not detect proxy discrimination (zip code as
  proxy for race). Pair with feature-correlation analysis and
  domain expertise.
- Mitigation often comes at accuracy cost; document the tradeoff
  with stakeholders, not unilaterally.

## References

- [Fairlearn quickstart] - MetricFrame, selection_rate,
  ExponentiatedGradient
- [Fairlearn postprocessing] - ThresholdOptimizer

[Fairlearn quickstart]: https://fairlearn.org/main/quickstart.html
[Fairlearn postprocessing]: https://fairlearn.org/main/user_guide/mitigation/postprocessing.html
