---
name: longterm-memory
description: Use for the episodic long-term memory store and retrieval.
---

# Long-Term Episodic Memory

Embedding-based long-term memory: `scripts/longterm_memory.py` (runtime copy +
repo copy + the installed copy under `openamer-agent/scripts/`).

- **Store**: `<HOME>/memory/longterm_episodes.jsonl` — 768-dim `nomic-embed-text`
  vectors inline, one JSON object per line
- **Brain read**: `<HOME>/a2a/openamer-brain.jsonl`, derived from `BASE`
- **Embedder**: Ollama `nomic-embed-text` on `localhost:11434` (~1.85 s uncached,
  skipped entirely for text already in `memory/embed_cache.json`)
- **Cron**: `longterm-memory-indexer` (`7e81680726d3`), `0 */6 * * *`, no_agent

## Commands

```bash
python scripts/longterm_memory.py index        # reindex, module default cap 3000
python scripts/longterm_memory.py index 400    # bounded run - use this from cron
python scripts/longterm_memory.py add "text"   # append one episode
python scripts/longterm_memory.py query "..."  # top-5 most similar episodes
python scripts/longterm_memory.py stats
```

## Verification

```bash
python scripts/longterm_memory.py stats
```

Then check that the store is actually GROWING - a healthy-looking `stats` proves
nothing, because this organ sat frozen for 17 days while every status stayed green:

```bash
python scripts/longterm_memory.py index 20    # then compare the line count before/after
```

## What was broken (fixed 2026-10-10, `9b873c77f`)

The store had written nothing since 2026-09-23. Three independent defects, and the
lesson in each is what to check first next time:

1. **Nothing called the writer.** `add_episode()` had exactly one caller: its own
   CLI. The indexer cron had been DISABLED, and **a disabled job keeps
   `last_status: ok` forever** - the same trap as the dormant swarm jobs. A frozen
   counter still looks like a counter.
2. **The indexer read the wrong brain.** `BRAIN` was a hardcoded foreign path
   (`~/.openamer/a2a/openamer-brain.jsonl`, 57 MB, 1.5 days stale) while the live
   brain the daemon writes is this install's own (`<HOME>/a2a/...`, 144 MB,
   current). Now derived from `BASE`.
3. **A latent data-loss bug.** `_load()` returns only records with both `text`
   and `embedding`; `_save()` wrote back exactly that list, so one index run would
   have DELETED every skipped record - 2898 of 3065 were `kind=compressed` with no
   embedding. `_save()` now carries skipped records through untouched.

Also: the embed-failure path was a blind `except: continue`, so a dead embedder
indexed nothing in total silence. It now stamps `embed_error` on the row, counts
it, and the CLI exits non-zero. **Do not treat a skipped row as normal** - that
assumption is exactly what hid this for 17 days.

## Gotchas

- **Ollama must be running.** If it is not, embeddings fail; the run reports the
  count and exits non-zero instead of silently indexing nothing.
- **Cap your run.** 3000 fresh embeddings ≈ 92 minutes and cannot finish inside a
  cron window. Progress saves every 50 rows, so bounded runs clear a backlog over
  several runs.
- Brute-force cosine is fine to ~100k episodes; beyond that an ANN index is needed.
- `_load()` deliberately ignores rows without `text`+`embedding` so one foreign
  line can never crash index/query/stats - which is why every write path must go
  through `_save()`, never a hand-rolled rewrite.
