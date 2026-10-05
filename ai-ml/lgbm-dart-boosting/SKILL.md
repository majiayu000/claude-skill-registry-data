---
name: tabular-lgbm-dart-boosting
description: Use LightGBM DART boosting (dropout on trees) with aggressive feature and bagging fractions to reduce overfitting on high-dimensional tabular data
domain: tabular
---

# LightGBM DART Boosting

## Overview

DART (Dropouts meet Multiple Additive Regression Trees) randomly drops completed trees during training, reducing over-specialization of later trees. Combined with aggressive feature subsampling (20%) and bagging fraction (50%), it produces strong generalization on high-dimensional tabular data where standard GBDT overfits. Trades training speed for better holdout scores.

## Quick Start

```python
import lightgbm as lgb

params = {
    'objective': 'binary',
    'metric': 'binary_logloss',
    'boosting': 'dart',
    'num_leaves': 100,
    'learning_rate': 0.01,
    'feature_fraction': 0.20,
    'bagging_freq': 10,
    'bagging_fraction': 0.50,
    'lambda_l2': 2,
    'min_data_in_leaf': 40,
    'n_jobs': -1,
}

model = lgb.train(
    params=params,
    train_set=lgb_train,
    num_boost_round=10500,
    valid_sets=[lgb_train, lgb_valid],
    callbacks=[lgb.early_stopping(1500), lgb.log_evaluation(100)],
)
```

## Key Decisions

- **feature_fraction=0.20**: aggressive subsampling forces diverse trees; increase to 0.4 for fewer features
- **early_stopping=1500**: DART needs a large patience since loss curves are noisier
- **num_boost_round=10500**: DART requires more rounds than GBDT due to dropout
- **No DART at inference**: all trees are used at prediction time — dropout is training-only
- **Slower than GBDT**: ~3-5x slower training; worth it when overfitting gap is large

## References

- Source: [amex-lgbm-dart-cv-0-7977](https://www.kaggle.com/code/ragnar123/amex-lgbm-dart-cv-0-7977)
- Competition: American Express - Default Prediction
