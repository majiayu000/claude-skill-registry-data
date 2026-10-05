---
name: cv-sigmoid-normalized-rmse
description: Sigmoid-transformed normalized RMSE that maps error from [0,inf) to a bounded (0,1] similarity score using R2-score ratio
---

# Sigmoid Normalized RMSE

## Overview

Standard RMSE is unbounded and hard to interpret across different scales. Normalize RMSE by dividing by the baseline error (predicting the mean), then apply a sigmoid transform `2 - 2/(1+exp(-x))` to map the result to (0, 1]. Perfect predictions score 1.0, predictions at baseline quality score ~0.63, and worse-than-baseline predictions approach 0. This creates a bounded, interpretable metric suitable for averaging across heterogeneous data series.

## Quick Start

```python
import numpy as np
from sklearn.metrics import r2_score

def sigmoid(x):
    return 2 - 2 / (1 + np.exp(-x))

def sigmoid_normalized_rmse(y_true, y_pred):
    r2 = r2_score(y_true, y_pred)
    normalized_error = max(0, (1 - r2)) ** 0.5
    return sigmoid(normalized_error)

y_true = [10, 20, 30, 40, 50]
y_pred = [12, 18, 33, 38, 52]
score = sigmoid_normalized_rmse(y_true, y_pred)  # ~0.89
```

## Workflow

1. Compute R2 score between predictions and ground truth
2. Convert to normalized error: `sqrt(max(0, 1 - R2))`
3. Apply sigmoid transform: `2 - 2/(1 + exp(-error))`
4. Result is in (0, 1] — higher is better

## Key Decisions

- **Why sigmoid**: bounds the metric to (0, 1], making it averageable across different scales
- **R2-based normalization**: divides by variance of true values, making it scale-invariant
- **sqrt(1-R2)**: equivalent to RMSE/std(y_true), the coefficient of variation of error
- **Use case**: comparing prediction quality across series with different magnitudes

## References

- [Competition Metric - Benetech Mixed-Match](https://www.kaggle.com/code/ryanholbrook/competition-metric-benetech-mixed-match)
