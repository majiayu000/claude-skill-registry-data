---
name: embeddings
description: Computes semantic embeddings for text and measures distance between sentences. Use for semantic similarity analysis and comparing text.
allowed-tools: Bash, Read
---

# Embeddings Skill

This skill computes semantic embeddings for text and measures the semantic distance between sentences using sentence transformers.

## Instructions

To compute embeddings and measure distance:
1. Accept one or more sentences as input
2. Use the sentence-transformers library with the 'all-MiniLM-L6-v2' model
3. Compute embeddings (384-dimensional vectors)
4. Calculate cosine distance or Euclidean distance between embeddings
5. Return the distance metric

## What are Embeddings?

Embeddings are numerical vector representations of text that capture semantic meaning. Sentences with similar meanings have embeddings that are close together in vector space.

## Distance Metrics

### Cosine Distance
- Range: [0, 2]
- 0 = identical meaning
- 2 = opposite meaning
- Most commonly used for semantic similarity

### Euclidean Distance
- Range: [0, ∞)
- Measures straight-line distance in embedding space
- Sensitive to magnitude differences

## Python Code Usage

```python
import sys
sys.path.append('.claude/skills/embeddings')
from embedding_utils import (
    compute_embedding,
    cosine_distance,
    semantic_similarity
)

# Compute embeddings
sentence1 = "The cat sits on the mat"
sentence2 = "A feline rests on the rug"

emb1 = compute_embedding(sentence1)
emb2 = compute_embedding(sentence2)

# Calculate distance
distance = cosine_distance(emb1, emb2)
print(f"Semantic distance: {distance:.4f}")

# Or use the convenience function
distance = semantic_similarity(sentence1, sentence2, distance_metric='cosine')
```

## Usage Example

**Similar sentences:**
- Sentence 1: "The dog runs in the park"
- Sentence 2: "A canine sprints through the garden"
- Cosine Distance: ~0.15 (very similar)

**Different sentences:**
- Sentence 1: "The dog runs in the park"
- Sentence 2: "Quantum physics explains particle behavior"
- Cosine Distance: ~0.85 (very different)

## Functions Available

1. `compute_embedding(sentence)` - Get embedding vector for a sentence
2. `compute_embeddings_batch(sentences)` - Get embeddings for multiple sentences
3. `cosine_distance(emb1, emb2)` - Calculate cosine distance
4. `euclidean_distance(emb1, emb2)` - Calculate Euclidean distance
5. `semantic_similarity(sent1, sent2, metric)` - End-to-end similarity calculation

## Model Information

- Model: `all-MiniLM-L6-v2`
- Embedding dimensions: 384
- Performance: Fast and efficient
- Use case: General-purpose sentence embeddings

## Notes

- The model is loaded once and cached for efficiency
- Requires `sentence-transformers` package
- Works well for short texts (sentences, paragraphs)
- Language: Primarily English, with some multilingual capability
