---
name: nlp-span-overlap-f1-metric
description: >
  Evaluates NER span predictions using bidirectional word-index overlap (>=50% both ways) to compute micro-F1 over predicted vs ground-truth spans.
---
# Span Overlap F1 Metric

## Overview

Standard NER metrics require exact span matches, which is too strict for discourse-level or paragraph-level span prediction. Span overlap F1 relaxes this: a predicted span is a true positive if it overlaps >=50% of the ground truth AND the ground truth overlaps >=50% of the prediction (bidirectional). This penalizes both under-segmentation and over-segmentation while tolerating minor boundary errors.

## Quick Start

```python
import pandas as pd

def span_overlap_f1(gt_df, pred_df):
    """Compute micro-F1 using bidirectional word overlap.

    gt_df/pred_df: columns [id, class, predictionstring]
    predictionstring: space-separated word indices (e.g., "3 4 5 6 7")
    """
    joined = gt_df.merge(pred_df, on=["id", "class"], suffixes=("_gt", "_pred"))

    def calc_overlap(row):
        s_pred = set(row["predictionstring_pred"].split())
        s_gt = set(row["predictionstring_gt"].split())
        inter = len(s_gt & s_pred)
        return inter / len(s_gt), inter / len(s_pred)

    joined[["overlap_gt", "overlap_pred"]] = joined.apply(
        calc_overlap, axis=1, result_type="expand"
    )
    joined["tp"] = (joined["overlap_gt"] >= 0.5) & (joined["overlap_pred"] >= 0.5)

    # Greedy matching: best overlap first, one-to-one
    tp_ids = (joined[joined["tp"]]
              .sort_values("overlap_gt", ascending=False)
              .drop_duplicates("predictionstring_gt")
              .drop_duplicates("predictionstring_pred"))

    TP = len(tp_ids)
    FP = len(pred_df) - TP
    FN = len(gt_df) - TP
    return TP / (TP + 0.5 * (FP + FN)) if (TP + FP + FN) > 0 else 0.0
```

## Workflow

1. Join predictions to ground truth on document ID and class label
2. Compute bidirectional overlap ratios for each (gt, pred) pair
3. Mark as TP if both overlaps >= 0.5
4. Greedy one-to-one matching (best overlap first) to avoid double-counting
5. Compute micro-F1: TP / (TP + 0.5*(FP+FN))

## Key Decisions

- **Overlap threshold**: 0.5 is standard; lower for lenient evaluation
- **Greedy matching**: Sort by overlap descending, deduplicate to enforce one-to-one
- **Per-class vs micro**: Compute per-class then macro-average, or pool all spans for micro

## References

- [TensorFlow LongFormer NER CV 0.633](https://www.kaggle.com/code/cdeotte/tensorflow-longformer-ner-cv-0-633)
- [PyTorch BigBird NER CV 0.615](https://www.kaggle.com/code/cdeotte/pytorch-bigbird-ner-cv-0-615)
