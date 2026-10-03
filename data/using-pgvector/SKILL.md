---
name: using-pgvector
description: Postgres-native vector storage with the pgvector extension — vector/halfvec/sparsevec types, HNSW/IVFFlat indexes, hybrid relational+similarity queries.
when_to_use: >
  Reach for this when the project already runs Postgres and wants to store embeddings alongside
  relational data without adding a dedicated vector store. For a managed/standalone vector DB use
  using-weaviate; for app-side TypeScript access to the same Postgres use using-prisma; for the
  end-to-end RAG architecture above the store (chunking, retrieval strategy, reranking, eval) use
  building-rag-pipelines; for the embedding model choice itself defer to the provider skill
  (using-openai-platform / using-anthropic-platform). **ALWAYS WebFetch
  https://github.com/pgvector/pgvector and the releases page BEFORE recommending an index type,
  operator class, distance op, or version-gated feature — pgvector adds capabilities (halfvec,
  sparsevec, binary quantization, iterative scans) faster than any training snapshot, and
  index/operator availability is strictly version-gated.**
allowed-tools: Read, Write, Edit, Bash, Grep, Glob
paths:
  - "prisma/schema.prisma"
  - "**/migrations/**/*.sql"
  - "**/*.sql"
---

# pgvector — Postgres Vector Search Quick Reference

Store and query embeddings inside Postgres using the `pgvector` extension. Combines vector
similarity (HNSW / IVFFlat) with native SQL filtering, joins, and transactions — no second
datastore required.

---

## Stay current — DO NOT rely on training-data knowledge of pgvector features or operators

pgvector ships new types (`halfvec`, `sparsevec`, `bit`), index improvements (HNSW, iterative
index scans, binary quantization), and operator classes on a fast cadence. Operator availability
is strictly version-gated; the wrong version + wrong opclass combo silently falls back to a
sequential scan. **Before** you (a) recommend a version, (b) pick an index type, (c) choose a
distance operator, (d) use halfvec/sparsevec/binary quantization, or (e) cite tuning defaults,
you **MUST** WebFetch the live sources and cite them:

- **Project README (canonical reference for types, operators, indexes, tuning):**
  https://github.com/pgvector/pgvector
- **Release notes / changelog (version-gated features):**
  https://github.com/pgvector/pgvector/blob/master/CHANGELOG.md
- **GitHub releases page:** https://github.com/pgvector/pgvector/releases
- **Postgres docs for index planner / `EXPLAIN`:** https://www.postgresql.org/docs/current/

In your deliverables, cite the source URL and the date you fetched it for every operator,
opclass, or tuning recommendation. **Trust the fetch over the snapshot.** For the embedding
model itself, defer to the provider skill's Stay-current. For RAG architecture (chunking,
retrieval, reranking), see `building-rag-pipelines`.

---

## When to Use

Load this skill when:
- `CREATE EXTENSION vector` in a migration
- `pgvector` Python package or `pgvector` npm package in dependencies
- `vector(...)` column type in a Postgres schema
- The project already uses Postgres and a new requirement adds embeddings/similarity search
- You see `<->`, `<=>`, or `<#>` operators in SQL

---

## Install & Enable

```sql
-- One-time per database
CREATE EXTENSION IF NOT EXISTS vector;
```

Managed Postgres support (verify current list via WebFetch):
- Supabase, Neon, AWS RDS/Aurora, Google Cloud SQL/AlloyDB, Azure Database for PostgreSQL.

---

## Types

| Type | Bytes/dim | Use for |
|------|-----------|---------|
| `vector(N)` | 4 (float32) | Default; most embedding models output float32 |
| `halfvec(N)` | 2 (float16) | Halve storage; minor recall loss; great for HNSW at scale |
| `sparsevec(N)` | variable | Sparse embeddings (SPLADE-style, BM25-derived) |
| `bit(N)` | 1/8 | Binary-quantized embeddings (very fast, lossy) |

> Verify type availability against your installed pgvector version — WebFetch the changelog.

---

## Distance Operators

| Operator | Distance | Use when |
|----------|----------|----------|
| `<->` | L2 / Euclidean | Geometric distance |
| `<=>` | Cosine | Most embedding models (OpenAI, Cohere, etc.) — most common |
| `<#>` | Negative inner product | Inner product (negated so smaller = closer) |
| `<+>` | L1 / Manhattan | Newer; verify availability in your version |

