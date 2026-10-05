---
name: nlp-text-overlap-features
description: >
  Computes n-gram overlap counts/ratios and NER entity overlap between reference and generated text as features.
---
# Text Overlap Features

## Overview

For tasks comparing two texts (summary vs. source, answer vs. reference), compute lexical overlap at multiple granularities: word-level, bigram, trigram, and named entity overlap. These features capture surface-level relevance that complements transformer embeddings.

## Quick Start

```python
import spacy
from collections import Counter

nlp = spacy.load("en_core_web_sm")

def ngram_overlap(text_a, text_b, n=2):
    tokens_a = text_a.lower().split()
    tokens_b = text_b.lower().split()
    ngrams_a = set(zip(*[tokens_a[i:] for i in range(n)]))
    ngrams_b = set(zip(*[tokens_b[i:] for i in range(n)]))
    overlap = ngrams_a & ngrams_b
    ratio = len(overlap) / max(len(ngrams_b), 1)
    return len(overlap), ratio

def ner_overlap(text_a, text_b):
    ents_a = {(e.text, e.label_) for e in nlp(text_a).ents}
    ents_b = {(e.text, e.label_) for e in nlp(text_b).ents}
    common = ents_a & ents_b
    return len(common), dict(Counter(e[1] for e in common))
```

## Workflow

1. Compute word overlap count and ratio
2. Compute bigram and trigram overlap counts and ratios
3. Extract NER entities from both texts, compute intersection by type
4. Combine all features into a feature vector for GBDT or stacking

## Key Decisions

- **Multiple n-gram scales**: Unigrams catch keywords; trigrams catch phrases
- **Ratios vs counts**: Normalize by summary length to handle variable-length inputs
- **NER by type**: PERSON, ORG, DATE overlaps may have different importance
- **Complement to embeddings**: These features are fast and interpretable

## References

- CommonLit - Evaluate Student Summaries (Kaggle)
- Source: [tuned-debertav3-lgbm-autocorrect](https://www.kaggle.com/code/cody11null/tuned-debertav3-lgbm-autocorrect)
