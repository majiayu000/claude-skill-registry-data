---
name: nlp-sqrt-mse-loss
description: >
  Uses square root of MSE as training loss to directly optimize for RMSE evaluation metric alignment.
---
# Sqrt MSE Loss

## Overview

When the competition metric is RMSE, training with standard MSE can misalign gradients because MSE squares the errors. Using `sqrt(MSE)` as the loss directly optimizes the metric you're evaluated on. This often improves final scores by 0.01-0.03 RMSE compared to plain MSE, especially when error magnitudes vary.

## Quick Start

```python
import torch
import torch.nn as nn

class RMSELoss(nn.Module):
    def __init__(self, eps=1e-8):
        super().__init__()
        self.mse = nn.MSELoss()
        self.eps = eps

    def forward(self, preds, targets):
        return torch.sqrt(self.mse(preds, targets) + self.eps)

# Usage
criterion = RMSELoss()
loss = criterion(model_output.view(-1), labels.view(-1))
loss.backward()
```

## Workflow

1. Replace `nn.MSELoss()` with `RMSELoss()` in training loop
2. Add small epsilon inside sqrt for numerical stability
3. Train as usual — gradients are automatically adjusted

## Key Decisions

- **Epsilon**: 1e-8 prevents NaN when loss approaches zero
- **When to use**: Whenever the evaluation metric is RMSE
- **Gradient behavior**: Sqrt amplifies gradients for small errors, dampens for large — acts as implicit focus on hard examples
- **Alternatives**: Huber loss if you want robustness to outliers instead

## References

- CommonLit Readability Prize (Kaggle)
- Source: [commonlit-readability-prize-roberta-torch-infer-3](https://www.kaggle.com/code/rhtsingh/commonlit-readability-prize-roberta-torch-infer-3)
