---
name: llm-tfidf-chunked-retrieval
description: >
  Scalable TF-IDF retrieval over large document corpora using frozen vocabulary and chunked top-k merging.
---
# TF-IDF Chunked Retrieval

## Overview

For large corpora (100K+ documents), compute TF-IDF similarity in chunks to avoid OOM. Fit vocabulary on the query corpus, freeze it, then apply to document chunks. Collect per-chunk top-k results and merge globally. This is faster than dense retrieval for keyword-heavy queries.

## Quick Start

```python
from sklearn.feature_extraction.text import TfidfVectorizer
import numpy as np

# Fit vocab on queries, freeze for documents
vectorizer = TfidfVectorizer(ngram_range=(1, 2))
vectorizer.fit(queries)
vocab = vectorizer.get_feature_names_out()

vectorizer_docs = TfidfVectorizer(ngram_range=(1, 2), vocabulary=vocab)
query_vecs = vectorizer_docs.fit_transform(queries)

# Chunked retrieval
chunk_size, top_k = 50000, 5
all_scores, all_indices = [], []
for start in range(0, len(documents), chunk_size):
    chunk_vecs = vectorizer_docs.transform(documents[start:start + chunk_size])
    scores = (query_vecs * chunk_vecs.T).toarray()
    top_idx = scores.argpartition(-top_k, axis=1)[:, -top_k:]
    all_indices.append(top_idx + start)
    all_scores.append(np.take_along_axis(scores, top_idx, axis=1))
```

## Workflow

1. Fit TF-IDF vocabulary on query corpus (questions + answer options)
2. Process document corpus in chunks (50K each)
3. Compute sparse similarity per chunk, keep top-k per chunk
4. Merge all chunk results, select global top-k
5. Retrieve full text for top-k document indices

## Key Decisions

- **Frozen vocab**: Fit on queries ensures all query terms are indexed
- **Chunk size**: 50K balances memory vs overhead; tune for your RAM
- **Sparse vs dense**: TF-IDF wins for keyword matching; dense for semantic
- **Combine both**: Use TF-IDF + dense retrieval and merge results

## References

- Kaggle LLM Science Exam (Kaggle)
- Source: [86-2-with-only-270k-articles](https://www.kaggle.com/code/mbanaei/86-2-with-only-270k-articles)
