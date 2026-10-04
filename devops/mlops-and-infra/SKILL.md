---
name: mlops-and-infra
version: 1.0.0
author: Param
description: Enforces ML infrastructure, experiment tracking, reproducibility, model packaging, CI/CD, monitoring, and infrastructure-as-code standards at principal-engineer level.
applies-to: .py, .yaml, .yml, .toml, Dockerfile, Makefile, .tf, .sh, training pipelines, model serving, CI/CD configs
---

## Intent

This skill ensures that every model trained in this session is production-ready from an operational standpoint — not just correct on the held-out test set, but reproducible, versioned, deployable, monitored, and maintainable. It prevents the ML graveyard of experiments that cannot be reproduced, models that cannot be redeployed, and production failures that go undetected for days. Every experiment is an artifact; every artifact has provenance; every deployment has a monitoring plan. Loading this skill means no model ships without the infrastructure to catch it failing.

See also: [`ml-engineering/SKILL.md`](../ml-engineering/SKILL.md) for modeling standards, [`api-and-system-design/SKILL.md`](../api-and-system-design/SKILL.md) for serving API design, [`software-architecture/SKILL.md`](../software-architecture/SKILL.md) for project structure.

---

## 1. Experiment Tracking

**Every experiment must be logged with all of the following before training begins:**
1. All hyperparameters (from the config dataclass — log the entire object)
2. The dataset version (hash, DVC tag, or dataset registry version)
3. The code version (git commit hash — fail loudly if the working tree is dirty)
4. The library environment (use `mlflow.log_artifact("requirements.txt")` or equivalent)
5. The random seed
6. A human-readable experiment name and description

```python
import mlflow
import subprocess
import hashlib

def start_experiment(config: TrainingConfig, dataset_path: str) -> None:
    # Fail if working tree is dirty — experiments must be reproducible from git
    result = subprocess.run(["git", "status", "--porcelain"], capture_output=True, text=True)
    if result.stdout.strip():
        raise RuntimeError(
            "Working tree is dirty. Commit or stash changes before running experiments. "
            f"Dirty files:\n{result.stdout}"
        )

    git_hash = subprocess.check_output(["git", "rev-parse", "HEAD"]).decode().strip()
    data_hash = hashlib.md5(open(dataset_path, "rb").read()).hexdigest()

    mlflow.set_experiment(config.experiment_name)
    mlflow.log_params(dataclasses.asdict(config))
    mlflow.set_tags({
        "git_commit": git_hash,
        "data_hash": data_hash,
        "data_path": dataset_path,
    })
```

**Never name model files with versions in the filename.** `model_v2_final_FINAL.pkl` is forbidden. Use the model registry.

```
# FORBIDDEN
model_v1.pkl
model_v2_final.pkl
best_model_FINAL_USE_THIS.pkl

# CORRECT — versions tracked in MLflow/W&B registry
mlflow.register_model("runs:/abc123/model", "ChurnPredictor")
```

**Experiments must be reproducible.** After logging, anyone with access to the experiment record and the git hash must be able to reproduce the run within a percentage point of the reported metrics. If they cannot, the experiment is not valid.

**Model registry stages:**
- `None` → freshly logged, not reviewed
- `Staging` → validated, passed quality gates, ready for A/B testing
- `Production` → currently serving traffic
- `Archived` → superseded; kept for rollback

Every stage transition must have a promotion justification logged as a model registry description.

---

## 2. Reproducibility Standards

**Every ML project must have a containerized or environment-captured runtime.** One of the following is mandatory:
1. `Dockerfile` that installs all dependencies from pinned versions
2. `conda` environment file with exact versions (`conda env export --no-builds > environment.yml`)
3. `pyproject.toml` with exact version pins + `uv lock` / `poetry.lock` committed

**Data versioning: every training run must reference a specific, immutable data snapshot:**
- Preferred: DVC with remote storage (`dvc add data/raw && dvc push`)
- Acceptable: Delta Lake or Iceberg table with a specific snapshot ID or timestamp
- Minimum: document the exact S3/GCS path and file hash in the experiment tracking log

