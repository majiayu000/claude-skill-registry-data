---
name: evo-parallel-index-building
description: Provides utilities for parallelizing TF-IDF inverted index construction using a MapReduce approach - chunking documents, computing local TF and DF in worker processes, merging partial results, and finalizing TF-IDF scores with global DF.
---

# Parallel TF-IDF Index Building

## Overview
Parallelizes TF-IDF index construction using MapReduce:
1. **Chunk**: Split documents into chunks
2. **Map**: Workers compute local TF and DF per chunk
3. **Reduce**: Merge partial results (Counter.update for DF, dict.update for TF)
4. **Finalize**: Compute IDF and TF-IDF scores, build inverted index

## Key Formulas (matching sequential.py)
- TF(t,d) = count(t in d) / total_tokens(d)
- IDF(t) = log(N / df(t)) + 1
- TF-IDF = TF * IDF
- Posting lists sorted by score descending

## Usage
```python
import sys
sys.path.insert(0, '/app/environment/skills/evo-parallel-index-building/scripts')
from utils import (
    chunk_documents,
    map_index_chunk,
    merge_partial_results,
    finalize_tfidf_scores,
    build_tfidf_index_parallel,
    tokenize,
    compute_term_frequencies
)

# Build index
index_dict, elapsed, num_docs, vocab_size = build_tfidf_index_parallel(
    documents, num_workers=4, chunk_size=500
)
```

## Functions
- `chunk_documents(documents, chunk_size=500)` - Split docs into (doc_id, text) chunks
- `map_index_chunk(chunk)` - Worker: compute local TF dict and DF Counter
- `merge_partial_results(partial_results)` - Merge all local TF/DF/vocab
- `finalize_tfidf_scores(all_doc_tf, global_df, vocabulary, num_documents)` - Compute IDF and build inverted index
- `build_tfidf_index_parallel(documents, num_workers=None, chunk_size=500)` - Full pipeline
