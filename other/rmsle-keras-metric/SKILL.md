---
name: tabular-rmsle-keras-metric
description: Custom Keras RMSLE metric using K.log with K.clip to safely evaluate price and count regression during training
---

# RMSLE Keras Metric

## Overview

Root Mean Squared Logarithmic Error (RMSLE) penalizes under-prediction more than over-prediction, making it ideal for price, sales, or count regression. Implement it as a custom Keras metric so it displays during training alongside loss. Use `K.clip` to avoid `log(0)`.

## Quick Start

```python
from tensorflow.keras import backend as K

def rmsle(y_true, y_pred):
    first_log = K.log(K.clip(y_pred, K.epsilon(), None) + 1.)
    second_log = K.log(K.clip(y_true, K.epsilon(), None) + 1.)
    return K.sqrt(K.mean(K.square(first_log - second_log), axis=-1))

model.compile(optimizer='adam', loss='mse', metrics=['mae', rmsle])
```

## Workflow

1. Define `rmsle` as a function of `(y_true, y_pred)` using Keras backend ops
2. Clip predictions to `[epsilon, inf)` before log to prevent NaN
3. Add 1 before log (log1p) to handle zero values
4. Pass as `metrics=[rmsle]` in `model.compile`
5. Monitor during training — it tracks the competition metric directly

## Key Decisions

- **Clip vs relu**: `K.clip` is safer — relu zeros out negatives silently
- **Loss vs metric**: use MSE or MAE as loss (smoother gradients), RMSLE as metric
- **Log1p target**: if target is already log-transformed, use RMSE instead of RMSLE
- **vs sklearn**: `sklearn.metrics.mean_squared_log_error` works for evaluation only, not as a Keras metric

## References

- [A simple nn solution with Keras](https://www.kaggle.com/code/knowledgegrappler/a-simple-nn-solution-with-keras-0-48611-pl)
