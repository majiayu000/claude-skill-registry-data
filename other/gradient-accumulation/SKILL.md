---
name: cv-gradient-accumulation
description: >
  Accumulates gradients over multiple mini-batches before stepping the optimizer, simulating larger effective batch sizes.
---
# Gradient Accumulation

## Overview

When GPU memory limits batch size, accumulate gradients over N mini-batches before calling `optimizer.step()`. The effective batch size becomes `mini_batch × N`. This is critical for large image models (ResNet200d, EfficientNet-B7) where batch size 4-8 per GPU would produce noisy gradients.

## Quick Start

```python
import torch
from torch.cuda.amp import autocast, GradScaler

accum_steps = 4  # effective batch = mini_batch * 4
scaler = GradScaler()

for step, (images, labels) in enumerate(train_loader):
    images, labels = images.cuda(), labels.cuda()

    with autocast():
        logits = model(images)
        loss = criterion(logits, labels) / accum_steps  # scale loss

    scaler.scale(loss).backward()

    if (step + 1) % accum_steps == 0:
        scaler.unscale_(optimizer)
        torch.nn.utils.clip_grad_norm_(model.parameters(), max_norm=1.0)
        scaler.step(optimizer)
        scaler.update()
        optimizer.zero_grad()
```

## Workflow

1. Choose accumulation steps N (effective_batch = mini_batch × N)
2. Divide loss by N before backward (keeps gradient scale consistent)
3. Call backward every step (gradients accumulate in `.grad`)
4. Call optimizer.step + zero_grad every N steps
5. Works seamlessly with mixed precision (GradScaler)

## Key Decisions

- **Divide loss by N**: Essential — without this, accumulated gradients are N× too large
- **Learning rate**: Keep same as if training with full effective batch size
- **BatchNorm**: Stats are computed per mini-batch, not effective batch — may differ slightly
- **Scheduler step**: Step scheduler every N steps or per epoch, not every mini-batch
- **Typical N**: 2-8; beyond 8, diminishing returns and BN statistics diverge

## References

- RANZCR CLiP - Catheter and Line Position Challenge (Kaggle)
- Source: [ranzcr-resnext50-32x4d-starter-training](https://www.kaggle.com/code/yasufuminakama/ranzcr-resnext50-32x4d-starter-training)
