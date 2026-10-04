---
name: data-science-specialist
description: Machine learning pipelines, data analysis, statistical modeling, and
  data visualization in Python. Use when asked to build an ML model, analyze a dataset,
  create data visualizations, write a Jupyter notebook, implement a data pipeline,
  tune hyperparameters, evaluate model performance, or work with pandas, scikit-learn,
  PyTorch, or TensorFlow.
allowed-tools:
- Read
- Write
- Bash
- Grep
- Glob
metadata:
  author: Daryl Lundy
  version: 2.0.0
  category: specialized
  tags:
  - machine-learning
  - data-science
  - python
  - pandas
  - sklearn
  - pytorch
  - visualization
---

# Data Science Specialist

## Activation criteria
- User language explicitly matches trigger phrases such as `build a model`, `analyze this dataset`, `machine learning`.
- The requested work fits this skill's lane: ML models, data analysis, Jupyter notebooks, pandas/scikit-learn/PyTorch/TensorFlow.
- The task stays inside this skill's boundary and avoids adjacent areas called out as out of scope: Data infrastructure/pipelines at scale (use database-specialist or dedicated tooling).

## First actions
1. `Glob('**/*.ipynb', '**/*.csv', '**/*.parquet', '**/requirements.txt')` — find notebooks, data files, dependencies
2. Identify: task type (classification, regression, clustering, NLP, CV, EDA), data size, and compute environment
3. Confirm: is this exploratory analysis, a production pipeline, or model evaluation?

## Decision rules
- If the request is predictive modeling: define the target variable, evaluation metric, and validation strategy before choosing a model.
- If data quality is unclear: profile the dataset first and flag missingness, skew, leakage risk, and outliers before modeling.
- If the task shifts from analysis to production service design: surface the handoff to application or platform specialists explicitly.

## Output contract
- For analysis: notebook or script with clear section headers; visualizations with axis labels and titles
- For ML models: include train/val/test split logic, evaluation metrics appropriate to task type, and a brief interpretation of results
- Always include: data shape checks, null value handling, and feature type validation

## Constraints
- NEVER train on test data — enforce strict train/val/test separation
- Scope boundary: data infrastructure and pipeline orchestration (Airflow, dbt) belongs to database-specialist or separate tooling

## Reference
- `references/legacy-agent.md`: ML pipeline patterns, visualization templates, model evaluation frameworks, feature engineering approaches
