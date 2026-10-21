---
name: reindex
description: Rebuild the cqs index and show before/after stats comparison.
disable-model-invocation: false
argument-hint: "[--force]"
---

# Reindex

Rebuild the cqs search index and compare stats.

## Process

1. **Before stats**: Run `cqs stats` and capture output (chunk count, note count, HNSW status)

2. **Reindex**:
   - Default: `cqs index` (incremental — only re-embeds changed files)
   - With `--force` argument: `cqs index --force` (full rebuild). Stop the daemon first (`systemctl --user stop cqs-watch`) — cqs itself warns to do this — and restart it after.

3. **After stats**: Run `cqs stats` again

4. **Compare**: Show before/after diff:
   - Chunks: added, removed, unchanged
   - Notes: count change
   - HNSW vectors: count change
   - Call graph: call count change

5. **Verify**: Run a quick search to confirm index is working:
   - `cqs "parse source file"` — should return results
   - If no results, something is wrong — investigate

## When to use

- After significant code changes
- After editing `docs/notes.toml` manually (if `cqs watch` isn't running)
- After switching branches with different file sets
- When search results seem stale or wrong
