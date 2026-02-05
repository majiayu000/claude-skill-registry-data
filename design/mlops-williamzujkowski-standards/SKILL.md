---
name: mlops
category: ml-ai
difficulty: advanced
estimated_time: 60 minutes
prerequisites:
- machine-learning
- docker-containers
- kubernetes-basics
learning_outcomes:
- Design end-to-end ML pipelines from training to production
- Implement model versioning, experiment tracking, and monitoring
- Deploy ML models with batch, real-time, and streaming strategies
- Detect and respond to model drift in production
- Build reproducible ML workflows with MLOps toolchains
related_skills:
- data-engineering
- ci-cd-pipelines
- observability
tags:
- mlops
- machine-learning
- model-deployment
- ml-pipelines
- model-monitoring
- mlflow
- kubeflow
version: 1.0.0
last_updated: 2025-01-17
description: MLOps engineering covering ML pipeline design, model versioning, experiment tracking, deployment strategies, drift detection, and monitoring for production ML systems with tools like MLflow, Kubeflow, and model registries
---


# MLOps (Machine Learning Operations)

## Overview

MLOps brings DevOps principles to machine learning workflows, enabling reliable, scalable, and reproducible ML systems in production. It covers the entire ML lifecycle from experimentation to deployment and monitoring.

**Core Principles:**

- **Reproducibility**: Version everything (code, data, models, environments)
- **Automation**: Automate training, testing, deployment pipelines
- - **Monitoring**: Track model performance, data drift, system health
- **Collaboration**: Bridge data scientists, engineers, and operations
- **Governance**: Ensure model compliance, explainability, and auditing

---

## Level 1: Quick Reference

### ML Lifecycle Stages

```
┌─────────────┐     ┌─────────────┐     ┌─────────────┐     ┌─────────────┐
│   Data      │────▶│  Training   │────▶│ Deployment  │────▶│ Monitoring  │
│ Collection  │     │ & Experiment│     │  & Serving  │     │ & Retraining│
└─────────────┘     └─────────────┘     └─────────────┘     └─────────────┘
      │                    │                    │                    │
      │                    │                    │                    │
      ▼                    ▼                    ▼                    ▼
  Versioning        Tracking             Inference          Drift Detection
  Validation        Reproducibility      Scalability        Performance Decay
  Feature Eng.      Hyperparameters      A/B Testing        Alerts & Triggers
```

### MLOps vs Traditional DevOps

| Aspect | Traditional DevOps | MLOps |
|--------|-------------------|-------|
| **Artifacts** | Code, binaries | Code + Data + Models + Features |
| **Testing** | Unit, integration tests | Data validation + Model evaluation + Inference tests |
| **Deployment** | Deploy once, stable | Continuous retraining, model decay |
| **Monitoring** | Logs, metrics, traces | + Data drift, concept drift, model performance |
| **Versioning** | Git for code | Git + DVC for data + Model registry |
| **Reproducibility** | Dockerfile, env vars | + Data versions, random seeds, feature pipelines |

### Essential MLOps Checklist

**Experimentation & Development:**

- [ ] Experiment tracking (MLflow, Weights & Biases, Neptune.ai)
- [ ] Notebook versioning and parameterization (Papermill)
- [ ] Feature engineering pipelines with versioning
- [ ] Data quality checks (Great Expectations)
- [ ] Model versioning and registry

**Training Pipelines:**

- [ ] Automated data validation before training
- [ ] Reproducible training environments (Docker, Conda)
- [ ] Hyperparameter tuning (Optuna, Ray Tune)
- [ ] Distributed training support (Horovod, PyTorch DDP)
- [ ] Model evaluation metrics logged and tracked

**Deployment & Serving:**

- [ ] Model serving infrastructure (TorchServe, TensorFlow Serving, Seldon)
- [ ] Batch prediction pipelines for offline inference
- [ ] Real-time inference APIs with latency SLAs
- [ ] Canary deployments and A/B testing
- [ ] Shadow mode for model validation

**Monitoring & Maintenance:**

- [ ] Data drift detection (statistical tests, KL divergence)
- [ ] Concept drift detection (model performance degradation)
- [ ] Prediction monitoring and alerting
- [ ] Model performance dashboards
- [ ] Automated retraining triggers
- [ ] Model rollback procedures

### Quick Commands

```bash
# MLflow - Track experiments
mlflow ui --host 0.0.0.0 --port 5000
mlflow run . -P alpha=0.5

# Kubeflow - Deploy pipeline
kfp pipeline create --pipeline-name my_pipeline pipeline.yaml
kfp run submit --experiment-name exp1 --pipeline-id <id>

# DVC - Version data
dvc add data/train.csv
dvc push
dvc pull

# Model serving - TorchServe
torch-model-archiver --model-name my_model --version 1.0 --serialized-file model.pt
torchserve --start --model-store ./model_store
curl -X POST http://localhost:8080/predictions/my_model -T input.json

# Feature store - Feast
feast apply
feast materialize-incremental $(date -u +"%Y-%m-%dT%H:%M:%S")
```

