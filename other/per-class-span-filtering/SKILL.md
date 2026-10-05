---
name: nlp-per-class-span-filtering
description: >
  Filters predicted NER spans using per-class minimum word-count and mean-probability thresholds to reduce false positives.
---
# Per-Class Span Filtering

## Overview

NER models produce many short, low-confidence span predictions that are false positives. Different entity types have different natural lengths — an "Evidence" span should be at least 14 words, while a "Claim" can be as short as 3. Per-class filtering applies separate minimum length and confidence thresholds for each class, tuned on validation data. This simple post-processing step consistently improves F1 by 2-5 points.

## Quick Start

```python
import numpy as np

# Thresholds tuned on validation set
MIN_WORDS = {"Lead": 9, "Position": 5, "Evidence": 14,
             "Claim": 3, "Concluding Statement": 11,
             "Counterclaim": 6, "Rebuttal": 4}
MIN_PROBA = {"Lead": 0.70, "Position": 0.55, "Evidence": 0.65,
             "Claim": 0.55, "Concluding Statement": 0.70,
             "Counterclaim": 0.50, "Rebuttal": 0.55}

def filter_spans(predictions):
    """Filter spans by per-class length and probability thresholds.

    predictions: list of (doc_id, class, word_indices_str, mean_proba)
    """
    filtered = []
    for doc_id, cls, pred_str, proba in predictions:
        n_words = len(pred_str.split())
        if n_words >= MIN_WORDS.get(cls, 1) and proba >= MIN_PROBA.get(cls, 0.5):
            filtered.append((doc_id, cls, pred_str))
    return filtered
```

## Workflow

1. Generate raw span predictions with confidence scores
2. For each span, compute word count and mean token probability
3. Filter out spans below per-class minimum length
4. Filter out spans below per-class probability threshold
5. Tune thresholds on validation set (grid search or Optuna)

## Key Decisions

- **Threshold tuning**: Grid search over (length, proba) pairs per class on validation F1
- **Length vs probability**: Length filtering alone gives most of the gain; probability adds refinement
- **Class-specific**: One-size-fits-all thresholds lose 1-2 F1 points vs per-class
- **Order**: Apply length filter first (cheaper), then probability filter

## References

- [Two Longformers Are Better Than 1](https://www.kaggle.com/code/abhishek/two-longformers-are-better-than-1)
- [Infer Fast Ensemble Models](https://www.kaggle.com/code/librauee/infer-fast-ensemble-models)
