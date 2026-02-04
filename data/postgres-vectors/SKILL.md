---
name: postgres-vectors
description: >-
  Use when working with embeddings, semantic similarity, vector search, or the
  <-> <#> <=> operators. Load for pgvector queries, HNSW index creation, 
  embedding storage, or similarity calculations. Covers distance operators,
  index strategies, and common pitfalls with 384-dimensional vectors.
---

# Postgres Vectors (pgvector)

Vector similarity search patterns for semantic matching.

> **Announce:** "I'm using postgres-vectors to implement vector similarity correctly."

## Vector Storage

Embeddings are stored in the `embeddings` table:

```sql
CREATE TABLE embeddings (
  id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  source_text text NOT NULL,
  embedding extensions.vector(384) NOT NULL,  -- 384 dimensions from gte-small
  created_at timestamptz DEFAULT now()
);

-- Unique constraint prevents duplicate embeddings
CREATE UNIQUE INDEX idx_embeddings_source_text 
ON embeddings (source_text);
```

**Key points:**
- Use `extensions.vector(384)` - pgvector is in extensions schema
- 384 dimensions matches gte-small model output
- Deduplicate by source_text

## Distance Operators

| Operator | Distance Type | Use Case |
|----------|---------------|----------|
| `<->` | L2 (Euclidean) | General purpose |
| `<#>` | Inner product (negative) | Normalized vectors (fastest) |
| `<=>` | Cosine distance | When normalization varies |

**For this project:** Use `<=>` (cosine) since we want similarity regardless of vector magnitude.

```sql
-- Cosine similarity = 1 - cosine_distance
SELECT 
  id,
  1 - (embedding <=> query_embedding) AS similarity
FROM embeddings
WHERE 1 - (embedding <=> query_embedding) > 0.5  -- 0.5 threshold
ORDER BY embedding <=> query_embedding  -- ASC for distance
LIMIT 10;
```

## Index Strategy

### When to Use HNSW

```sql
-- HNSW: Good recall, slightly slower builds
CREATE INDEX idx_embeddings_hnsw 
ON embeddings 
USING hnsw (embedding extensions.vector_cosine_ops)
WITH (m = 16, ef_construction = 64);
```

**Use HNSW when:**
- Table has >10,000 rows
- Accuracy matters more than build time
- Queries use cosine distance (`<=>`)

### When to Use IVFFlat

```sql
-- IVFFlat: Faster builds, requires tuning
CREATE INDEX idx_embeddings_ivfflat
ON embeddings
USING ivfflat (embedding extensions.vector_cosine_ops)
WITH (lists = 100);

-- Query with probes
SET ivfflat.probes = 10;
```

**Use IVFFlat when:**
- Rapid index rebuilds needed
- Willing to tune `lists` and `probes`

### This Project Uses HNSW

We prioritize accuracy for semantic matching.

## Common Patterns

### Find Similar Traits

```sql
-- Find traits similar to a query
SELECT 
  t.id,
  t.canonical_text,
  1 - (e.embedding <=> v_query_embedding) AS similarity
FROM traits t
JOIN embeddings e ON e.source_text = t.canonical_text
WHERE 1 - (e.embedding <=> v_query_embedding) > 0.6
ORDER BY e.embedding <=> v_query_embedding
LIMIT 20;
```

### Batch Similarity Calculation

```sql
-- Calculate similarity for multiple places at once
WITH place_similarities AS (
  SELECT 
    pt.place_id,
    1 - (e.embedding <=> v_description_embedding) AS trait_similarity
  FROM place_traits pt
  JOIN embeddings e ON e.id = pt.embedding_id
)
SELECT 
  place_id,
  AVG(trait_similarity) AS avg_similarity,
  MAX(trait_similarity) AS max_similarity
FROM place_similarities
GROUP BY place_id
ORDER BY avg_similarity DESC;
```

## Anti-Patterns

### DON'T: Filter After Ordering

```sql
-- WRONG: Index can't help with post-filter
SELECT * FROM embeddings
ORDER BY embedding <=> query
LIMIT 100
WHERE some_condition;  -- Filter after ORDER BY

-- CORRECT: Filter first, then order
SELECT * FROM embeddings
WHERE some_condition
ORDER BY embedding <=> query
LIMIT 100;
```

### DON'T: Use Wrong Operator for Index

```sql
-- WRONG: Index is cosine_ops but query uses L2
CREATE INDEX ... USING hnsw (embedding vector_cosine_ops);
SELECT * FROM embeddings ORDER BY embedding <-> query;  -- L2!

-- CORRECT: Match operator to index
SELECT * FROM embeddings ORDER BY embedding <=> query;  -- Cosine
```

### DON'T: Forget the Extensions Schema

```sql
-- WRONG: Will fail
embedding vector(384)

-- CORRECT: Prefix with extensions
embedding extensions.vector(384)
```

## Generating Embeddings

Embeddings come from edge function, stored via database function:

```sql
-- Called by edge function after generating embedding
INSERT INTO embeddings (source_text, embedding)
VALUES (v_text, v_embedding)
ON CONFLICT (source_text) DO UPDATE 
SET embedding = EXCLUDED.embedding;
```

## References

See `references/similarity-queries.md` for more query examples.
