---
name: nlp-multisample-dropout
description: >
  Applies multiple dropout masks to the same hidden state and averages predictions for regularization and variance reduction.
---
# Multisample Dropout

## Overview

Instead of a single dropout mask, apply N different dropout masks to the pooled representation and average the resulting logits. During training this acts as stronger regularization; during inference it functions as a cheap ensemble of N sub-networks without N forward passes through the backbone.

## Quick Start

```python
import torch.nn as nn

class MultisampleDropoutHead(nn.Module):
    def __init__(self, hidden_size, n_dropouts=5, drop_rate=0.3):
        super().__init__()
        self.dropouts = nn.ModuleList([nn.Dropout(drop_rate) for _ in range(n_dropouts)])
        self.regressor = nn.Linear(hidden_size, 1)

    def forward(self, hidden_state):
        logits = None
        for i, dropout in enumerate(self.dropouts):
            out = self.regressor(dropout(hidden_state))
            logits = out if logits is None else logits + out
        return logits / len(self.dropouts)
```

## Workflow

1. Replace single dropout + linear head with MultisampleDropoutHead
2. Each forward pass applies N different random masks
3. Average the N outputs to get the final prediction
4. Loss is computed on the averaged output

## Key Decisions

- **N dropouts**: 5 is standard; diminishing returns past 8
- **Drop rate**: 0.1-0.5; higher rates need more samples to stabilize
- **Training vs inference**: Works in both; at eval, dropout is still active
- **Cost**: ~Nx the head computation, but head is tiny vs backbone — negligible

## References

- CommonLit Readability Prize (Kaggle)
- Source: [commonlit-two-models](https://www.kaggle.com/code/andretugan/commonlit-two-models)
