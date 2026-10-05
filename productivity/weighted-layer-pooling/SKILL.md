---
name: nlp-weighted-layer-pooling
description: >
  Learns a weighted combination of CLS embeddings across all transformer layers instead of using only the last layer.
---
# Weighted Layer Pooling

## Overview

Different transformer layers capture different linguistic features — lower layers for syntax, higher for semantics. Instead of using only the final layer, weighted layer pooling learns a soft weight per layer and computes a weighted mean. This typically improves regression tasks where multiple levels of language understanding matter.

## Quick Start

```python
import torch
import torch.nn as nn

class WeightedLayerPooling(nn.Module):
    def __init__(self, num_hidden_layers, layer_start=4):
        super().__init__()
        self.layer_start = layer_start
        self.num_layers = num_hidden_layers - layer_start + 1
        self.layer_weights = nn.Parameter(torch.ones(self.num_layers))

    def forward(self, all_hidden_states):
        layers = torch.stack(all_hidden_states[self.layer_start:])  # (L, B, S, H)
        weights = self.layer_weights.unsqueeze(-1).unsqueeze(-1).unsqueeze(-1)
        weights = weights.expand(layers.size())
        weighted = (weights * layers).sum(dim=0) / self.layer_weights.sum()
        return weighted[:, 0]  # CLS token
```

## Workflow

1. Set `output_hidden_states=True` in model config
2. Collect all hidden states from the transformer
3. Apply learnable weights across selected layers
4. Use weighted output as input to regression/classification head

## Key Decisions

- **layer_start**: Skip early layers (0-3) which capture low-level token features
- **Initialization**: Start with uniform weights; the model learns the optimal mix
- **Alternatives**: Concatenation (4x hidden size) or LSTM pooling (more params)

## References

- Feedback Prize - English Language Learning (Kaggle)
- Source: [utilizing-transformer-representations-efficiently](https://www.kaggle.com/code/rhtsingh/utilizing-transformer-representations-efficiently)
