---
name: kdense-ml-ai-selected
description: "精选 K-Dense Scientific Agent Skills 的机器学习与人工智能工具包。用于 scikit-learn、PyTorch Lightning、Transformers、SHAP、time series ML、TimesFM、PyTorch Geometric、UMAP 等科研建模路线，并按 Auto-sci-research 的体育地理、城市暴露、空间公平、健康影响和论文解释边界进行封装。"
---

# K-Dense ML/AI Selected

This wrapper packages selected Machine Learning & AI skills from `K-Dense-AI/scientific-agent-skills` for Auto-sci-research.

Use it when a task needs technical playbooks for:

- `scikit-learn`
- `pytorch-lightning`
- `transformers`
- `shap`
- `timesfm-forecasting`
- `torch-geometric`
- `umap-learn`

## Local Adaptation

Use these upstream skills with local research constraints:

1. Define prediction target, population, spatial unit, temporal unit, and leakage risks before model choice.
2. Prefer simple baselines before complex models.
3. Separate predictive utility from causal interpretation.
4. For exposure, accessibility, and spatial equity work, document spatial and temporal validation splits.
5. Treat SHAP, feature importance, and embeddings as interpretation aids, not causal evidence.

For domain-specific guidance, also read:

- `../agent-auto-sci-ai-ml/references/k_dense_ml_ai_mapping.md`
- `../agent-auto-sci-ai-ml/references/ml_leakage_and_validation.md`

## Must Not Do

- Do not report only accuracy without calibration, uncertainty, and validation design.
- Do not mix training and test geographies or time periods without disclosure.
- Do not present model explanations as mechanisms unless the design supports that claim.
