---
name: nlp-masked-bce-span-loss
description: Binary cross-entropy loss with mask to ignore special and padding tokens in token-level span classification
domain: nlp
---

# Masked BCE Span Loss

## Overview

For token-level span classification, special tokens (CLS, SEP, PAD) should not contribute to the loss. Label them as -1 during preprocessing, then use `torch.masked_select` to exclude them before computing mean BCE loss.

## Quick Start

```python
import torch
import torch.nn as nn

criterion = nn.BCEWithLogitsLoss(reduction="none")

def masked_bce_loss(logits, labels):
    """BCE loss that ignores tokens labeled -1 (special/padding)."""
    loss = criterion(logits.view(-1, 1), labels.view(-1, 1))
    mask = labels.view(-1, 1) != -1
    return torch.masked_select(loss, mask).mean()
```

## Label Creation

```python
import numpy as np

def create_token_labels(tokenizer, text, char_spans, max_len):
    enc = tokenizer(text, max_length=max_len, padding="max_length",
                    return_offsets_mapping=True, add_special_tokens=True)
    labels = np.zeros(max_len)
    # Mark non-text tokens as -1
    labels[np.array(enc.sequence_ids()) != 0] = -1
    # Mark span tokens as 1
    for start, end in char_spans:
        for i, (os, oe) in enumerate(enc["offset_mapping"]):
            if os >= start and oe <= end and labels[i] != -1:
                labels[i] = 1.0
    return labels
```

## Key Decisions

- **-1 label convention**: compatible with any loss function via masking, no custom loss class needed
- **reduction='none'**: required so masking happens before aggregation
- **Mask includes PAD + special**: both CLS/SEP and padding tokens get -1

## References

- Source: [nbme-deberta-base-baseline-train](https://www.kaggle.com/code/yasufuminakama/nbme-deberta-base-baseline-train)
- Competition: NBME - Score Clinical Patient Notes
