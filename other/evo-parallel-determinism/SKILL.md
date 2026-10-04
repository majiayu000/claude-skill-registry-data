---
name: evo-parallel-determinism
description: Provides patterns and utilities to ensure parallel TF-IDF results are identical to the sequential baseline, addressing floating-point ordering, tie-breaking, and pickling compatibility.
---

# Parallel Determinism

## Overview
Ensures parallel results match sequential exactly by handling:
- Floating-point accumulation order
- Tie-breaking in result sorting
- Pickling compatibility for multiprocessing
- Safe context selection (fork vs spawn)

## Key Principles
1. **FP Ordering**: Iterate query terms in same order as sequential (dict insertion order)
2. **Tie-breaking**: Sort by (-score, doc_id) for deterministic ordering
3. **Pickling**: Define NamedTuples/dataclasses at module level
4. **Context**: Use 'fork' on Linux for performance (copy-on-write)

## Usage
```python
import sys
sys.path.insert(0, '/app/environment/skills/evo-parallel-determinism/scripts')
from utils import (
    deterministic_score_accumulation,
    stable_sort_results,
    get_safe_mp_context
)
```

## Functions
- `deterministic_score_accumulation(query_vector, doc_vector)` - FP-safe dot product
- `stable_sort_results(results)` - Sort with deterministic tie-breaking
- `get_safe_mp_context()` - Get appropriate multiprocessing context
