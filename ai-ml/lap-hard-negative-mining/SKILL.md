---
name: cv-lap-hard-negative-mining
description: Use linear assignment problem (LAP/lapjv) on a score matrix to select globally optimal hard-negative pairs for metric learning
---

# LAP Hard Negative Mining

## Overview

In metric learning, hard negatives (close but different-class examples) drive the most learning. Random negatives are too easy; per-anchor hardest negatives cause collapse. LAP (linear assignment problem) via the Jonker-Volgenant algorithm finds a globally optimal one-to-one assignment that maximizes overall difficulty across the entire batch, avoiding degenerate pairings.

## Quick Start

```python
import numpy as np
from lap import lapjv

def mine_hard_negatives(score_matrix, labels, t2i):
    cost = -score_matrix.copy()
    # Block same-class pairs with high cost
    for cls_indices in labels.values():
        idxs = [t2i[t] for t in cls_indices]
        for i in idxs:
            for j in idxs:
                cost[i, j] = 10000.0

    _, _, col_assignment = lapjv(cost)
    hard_pairs = []
    for j, i in enumerate(col_assignment):
        hard_pairs.append((i, j))
        cost[i, j] = 10000.0
        cost[j, i] = 10000.0
    return hard_pairs
```

## Workflow

1. Compute pairwise similarity/score matrix from current embeddings
2. Mask same-class pairs with large cost to prevent them being selected
3. Run `lapjv` to find optimal one-to-one hard negative assignment
4. Use assigned pairs for contrastive/siamese training
5. Recompute assignments periodically as embeddings evolve

## Key Decisions

- **LAP vs random**: LAP finds globally hard negatives; random wastes training on easy pairs
- **LAP vs per-anchor hardest**: per-anchor can cause model collapse; LAP distributes difficulty
- **Recompute frequency**: every epoch or every N batches — stale assignments degrade quality
- **`lap` package**: `pip install lap` for fast C++ Jonker-Volgenant solver

## References

- [Siamese (pretrained) 0.822](https://www.kaggle.com/code/seesee/siamese-pretrained-0-822)
