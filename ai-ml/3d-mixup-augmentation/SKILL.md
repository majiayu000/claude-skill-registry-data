---
name: cv-3d-mixup-augmentation
description: >
  Applies Mixup augmentation to 3D volumetric images and their segmentation masks, interpolating both inputs and loss targets.
---
# 3D Mixup Augmentation

## Overview

Mixup creates virtual training samples by linearly interpolating pairs of inputs and their labels. For 3D medical imaging (CT, MRI), this regularizes the model by blending volumetric scans and their segmentation masks. The loss is computed against both original and shuffled targets, weighted by the interpolation factor lambda. Reduces overfitting on small 3D datasets where traditional augmentations (flip, rotate) are limited.

## Quick Start

```python
import torch
import numpy as np

def mixup_3d(images, masks, alpha=1.0):
    """Mixup for 3D volumes and segmentation masks.

    Args:
        images: (B, C, D, H, W) volumetric input
        masks: (B, C, D, H, W) segmentation targets
        alpha: Beta distribution parameter (1.0 = uniform)
    """
    lam = np.random.beta(alpha, alpha)
    indices = torch.randperm(images.size(0))
    mixed_images = lam * images + (1 - lam) * images[indices]
    return mixed_images, masks, masks[indices], lam

# In training loop:
if np.random.random() < 0.5:  # 50% probability
    images, masks_a, masks_b, lam = mixup_3d(images, masks)
    logits = model(images)
    loss = lam * criterion(logits, masks_a) + (1 - lam) * criterion(logits, masks_b)
else:
    logits = model(images)
    loss = criterion(logits, masks)
```

## Workflow

1. Sample lambda from Beta(alpha, alpha) distribution
2. Shuffle batch to get pairing indices
3. Blend images: `lam * img_A + (1-lam) * img_B`
4. Compute loss against both original and shuffled targets, weighted by lambda

## Key Decisions

- **alpha**: 1.0 gives uniform lambda; lower values (0.2-0.4) keep lambda closer to 0 or 1
- **Probability**: Apply mixup stochastically (30-50% of batches) to preserve some clean samples
- **Segmentation vs classification**: For segmentation, blend masks too; for classification, blend labels
- **CutMix alternative**: Replace a random 3D patch instead of blending the whole volume

## References

- [RSNA 2022 1st Place Solution - Train Stage1](https://www.kaggle.com/code/haqishen/rsna-2022-1st-place-solution-train-stage1)
