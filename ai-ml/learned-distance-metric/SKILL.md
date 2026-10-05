---
name: cv-learned-distance-metric
description: Trainable nonlinear distance metric that transforms (v1-v2) and (v1-v2)^2 through a linear layer before computing squared norm
---

# Learned Distance Metric

## Overview

Euclidean and cosine distances treat all embedding dimensions equally. A learned distance metric passes the difference vector and its element-wise square through a linear transformation, then computes the squared norm. This approximates a Mahalanobis-like distance but with nonlinear capacity from the squared terms, learning which dimensions and interactions matter for similarity.

## Quick Start

```python
import torch
import torch.nn as nn

class LearnedMetric(nn.Module):
    def __init__(self, emb_dim=64):
        super().__init__()
        self.linear = nn.Linear(emb_dim * 2, emb_dim * 2, bias=False)

    def forward(self, v1, v2):
        d = v1 - v2
        d2 = d.pow(2)
        x = self.linear(torch.cat([d, d2], dim=-1))
        return x.pow(2).sum(dim=-1)

metric = LearnedMetric(emb_dim=128)
dist = metric(embedding_a, embedding_b)
```

## Workflow

1. Train embedding model with a fixed or learned metric
2. Initialize `LearnedMetric` matching embedding dimension
3. Train jointly with contrastive or triplet loss
4. At inference, use the learned metric for nearest-neighbor retrieval

## Key Decisions

- **No bias**: bias-free linear keeps distance symmetric and zero for identical inputs
- **Concat [d, d^2]**: captures both linear (Mahalanobis-like) and nonlinear distance components
- **Joint training**: train metric alongside the embedding model end-to-end
- **vs Mahalanobis**: Mahalanobis is linear-only; this adds nonlinear capacity with minimal parameters

## References

- [Similarity DenseNet121 [0.805LB]](https://www.kaggle.com/code/iafoss/similarity-densenet121-0-805lb-kernel-time-limit)
