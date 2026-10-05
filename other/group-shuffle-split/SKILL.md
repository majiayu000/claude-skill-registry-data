---
name: tabular-group-shuffle-split
description: >
  Splits train/validation using GroupShuffleSplit so that related samples (forks, families, sessions) never span both sets.
---
# Group Shuffle Split

## Overview

When samples have group relationships (notebook forks sharing an ancestor, patients in the same hospital, users in the same household), random splits leak information across train/validation. `GroupShuffleSplit` ensures all samples from the same group land in the same split, preventing data leakage while still allowing a simple holdout split (unlike GroupKFold which requires K folds).

## Quick Start

```python
from sklearn.model_selection import GroupShuffleSplit

splitter = GroupShuffleSplit(n_splits=1, test_size=0.1, random_state=42)
groups = df["group_id"]  # e.g., ancestor_id, patient_id, session_id

train_idx, val_idx = next(splitter.split(df, groups=groups))
train_df = df.iloc[train_idx].reset_index(drop=True)
val_df = df.iloc[val_idx].reset_index(drop=True)
```

## Workflow

1. Identify the group column (ancestor, patient, user, session, etc.)
2. Create a `GroupShuffleSplit` with desired test size
3. Split once to get train/val indices where no group spans both sets
4. Use the indices to create train and validation DataFrames

## Key Decisions

- **vs GroupKFold**: GroupShuffleSplit gives a single random split; GroupKFold gives K deterministic folds
- **test_size**: Fraction of groups held out (0.1-0.2 typical)
- **n_splits**: Set to 1 for a single holdout; increase for repeated random splits
- **Group granularity**: Choose the coarsest meaningful group to maximize leakage prevention

## References

- [Getting Started with AI4Code](https://www.kaggle.com/code/ryanholbrook/getting-started-with-ai4code)
- [AI4Code Pytorch DistilBert Baseline](https://www.kaggle.com/code/aerdem4/ai4code-pytorch-distilbert-baseline)
