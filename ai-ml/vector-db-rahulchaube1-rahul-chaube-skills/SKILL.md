---
name: vector-db
description: Index setups, embeddings models, distances metrics, and cosine similarity.
---

# Vector Db

Index setups, embeddings models, distances metrics, and cosine similarity.

## Core Guidelines

- **Index Optimization**: Use HNSW indices for faster similarity searches.
- **Metric Match**: Ensure the query metric (Cosine, L2, Dot Product) matches the embedding training parameters.
- **Metadata Filters**: Apply metadata pre-filtering to scope queries efficiently.