### Common Patterns

**1. Experiment Tracking**

```python
import mlflow

with mlflow.start_run():
    mlflow.log_param("learning_rate", 0.01)
    mlflow.log_metric("accuracy", 0.95)
    mlflow.sklearn.log_model(model, "model")
```

**2. Model Versioning**

```python
from mlflow.tracking import MlflowClient

client = MlflowClient()
result = client.create_model_version(
    name="my_model",
    source="runs:/abc123/model",
    run_id="abc123"
)
```

**3. Model Serving**

```python
# Load model from registry
model = mlflow.pyfunc.load_model(f"models:/my_model/production")

# Inference
predictions = model.predict(input_data)
```

**4. Drift Detection**

```python
from scipy.stats import ks_2samp

# Compare training and production distributions
statistic, p_value = ks_2samp(train_distribution, production_distribution)
if p_value < 0.05:
    trigger_alert("Data drift detected")
```

---

## Level 2:
>
> **📚 Full Examples**: See [REFERENCE.md](./REFERENCE.md) for complete code samples, detailed configurations, and production-ready implementations.

 Implementation Guide

### 1. ML Model Lifecycle Management

#### Training Phase

**Reproducible Training Environment:**


*See [REFERENCE.md](./REFERENCE.md#example-0) for complete implementation.*


**Hyperparameter Optimization:**


*See [REFERENCE.md](./REFERENCE.md#example-1) for complete implementation.*


#### Model Versioning

**Model Registry Pattern:**


*See [REFERENCE.md](./REFERENCE.md#example-2) for complete implementation.*


### 2. Feature Engineering & Feature Stores

**Feature Store with Feast:**


*See [REFERENCE.md](./REFERENCE.md#example-3) for complete implementation.*


**Feature Retrieval in Training:**


*See [REFERENCE.md](./REFERENCE.md#example-4) for complete implementation.*


### 3. Model Serving Strategies

#### Batch Prediction Pipeline

**Apache Airflow DAG:**


*See [REFERENCE.md](./REFERENCE.md#example-5) for complete implementation.*


#### Real-Time Inference API

**FastAPI Model Serving:**


*See [REFERENCE.md](./REFERENCE.md#example-6) for complete implementation.*


#### Streaming Inference

**Kafka Consumer with Model:**


*See [REFERENCE.md](./REFERENCE.md#example-7) for complete implementation.*


### 4. Model Monitoring & Drift Detection

#### Data Drift Detection

**Statistical Testing Approach:**


*See [REFERENCE.md](./REFERENCE.md#example-8) for complete implementation.*


#### Concept Drift Detection

**Performance-Based Monitoring:**


*See [REFERENCE.md](./REFERENCE.md#example-9) for complete implementation.*


#### Production Monitoring Dashboard

**Prometheus Metrics + Grafana:**


*See [REFERENCE.md](./REFERENCE.md#example-10) for complete implementation.*


### 5. ML Pipelines & Orchestration

#### Kubeflow Pipelines

**Pipeline Definition:**


*See [REFERENCE.md](./REFERENCE.md#example-11) for complete implementation.*


### 6. A/B Testing & Canary Deployments

**Multi-Armed Bandit for Model Selection:**


*See [REFERENCE.md](./REFERENCE.md#example-12) for complete implementation.*


### 7. Production Best Practices

#### Model Governance

**Model Card Documentation:**


*See [REFERENCE.md](./REFERENCE.md#example-13) for complete implementation.*


#### CI/CD for ML

**GitHub Actions Workflow:**


*See [REFERENCE.md](./REFERENCE.md#example-14) for complete implementation.*


---

## Level 3: Deep Dive Resources

### Advanced Topics

1. **Distributed Training**
   - Horovod for data parallelism
   - PyTorch DistributedDataParallel
   - Model parallelism with Megatron-LM
   - Gradient compression techniques

2. **Advanced Monitoring**
   - Explainable AI monitoring (SHAP, LIME)
   - Adversarial robustness testing
   - Model interpretability dashboards
   - Automated root cause analysis

3. **AutoML & Meta-Learning**
   - AutoML platforms (H2O AutoML, Auto-sklearn)
   - Neural architecture search (NAS)
   - Transfer learning pipelines
   - Few-shot learning for rapid adaptation

4. **Edge ML & Model Optimization**
   - Model quantization (INT8, mixed precision)
   - Knowledge distillation
   - Pruning and compression
   - ONNX for cross-platform deployment

### Official Documentation

- **MLflow**: https://mlflow.org/docs/latest/index.html
- **Kubeflow**: https://www.kubeflow.org/docs/
- **Feast Feature Store**: https://docs.feast.dev/
- **DVC (Data Version Control)**: https://dvc.org/doc
- **Great Expectations**: https://docs.greatexpectations.io/
- **TorchServe**: https://pytorch.org/serve/
- **TensorFlow Serving**: https://www.tensorflow.org/tfx/guide/serving
- **Seldon Core**: https://docs.seldon.io/projects/seldon-core/en/latest/

### Books

- "Machine Learning Design Patterns" by Lakshmanan, Robinson, Munn
- "Building Machine Learning Powered Applications" by Emmanuel Ameisen
- "Designing Machine Learning Systems" by Chip Huyen
- "Machine Learning Engineering" by Andriy Burkov

### Courses

- Google Cloud Professional ML Engineer Certification
- AWS Certified Machine Learning – Specialty
- Coursera: MLOps Specialization (DeepLearning.AI)
- Full Stack Deep Learning (Berkeley)

### Tools & Platforms

- **Experiment Tracking**: MLflow, Weights & Biases, Neptune.ai, Comet.ml
- **Pipeline Orchestration**: Kubeflow, Apache Airflow, Metaflow, Prefect
- **Feature Stores**: Feast, Tecton, Hopsworks
- **Model Serving**: TorchServe, TensorFlow Serving, Seldon Core, KServe
- **Monitoring**: Evidently AI, WhyLabs, Arize AI, Fiddler
- **Data Versioning**: DVC, LakeFS, Pachyderm

### Community Resources

- MLOps Community: https://mlops.community/
- Made With ML: https://madewithml.com/
- Papers with Code: https://paperswithcode.com/
- MLOps Subreddit: r/mlops

---

## Practice Exercises

### Exercise 1: End-to-End Pipeline

Build a complete MLOps pipeline:

1. Version dataset with DVC
2. Train model with MLflow tracking
3. Register model in MLflow Model Registry
4. Create Kubeflow pipeline for retraining
5. Deploy with FastAPI + Docker
6. Monitor with Prometheus + Grafana

### Exercise 2: Drift Detection System

Implement comprehensive drift detection:

1. Collect baseline statistics from training data
2. Implement KS test for numerical features
3. Implement Chi-square test for categorical features
4. Create concept drift detector tracking model performance
5. Set up alerts for drift detection
6. Build automated retraining trigger

### Exercise 3: A/B Testing Framework

Build an A/B testing system for models:

1. Deploy two model versions
2. Implement Thompson Sampling for traffic routing
3. Collect feedback and update reward statistics
4. Create dashboard showing model performance comparison
5. Implement automated winner selection
6. Gradual rollout of winning model

### Exercise 4: Feature Store

Set up a production feature store:

1. Define entities and feature views in Feast
2. Materialize historical features for training
3. Set up online feature serving
4. Implement feature freshness monitoring
5. Create feature lineage tracking
6. Build feature validation pipeline

## Examples

### Basic Usage

```python
// TODO: Add basic example for mlops
// This example demonstrates core functionality
```

### Advanced Usage

```python
// TODO: Add advanced example for mlops
// This example shows production-ready patterns
```

### Integration Example

```python
// TODO: Add integration example showing how mlops
// works with other systems and services
```

See `examples/mlops/` for complete working examples.

## Integration Points

This skill integrates with:

### Upstream Dependencies

- **Tools**: Common development tools and frameworks
- **Prerequisites**: Basic understanding of general concepts

### Downstream Consumers

- **Applications**: Production systems requiring mlops functionality
- **CI/CD Pipelines**: Automated testing and deployment workflows
- **Monitoring Systems**: Observability and logging platforms

### Related Skills

- See other skills in this category

### Common Integration Patterns

1. **Development Workflow**: How this skill fits into daily development
2. **Production Deployment**: Integration with production systems
3. **Monitoring & Alerting**: Observability integration points

## Common Pitfalls

### Pitfall 1: Insufficient Testing

**Problem:** Not testing edge cases and error conditions leads to production bugs

**Solution:** Implement comprehensive test coverage including:

- Happy path scenarios
- Error handling and edge cases
- Integration points with external systems

**Prevention:** Enforce minimum code coverage (80%+) in CI/CD pipeline

### Pitfall 2: Hardcoded Configuration

**Problem:** Hardcoding values makes applications inflexible and environment-dependent

**Solution:** Use environment variables and configuration management:

- Separate config from code
- Use environment-specific configuration files
- Never commit secrets to version control

**Prevention:** Use tools like dotenv, config validators, and secret scanners

### Pitfall 3: Ignoring Security Best Practices

**Problem:** Security vulnerabilities from not following established security patterns

**Solution:** Follow security guidelines:

- Input validation and sanitization
- Proper authentication and authorization
- Encrypted data transmission (TLS/SSL)
- Regular security audits and updates

**Prevention:** Use security linters, SAST tools, and regular dependency updates

**Best Practices:**

- Follow established patterns and conventions for mlops
- Keep dependencies up to date and scan for vulnerabilities
- Write comprehensive documentation and inline comments
- Use linting and formatting tools consistently
- Implement proper error handling and logging
- Regular code reviews and pair programming
- Monitor production metrics and set up alerts

---

**Next Steps:** Explore [data-engineering](../data-engineering/SKILL.md) for upstream data pipelines or [observability](../../devops/observability/SKILL.md) for production monitoring integration.
