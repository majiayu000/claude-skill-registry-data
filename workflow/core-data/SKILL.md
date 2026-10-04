---
name: core-data
description: "Diagnose Core Data contexts, managed object identity, fetches, batch changes, persistent history, SQLite migrations, merge policies, and CloudKit mirroring."
---

# Core Data confinement, history, and migration

## Inputs

Identify container/store type, model versions, context queues, transaction authors, history consumers, merge policy, and mirroring configuration.

## Rules

- **CD-001 — Respect context confinement.** Perform work on each context through its supported scheduling API; pass object IDs or immutable values across boundaries.
- **CD-002 — Resolve identifiers safely.** Do not assume a temporary ID identifies a saved object, or that an object still exists when another context resolves it.
- **CD-003 — Merge store-level mutations.** Batch operations bypass registered object state; explicitly merge relevant IDs or consume history as appropriate.
- **CD-004 — Keep history consumer-aware.** Advance durable cursors after successful processing, and prune only when the consumer policy permits it.
- **CD-005 — Migrate without destruction.** Test supported schema transitions on actual disk stores; preserve data and diagnostics if opening or migration fails.

## Workflow

1. Map contexts and every cross-context handoff.
2. Bound fetch/import work and choose an explicit merge policy.
3. Trace batch/history notifications through the UI update path.
4. Verify disk reopen, upgrades, conflicts, and account boundaries.

## Verify

Use SQLite fixtures for SQLite-only operations. Test deleted IDs, fresh contexts, competing edits, replayed history, and migration from shipped versions.

## Output

Return the context/transaction map, merge and recovery policy, store-specific tests, and limitations.

## References

- [Contexts, batch operations, and history](references/contexts-and-history.md).
- [Fetch performance and schema evolution](references/migration-and-fetches.md).
