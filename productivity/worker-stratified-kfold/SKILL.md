---
name: nlp-worker-stratified-kfold
description: >
  Stratifies CV folds by annotator/worker ID to prevent annotator style leakage across train and validation splits in crowd-sourced datasets.
---
# Worker-Stratified KFold

## Overview

In crowd-sourced annotation datasets, multiple workers label different subsets of examples. If the same worker's annotations appear in both train and validation, the model can learn annotator-specific biases rather than the task signal. Stratifying folds by worker ID ensures each annotator's labels stay entirely within one fold, giving a more honest estimate of generalization. This is distinct from group-based splitting — here we stratify (balance worker distribution) rather than group (isolate entire groups).

## Quick Start

```python
from sklearn.model_selection import StratifiedKFold

# df has columns: 'text', 'label', 'worker' (annotator ID)
skf = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)

df['fold'] = -1
for fold, (_, val_idx) in enumerate(skf.split(X=df, y=df['worker'])):
    df.loc[val_idx, 'fold'] = fold

# Train/val split for a specific fold
train_df = df[df['fold'] != 0]
val_df = df[df['fold'] == 0]
```

## Workflow

1. Identify the worker/annotator ID column in the dataset
2. Use StratifiedKFold with `y=worker_id` to balance workers across folds
3. Each fold gets a proportional share of each worker's annotations
4. Train and evaluate per fold as usual

## Key Decisions

- **Stratify vs Group**: Stratify balances workers across folds; GroupKFold isolates workers entirely — choose based on whether workers overlap with test set
- **Many workers**: If workers >> folds, stratification is approximate; consider GroupKFold instead
- **vs label stratification**: Can combine both by creating a composite key `f"{worker}_{label}"`
- **When to use**: Any dataset with annotator IDs — toxicity, NER, sentiment with crowd labels

## References

- [Pytorch + W&B Jigsaw Starter](https://www.kaggle.com/code/debarshichanda/pytorch-w-b-jigsaw-starter)
