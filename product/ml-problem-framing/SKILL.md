---
name: ml-problem-framing
category: ml
description: Use when a task asks for a model, a score, a forecast or a prediction-driven feature — pin down the decision, target, unit, prediction time, metric and baseline before writing any modelling code
tech_stack: Python
source: original; informed by the scikit-learn user guide on metrics and scoring (cited, not reproduced)
---
# ML Problem Framing

## Overview

Most failed models were well trained on the wrong question: a target that leaks the outcome, a metric nobody acts on, a population that differs from the one scored in production, or no baseline to show the model is worth its upkeep. Framing is a short written spec, done before the first line of model code.

**Core principle:** a model exists to change a decision. If you cannot name the decision, the cost of each kind of error and the baseline the model must beat, you are not ready to train.

## 1. The framing card

Fill this in from the task, the code and the data. Put it in your closing message, and in the repository's model card or README section when the repo keeps one.

| Field | Question | Example |
|---|---|---|
| Decision | What action changes based on the output? | Send a retention offer to the top 5% risk each Monday |
| Target | Exact definition, as code or SQL | `churned = no paid order in the 60 days after snapshot_date` |
| Unit | One row is one what? | customer × weekly snapshot |
| Prediction time | When is the prediction made, what is known then? | Monday 00:00 UTC, data up to Sunday 23:59 |
| Horizon / label window | How far ahead, and when is the label final? | 60 days; labels final 60 days after snapshot |
| Population | Who is scored, who is excluded? | Active paying customers; exclude staff and test accounts |
| Metric | Which number decides, tied to error costs? | Precision@5% (offer budget is fixed) |
| Baseline | What it must beat | "days since last order" rule; current heuristic |
| Constraints | Latency, interpretability, fairness, retrain cadence | Weekly batch; reasons per customer for the CRM team |

Anything in this table the task does not settle and the data cannot answer — what counts as churn, which population — is a product question: numbered questions via add_task_comment, then stop on it. Choosing between two reasonable technical options (a 60- vs 90-day window when the task said "about two months") is a decision you make and record.

## 2. Choose the metric from the decision

| Situation | Use | Not |
|---|---|---|
| Fixed budget of actions (top-k) | precision@k, recall@k, lift@k | accuracy, ROC-AUC alone |
| Rare positive class | PR-AUC (average precision), recall at fixed precision | accuracy (99% by predicting "no") |
| Probabilities consumed downstream (pricing, expected value) | log loss, Brier score + calibration curve | ranking metrics alone |
| Asymmetric error costs | expected cost with an explicit cost matrix; tune the threshold for it | default 0.5 threshold |
| Regression with outliers that matter less | MAE, quantile loss | RMSE |
| Forecasting several series | MASE, or WAPE against a seasonal naive forecast | MAPE near zero actuals |

Write the metric as a tested function when the library does not provide it — a precision@k with an off-by-one is a wrong decision every week.

```python
def precision_at_k(y_true: np.ndarray, scores: np.ndarray, k: int) -> float:
    top = np.argsort(-scores, kind="stable")[:k]
    return float(y_true[top].mean())

def test_precision_at_k_counts_only_top_k() -> None:
    y = np.array([1, 0, 1, 0])
    s = np.array([0.9, 0.8, 0.1, 0.7])
    assert precision_at_k(y, s, 2) == 0.5
```

## 3. Baselines first

Before any learned model, compute the baseline on the same split and metric:

```python
from sklearn.dummy import DummyClassifier
baseline = DummyClassifier(strategy="prior").fit(X_train, y_train)
```

plus the simple rule a domain expert would use (sort by recency, last week's value, the seasonal naive forecast). If a gradient-boosted model beats the rule by a margin inside the noise, report that — "a rule is as good" is a valid, cheap result.

## 4. Prediction-time thinking prevents leakage

For every candidate feature, ask: at the prediction timestamp, in production, would this value already exist and would it have this value? `refund_issued` when predicting fraud, `account_closed_at` when predicting churn, an aggregate computed over the whole table — all fail this question. Build training rows with an as-of snapshot (leakage-safe-feature-engineering) so training and scoring see the world the same way.

## 5. Population and drift

The training population must match the scored population: same filters, same exclusions, same time span shape. If production scores new customers but training only has customers with 90 days of history, the model is evaluated on a population it never serves. Check the most recent period separately — a model that only works on old data is a drift problem waiting to be noticed.

## Common Mistakes

- Starting with model selection before the target is defined in code.
- A target window that overlaps the feature window.
- Reporting ROC-AUC for a top-5% campaign where only precision at the top matters.
- No baseline, so "0.81 AUC" has no meaning.
- Treating the 0.5 threshold as part of the model instead of a decision tuned on validation data.

## Red Flags

- A single feature with near-perfect predictive power.
- The target column, or a column derived from it, appears in the feature list.
- The task's success criterion is "build a model" with no metric — ask what decision it changes.
- Train and score populations filtered by different code paths.
