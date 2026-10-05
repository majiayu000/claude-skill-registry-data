---
name: nlp-label-smoothing-binary
description: >
  Applies label smoothing to binary cross-entropy loss to reduce overconfidence and improve generalization in text classification.
---
# Label Smoothing (Binary)

## Overview

Replace hard labels (0/1) with softened labels (ε, 1-ε) during training. This prevents the model from becoming overconfident on training examples, acts as implicit regularization, and improves calibration of predicted probabilities. Especially useful in text classification where boundary examples are ambiguous.

## Quick Start

```python
# Keras / TensorFlow
import tensorflow as tf

loss = tf.keras.losses.BinaryCrossentropy(label_smoothing=0.02)
model.compile(optimizer='adam', loss=loss, metrics=['accuracy'])

# PyTorch (manual)
import torch
import torch.nn.functional as F

def smooth_bce(preds, targets, smoothing=0.02):
    """Binary cross-entropy with label smoothing."""
    targets = targets * (1 - smoothing) + 0.5 * smoothing
    return F.binary_cross_entropy_with_logits(preds, targets)

# Usage in training loop
loss = smooth_bce(logits, labels, smoothing=0.02)
loss.backward()
```

## Workflow

1. Choose smoothing factor ε (typically 0.01-0.1)
2. Replace loss function with smoothed version
3. Train as usual — no other changes needed
4. At inference, predictions are naturally better calibrated

## Key Decisions

- **Smoothing value**: 0.02 for clean labels, 0.1 for noisy labels
- **Effect**: Label 1→0.99, label 0→0.01 (with ε=0.02) — tiny change, significant regularization
- **vs dropout**: Complementary — use both for best results
- **When to avoid**: Very small datasets where every label is precious and verified correct
- **Calibration**: Smoothed models output more calibrated probabilities — good for ensembling

## References

- LLM - Detect AI Generated Text (Kaggle)
- Source: [detect-fake-text-kerasnlp-tf-torch-jax-train](https://www.kaggle.com/code/awsaf49/detect-fake-text-kerasnlp-tf-torch-jax-train)
