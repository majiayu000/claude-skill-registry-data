---
name: nlp-averaged-meta-embedding
description: Element-wise average of multiple pretrained embedding matrices as a parameter-free meta-embedding
---

## Overview

Concatenating embedding matrices (GloVe + Paragram + FastText) doubles or triples the input dimension, inflating model size. An unweighted mean of the matrices — Dynamic Meta Embedding (DME) — preserves the original dimension while combining the semantic signal from each source. It's parameter-free, adds no inference cost, and often performs comparably to weighted blends.

## Quick Start

```python
import numpy as np

def load_glove(word_index, embed_size):
    # ... returns (vocab_size, embed_size)
    ...

def load_paragram(word_index, embed_size):
    # ... returns (vocab_size, embed_size)
    ...

embedding_matrix_1 = load_glove(word_index, 300)
embedding_matrix_2 = load_paragram(word_index, 300)

# Unweighted DME: element-wise mean, same shape as inputs
embedding_matrix = np.mean([embedding_matrix_1, embedding_matrix_2], axis=0)
# Shape: (vocab_size, 300) — NOT (vocab_size, 600)
```

## Workflow

1. Build embedding matrices from each pretrained source using the same word→index mapping
2. Stack them and take `np.mean(..., axis=0)` — result has the same shape as each source
3. Pass the averaged matrix to your `Embedding` layer
4. Train the model normally — no special architecture changes required

## Key Decisions

- **Dim compatibility**: All matrices must share the same dimension. Project mismatched sources with a linear layer or drop them.
- **vs. concat**: Concat doubles input dim, increases first-layer parameters. Mean keeps dim fixed, no parameter growth.
- **vs. weighted mean**: Simple mean is often within 0.5% of weighted blends and needs no hyperparameter search.
- **Init alignment**: Ensure OOV rows are handled consistently across sources before averaging, or the mean becomes noisy.

## References

- [Single RNN with 4 folds (CLR)](https://www.kaggle.com/code/shujian/single-rnn-with-4-folds-clr)
