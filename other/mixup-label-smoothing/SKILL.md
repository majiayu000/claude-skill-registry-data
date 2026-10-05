---
name: cv-mixup-label-smoothing
description: >
  Combines mixup augmentation (linear interpolation of image pairs and their labels) with label smoothing in a single training pipeline for regularization.
---
# Mixup + Label Smoothing

## Overview

Mixup and label smoothing both soften training targets to reduce overfitting, but through different mechanisms. Mixup creates virtual training examples by linearly blending two images and their labels: `img = λ·img1 + (1-λ)·img2`, `label = λ·y1 + (1-λ)·y2`. Label smoothing shifts hard labels toward uniform: `y_smooth = (1-ε)·y + ε/K`. Combining both provides complementary regularization — mixup smooths the input space while label smoothing prevents overconfident predictions. Together they typically improve generalization by 0.5–1.5% accuracy.

## Quick Start

```python
import numpy as np
import torch

class MixupLabelSmoothingDataset(torch.utils.data.Dataset):
    def __init__(self, dataset, mixup_prob=0.5, mixup_alpha=0.2,
                 label_smoothing=0.05, num_classes=2):
        self.dataset = dataset
        self.mixup_prob = mixup_prob
        self.alpha = mixup_alpha
        self.eps = label_smoothing
        self.K = num_classes

    def smooth_label(self, label):
        """Apply label smoothing: shift toward uniform."""
        one_hot = torch.zeros(self.K)
        one_hot[label] = 1.0
        return one_hot * (1 - self.eps) + self.eps / self.K

    def __getitem__(self, idx):
        img1, label1 = self.dataset[idx]
        target1 = self.smooth_label(label1)

        if np.random.random() < self.mixup_prob:
            j = np.random.randint(len(self.dataset))
            img2, label2 = self.dataset[j]
            target2 = self.smooth_label(label2)

            lam = np.random.beta(self.alpha, self.alpha)
            img = lam * img1 + (1 - lam) * img2
            target = lam * target1 + (1 - lam) * target2
        else:
            img, target = img1, target1

        return img, target
```

## Workflow

1. Apply label smoothing to convert hard labels to soft targets
2. With probability `mixup_prob`, sample a second example and blend
3. Blend both images and soft targets with the same lambda
4. Train with soft cross-entropy (KL divergence) loss, not hard CE

## Key Decisions

- **Mixup alpha**: 0.2 is standard; higher (0.4) for stronger regularization
- **Label smoothing ε**: 0.05–0.1; higher for noisy labels or small datasets
- **Loss function**: Must use soft-label loss (KLDivLoss or manual BCE with soft targets)
- **Order**: Smooth first, then mixup — smoothing modifies the targets mixup will blend

## References

- [VinBigData 2-Class Classifier Complete Pipeline](https://www.kaggle.com/code/corochann/vinbigdata-2-class-classifier-complete-pipeline)
