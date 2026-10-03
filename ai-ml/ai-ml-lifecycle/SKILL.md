---
name: ai-ml-lifecycle
description: Route AI evaluation, ML training and inference engineering, and model operational readiness; use security review for authority-boundary threats.
---

# AI And ML Lifecycle

Choose one primary mode and read only its workflow. Add another mode only when the requested evidence crosses lifecycle stages.

| Mode | Use when | Workflow |
| --- | --- | --- |
| `ai-evals` | Design cases, datasets, rubrics, judges, thresholds, or behavioral regression evidence. | [AI evaluations](references/workflows/ai-evals.md) |
| `ml-engineering` | Design or review features, training, evaluation, packaging, inference, or integration behavior. | [ML engineering](references/workflows/ml-engineering.md) |
| `mlops-readiness` | Review registry, promotion, reproducibility, deployment, monitoring, drift, or rollback controls. | [MLOps readiness](references/workflows/mlops-readiness.md) |

Do not load sibling workflows or artifacts prospectively. Keep claims tied to datasets and executed evidence; keep production promotion and rollback behind named owner approval.