**Each operator needs a matching index opclass** (e.g. `vector_cosine_ops`). Mismatched =
sequential scan. Verify your index uses the same opclass as your queries.

---

## Schema Patterns

### Single-table embedding column

```sql
CREATE TABLE documents (
    id          bigserial PRIMARY KEY,
    tenant_id   uuid NOT NULL,
    title       text,
    body        text,
    embedding   vector(1536),         -- e.g. text-embedding-3-small
    created_at  timestamptz DEFAULT now()
);
```

### Separate chunk table (RAG-friendly)

```sql
CREATE TABLE doc_chunks (
    id          bigserial PRIMARY KEY,
    document_id bigint NOT NULL REFERENCES documents(id) ON DELETE CASCADE,
    chunk_index int NOT NULL,
    content     text NOT NULL,
    embedding   vector(1536),
    metadata    jsonb DEFAULT '{}',
    UNIQUE (document_id, chunk_index)
);
```

Why separate: chunk strategy can change without rewriting documents; deletes cascade cleanly.

---

## Indexes — HNSW vs IVFFlat

| | HNSW | IVFFlat |
|---|------|---------|
| Build time | Slow | Fast |
| Query speed | Fast | Fast (after warm) |
| Recall | High | Moderate (tunable) |
| Updates | Good (incremental) | Poor (rebuild for best recall) |
| Memory | Higher | Lower |
| Default choice | **Yes for most workloads** | When build time / memory matters |

### HNSW (recommended default)

```sql
CREATE INDEX ON doc_chunks
USING hnsw (embedding vector_cosine_ops)
WITH (m = 16, ef_construction = 64);

-- Query-time recall/speed knob:
SET hnsw.ef_search = 100;       -- higher = better recall, slower
```

### IVFFlat

```sql
-- lists ≈ rows / 1000  (rule of thumb; verify via current docs)
CREATE INDEX ON doc_chunks
USING ivfflat (embedding vector_cosine_ops)
WITH (lists = 100);

SET ivfflat.probes = 10;        -- higher = better recall, slower
```

**Critical**: IVFFlat needs data present *before* index creation for good cluster centroids.
HNSW does not.

### halfvec index (storage savings)

```sql
ALTER TABLE doc_chunks ADD COLUMN embedding_h halfvec(1536);
UPDATE doc_chunks SET embedding_h = embedding::halfvec(1536);
CREATE INDEX ON doc_chunks USING hnsw (embedding_h halfvec_cosine_ops);
```

---

## Query Patterns

### Top-k nearest neighbors

```sql
SELECT id, content, embedding <=> $1 AS distance
FROM doc_chunks
ORDER BY embedding <=> $1
LIMIT 10;
```

`$1` is a `vector(1536)`-typed parameter (the query embedding).

### Hybrid: relational filter + vector similarity

```sql
SELECT c.id, c.content, c.embedding <=> $1 AS distance
FROM doc_chunks c
JOIN documents  d ON d.id = c.document_id
WHERE d.tenant_id = $2
  AND d.created_at > now() - interval '90 days'
ORDER BY c.embedding <=> $1
LIMIT 20;
```

**Watch out**: a WHERE clause that eliminates most rows can cause the planner to skip the index.
Verify with `EXPLAIN (ANALYZE, BUFFERS)`. Recent pgvector versions support *iterative index
scans* that re-scan when the filter is selective — WebFetch the changelog to confirm support in
your version.

### Hybrid keyword + vector (RRF)

```sql
WITH vec AS (
  SELECT id, ROW_NUMBER() OVER (ORDER BY embedding <=> $1) AS rank
  FROM doc_chunks ORDER BY embedding <=> $1 LIMIT 50
),
kw AS (
  SELECT id, ROW_NUMBER() OVER (ORDER BY ts_rank(to_tsvector('english', content),
                                                 plainto_tsquery('english', $2)) DESC) AS rank
  FROM doc_chunks
  WHERE to_tsvector('english', content) @@ plainto_tsquery('english', $2)
  LIMIT 50
)
SELECT id, SUM(1.0 / (60 + rank)) AS rrf
FROM (SELECT id, rank FROM vec UNION ALL SELECT id, rank FROM kw) u
GROUP BY id ORDER BY rrf DESC LIMIT 10;
```

