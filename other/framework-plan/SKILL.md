---
name: framework-plan
description: "Explicit framework workflow: plan"
disable-model-invocation: true
---

# /plan — Implementation plan

Use after a spec exists (or for small tasks, a verbal agreement). Prefer **plan mode** or explicit user approval before large edits.

## Inputs

- Approved spec or tight task description.
- Relevant files the user pointed at.

## Output

1. **Goal** — What “done” means.
2. **Files / areas to touch** — Paths or components.
3. **Approach** — Steps in order; call out risky changes.
4. **Failing test stubs to write BEFORE touching implementation** — Name the specific tests/assertions (mapped from spec acceptance criteria) that should be authored and confirmed failing first; map them to AGENTS.md commands.
5. **Rollback / flags** — If feature-flagged or migratory.

## Done when

- Another developer could execute the plan without guessing.
- Failing test stubs identified and ready to write before implementation begins.
- Test plan matches project conventions.

## Note

If the user has not approved implementation, **do not** apply code changes until they confirm.
