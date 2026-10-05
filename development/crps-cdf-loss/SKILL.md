---
name: tabular-crps-cdf-loss
description: Model cumulative distribution via softmax output layer and CRPS loss — for probabilistic regression over discrete bins
domain: tabular
---

# CRPS CDF Loss

## Overview

When the target is a probability distribution (e.g., "what is the CDF of yards gained?"), encode the label as a step function over discrete bins, use a softmax output layer, then train with Continuous Ranked Probability Score (CRPS) loss. CRPS penalizes the squared difference between predicted and true CDFs, rewarding both calibration and sharpness.

## Quick Start

```python
import numpy as np
import tensorflow.keras.backend as K

def crps_loss(y_true, y_pred):
    """CRPS loss on cumulative softmax output."""
    return K.mean(K.square(y_true - K.cumsum(y_pred, axis=1)), axis=1)

def encode_cdf_target(values, n_bins=199, offset=99):
    """Encode scalar targets as step-function CDFs.
    
    Args:
        values: array of integer targets
        n_bins: number of discrete bins
        offset: bin index corresponding to target=0
    """
    y = np.zeros((len(values), n_bins))
    for i, v in enumerate(values):
        y[i, v + offset:] = 1.0
    return y

# Model
output = Dense(199, activation='softmax')(hidden)
model.compile(optimizer='adam', loss=crps_loss)

# CRPS evaluation callback
y_pred_cdf = np.clip(np.cumsum(model.predict(X_val), axis=1), 0, 1)
y_true_cdf = np.clip(np.cumsum(y_val, axis=1), 0, 1)
crps = np.mean(np.sum((y_true_cdf - y_pred_cdf) ** 2, axis=1)) / n_bins
```

## Key Decisions

- **Softmax output**: guarantees predicted PDF sums to 1; cumsum gives valid CDF
- **Bin count**: 199 for yards (−99 to +99); adjust to match your target range
- **Clip cumsum**: numerical safety — ensures CDF stays in [0, 1]
- **CRPS vs MSE**: CRPS is a proper scoring rule for distributions; MSE on CDF works but lacks calibration incentive

## References

- Source: [neural-networks-feature-engineering-for-the-win](https://www.kaggle.com/code/bgmello/neural-networks-feature-engineering-for-the-win)
- Competition: NFL Big Data Bowl
