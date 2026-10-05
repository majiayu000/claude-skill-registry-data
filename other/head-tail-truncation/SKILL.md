---
name: nlp-head-tail-truncation
description: >
  Preserves both the start and end of long text sequences when truncating for transformer input limits.
---
# Head-Tail Truncation

## Overview

Standard BERT truncation drops tokens from the end, losing potentially important closing content. Head-tail truncation keeps the first N and last M tokens, discarding the middle. This preserves both the introduction and conclusion of long documents, which often carry the most signal.

## Quick Start

```python
def head_tail_truncate(token_ids, max_length, head_ratio=0.5):
    """Keep head and tail tokens, drop the middle.

    Args:
        token_ids: list of token IDs (without special tokens)
        max_length: maximum allowed tokens (excluding [CLS]/[SEP])
        head_ratio: fraction of budget allocated to head

    Returns:
        truncated token ID list
    """
    if len(token_ids) <= max_length:
        return token_ids

    head_len = int(max_length * head_ratio)
    tail_len = max_length - head_len
    return token_ids[:head_len] + token_ids[-tail_len:]
```

## Workflow

1. Tokenize input text into subword tokens
2. If length exceeds budget, split budget between head and tail
3. Concatenate head tokens + tail tokens
4. Add special tokens ([CLS], [SEP]) around the result
5. For multi-segment inputs, apply per-segment or with shared budget

## Key Decisions

- **Head ratio**: 0.5 is default; bias toward head for Q&A, toward tail for conclusions
- **Per-segment budgets**: For question+answer pairs, allocate separate budgets per segment
- **vs sliding window**: Head-tail is simpler and often sufficient; sliding window adds complexity
- **Middle content**: If middle matters (e.g., evidence paragraphs), use hierarchical encoding instead

## References

- Google QUEST Q&A Labeling competition, 1st place solution (Kaggle)
- Source: [1st-place-solution](https://www.kaggle.com/code/ddanevskyi/1st-place-solution)
