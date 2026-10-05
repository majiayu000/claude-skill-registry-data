---
name: cv-dice-loss
description: >
  Dice coefficient loss for pixel-level segmentation that directly optimizes the overlap between predicted and ground-truth masks.
---
# Dice Loss

## Overview

Dice loss computes `1 - (2*|P intersect G| / (|P| + |G|))`, directly optimizing the F1/Dice overlap metric. Unlike BCE which operates per-pixel independently, Dice loss considers the global mask overlap, making it naturally robust to class imbalance — when only 1% of pixels are positive, BCE is dominated by easy negatives, but Dice loss focuses on the positive region overlap. Dice loss is the default choice for binary segmentation and typically improves IoU by 2-5% over pure BCE on imbalanced masks.

## Quick Start

```python
import torch
import torch.nn as nn

class DiceLoss(nn.Module):
    def __init__(self, smooth=1.0):
        super().__init__()
        self.smooth = smooth

    def forward(self, inputs, targets):
        inputs = torch.sigmoid(inputs).view(-1)
        targets = targets.view(-1)
        intersection = (inputs * targets).sum()
        dice = (2.0 * intersection + self.smooth) / (
            inputs.sum() + targets.sum() + self.smooth
        )
        return 1 - dice

# Usage
criterion = DiceLoss()
loss = criterion(logits, masks)
```

## Workflow

1. Apply sigmoid to raw logits
2. Flatten predictions and targets to 1D
3. Compute soft intersection: sum of element-wise product
4. Compute Dice coefficient with smoothing
5. Return `1 - Dice` as loss

## Key Decisions

- **Smooth**: 1.0 is standard; prevents NaN when both prediction and target are empty
- **Per-class vs global**: For multi-class, compute per-class then average for balanced gradients
- **vs BCE+Dice**: Combining BCE + Dice often outperforms either alone (see `cv-bce-dice-combined-loss`)
- **Soft vs hard**: Soft Dice (use probabilities) for training; hard Dice (threshold first) for evaluation

## References

- [Loss Function Library - Keras & PyTorch](https://www.kaggle.com/code/bigironsphere/loss-function-library-keras-pytorch)
