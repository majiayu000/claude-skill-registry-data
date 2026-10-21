---
name: deprecation-migration
description: Replace dependencies, interfaces or data models with verified consumer handling. Triggers on "deprecate", "弃用".
---

# Deprecation and Migration

## When to use

- Replace dependencies, interfaces or data models with verified consumer handling.

**Not for:** refactoring for structural moves; architecture for replacement design.

## Steps

1. Identify consumers, persistent data and target; read official current migration guidance.

2. Choose atomic internal migration or a bounded transition needed by real external consumers, with removal criteria.

3. Update consumers, schema, config and approved docs; check integrity, repetition and recovery without casts or suppression masking errors.

4. Remove old implementation after verified migration and run behavior checks; report unverified consumers and commit only on request.

## Verify

- Required consumer and data behavior survives; transition logic has necessity and removal evidence.

## References

- [engineering-principles.md](../../../references/engineering-principles.md) — shared decision boundaries, scope and verification.
- [references/dependency-upgrade.md](references/dependency-upgrade.md) — changelog/migration-guide reading, breaking-change triage, branch-based upgrade, root-cause fix per break
- [references/data-migration.md](references/data-migration.md) — moving data between systems: dual-write + backfill, CDC, cutover, verification, failure modes
