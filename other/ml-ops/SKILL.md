---
name: ml-ops
description: Model deployment, versioning, monitoring, A/B testing, feature stores, and ML pipeline orchestration
layer: domain
category: ai-ml
triggers:
  - "MLOps"
  - "model deployment"
  - "model monitoring"
  - "model versioning"
  - "A/B testing models"
  - "feature store"
  - "ML pipeline"
  - "model serving"
inputs:
  - model: Model type, framework (PyTorch, TensorFlow, ONNX, LLM)
  - requirements: Latency, throughput, availability, cost targets
  - infrastructure: Cloud provider, Kubernetes, serverless preferences
  - workflow: Training, evaluation, deployment, monitoring needs
outputs:
  - deployment_architecture: Model serving infrastructure design
  - pipeline_config: Training and deployment pipeline configuration
  - monitoring_setup: Model performance and data drift monitoring
  - versioning_strategy: Model and dataset version management
  - ab_testing_plan: Experiment design for model comparison
linksTo:
  - docker
  - kubernetes
  - monitoring
  - cicd
  - logging
linkedFrom:
  - ai-agents
  - rag
  - plan
preferredNextSkills:
  - monitoring
  - docker
fallbackSkills:
  - cicd
riskLevel: medium
memoryReadPolicy: selective
memoryWritePolicy: none
sideEffects:
  - May create deployment configurations
  - May configure monitoring dashboards
  - Model deployments affect production traffic
---

# ML Ops Skill

## Purpose

Design and implement the operational infrastructure for machine learning systems: model versioning, reproducible training pipelines, deployment strategies, A/B testing, monitoring for data drift and model degradation, and feature stores. MLOps bridges the gap between training a model in a notebook and running it reliably in production.

## Key Concepts

### MLOps Lifecycle

```
DATA:
  Collection -> Cleaning -> Feature Engineering -> Feature Store
                                                       |
MODEL:                                                 v
  Experiment -> Train -> Evaluate -> Register -> Deploy -> Monitor
      ^                                                      |
      |                                                      v
      +<--- Retrain <--- Alert (drift/degradation detected) -+
```

### Deployment Patterns

```
BATCH INFERENCE:
  Run predictions on a schedule (hourly, daily)
  Results stored in database/cache
  Good for: Recommendations, risk scoring, email personalization
  Latency: Minutes to hours (acceptable)

REAL-TIME INFERENCE:
  HTTP API endpoint, request-response
  Good for: Search ranking, fraud detection, chatbots
  Latency: <100ms (required)

STREAMING INFERENCE:
  Process events from a message queue
  Good for: Anomaly detection, real-time scoring
  Latency: Seconds (near real-time)

EDGE INFERENCE:
  Model runs on device (browser, mobile, IoT)
  Good for: Image classification, NLP on device
  Latency: <10ms (on-device)

LLM SERVING:
  Managed API (OpenAI, Anthropic) or self-hosted (vLLM, Ollama)
  Good for: Text generation, chat, code generation
  Latency: 1-30 seconds (token streaming)
```

### Model Versioning

```
MODEL REGISTRY:
  model-name/
    v1.0.0/
      model.onnx (or model.pt, model weights)
      config.json (hyperparameters, architecture)
      metrics.json (evaluation results)
      requirements.txt (dependencies)
      README.md (training notes, known limitations)
    v1.1.0/
      ...
    v2.0.0/
      ...

VERSIONING SCHEME:
  MAJOR: Architecture change, different input/output schema
  MINOR: Retrained on new data, improved accuracy
  PATCH: Bug fix, configuration change

METADATA TO TRACK:
  - Training data version (hash or timestamp)
  - Hyperparameters used
  - Evaluation metrics (accuracy, F1, latency)
  - Training duration and cost
  - Git commit of training code
  - Feature set version
```

## Patterns

### Model Serving with FastAPI

```python
# serve.py
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import onnxruntime as ort
import numpy as np

app = FastAPI(title="Model Serving API", version="1.0.0")

# Load model at startup
session = ort.InferenceSession("model.onnx")

class PredictionRequest(BaseModel):
    features: list[float]

class PredictionResponse(BaseModel):
    prediction: float
    confidence: float
    model_version: str

@app.post("/predict", response_model=PredictionResponse)
async def predict(request: PredictionRequest):
    input_array = np.array([request.features], dtype=np.float32)
    outputs = session.run(None, {"input": input_array})

    return PredictionResponse(
        prediction=float(outputs[0][0]),
        confidence=float(outputs[1][0]),
        model_version="1.0.0",
    )

@app.get("/health")
async def health():
    return {"status": "healthy", "model_version": "1.0.0"}
```

