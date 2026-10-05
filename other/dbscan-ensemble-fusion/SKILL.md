---
name: cv-dbscan-ensemble-fusion
description: >
  Fuses 3D object detections from multiple models by clustering nearby predictions with DBSCAN and taking cluster centroids.
---
# DBSCAN Ensemble Fusion

## Overview

When multiple detection models produce overlapping 3D point predictions, fuse them by clustering nearby detections with DBSCAN. Each cluster's centroid becomes a single fused detection. Unlike NMS which needs box IoU, DBSCAN works directly on point coordinates — ideal for particle picking, cell detection, and any centroid-based 3D detection.

## Quick Start

```python
from sklearn.cluster import DBSCAN
import numpy as np

def fuse_detections(all_preds, eps=10.0, min_samples=2):
    """Fuse detections from multiple models.
    all_preds: list of arrays, each (N_i, 3) in (z, y, x) coords.
    """
    coords = np.vstack(all_preds)
    if len(coords) == 0:
        return np.empty((0, 3))
    clustering = DBSCAN(eps=eps, min_samples=min_samples).fit(coords)
    centroids = []
    for label in set(clustering.labels_):
        if label == -1:  # noise — include as single detections
            noise_pts = coords[clustering.labels_ == label]
            centroids.extend(noise_pts)
        else:
            cluster_pts = coords[clustering.labels_ == label]
            centroids.append(cluster_pts.mean(axis=0))
    return np.array(centroids)
```

## Workflow

1. Collect (z, y, x) predictions from each model
2. Concatenate all predictions into one array
3. Run DBSCAN with `eps` = expected merge radius, `min_samples` = minimum agreement count
4. Compute centroid per cluster; optionally discard noise points (single-model detections)
5. Output fused detection coordinates

## Key Decisions

- **eps**: Set to expected particle radius or localization error; too large merges distinct objects
- **min_samples**: 2 = fuse if any two models agree; higher = stricter consensus filter
- **Noise handling**: Keep noise points for recall; discard for precision
- **Per-class fusion**: Run DBSCAN separately per class to prevent cross-class merging
- **Weighted centroids**: Weight by model confidence if available

## References

- [CZII YOLO11+Unet3D-Monai LB.707](https://www.kaggle.com/code/hideyukizushi/czii-yolo11-unet3d-monai-lb-707)
