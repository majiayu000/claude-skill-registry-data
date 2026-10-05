---
name: tabular-ridge-xgb-stacking
description: >
  Two-stage stacking where Ridge regression on OHE+scaled features produces OOF predictions fed as an extra feature to XGBoost, letting the tree model correct non-linear residuals on top of captured linear patterns.
---

# Ridge-XGBoost Stacking

## Overview

Stage 1 fits a Ridge regression on one-hot encoded, scaled features to cheaply capture linear relationships. Its out-of-fold (OOF) predictions become an additional feature for Stage 2, where XGBoost trains on all original features plus the Ridge OOF column. XGBoost focuses on correcting non-linear residuals rather than re-learning linear signals. Both stages share the same CV splits for consistency.

## Quick Start

```python
from sklearn.linear_model import Ridge
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.model_selection import StratifiedKFold
import xgboost as xgb
import numpy as np

kf = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)
ridge_oof = np.zeros(len(X_train))
ridge_test = np.zeros(len(X_test))

# Stage 1: Ridge OOF
ohe = OneHotEncoder(sparse_output=False, handle_unknown='ignore')
X_ohe = ohe.fit_transform(X_train[cat_cols])
X_test_ohe = ohe.transform(X_test[cat_cols])
X_combined = np.hstack([StandardScaler().fit_transform(X_train[num_cols]), X_ohe])

for tr_idx, val_idx in kf.split(X_train, y_train):
    scaler = StandardScaler()
    X_tr = scaler.fit_transform(X_combined[tr_idx])
    X_val = scaler.transform(X_combined[val_idx])
    ridge = Ridge(alpha=10)
    ridge.fit(X_tr, y_train.iloc[tr_idx])
    ridge_oof[val_idx] = ridge.predict(X_val)
    ridge_test += ridge.predict(scaler.transform(
        np.hstack([StandardScaler().fit_transform(X_test[num_cols]), X_test_ohe])
    )) / kf.n_splits

# Stage 2: XGBoost with ridge_oof feature
X_train['ridge_oof'] = ridge_oof
X_test['ridge_oof'] = ridge_test

xgb_model = xgb.XGBClassifier(n_estimators=1000, learning_rate=0.05,
                                max_depth=6, early_stopping_rounds=50)
# Train with same KFold splits...
```

## Workflow

1. Define a single `StratifiedKFold(n_splits=5)` shared across both stages
2. **Stage 1:** OneHotEncode categoricals, StandardScale all features, fit Ridge(alpha=10)
3. Collect OOF predictions for train, averaged predictions for test
4. **Stage 2:** Add `ridge_oof` column to original feature set
5. Train XGBoost on original features + ridge_oof using same folds
6. Final prediction comes from Stage 2 XGBoost

## Key Decisions

- **Ridge alpha=10:** moderate regularization prevents overfitting on high-cardinality OHE
- **Same CV splits:** ensures Ridge OOF values are truly out-of-fold for XGBoost training rows
- **Why not just blend?** Stacking as a feature lets XGBoost learn *when* to trust the linear model vs. override it, unlike a fixed-weight blend
- **OHE for Ridge only:** trees handle categoricals natively; Ridge needs explicit encoding

## References

- Source: "S6E3 Ridge XGB N-gram 0.91927 CV" (Kaggle Playground Series S6E3)
