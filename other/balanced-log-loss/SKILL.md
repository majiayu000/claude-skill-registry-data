---
name: tabular-balanced-log-loss
description: >
  Class-balanced log loss that weights each class by the inverse of its sample count, equalizing the contribution of minority and majority classes.
---
# Balanced Log Loss

## Overview

Standard log loss is dominated by the majority class — in a 90/10 split, the loss is 90% driven by class-0 predictions. Balanced log loss weights each class by `1/N_class`, equalizing their contribution regardless of sample count. This is the correct metric when false negatives on the minority class are as costly as false positives on the majority class. Many Kaggle competitions with imbalanced binary targets use this as the official metric.

## Quick Start

```python
import numpy as np

def balanced_log_loss(y_true, y_pred):
    """Compute class-balanced log loss.

    Args:
        y_true: binary labels (0 or 1)
        y_pred: predicted probability of class 1
    Returns:
        Balanced log loss (lower is better)
    """
    y_pred = np.clip(y_pred, 1e-15, 1 - 1e-15)
    n_0 = np.sum(1 - y_true)
    n_1 = np.sum(y_true)

    loss_0 = -np.sum((1 - y_true) * np.log(1 - y_pred)) / n_0
    loss_1 = -np.sum(y_true * np.log(y_pred)) / n_1

    return (loss_0 + loss_1) / 2

# Usage
score = balanced_log_loss(y_val, model.predict_proba(X_val)[:, 1])
```

## Workflow

1. Clip predictions to avoid log(0)
2. Compute log loss for each class separately
3. Divide each class's loss by its sample count
4. Average the two normalized losses

## Key Decisions

- **Clipping**: 1e-15 is standard; prevents -inf from log(0)
- **vs sample_weight**: Equivalent to `log_loss(y, p, sample_weight=inverse_freq)` but more explicit
- **Multiclass**: Extend by weighting each of K classes by `1/N_k`
- **Optimization**: Train with class-weighted BCE to optimize for this metric directly

## References

- [Postprocessin_ Ensemble](https://www.kaggle.com/code/vadimkamaev/postprocessin-ensemble)
