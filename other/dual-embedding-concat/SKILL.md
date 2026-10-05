---
name: nlp-dual-embedding-concat
description: Concatenate GloVe and FastText embedding matrices along feature axis for richer 600d word representations
domain: nlp
---

# Dual Embedding Concatenation

## Overview

Single pretrained embeddings miss some word relationships — GloVe captures co-occurrence patterns while FastText handles subword morphology and OOV words. Concatenate both along the feature dimension to get a 600d embedding that combines both strengths. Especially useful for noisy text (social media, comments) where misspellings are common.

## Quick Start

```python
import numpy as np

def build_embedding_matrix(word_index, embedding_path, embed_dim=300):
    """Load pretrained embeddings into a matrix aligned with tokenizer vocab."""
    embeddings = load_embeddings(embedding_path)  # dict: word -> vector
    matrix = np.zeros((len(word_index) + 1, embed_dim))
    unknown = []
    for word, idx in word_index.items():
        if word in embeddings:
            matrix[idx] = embeddings[word]
        else:
            unknown.append(word)
    return matrix, unknown

# Build and concatenate
glove_matrix, unk_glove = build_embedding_matrix(
    tokenizer.word_index, 'glove.840B.300d.txt')
fasttext_matrix, unk_ft = build_embedding_matrix(
    tokenizer.word_index, 'crawl-300d-2M.vec')
embedding_matrix = np.concatenate([glove_matrix, fasttext_matrix], axis=-1)
# Shape: (vocab_size, 600)

# Use in model
embedding = nn.Embedding.from_pretrained(
    torch.tensor(embedding_matrix, dtype=torch.float32), freeze=False)
```

## Key Decisions

- **GloVe + FastText**: complementary — FastText handles OOV via subwords, GloVe has broader context
- **freeze=False**: fine-tune embeddings during training for domain adaptation
- **OOV handling**: FastText covers ~95% of words vs GloVe's ~85% — concat reduces unknown words
- **Memory cost**: 600d doubles memory vs single embedding — acceptable for most GPU setups

## References

- Source: [simple-lstm-pytorch-version](https://www.kaggle.com/code/bminixhofer/simple-lstm-pytorch-version)
- Competition: Jigsaw Unintended Bias in Toxicity Classification
