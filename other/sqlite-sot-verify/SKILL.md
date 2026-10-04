---
name: sqlite-sot-verify
description: >
  Verify SQLite-backed source-of-truth changes with direct PRE/POST row reads,
  delta accounting, restart durability checks, and rejection of ORM-only proof.
when_to_use: >
  Use when changes touch SQLite-backed state, TradeStore, trade lifecycle
  persistence, audit rows, restart durability, or direct source-of-truth
  verification.
---

# SQLite Source-of-Truth Verify

## Workflow

1. Identify the DB file, table, primary key, and transaction boundary.
2. PRE: read rows directly from SQLite before the operation.
3. ACT: perform the operation under test.
4. POST: read rows directly from SQLite after the operation, preferably through a fresh connection when durability matters.
5. DIFF: compute the expected row-level delta and compare exactly.
6. HALT: reject proof based only on return values, mocks, logs, or in-memory objects.

## Required Checks

- WAL/restart behavior for durable lifecycle state.
- Terminal trade states cannot transition.
- Partial-close deduplication survives process restart.
- `upsert_trade` updates every intended mutable field and no unintended immutable fields.
