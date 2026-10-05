---
name: nlp-tfidf-to-boolean-query
description: >
  Converts TF-IDF top-k terms into field-scoped boolean OR queries for structured document retrieval from a full-text index.
---
# TF-IDF to Boolean Query

## Overview

Full-text search engines accept boolean queries (term1 OR term2 AND field:term3), but choosing which terms to include is non-trivial. This technique uses TF-IDF to rank vocabulary terms by importance, selects the top-k, qualifies each with its source field (title, abstract, classification code), and joins them into a boolean OR query. The result is a structured, field-aware query derived from the document's own content — useful for prior art search, duplicate detection, and similar-document retrieval.

## Quick Start

```python
from sklearn.feature_extraction.text import TfidfVectorizer
import numpy as np

def select_top_k(tfidf_matrix, k=10):
    """Select top-k globally important terms by column sum."""
    col_sums = np.asarray(tfidf_matrix.sum(axis=0)).flatten()
    top_indices = np.argsort(-col_sums)[:k]
    return top_indices

def build_boolean_query(doc_text, cpc_codes, ti_tfidf, cpc_tfidf, k=10):
    """Build a field-scoped boolean OR query from TF-IDF top-k."""
    # Get top-k title terms
    ti_matrix = ti_tfidf.transform([doc_text])
    ti_indices = select_top_k(ti_matrix, k)
    ti_terms = ti_tfidf.get_feature_names_out()[ti_indices]

    # Get top-k CPC codes
    cpc_matrix = cpc_tfidf.transform([cpc_codes])
    cpc_indices = select_top_k(cpc_matrix, k)
    cpc_terms = cpc_tfidf.get_feature_names_out()[cpc_indices]

    # Build field-qualified query
    parts = [f"ti:{t}" for t in ti_terms] + [f"cpc:{c}" for c in cpc_terms]
    return " OR ".join(parts)

# Fit TF-IDF on corpus, then build queries
ti_tfidf = TfidfVectorizer(max_features=5000).fit(titles)
cpc_tfidf = TfidfVectorizer(analyzer='word').fit(cpc_strings)
query = build_boolean_query(doc_title, doc_cpc, ti_tfidf, cpc_tfidf)
# → "ti:neural OR ti:network OR cpc:G06F OR cpc:H04L"
```

## Workflow

1. Fit TF-IDF vectorizers on the corpus (one per field: title, abstract, CPC, etc.)
2. For each query document, transform and select top-k terms per field
3. Prefix each term with its field name (`ti:`, `abs:`, `cpc:`)
4. Join with `OR` to form the boolean query
5. Execute against a full-text index (Whoosh, Elasticsearch)

## Key Decisions

- **k per field**: 10 title terms + 10 CPC codes is a good start; tune by retrieval metric
- **Field weights**: Title terms are more discriminative than abstract terms — use fewer abstract terms
- **Token budget**: Some search systems limit query tokens (e.g., 50) — truncate lowest-ranked terms
- **Combines with SA**: Use TF-IDF top-k as candidate set, then simulated annealing to select optimal subset

## References

- [USPTO - Annealing [LB = 0.31]](https://www.kaggle.com/code/andrey67/uspto-annealing-lb-0-31)
- [USPTO-Simulated-Annealing-Baseline](https://www.kaggle.com/code/tubotubo/uspto-simulated-annealing-baseline)
