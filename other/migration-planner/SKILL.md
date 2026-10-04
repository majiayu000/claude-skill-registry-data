---
name: migration-planner
description: "Plans framework, API, schema, service, package, UI, build, or infrastructure migrations with slices, rollback, and validation."
---

# Migration Planner

Plan migrations as ordered, verifiable slices.

## Workflow

1. Inspect current versions, boundaries, tests, and runtime entrypoints.
2. Define the target state and non-goals.
3. Split work into independent slices with expected diffs.
4. Identify compatibility shims, data migration risk, and rollback points.
5. Define validation for each slice and final acceptance criteria.

## Output

- current state
- target state
- ordered work slices
- files or modules likely touched
- validation commands
- rollback plan
- risks and open questions

## Rule

Do not start implementation from this skill unless the user asked for both
planning and execution. Hand off to the relevant build/security/UI skill for
implementation.
