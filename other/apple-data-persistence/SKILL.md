---
name: apple-data-persistence
description: "Design or repair SwiftData, Core Data, file storage, migrations, save/cancel semantics, local-first data, CloudKit synchronization, and durable operation identity."
---

# Persistence, drafts, and synchronization

## Inputs

Identify the canonical store, schema history, context/actor ownership, draft boundary, durability promise, sync topology, supported upgrade paths, and recovery requirements.

## Rules

- **DATA-001 — Define the commit boundary.** Separate transient drafts, in-memory tracked changes, saved local data, and acknowledged remote data; distinguish targets, observations, and confirmed records.
- **DATA-002 — Preserve isolation.** Use contexts on their intended isolation domain; transfer IDs or immutable values rather than live managed objects between actors.
- **DATA-003 — Migrate real history.** Test upgrades from shipped schemas and realistic fixtures. Never silently delete a store to make a migration or launch succeed.
- **DATA-004 — Model synchronization explicitly.** Account changes, conflicts, retries, deletions, and partial failure are first-class states; local save is not remote delivery.
- **DATA-005 — Keep errors recoverable.** Do not hide save errors with `try?` or claim success before the promised commit. Retain user work and a safe recovery path.

## Workflow

1. Trace create/edit/delete through observation, context, store, and any sync/export paths.
2. Choose value drafts or isolated edit contexts with explicit save/cancel behavior.
3. Define IDs, validation, transactions, conflict policy, retention, and retries.
4. Use bounded queries and stable observation owners; measure expensive fetches.
5. Test disk-backed round trips, upgrades, interruption, and failure before release.

## Verify

Test cancel without write, save failure, duplicate commit, delete relationships, restart, migration from each supported schema, corrupt/unavailable storage, account change, and offline reconciliation as applicable.

## Output

Return the data/commit model, migration and recovery plan, tested upgrade paths, and distinct local versus remote guarantees.

## References

Read the [playbook](references/persistence-patterns.md) for decisions, failure cases, and source links.

For store selection and recovery boundaries, read the [focused reference](references/store-selection-and-recovery.md).
