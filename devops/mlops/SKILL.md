---
name: mlops
description: Machine Learning Operations including model deployment, training pipelines, model monitoring, feature stores, experiment tracking, and ML infrastructure. Use when deploying ML models, building training pipelines, monitoring model performance, or managing ML infrastructure.
user-invocable: true
allowed-tools: Read, Grep, Glob, Edit, Write, Bash
---

# MLOps Skill

You are an MLOps Engineer specializing in productionizing machine learning models, building scalable training pipelines, monitoring model performance, and managing ML infrastructure. You bridge the gap between data science and production engineering.

## Core Responsibilities

1. **Model Deployment**
   - Containerizing ML models
   - Serving infrastructure (REST, gRPC, batch)
   - Model versioning
   - A/B testing and canaries

2. **Training Pipelines**
   - Pipeline orchestration (Kubeflow, Airflow)
   - Data versioning
   - Feature engineering pipelines
   - Distributed training

3. **Model Monitoring**
   - Data drift detection
   - Model performance degradation
   - Concept drift
   - Bias detection

4. **Feature Store**
   - Feature registry
   - Online vs offline features
   - Feature versioning
   - Feature sharing

5. **ML Infrastructure**
   - GPU cluster management
   - Auto-scaling for inference
   - Model registry
   - Experiment tracking

## ML Architecture Patterns

### Model Serving Patterns

```yaml
# model-serving-patterns.yml
patterns:

  real_time_rest_api:
    use_case: "Low latency predictions"
    latency_sla: "<100ms p99"
    framework: "FastAPI + Model"
    scaling: "Horizontal with CPU"
    example: "Fraud detection, recommendations"

  real_time_grpc:
    use_case: "High throughput streaming"
    latency_sla: "<50ms p99"
    framework: "gRPC + Triton/TF Serving"
    scaling: "Horizontal with GPU"
    example: "Computer vision, NLP"

  batch_inference:
    use_case: "Large scale offline processing"
    throughput: "Millions of records"
    framework: "Spark + Model"
    scaling: "Cluster based on data size"
    example: "Customer churn scoring, forecasting"

  streaming_inference:
    use_case: "Real-time event processing"
    latency_sla: "<1 second"
    framework: "Kafka + Flink/Spark Streaming"
    scaling: "Stream processing cluster"
    example: "IoT anomaly detection"

  edge_deployment:
    use_case: "On-device inference"
    constraints: "Memory, battery, offline"
    framework: "TensorFlow Lite, ONNX"
    optimization: "Quantization, pruning"
    example: "Mobile apps, IoT devices"

  serverless:
    use_case: "Variable traffic, cost optimization"
    cold_start: "Acceptable"
    framework: "AWS Lambda + Container"
    scaling: "Auto (0 to N)"
    example: "Ad-hoc predictions"
```

### Reference Architecture

```yaml
# ml-platform-architecture.yml
platform_components:

  data_ingestion:
    sources:
      - streaming: kafka
      - batch: s3/hdfs
      - databases: postgres/mongodb
    quality: great_expectations
    validation: schema_validation

  feature_store:
    online_store: redis  # Low latency features
    offline_store: delta_lake  # Training data
    registry: feast
    transformation: spark/flink

  training_pipeline:
    orchestration: kubeflow_pipelines
    compute: kubernetes_gpu_pool
    frameworks:
      - pytorch
      - tensorflow
      - sklearn
      - xgboost
    distributed: horovod/ray

  model_registry:
    tool: mlflow
    versioning: semantic_versioning
    artifacts: s3
    metadata: postgresql

  experiment_tracking:
    tool: mlflow/weights_and_biases
    metrics: automatic_logging
    artifacts: model_binaries
    comparison: parallel_coordinates

  model_serving:
    platform: seldon_core/kserving
    gateway: istio
    scaling: hpa_gpu
    monitoring: prometheus

  monitoring:
    data_drift: evidently
    performance: custom_metrics
    alerts: pagerduty
    dashboards: grafana

  ci_cd:
    training: jenkins/github_actions
    testing: pytest/pytest_ml
    deployment: argocd
    promotion: automated_canary
```

## Training Pipelines

### Kubeflow Pipeline Example

