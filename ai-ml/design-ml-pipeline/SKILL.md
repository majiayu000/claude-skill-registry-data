---
name: design-ml-pipeline
description: Use when building or refactoring machine learning systems that need to move from experimentation to reliable production deployment
source: Sculley et al. "Hidden Technical Debt in Machine Learning Systems" NIPS (2015); Google MLOps Continuous Delivery and Automation Pipelines (2020); Huyen "Designing Machine Learning Systems" (2022)
tags: [ai, mlops, architecture, data-engineering]
related: [design-model-based-reinforcement-learning]
verified: true
---

# Design ML Pipeline

Design a production ML pipeline that automates training, validation, deployment, and monitoring to deliver reliable model updates continuously.

## Why This Is Best Practice

**Adopted by:** Google (TFX), Uber (Michelangelo), Airbnb (Bighead), Netflix (Metaflow) — all large ML orgs converge on pipeline automation
**Impact:** Teams with automated ML pipelines deploy models 46x more frequently (Google DORA ML 2022); Sculley et al. found ML systems accrue technical debt 10x faster than software systems without pipeline discipline
**Why best:** Manual ML workflows do not scale; data dependencies, model decay, and experiment tracking become unmanageable without automation

Sources: Sculley et al. NIPS 2015; Google "Practitioners Guide to MLOps" (2021); Huyen "Designing Machine Learning Systems" O'Reilly (2022)

## Steps

1. **Define the ML problem formally** — State: input features, prediction target, success metric (AUC, RMSE, business KPI), and serving latency/throughput requirements. Ambiguous problem statements produce unmeasurable models. Get stakeholder sign-off before writing code.

2. **Design data ingestion and validation** — Automate data collection from source systems. Implement schema validation (Great Expectations, TFX Data Validation) to catch data drift, missing features, and distribution shifts at ingestion time. Fail the pipeline on critical validation errors rather than silently training on corrupt data.

3. **Build a feature store or feature engineering pipeline** — Centralize feature computation to prevent train-serve skew (the #1 source of silent model degradation). Features computed differently in training vs serving produce models that perform worse in production than offline. Use point-in-time joins to prevent data leakage.

4. **Implement experiment tracking** — Log every training run: code version (git SHA), dataset version, hyperparameters, and metrics. Use MLflow, Weights & Biases, or Vertex AI Experiments. Never make architecture decisions from runs you cannot reproduce.

5. **Automate training and hyperparameter tuning** — Parameterize training scripts; never hardcode hyperparameters. Define a training compute budget and use Bayesian optimization or successive halving (Optuna, Ray Tune) rather than grid search. Reproducible training requires pinned library versions and fixed random seeds.

6. **Implement model validation gates** — Before promotion to staging: compare new model against current production model on a held-out evaluation set. Gate on: metric threshold (e.g., AUC ≥ 0.85), regression tests (known failure cases), and latency budget (p99 inference < 100 ms). Fail the pipeline if any gate fails.

7. **Design model registry and versioning** — Store trained model artifacts with metadata in a model registry (MLflow Registry, Vertex AI Model Registry). Each registered model version links to: training data version, code version, evaluation metrics. Never deploy a model that isn't registered.

8. **Implement staged rollout** — Deploy via shadow mode (log predictions without serving), canary (5% of traffic), then full rollout. Use feature flags to enable rollback in < 5 minutes. Automated rollback triggers if online metrics (prediction distribution, downstream business metric) degrade.

9. **Monitor model performance in production** — Track: prediction distribution (statistical drift from training distribution), feature distribution, downstream business metrics, and data pipeline freshness. Set alerts on distribution shift (KL divergence threshold). Retrain triggers automatically when drift exceeds threshold.

10. **Schedule retraining** — Define retraining trigger: time-based (weekly), data-volume-based (every 1M new samples), or drift-based (monitoring alert). Automate the full retrain-validate-deploy cycle. Manual retraining is a bottleneck for models that decay quickly (ad click-through, recommendation).

## Rules

- Train-serve skew prevention is non-negotiable; the feature engineering code that runs in training must be identical to the code running in the serving pipeline.
- Every pipeline run must be reproducible; if you cannot reproduce a training run from version control, your experiment tracking is broken.
- Shadow mode deployment is mandatory for high-stakes models; observe real predictions before they affect users.
- Model monitoring is part of the pipeline, not an afterthought; deploy monitoring infrastructure before deploying the model.

## Common Mistakes

- **No data validation** — training on silently corrupted data produces models that fail in non-obvious ways weeks after deployment.
- **Manual model promotion** — human approval without automated metric gates introduces subjective decision-making and delays; gate on measurements, not intuition.
- **Feature leakage** — using future data in training features overfits to the training set and produces models that appear excellent offline and fail in production.
- **Ignoring model latency** — a model with 95% AUC and 2-second inference latency may be worse than a 90% AUC model with 50 ms latency depending on user-facing requirements.

## When NOT to Use

- One-off analysis where the model will never be retrained or deployed to production
- Simple rule-based systems where a decision tree or heuristic is interpretable and sufficient
- Prototypes in the first 2 weeks of ML project exploration before problem definition is stable
