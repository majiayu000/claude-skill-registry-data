---
name: cv-map-iou-precision-sweep
description: Compute mean Average Precision by sweeping IoU thresholds from 0.5 to 0.95 on RLE-encoded instance masks using pycocotools
---

# mAP IoU Precision Sweep

## Overview

The standard COCO-style mAP for instance segmentation averages precision across IoU thresholds [0.5, 0.55, ..., 0.95]. This implementation uses pycocotools `mask_util.iou` for fast RLE-based IoU computation, then sweeps thresholds to compute TP/FP/FN counts and average precision. Essential for offline evaluation of Mask R-CNN, Detectron2, or MMDetection outputs.

## Quick Start

```python
import numpy as np
from pycocotools import mask as mask_util

def precision_at(threshold, iou_matrix):
    matches = iou_matrix > threshold
    tp = np.sum(np.sum(matches, axis=1) == 1)
    fp = np.sum(np.sum(matches, axis=0) == 0)
    fn = np.sum(np.sum(matches, axis=1) == 0)
    return tp, fp, fn

def compute_map(pred_masks, gt_masks):
    enc_preds = [mask_util.encode(np.asfortranarray(m)) for m in pred_masks]
    enc_gts = [mask_util.encode(np.asfortranarray(m)) for m in gt_masks]
    ious = mask_util.iou(enc_preds, enc_gts, [0] * len(enc_gts))
    precisions = []
    for t in np.arange(0.5, 1.0, 0.05):
        tp, fp, fn = precision_at(t, ious)
        precisions.append(tp / (tp + fp + fn) if (tp + fp + fn) > 0 else 0)
    return np.mean(precisions)
```

## Workflow

1. Encode predicted and ground-truth binary masks as RLE using `mask_util.encode`
2. Compute the full IoU matrix with `mask_util.iou` (fast C implementation)
3. For each threshold in [0.5, 0.55, ..., 0.95], count TP/FP/FN
4. Compute precision per threshold, then average across all 10 thresholds

## Key Decisions

- **RLE encoding**: `np.asfortranarray` is required — pycocotools expects Fortran-order arrays
- **One-to-one matching**: each pred matches at most one GT (sum axis check == 1)
- **Empty predictions**: return 0 if no predictions; missing this causes division errors
- **Integration**: wrap in a Detectron2 `DatasetEvaluator` for periodic validation during training

## References

- [Positive score with Detectron 2/3 - Training](https://www.kaggle.com/code/slawekbiel/positive-score-with-detectron-2-3-training)
- [Sartorius Segmentation - Detectron2 [Training]](https://www.kaggle.com/code/ammarnassanalhajali/sartorius-segmentation-detectron2-training)