This is Reciprocal Rank Fusion — combine sparse + dense without normalizing scores.

---

## Client Integration

### Python — raw `psycopg` + `pgvector`

```python
import psycopg
from pgvector.psycopg import register_vector

with psycopg.connect(DSN) as conn:
    register_vector(conn)
    with conn.cursor() as cur:
        cur.execute(
            "SELECT id, content FROM doc_chunks ORDER BY embedding <=> %s LIMIT %s",
            (query_embedding, 10),
        )
        rows = cur.fetchall()
```

### Python — SQLAlchemy

```python
from sqlalchemy import Column, Integer, Text
from sqlalchemy.orm import declarative_base
from pgvector.sqlalchemy import Vector

Base = declarative_base()

class Chunk(Base):
    __tablename__ = "doc_chunks"
    id = Column(Integer, primary_key=True)
    content = Column(Text)
    embedding = Column(Vector(1536))

# Query
results = (
    session.query(Chunk)
    .order_by(Chunk.embedding.cosine_distance(query_embedding))
    .limit(10)
    .all()
)
```

### TypeScript — Prisma

Prisma's first-class `vector` support is evolving; current pattern uses `Unsupported("vector")`
plus raw queries. **Verify against current Prisma docs.**

```prisma
model DocChunk {
  id         Int                       @id @default(autoincrement())
  content    String
  embedding  Unsupported("vector(1536)")?
}
```

```typescript
const results = await prisma.$queryRaw<Array<{ id: number; content: string }>>`
  SELECT id, content
  FROM "DocChunk"
  ORDER BY embedding <=> ${queryEmbedding}::vector
  LIMIT 10
`;
```

See `using-prisma` for migration patterns and `$queryRaw` typing.

### TypeScript — node-postgres + pgvector

```typescript
import pg from 'pg';
import pgvector from 'pgvector/pg';

const client = new pg.Client({ connectionString: process.env.DATABASE_URL });
await client.connect();
await pgvector.registerTypes(client);

const { rows } = await client.query(
  'SELECT id, content FROM doc_chunks ORDER BY embedding <=> $1 LIMIT $2',
  [pgvector.toSql(queryEmbedding), 10]
);
```

---

## Common Patterns

- **Backfill embeddings in batches.** `UPDATE ... WHERE embedding IS NULL LIMIT N` in a loop;
  commit per batch; index AFTER backfill for IVFFlat, BEFORE or after for HNSW.
- **Store the embedding model + version in a sibling column** so you can re-embed without
  losing track of mixed-version data.
- **Always normalize dimension** in the column type (`vector(1536)` not `vector`); mismatches
  fail at insert time, not query time.
- **Use `halfvec` when vectors > ~5M rows** and you can tolerate ~1% recall drop.
- **Add a composite index** for tenant-scoped queries: `(tenant_id) INCLUDE (embedding)` is NOT
  useful — you want the vector index plus the planner to filter first. Measure with `EXPLAIN`.

---

## Anti-Patterns

- **Mixing distance operator and opclass.** `vector_l2_ops` index + `<=>` query = seq scan.
- **Creating IVFFlat index on an empty table.** Centroids are garbage; recall tanks.
- **Storing embeddings without the dimension in the type.** `vector` (no N) bypasses checks.
- **Round-tripping through float64.** Most clients handle float32; explicit casts add latency.
- **Re-embedding the corpus on every query.** Embed once at ingest, cache the query vector.
- **Ignoring `EXPLAIN ANALYZE`.** The only way to confirm the index is actually used.

---

## See Also

- `using-weaviate` — dedicated vector DB alternative; choose this for very large scale or
  multi-tenant SaaS isolation patterns.
- `using-prisma` — TypeScript ORM patterns for the same Postgres database.
- `building-rag-pipelines` — chunking, retrieval strategy, reranking, evaluation above the store.
- `using-openai-platform` / `using-anthropic-platform` — embedding model selection and pricing.
- `managing-supabase` — when Postgres is hosted on Supabase (pgvector is enabled by default).