**Training pipelines must be idempotent.** Running a training pipeline twice with the same config and data must produce the same artifacts:
- Set the random seed before any stochastic operation
- Use deterministic algorithms where available (PyTorch: `torch.use_deterministic_algorithms(True)`)
- Document any known sources of non-determinism (GPU floating-point, data loading order)

**Never depend on local file paths.** All data, artifact, and config locations must come from environment variables or a config file:

```python
# WRONG
df = pd.read_csv("/Users/param/data/training_data.csv")

# CORRECT
from mypackage.config import settings
df = pd.read_csv(settings.training_data_path)
```

---

## 3. Model Packaging and Serving

**Every model artifact must be packaged with its preprocessing pipeline.** The artifact that gets deployed must contain everything needed to go from raw input to prediction:

```python
# Using MLflow pyfunc for a custom packaging wrapper
class ChurnModelWrapper(mlflow.pyfunc.PythonModel):
    def load_context(self, context: mlflow.pyfunc.PythonModelContext) -> None:
        self.pipeline = joblib.load(context.artifacts["pipeline"])
        self.feature_validator = FeatureValidator.from_registry(CHURN_FEATURES)

    def predict(
        self,
        context: mlflow.pyfunc.PythonModelContext,
        model_input: pd.DataFrame,
    ) -> pd.DataFrame:
        self.feature_validator.validate(model_input)  # validate at inference time
        return pd.DataFrame(
            {"churn_probability": self.pipeline.predict_proba(model_input)[:, 1]}
        )
```

**Define an explicit input schema and output schema for every model. Validate at inference time:**

```python
from pydantic import BaseModel, Field

class ChurnPredictionInput(BaseModel):
    user_id: int
    days_since_last_purchase: int = Field(ge=0)
    total_spend_90d: float = Field(ge=0.0)
    support_tickets_30d: int = Field(ge=0)
    subscription_tier: Literal["free", "basic", "premium"]

class ChurnPredictionOutput(BaseModel):
    user_id: int
    churn_probability: float = Field(ge=0.0, le=1.0)
    model_version: str
    prediction_timestamp: datetime
```

**Document batch vs. online serving choice with latency and throughput requirements:**

```python
"""
Serving Strategy: Batch (not online)
=====================================
Requirement: Predictions needed once daily for the marketing team's send-list.
Latency: No SLO — batch job runs overnight.
Throughput: ~500k users per run.
Decision: Online serving would add infrastructure complexity for no benefit.
          Batch job runs via Airflow at 02:00 UTC.
"""
```

**Every model REST API must include at minimum:**
- `GET /health` — returns 200 if the model is loaded and ready; non-200 triggers load balancer removal
- `POST /predict` — validates input with Pydantic, runs inference, returns structured output
- `GET /model-info` — returns model version, training date, feature list, and performance summary

---

## 4. CI/CD for ML

**Every pull request must automatically run:**
1. Unit tests (`pytest tests/unit/`)
2. Linting (`ruff check .`)
3. Type checking (`mypy src/`)
4. Import sorting (`isort --check .`)
5. Formatting check (`black --check .`)

**Model training jobs must be parameterized and runnable from the CLI with a `--config` flag:**

```python
# pyproject.toml entry point
[project.scripts]
train-model = "mypackage.cli.train:main"

# CLI
$ train-model --config configs/churn_v2.yaml --run-name "churn-v2-experiment-3"
```

**Never chain training steps with bash scripts.** Use a workflow orchestrator for multi-step pipelines. Acceptable choices:
- **Prefect** (preferred for ML, Python-native)
- **Airflow** (for data engineering heavy pipelines)
- **Temporal** (for long-running, durable workflows)
- **Metaflow** (for data science workflows with S3 artifact tracking)

```python
# WRONG — bash pipeline
# run_training.sh: python preprocess.py && python train.py && python evaluate.py

# CORRECT — Prefect flow
@flow(name="churn-training-pipeline")
def train_churn_model(config: TrainingConfig) -> str:
    raw_data = extract_features(config.data_cutoff_date)
    processed = preprocess_features(raw_data, config)
    model_uri = train_model(processed, config)
    metrics = evaluate_model(model_uri, processed.test_set)
    if metrics.auc_roc >= config.promotion_threshold:
        promote_to_staging(model_uri, metrics)
    return model_uri
```

