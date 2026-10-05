---
name: cv-tversky-loss
description: >
  Tversky loss with independent alpha/beta constants to separately penalize false positives and false negatives in imbalanced segmentation.
---
# Tversky Loss

## Overview

Dice loss weights false positives and false negatives equally, but in many segmentation tasks they have different costs — missing a tumor (FN) is worse than a false alarm (FP). Tversky loss generalizes Dice by introducing `alpha` and `beta` to independently control FP and FN penalties: `Tversky = TP / (TP + alpha*FP + beta*FN)`. Setting `alpha=beta=0.5` recovers Dice; `alpha=0.3, beta=0.7` penalizes false negatives more, improving recall on small or rare objects.

## Quick Start

```python
import torch
import torch.nn as nn
import torch.nn.functional as F

class TverskyLoss(nn.Module):
    def __init__(self, alpha=0.3, beta=0.7, smooth=1.0):
        super().__init__()
        self.alpha = alpha
        self.beta = beta
        self.smooth = smooth

    def forward(self, inputs, targets):
        inputs = torch.sigmoid(inputs).view(-1)
        targets = targets.view(-1)
        tp = (inputs * targets).sum()
        fp = ((1 - targets) * inputs).sum()
        fn = (targets * (1 - inputs)).sum()
        tversky = (tp + self.smooth) / (tp + self.alpha * fp + self.beta * fn + self.smooth)
        return 1 - tversky

# Usage: penalize FN more than FP
criterion = TverskyLoss(alpha=0.3, beta=0.7)
loss = criterion(logits, masks)
```

## Workflow

1. Apply sigmoid to raw logits
2. Compute true positives, false positives, false negatives
3. Compute Tversky index with alpha/beta weighting
4. Return `1 - Tversky` as loss

## Key Decisions

- **alpha/beta**: `alpha < beta` boosts recall (fewer FN); `alpha > beta` boosts precision (fewer FP)
- **alpha=beta=0.5**: Equivalent to Dice loss — use as a sanity check
- **Focal Tversky**: Add `(1-Tversky)^gamma` to further focus on hard examples
- **Smooth**: 1.0 prevents division by zero; lower values (0.01) for sharper gradients

## References

- [Loss Function Library - Keras & PyTorch](https://www.kaggle.com/code/bigironsphere/loss-function-library-keras-pytorch)
