---
name: deprecation-and-migration
description: Use when replacing or retiring an API, library, system, feature, dependency, configuration, or schema, or when moving consumers from one implementation to another. Do not use for a local rename or ordinary feature work with no compatibility or lifecycle concern.
license: MIT
---

# Deprecation and Migration

Retire old behavior only after understanding its consumers and giving them a
safe path to the replacement. Migration is a compatibility and risk-management
workflow, not just a search-and-replace.

## Decide before deprecating

Establish:

- The value, maintenance cost, security risk, and ownership of the old system.
- All known callers, users, jobs, integrations, configurations, and runtime
  consumers, not only static references.
- A replacement that covers critical use cases, or an explicit approved
  decision that no replacement is needed.
- Compatibility requirements, data invariants, support window, cutoff, and
  rollback strategy.

Do not claim zero usage from a repository search alone. Combine static evidence
with tests, telemetry, logs, dependency analysis, or owner confirmation when
the surface has external consumers.

## Deprecation modes

- **Advisory:** the old path remains supported while consumers migrate; provide
  warnings, documentation, and a target date or review point.
- **Compulsory:** use only when security, operational, legal, or maintenance
  risk justifies a deadline. Provide migration tooling, a concrete guide,
  support expectations, and an approved removal date.

Default to advisory when the old path is stable and migration is optional.

## Migration workflow

### 1. Inventory and announce

Map the old interface, data shape, configuration, behavior, error semantics,
side effects, and observability. Publish the replacement, reason, compatibility
notes, examples, verification steps, support window, and removal criteria.

### 2. Define a reversible cutover

Choose the least risky pattern that fits the boundary:

- An adapter can preserve the old interface while the implementation changes.
- A strangler or feature flag can move consumers incrementally.
- A compatibility layer can support old and new formats during a bounded
  transition.
- For schema changes, use expand → migrate/backfill → contract. Add the new
  shape first, support old and new code together, migrate in bounded batches,
  switch reads, then remove the old shape in a later separately approved step.

Do not couple a destructive schema change to the first code release that needs
the new shape. A rollback of application code cannot restore deleted data.
Define backup/restore or forward-repair evidence for data that cannot be
reversed by a normal code rollback.

### 3. Migrate in thin slices

For each consumer:

1. Identify every touchpoint and its compatibility contract.
2. Move it to the replacement or adapter.
3. Verify outputs, errors, side effects, permissions, and performance.
4. Observe the old and new paths where the system supports that comparison.
5. Record completion and rollback readiness before the next consumer.

Keep old and new behavior valid at the same time when rolling deployment,
parallel workers, or external clients make mixed versions possible.

### 4. Remove only after evidence

Before removal, verify no active consumers remain using the strongest available
combination of search, tests, dependency analysis, telemetry, and ownership
confirmation. Then remove old code, tests, configuration, documentation,
compatibility shims, and deprecation notices in a reviewable change. Preserve
the migration record and any operational runbook needed for recovery.

## Approval and safety gates

Pause for explicit approval before changing public contracts, user-visible
behavior, production data, retention, permissions, external integrations, or
destructive schema/configuration state. Do not run a production migration,
backfill, rollout, or deletion as part of planning or local verification.

## Verification

- [ ] Replacement covers critical use cases and has owner/support coverage.
- [ ] Migration guide and compatibility behavior are concrete and testable.
- [ ] Mixed-version behavior is safe where applicable.
- [ ] Each slice has behavioral and rollback evidence.
- [ ] Data migrations are additive first, bounded, and separately contracted.
- [ ] Active usage is verified with more than static search when needed.
- [ ] Old code and references are removed only after the evidence threshold is
      met.
- [ ] The final diff contains no unrelated cleanup or hidden behavior change.

## Upstream basis

Adapted for this harness-agnostic repository from
[addyosmani/agent-skills deprecation-and-migration](https://github.com/addyosmani/agent-skills/tree/6ca0cd7db39b41b1c37e26d335c507ee92382c6d/skills/deprecation-and-migration),
licensed under MIT.
