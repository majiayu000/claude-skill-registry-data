---
name: mlflow
description: "Track machine-learning experiments, parameters, metrics, artifacts, and model-registry changes with MLflow."
category: scientific
risk: safe
source: self
source_type: self
date_added: "2026-08-26"
tags: ["mlflow", "experiment-tracking", "model-registry", "mlops", "python", "claude"]
tools: ["claude", "cursor", "gemini", "codex"]
---

# MLflow Experiment Tracking AI Skill Guide

## Overview & Engine Architecture

MLflow records experiments as runs with parameters, metrics, tags, and artifacts. A tracking server (or local `mlruns/`) stores metadata; the Model Registry promotes versions through stages/aliases. Agents log enough to reproduce a run (code version, data URI, params), avoid silent metric overwrites, and register only evaluated candidates.

```
Training code
   -> mlflow.start_run
   -> log_param / log_metric / log_artifact
   -> log_model -> Registry (aliases/stages)
```

## When to use this skill

- Comparing hyperparameters and model families
- Attaching plots, confusion matrices, and conda/pip envs to runs
- Promoting models for batch/online inference with audit trail

## Operational directives

1. Set `experiment_name` explicitly; do not dump everything into `Default`.
2. Log data version / query / path as params or tags.
3. Use nested runs for sweeps when parent/child clarity helps.
4. Prefer `log_model` with signature/input example for serving readiness.
5. Gate registry promotion on held-out metrics, not training loss alone.

## Tracking example

```python
import mlflow
import mlflow.sklearn
from mlflow.models import infer_signature

mlflow.set_tracking_uri("http://127.0.0.1:5000")
mlflow.set_experiment("churn-models")

with mlflow.start_run(run_name="hgb-v3") as run:
    mlflow.log_params({"max_depth": 6, "learning_rate": 0.08})
    # ... train sklearn pipeline `clf` ...
    mlflow.log_metrics({"roc_auc": 0.91, "f1": 0.74})
    sig = infer_signature(X_train, clf.predict(X_train))
    mlflow.sklearn.log_model(clf, artifact_path="model", signature=sig)
    mlflow.set_tags({"data": "s3://bucket/churn_v4.parquet", "git_sha": "abc123"})
```

## CLI

```bash
mlflow ui --backend-store-uri sqlite:///mlflow.db --port 5000
mlflow runs list --experiment-name churn-models
```

## Common failures

| Symptom | Cause | Fix |
| --- | --- | --- |
| Empty UI | wrong tracking URI | align train + UI URIs |
| Cannot compare | inconsistent metric names | standardize naming |
| Huge artifacts | logging full datasets | log hashes/paths instead |
| Registry clutter | auto-register every run | register only candidates |

## Best practices

- One primary metric per experiment for sorting.
- Log environment (`mlflow.sklearn.autolog` carefully - still review).
- Immutable training data snapshots or lake table versions.
- Pair with `@scikit-learn` / `@pytorch` / `@huggingface-transformers`.

## Limitations

- Auth, multi-tenant servers, and artifact stores need ops setup.
- Autolog can miss custom loops - log manually when needed.
- Model serving deployment is separate from tracking.

## Related skills

- `@scikit-learn` / `@pytorch` - training frameworks
- `@airflow` / `@prefect` - schedule training jobs that log to MLflow
- `@jupyter` - exploratory runs still should log when kept
