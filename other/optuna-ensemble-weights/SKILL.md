---
name: nlp-optuna-ensemble-weights
description: >
  Learns optimal per-model blending weights via Optuna optimization, supporting negative weights for error cancellation.
---
# Optuna Ensemble Weights

## Overview

Instead of equal-weight averaging across models, use Optuna to search for optimal per-model weights that minimize the validation metric. Weights can be negative — allowing error cancellation between correlated models. Optimize separately per target when targets have different optimal blends.

## Quick Start

```python
import optuna
import numpy as np

def optimize_weights(predictions, labels, n_models, target_name):
    def objective(trial):
        weights = [trial.suggest_float(f"w{i}", -0.5, 1.0) for i in range(n_models)]
        blended = np.stack([p * w for p, w in zip(predictions, weights)]).sum(0)
        rmse = np.sqrt(np.mean((blended - labels) ** 2))
        return rmse

    study = optuna.create_study(direction="minimize")
    study.optimize(objective, n_trials=200, show_progress_bar=False)
    return [study.best_params[f"w{i}"] for i in range(n_models)]

# Per-target optimization
content_weights = optimize_weights(content_preds, content_labels, 4, "content")
wording_weights = optimize_weights(wording_preds, wording_labels, 4, "wording")
```

## Workflow

1. Collect OOF predictions from each model architecture
2. Define Optuna objective: weighted sum → RMSE on validation
3. Search weight space (allow negative for error cancellation)
4. Optimize separately per target
5. Apply learned weights at inference time

## Key Decisions

- **Negative weights**: Allow [-0.5, 1.0] range; enables cancellation of correlated errors
- **Per-target weights**: Different targets may prefer different model mixes
- **n_trials**: 200 is usually sufficient for 3-5 models
- **vs grid search**: Optuna's TPE sampler is more efficient in continuous weight space

## References

- CommonLit - Evaluate Student Summaries (Kaggle)
- Source: [infer-2x-t4](https://www.kaggle.com/code/nbroad/infer-2x-t4)
