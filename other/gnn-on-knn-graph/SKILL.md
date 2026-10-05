---
name: tabular-gnn-on-knn-graph
description: >
  Constructs a customer similarity graph via KNN on mixed features, then trains a GraphSAGE GNN for node classification. Captures relational patterns that tree and linear models miss, adding ensemble diversity.
---

# GNN on KNN Graph

## Overview

Build a K-nearest-neighbor similarity graph from tabular features, then train a GraphSAGE GNN for node classification. Each row becomes a node; edges connect similar rows based on OHE categorical + scaled numerical distances. The GNN aggregates neighbor embeddings across hops, learning relational patterns invisible to pointwise models. Valuable in ensembles even at slightly lower solo AUC due to high prediction diversity.

## Quick Start

```python
import torch
from torch_geometric.nn import SAGEConv
from torch_geometric.loader import NeighborLoader
from cuml.neighbors import NearestNeighbors
from sklearn.preprocessing import OneHotEncoder, StandardScaler
import numpy as np

# 1. Build graph edges via KNN
ohe = OneHotEncoder(sparse_output=False).fit_transform(X_cat)
num = StandardScaler().fit_transform(X_num) * 3.0  # multiplier for numerics
features = np.hstack([ohe, num]).astype("float32")
knn = NearestNeighbors(n_neighbors=8).fit(features)
_, indices = knn.kneighbors(features)
src = np.repeat(np.arange(len(features)), 8)
dst = indices.flatten()
edge_index = torch.tensor(np.stack([src, dst]), dtype=torch.long)

# 2. Node features: categorical embeddings + scaled numerics (25-dim)
# (CatEmbed layer maps each categorical to a learned embedding)

# 3. Mini-batch training with subgraph sampling
loader = NeighborLoader(data, num_neighbors=[6, 4], batch_size=512)
for batch in loader:
    out = model(batch.x, batch.edge_index)
    loss = F.binary_cross_entropy_with_logits(out, batch.y, label_smoothing=0.01)
```

## Workflow

1. **Encode features for KNN**: OHE categoricals + StandardScaler numerics (multiply numerics by 3.0 to balance distance contribution).
2. **Build KNN graph**: cuML `NearestNeighbors(k=8)` on encoded features. Convert neighbor indices to `edge_index`.
3. **Prepare node features**: Categorical embedding layers (22 features) + scaled numerics (3 features) = 25-dim input per node.
4. **Define model**: `CatEmbed → Linear → SAGEConv → LayerNorm → SAGEConv → LayerNorm → MLP head`. Residual connections with 0.5 scaling: `x = x + 0.5 * conv(x)`.
5. **Train with mini-batches**: `NeighborLoader` with fanouts `[6, 4]`. Label-smoothed BCE loss (eps=0.01).
6. **Predict**: Full-batch or batched inference. Use sigmoid outputs for ensemble blending.

## Key Decisions

| Decision | Guidance |
|---|---|
| K in KNN | k=8 balances graph density vs noise. Too high adds weak edges. |
| Numeric multiplier | 3.0 gives numerics comparable influence to OHE block in distance. Tune per dataset. |
| Fanouts | `[6, 4]` keeps mini-batch subgraphs tractable. Larger fanouts cost memory. |
| Residual scaling | 0.5 prevents over-smoothing across hops. |
| Label smoothing | eps=0.01 regularizes against noisy labels in synthetic/competition data. |
| GPU KNN | cuML drastically speeds KNN on large datasets. Fall back to sklearn if no GPU. |
| Ensemble role | GNN predictions are structurally diverse from GBDT/linear. Blend even if solo AUC is 1-2% lower. |

## References

- Kaggle: "GNN Starter [CV 0.9155] with Hill Climbing Demo" (playground-series-s6e3)
- Hamilton et al. "Inductive Representation Learning on Large Graphs" (NeurIPS 2017) — GraphSAGE