```python
# training_pipeline.py
import kfp
from kfp import dsl
from kfp.components import create_component_from_func

@create_component_from_func
def load_data(dataset_path: str) -> str:
    """Load and validate training data."""
    import pandas as pd
    df = pd.read_parquet(dataset_path)
    # Validation logic
    assert len(df) > 1000, "Insufficient data"
    output_path = '/tmp/train_data.parquet'
    df.to_parquet(output_path)
    return output_path

@create_component_from_func
def feature_engineering(input_path: str) -> str:
    """Create features."""
    import pandas as pd
    from feature_engineering import create_features

    df = pd.read_parquet(input_path)
    df = create_features(df)
    output_path = '/tmp/features.parquet'
    df.to_parquet(output_path)
    return output_path

@create_component_from_func
def train_model(
    features_path: str,
    model_params: dict,
    experiment_name: str
) -> str:
    """Train model with MLflow tracking."""
    import mlflow
    import xgboost as xgb
    import pandas as pd
    from sklearn.model_selection import train_test_split

    df = pd.read_parquet(features_path)
    X = df.drop('target', axis=1)
    y = df['target']
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)

    mlflow.set_experiment(experiment_name)
    with mlflow.start_run():
        # Train
        model = xgb.XGBClassifier(**model_params)
        model.fit(X_train, y_train)

        # Evaluate
        train_score = model.score(X_train, y_train)
        test_score = model.score(X_test, y_test)

        # Log metrics
        mlflow.log_params(model_params)
        mlflow.log_metric('train_accuracy', train_score)
        mlflow.log_metric('test_accuracy', test_score)

        # Log model
        mlflow.xgboost.log_model(model, 'model')

        # Save model
        model_path = '/tmp/model.json'
        model.save_model(model_path)

    return model_path

@create_component_from_func
def evaluate_model(
    model_path: str,
    test_data_path: str,
    threshold: float
) -> bool:
    """Evaluate model and check thresholds."""
    import xgboost as xgb
    import pandas as pd
    import json

    model = xgb.XGBClassifier()
    model.load_model(model_path)

    df = pd.read_parquet(test_data_path)
    X = df.drop('target', axis=1)
    y = df['target']

    score = model.score(X, y)
    print(f"Model accuracy: {score}")

    return score >= threshold

@dsl.pipeline(
    name='Training Pipeline',
    description='End-to-end model training'
)
def training_pipeline(
    dataset_path: str,
    model_params: dict = {'max_depth': 6, 'n_estimators': 100},
    accuracy_threshold: float = 0.85
):
    """Define pipeline DAG."""

    # Step 1: Load data
    load_task = load_data(dataset_path)

    # Step 2: Feature engineering
    feature_task = feature_engineering(load_task.output)

    # Step 3: Train model
    train_task = train_model(
        feature_task.output,
        model_params,
        'churn-prediction'
    )

    # Step 4: Evaluate
    evaluate_task = evaluate_model(
        train_task.output,
        feature_task.output,
        accuracy_threshold
    )

    # Conditional deployment
    with dsl.Condition(evaluate_task.output == True):
        deploy_task = deploy_model(train_task.output)

# Compile
kfp.compiler.Compiler().compile(
    training_pipeline,
    'training_pipeline.yaml'
)
```

## Feature Store

### Feast Configuration

```yaml
# feature_store.yaml
project: churn_prediction
registry: s3://mlops-registry/registry.db
provider: aws
online_store:
  type: redis
  connection_string: redis://redis:6379
offline_store:
  type: redshift
  host: redshift.cluster.region.redshift.amazonaws.com
  port: 5439
database: ml_features
schema: public

entities:
  - name: customer_id
    value_type: STRING
    join_key: customer_id
    description: "Unique customer identifier"

feature_views:
  - name: customer_transactions
    entities:
      - customer_id
    ttl: 86400  # 24 hours
    online: true
    offline: true
    features:
      - name: total_spend_30d
        dtype: FLOAT
        description: "Total spend in last 30 days"
      - name: transaction_count_30d
        dtype: INT
        description: "Number of transactions in last 30 days"
      - name: avg_transaction_amount
        dtype: FLOAT
        description: "Average transaction amount"
    batch_source:
      type: redshift
      query: |
        SELECT
          customer_id,
          SUM(amount) as total_spend_30d,
          COUNT(*) as transaction_count_30d,
          AVG(amount) as avg_transaction_amount
        FROM transactions
        WHERE transaction_date >= CURRENT_DATE - INTERVAL '30 days'
        GROUP BY customer_id

  - name: customer_demographics
    entities:
      - customer_id
    ttl: null  # Static features
    online: true
    features:
      - name: signup_date
        dtype: STRING
      - name: account_type
        dtype: STRING
    batch_source:
      type: redshift
      table: customers

  - name: real_time_clicks
    entities:
      - customer_id
    ttl: 3600  # 1 hour
    online: true
    offline: false
    features:
      - name: clicks_last_hour
        dtype: INT
    stream_source:
      type: kafka
      bootstrap_servers: kafka:9092
      topic: clickstream
```

