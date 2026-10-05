---
name: nlp-bucket-batching-seq2seq
description: Group variable-length sequences into length-sorted buckets before batching to minimize padding waste during seq2seq inference
domain: nlp
---

# Bucket Batching for Seq2Seq

## Overview

Naive batching pads all sequences to the longest in the batch, wasting compute on short inputs. Sort by length, split into buckets, then batch within each bucket. Reduces padding by 30-60% and stabilizes GPU memory usage.

## Quick Start

```python
from torch.utils.data import Sampler
import numpy as np

class BucketBatchSampler(Sampler):
    def __init__(self, lengths, batch_size, num_buckets=8, shuffle=False):
        sorted_idx = sorted(range(len(lengths)), key=lambda i: lengths[i])
        bsize = max(1, len(sorted_idx) // num_buckets)
        self.batches = []
        for b in range(num_buckets):
            start = b * bsize
            end = None if b == num_buckets - 1 else (b + 1) * bsize
            bucket = sorted_idx[start:end]
            if shuffle:
                np.random.shuffle(bucket)
            for i in range(0, len(bucket), batch_size):
                self.batches.append(bucket[i:i + batch_size])

    def __iter__(self):
        return iter(self.batches)

    def __len__(self):
        return len(self.batches)
```

## Key Decisions

- **num_buckets=8**: enough granularity without over-fragmenting
- **Sort within bucket only**: preserves some randomness across epochs if shuffled
- **Restore original order**: after inference, unsort results back to input order

## References

- Source: [lb-35-9-with-regex-corrections-public-model](https://www.kaggle.com/code/vitorhugobarbedo/lb-35-9-with-regex-corrections-public-model)
- Competition: Deep Past Challenge - Translate Akkadian to English
