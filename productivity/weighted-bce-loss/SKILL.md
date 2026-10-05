---
name: cv-weighted-bce-loss
description: >
  BCE loss with per-class asymmetric positive/negative weights to match competition metrics or handle class imbalance in multilabel classification.
---
# Weighted BCE Loss

## Overview

Standard BCE treats false positives and false negatives equally across all classes. In medical imaging and multilabel tasks, certain classes matter more (e.g., missing a fracture is worse than a false alarm). This loss applies separate positive and negative weights per class, normalizing per sample so that the total contribution stays balanced. Matches competition scoring functions that penalize certain errors more heavily.

## Quick Start

```python
import torch
import torch.nn.functional as F

def weighted_bce_loss(logits, targets, pos_weights, neg_weights, reduction='mean'):
    """BCE with per-class asymmetric weights.

    Args:
        logits: (B, C) raw model output
        targets: (B, C) binary targets
        pos_weights: (C,) weight for positive samples per class
        neg_weights: (C,) weight for negative samples per class
    """
    loss = F.binary_cross_entropy_with_logits(logits, targets, reduction='none')
    weights = targets * pos_weights.unsqueeze(0) + (1 - targets) * neg_weights.unsqueeze(0)
    loss = loss * weights
    # Normalize per sample
    norm = weights.sum(dim=1, keepdim=True)
    loss = (loss / norm).sum(dim=1)
    return loss.mean() if reduction == 'mean' else loss

# Example: fracture detection — penalize missed fractures 2x
pos_w = torch.tensor([14., 2., 2., 2., 2., 2., 2., 2.])
neg_w = torch.tensor([7., 1., 1., 1., 1., 1., 1., 1.])
loss = weighted_bce_loss(logits, targets, pos_w, neg_w)
```

## Workflow

1. Define per-class positive and negative weights (from competition metric or domain knowledge)
2. Compute standard BCE loss per element
3. Multiply by class-specific weights based on whether target is 0 or 1
4. Normalize per sample to prevent weight magnitude from dominating learning rate

## Key Decisions

- **Weight ratio**: Derived from competition metric or class frequency (e.g., `pos_weight = neg_count / pos_count`)
- **Normalization**: Per-sample normalization prevents classes with high weights from dominating
- **vs pos_weight in PyTorch**: `BCEWithLogitsLoss(pos_weight=...)` only supports positive weights, not separate pos/neg
- **Combine with**: Focal loss for hard-example mining on top of class weighting

## References

- [PyTorch-EffNetV2 baseline CV:0.49](https://www.kaggle.com/code/vslaykovsky/train-pytorch-effnetv2-baseline-cv-0-49)
