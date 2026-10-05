---
name: cv-lovasz-hinge-loss
description: >
  Lovasz hinge loss that directly optimizes IoU for binary segmentation by computing a convex surrogate via sorted prediction errors and cumulative Jaccard gradients.
---
# Lovasz Hinge Loss

## Overview

Standard losses (BCE, Dice) are proxies for IoU — they correlate with it but don't optimize it directly. Lovasz hinge loss computes the exact subgradient of the Jaccard index by sorting prediction errors, computing cumulative intersection/union, and using the Lovasz extension of submodular functions. This makes it a tight convex surrogate for 1-IoU. In practice, it consistently outperforms BCE and Dice on IoU-based metrics by 1-3%, especially when mask shapes are irregular or class distributions are skewed.

## Quick Start

```python
import torch
import torch.nn.functional as F

def lovasz_grad(gt_sorted):
    p = len(gt_sorted)
    gts = gt_sorted.sum()
    intersection = gts - gt_sorted.float().cumsum(0)
    union = gts + (1 - gt_sorted).float().cumsum(0)
    jaccard = 1.0 - intersection / union
    if p > 1:
        jaccard[1:p] = jaccard[1:p] - jaccard[0:-1]
    return jaccard

def lovasz_hinge_flat(logits, labels):
    signs = 2.0 * labels.float() - 1.0
    errors = 1.0 - logits * signs
    errors_sorted, perm = torch.sort(errors, dim=0, descending=True)
    gt_sorted = labels[perm.data]
    grad = lovasz_grad(gt_sorted)
    return torch.dot(F.relu(errors_sorted), grad)

# Usage: pass raw logits (before sigmoid)
loss = lovasz_hinge_flat(logits.view(-1), masks.view(-1))
```

## Workflow

1. Compute signed errors: `1 - logit * sign(label)`
2. Sort errors in descending order
3. Compute cumulative Jaccard gradients via `lovasz_grad`
4. Dot product of ReLU'd errors with gradients gives the loss
5. Operates on raw logits — do NOT apply sigmoid first

## Key Decisions

- **Input**: Raw logits, not probabilities — the hinge formulation needs unbounded values
- **Per-image vs batch**: Compute per-image then average for stable gradients
- **Warm-up**: Train with BCE for first few epochs, then switch to Lovasz for fine-tuning
- **Multi-class**: Use `lovasz_softmax` variant for multi-class segmentation

## References

- [Loss Function Library - Keras & PyTorch](https://www.kaggle.com/code/bigironsphere/loss-function-library-keras-pytorch)