```python
# feature_store_client.py
from feast import FeatureStore
import pandas as pd

store = FeatureStore(repo_path='.')

# Get online features for real-time inference
def get_online_features(customer_ids):
    features = store.get_online_features(
        features=[
            'customer_transactions:total_spend_30d',
            'customer_transactions:transaction_count_30d',
            'customer_demographics:account_type',
            'real_time_clicks:clicks_last_hour'
        ],
        entity_rows=[{'customer_id': cid} for cid in customer_ids]
    )
    return features.to_df()

# Get historical features for training
def get_historical_features(customer_ids, timestamps):
    entity_df = pd.DataFrame({
        'customer_id': customer_ids,
        'event_timestamp': timestamps
    })

    training_df = store.get_historical_features(
        entity_df=entity_df,
        features=[
            'customer_transactions:total_spend_30d',
            'customer_transactions:transaction_count_30d',
            'customer_demographics:account_type'
        ]
    ).to_df()

    return training_df
```

## Model Serving

### Seldon Deployment

```yaml
# seldon-deployment.yaml
apiVersion: machinelearning.seldon.io/v1
kind: SeldonDeployment
metadata:
  name: churn-predictor
  namespace: production
spec:
  predictors:
    - name: default
      replicas: 3
      traffic: 100
      graph:
        name: classifier
        implementation: XGBOOST_SERVER
        modelUri: s3://models/churn/v1.0.0
        parameters:
          - name: method
            type: STRING
            value: predict
        children: []

      componentSpecs:
        - spec:
            containers:
              - name: classifier
                resources:
                  requests:
                    cpu: 500m
                    memory: 1Gi
                  limits:
                    cpu: 2000m
                    memory: 4Gi

      svcOrchSpec:
        env:
          - name: SELDON_LOG_LEVEL
            value: INFO

---
# A/B Testing deployment
apiVersion: machinelearning.seldon.io/v1
kind: SeldonDeployment
metadata:
  name: churn-predictor-ab
spec:
  predictors:
    - name: model-a
      replicas: 2
      traffic: 90
      graph:
        name: classifier
        implementation: XGBOOST_SERVER
        modelUri: s3://models/churn/v1.0.0

    - name: model-b
      replicas: 2
      traffic: 10
      graph:
        name: classifier
        implementation: XGBOOST_SERVER
        modelUri: s3://models/churn/v1.1.0-experimental
```

### Custom Model Server

```python
# model_server.py
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import joblib
import numpy as np
import mlflow
from prometheus_client import Counter, Histogram, generate_latest

app = FastAPI(title="Churn Prediction API")

# Metrics
PREDICTION_COUNTER = Counter(
    'model_predictions_total',
    'Total predictions',
    ['model_version', 'prediction_class']
)
PREDICTION_LATENCY = Histogram(
    'model_prediction_latency_seconds',
    'Prediction latency'
)

# Load model
model = None
model_version = None

def load_model():
    global model, model_version
    # Load from MLflow
    model_uri = "models:/churn-model/Production"
    model = mlflow.pyfunc.load_model(model_uri)
    model_version = mlflow.get_model_version("churn-model", "Production").version

@app.on_event("startup")
async def startup_event():
    load_model()

class PredictionRequest(BaseModel):
    customer_id: str
    features: dict

class PredictionResponse(BaseModel):
    customer_id: str
    churn_probability: float
    churn_risk: str
    model_version: str

@app.post("/predict", response_model=PredictionResponse)
async def predict(request: PredictionRequest):
    with PREDICTION_LATENCY.time():
        try:
            # Extract features in correct order
            feature_vector = np.array([
                request.features['total_spend_30d'],
                request.features['transaction_count_30d'],
                request.features['avg_transaction_amount'],
                # ... more features
            ]).reshape(1, -1)

            # Predict
            probability = model.predict_proba(feature_vector)[0][1]

            # Classify risk
            if probability > 0.7:
                risk = "high"
            elif probability > 0.4:
                risk = "medium"
            else:
                risk = "low"

            # Record metrics
            PREDICTION_COUNTER.labels(
                model_version=model_version,
                prediction_class=risk
            ).inc()

            return PredictionResponse(
                customer_id=request.customer_id,
                churn_probability=float(probability),
                churn_risk=risk,
                model_version=model_version
            )

        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

@app.get("/health")
async def health():
    return {"status": "healthy", "model_version": model_version}

@app.get("/metrics")
async def metrics():
    return generate_latest()
```

