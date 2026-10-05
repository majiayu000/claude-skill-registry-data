---
name: nlp-adjacent-span-merging
description: >
  Merges nearby predicted NER spans of the same class within a word-distance threshold into single coherent segments.
---
# Adjacent Span Merging

## Overview

Token-level NER models often fragment a single discourse element into multiple adjacent spans — a long "Evidence" paragraph gets split into two or three pieces. Adjacent span merging fixes this by joining same-class spans that are within a configurable word-distance gap. This is especially important for long-document NER where discourse elements span many sentences.

## Quick Start

```python
def merge_adjacent_spans(predictions, max_gap=1, merge_classes=None):
    """Merge nearby same-class spans within max_gap words.

    Args:
        predictions: list of (doc_id, class, word_indices_str)
        max_gap: max word-index gap to merge across
        merge_classes: set of classes to merge (None = all)
    Returns:
        list of merged (doc_id, class, word_indices_str)
    """
    from collections import defaultdict
    by_doc_class = defaultdict(list)
    for doc_id, cls, pred_str in predictions:
        words = sorted(int(x) for x in pred_str.split())
        by_doc_class[(doc_id, cls)].append(words)

    merged = []
    for (doc_id, cls), spans in by_doc_class.items():
        if merge_classes and cls not in merge_classes:
            for s in spans:
                merged.append((doc_id, cls, " ".join(map(str, s))))
            continue
        # Sort spans by start position
        all_words = sorted(set(w for s in spans for w in s))
        # Split into groups by gap
        groups = [[all_words[0]]]
        for w in all_words[1:]:
            if w - groups[-1][-1] <= max_gap:
                groups[-1].append(w)
            else:
                groups.append([w])
        for g in groups:
            merged.append((doc_id, cls, " ".join(map(str, g))))
    return merged
```

## Workflow

1. Group predictions by (document_id, class)
2. Sort word indices across all spans of the same class
3. Walk through sorted indices; if gap between consecutive words <= max_gap, merge
4. Otherwise start a new span
5. Optionally limit merging to specific classes (e.g., only "Evidence")

## Key Decisions

- **max_gap**: 1-2 for tight merging; higher values risk over-merging distinct spans
- **Selective classes**: Only merge classes known to fragment (long spans like Evidence)
- **Max merged length**: Optionally cap merged span length to prevent runaway merging
- **Order**: Apply merging before length/probability filtering

## References

- [Two Longformers Are Better Than 1](https://www.kaggle.com/code/abhishek/two-longformers-are-better-than-1)
