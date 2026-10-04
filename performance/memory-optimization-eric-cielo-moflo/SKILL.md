---
name: "memory-optimization"
description: "Tune moflo's memory stack for speed, RAM, and index quality. Covers HNSW parameters (M, efConstruction, ef), vector quantization, batch operations, and common bottlenecks. Use when scaling past ~100k entries or when search latency regresses."
---

# MoFlo Memory Optimization

When the default moflo memory settings stop being enough — past ~100k entries, or when p95 search latency climbs — these are the levers.

## HNSW Parameters

HNSW has three knobs. They trade build time, query time, memory, and recall.

```typescript
import { HNSWIndex } from 'moflo/dist/src/cli/memory/index.js';

const index = new HNSWIndex({
  dimensions: 1536,        // must match your embedding model
  maxElements: 1_000_000,  // pre-allocated capacity
  M: 16,                   // graph connectivity (default 16)
  efConstruction: 200,     // build-time search width (default 200)
  metric: 'cosine',        // 'cosine' | 'l2' | 'ip'
});
```

| Knob | Higher | Lower | When to change |
|------|--------|-------|----------------|
| `M` | better recall, more RAM (~2×M pointers per point) | less RAM, worse recall | Bump to 32–64 if recall@10 < 0.95; drop to 8 if memory-bound |
| `efConstruction` | better index quality, slower build | faster build, worse queries | 200–400 is sweet spot; only lower in test fixtures |
| `ef` (search-time, passed to `search()`) | better recall, slower queries | faster queries, worse recall | Start at 2×k, raise until recall plateaus |

Rule of thumb: `M` and `efConstruction` are set once. `ef` is the runtime dial.

## Quantization

moflo memory supports scalar quantization (Float32 → Int8) for a ~4× memory reduction with a ~1-2% recall hit. Turn it on when the index doesn't fit comfortably in RAM.

```typescript
const index = new HNSWIndex({
  dimensions: 1536,
  maxElements: 5_000_000,
  quantization: {
    enabled: true,
    type: 'scalar',   // scalar (Int8) is the supported path
    rebuildThreshold: 10_000,
  },
});
```

Measure recall before/after on your own query distribution — public benchmarks don't predict your domain.

## Batch Operations

Single-entry writes pay the HNSW insert cost per call. For bulk ingest, batch:

```typescript
const entries: Array<[string, Float32Array]> = buildCorpus();

// Parallelise at the adapter level; don't await sequentially.
await Promise.all(
  entries.map(([id, vec]) => index.addPoint(id, vec))
);

// Or via MCP for moflo-native batch into .swarm/memory.db:
await mcp.memory_store(/* … */);  // upsert: true + Promise.all is fine
```

For >10k entries, prefer `bin/build-embeddings.mjs` / `bin/index-all.mjs` — they stream in batches with a progress bar and skip unchanged chunks via a hash file.

## Caching

`MofloDbAdapter` has a built-in LRU cache (default 10k entries, 5-min TTL):

```typescript
import { MofloDbAdapter } from 'moflo/dist/src/cli/memory/index.js';

const store = new MofloDbAdapter({
  cacheEnabled: true,
  cacheSize: 50_000,      // scale with working set, not total corpus
  cacheTtl: 10 * 60_000,  // 10 minutes
});
```

Cache hits on exact keys bypass HNSW entirely. If your workload is read-heavy and hits a narrow keyspace, this is the cheapest win.

## Measuring

```bash
npx vitest bench src/cli/memory/benchmarks/vector-search.bench.ts
```

The bench prints linear vs HNSW times for 1k and 10k vectors. Run it before and after any parameter change — "it felt faster" is not a benchmark.

For production memory stats:

```typescript
const stats = await mcp.memory_stats({});
// { entryCount, indexSize, cacheHitRate, avgSearchMs, … }
```

## Common Bottlenecks

| Symptom | Likely cause | Fix |
|---------|--------------|-----|
| Cold-start of 5s on first search | HNSW loading from disk | Share a single instance via `beforeAll` in tests; keep the adapter resident in long-running processes |
| Search latency climbs linearly with `limit` | Over-fetching and re-ranking on the hot path | Lower `limit`; raise `threshold` to prune |
| Inserts slow past ~100k entries | `maxElements` too close to entry count → reallocation | Set `maxElements` to 2× expected corpus |
| High RSS on a small corpus | Vector dimension mismatch with index | Confirm `dimensions` matches embedder output (OpenAI = 1536, local models vary) |

## Anti-Patterns

- **Don't rebuild the index on every test.** Use a module-level singleton + `beforeAll`. HNSW cold-boot is ~5s.
- **Don't raise `ef` globally.** Raise it on the specific queries that need recall. Default is fine for 90% of calls.
- **Don't quantize a small corpus.** Below ~500k vectors the RAM saving doesn't justify the recall cost.
- **Don't measure in dev mode.** The memory stack behaves differently under `NODE_ENV=production`; benches should match the target.

## See Also

- `memory-patterns` skill — API usage and namespace design
- `vector-search` skill — RAG-specific patterns on top of the optimized index
- `src/cli/memory/benchmarks/` — runnable benches for every knob above
