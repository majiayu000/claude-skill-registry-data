---
name: nlp-dynamic-batch-padding
description: >
  Pads each batch to its actual max sequence length instead of the global max_len, reducing wasted computation.
---
# Dynamic Batch Padding

## Overview

Standard padding pads all sequences to `max_len` (e.g., 512 or 1024). Dynamic batch padding pads only to the longest sequence in each batch, saving significant GPU memory and computation — especially when most sequences are much shorter than the limit.

## Quick Start

```python
def collate_fn(batch):
    """Custom collator that trims padding to batch max length."""
    inputs = default_collate(batch)
    max_len = int(inputs["attention_mask"].sum(dim=1).max())
    for key in ["input_ids", "attention_mask", "token_type_ids"]:
        if key in inputs:
            inputs[key] = inputs[key][:, :max_len]
    return inputs
```

## Workflow

1. Tokenize with a generous `max_length` (covers longest possible input)
2. In the collate function, find actual max attention length in the batch
3. Trim all tensors to that length
4. Optionally sort dataset by length first for even better packing

## Key Decisions

- **Sort by length**: Grouping similar-length sequences minimizes padding waste further
- **Combine with adaptive max_len**: Set global max from data distribution, not a fixed number
- **Memory savings**: 30-50% reduction on datasets with high length variance
- **Compatibility**: Works with any HuggingFace tokenizer output

## References

- Feedback Prize - English Language Learning (Kaggle)
- Source: [fb3-deberta-v3-base-baseline-train](https://www.kaggle.com/code/yasufuminakama/fb3-deberta-v3-base-baseline-train)
