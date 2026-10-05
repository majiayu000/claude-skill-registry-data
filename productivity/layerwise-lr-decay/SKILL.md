---
name: nlp-layerwise-lr-decay
description: >
  Applies different learning rates to transformer encoder vs task-specific head, with no weight decay on bias and LayerNorm.
---
# Layer-wise Learning Rate Decay

## Overview

Pretrained transformer layers need gentle updates to preserve knowledge, while the randomly initialized task head needs aggressive learning. Use a lower learning rate for the encoder and a higher one for the decoder/head. Exclude bias and LayerNorm parameters from weight decay to prevent underfitting.

## Quick Start

```python
def get_optimizer_params(model, encoder_lr=2e-5, decoder_lr=1e-3, weight_decay=0.01):
    no_decay = ["bias", "LayerNorm.bias", "LayerNorm.weight"]
    params = [
        {"params": [p for n, p in model.model.named_parameters()
                     if not any(nd in n for nd in no_decay)],
         "lr": encoder_lr, "weight_decay": weight_decay},
        {"params": [p for n, p in model.model.named_parameters()
                     if any(nd in n for nd in no_decay)],
         "lr": encoder_lr, "weight_decay": 0.0},
        {"params": [p for n, p in model.named_parameters()
                     if "model" not in n],
         "lr": decoder_lr, "weight_decay": 0.0},
    ]
    return params
```

## Workflow

1. Split parameters into encoder (pretrained) and decoder (new head) groups
2. Within encoder, separate decay and no-decay parameters
3. Assign lower LR to encoder (~2e-5), higher to decoder (~1e-3)
4. Pass parameter groups to AdamW optimizer

## Key Decisions

- **LR ratio**: Typically 10-100x between head and encoder
- **No decay on bias/LayerNorm**: Standard practice; prevents regularizing normalization params
- **Per-layer decay**: For deeper control, multiply LR by 0.95^(N-layer) from top to bottom

## References

- Feedback Prize - English Language Learning (Kaggle)
- Source: [fb3-deberta-v3-base-baseline-train](https://www.kaggle.com/code/yasufuminakama/fb3-deberta-v3-base-baseline-train)
