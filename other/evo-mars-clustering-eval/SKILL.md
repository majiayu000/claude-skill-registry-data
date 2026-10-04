---
name: evo-mars-clustering-eval
description: Core clustering and evaluation utilities for Mars cloud annotations. Custom weighted Euclidean DBSCAN clustering, centroid computation, greedy bipartite matching, and per-image F1/delta scoring.
---

# evo-mars-clustering-eval

Core clustering and evaluation utilities for DBSCAN-based Mars cloud annotation clustering.

## Key Functions

- `weighted_euclidean_pairwise(u, v, w)` - Custom distance: sqrt((w*dx)^2 + ((2-w)*dy)^2)
- `compute_precomputed_distance_matrix(X, w)` - Build precomputed distance matrix for DBSCAN
- `run_dbscan_and_get_centroids(X, eps, min_samples, dist_matrix)` - Run DBSCAN, return centroids
- `greedy_match(centroids, ground_truth, threshold=100.0)` - Greedy bipartite matching
- `score_image(citsci_points, expert_points, eps, min_samples, w)` - Full per-image scoring

## Usage

```python
import sys
sys.path.insert(0, '/app/environment/skills/evo-mars-clustering-eval/scripts')
from utils import score_image, greedy_match, run_dbscan_and_get_centroids

f1, delta = score_image(citsci_xy, expert_xy, eps=10, min_samples=5, w=1.0)
```

## Domain Rules

- DBSCAN uses precomputed distance matrix with custom weighted Euclidean metric
- Greedy matching uses standard Euclidean distance (not custom), max threshold 100px
- F1 = 2*TP / (2*TP + FP + FN), handles edge cases (both empty = 1.0)
- Delta = mean standard Euclidean distance of matched pairs, NaN if no matches
- Noise points (label -1) are excluded from centroid computation
