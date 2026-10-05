---
name: cv-mixed-precision-training
description: >
  Uses PyTorch AMP autocast and GradScaler for FP16 training, halving memory usage and speeding up training on modern GPUs.
---
# Mixed Precision Training

## Overview

Run forward pass in FP16 (half precision) while keeping master weights in FP32. This halves GPU memory for activations and enables larger batch sizes or image resolutions. PyTorch's `autocast` handles dtype selection per operation; `GradScaler` prevents underflow in FP16 gradients.

## Quick Start

```python
import torch
from torch.cuda.amp import autocast, GradScaler

scaler = GradScaler()

for images, labels in train_loader:
    images, labels = images.cuda(), labels.cuda()
    optimizer.zero_grad()

    with autocast():
        logits = model(images)
        loss = criterion(logits, labels)

    scaler.scale(loss).backward()
    scaler.unscale_(optimizer)
    torch.nn.utils.clip_grad_norm_(model.parameters(), max_norm=1.0)
    scaler.step(optimizer)
    scaler.update()
```

## Workflow

1. Create `GradScaler()` before training loop
2. Wrap forward pass + loss in `autocast()` context
3. Call `scaler.scale(loss).backward()` instead of `loss.backward()`
4. Optionally unscale before gradient clipping
5. `scaler.step(optimizer)` and `scaler.update()` replace `optimizer.step()`

## Key Decisions

- **Memory savings**: ~40-50% reduction in activation memory → can double batch size
- **Speed**: 1.5-2x faster on Volta/Ampere GPUs (V100, A100, RTX 30xx+)
- **Accuracy**: Virtually identical to FP32 — safe for almost all CV tasks
- **Gradient clipping**: Must `unscale_` before `clip_grad_norm_` to clip in FP32 space
- **When to skip**: Very small models where memory isn't a bottleneck

## References

- RANZCR CLiP - Catheter and Line Position Challenge (Kaggle)
- Source: [ranzcr-resnext50-32x4d-starter-training](https://www.kaggle.com/code/yasufuminakama/ranzcr-resnext50-32x4d-starter-training)
