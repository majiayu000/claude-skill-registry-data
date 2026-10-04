---
name: "vector-search"
description: "Semantic vector search with moflo — RAG over your own documents, similarity matching, context-aware retrieval via HNSW (node:sqlite-backed). Use when building retrieval layers for chat, search, or context-assembly."
---

# MoFlo Vector Search (RAG)

Semantic search over your own documents, backed by moflo's HNSW index in `.moflo/moflo.db` (node:sqlite, Node 22+ built-in). Small enough to ship in a devDependency; fast enough for interactive retrieval at 100k–1M vectors.

## When to Use This vs `memory-patterns`

- **`memory-patterns`** — structured, namespaced memory you own (sessions, learnings, patterns). Keys matter. Entries are conceptual units.
- **This skill (`vector-search`)** — search over documents you've ingested for retrieval. Entries are content chunks. Keys are just stable IDs for dedupe.

Both use the same index; the difference is how you chunk and what you put in the `value` field.

## Ingest

Two paths. Pick the one that matches your source of truth:

### A. Ad-hoc ingest from Claude Code

```typescript
for (const [id, text] of chunks) {
  await mcp.memory_store({
    namespace: 'docs',        // your RAG corpus
    key: id,                  // stable ID for this chunk (file path + offset, etc.)
    value: text,              // the chunk content — what gets embedded
    tags: ['doc', docType],
    upsert: true,
  });
}
```

### B. Repeatable ingest from the filesystem

Use moflo's shipped indexers (cross-platform, skip unchanged chunks via a hash file):

```bash
# Guidance docs → namespace 'guidance'
node .claude/scripts/index-guidance.mjs

# Code structure → namespace 'code-map'
node .claude/scripts/generate-code-map.mjs

# Your own corpus — write a small indexer that loops over files and calls
# memory_store. Model it on bin/index-patterns.mjs.
```

## Retrieve

```typescript
const hits = await mcp.memory_search({
  namespace: 'docs',
  query: userQuestion,
  limit: 8,
  threshold: 0.35,   // drop irrelevant noise; tune per-corpus
});

// hits[] = [{ key, namespace, value, similarity, ... }]
```

Plug the retrieved `value` strings into your prompt as context. Filter or rerank higher up if needed.

## Chunking Rules That Actually Matter

1. **One idea per chunk.** 200–800 tokens. Smaller for code, larger for prose.
2. **Include enough context for the chunk to stand alone.** A bare "it does X" chunk won't retrieve well because the embedding has no subject.
3. **Deduplicate by stable ID.** Re-ingest is a no-op if `key` + `value` hash match. Cheap to re-run.
4. **Keep metadata minimal in `value`.** The embedding is built from the full value — noisy prefixes dilute the vector. Put structured metadata in `tags` or a separate `meta:${id}` key.

## Threshold Tuning

The `threshold` parameter is a similarity floor (0–1, cosine). No universal number.

Workflow for a new corpus:

1. Pick 10 queries you care about.
2. Search with `threshold: 0.2` and `limit: 20` — inspect the ranked results.
3. Note the similarity score where results go from "relevant" to "noise."
4. Set `threshold` just under that cliff. Expect values between 0.3 and 0.6 for most corpora.

Cheaper than trying to predict it.

## Hybrid: Semantic + Metadata Filter

moflo's `memory_search` doesn't have metadata filtering built-in. Do it in two steps:

```typescript
const candidates = await mcp.memory_search({
  namespace: 'docs',
  query: q,
  limit: 50,           // over-fetch
  threshold: 0.25,
});
const filtered = candidates.filter(c => c.tags?.includes('api-v2'));
const topK = filtered.slice(0, 8);
```

This is "search then filter" — works well when the filter is permissive. For highly selective filters, reverse the order: list by tag first, then re-rank against the query.

## RAG Pattern: Context Assembly

```typescript
async function answer(question: string) {
  const hits = await mcp.memory_search({
    namespace: 'docs',
    query: question,
    limit: 8,
    threshold: 0.35,
  });

  const context = hits
    .map((h, i) => `[Source ${i + 1}] ${h.value}`)
    .join('\n\n');

  return callModel({
    system: 'Answer using ONLY the sources below. Cite by source number.',
    user: `${context}\n\nQuestion: ${question}`,
  });
}
```

## Anti-Patterns

- **Don't store 50-page documents as single entries.** Chunk. Embeddings capture one topic at a time; big values average their meaning into mush.
- **Don't set `threshold: 0`.** You'll get the whole table sorted by similarity — including total noise at the bottom — and waste tokens on worthless context.
- **Don't re-embed on every query.** The embedding cost is in the ingest path; queries reuse the HNSW graph. If you find yourself re-embedding, you're doing it wrong.
- **Don't mix namespaces.** Keep each corpus in its own namespace so scores are comparable and threshold tuning actually works.

## Performance

- 100k chunks, dim 1536: ~5–15ms per search on commodity hardware.
- Cold-start: ~5s to load/build HNSW on first query in a process. Keep the process warm.
- Tuning: see `memory-optimization` skill for M/ef/quantization knobs.

## See Also

- `memory-patterns` skill — non-RAG memory usage (sessions, knowledge, patterns)
- `memory-optimization` skill — scaling past ~100k vectors
- `bin/semantic-search.mjs` / `flo-search` CLI — shell access to the same index
