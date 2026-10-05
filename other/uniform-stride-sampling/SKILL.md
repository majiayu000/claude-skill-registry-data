---
name: nlp-uniform-stride-sampling
description: >
  Samples N items uniformly by stride from a variable-length list, always preserving the first and last elements, to fit long sequences into a fixed token budget.
---
# Uniform Stride Sampling

## Overview

When a document has many segments (code cells, paragraphs, passages) but you can only fit N into a model's context window, random sampling misses structure and consecutive sampling biases toward the start. Uniform stride sampling picks items at evenly spaced intervals, always including the first and last, giving the model a representative sketch of the full document regardless of length.

## Quick Start

```python
import numpy as np

def sample_uniform(items, n):
    if n >= len(items):
        return items
    result = []
    step = len(items) / n
    idx = 0.0
    while int(np.round(idx)) < len(items):
        result.append(items[int(np.round(idx))])
        idx += step
    # Ensure last item is always included
    if result[-1] != items[-1]:
        result[-1] = items[-1]
    return result

# Sample 20 code cells from a notebook with 100+ cells
sampled = sample_uniform(all_code_cells, n=20)
```

## Workflow

1. Determine the budget N (how many items fit in the context)
2. If the list is shorter than N, use all items
3. Compute step size: `len(items) / N`
4. Walk through at fractional indices, rounding to nearest integer
5. Replace the last picked item with the actual last item if not already included

## Key Decisions

- **Truncation per item**: Cap each sampled item's length (e.g., 200 chars) to stay within token budget
- **First/last guarantee**: Critical for documents where intro and conclusion carry key signals
- **Alternative**: Weighted sampling by importance (e.g., longer cells get priority)
- **Use case**: Any long-document task — notebook ordering, multi-passage QA, document summarization

## References

- [Stronger baseline with code cells](https://www.kaggle.com/code/suicaokhoailang/stronger-baseline-with-code-cells)
