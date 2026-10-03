---
name: pgvector-rag-beamix
last_updated: 2026-05-17
description: "Querying Beamix's five RAG corpora stored in Supabase pgvector: DECISIONS, sessions, codebase, brain, and skills. Use when any CEO, CTO, or Research-Lead agent needs semantic search over internal knowledge during pre-flight or research."
tags: [rag, beamix-specific, database, ai, memory]
source: beamix-authored 2026-05-16
risk: low
---

# pgvector RAG — Beamix

## Quick reference

> pgvector for product-domain RAG only (scan corpora, competitor docs). Mem0 owns agent-to-agent state. ivfflat lists = sqrt(N).

## When to use

- Pre-flight: "Has this architectural decision been made before?"
- Research-Lead synthesizing across session history
- CTO checking whether a migration pattern exists in the codebase corpus
- CEO cross-referencing past board meeting outputs

## When NOT to use

- For real-time product data (use Supabase MCP with `execute_sql` instead)
- When you need the exact current source file (use Read or Glob — RAG gives semantic proximity, not file state)
- Workers do not have pgvector MCP grant — this is leads/CEO only

## The five corpora

| Corpus name | Source | Re-embedded by | Freshness |
|-------------|--------|---------------|-----------|
| `decisions` | `.claude/memory/DECISIONS.md` | Inngest `embed-decisions` on git push | Near-real-time |
| `sessions` | `docs/08-agents_work/sessions/**` | Inngest `embed-sessions` on git push (incremental) | Near-real-time |
| `codebase` | `apps/web/src/**` | Inngest `embed-codebase` on PR merge to `main` | Merge-time |
| `brain` | `docs/00-brain/**` | Inngest `embed-brain` on git push | Near-real-time |
| `skills` | `.claude/skills/**` | Inngest `embed-skills` on git push | Near-real-time |

## Embedding model

All corpora use `text-embedding-3-small` (OpenAI) with 1536 dimensions. Chunking: 512 tokens per chunk, 50-token overlap. Index type: `ivfflat` with `lists = 100`.

## Query patterns

### Basic semantic search

```typescript
// Query the decisions corpus
const results = await pgvectorQuery({
  corpus: 'decisions',
  query: 'which billing provider did we choose',
  topK: 5,
});

// Results shape:
// [{ chunk_text: string, similarity: number, source_file: string, chunk_index: number }]
```

### Hybrid search (vector + keyword)

Use hybrid when you need high precision on known terms (agent names, ticket IDs, table names).

```typescript
const results = await pgvectorHybridQuery({
  corpus: 'codebase',
  vectorQuery: 'scan rate limiting middleware',
  keywordFilter: 'scan_rate_limit',  // PostgreSQL text search filter
  topK: 10,
  rrf_k: 60,  // Reciprocal Rank Fusion constant
});
```

### Raw SQL via Supabase MCP

When the custom MCP is unavailable, fall back to direct SQL:

```sql
-- Semantic search over codebase corpus
SELECT
  chunk_text,
  source_file,
  1 - (embedding <=> query_embedding) AS similarity
FROM rag_corpus
WHERE corpus = 'codebase'
ORDER BY embedding <=> '[...1536 floats...]'
LIMIT 10;
```

### Multi-corpus query (Research-Lead pattern)

When synthesizing across domains, query all five corpora in parallel, then merge by similarity score:

```typescript
const [decisions, sessions, codebase] = await Promise.all([
  pgvectorQuery({ corpus: 'decisions', query: topic, topK: 3 }),
  pgvectorQuery({ corpus: 'sessions', query: topic, topK: 3 }),
  pgvectorQuery({ corpus: 'codebase', query: topic, topK: 3 }),
]);

const merged = [...decisions, ...sessions, ...codebase]
  .sort((a, b) => b.similarity - a.similarity)
  .slice(0, 8);
```

## rag_corpus table schema

```sql
CREATE TABLE rag_corpus (
  id           uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  corpus       text NOT NULL,         -- 'decisions' | 'sessions' | 'codebase' | 'brain' | 'skills'
  source_file  text NOT NULL,         -- original file path
  chunk_index  int NOT NULL,
  chunk_text   text NOT NULL,
  embedding    vector(1536),
  created_at   timestamptz DEFAULT now(),
  updated_at   timestamptz DEFAULT now()
);

CREATE INDEX ON rag_corpus USING ivfflat (embedding vector_cosine_ops) WITH (lists = 100);
CREATE INDEX ON rag_corpus (corpus, source_file);  -- filter fast before vector scan
```

## Confidence and freshness caveats

- `codebase` corpus reflects state at last `main` merge — never use it to assert "the file currently does X"
- `decisions` corpus is near-real-time but always read `DECISIONS.md` directly for the authoritative record
- Similarity < 0.7 = weak match; cite with confidence: low
- Never synthesize a claim from RAG alone without cross-checking the source file for critical decisions

## See also

- `mem0-patterns` — [[mem0-patterns]]
- `embedding-strategies` — [[embedding-strategies]]
- `rag-engineer` — [[rag-engineer]]
- `vector-database-engineer` — [[vector-database-engineer]]

## Anti-patterns

- Using RAG instead of `Read` when you need the exact current file state
- Querying `topK > 15` (bloats context; similarity degrades)
- Skipping hybrid search when searching for a specific identifier (table name, function name, ticket ID)
- Treating similarity 0.6 as a strong match — always note confidence level in output
- Re-embedding a corpus manually (let Inngest functions handle it — manual embeds cause deduplication drift)
