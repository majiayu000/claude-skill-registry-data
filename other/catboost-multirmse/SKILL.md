---
name: tabular-catboost-multirmse
description: >
  CatBoostRegressor with MultiRMSE loss for native multi-output regression, predicting all targets in a single model without per-target loops.
---
# CatBoost MultiRMSE

## Overview

Most gradient boosting libraries (XGBoost, LightGBM) require fitting one model per output column for multi-output regression — slow when there are 100+ targets. CatBoost's `MultiRMSE` loss natively handles multiple outputs in a single model, sharing tree structure across targets. This is 5-50x faster than per-target loops and can capture cross-target correlations. Combined with SVD target compression, it enables efficient prediction of thousands of outputs.

## Quick Start

```python
from catboost import CatBoostRegressor

params = {
    'learning_rate': 0.1,
    'depth': 7,
    'l2_leaf_reg': 4,
    'loss_function': 'MultiRMSE',
    'eval_metric': 'MultiRMSE',
    'iterations': 200,
    'boosting_type': 'Plain',
    'bootstrap_type': 'Bayesian',
    'allow_const_label': True,
    'random_state': 42,
}

model = CatBoostRegressor(**params)
model.fit(X_train, Y_train, eval_set=(X_val, Y_val), verbose=50)
preds = model.predict(X_test)  # shape: (n_test, n_targets)
```

## Workflow

1. Prepare target matrix Y with shape (n_samples, n_targets)
2. Configure CatBoostRegressor with `loss_function='MultiRMSE'`
3. Fit single model on all targets simultaneously
4. Predict returns (n_samples, n_targets) array directly

## Key Decisions

- **boosting_type='Plain'**: Required for MultiRMSE; 'Ordered' not supported
- **vs per-target loop**: Single model is faster but may underperform if targets have very different distributions
- **Target reduction**: Combine with SVD to predict 128 components instead of 23,000 raw targets
- **GPU support**: Set `task_type='GPU'` for large datasets; MultiRMSE supports GPU training
- **depth**: Start at 6-8; deeper trees risk overfitting on compressed targets

## References

- [LB T15 MSCI Multiome CatBoostRegressor](https://www.kaggle.com/code/xiafire/lb-t15-msci-multiome-catboostregressor)
