---
name: swiftdata
description: "Design and repair SwiftData models, relationships, predicates, contexts, disk-backed migrations, indexes, history, and CloudKit-compatible schema evolution."
---

# SwiftData schemas, queries, and migrations

## Inputs

Inspect model/container registration, store configuration, context ownership, schema versions, deployment minimums, and whether synchronization is enabled.

## Rules

- **SD-001 — Own the graph.** Define inverses and deletion behavior from domain lifecycle; neither cascade nor nullify is universally correct.
- **SD-002 — Test translated queries.** A predicate compiling in Swift does not prove store execution. Test real predicates, ordering, nil relationships, and limits on the supported store.
- **SD-003 — Isolate mutable models.** Keep context-bound objects on their intended actor; transfer identifiers or snapshots rather than live models.
- **SD-004 — Treat schemas as history.** Preserve shipped versions and test disk-backed upgrades. Never delete a failing store or switch silently to memory.
- **SD-005 — Separate sync from save.** Validate CloudKit constraints and account behavior; local uniqueness or a completed save is not distributed exactly-once delivery.

## Workflow

1. Map each model and relationship to the configured schema and store.
2. Define draft/commit and query contracts before adding modifiers.
3. Choose a supported migration with realistic historical fixtures.
4. Exercise failures, relationships, reopens, and synchronization boundaries.

## Verify

Test explicit saves through fresh contexts, failed commits, deletion graphs, query edge cases, and upgrades from every supported shipped schema. Label in-memory tests separately.

## Output

Return schema/ownership decisions, query fixtures, upgrade evidence, and unverified store or account behavior.

## References

- [Models, contexts, and query correctness](references/models-and-queries.md).
- [Schema evolution and synchronization](references/migration-and-sync.md).
