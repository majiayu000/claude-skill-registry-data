---
name: engram-live-verify
description: Use when changing engram-mcp, the scan pipeline, retrieval, or any Rust behavior that the MCP surface exposes — BEFORE claiming a fix works. Triggers on "verify live", "test against the real store", "does the fix work end-to-end", or as the mandatory final step of any engram code change. Drives the real stdio server against a real store with timed tool calls. Unit tests alone have shipped broken paths before (the pgvector lane never ran against real Postgres until live verification caught it).
---

# Skill: engram-live-verify

Unit + integration tests prove wiring; live verification proves behavior.
Run the actual server binary against an actual store and call the actual
tools. This is non-negotiable for scan/retrieval/MCP changes.

## The driver

```bash
cargo build --release -p engram-mcp   # (add --features pgvector,fastembed for PG/vector work)
python3 scripts/dev/mcp_driver.py \
  --storage ~/.engram/<store> --project <project> [--no-vector] [--wait 12] \
  call <tool> '<json-args>' \
  call <tool> '<json-args>'
```

Timed responses + captured stderr. Stores on this machine:
`agentzero` (shared, mixed repos + session memories — do not wipe),
`mem-alpha-self` (this repo only), `springboot-demo`, `dreamhouse-lwc`
(single-repo demos; wipe-able after killing the BFF on :3001).

## The scars this checklist is made of

- **`--wait 12`+ when vector is on** — FastEmbed model load takes seconds;
  requests sent too early queue behind boot and pollute timings.
- **stderr is where boot lives.** `knowledge_store=false` in a bootstrap
  warning means silent capability degradation — a store that "boots" can be
  missing its knowledge handle. Always read the STDERR section.
- **Silent-empty is the default failure mode.** A query returning `[]`/0 may
  be correct OR may be: wrong scope semantics (`IS NULL OR =` is NOT
  scope-allows — NULL is not a wildcard), a camelCase JSON path probe
  (`$.documentId`, never `$.document_id`), a swallowed `unwrap_or_default`,
  or a schema drift. Cross-check counts with sqlite3 CLI before believing
  empty.
- **The vec0 vector table is a virtual table** — plain CLI reads of
  `vectors_vector_chunks*` shadows mislead (inserts "vanish"); the
  `vectors_rowids` shadow holds the id map. The tool's own embedded/reused
  accounting is authoritative for reindex.
- **Wiping a store**: kill the BFF (`lsof -ti :3001 | xargs -r kill`) first —
  an open handle blocks `rm -rf` silently. `rm -rf` failures print nothing
  when backgrounded; verify with `[ -d path ]`.
- **Heredoc-python drivers get their logs eaten** by the shell harness — use
  script files (`scripts/dev/mcp_driver.py` exists for this reason).
- **Postgres work**: `docker compose -f docs/how-to-pg/docker-compose.yaml up -d`;
  TRUNCATE tables between tests; the docker-gated recipe tests run with
  `cargo test -p engram-backend-pgvector -- --ignored --test-threads=1`.

## What "verified" means

1. The tool call returned (not timed out) with the expected shape.
2. Counts changed where they should (scan → entities/rels; reindex →
   embedded/reused split; embed → the vectors accounting).
3. The invariant held: resolved-signal counts stay stable when only noise is
   removed (e.g. resolved calls before/after a filter change).
4. For perf claims: before AND after numbers from the same store, same call,
   same cap — single-sided timings are not evidence.

Record the verification (commands + numbers) in the commit message.
