---
name: cv-embedding-knn-regression
description: GPU-accelerated k-NN regression on CLIP image embeddings using cosine distance and inverse-distance-power weighting to predict target embedding vectors
---

# Embedding k-NN Regression

## Overview

When mapping images to target embeddings (e.g., prompt embeddings), k-NN regression in the CLIP embedding space is a strong non-parametric baseline. Compute cosine distances between test image embeddings and a reference set, find the k nearest neighbors, then weight their target embeddings by inverse distance raised to a power. GPU acceleration with batched matrix multiply makes this fast even for 100k+ reference points.

## Quick Start

```python
import torch
import numpy as np

def knn_predict(ref_x, ref_y, test_x, k=100, power=6, batch=1000):
    ref_x = torch.from_numpy(ref_x).cuda()
    ref_x /= ref_x.norm(dim=-1, keepdim=True)
    ref_y = torch.from_numpy(ref_y).cuda()
    preds = []
    for i in range(0, len(test_x), batch):
        batch_x = torch.from_numpy(test_x[i:i+batch]).cuda()
        batch_x /= batch_x.norm(dim=-1, keepdim=True)
        dists = 1 - batch_x @ ref_x.T  # cosine distance
        topk_dists, topk_idx = dists.topk(k, largest=False)
        weights = 1.0 / (topk_dists ** power + 1e-8)
        weights /= weights.sum(dim=-1, keepdim=True)
        pred = (weights.unsqueeze(-1) * ref_y[topk_idx]).sum(dim=1)
        preds.append(pred.cpu().numpy())
    return np.concatenate(preds)
```

## Workflow

1. Extract CLIP embeddings for all reference images and their target embeddings
2. L2-normalize reference and test embeddings
3. Compute cosine distance via batched matrix multiply on GPU
4. For each test sample, find k nearest neighbors by distance
5. Compute inverse-distance weights with a power parameter for sharpness
6. Weighted-average the neighbors' target embeddings as the prediction

## Key Decisions

- **k (neighbors)**: 50-200; higher k smooths predictions, lower k captures local structure
- **distance power**: 4-8; higher values make predictions more local (closer neighbors dominate)
- **Batch size**: 500-2000 depending on GPU memory; trades memory for speed
- **Streaming merge**: for reference sets too large for GPU, process in chunks and merge top-k indices via argpartition
- **vs. linear probe**: k-NN needs no training and is competitive when reference set is large and diverse

## References

- [SDIP CLIP kNNRegression +CLIP+ViT](https://www.kaggle.com/code/lhllmlt/sdip-clip-knnregression-clip-vit)
