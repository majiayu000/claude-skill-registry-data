---
name: nlp-lda-topic-modeling
description: Latent Dirichlet Allocation on CountVectorizer bag-of-words to discover latent topics with per-document topic distributions for feature engineering or EDA
---

# LDA Topic Modeling

## Overview

Latent Dirichlet Allocation discovers latent topics in a text corpus. Each document is modeled as a mixture of topics, each topic as a distribution over words. Fit LDA on a CountVectorizer bag-of-words matrix to extract topic distributions per document — usable as features for downstream models or for understanding corpus structure.

## Quick Start

```python
from sklearn.decomposition import LatentDirichletAllocation
from sklearn.feature_extraction.text import CountVectorizer
import numpy as np

cvec = CountVectorizer(min_df=4, max_features=50000,
                       ngram_range=(1, 2), stop_words='english')
bow = cvec.fit_transform(texts)

lda = LatentDirichletAllocation(
    n_components=20, learning_method='online',
    max_iter=20, random_state=42)
topic_dist = lda.fit_transform(bow)  # shape: (n_docs, n_topics)

vocab = cvec.get_feature_names_out()
for i, topic in enumerate(lda.components_):
    top_words = [vocab[j] for j in topic.argsort()[:-11:-1]]
    print(f"Topic {i}: {', '.join(top_words)}")
```

## Workflow

1. Build bag-of-words with `CountVectorizer` (not TF-IDF — LDA expects raw counts)
2. Fit LDA with `learning_method='online'` for large corpora
3. `fit_transform` returns per-document topic distributions (features)
4. Inspect `lda.components_` to label topics by their top words
5. Append topic distributions as features to the original dataset

## Key Decisions

- **n_components**: 10-30 for EDA, tune via coherence score for production
- **CountVectorizer not TfidfVectorizer**: LDA's generative model assumes word counts
- **online vs batch**: online is faster for large datasets, batch is more accurate
- **min_df**: 3-5 removes rare terms that create noise topics

## References

- [Mercari Interactive EDA + Topic Modelling](https://www.kaggle.com/code/thykhuely/mercari-interactive-eda-topic-modelling)
