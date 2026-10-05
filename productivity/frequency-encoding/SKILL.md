---
name: tabular-frequency-encoding
description: >
  Adds each feature's value-count frequency as a new column, enabling tree models to split on how common or rare a value is.
---
# Frequency Encoding

## Overview

For categorical or high-cardinality numeric features, the raw value itself may be less informative than how often it appears. Frequency encoding replaces (or augments) each value with its count in the dataset. Tree models can then split on "values appearing fewer than N times" — a pattern that captures rarity without target leakage. Compute counts on train + real test combined for consistency.

## Quick Start

```python
import pandas as pd

def frequency_encode(train, test, col):
    # Count on combined data for consistent frequencies
    combined = pd.concat([train[[col]], test[[col]]], axis=0)
    freq = combined[col].value_counts()
    train[col + "_FE"] = train[col].map(freq)
    test[col + "_FE"]  = test[col].map(freq).fillna(0)

for col in feature_cols:
    frequency_encode(train, test, col)
```

## Workflow

1. Concatenate train and test (or real test only if synthetic rows exist)
2. Compute `value_counts()` for each feature
3. Map counts back as a new `_FE` column
4. Fill missing values with 0 (unseen values in test)
5. Optionally downcast to `uint8`/`uint16` for memory savings

## Key Decisions

- **Combined vs train-only**: Combined gives consistent counts; train-only avoids test leakage in strict setups
- **Exclude synthetics**: If test has fake rows, exclude them from frequency counts
- **Log transform**: `np.log1p(freq)` compresses skewed distributions
- **Pair with original**: Keep the raw feature alongside the frequency feature
- **Memory**: Downcast to smallest uint type fitting `max(freq)`

## References

- [200 Magical Models - Santander - [0.920]](https://www.kaggle.com/code/cdeotte/200-magical-models-santander-0-920)
