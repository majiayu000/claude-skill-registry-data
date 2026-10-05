---
name: nlp-attention-head-pooling
description: >
  Learns attention weights over token positions to compute a weighted average of hidden states for sequence representation.
---
# Attention Head Pooling

## Overview

Instead of CLS token or mean pooling, add a learnable attention layer that scores each token position and computes a weighted sum. This lets the model focus on the most informative tokens in the sequence — e.g., complex vocabulary in readability tasks or key entities in classification.

## Quick Start

```python
import torch
import torch.nn as nn

class AttentionPooling(nn.Module):
    def __init__(self, hidden_size):
        super().__init__()
        self.attention = nn.Sequential(
            nn.Linear(hidden_size, hidden_size),
            nn.Tanh(),
            nn.Linear(hidden_size, 1),
        )

    def forward(self, hidden_states, attention_mask=None):
        # hidden_states: (B, S, H)
        weights = self.attention(hidden_states).squeeze(-1)  # (B, S)
        if attention_mask is not None:
            weights = weights.masked_fill(attention_mask == 0, -1e9)
        weights = torch.softmax(weights, dim=1)  # (B, S)
        return torch.sum(hidden_states * weights.unsqueeze(-1), dim=1)  # (B, H)
```

## Workflow

1. Get full sequence hidden states from transformer (not just CLS)
2. Apply learned attention layer to score each token
3. Mask padding positions before softmax
4. Compute weighted sum as the sequence representation
5. Feed into regression/classification head

## Key Decisions

- **vs mean pooling**: Attention pooling learns which tokens matter; mean treats all equally
- **vs CLS**: CLS depends on pre-training; attention adapts to your task
- **Architecture**: Tanh + linear is standard; single linear also works
- **Combine**: Concatenate attention-pooled + mean-pooled for best results

## References

- CommonLit Readability Prize (Kaggle)
- Source: [commonlit-two-models](https://www.kaggle.com/code/andretugan/commonlit-two-models)
