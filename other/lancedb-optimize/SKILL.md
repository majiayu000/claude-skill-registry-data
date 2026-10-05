---
name: lancedb-optimize
description: >-
  Optimize (compact + prune) all StaticFlow LanceDB tables across content,
  comments, and music databases to merge fragment files and reclaim storage.
---

# LanceDB Optimize

Compact and prune all LanceDB tables to merge accumulated fragment files,
reduce open file descriptors, and improve query performance.

## When To Use
1. Periodic maintenance (recommended weekly or after heavy write activity).
2. After "Too many open files" (os error 24) errors.
3. After bulk imports, batch embeds, or large cleanup operations.
4. Before backups to minimize storage footprint.

## Database Roots

All paths are relative to `DB_ROOT` (default: `/mnt/wsl/data4tb/static-flow-data`).

| DB | Path | Tables |
|----|------|--------|
| Content | `$DB_ROOT/lancedb` | `api_behavior_events`, `article_request_ai_run_chunks`, `article_request_ai_runs`, `article_requests`, `article_views`, `articles`, `images`, `interactive_assets`, `interactive_page_locales`, `interactive_pages`, `llm_gateway_keys`, `llm_gateway_usage_events`, `llm_gateway_runtime_config`, `taxonomies` |
| Comments | `$DB_ROOT/lancedb-comments` | `comment_ai_run_chunks`, `comment_ai_runs`, `comment_audit_logs`, `comment_published`, `comment_tasks` |
| Music | `$DB_ROOT/lancedb-music` | `music_comments`, `music_plays`, `music_wish_ai_run_chunks`, `music_wish_ai_runs`, `music_wishes`, `songs` |

## Preconditions
1. Resolve CLI in this order:
   - `./target/release/sf-cli`
   - `./target/debug/sf-cli`
   - `../target/release/sf-cli`
   - `sf-cli` from `PATH`
2. Verify CLI works: `<cli> --help`
   - Build if needed: `cargo build -p sf-cli --release`
3. If the checkout is newer than the chosen binary, rebuild before use.
4. Do not prefer legacy `./bin/sf-cli` snapshots for storage-format-sensitive writes.
5. Verify DB paths exist.

## Execution Workflow

### Step 1: Pre-check — Count Fragments

For each DB root and each table, inspect fragment counts via Lance metadata
instead of counting files under `data/`:

```bash
<cli> db --db-path <db_path> audit-storage --table <table>
```

Report a summary table of fragment counts. Tables with <= 3 fragments can be
skipped (already compact).

### Step 2: Optimize All Tables

For each table that needs compaction:

```bash
<cli> db --db-path <db_path> optimize <table> --all --prune-now
```

- `--all`: full optimization (compact fragments + rebuild indexes)
- `--prune-now`: immediately remove old versions (older_than=0, delete_unverified=true)
- On the current StaticFlow fork, blob v2 tables such as `songs`, `images`,
  and `interactive_assets` are expected to compact normally.

Run tables within the same DB sequentially (they share the same lock).
Different DBs can run in parallel.

### Step 3: Post-check — Verify

1. Re-check fragment counts with `audit-storage`.
2. Verify row counts match pre-optimization counts:
   ```bash
   <cli> db --db-path <db_path> count-rows <table>
   ```
3. Report before/after comparison.

## Selective Optimization

To optimize only specific DBs or tables:

```bash
# Single table
<cli> db --db-path /mnt/wsl/data4tb/static-flow-data/lancedb optimize api_behavior_events --all --prune-now

# All tables in one DB
for t in <table_list>; do
  <cli> db --db-path <db_path> optimize "$t" --all --prune-now
done
```

## Safety Notes
- Optimization is non-destructive: it merges fragments and removes old versions,
  but never deletes current data.
- The backend should ideally not be writing heavily during optimization to avoid
  lock contention. Light writes (normal API traffic) are fine.
- If optimization fails mid-way, the table remains valid — just not fully compacted.
  Re-run to complete.
