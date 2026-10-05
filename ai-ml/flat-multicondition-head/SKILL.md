---
name: cv-flat-multicondition-head
description: >
  Models multiple conditions with a single flat output layer of N_labels × N_classes logits, sliced into per-condition softmax at inference.
---
# Flat Multi-Condition Head

## Overview

When predicting severity grades (Normal/Moderate/Severe) for multiple conditions simultaneously (e.g., 5 spinal conditions × 5 vertebral levels = 25 labels, each with 3 classes), a flat 75-dimensional output head avoids the complexity of multiple classification heads. During training, use cross-entropy on all 75 logits. At inference, slice the output into 25 groups of 3 and apply softmax per group. This is simpler to implement, faster to train, and often matches multi-head performance.

## Quick Start

```python
import torch
import torch.nn as nn
import timm

N_LABELS = 25       # conditions × levels
N_CLASSES = 3       # normal, moderate, severe
N_OUTPUT = N_LABELS * N_CLASSES  # 75

class MultiConditionModel(nn.Module):
    def __init__(self, model_name, in_chans=30):
        super().__init__()
        self.backbone = timm.create_model(
            model_name, pretrained=True,
            in_chans=in_chans, num_classes=N_OUTPUT, global_pool='avg'
        )

    def forward(self, x):
        return self.backbone(x)  # (B, 75)

# Training: reshape for per-label CE loss
logits = model(images)  # (B, 75)
logits = logits.view(-1, N_LABELS, N_CLASSES)  # (B, 25, 3)
loss = nn.CrossEntropyLoss()(logits.view(-1, N_CLASSES), labels.view(-1))

# Inference: per-condition softmax
logits = model(images)[0]  # (75,)
for i in range(N_LABELS):
    probs = logits[i*3:(i+1)*3].float().softmax(0).cpu().numpy()
    predictions.append(probs)
```

## Workflow

1. Set `num_classes = N_labels × N_classes` in the backbone
2. Train with CE loss on reshaped `(B × N_labels, N_classes)` logits
3. At inference, slice flat output into per-label chunks
4. Apply softmax per chunk to get per-condition probability distributions

## Key Decisions

- **Flat vs multi-head**: Flat is simpler; multi-head allows per-condition learning rates
- **Loss weighting**: Weight rare conditions higher with class weights in CE loss
- **Shared backbone**: All conditions share features — works well when inputs overlap
- **Label ordering**: Keep consistent ordering between training labels and output slicing

## References

- [RSNA2024 LSDC DenseNet Submission](https://www.kaggle.com/code/hugowjd/rsna2024-lsdc-densenet-submission)
- [RSNA2024 LSDC Submission Baseline](https://www.kaggle.com/code/itsuki9180/rsna2024-lsdc-submission-baseline)