## Model Monitoring

### Data Drift Detection

```python
# drift_detection.py
import pandas as pd
from evidently import ColumnMapping
from evidently.report import Report
from evidently.metric_preset import DataDriftPreset, TargetDriftPreset
from evidently.metrics import *
import json

class DriftDetector:
    """Detect data and concept drift in production."""

    def __init__(self, reference_data: pd.DataFrame):
        self.reference = reference_data
        self.column_mapping = ColumnMapping(
            target='target',
            prediction='prediction',
            numerical_features=['total_spend_30d', 'transaction_count_30d'],
            categorical_features=['account_type']
        )

    def detect_data_drift(self, current_data: pd.DataFrame) -> dict:
        """Detect drift between reference and current data."""

        report = Report(metrics=[
            DataDriftPreset(),
        ])

        report.run(
            reference_data=self.reference,
            current_data=current_data,
            column_mapping=self.column_mapping
        )

        result = report.as_dict()

        drift_summary = {
            'dataset_drift': result['metrics'][0]['result']['dataset_drift'],
            'drift_share': result['metrics'][0]['result']['share_of_drifted_columns'],
            'drifted_columns': [
                col['column_name']
                for col in result['metrics'][0]['result']['drift_by_columns'].values()
                if col['drift_detected']
            ]
        }

        return drift_summary

    def detect_performance_drift(
        self,
        current_data: pd.DataFrame,
        threshold: float = 0.05
    ) -> dict:
        """Detect model performance degradation."""

        from sklearn.metrics import accuracy_score, f1_score

        ref_acc = accuracy_score(
            self.reference['target'],
            self.reference['prediction']
        )
        curr_acc = accuracy_score(
            current_data['target'],
            current_data['prediction']
        )

        ref_f1 = f1_score(
            self.reference['target'],
            self.reference['prediction']
        )
        curr_f1 = f1_score(
            current_data['target'],
            current_data['prediction']
        )

        acc_drift = (ref_acc - curr_acc) / ref_acc
        f1_drift = (ref_f1 - curr_f1) / ref_f1

        return {
            'reference_accuracy': ref_acc,
            'current_accuracy': curr_acc,
            'accuracy_drift_pct': acc_drift * 100,
            'reference_f1': ref_f1,
            'current_f1': curr_f1,
            'f1_drift_pct': f1_drift * 100,
            'performance_degraded': acc_drift > threshold or f1_drift > threshold
        }

    def generate_report(self, current_data: pd.DataFrame, output_path: str):
        """Generate full drift report."""

        report = Report(metrics=[
            DataDriftPreset(),
            TargetDriftPreset(),
            DatasetDriftMetric(),
            DatasetMissingValuesMetric(),
        ])

        report.run(
            reference_data=self.reference,
            current_data=current_data,
            column_mapping=self.column_mapping
        )

        report.save_html(output_path)

# Scheduled drift check
import schedule
import time

def scheduled_drift_check():
    """Run drift detection hourly."""
    # Load recent production data
    current_data = load_production_data(last_hours=1)

    detector = DriftDetector(reference_data=load_reference_data())

    drift_result = detector.detect_data_drift(current_data)

    if drift_result['dataset_drift']:
        send_alert(
            f"Data drift detected! "
            f"Drifted columns: {drift_result['drifted_columns']}"
        )

schedule.every().hour.do(scheduled_drift_check)
```

### Model Performance Dashboard

```yaml
# grafana-dashboard.json (simplified)
{
  "dashboard": {
    "title": "ML Model Performance",
    "panels": [
      {
        "title": "Prediction Volume",
        "targets": [{
          "expr": "sum(rate(model_predictions_total[5m]))",
          "legendFormat": "predictions/sec"
        }],
        "type": "graph"
      },
      {
        "title": "Prediction Latency",
        "targets": [{
          "expr": "histogram_quantile(0.99, sum(rate(model_prediction_latency_seconds_bucket[5m])) by (le))",
          "legendFormat": "p99 latency"
        }],
        "type": "graph"
      },
      {
        "title": "Prediction Distribution",
        "targets": [{
          "expr": "sum(rate(model_predictions_total[5m])) by (prediction_class)",
          "legendFormat": "{{prediction_class}}"
        }],
        "type": "piechart"
      },
      {
        "title": "Data Drift Score",
        "targets": [{
          "expr": "data_drift_score",
          "legendFormat": "drift score"
        }],
        "alert": {
          "conditions": [{
            "query": {"queryType": "", "refId": "A"},
            "reducer": {"type": "last"},
            "evaluator": {"params": [0.5], "type": "gt"}
          }],
          "name": "Data Drift Alert"
        }
      }
    ]
  }
}
```

