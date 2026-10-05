---
name: cv-focal-loss
description: >
  Alpha-weighted focal loss that down-weights easy examples to focus training on hard, misclassified pixels in imbalanced segmentation tasks.
---
# Focal Loss

## Overview

Focal loss addresses extreme class imbalance in segmentation (e.g., defects covering <1% of pixels). Standard BCE treats all pixels equally, so the loss is dominated by easy negatives. Focal loss adds a modulating factor `(1-p_t)^gamma` that suppresses the contribution of well-classified examples. With `gamma=2`, a pixel classified at 0.9 confidence contributes 100x less loss than one at 0.5. Combined with alpha-weighting for positive/negative balance, focal loss typically improves recall on rare classes by 5-15%.

## Quick Start

```python
import torch
import torch.nn as nn
import torch.nn.functional as F

class FocalLoss(nn.Module):
    def __init__(self, alpha=0.8, gamma=2.0):
        super().__init__()
        self.alpha = alpha
        self.gamma = gamma

    def forward(self, inputs, targets):
        inputs = torch.sigmoid(inputs).view(-1)
        targets = targets.view(-1)
        bce = F.binary_cross_entropy(inputs, targets, reduction='none')
        p_t = inputs * targets + (1 - inputs) * (1 - targets)
        focal_weight = self.alpha * (1 - p_t) ** self.gamma
        return (focal_weight * bce).mean()

# Usage
criterion = FocalLoss(alpha=0.8, gamma=2.0)
loss = criterion(logits, masks)
```

## Workflow

1. Apply sigmoid to raw logits
2. Compute per-pixel binary cross-entropy
3. Compute modulating factor `(1-p_t)^gamma` to down-weight easy examples
4. Scale by alpha for positive/negative class balance
5. Average over all pixels

## Key Decisions

- **Gamma**: 2.0 is standard; higher (3-5) for extreme imbalance, lower (0.5-1) for mild
- **Alpha**: 0.8 gives more weight to positives (minority class); tune on validation
- **vs BCE**: Use focal when positive pixels are <5% of total; BCE is fine for balanced masks
- **Combining**: Can add to Dice loss for a focal-dice hybrid

## References

- [Loss Function Library - Keras & PyTorch](https://www.kaggle.com/code/bigironsphere/loss-function-library-keras-pytorch)
