---
name: tabular-pseudo-labeling
description: >
  Augments training data with high-confidence test predictions as pseudo labels, retrains the model, and keeps the result only if OOF AUC improves. A semi-supervised technique for tabular competitions.
---

# Pseudo Labeling

## Overview

Pseudo labeling leverages unlabeled test data by treating high-confidence model predictions as ground truth. After a base model is trained with KFold CV, test samples where the model is very confident (near 0 or 1) are added to training with their predicted labels. The model is retrained and the result is kept only if OOF AUC improves.

## Quick Start

```python
import xgboost as xgb
from sklearn.model_selection import StratifiedKFold
from sklearn.metrics import roc_auc_score
import numpy as np

# 1. Train base model with KFold, collect OOF and test predictions
oof_preds, test_preds = train_kfold(X_train, y_train, X_test, n_splits=5)
base_auc = roc_auc_score(y_train, oof_preds)

# 2. Select high-confidence test samples
THRESHOLD = 0.995
mask_pos = test_preds > THRESHOLD
mask_neg = test_preds < (1 - THRESHOLD)
pseudo_mask = mask_pos | mask_neg

X_pseudo = X_test[pseudo_mask]
y_pseudo = (test_preds[pseudo_mask] > 0.5).astype(int)

# 3. Augment training set
X_aug = np.concatenate([X_train, X_pseudo])
y_aug = np.concatenate([y_train, y_pseudo])

# 4. Retrain and compare
oof_preds_aug, _ = train_kfold(X_aug, y_aug, X_test, n_splits=5)
new_auc = roc_auc_score(y_aug[:len(y_train)], oof_preds_aug[:len(y_train)])

# 5. Keep only if improved
if new_auc > base_auc:
    print(f"Pseudo labeling improved AUC: {base_auc:.5f} -> {new_auc:.5f}")
```

## Workflow

1. **Train base model** with StratifiedKFold CV (typically 5-10 folds).
2. **Collect OOF predictions** on train and mean predictions on test.
3. **Filter test samples** by confidence threshold (e.g., >0.995 or <0.005).
4. **Assign pseudo labels** (round predictions to 0 or 1).
5. **Concatenate** pseudo-labeled samples with original training data.
6. **Retrain** with the same KFold CV setup on the augmented dataset.
7. **Compare OOF AUC** on the original training labels only. Keep if improved.

## Key Decisions

| Decision | Guidance |
|---|---|
| Confidence threshold | Start high (0.995). Lower thresholds add more data but risk label noise. |
| How many rounds | One round is usually enough. Iterating risks confirmation bias. |
| Validation | Always compare AUC on the *original* train labels, not on pseudo labels. |
| Class balance | Check that pseudo labels don't skew class ratio excessively. |
| Model choice | Works best with gradient boosting (XGBoost, LightGBM, CatBoost). |
| When to skip | If base model AUC is low (<0.80), pseudo labels are too noisy to help. |

## References

- Kaggle: "S6E3 Detail EDA + Baseline XGB" (playground-series-s6e3)
- Lee, D.H. "Pseudo-label: The simple and efficient semi-supervised learning method" (ICML 2013 Workshop)
