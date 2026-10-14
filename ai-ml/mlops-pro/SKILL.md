---
name: mlops-pro
description: MLOps guidance — experiment tracking, model registry, feature stores, training pipelines, deployment, and monitoring.
category: development
---

## Overview

MLOps is DevOps for machine learning: the practices that take a model from a notebook to a reliable production system — experiment tracking, reproducible training, model registries, deployment strategies, and monitoring for data/model drift. Most ML projects fail not on modeling but on everything around it: untracked experiments, unreproducible training, and silent degradation in production.

This skill covers the MLOps lifecycle: tracking experiments, versioning data and models, building training pipelines, deploying safely, and monitoring what matters once live.

## When to use

- Setting up experiment tracking (MLflow, Weights & Biases).
- Versioning datasets and models (DVC, model registry).
- Building reproducible training pipelines.
- Deploying models (batch, real-time, edge).
- Monitoring models in production (drift, performance, data quality).
- Choosing MLOps tooling for a team.

## Core concepts

- **Experiment tracking.** Log params, metrics, code version, and artifacts for every run (MLflow, W&B). The question "which run produced this model?" must always have an answer. Track everything; storage is cheap, reruns aren't.
- **Reproducibility.** Pinned dependencies, seeded randomness, versioned data, containerized training. A training run that can't be reproduced is a rumor. Docker + lockfiles + data versions = reproducibility.
- **Data versioning.** DVC (git for data, pointer files in git), LakeFS, or dataset snapshots — models are functions of their training data; unversioned data means unexplainable models.
- **Model registry.** Staging → production lifecycle (MLflow Registry, SageMaker, Vertex): versioned models with metadata, approval gates, and lineage (which data + code + run produced this artifact). Promotion is a deliberate act, not a file copy.
- **Feature stores.** Feast, Tecton — consistent features between training and serving (the training-serving skew killer), feature reuse across models, point-in-time correctness. Worth it when multiple models share features; overkill for one model.
- **Training pipelines.** Orchestrated DAGs (Kubeflow, SageMaker Pipelines, Airflow, Metaflow): data validation → preprocessing → training → evaluation → registration. Scheduled retraining with the same pipeline that produced the original model.
- **Evaluation gates.** Automated checks before promotion: metric thresholds on holdout data, slice evaluations (performance per segment — aggregate metrics hide failures on minorities), comparison against the current production model (champion/challenger).
- **Deployment patterns.** Batch (scheduled scoring — simplest, cheapest), real-time endpoints (SageMaker, Triton, custom FastAPI), edge (ONNX/TFLite), shadow mode (new model scores live traffic without serving), canary (gradual traffic shift with metric comparison).
- **Drift monitoring.** Data drift (input distribution shifting), concept drift (relationships changing), prediction drift (output distribution shifting) — Evidently, WhyLabs, or custom statistical tests. Alert on drift, investigate before retraining blindly.
- **Data quality checks.** Schema validation, null rates, range checks on serving inputs (Great Expectations, custom) — most "model degradations" are data pipeline breakages wearing a costume.
- **Feedback loops.** Capture ground truth when it arrives (delayed labels are normal); close the loop for retraining. Without labels, you're flying blind on actual performance.
- **Cost management.** GPU utilization (idle GPUs are money burning), spot/preemptible training with checkpointing, right-sizing inference (smaller models, quantization, batching). Track $/1k predictions like any unit cost.
- **Governance.** Model cards (intended use, limitations, evaluation), audit trails (who promoted what when), bias/fairness evaluations per slice. Increasingly a regulatory requirement, always a trust requirement.
- **A/B testing models.** Champion/challenger as a randomized experiment — traffic split with business-metric comparison; the rigorous promotion path beyond offline metrics.
- **Explainability.** SHAP values and feature importance for debugging ("why this prediction?") and stakeholder trust — global behavior and individual decisions both need answers.

## Practical workflow

1. **Track from run one.** MLflow or W&B logging params/metrics/artifacts in the training script — before the first "real" experiment:
   ```python
   import mlflow
   with mlflow.start_run():
       mlflow.log_params({"lr": 1e-3, "batch": 64, "arch": "resnet50"})
       # ... train ...
       mlflow.log_metrics({"val_acc": 0.94, "val_loss": 0.21})
       mlflow.pytorch.log_model(model, "model")
   ```
2. **Version data with code.** DVC pointer files in git; dataset versions referenced in experiment metadata. Never train on "the CSV on my laptop."
3. **Build the pipeline.** Orchestrate data → train → evaluate → register as a DAG; the same pipeline runs for initial training and retraining. Containerize each step.
4. **Gate promotion.** Automated evaluation: threshold checks, slice metrics, champion comparison. Human approval for production promotion — the registry records who/when/why.
5. **Deploy with a safety pattern.** Shadow first (validate on live traffic), then canary (5% → 50% → 100% with metric comparison), with instant rollback to the previous registry version.
6. **Monitor three layers.** Data quality (schema, nulls, ranges) → drift (input/prediction distributions) → business/performance metrics (with delayed labels). Alert on the first, investigate the second, optimize the third.
   ```python
   # pseudocode: drift check on serving inputs vs training baseline
   report = evidently.report(reference=training_df, current=serving_window_df)
   if report.drift_detected("income", threshold=0.1):
       alert("data drift: income distribution shifted")
   ```
7. **Close the feedback loop.** Capture labels/outcomes; scheduled retraining jobs using the same pipeline; compare challenger vs champion before promoting.
8. **Document and govern.** Model cards per production model; audit trail in the registry; slice evaluations for fairness; cost dashboards per model.

## Common pitfalls

- **No experiment tracking** — "which run was best?" unanswerable; track from day one.
- **Unversioned training data** — unreproducible, unexplainable models; DVC/LakeFS.
- **Training-serving skew** — different preprocessing in training vs serving; feature store or shared code.
- **Aggregate metrics only** — failing silently on segments; slice evaluations always.
- **Deploying without shadow/canary** — production as the test environment; gradual rollouts.
- **Monitoring predictions, not data** — drift detected late; data quality checks first.
- **Retraining blindly on drift** — drift from a broken pipeline, not a changed world; investigate first.
- **No feedback loop** — never learning actual performance; capture ground truth.
- **GPU waste** — idle/oversized instances; utilization monitoring, spot training, right-sizing.
- **Notebook-to-production copy-paste** — untested, unreviewed code serving traffic; pipelines with CI.
- **No rollback plan** — bad model stuck in production; registry versions + instant rollback.
- **Ignoring data quality** — "model degradation" that's actually upstream breakage; validate inputs.
- **Skipping model cards/governance** — unknown limitations and no audit trail; document intended use and limits.
- **No champion/challenger discipline** — promoting on offline metrics alone; online experiments measuring business impact before full rollout.
