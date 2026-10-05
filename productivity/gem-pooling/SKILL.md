---
name: cv-gem-pooling
description: >
  Replaces global average pooling with Generalized Mean (GeM) pooling, using a learnable or fixed exponent to emphasize high-activation regions.
---
# GeM Pooling

## Overview

Global Average Pooling (GAP) treats all spatial locations equally, diluting strong local signals in large feature maps. Generalized Mean (GeM) pooling raises activations to power `p` before averaging, then takes the p-th root — higher `p` values emphasize peak activations (approaching max pooling at p→∞). With p=1 it's average pooling; p=3 is a common default that boosts discriminative regions. Used extensively in retrieval (image search, metric learning) and medical imaging where lesions occupy small regions.

## Quick Start

```python
import torch
import torch.nn as nn
import torch.nn.functional as F
from torch.nn.parameter import Parameter
import timm

class GeM(nn.Module):
    def __init__(self, p=3.0, eps=1e-6, p_trainable=False):
        super().__init__()
        self.p = Parameter(torch.ones(1) * p) if p_trainable else p
        self.eps = eps

    def forward(self, x):
        return F.avg_pool2d(
            x.clamp(min=self.eps).pow(self.p),
            (x.size(-2), x.size(-1))
        ).pow(1.0 / self.p)

# Plug into any timm backbone
backbone = timm.create_model('seresnext50_32x4d', pretrained=True,
                              num_classes=0, global_pool='')
pool = GeM(p=3.0, p_trainable=True)
head = nn.Linear(backbone.num_features, num_classes)

# Forward
features = backbone(images)       # (B, C, H, W)
pooled = pool(features).squeeze()  # (B, C)
logits = head(pooled)              # (B, num_classes)
```

## Workflow

1. Create backbone with `global_pool=''` and `num_classes=0` to get raw feature maps
2. Add GeM pooling layer (fixed p=3 or learnable)
3. Add linear classification head on top
4. Train end-to-end — if p is learnable, it adapts to the task

## Key Decisions

- **p value**: p=3 is standard; higher (5–7) for very localized signals; p=1 degrades to GAP
- **Trainable p**: Set `p_trainable=True` for the model to learn optimal pooling aggression
- **eps clamping**: Essential — prevents NaN from negative activations raised to fractional power
- **vs MAC/SPoC**: GeM generalizes both; SPoC=p=1, MAC≈p→∞

## References

- [SE-ResNeXt50 Full GPU Decoding](https://www.kaggle.com/code/christofhenkel/se-resnext50-full-gpu-decoding)
