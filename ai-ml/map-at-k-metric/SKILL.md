---
name: nlp-map-at-k-metric
description: Custom MAP@K evaluation metric — scores top-K classification predictions with reciprocal rank weighting for HuggingFace Trainer
domain: nlp
---

# MAP@K Metric

## Overview

Mean Average Precision at K (MAP@K) scores multi-class predictions by checking if the true label appears in the top-K predictions. The score is 1/rank if found (1.0 for rank 1, 0.5 for rank 2, etc.), 0 if not in top-K. Averages across all samples. Standard metric for classification-as-ranking tasks.

## Quick Start

```python
import numpy as np
import torch

def compute_map_at_k(eval_pred, k=3):
    """MAP@K metric compatible with HuggingFace Trainer.
    
    Args:
        eval_pred: (logits, labels) tuple from Trainer
        k: number of top predictions to consider
    """
    logits, labels = eval_pred
    probs = torch.nn.functional.softmax(
        torch.tensor(logits, dtype=torch.float32), dim=-1
    ).numpy()
    top_k = np.argsort(-probs, axis=1)[:, :k]
    
    score = 0.0
    for i in range(len(labels)):
        matches = np.where(top_k[i] == labels[i])[0]
        if len(matches) > 0:
            score += 1.0 / (matches[0] + 1)  # reciprocal rank
    return {f"map@{k}": score / len(labels)}

# Usage with HuggingFace Trainer
trainer = Trainer(
    model=model,
    args=training_args,
    compute_metrics=lambda ep: compute_map_at_k(ep, k=3),
)
```

## Key Decisions

- **K=3**: common in Kaggle; adjust to match competition metric
- **Softmax before argsort**: converts logits to probabilities for proper ranking
- **Single-label only**: each sample has one true label; for multi-label, use per-label AP
- **metric_for_best_model**: set to "map@3" with greater_is_better=True for checkpointing

## References

- Source: [gemma2-9b-it-cv-0-945](https://www.kaggle.com/code/cdeotte/gemma2-9b-it-cv-0-945)
- Competition: MAP - Charting Student Math Misunderstandings
