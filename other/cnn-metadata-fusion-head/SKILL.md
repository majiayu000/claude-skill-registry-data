---
name: cv-cnn-metadata-fusion-head
description: Fuse CNN image features with a small tabular MLP branch via concat before a final classifier, training both branches end-to-end
---

## Overview

Many image-classification tasks ship with tabular metadata (patient age, sex, anatomic site, device model) that is independently predictive. The cleanest way to use both is a two-branch network: a CNN processes the image, a small MLP processes normalized tabular features, and the two feature vectors are concatenated before the final classifier. Everything trains end-to-end with a single loss. Reported lift on SIIM-ISIC Melanoma: ~0.5-1 AUC point over image-only baselines, and the tabular branch is tiny (~0.1M params).

## Quick Start

```python
import torch
import torch.nn as nn
from efficientnet_pytorch import EfficientNet

class ImageMetaNet(nn.Module):
    def __init__(self, n_meta_features, arch='efficientnet-b0'):
        super().__init__()
        self.cnn = EfficientNet.from_pretrained(arch)
        self.cnn._fc = nn.Linear(self.cnn._fc.in_features, 500)

        self.meta = nn.Sequential(
            nn.Linear(n_meta_features, 500),
            nn.BatchNorm1d(500), nn.ReLU(), nn.Dropout(0.2),
            nn.Linear(500, 250),
            nn.BatchNorm1d(250), nn.ReLU(), nn.Dropout(0.2),
        )
        self.classifier = nn.Linear(750, 1)   # 500 + 250 concat

    def forward(self, inputs):
        x, meta = inputs            # x: image, meta: (B, n_meta_features)
        img_feat = self.cnn(x)
        meta_feat = self.meta(meta)
        fused = torch.cat((img_feat, meta_feat), dim=1)
        return self.classifier(fused)
```

## Workflow

1. Normalize tabular features (standardize continuous, one-hot or embed categorical) in the dataset
2. Dataset `__getitem__` returns a tuple `(image_tensor, meta_tensor, label)`
3. Forward takes a tuple `(x, meta)` and runs both branches in parallel
4. Concatenate on the feature axis, not the batch axis
5. Train with one loss on the classifier output — no separate tabular loss needed

## Key Decisions

- **Meta branch width ~ image feature width / 2**: equal widths drown out the image branch; too small and the meta branch collapses.
- **BN + Dropout on the meta path**: prevents the small MLP from overfitting the low-dim tabular input.
- **Concat, not add**: addition requires same dims and imposes an untrained alignment.
- **vs. separate models + late blending**: end-to-end fusion learns which features help, blending requires hand-tuned weights and loses interaction terms.

## References

- [Melanoma. Pytorch starter. EfficientNet](https://www.kaggle.com/code/nroman/melanoma-pytorch-starter-efficientnet)
