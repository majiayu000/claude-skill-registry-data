---
name: cv-open-set-distance-cutoff
description: Assign an unknown/novel class when all nearest-neighbor distances exceed a tuned cutoff threshold for open-set recognition
---

# Open-Set Distance Cutoff

## Overview

In open-set recognition, test images may belong to classes not seen during training (e.g., "new_whale"). After retrieving k nearest neighbors by embedding distance, if all distances exceed a learned cutoff, insert the unknown class into the prediction list. The cutoff is tuned on a validation set to maximize the ranking metric (e.g., MAP@5).

## Quick Start

```python
import numpy as np

def predict_with_unknown(query_dists, query_nbs, train_labels,
                         unknown_label='new_whale', dcut=3.8, top_k=5):
    predictions = []
    for i in range(len(query_dists)):
        seen = {}
        for j in range(query_nbs.shape[1]):
            label = train_labels[query_nbs[i, j]]
            dist = query_dists[i, j]
            if dist > dcut and unknown_label not in seen:
                seen[unknown_label] = dcut
            if label not in seen:
                seen[label] = dist
            if len(seen) >= top_k:
                break
        preds = sorted(seen.items(), key=lambda x: x[1])[:top_k]
        predictions.append([p[0] for p in preds])
    return predictions
```

## Workflow

1. Compute embeddings for train and test sets
2. Find k nearest neighbors for each test sample
3. For each test query, iterate neighbors by distance
4. Insert unknown class when distance exceeds cutoff `dcut`
5. Tune `dcut` on validation set to maximize MAP@k or accuracy

## Key Decisions

- **Cutoff tuning**: sweep `dcut` values on validation set; optimal value depends on embedding space scale
- **Insertion point**: unknown class enters at the position where distance first exceeds cutoff
- **Distance metric**: Euclidean on L2-normalized embeddings ≈ cosine distance
- **When to use**: any retrieval task where query may not match any gallery class

## References

- [Similarity DenseNet121 [0.805LB]](https://www.kaggle.com/code/iafoss/similarity-densenet121-0-805lb-kernel-time-limit)
