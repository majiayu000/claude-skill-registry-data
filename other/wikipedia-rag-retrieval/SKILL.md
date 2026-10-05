---
name: llm-wikipedia-rag-retrieval
description: >
  Dense retrieval over a FAISS-indexed Wikipedia corpus to provide grounding context for LLM question answering.
---
# Wikipedia RAG Retrieval

## Overview

For knowledge-intensive QA tasks, retrieve relevant Wikipedia passages using dense embeddings (e.g., sentence-transformers) indexed in FAISS. Prepend retrieved passages as context to the LLM prompt. This grounds the model in factual content and dramatically improves accuracy over closed-book inference.

## Quick Start

```python
import faiss
import numpy as np
from sentence_transformers import SentenceTransformer

# Build index (offline)
encoder = SentenceTransformer("all-MiniLM-L6-v2")
embeddings = encoder.encode(passages, batch_size=256, show_progress_bar=True)
index = faiss.IndexFlatIP(embeddings.shape[1])
index.add(np.float32(embeddings))
faiss.write_index(index, "wiki.index")

# Retrieve at inference
query_embs = encoder.encode(questions)
scores, indices = index.search(np.float32(query_embs), k=5)
contexts = ["\n".join(passages[i] for i in idx) for idx in indices]
```

## Workflow

1. Chunk Wikipedia articles into ~200-word passages
2. Encode passages with a sentence-transformer model
3. Build FAISS index (IndexFlatIP for cosine, IndexIVFFlat for scale)
4. At inference, encode questions and retrieve top-k passages
5. Format retrieved passages as context in the LLM prompt

## Key Decisions

- **Encoder choice**: MiniLM is fast; E5/BGE are more accurate for retrieval
- **Chunk size**: 200 words balances specificity vs coverage
- **Top-k**: 3-5 passages; more adds noise without helping
- **Index type**: Flat for <1M passages, IVF for larger corpora

## References

- Kaggle LLM Science Exam (Kaggle)
- Source: [platypus2-70b-with-wikipedia-rag](https://www.kaggle.com/code/simjeg/platypus2-70b-with-wikipedia-rag)