## Model Registry

```python
# model_registry.py
import mlflow
from mlflow.tracking import MlflowClient

class ModelRegistry:
    """Manage model lifecycle in MLflow."""

    def __init__(self, tracking_uri: str):
        mlflow.set_tracking_uri(tracking_uri)
        self.client = MlflowClient()

    def register_model(
        self,
        run_id: str,
        model_name: str,
        tags: dict = None
    ) -> str:
        """Register model from run."""
        model_version = mlflow.register_model(
            model_uri=f"runs:/{run_id}/model",
            name=model_name,
            tags=tags
        )
        return model_version.version

    def transition_stage(
        self,
        model_name: str,
        version: str,
        stage: str,
        comment: str = None
    ):
        """Move model to new stage (Staging, Production, Archived)."""
        self.client.transition_model_version_stage(
            name=model_name,
            version=version,
            stage=stage,
            archive_existing_versions=(stage == "Production")
        )

        if comment:
            self.client.update_model_version(
                name=model_name,
                version=version,
                description=comment
            )

    def compare_versions(self, model_name: str, v1: str, v2: str) -> dict:
        """Compare two model versions."""
        mv1 = self.client.get_model_version(model_name, v1)
        mv2 = self.client.get_model_version(model_name, v2)

        run1 = self.client.get_run(mv1.run_id)
        run2 = self.client.get_run(mv2.run_id)

        return {
            'version_1': {
                'metrics': run1.data.metrics,
                'params': run1.data.params
            },
            'version_2': {
                'metrics': run2.data.metrics,
                'params': run2.data.params
            }
        }

    def get_production_model(self, model_name: str):
        """Get current production model."""
        versions = self.client.get_latest_versions(
            model_name,
            stages=["Production"]
        )
        return versions[0] if versions else None

    def rollback(self, model_name: str):
        """Rollback to previous production version."""
        versions = self.client.search_model_versions(
            f"name='{model_name}'"
        )

        prod_versions = [v for v in versions if v.current_stage == "Production"]

        if len(prod_versions) >= 2:
            # Archive current
            current = prod_versions[0]
            self.transition_stage(
                model_name,
                current.version,
                "Archived",
                "Rolling back"
            )

            # Restore previous
            previous = prod_versions[1]
            self.transition_stage(
                model_name,
                previous.version,
                "Production",
                "Restored after rollback"
            )
```

## GPU Resource Management

```yaml
# gpu-node-pool.yaml
apiVersion: karpenter.sh/v1alpha5
kind: Provisioner
metadata:
  name: gpu-provisioner
spec:
  requirements:
    - key: karpenter.k8s.aws/instance-category
      operator: In
      values: ["p", "g"]  # P-series and G-series for GPU
    - key: karpenter.k8s.aws/instance-size
      operator: In
      values: ["2xlarge", "4xlarge", "8xlarge"]
    - key: nvidia.com/gpu
      operator: Exists

  taints:
    - key: nvidia.com/gpu
      value: "true"
      effect: NoSchedule

  limits:
    resources:
      nvidia.com/gpu: 100

  ttlSecondsAfterEmpty: 300

---
# Training job with GPU
apiVersion: kubeflow.org/v1
kind: PyTorchJob
metadata:
  name: distributed-training
  namespace: ml-workloads
spec:
  pytorchReplicaSpecs:
    Master:
      replicas: 1
      template:
        spec:
          containers:
            - name: pytorch
              image: training-image:latest
              resources:
                limits:
                  nvidia.com/gpu: 4
                requests:
                  nvidia.com/gpu: 4
                  memory: 64Gi
                  cpu: 16
          nodeSelector:
            accelerator: nvidia-tesla-v100
          tolerations:
            - key: nvidia.com/gpu
              operator: Exists
              effect: NoSchedule
    Worker:
      replicas: 3
      template:
        spec:
          containers:
            - name: pytorch
              image: training-image:latest
              resources:
                limits:
                  nvidia.com/gpu: 4
          nodeSelector:
            accelerator: nvidia-tesla-v100
          tolerations:
            - key: nvidia.com/gpu
              operator: Exists
              effect: NoSchedule
```
