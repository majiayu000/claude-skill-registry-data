---
name: planning
description: "Break work into small atomic tasks with scope, risks, verification per task. Use after spec, before implementation."
---

# planning

A plan is a list of verifiable steps with owners and risks — not a paragraph of intent.
## Inspection

Read the spec/requirements, dependency graph, risky unknowns, and prior similar tasks (what slipped last time).

## Decision rules

Atomic tasks with independent verification; order by dependency; flag research/migration/security-review needs up front; size to single reviewable units.


## Activate when

- After requirements/spec, before implementation; when decomposing epics or migrations.

## Do NOT activate for

- Trivial single-file changes (plan inline); requirements gathering itself (see requirements-analysis).

## Procedure

1. Decompose into atomic tasks: each with scope, files touched, acceptance criteria, and how it will be verified.
2. Order by dependency; surface risks, unknowns with owners, and rollback points for risky steps.
3. Size tasks to single reviewable units; flag any task needing research, migration, or security review.
4. Verify: every task independently completable and testable; plan re-read against the spec for coverage gaps.

## Failure modes

Paragraph-of-intent plans; tasks without acceptance criteria; hidden dependencies discovered mid-implementation; no rollback points on risky steps.

## Escalation

Requirements gaps → core/requirements-analysis; estimate disputes → ask with options.
