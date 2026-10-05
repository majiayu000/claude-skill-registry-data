---
name: tabular-oof-meta-features
description: >
  Generates out-of-fold predictions from auxiliary models and uses them as input features for the final model.
---
# OOF Meta-Features

## Overview

Train a model to predict an auxiliary target (e.g., a related physical property, an intermediate label), collect its out-of-fold (OOF) predictions, and feed those as features into the final model. This injects learned representations without leakage — each sample's meta-feature comes from a model that never saw that sample during training.

## Quick Start

```python
import numpy as np
from sklearn.model_selection import KFold
import lightgbm as lgb

def generate_oof_feature(X, y_aux, X_test, params, n_splits=5):
    """Train on auxiliary target, return OOF predictions as features."""
    folds = KFold(n_splits=n_splits, shuffle=True, random_state=42)
    oof = np.zeros(len(X))
    test_pred = np.zeros(len(X_test))

    for train_idx, val_idx in folds.split(X):
        model = lgb.LGBMRegressor(**params)
        model.fit(X.iloc[train_idx], y_aux.iloc[train_idx],
                  eval_set=[(X.iloc[val_idx], y_aux.iloc[val_idx])],
                  callbacks=[lgb.early_stopping(100)])
        oof[val_idx] = model.predict(X.iloc[val_idx])
        test_pred += model.predict(X_test) / n_splits

    return oof, test_pred

# Usage: predict auxiliary target, add as feature
oof_aux, test_aux = generate_oof_feature(X, y_auxiliary, X_test, params)
X['meta_aux'] = oof_aux
X_test['meta_aux'] = test_aux

# Now train final model with the meta-feature included
final_model.fit(X, y_target)
```

## Workflow

1. Identify auxiliary targets related to the main target (e.g., intermediate properties)
2. Generate OOF predictions for each auxiliary target using K-Fold
3. Average test predictions across folds (no leakage)
4. Add OOF columns to training features, averaged predictions to test features
5. Train final model with enriched feature set

## Key Decisions

- **No leakage**: OOF ensures each sample's meta-feature comes from held-out predictions
- **Same folds**: Use identical fold splits for OOF generation and final training
- **Multiple meta-features**: Stack several auxiliary predictions — each adds a learned signal
- **Diminishing returns**: 2-3 meta-features usually saturate; more adds noise

## References

- Predicting Molecular Properties / CHAMPS Scalar Coupling (Kaggle)
- Source: [using-meta-features-to-improve-model](https://www.kaggle.com/code/artgor/using-meta-features-to-improve-model)
