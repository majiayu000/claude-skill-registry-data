---
name: nlp-mean-max-concat-pooling
description: >
  Concatenates token-level mean pooling and max pooling from the last hidden state for a richer sequence representation.
---
# Mean-Max Concat Pooling

## Overview

Mean pooling captures the average semantic content; max pooling highlights the most salient features. Concatenating both gives a representation that is both smooth (mean) and discriminative (max). This 2x-width vector feeds into the classification head, often outperforming either pooling strategy alone.

## Quick Start

```python
import torch
import torch.nn as nn

class MeanMaxPooling(nn.Module):
    def forward(self, last_hidden_state, attention_mask):
        # Mean pooling (mask-aware)
        mask = attention_mask.unsqueeze(-1).float()
        mean_pool = (last_hidden_state * mask).sum(dim=1) / mask.sum(dim=1).clamp(min=1e-9)

        # Max pooling (mask -inf for padding)
        masked = last_hidden_state.masked_fill(~attention_mask.unsqueeze(-1).bool(), -1e9)
        max_pool, _ = masked.max(dim=1)

        return torch.cat([mean_pool, max_pool], dim=1)  # (batch, 2 * hidden_size)

# Usage:
outputs = model(input_ids, attention_mask=attention_mask)
pooled = mean_max_pool(outputs.last_hidden_state, attention_mask)
logits = nn.Linear(config.hidden_size * 2, num_classes)(pooled)
```

## Workflow

1. Get `last_hidden_state` from transformer (batch, seq_len, hidden_size)
2. Compute mean pooling with attention mask (exclude padding tokens)
3. Compute max pooling with padding masked to -inf
4. Concatenate along feature dimension → (batch, 2 * hidden_size)
5. Adjust classifier head input dimension to `hidden_size * 2`

## Key Decisions

- **vs CLS token**: Mean-max captures full sequence information; CLS may miss tail tokens
- **vs mean-only**: Max pooling adds discriminative power for rare but important tokens
- **Head size**: Double the input dimension of the classifier head
- **Combine with**: Attention pooling or weighted-layer-pooling for further gains

## References

- [feedback_deberta_large_LB0.619](https://www.kaggle.com/code/brandonhu0215/feedback-deberta-large-lb0-619)
