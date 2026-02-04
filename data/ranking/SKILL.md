---
name: ranking
description: Ranks and scores retrieved documents based on similarity metrics from vector search. Use when sorting documents by relevance, prioritizing results, or when the user mentions ranking, scoring, or ordering documents.
---

# Document Ranking

## Instructions

Rank and score documents based on similarity metrics already computed by the Retrieval Agent. This skill operates on retrieved documents with distance/similarity information - it does NOT query ChromaDB again.

**Default workflow:**

1. Receive documents from Retrieval Agent (includes distance and similarity_score)
2. Call ranking functions to sort documents by relevance
3. Optionally filter by similarity threshold
4. Return ranked list for downstream processing (grading or generation)

**Key functions:**

```python
# Rank documents by similarity score (descending)
ranked_docs = rank_documents_by_similarity(documents)

# Rank documents by distance (ascending - lower is better)
ranked_docs = rank_documents_by_distance(documents)

# Filter documents by similarity threshold
filtered_docs = filter_by_similarity_threshold(documents, threshold=0.7)

# Get top-k ranked documents
top_docs = get_top_k_documents(ranked_docs, k=10)
```

**Similarity Metrics:**

Each document from Retrieval Agent contains:
- `distance`: Cosine distance from ChromaDB (lower = more similar)
  - Range: [0, 2] for cosine distance
  - 0 = identical, 2 = opposite
- `similarity_score`: Computed as `1 - distance` (higher = more similar)
  - Range: [-1, 1] for cosine
  - 1 = identical, -1 = opposite
  - Typical useful range: [0.5, 1.0]

**Ranking Strategies:**

1. **By Similarity Score (Recommended)**: Sort descending by `similarity_score`
   - Higher scores = more relevant
   - Intuitive: 0.9 > 0.7 > 0.5

2. **By Distance**: Sort ascending by `distance`
   - Lower distances = more relevant
   - Direct from vector search

3. **Hybrid with Collection Priority**: Rank by score within each collection, then merge

**Critical: NEVER query ChromaDB**

This skill operates on already-retrieved documents. The Retrieval Agent has already computed distances and similarity scores. Ranking simply sorts and filters based on these existing metrics.

**Implementation:** Functions should be in `components/ranker.py`, similar to `components/grader.py`.

## Examples

### Example 1: Basic ranking by similarity

```python
from components.ranker import rank_documents_by_similarity

# Input: Documents from Retrieval Agent
# Each has: document, metadata, distance, collection, similarity_score
documents = [
    {'document': 'Laptop A...', 'similarity_score': 0.85, 'distance': 0.15, ...},
    {'document': 'Laptop B...', 'similarity_score': 0.92, 'distance': 0.08, ...},
    {'document': 'Laptop C...', 'similarity_score': 0.73, 'distance': 0.27, ...},
]

# Rank by similarity (descending)
ranked = rank_documents_by_similarity(documents)

# Output: [Laptop B (0.92), Laptop A (0.85), Laptop C (0.73)]
```

### Example 2: Filter by threshold then rank

```python
from components.ranker import filter_by_similarity_threshold, rank_documents_by_similarity

# Input: 15 documents from 3 collections (5 each)
documents = retrieve_from_chromadb("gaming laptop", collections=["catalog", "faq", "troubleshooting"])

# Filter to only high-quality matches (similarity > 0.7)
high_quality = filter_by_similarity_threshold(documents, threshold=0.7)
# Reduced from 15 to 8 documents

# Rank the high-quality matches
ranked = rank_documents_by_similarity(high_quality)

# Output: 8 documents sorted by similarity, all > 0.7
```

### Example 3: Combined ranking and grading workflow

```python
from components.ranker import rank_documents_by_similarity, get_top_k_documents
from components.grader import grade_documents, filter_relevant_documents

# Step 1: Retrieve documents (done by Retrieval Agent)
retrieved_docs = await retrieval_agent.retrieve_documents("best laptop for video editing", top_k=5)
# Retrieved 15 documents (5 per collection)

# Step 2: Rank by similarity score
ranked_docs = rank_documents_by_similarity(retrieved_docs)

# Step 3: Take top 10 for grading (reduce cost)
top_docs = get_top_k_documents(ranked_docs, k=10)

# Step 4: Grade for binary relevance
graded_docs = grade_documents("best laptop for video editing", top_docs)
relevant_docs = filter_relevant_documents(graded_docs)

# Output: Only the most relevant documents (high similarity + graded as relevant)
```

### Example 4: Ranking within collections

```python
from components.ranker import rank_by_collection

# Input: Mixed documents from multiple collections
documents = retrieve_from_chromadb("laptop warranty", collections=["catalog", "faq"])

# Rank within each collection, then combine
ranked = rank_by_collection(documents)

# Output: {
#   'catalog': [doc1 (0.88), doc2 (0.75), doc3 (0.62)],
#   'faq': [doc4 (0.95), doc5 (0.91), doc6 (0.84)]
# }

# Use this to prioritize certain collections or balance results
```

## Distance vs Similarity Score

**When to use each:**

- **Similarity Score**: Easier to understand, use for thresholds and display
  - "Keep documents with similarity > 0.7"
  - "Top document has 92% similarity"

- **Distance**: Direct from vector search, use for debugging
  - "ChromaDB returned distance of 0.08"
  - "Check if distance < 0.3 for high confidence"

**Conversion:**
```python
similarity_score = 1 - distance
distance = 1 - similarity_score
```

**Typical thresholds:**
- similarity_score > 0.8: Very relevant
- similarity_score > 0.7: Relevant
- similarity_score > 0.5: Possibly relevant
- similarity_score < 0.5: Likely not relevant

## Integration with Grading

Ranking and grading serve different purposes:

- **Ranking**: Sorts documents by similarity score (continuous 0-1)
  - Fast, cheap (no API calls)
  - Based on vector similarity alone
  - Use for initial filtering and prioritization

- **Grading**: Binary relevance with reasoning (yes/no)
  - Slower, costs tokens (Claude API)
  - Semantic understanding of relevance
  - Use for final filtering before generation

**Recommended workflow:**
1. Retrieve documents (Retrieval Agent)
2. Rank by similarity (Ranking skill)
3. Take top-k to reduce grading cost
4. Grade for binary relevance (Grading skill)
5. Generate answer from relevant docs (Generator Agent)
