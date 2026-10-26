---
name: databricks-ml-associate
description: Use when preparing for Databricks Certified Machine Learning Associate — the four sections (Databricks Machine Learning, ML workflows, model development, model deployment), MLflow tracking and the Unity Catalog model registry, AutoML, feature engineering and the feature store, Spark ML and pandas API on Spark, hyperparameter tuning, and batch or real-time serving; practising with hands-on runs on Databricks. Also use when writing or verifying practice questions grounded in Databricks, MLflow and Spark documentation.
---

# Databricks Certified Machine Learning Associate

Bottom line: **know which Databricks feature does each step of an ML workflow, and read Python code fluently**. Questions are mostly scenarios ("a data scientist needs to ... with the least effort") and code snippets in Python (data manipulation may appear in SQL).

## Exam shape (confirm on the Databricks certification page)

- Multiple choice, 90 minutes, online proctored; recertification every two years by taking the current version.
- Sections: Databricks Machine Learning (largest), ML Workflows, Model Development, Model Deployment. Check the exam guide for the current weights and objectives — the guide changes between versions.

Primary sources: Databricks certification page and exam guide (https://www.databricks.com/learn/certification), Databricks documentation (machine learning, Unity Catalog, Model Serving), MLflow documentation, Apache Spark MLlib documentation.

## Concept map

| Section | Know |
|---|---|
| Databricks ML | Workspace and compute choices for ML (ML runtime, serverless), AutoML (what it produces: notebooks, best run, data exploration), feature engineering in Unity Catalog (feature tables, point-in-time lookups), MLflow experiments and runs, model registration in Unity Catalog with aliases |
| ML workflows | Exploratory analysis, train/test splits, cross-validation, handling missing values (imputation), encoding categorical features, pipelines |
| Model development | Spark ML estimators/transformers/pipelines, pandas API on Spark and pandas UDFs, hyperparameter tuning (e.g. Hyperopt or Optuna, parallel trials), evaluation metrics for classification and regression |
| Model deployment | Batch inference with Spark UDFs from MLflow models, streaming inference, real-time Model Serving endpoints, choosing between them by latency and volume |

## Hands-on loop (Free Edition or any workspace)

1. Train a small scikit-learn model with MLflow autologging; inspect the run (params, metrics, artifacts).
2. Register it in Unity Catalog, set an alias, load it by alias.
3. Score a table in batch with `mlflow.pyfunc.spark_udf`.
4. Run AutoML on a sample table and read the generated notebook.
5. Build a Spark ML pipeline with an imputer, a string indexer, a vector assembler and an estimator; cross-validate it.

Doing each once answers many scenario questions better than reading.

## Writing practice questions

- Verify every behaviour against the documentation page and cite it; check method and parameter names in the current library versions.
- Mix question types: mostly scenarios, a few term-to-definition items, each with a reason for every option.
- Do not reuse the same stem with options shuffled; vary situations.

## Pitfalls

- **Stages vs aliases:** current Unity Catalog registry uses aliases; older material talks about Staging/Production stages.
- **Spark ML fit/transform:** estimators `fit` and return models (transformers); transformers `transform`.
- **Data leakage:** fitting imputers or scalers on the full dataset before splitting.
- **pandas on a cluster:** plain pandas runs on the driver; use pandas API on Spark or pandas UDFs for distributed work.
- **Feature lookups** at inference must use the same feature definitions as training.

## Self-check

- A full practice set within 90 minutes with clear margin.
- Explain the path from experiment run to served endpoint, naming the Databricks feature at each step.
- Read an unfamiliar Spark ML code snippet and predict its output schema.
