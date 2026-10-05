---
name: cv-min-area-mask-filtering
description: >
  Removes predicted segmentation masks below a per-class minimum pixel area threshold to eliminate small false positive regions at inference time.
---
# Min-Area Mask Filtering

## Overview

Segmentation models often produce small spurious predictions — isolated pixel clusters that score above the confidence threshold but are too small to be real objects. Min-area filtering applies a per-class pixel count threshold: after binarizing the predicted mask, any connected component (or entire class mask) with fewer pixels than the threshold is zeroed out. This simple post-processing step typically improves Dice/IoU by 0.5-2% by eliminating false positives, especially in defect detection and medical imaging where true objects have known minimum sizes.

## Quick Start

```python
import numpy as np

def filter_small_masks(pred_masks, min_areas, thresholds):
    """Filter masks below per-class minimum area.

    Args:
        pred_masks: (H, W, C) float array of predicted probabilities
        min_areas: list of minimum pixel counts per class
        thresholds: list of binarization thresholds per class
    Returns:
        Filtered binary masks (H, W, C)
    """
    filtered = np.zeros_like(pred_masks, dtype=np.uint8)
    for c in range(pred_masks.shape[-1]):
        mask = (pred_masks[:, :, c] > thresholds[c]).astype(np.uint8)
        if mask.sum() < min_areas[c]:
            mask = np.zeros_like(mask)
        filtered[:, :, c] = mask
    return filtered

# Per-class thresholds and min areas (tune on validation)
thresholds = [0.5, 0.5, 0.5, 0.5]
min_areas = [600, 600, 1000, 2000]
clean_masks = filter_small_masks(raw_preds, min_areas, thresholds)
```

## Workflow

1. Binarize predicted probabilities with per-class confidence thresholds
2. Count positive pixels per class
3. Zero out any class mask with fewer pixels than its minimum area
4. Encode cleaned masks for submission (e.g., RLE)

## Key Decisions

- **Per-class thresholds**: Different defect types have different minimum sizes — tune each independently
- **Min area values**: Derive from training set statistics (smallest real annotation area)
- **Connected components**: For finer control, filter individual connected components instead of the whole mask
- **Threshold search**: Grid-search both confidence threshold and min-area on validation Dice/IoU

## References

- [Severstal mlcomp+catalyst Inference](https://www.kaggle.com/code/lightforever/severstal-mlcomp-catalyst-infer-0-90672)
