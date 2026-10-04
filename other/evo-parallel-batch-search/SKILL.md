---
name: evo-parallel-batch-search
description: Provides utilities for parallelizing batch query search over a pre-built TF-IDF index using the worker initializer pattern to efficiently share the read-only index across worker processes.
---

# Parallel Batch Search

## Overview
Parallelizes batch query search using ProcessPoolExecutor with the
worker initializer pattern. The index is passed once per worker at
pool creation time (via initargs), avoiding repeated pickling.

## Worker Initializer Pattern
- `init_search_worker(index, documents, top_k)` sets module-level globals
- `worker_search_query(query)` reads those globals to perform search
- Each query is independent - perfect for data parallelism

## Usage
```python
import sys
sys.path.insert(0, '/app/environment/skills/evo-parallel-batch-search/scripts')
from utils import (
    init_search_worker,
    worker_search_query,
    batch_search_parallel
)

# Batch search
results, elapsed = batch_search_parallel(
    queries, index, top_k=10, num_workers=4, documents=docs
)
```

## Functions
- `init_search_worker(index_data, documents_data, top_k)` - Worker initializer
- `worker_search_query(query)` - Per-query search in worker process
- `batch_search_parallel(queries, index, top_k, num_workers, documents)` - Full pipeline