### A/B Testing Models

```typescript
// Traffic splitting for model comparison
interface ModelConfig {
  name: string;
  version: string;
  endpoint: string;
  trafficWeight: number;  // 0-100
}

const modelConfigs: ModelConfig[] = [
  { name: 'baseline', version: 'v1.0.0', endpoint: '/models/v1/predict', trafficWeight: 80 },
  { name: 'challenger', version: 'v2.0.0', endpoint: '/models/v2/predict', trafficWeight: 20 },
];

async function routeRequest(request: PredictionRequest, userId: string) {
  // Consistent routing: same user always goes to same model
  const hash = hashString(`${userId}:experiment-2026-03`);
  const bucket = hash % 100;

  let cumulative = 0;
  for (const config of modelConfigs) {
    cumulative += config.trafficWeight;
    if (bucket < cumulative) {
      const result = await callModel(config.endpoint, request);

      // Log for analysis
      await logExperiment({
        userId,
        model: config.name,
        version: config.version,
        input: request,
        output: result,
        timestamp: new Date(),
      });

      return { ...result, model: config.name };
    }
  }
}
```

### Monitoring for Data Drift

```python
# monitor.py
import numpy as np
from scipy.stats import ks_2samp

class DriftDetector:
    def __init__(self, reference_data: np.ndarray, threshold: float = 0.05):
        self.reference = reference_data
        self.threshold = threshold

    def check_drift(self, current_data: np.ndarray) -> dict:
        results = {}
        for i in range(current_data.shape[1]):
            stat, p_value = ks_2samp(
                self.reference[:, i],
                current_data[:, i],
            )
            results[f"feature_{i}"] = {
                "statistic": float(stat),
                "p_value": float(p_value),
                "drift_detected": p_value < self.threshold,
            }

        drift_count = sum(1 for r in results.values() if r["drift_detected"])
        return {
            "features": results,
            "drift_count": drift_count,
            "total_features": current_data.shape[1],
            "alert": drift_count > current_data.shape[1] * 0.3,
        }

# Run daily
# detector = DriftDetector(training_data)
# report = detector.check_drift(last_24h_data)
# if report["alert"]:
#     send_alert("Data drift detected", report)
```

### CI/CD Pipeline for Models

```yaml
# .github/workflows/ml-pipeline.yml
name: ML Pipeline
on:
  push:
    paths: ['models/**', 'training/**']

jobs:
  train:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Train model
        run: python training/train.py --config training/config.yaml
      - name: Evaluate model
        run: python training/evaluate.py
      - name: Check quality gate
        run: |
          python -c "
          import json
          metrics = json.load(open('metrics.json'))
          assert metrics['accuracy'] >= 0.95, f'Accuracy {metrics[\"accuracy\"]} below threshold'
          assert metrics['latency_p99_ms'] <= 100, f'Latency {metrics[\"latency_p99_ms\"]}ms above threshold'
          "
      - name: Register model
        if: success()
        run: python training/register.py --version ${{ github.sha }}
      - name: Deploy canary
        if: success()
        run: python deploy/canary.py --version ${{ github.sha }} --traffic 10
```

## Best Practices

1. **Version everything** -- model weights, training data, code, configuration, features
2. **Automate training pipelines** -- manual training does not scale and is not reproducible
3. **Quality gates before deployment** -- model must pass accuracy, latency, and fairness checks
4. **Canary deployments** -- route 5-10% of traffic to new model before full rollout
5. **Monitor for drift** -- data distribution changes cause silent model degradation
6. **Log predictions** -- store input features, predictions, and ground truth for evaluation
7. **Feature stores for consistency** -- same features in training and serving prevents skew
8. **Set SLAs for inference** -- latency p99, throughput, availability targets
9. **Rollback capability** -- one-click rollback to previous model version
10. **Cost tracking** -- GPU hours, API calls, storage are real costs

## Common Pitfalls

| Pitfall | Impact | Fix |
|---------|--------|-----|
| Training-serving skew | Model performs differently in prod | Use feature store, same preprocessing |
| No drift monitoring | Silent degradation over time | Automated drift detection with alerts |
| Manual deployments | Slow, error-prone, not reproducible | CI/CD pipeline with quality gates |
| No model versioning | Cannot rollback, cannot reproduce | Register every model with metadata |
| Ignoring latency | Timeouts, bad user experience | Profile and optimize, set SLA targets |
| No A/B testing | Ship worse models without knowing | Canary deploy, measure business metrics |
