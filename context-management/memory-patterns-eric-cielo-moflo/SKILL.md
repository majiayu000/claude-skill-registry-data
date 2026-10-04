---
name: "memory-patterns"
description: "Persistent memory patterns for moflo agents — session memory, long-term knowledge, pattern learning, and cross-session context via moflo's node:sqlite + HNSW vector store. Use when building stateful agents or assistants that need to remember across runs."
---

# MoFlo Memory Patterns

Persistent, semantically-searchable memory for moflo-enabled projects. Backed by `.moflo/moflo.db` (node:sqlite + HNSW vector index) and exposed through MCP tools.

## Core API

Three things to know:

1. **MCP tools** — call from Claude Code sessions:
   - `mcp__moflo__memory_store { key, value, namespace?, tags?, ttl?, upsert? }`
   - `mcp__moflo__memory_search { query, namespace?, limit?, threshold? }` — semantic, HNSW-backed
   - `mcp__moflo__memory_retrieve { key, namespace? }` — exact key lookup
   - `mcp__moflo__memory_list { namespace?, limit? }`
   - `mcp__moflo__memory_delete { key, namespace? }`
   - `mcp__moflo__memory_stats {}`

2. **CLI** — `flo-search "<query>" --namespace <ns>` for quick semantic lookup from the shell.

3. **Namespaces** — namespace + key is the unique identity. Default namespaces shipped by moflo: `learnings`, `patterns`, `guidance`, `code-map`. (`knowledge` is a deprecated alias — writes are transparently redirected to `learnings`.) Create your own for application memory (e.g. `app:sessions`, `app:users`).

## Pattern 1: Session Memory

Rolling per-conversation memory with TTL so old sessions expire:

```typescript
// Store a turn
await mcp.memory_store({
  namespace: 'app:sessions',
  key: `${sessionId}:msg:${turnIndex}`,
  value: { role, content, ts: Date.now() },
  ttl: 60 * 60 * 24 * 7, // 7 days
});

// Recall the session — keys sort lexicographically, so prefixing with
// sessionId groups a conversation.
const all = await mcp.memory_list({ namespace: 'app:sessions' });
const current = all.filter(t => t.key.startsWith(`${sessionId}:`));
```

Why namespace-per-use: search scope stays small and delete-by-namespace becomes `memory_list` + `memory_delete` in a loop.

## Pattern 2: Long-Term Knowledge

Facts that should survive any session and be findable by meaning, not exact key:

```typescript
await mcp.memory_store({
  namespace: 'learnings',
  key: 'auth:session-token-rotation',
  value: 'Session tokens are rotated every 15 minutes by the auth middleware. Refresh happens transparently on the client.',
  tags: ['auth', 'security'],
  upsert: true,
});

// Retrieval: semantic, not keyword
const hits = await mcp.memory_search({
  namespace: 'learnings',
  query: 'how do auth tokens refresh?',
  limit: 5,
  threshold: 0.4,
});
```

`upsert: true` is the norm — you're updating your own knowledge, not guarding against collisions.

## Pattern 3: Pattern Learning (store + promote)

Capture what worked, then let the next run find it:

```typescript
// After a successful task
await mcp.memory_store({
  namespace: 'patterns',
  key: `${patternType}:${shortHash(signature)}`,
  value: {
    signature,          // what triggered this
    approach,           // what you did
    outcome: 'success', // how it landed
    occurrences: 1,
  },
  tags: [patternType],
  upsert: true,
});

// Before starting a similar task
const similar = await mcp.memory_search({
  namespace: 'patterns',
  query: currentTaskDescription,
  limit: 3,
  threshold: 0.5,
});
```

On repeated hits, read the existing entry, increment `occurrences`, and `upsert`.

## Pattern 4: Context Recall at Prompt Start

moflo's gate hooks enforce "search memory before exploring files." Mirror that in your own agents:

```typescript
async function beforeTask(description: string) {
  const [guidance, patterns, codeMap] = await Promise.all([
    mcp.memory_search({ namespace: 'guidance', query: description, limit: 5 }),
    mcp.memory_search({ namespace: 'patterns',  query: description, limit: 5 }),
    mcp.memory_search({ namespace: 'code-map',  query: description, limit: 8 }),
  ]);
  return { guidance, patterns, codeMap };
}
```

This is the same fan-out the `/flo` spell does — cheap (HNSW, parallel) and replaces a lot of exploratory Glob/Grep.

## Anti-Patterns

- **Don't put large blobs in `value`.** Store pointers/keys — the embedding is built from the value string, and huge values bloat the index.
- **Don't search without a namespace.** Cross-namespace search mixes `guidance` (prose) with `patterns` (structured) — signal collapses.
- **Don't use sequential numeric keys** if you also want semantic search over them. Pick keys humans/agents would search for by meaning.
- **Don't use `ttl` on knowledge you want long-lived.** TTL is for sessions, ephemeral cache, WIP notes.

## Persistence & Indexing

- File: `.moflo/moflo.db` at project root (node:sqlite, Node 22+ built-in).
- Embeddings: built by cli's embeddings module; indexed with HNSW from `src/cli/memory/`.
- Cold-start cost: ~5 seconds to initialize HNSW. Tests should share a single instance (`beforeAll`, not `beforeEach`).
- Namespace isolation: each namespace is a logical partition, but the HNSW index spans the table. Query time scales with `limit` and `threshold`, not total row count.

## See Also

- `vector-search` skill — RAG patterns over your own documents
- `memory-optimization` skill — HNSW tuning, quantization, batch ops
- `.claude/guidance/moflo-core-guidance.md` — CLI/MCP reference
