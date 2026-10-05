---
name: cv-iou-threshold-sweep
description: Grid search binarization thresholds on validation predictions to find the cutoff that maximizes mean IoU
---

## Overview

Segmentation models output continuous probability maps but metrics require binary masks. The default 0.5 threshold is often suboptimal — shifting it can improve IoU by several points with zero cost. This technique sweeps a dense grid of thresholds over the validation set, measures mean IoU at each, and picks the best one as the final binarization cutoff.

## Quick Start

```python
import numpy as np

def iou_metric_batch(y_true, y_pred_binary):
    batch = y_true.shape[0]
    return np.mean([iou_metric(y_true[i], y_pred_binary[i]) for i in range(batch)])

# Sweep thresholds
thresholds = np.linspace(0.2, 0.9, 31)
ious = np.array([
    iou_metric_batch(y_valid, (preds_valid > t).astype(np.int32))
    for t in thresholds
])
best_idx = np.argmax(ious)
best_threshold = thresholds[best_idx]
best_iou = ious[best_idx]

print(f"Best threshold: {best_threshold:.3f} → IoU: {best_iou:.4f}")
```

## Workflow

1. Generate continuous predictions on the validation set
2. Define a threshold grid — linspace(0.2, 0.9, 31) works for most tasks
3. For each threshold, binarize and compute mean IoU
4. Pick the argmax threshold and apply it at test time
5. Optional: also compute the best threshold per fold and average them

## Key Decisions

- **Grid resolution**: 31 points is usually enough. Finer grids rarely change the answer.
- **Grid range**: (0.2, 0.9) covers most cases. Extend to (0.05, 0.95) if predictions are very peaked.
- **Per-fold vs global**: Per-fold thresholds capture calibration differences but risk overfitting — average them for the final submission.
- **vs. fixed 0.5**: Almost always better. A properly tuned threshold routinely adds 1-3 IoU points.

## References

- [Nested Unet with EfficientNet Encoder](https://www.kaggle.com/code/meaninglesslives/nested-unet-with-efficientnet-encoder)
