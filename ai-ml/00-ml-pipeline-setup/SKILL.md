---
name: ml-pipeline-setup
description: MLflow and ML Model patterns for Databricks including experiment creation, model training, batch inference, and Unity Catalog integration. Use when implementing ML pipelines, training models with Feature Store, or deploying batch inference jobs. Includes 19 non-negotiable rules covering experiment paths, dataset logging, UC model registration, NaN handling, label binarization, feature engineering workflows, and signature-driven preprocessing.
clients: [ide_cli, genie_code]
bundle_resource: jobs
deploy_verb: bundle_deploy
deploy_note: "Feature/training/batch-inference jobs deploy via `bundle deploy --target dev` (runDatabricksCli on Genie Code); UC model registration in the per-user prefixed catalog/schema. On Genie Code, write generated training/inference .py under the cloned repo root (`{REPO_ROOT}` = `state_file_root` from `skills/vibecoding-state`, e.g. `src/{project}_ml/...`), not a bare relative path \u2014 relative paths resolve against the page CWD (see `skills/genie-code-environment` \u00a78)."
coverage: full
metadata:
  author: prashanth subrahmanyam
  version: "2.0"
  domain: ml
  role: orchestrator
  pipeline_stage: 8
  pipeline_stage_name: ml
  next_stages:
    - genai-agents-setup
  workers: []
  common_dependencies:
    - databricks-asset-bundles
    - databricks-expert-agent
    - databricks-python-imports
    - naming-tagging-standards
    - databricks-autonomous-operations
  consumes:
    - plans/manifests/ml-manifest.yaml
  consumes_fallback: "Gold table inventory (self-discovery from catalog)"
  last_verified: "2026-06-05"
  volatility: high
  upstream_sources:
    - name: "databricks-agent-skills"
      repo: "databricks/databricks-agent-skills"
      paths:
        - "skills/databricks-model-serving/SKILL.md"
        - "skills/databricks-vector-search/SKILL.md"
      relationship: "extended"
      last_synced: "2026-08-30"
      sync_commit: "ca92a6c"
    - name: "databricks-docs-feature-store"
      url: "https://docs.databricks.com/aws/en/machine-learning/feature-store/"
      relationship: "upstream"
      last_synced: "2026-06-05"
    - name: "databricks-docs-feature-tables-uc"
      url: "https://docs.databricks.com/aws/en/machine-learning/feature-store/uc/feature-tables-uc"
      relationship: "upstream"
      last_synced: "2026-06-05"
    - name: "databricks-docs-feature-store-python-api"
      url: "https://docs.databricks.com/aws/en/machine-learning/feature-store/python-api"
      relationship: "upstream"
      last_synced: "2026-06-05"
---

# MLflow & ML Models Patterns

## Phase 0: Read Plan (5 minutes)

**Before starting implementation, check for a planning manifest that defines what to build.**

```python
import yaml
from pathlib import Path

manifest_path = Path("plans/manifests/ml-manifest.yaml")

if manifest_path.exists():
    with open(manifest_path) as f:
        manifest = yaml.safe_load(f)
    
    # Extract implementation checklist from manifest
    feature_tables = manifest.get('feature_tables', [])
    models = manifest.get('models', [])
    experiments = manifest.get('experiments', [])
    print(f"Plan: {len(feature_tables)} feature tables, {len(models)} models, {len(experiments)} experiments")
    
    # Each model has: name, domain, model_type, algorithm, feature_table,
    #                  label_column, label_type, business_questions
    # Each feature table has: name, primary_keys, source_gold_tables, features
else:
    # Fallback: self-discovery from Gold tables
    print("No manifest found — falling back to Gold table self-discovery")
    # Discover Gold fact tables, infer feature columns, create one model per domain
```

**If manifest exists:** Use it as the implementation checklist. Every feature table, model, and experiment is pre-defined with configuration details. Track completion against the manifest's `summary` counts.

**If manifest doesn't exist:** Fall back to self-discovery — inventory Gold fact tables, infer feature columns from numeric columns, and create one model per domain. This works but may miss specific label derivations and business context the planning phase would have defined.

---

## Quick Start (4-6 hours)

