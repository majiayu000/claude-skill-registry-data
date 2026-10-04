---
name: apple-persistence-integrity
description: Use when an Apple app needs SwiftData recovery, migration, bounded-query, transaction, or cross-store integrity work, including custom SQLite coexistence.
license: "MIT"
metadata:
  author: "coryparrry"
  version: "0.1.0"
  last-updated: "2026-08-31"
  last-reviewed: "2026-08-31"
  apple-docs-reviewed: "2026-08-30"
---

# Apple Persistence Integrity

Preserve durable data by making store ownership, commit boundaries, migration, and recovery explicit.

## Route the Work

1. Inspect every container, configuration, context/actor, schema, migration, store URL, writer, save, retry, fallback, import, delete, and reset path before editing.
2. Map the authority, identity, write path, propagation, delete semantics, and failure policy for each durable fact.
3. Read [store-boundaries.md](references/store-boundaries.md) for SwiftData isolation, bounded queries, or any coexistence with SQLite, files, indexes, caches, IPC, or remote stores.
4. Read [migration-and-recovery.md](references/migration-and-recovery.md) before changing schemas, container startup, fallback, quarantine, or reset behavior.
5. If Xcode MCP is available, run `DocumentationSearch`; use [apple-documentation.md](references/apple-documentation.md) as the dated API index.

## Preserve These Invariants

- Give production container construction one owner; do not create hidden containers in views.
- Move stable domain IDs, non-temporary `PersistentIdentifier`s, or immutable `Sendable` snapshots across isolation boundaries, not live models or contexts. Refetch in the destination context.
- Use a clean, dedicated context with deliberate autosave behavior and explicit save/rollback boundaries for multi-step durable operations; shared-context save or rollback can include unrelated pending changes.
- Never claim atomicity across independent stores. Use projection, outbox, compensation, or reconciliation with idempotent replay.
- Keep released schemas immutable and test migrations from real file-backed prior-version stores.
- Bound reads at the fetch layer rather than materializing an entire store. Name the mechanism—such as `fetchLimit`, batch-size fetches, `fetchCount`, or identifier-only fetches—and test its pending-change behavior.
- Classify startup failure before recovery. Never silently delete, replace, copy, or mask authoritative data with an in-memory container; store-file quarantine/export requires a coherent store-aware snapshot and exclusive ownership.
- Require explicit authorization for destructive reset and preserve diagnostic evidence where feasible.

## Complete the Task

Implement the smallest safe change and verify durable state after reopening. Report the ownership map, commit invariants, migration/recovery behavior, focused evidence, and any remaining data-loss or cross-store risk.

## Review

- Last updated: 2026-08-31
- Last reviewed: 2026-08-31
- Apple documentation reviewed: 2026-08-30

Scope/evidence: SwiftData store ownership, transactions, migrations, bounded queries, and recovery guidance was checked with Xcode MCP `DocumentationSearch`; concrete fetch-bound instruction behavior was re-reviewed with a live Codex evaluation.

[Apple documentation evidence](references/apple-documentation.md)
