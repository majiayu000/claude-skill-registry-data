---
name: tabular-optuna-lgbm-tuning
description: >
  Uses Optuna with TPE sampler for Bayesian hyperparameter optimization of LightGBM, searching key params like num_leaves, depth, and learning rate.
---
# Optuna LightGBM Tuning

## Overview

Optuna's Tree-structured Parzen Estimator (TPE) efficiently searches LightGBM hyperparameter space by building a probabilistic model of which regions produce good scores. Typically finds better parameters than grid/random search in fewer trials. Define an objective function, let Optuna propose params, evaluate with CV.

## Quick Start

```python
import optuna
import lightgbm as lgb
from sklearn.model_selection import cross_val_score

def objective(trial):
    params = {
        'n_estimators': trial.suggest_int('n_estimators', 100, 2000),
        'num_leaves': trial.suggest_int('num_leaves', 16, 256),
        'max_depth': trial.suggest_int('max_depth', 3, 12),
        'learning_rate': trial.suggest_float('learning_rate', 1e-3, 0.3, log=True),
        'min_child_samples': trial.suggest_int('min_child_samples', 5, 100),
        'subsample': trial.suggest_float('subsample', 0.5, 1.0),
        'colsample_bytree': trial.suggest_float('colsample_bytree', 0.5, 1.0),
        'reg_alpha': trial.suggest_float('reg_alpha', 1e-8, 10.0, log=True),
        'reg_lambda': trial.suggest_float('reg_lambda', 1e-8, 10.0, log=True),
    }
    model = lgb.LGBMClassifier(**params, random_state=42, n_jobs=-1)
    score = cross_val_score(model, X_train, y_train, cv=5, scoring='roc_auc').mean()
    return score

study = optuna.create_study(direction='maximize', sampler=optuna.samplers.TPESampler(seed=42))
study.optimize(objective, n_trials=100, show_progress_bar=True)

best_model = lgb.LGBMClassifier(**study.best_params)
best_model.fit(X_train, y_train)
```

## Workflow

1. Define objective function with `trial.suggest_*` for each hyperparameter
2. Use log scale for learning rate and regularization params
3. Run 50-200 trials (TPE converges fast)
4. Extract best params and retrain on full data
5. Optionally use `optuna.visualization` to inspect param importance

## Key Decisions

- **TPE vs random**: TPE finds good regions 2-3x faster than random search
- **n_trials**: 50 for quick search, 200 for thorough; diminishing returns after ~100
- **Pruning**: Add `optuna.integration.LightGBMPruningCallback` to early-stop bad trials
- **Seed**: Fix sampler seed for reproducibility across runs

## References

- Riiid Answer Correctness Prediction (Kaggle)
- Source: [riiid-answer-correctness-prediction-eda-modeling](https://www.kaggle.com/code/isaienkov/riiid-answer-correctness-prediction-eda-modeling)
