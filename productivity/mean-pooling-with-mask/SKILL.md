---
name: nlp-mean-pooling-with-mask
description: >
  Computes attention-mask-weighted mean of token embeddings, excluding padding tokens from the average.
---
# Mean Pooling with Attention Mask

## Overview

Instead of using the CLS token or naive mean, mask-aware mean pooling averages only the real token embeddings by weighting with the attention mask. This prevents padding tokens from diluting the representation, especially important for variable-length inputs.

## Quick Start

```python
import torch
import torch.nn as nn

class MeanPooling(nn.Module):
    def forward(self, last_hidden_state, attention_mask):
        mask = attention_mask.unsqueeze(-1).expand(last_hidden_state.size()).float()
        sum_embeddings = torch.sum(last_hidden_state * mask, dim=1)
        sum_mask = torch.clamp(mask.sum(dim=1), min=1e-9)
        return sum_embeddings / sum_mask
```

## Workflow

1. Get `last_hidden_state` from transformer (shape: B x S x H)
2. Expand attention mask to match hidden state dimensions
3. Multiply hidden states by mask, sum along sequence dimension
4. Divide by sum of mask values (count of real tokens)

## Key Decisions

- **Clamp min=1e-9**: Prevents division by zero for empty sequences
- **vs CLS token**: Mean pooling captures more context; CLS can be undertrained
- **vs max pooling**: Mean is smoother; max captures salient features. Concatenate both for best results
- **Normalization**: Optionally L2-normalize output for cosine similarity tasks

## References

- Feedback Prize - English Language Learning (Kaggle)
- Source: [fb3-deberta-v3-base-baseline-train](https://www.kaggle.com/code/yasufuminakama/fb3-deberta-v3-base-baseline-train)
