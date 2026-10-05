---
name: cv-phash-duplicate-grouping
description: Group near-duplicate images by perceptual hash (pHash) as a zero-cost baseline signal for product or image matching
domain: cv
---

# Perceptual Hash Duplicate Grouping

## Overview

Perceptual hashing (pHash) produces a compact fingerprint that is identical for visually similar images regardless of resolution or minor edits. Group items sharing the same hash to find near-duplicates without any model inference. Use as a cheap baseline or combine with learned embeddings for higher recall.

## Quick Start

```python
import pandas as pd

def phash_group_matches(df, hash_col='image_phash', id_col='posting_id'):
    """Group items by perceptual hash.
    
    Args:
        df: DataFrame with hash and ID columns
        hash_col: column containing perceptual hash strings
        id_col: column containing item identifiers
    Returns:
        Series mapping each item to its hash-group matches
    """
    hash_groups = df.groupby(hash_col)[id_col].agg(list).to_dict()
    return df[hash_col].map(hash_groups)

# Usage
df['phash_matches'] = phash_group_matches(df)

# Compute hash if not provided
from PIL import Image
import imagehash
df['image_phash'] = df['image_path'].apply(
    lambda p: str(imagehash.phash(Image.open(p)))
)
```

## Key Decisions

- **Zero compute cost**: no GPU needed — hash lookup is O(1) per item
- **High precision, low recall**: only catches near-exact duplicates; combine with KNN for broader matches
- **Hash function**: pHash is robust to resizing/compression; use dHash for rotation invariance
- **Hamming distance**: for fuzzy matching, compare hash bit distance instead of exact equality

## References

- Source: [part-2-rapids-tfidfvectorizer-cv-0-700](https://www.kaggle.com/code/cdeotte/part-2-rapids-tfidfvectorizer-cv-0-700)
- Competition: Shopee - Price Match Guarantee