**Goal:** Build production-ready ML pipelines with MLflow 3.1+, Unity Catalog Model Registry, and **Databricks Feature Engineering** for training-serving consistency.

**What You'll Create:**
1. `features/create_feature_tables.py` - Feature tables in Unity Catalog
2. `{domain}/train_{model_name}.py` - Training pipelines with Feature Engineering
3. `inference/batch_inference_all_models.py` - Batch scoring with `fe.score_batch`
4. Asset Bundle jobs for orchestration

**Fast Track:**

> **Client note:** IDE runs these in a terminal; Genie Code runs the `databricks bundle …` commands via `runDatabricksCli` (be on the bundle's page; generated files anchor to `{REPO_ROOT}`). See `skills/genie-code-environment`.

```bash
# 1. Create Feature Tables
databricks bundle run ml_feature_pipeline_job -t dev

# 2. Train all models (parallel)
databricks bundle run ml_training_pipeline_job -t dev

# 3. Run batch inference
databricks bundle run ml_inference_pipeline_job -t dev
```

---

## Overview

Production-grade patterns for implementing ML pipelines on Databricks using MLflow, Unity Catalog, and Feature Store. Based on production experience with 25 models across 5 domains, achieving 96% inference success rate and 93% reduction in debugging time.

**Pattern Origin:** December 2025 (Updated: February 6, 2026 - v5.0)

---

## When to Use This Skill

Use this skill when:
- **Implementing ML pipelines** on Databricks with MLflow tracking
- **Training models** with Feature Store integration
- **Deploying batch inference** jobs
- **Registering models** to Unity Catalog
- **Troubleshooting** MLflow experiment, model registration, or inference errors
- **Setting up** Databricks Asset Bundle jobs for ML workflows
- **Creating feature tables** in Unity Catalog with proper primary keys and NaN handling

**Critical for:**
- Ensuring training and inference consistency via `fe.score_batch`
- Preventing common MLflow signature errors
- Handling data quality issues (NaN, label binarization, single-class data)
- Configuring serverless ML jobs correctly

---

## Working Memory Management

This orchestrator covers Phase 0 (plan reading) plus multiple implementation sections (feature tables, training, inference, deployment). To maintain coherence without context pollution:

**After each major section, persist a brief summary note** capturing:
- **Phase 0 output:** Manifest found (yes/no), model count, feature table count, experiment names from manifest or discovery
- **Feature tables output:** Feature table names and paths, primary key columns, NaN handling decisions
- **Training output:** Experiment names, model URIs, MLflow signature details, label binarization strategy
- **Inference output:** Batch inference notebook paths, `fe.score_batch` config, output table names
- **Jobs output:** Job YAML file paths, environment config, `databricks.yml` sync status

**What to keep in working memory:** Only the current section's reference skill, the model/feature inventory (from Phase 0), and the previous section's summary note. Discard intermediate outputs (full DataFrames, training logs, model artifacts) — they are in MLflow and reproducible.

---

## Architecture Overview

```
┌─────────────────────────────────────────────────────────────────┐
│                          Gold Layer                              │
│   (fact_tables, dim_tables - source for feature engineering)    │
└───────────────────────┬─────────────────────────────────────────┘
                        │
                        ▼
┌─────────────────────────────────────────────────────────────────┐
│              Feature Tables (Unity Catalog)                      │
│  ┌───────────────────┐ ┌──────────────────┐ ┌─────────────────┐ │
│  │ cost_features     │ │ security_features│ │ performance_    │ │
│  │ PK: workspace_id, │ │ PK: user_id,     │ │   features      │ │
│  │     usage_date    │ │     event_date   │ │ PK: warehouse_id│ │
│  └───────────────────┘ └──────────────────┘ │     query_date  │ │
│                                             └─────────────────┘ │
└───────────────────────┬─────────────────────────────────────────┘
                        │
                        ▼
┌─────────────────────────────────────────────────────────────────┐
│                    Training Pipelines                            │
│  ┌─────────────────────────────────────────────────────────────┐│
│  │  FeatureLookup → create_training_set → train → fe.log_model ││
│  │  (Embeds feature metadata for inference consistency)        ││
│  └─────────────────────────────────────────────────────────────┘│
└───────────────────────┬─────────────────────────────────────────┘
                        │
                        ▼
┌─────────────────────────────────────────────────────────────────┐
│             Unity Catalog Model Registry (MLflow 3.1+)           │
│         catalog.{feature_schema}.{model_name}                    │
│         (Model + Feature Lookup Metadata embedded)               │
└───────────────────────┬─────────────────────────────────────────┘
                        │
                        ▼
┌─────────────────────────────────────────────────────────────────┐
│                      Inference Layer                             │
│  ┌──────────────────────────────────────────────────────────┐   │
│  │  fe.score_batch(model_uri, df_with_lookup_keys_only)     │   │
│  │  → Automatically retrieves features from Feature Tables  │   │
│  │  → Guarantees training-serving consistency               │   │
│  └──────────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────┘
```

---

## Directory Structure

```
src/{project}_ml/
├── features/
│   └── create_feature_tables.py     # Feature table creation
├── cost/
│   ├── train_budget_forecaster.py
│   ├── train_cost_anomaly_detector.py
│   └── train_chargeback_attribution.py
├── security/
│   └── train_security_threat_detector.py
├── performance/
│   └── train_query_performance_forecaster.py
├── reliability/
│   └── train_job_failure_predictor.py
├── quality/
│   └── train_data_drift_detector.py
├── inference/
│   └── batch_inference_all_models.py  # Uses fe.score_batch
└── README.md

resources/ml/
├── ml_feature_pipeline_job.yml       # Feature table creation
├── ml_training_pipeline_job.yml      # Training orchestrator
└── ml_inference_pipeline_job.yml     # Batch inference
```

---

## Critical Rules (Quick Reference)

| # | Rule | Pattern | Why It Fails Otherwise |
|---|------|---------|----------------------|
| 0 | **Pin Package Versions Consistently** | Pin the **same** mlflow / sklearn / xgboost versions in training AND inference (exact pins); the `mlflow==3.7.0` value in this skill's templates is a repo-template baseline, not an official Databricks requirement — match the version you actually train with | Version mismatch warnings, deserialization failures, autologging behavior drift |
| 1 | **Experiment Path** | `/Shared/{project}_ml_{model_name}` | `/Users/...` fails silently if subfolder doesn't exist |
| 2 | **Dataset Logging** | Inside `mlflow.start_run()` context | Won't associate with run, invisible in UI |
| 3 | **Exit Signal** | `dbutils.notebook.exit("SUCCESS")` | Job status unclear, may show SUCCESS on failure |
| 4 | **UC Model Logging** | Prefer `fe.log_model()` with `infer_input_example=True`; supply `output_schema` only when the `training_set` has no label column (or the model returns a non-default output shape) — current Feature Engineering docs treat `output_schema` as a fallback, not a universal UC requirement | Unity Catalog model fails to register or returns the wrong output spec at inference |
| 5 | **Feature Engineering Workflow** | `FeatureLookup` + `create_training_set` + `fe.log_model` | Feature skew between training and inference |
| 6 | **NaN Handling at Source** | Clean NaN/Inf at **feature table creation** with `clean_numeric()` | sklearn GradientBoosting fails at inference; XGBoost handles NaN but sklearn doesn't |
| 7 | **Label Binarization** | Convert 0-1 rates to binary for classifiers | `XGBoostError: base_score must be in (0,1)` |
| 8 | **Single-Class Check** | Verify label distribution before training | Classifier can't train on all-same labels |
| 9 | **Exclude Labels** | Use `exclude_columns=[LABEL_COLUMN]` in `create_training_set` | Label included as feature causes inference failure |
| 10 | **Label Type Casting** | Cast to INT (classification) or DOUBLE (regression) before training | Type mismatch in model output |
| 11 | **Double Type Casting** | Cast ALL numeric features to DOUBLE in feature tables | MLflow signatures reject DecimalType |
| 12 | **Lookup Keys Match PKs** | `lookup_key` MUST match Feature Table primary keys EXACTLY | `Unable to find feature` errors |
| 13 | **Use fe.score_batch** | Use `fe.score_batch` NOT manual feature joins for inference | Automatic feature retrieval ensures training-serving consistency |
| 14 | **Feature Registry** | Query feature table schemas dynamically | Hardcoded feature lists drift out of sync |
| 15 | **Custom Inference** | Separate task for TF-IDF/NLP models that need runtime features | `fe.score_batch()` can't compute runtime features |
| 16 | **Helper Functions Inline** | ALWAYS inline helper functions (don't import modules) | `ModuleNotFoundError` in serverless Asset Bundle notebooks |
| 17 | **Bundle Path Setup** | Use `sys.path.insert(0, _bundle_root)` pattern | Module imports fail in serverless |
| 18 | **Standardized Templates** | Copy-and-customize from skill templates (don't roll custom) | Custom implementations miss edge cases |

---

## Core Patterns (Quick Examples)

### Experiment Setup

```python
# ✅ CORRECT: Always use /Shared/ path
experiment_name = f"/Shared/{project}_ml_{model_name}"
mlflow.set_experiment(experiment_name)
```

**See:** [Experiment Patterns](references/experiment-patterns.md) for full details

### Model Registration with Feature Store

```python
from databricks.feature_engineering import FeatureEngineeringClient
from mlflow.types import ColSpec, DataType, Schema

fe = FeatureEngineeringClient()
mlflow.set_registry_uri("databricks-uc")

# Regression: output_schema = Schema([ColSpec(DataType.double)])
# Classification: output_schema = Schema([ColSpec(DataType.long)])

fe.log_model(
    model=model,
    artifact_path="model",
    flavor=mlflow.sklearn,  # required
    training_set=training_set,
    registered_model_name=f"{catalog}.{schema}.{model_name}",
    infer_input_example=True,  # preferred per current Feature Engineering docs
    output_schema=output_schema,  # required only when training_set has no label, or to override inferred shape
)
```

**See:** [Model Registry](references/model-registry.md) for full patterns by model type

### Feature Table Creation with NaN Cleaning

```python
# ✅ CORRECT: Clean NaN/Inf at source for sklearn compatibility
from pyspark.sql.functions import F, isnan
from pyspark.sql.types import DoubleType

def clean_numeric(col_name):
    return F.when(
        F.col(col_name).isNull() | isnan(F.col(col_name)) |
        (F.col(col_name) == float('inf')) | (F.col(col_name) == float('-inf')),
        F.lit(0.0)
    ).otherwise(F.col(col_name))

# Apply to ALL DoubleType columns
for field in df.schema.fields:
    if isinstance(field.dataType, DoubleType):
        df = df.withColumn(field.name, clean_numeric(field.name))
```

**See:** [Data Quality Patterns](references/data-quality-patterns.md) for full patterns

### Batch Inference with fe.score_batch

```python
from databricks.feature_engineering import FeatureEngineeringClient

fe = FeatureEngineeringClient()

# ✅ CORRECT: scoring_df has ONLY lookup keys (features auto-retrieved)
scoring_df = spark.table(feature_table).select(*lookup_keys).distinct()

predictions_df = fe.score_batch(
    model_uri=model_uri,
    df=scoring_df  # Contains only lookup keys
)
```

**See:** [Feature Engineering Workflow](references/feature-engineering-workflow.md) for full inference patterns

### Asset Bundle Job Configuration

```yaml
resources:
  jobs:
    ml_training_job:
      environments:
        - environment_key: default
          spec:
            environment_version: "4"
            dependencies:
              - "mlflow==3.7.0"  # Pin exact version
              - "xgboost==2.0.3"
      tasks:
        - task_key: train_model
          notebook_task:
            notebook_path: ../../src/ml/models/train.py
            base_parameters:  # NOT parameters with --flags!
              catalog: ${var.catalog}
              model_name: my_model
      # ❌ DO NOT define experiments in Asset Bundle
```

**See:** [DAB Integration](references/dab-integration.md) for full patterns

---

## Reference Files

Detailed documentation is organized in the `references/` directory:

### **[Experiment Patterns](references/experiment-patterns.md)**
Complete experiment setup, tracking, metric logging, dataset logging, hyperparameter tuning. Covers `/Shared/` vs `/Users/` paths, run context requirements, helper function inlining, exit signals, and common errors.

### **[Model Registry](references/model-registry.md)**
Model registration, versioning, aliases, deployment patterns, serving endpoints. Covers Unity Catalog integration with `fe.log_model()`, output schema patterns by model type (regression, classification, anomaly detection), signature-driven preprocessing, and model loading from UC. Documents both `output_schema` (primary) and `infer_signature` (alternative) approaches.

### **[DAB Integration](references/dab-integration.md)**
Asset Bundle integration, notebook patterns, inline helpers, parameter passing. Covers training and inference job configuration, package version pinning, `base_parameters` vs argparse, serverless environment setup, and common deployment errors.

### **[Feature Store Patterns](references/feature-store-patterns.md)**
Feature table creation, feature lookup configuration, column conflict resolution, Feature Registry pattern for dynamic schema querying. Covers training set creation, feature lookups, and inference patterns.

### **[Data Quality Patterns](references/data-quality-patterns.md)**
NaN/Inf handling at feature table source, label binarization for XGBoost classifiers, single-class data detection, feature column exclusion. Covers sklearn vs XGBoost compatibility, preprocessing requirements, and training/inference checklists.

### **[Troubleshooting](references/troubleshooting.md)**
Comprehensive error reference table, schema verification patterns, SCD2 vs regular dimension table handling, pre-development checklist. Covers common MLflow errors, signature issues, and debugging workflows.

### **[Requirements Template](references/requirements-template.md)**
Fill-in-the-blank requirements template for ML projects. Includes project context (catalog, schemas), feature table inventory (primary keys, features, source tables), model inventory (type, algorithm, label column, label type), and label type reference (regression vs classification vs anomaly detection casting).

### **[Feature Engineering Workflow](references/feature-engineering-workflow.md)**
End-to-end Feature Engineering workflow with `FeatureLookup`, `create_training_set`, `fe.log_model`, and `fe.score_batch`. Covers feature table creation with NaN cleaning, training set creation with proper `base_df` (ONLY keys + label), model logging with embedded feature metadata, and batch inference with automatic feature retrieval.

---

## Scripts

### **[setup_experiment.py](scripts/setup_experiment.py)**

Utility functions for MLflow experiment setup. **CRITICAL:** These functions should be INLINED in each training notebook, not imported.

**Functions:**
- `setup_mlflow_experiment(model_name)` - Set up experiment with `/Shared/` path
- `log_training_dataset(spark, catalog, schema, table_name)` - Log dataset inside run context
- `get_run_name(model_name, algorithm, version)` - Generate descriptive run names
- `get_standard_tags(...)` - Get standard MLflow tags
- `get_parameters()` - Get job parameters from dbutils widgets (returns 4: catalog, gold_schema, feature_schema, model_name)

**Usage:**
```python
# Copy these functions into your notebook (don't import)
# See scripts/setup_experiment.py for full implementation
```

### **[create_feature_tables_template.py](scripts/create_feature_tables_template.py)**

Complete feature table creation template with NaN/Inf cleaning at source, DOUBLE type casting, PK NULL filtering, rolling window aggregations, and proper `fe.create_table()` calls. Uses 3-parameter `get_parameters()` (catalog, gold_schema, feature_schema).

**Key functions:**
- `get_parameters()` - Returns (catalog, gold_schema, feature_schema) — no model_name needed
- `create_feature_table(spark, fe, features_df, ...)` - Create with NaN cleaning + PK filtering
- `compute_{domain}_features(spark, catalog, gold_schema)` - Domain-specific feature engineering
- `main()` - Orchestrates schema creation and all feature tables

### **[train_model_template.py](scripts/train_model_template.py)**

Complete training pipeline template using Feature Engineering with `FeatureLookup`, `create_training_set`, and `fe.log_model` with `output_schema`. Includes inline helpers, label type casting, label binarization, single-class detection, and proper exit signals.

**Key functions:**
- `setup_mlflow_experiment(model_name)` - Inlined `/Shared/` path setup
- `get_parameters()` - Returns (catalog, gold_schema, feature_schema, model_name)
- `create_training_set_with_features(...)` - FeatureLookup + create_training_set
- `prepare_and_train(training_df, ...)` - Data prep with DECIMAL→DOUBLE + train/eval
- `log_model_with_feature_engineering(...)` - `fe.log_model()` with `output_schema`
- `main()` - Full pipeline with error handling + exit signal

### **[batch_inference_template.py](scripts/batch_inference_template.py)**

Complete batch inference template using `fe.score_batch` for automatic feature retrieval. Supports multi-model scoring loop with per-model error isolation and PARTIAL_FAILURE exit signal.

**Key functions:**
- `get_parameters()` - Returns (catalog, gold_schema, feature_schema)
- `load_model_uri(catalog, feature_schema, model_name)` - Get latest model version URI
- `score_with_feature_engineering(...)` - `fe.score_batch()` + metadata columns + Delta save
- `run_inference_for_model(...)` - Single-model inference with error isolation
- `main()` - Multi-model loop with summary + PARTIAL_FAILURE handling

---

## Assets

### **[ml-feature-pipeline-job.yaml](assets/templates/ml-feature-pipeline-job.yaml)**

Asset Bundle job template for feature table creation. Includes `databricks-feature-engineering` dependency, `notebook_task` with `base_parameters` (catalog, gold_schema, feature_schema), and proper tags.

**Usage:**
```yaml
# Copy and customize for your project
# Replace {project} placeholder in notebook_path
```

### **[ml-training-pipeline-job.yaml](assets/templates/ml-training-pipeline-job.yaml)**

Asset Bundle job template for parallel model training. Includes pinned package versions (`mlflow==3.7.0`, `scikit-learn==1.3.2`, `xgboost==2.0.3`), multiple parallel tasks (one per model), weekly schedule (paused by default), and 4-hour timeout. Does NOT define experiments (experiments created in notebook code).

**Usage:**
```yaml
# Copy and customize: add one task_key per model
# Pin package versions to match your training environment
```

### **[ml-inference-pipeline-job.yaml](assets/templates/ml-inference-pipeline-job.yaml)**

Asset Bundle job template for batch inference with `fe.score_batch`. Includes pinned package versions (MUST match training), daily schedule (paused by default), 2-hour timeout, and proper tags.

**Usage:**
```yaml
# Copy and customize for your project
# Package versions MUST match training pipeline exactly
```

---

## Quick Validation Checklists

### Pre-Development
- [ ] Verify ALL column names against Gold layer YAML schemas
- [ ] Check if dimension tables are SCD2 (has `is_current`?)
- [ ] Confirm data types (DECIMAL, STRING, BOOLEAN, etc.)
- [ ] Identify categorical columns needing encoding
- [ ] Review Feature Store tables if using feature lookups
- [ ] Fill in [Requirements Template](references/requirements-template.md)

### MLflow Setup
- [ ] Use `/Shared/{project}_ml_{model_name}` experiment path
- [ ] Do NOT define experiments in Asset Bundle
- [ ] Inline ALL helper functions (no module imports)
- [ ] Set `mlflow.set_registry_uri("databricks-uc")` at module level
- [ ] Add `mlflow.autolog(disable=True)` before custom logging

### Feature Table Creation
- [ ] Cast ALL numeric columns to DOUBLE
- [ ] Clean NaN/Inf at source with `clean_numeric()` (sklearn compatibility)
- [ ] Filter NULL primary key rows before writing
- [ ] All columns verified against Gold layer schema
- [ ] Feature table has descriptive description
- [ ] Rolling window aggregations use proper Window specs

### Feature Engineering (Training Set)
- [ ] Uses `FeatureLookup` for feature retrieval
- [ ] `base_df` has ONLY lookup keys + label column
- [ ] `lookup_key` matches feature table primary keys EXACTLY
- [ ] `training_set` passed to `fe.log_model` (embeds feature metadata)
- [ ] **Exclude Labels**: Use `exclude_columns=[LABEL_COLUMN]` — label MUST NOT be a feature

### Training Pipeline
- [ ] Log dataset INSIDE `mlflow.start_run()` context
- [ ] Use `fe.log_model()` with `flavor=mlflow.sklearn` and `output_schema` (PRIMARY)
- [ ] `input_example` provided (or use `infer_input_example=True`)
- [ ] Register model with 3-level name: `catalog.schema.model_name`
- [ ] Label column CAST to correct type (INT for classification, DOUBLE for regression)
- [ ] All features CAST to float64 before training
- [ ] **Label Binarization**: Binarize 0-1 rates for XGBClassifier
- [ ] **Single-Class Check**: Verify label has multiple classes before training classifier
- [ ] Add `dbutils.notebook.exit("SUCCESS")` at end
- [ ] All helper functions inlined (not imported)

### Batch Inference
- [ ] Uses `fe.score_batch` for automatic feature retrieval
- [ ] Scoring DataFrame has ONLY lookup keys
- [ ] Model URI points to latest version
- [ ] Predictions saved with metadata columns (model_name, model_uri, scored_at)
- [ ] Verify feature table has no NaN before inference (sklearn compatibility)
- [ ] Error handling with proper exit signals (SUCCESS / PARTIAL_FAILURE / FAILED)
- [ ] Test with small batch before full inference

### Job Configuration
- [ ] Use `notebook_task` with `base_parameters` (not argparse)
- [ ] Pin exact package versions (match training and inference)
- [ ] DO NOT define experiments in Asset Bundle

**See:** [Troubleshooting](references/troubleshooting.md) for detailed checklists

---

## Time Estimates

| Task | Duration |
|------|----------|
| Feature Tables Setup | 2-3 hours |
| First Model (with FE) | 3-4 hours |
| Additional Models (each) | 1-2 hours |
| Batch Inference Pipeline | 2-3 hours |
| Asset Bundle Configuration | 1 hour |
| **Total (5 models)** | **10-16 hours** |

---

## Version History

### v5.1 (April 27, 2026)
- Reframed Rule #0: explicit version pins are a template-compatibility choice (training and inference must match), not an official Databricks requirement. The `mlflow==3.7.0` value in templates is a baseline.
- Reworded Rule #4 and the model-registration example: `infer_input_example=True` is the preferred path per current Feature Engineering docs; `output_schema` is a fallback for training sets without a label or non-default output shapes — not a universal UC requirement.
- Replaced 404/legacy Feature Store doc links (`feature-store/uc/index.html`, `feature-tables-uc.html`) with current docs paths under `/machine-learning/feature-store/...`.
- Added current Feature Store capability links: Online Feature Stores (Lakebase), automatic feature lookup at serving, feature serving endpoints, on-demand feature computation, point-in-time joins, declarative features, and UC feature lineage.

### v5.0 (February 2026)
- Merged comprehensive implementation guide (12-ml-models-prompt.md)
- Added Quick Start, Architecture, Directory Structure, Time Estimates
- Expanded to 19 non-negotiable rules (merged from 10+16)
- Created 3 complete script templates (feature tables, training, inference)
- Split asset templates into 3 separate job YAMLs
- Added requirements-template.md and feature-engineering-workflow.md
- Replaced hardcoded project names with `{project}` placeholders
- Resolved model registration conflict (`output_schema` as primary)
- Resolved NaN handling (clean at source, not training time)

### Future Enhancements (v6.0)
- Model aliases (`@champion`/`@challenger`) for lifecycle management
- Hyperparameter tuning (Hyperopt/Optuna + MLflow)
- Feature importance logging and visualization
- Cross-validation patterns (TimeSeriesSplit)
- Prediction monitoring integration with Lakehouse Monitoring
- AutoML baseline patterns

### v4.0 (January 14, 2026)
- Restructured to comply with AgentSkills.io specification
- Split into reference files for better organization
- Extracted scripts and templates

### v3.0 (January 4, 2026)
- NaN handling at feature table source
- Label binarization patterns
- Single-class data detection
- Feature column exclusion

### v2.0 (January 2026)
- `fe.log_model()` and `output_schema` patterns
- Model type to DataType mapping

### v1.0 (December 2025)
- Initial patterns from 5 model implementation

---

## Pipeline Progression

**Previous stage:** `monitoring/00-observability-setup` → Monitoring, dashboards, and alerts should be configured

**Next stage:** After completing ML setup, proceed to:
- **`genai-agents/00-course-orchestrator`** — Route GenAI agent implementation, evaluation, deployment, and monitoring

---

## Post-Completion: Skill Usage Summary (MANDATORY)

**After completing all sections of this orchestrator, output a Skill Usage Summary reflecting what you ACTUALLY did — not a pre-written summary.**

### What to Include

1. Every skill `SKILL.md` or `references/` file you read (via the Read tool), in the order you read them
2. Which section or step you were in when you read it (e.g., "Feature Tables", "Training", "Inference", "Jobs")
3. Whether it was a **Common**, **Reference**, or **Template** file
4. A one-line description of what you specifically used it for in this session

### Format

| # | Section | Skill / Reference Read | Type | What It Was Used For |
|---|---------|----------------------|------|---------------------|
| 1 | Section Name | `path/to/SKILL.md` | Common / Reference / Template | One-line description |

### Summary Footer

End with:
- **Totals:** X common skills, Y reference files, Z templates read across N sections
- **Models trained:** List each model name, type (classification/regression/anomaly), and algorithm
- **Skipped:** List any skills from the dependency table above that you did NOT need to read, and why (e.g., "section not applicable", "user skipped", "no issues encountered")
- **Unplanned:** List any skills you read that were NOT listed in the dependency table (e.g., for troubleshooting, edge cases, or user-requested detours)

---

## References

### Official Documentation
- [FeatureEngineeringClient Python API reference](https://api-docs.databricks.com/python/feature-engineering/latest/feature_engineering.client.html)
- [MLflow Experiments on Databricks](https://learn.microsoft.com/en-us/azure/databricks/mlflow/experiments)
- [MLflow 3.x LoggedModel](https://docs.databricks.com/aws/en/mlflow/logged-model)
- [Unity Catalog Model Registry](https://learn.microsoft.com/en-us/azure/databricks/machine-learning/manage-model-lifecycle/)
- [Databricks Feature Store overview](https://docs.databricks.com/aws/en/machine-learning/feature-store/)

### Feature Engineering on Databricks (Unity Catalog)
- [Feature Store overview and glossary](https://docs.databricks.com/aws/en/machine-learning/feature-store/concepts)
- [Create and work with feature tables](https://docs.databricks.com/aws/en/machine-learning/feature-store/uc/feature-tables-uc)
- [Train models with feature tables](https://docs.databricks.com/aws/en/machine-learning/feature-store/train-models-with-feature-store)
- [Python API reference (FeatureLookup, create_training_set, log_model, score_batch)](https://docs.databricks.com/aws/en/machine-learning/feature-store/python-api)
- [Point-in-time feature joins](https://docs.databricks.com/aws/en/machine-learning/feature-store/time-series)
- [Databricks Online Feature Stores (powered by Lakebase)](https://docs.databricks.com/aws/en/machine-learning/feature-store/online-feature-store)
- [Model Serving with automatic feature lookup](https://docs.databricks.com/aws/en/machine-learning/feature-store/automatic-feature-lookup)
- [Feature Serving endpoints](https://docs.databricks.com/aws/en/machine-learning/feature-store/feature-function-serving)
- [On-demand feature computation](https://docs.databricks.com/aws/en/machine-learning/feature-store/on-demand-features)
- [Feature governance and lineage in Unity Catalog](https://docs.databricks.com/aws/en/machine-learning/feature-store/lineage)
- [Declarative features and materialization](https://docs.databricks.com/aws/en/machine-learning/feature-store/declarative-apis)
- [MLflow Model Signatures](https://mlflow.org/docs/latest/models.html#model-signature)

### Related Skills
- `databricks-python-imports` - sys.path setup for Asset Bundles
- `databricks-asset-bundles` - Infrastructure-as-code patterns
- `databricks-autonomous-operations` - **Troubleshooting:** Read when jobs fail — provides Deploy → Poll → Diagnose → Fix → Redeploy autonomous loop, error-solution matrix, and self-healing patterns

---

## See Also

- Authoritative upstream: [databricks-agent-skills / `databricks-model-serving`](https://github.com/databricks/databricks-agent-skills/tree/main/skills/databricks-model-serving) — canonical Model Serving endpoint guidance. (Matches the `databricks-agent-skills` `upstream_sources` entry on this skill.)