**Artifact storage: all model files, evaluation reports, and data samples must be stored in versioned object storage.** Local filesystem storage is for development only, never for production artifacts.

---

## 5. Monitoring and Alerting

**Every deployed model must have monitoring configured before go-live. These three are mandatory:**

1. **Input data drift detection**: Monitor the distribution of each input feature. Use Population Stability Index (PSI) or Kolmogorov-Smirnov test. Alert when PSI > 0.2 for any feature.

2. **Output distribution monitoring**: Track the distribution of model predictions over time. A sudden shift in predicted probabilities often precedes a drop in business metrics.

3. **Latency tracking**: Track p50, p95, and p99 latency. Alert when p95 exceeds the SLO.

```python
# Monitoring config — defined before deployment, not after
@dataclass
class ModelMonitoringConfig:
    model_name: str
    input_features_to_monitor: list[str]   # subset of all features; focus on high-impact ones
    psi_alert_threshold: float = 0.2
    prediction_drift_threshold: float = 0.15  # KS statistic
    latency_p95_slo_ms: float = 200.0
    monitoring_cadence: str = "daily"          # "hourly", "daily", "weekly"
    retraining_trigger: str = "performance"    # "time", "performance", "drift"
    retraining_metric_threshold: float = 0.05  # AUC-ROC drop that triggers retraining
    alert_channel: str                          # Slack channel, PagerDuty policy, etc.
```

**Define SLOs before deployment.** Every deployed model must have documented SLOs:

| SLO | Value | Alert Threshold |
|-----|-------|-----------------|
| p50 latency | < 50ms | > 75ms |
| p95 latency | < 200ms | > 250ms |
| p99 latency | < 500ms | > 600ms |
| Error rate | < 0.1% | > 0.5% |
| Throughput | > 100 req/s | < 80 req/s |

**Retraining triggers must be explicit and documented. Choose one (or combine):**
- **Time-based**: retrain every N days regardless of performance
- **Performance-based**: retrain when business metric drops by X%
- **Drift-based**: retrain when PSI > threshold for K features

Document the trigger strategy in the model registry entry and in the monitoring config.

**Use shadow mode or canary deployment for new model versions:**

```
Shadow mode: new model receives 100% of traffic but its predictions are not served.
             Compare against production model offline. Promote when satisfied.

Canary: new model serves 5% of traffic. Monitor for 48 hours.
        If error rate and latency SLOs are met, ramp to 25%, 50%, 100%.
        Rollback immediately if any SLO is violated.
```

---

## 6. Infrastructure as Code

**All infrastructure must be defined in code. No manual cloud console configuration is allowed for any resource that needs to be reproducible or auditable.**

Acceptable IaC tools:
- **Terraform** (preferred for multi-cloud)
- **Pulumi** (preferred when Python is the team language)
- **AWS CDK** (preferred for AWS-only stacks)

```hcl
# terraform/modules/ml-serving/main.tf
resource "aws_sagemaker_endpoint" "churn_model" {
  name                 = "churn-predictor-${var.environment}"
  endpoint_config_name = aws_sagemaker_endpoint_configuration.churn_model.name

  tags = {
    Project     = "churn-prediction"
    Owner       = "ml-team"
    Environment = var.environment
    CostCenter  = "ml-platform"
  }
}
```

**Secrets management: secrets must never appear in code, environment files committed to git, or CI/CD logs.** Use:
- AWS: Secrets Manager or Parameter Store
- GCP: Secret Manager
- Self-hosted: HashiCorp Vault

```python
# WRONG — secret in environment file committed to git
OPENAI_API_KEY=sk-abc123xyz

# CORRECT — retrieved at runtime from secrets manager
import boto3

def get_secret(secret_name: str) -> str:
    client = boto3.client("secretsmanager")
    return client.get_secret_value(SecretId=secret_name)["SecretString"]
```

**Every cloud resource must be tagged with all of:**
- `Project`: which ML project or product this serves
- `Owner`: team or individual responsible
- `Environment`: `development`, `staging`, or `production`
- `CostCenter`: for budget allocation

Untagged resources cannot be audited and will generate alerts in any mature cloud environment.
