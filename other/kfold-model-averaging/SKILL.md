---
name: cv-kfold-model-averaging
description: Average predictions from K independently trained fold models at inference time for variance reduction without stacking complexity
domain: cv
---

# K-Fold Model Averaging

## Overview

Train K separate models on K-fold splits, save each checkpoint, then average their predictions at inference. Simpler than stacking — no meta-learner needed — yet typically captures 80% of the ensemble benefit. Works with any model type (CNN, transformer, tree-based).

## Quick Start

```python
import numpy as np
import tensorflow as tf

# Training: save best model per fold
from sklearn.model_selection import GroupKFold

gkf = GroupKFold(n_splits=5)
for fold, (train_idx, val_idx) in enumerate(gkf.split(df, groups=df.patient_id)):
    model = build_model()
    checkpoint = tf.keras.callbacks.ModelCheckpoint(
        f'model_fold{fold}.h5', save_best_only=True,
        monitor='val_loss', mode='min'
    )
    model.fit(train_data, epochs=20, callbacks=[checkpoint],
              validation_data=val_data)

# Inference: load all folds, average predictions
models = [tf.keras.models.load_model(f'model_fold{i}.h5') for i in range(5)]
predictions = sum(m.predict(test_data) for m in models) / len(models)
```

## Key Decisions

- **Simple average**: equal weights work well when folds are balanced; use weighted average if fold quality varies
- **Best checkpoint per fold**: save_best_only prevents averaging poorly-converged models
- **GroupKFold**: prevent data leakage when samples share a group (e.g., same patient)
- **Memory tradeoff**: K models in memory simultaneously — use sequential prediction if GPU-constrained

## References

- Source: [siim-cov19-efnb7-yolov5-infer](https://www.kaggle.com/code/h053473666/siim-cov19-efnb7-yolov5-infer)
- Competition: SIIM-FISABIO-RSNA COVID-19 Detection
