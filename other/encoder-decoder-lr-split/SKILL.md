---
name: nlp-encoder-decoder-lr-split
description: Use separate learning rates for pretrained backbone (low) and randomly initialized classification head (high)
domain: nlp
---

# Encoder-Decoder Learning Rate Split

## Overview

Pretrained transformer backbones need a lower learning rate to avoid catastrophic forgetting, while the randomly initialized classification head needs a higher learning rate to converge quickly. Split optimizer param groups into encoder vs decoder with different LRs.

## Quick Start

```python
def get_optimizer_params(model, encoder_lr=2e-5, decoder_lr=1e-3, weight_decay=0.01):
    no_decay = ["bias", "LayerNorm.bias", "LayerNorm.weight"]
    return [
        {"params": [p for n, p in model.backbone.named_parameters()
                    if not any(nd in n for nd in no_decay)],
         "lr": encoder_lr, "weight_decay": weight_decay},
        {"params": [p for n, p in model.backbone.named_parameters()
                    if any(nd in n for nd in no_decay)],
         "lr": encoder_lr, "weight_decay": 0.0},
        {"params": [p for n, p in model.named_parameters()
                    if "backbone" not in n],
         "lr": decoder_lr, "weight_decay": 0.0},
    ]

optimizer = torch.optim.AdamW(get_optimizer_params(model))
```

## Key Decisions

- **Typical ratio**: decoder_lr / encoder_lr ≈ 10–100x (e.g. 2e-5 vs 1e-3)
- **No weight decay on bias/LayerNorm**: standard practice, prevents regularizing scale params
- **Differs from layerwise-lr-decay**: this splits encoder vs head only; layerwise-lr-decay applies a per-layer multiplier within the encoder

## Workflow

1. Define param groups: encoder-with-decay, encoder-no-decay, head
2. Assign different LRs per group
3. Use single AdamW optimizer with all groups
4. Scheduler operates on all groups (each group can have its own warmup)

## References

- Source: [nbme-deberta-base-baseline-train](https://www.kaggle.com/code/yasufuminakama/nbme-deberta-base-baseline-train)
- Competition: NBME - Score Clinical Patient Notes
