---
name: mlops
description: >
  Design and implement ML operations — model registry, serving patterns,
  deployment strategies (shadow/canary/blue-green), drift detection,
  feature stores, retraining triggers, and prediction monitoring. Use when
  asked to "deploy a model", "model registry", "MLflow", "feature store",
  "drift detection", "retrain trigger", "shadow mode", "model versioning",
  "serving infrastructure", or "ML pipeline". Do NOT use for: prompt
  engineering or RAG pipelines — see prompt-engineering and rag-architect
  skills. Do NOT use for: general API deployment without an ML component.
origin: yamtam-original
license: MIT © 2026 Vũ Văn Tâm
version: 1.0.0
compatibility: "MLflow ≥ 2.x, BentoML ≥ 1.x, Ray Serve ≥ 2.x. Patterns are framework-agnostic."
---

## When to Use

- Use when: shipping a trained model as a production API endpoint
- Use when: tracking experiments and promoting models to production
- Use when: detecting model quality degradation without ground-truth labels
- Use when: building a retraining pipeline triggered by drift or schedule
- Do NOT use for: prompt/RAG pipelines — those are LLM patterns, not classical MLOps
- Do NOT use for: data engineering ETL — model serving starts after features are ready

---

## Model Registry

A registry gives every model artifact a version, status, and audit trail.

```python
import mlflow

# Log a training run
with mlflow.start_run():
    mlflow.log_params({"learning_rate": 0.01, "n_estimators": 100})
    mlflow.log_metrics({"auc": 0.94, "f1": 0.87})
    mlflow.sklearn.log_model(model, "model", registered_model_name="churn-predictor")

# Promote to production after review
client = mlflow.MlflowClient()
client.transition_model_version_stage(
    name="churn-predictor", version="3", stage="Production"
)
# Stages: None → Staging → Production → Archived
```

**Never deploy directly from a training run** — always register, validate in staging, then promote.

---

## Serving Patterns

| Pattern | Use when | Latency | Throughput |
|---|---|---|---|
| **REST endpoint** | Single predictions, interactive | < 100 ms | Medium |
| **Batch inference** | Scoring millions of rows offline | N/A | High |
| **Streaming inference** | Kafka/Kinesis event scoring | < 500 ms | High |
| **Shadow mode** | Validate new model against live traffic | Async | — |

```python
# BentoML REST endpoint
import bentoml
from bentoml.io import JSON

runner = bentoml.mlflow.get("churn-predictor:production").to_runner()
svc = bentoml.Service("churn-api", runners=[runner])

@svc.api(input=JSON(), output=JSON())
async def predict(input_data: dict) -> dict:
    features = extract_features(input_data)
    score = await runner.predict.async_run([features])
    return {"churn_probability": float(score[0])}
```

---

## Deployment Strategies

```
Shadow mode   → new model receives same traffic, results discarded
               → compare predictions vs champion offline
               → zero user risk, full production signal

Canary        → new model serves 5% of traffic
               → monitor error rate + business metric
               → ramp: 5% → 20% → 50% → 100%

Blue/green    → two identical stacks, instant cutover via load balancer
               → instant rollback by flipping DNS/LB
               → costs 2× infra during transition
```

Default path: **shadow → canary → full rollout**. Skip shadow only if model is a minor retrain with identical feature schema.

---

## Drift Detection

Drift = distribution of inputs or outputs diverges from training distribution.

| Type | What shifts | Detection method |
|---|---|---|
| **Data drift** | Input feature distribution | PSI, KS test, Jensen-Shannon divergence |
| **Concept drift** | Relationship between X and y | Monitor prediction accuracy on labeled sample |
| **Prediction drift** | Output distribution | Score distribution histogram shift |

```python
# PSI (Population Stability Index) — industry standard for data drift
def psi(expected, actual, buckets=10):
    e, _ = np.histogram(expected, bins=buckets, density=True)
    a, _ = np.histogram(actual, bins=np.histogram(expected, bins=buckets)[1], density=True)
    e = np.clip(e, 1e-6, None); a = np.clip(a, 1e-6, None)
    return np.sum((a - e) * np.log(a / e))

# PSI < 0.1: no drift. 0.1–0.25: moderate. > 0.25: retrain.
```

Run drift checks on a daily sample — not on every prediction (too expensive).

---

## Feature Store

Solves **training-serving skew** — training and serving must compute features identically.

```
Offline store  → historical features for training (S3, BigQuery, Delta Lake)
Online store   → low-latency feature lookup for serving (Redis, DynamoDB)
Feature server → materializes offline → online on a schedule

Request time:
  features = feature_store.get_online_features(
      feature_refs=["user:age", "user:churn_score_30d"],
      entity_rows=[{"user_id": user_id}]
  )
```

If you can't afford a feature store (Feast, Tecton, Hopsworks): at minimum, **share the same feature-computation code** between training and serving via a Python package — no copy-paste.

---

## Retraining Triggers

| Trigger | When to use |
|---|---|
| **Scheduled** | Stable distribution, weekly/monthly cadence |
| **Drift threshold** | PSI > 0.25 on key features |
| **Performance degradation** | Accuracy drops below SLO on labeled holdout |
| **Data volume** | New data volume exceeds X% of training set |

```yaml
# Example Airflow DAG trigger
retrain_dag:
  schedule: "@weekly"
  on_failure_callback: alert_slack
  tasks:
    - check_drift        # abort if PSI < 0.1 (no drift → no need)
    - run_training
    - evaluate_vs_champion  # only promote if new model beats current
    - promote_to_staging
    - notify_ml_team
```

Never auto-promote to production — a human or automated gate must compare champion vs challenger.

---

## Prediction Monitoring

Log every prediction with enough context to debug incidents and detect drift.

```python
# Minimum prediction log schema
{
  "request_id":   str,   # for deduplication
  "model_name":   str,
  "model_version": str,
  "timestamp":    ISO8601,
  "features":     dict,  # input snapshot — enables drift recomputation
  "prediction":   float | int | str,
  "latency_ms":   int,
  "ground_truth": None   # filled in later via feedback loop
}
```

Store prediction logs separately from app logs — they need long retention for drift analysis.

---

## Anti-Fake-Pass Rules

Before claiming an ML deployment is done, you MUST show:
- [ ] Model registered with version + stage — not deployed from a raw artifact path
- [ ] Serving schema validated — feature names/types match training schema exactly
- [ ] Shadow or canary deployed first — not straight to 100% traffic
- [ ] Drift detection scheduled — PSI or equivalent running on daily sample
- [ ] Retraining trigger defined — schedule or drift threshold, not manual-only
- [ ] Prediction logs captured — include features snapshot, model version, latency
- [ ] Rollback path tested — old model version can be restored without a redeploy

Reference: `gates/anti-fake-pass-gate.md`
