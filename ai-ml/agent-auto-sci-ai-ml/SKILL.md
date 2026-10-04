---
name: agent-auto-sci-ai-ml
description: "机器学习与人工智能科研子 skill。用于地理学+体育学项目中的 classical ML、深度学习、时间序列、模型评估、数据泄露检查、基线设计、超参数搜索、SHAP/可解释 AI、公平性诊断、实验复现和论文方法写作。触发于 machine learning、AI、scikit-learn、PyTorch Lightning、transformers、SHAP、model evaluation、XAI、spatial ML、time series 等任务。"
---

# Agent Auto Sci AI ML

Use this subskill when the project needs modeling rather than only descriptive analysis.

## Fast Workflow

1. Define prediction or explanation target.
2. Build a data dictionary and leakage checklist.
3. Establish simple baselines before complex models.
4. Choose model family: classical ML, deep learning, time series, spatial ML, or NLP/transformer.
5. Split data correctly: spatial, temporal, group, or external validation as needed.
6. Evaluate with task-appropriate metrics and uncertainty.
7. Interpret with SHAP, permutation importance, partial dependence, or ablation.
8. Translate model results into manuscript claims only after robustness checks.

Read `references/ml_ai_workflows.md`.

For full paper projects, this skill owns baseline design, model/method selection, leakage checks, train/test split logic, hyperparameter search, ablation, robustness, error-case analysis, XAI, and methods/results reporting boundaries. It must work with `agent-auto-sci-methodology` before turning feature importance into mechanism language.

For deeper K-Dense-style encapsulation:

- `references/k_dense_ml_ai_mapping.md`: how scikit-learn, PyTorch Lightning, transformers, SHAP, time-series, and XAI skills are adapted.
- `references/sport_geography_ml_playbook.md`: sport geography modeling patterns, leakage checks, baselines, and manuscript reporting.

## Related Helper Skills

Use installed helper skills when useful:

- `scikit-learn`
- `pytorch-lightning`
- `transformers`
- `shap`
- `aeon`
- `timesfm-forecasting`
- `statistical-analysis`
- `agent-auto-sci-data-viz`
- `agent-auto-sci-geospatial`

## Must Not Do

- Do not use ML if the research question only needs transparent spatial/statistical analysis.
- Do not report accuracy without baselines and uncertainty.
- Do not mix train/test spatial units when spatial leakage is possible.
- Do not use SHAP as causal evidence.

