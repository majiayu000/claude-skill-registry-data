---
name: cv-bce-dice-combined-loss
description: >
  Combines BCE-with-logits and soft Dice loss with configurable weights for binary and multilabel segmentation training.
---
# BCE + Dice Combined Loss

## Overview

BCE loss optimizes per-pixel accuracy but struggles with class imbalance in segmentation (background dominates). Dice loss directly optimizes the Dice coefficient (F1 score) and handles imbalance well, but has noisy gradients. Combining both gives stable training from BCE while pushing toward high Dice overlap. This is the standard loss for medical image segmentation tasks.

## Quick Start

```python
import torch
import torch.nn as nn

def dice_loss(logits, targets, smooth=1.0):
    probs = torch.sigmoid(logits)
    iflat = probs.view(-1)
    tflat = targets.view(-1)
    intersection = (iflat * tflat).sum()
    return 1 - (2. * intersection + smooth) / (iflat.sum() + tflat.sum() + smooth)

def bce_dice_loss(logits, targets, bce_weight=1.0, dice_weight=1.0):
    bce = nn.functional.binary_cross_entropy_with_logits(logits, targets)
    dice = dice_loss(logits, targets)
    return (bce_weight * bce + dice_weight * dice) / (bce_weight + dice_weight)

# Usage
loss = bce_dice_loss(model_output, mask_target)
```

## Workflow

1. Compute BCE with logits loss (handles numerical stability internally)
2. Compute soft Dice loss from sigmoid probabilities
3. Combine with configurable weights (default 1:1)
4. Backpropagate the combined loss

## Key Decisions

- **Weight ratio**: 1:1 is standard; increase Dice weight (e.g., 1:2) if IoU/Dice metric matters more
- **Smooth factor**: 1.0 prevents division by zero; lower (0.01) for sharper gradients
- **Multilabel**: Apply per-channel, then average across classes
- **vs Focal + Dice**: Use Focal instead of BCE when many easy negatives dominate
- **vs Lovasz**: Lovasz loss directly optimizes IoU but is slower; combine with BCE similarly

## References

- [RSNA 2022 1st Place Solution - Train Stage1](https://www.kaggle.com/code/haqishen/rsna-2022-1st-place-solution-train-stage1)
