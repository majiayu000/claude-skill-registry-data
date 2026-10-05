---
name: nlp-mbr-decoding-reranking
description: Minimum Bayes Risk decoding — select the candidate with highest average chrF++ agreement against all others in the pool
domain: nlp
---

# MBR Decoding Reranking

## Overview

Instead of picking the single highest-probability beam, generate a pool of candidates and select the one most agreed-upon by the others. Uses chrF++ (character F-score with word bigrams) as the utility metric. Consistently outperforms pure beam search for translation tasks.

## Quick Start

```python
import sacrebleu
import numpy as np

def mbr_select(candidates, pool_cap=32):
    metric = sacrebleu.metrics.CHRF(word_order=2)
    unique = list(dict.fromkeys(c.strip() for c in candidates if c.strip()))
    pool = unique[:pool_cap]
    n = len(pool)
    if n <= 1:
        return pool[0] if pool else ""
    scores = np.zeros(n)
    for i in range(n):
        for j in range(n):
            if i != j:
                scores[i] += metric.sentence_score(pool[i], [pool[j]]).score
        scores[i] /= (n - 1)
    return pool[int(np.argmax(scores))]
```

## Key Decisions

- **chrF++ over BLEU**: more robust at sentence level, handles morphologically rich languages better
- **Pool cap**: 32 candidates balances quality vs O(n^2) pairwise cost
- **Deduplicate first**: removes exact duplicates before scoring to avoid self-reinforcing bias
- **Combine with multi-temperature sampling**: MBR needs diverse candidates to work well

## References

- Source: [lb-35-9-with-regex-corrections-public-model](https://www.kaggle.com/code/vitorhugobarbedo/lb-35-9-with-regex-corrections-public-model)
- Source: [hybrid-best-akkadian](https://www.kaggle.com/code/meenalsinha/hybrid-best-akkadian)
- Competition: Deep Past Challenge - Translate Akkadian to English
