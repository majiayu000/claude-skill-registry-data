---
name: nlp-char-prob-weighted-blend
description: Blend character-level probability arrays from multiple models with OOF-tuned weights before thresholding
domain: nlp
---

# Character-Probability Weighted Blend

## Overview

For span extraction tasks, ensemble at the character-probability level rather than at the span level. Each model produces char-level probability arrays; blend them with scalar weights tuned on OOF predictions, then threshold once. This is smoother and more accurate than ensembling discrete spans.

## Quick Start

```python
import numpy as np

def blend_char_probs(model_probs, weights):
    """Weighted blend of char-level probability arrays from multiple models.

    Args:
        model_probs: list of [n_samples] arrays, each element is char-prob array
        weights: list of floats, one per model
    """
    blended = []
    for sample_probs in zip(*model_probs):
        combined = sum(w * p for w, p in zip(weights, sample_probs))
        blended.append(combined)
    return blended

# Example: 3-model blend
weights = [0.5, 0.4, 0.18]  # tuned on OOF
blended = blend_char_probs(
    [deberta_v3_probs, deberta_v1_probs, deberta_base_probs],
    weights
)
spans = get_spans(blended, threshold=0.5)
```

## Key Decisions

- **Char-level, not span-level**: blending probabilities before thresholding preserves soft information; majority-voting on spans loses boundary precision
- **Weights don't sum to 1**: combined values can exceed 1.0 — that's fine, threshold still works
- **OOF tuning**: optimize weights on out-of-fold char probs using grid search or scipy.optimize
- **Fold averaging first**: each model should average its own fold predictions before cross-model blending

## Workflow

1. For each model: run inference per fold → average char probs across folds
2. Tune blend weights on OOF char probs (maximize span-level F1)
3. Apply weights to test char probs
4. Threshold blended probs → extract spans

## References

- Source: [nbme-ensemble-debertas](https://www.kaggle.com/code/motloch/nbme-ensemble-debertas)
- Competition: NBME - Score Clinical Patient Notes
