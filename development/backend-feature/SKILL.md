---
name: backend-feature
description: Implement exactly one bounded backend/API task selected from an approved or in-progress SPEC while following its contract and repository rules. Use for server-side feature, bug, improvement, migration, or maintenance work; do not use for SPEC authoring, repository bootstrap, or frontend design.
license: MIT
---

# Backend Feature

## Preconditions

For substantial work, require:

- the exact approved or in-progress SPEC path or identifier
- valid `Approval: Explicit user approval — YYYY-MM-DD` evidence
- the exact first eligible SPEC task, selected through `implement-next` when
  that companion is available
- a matching SPEC scope; never infer approval from the user's implementation
  request, a review verdict, or an existing task

An explicitly requested trivial/localized fix may proceed without persistent
SPEC files only when it is one bounded behavior or defect, does not change
schema, public API, authentication/authorization, security boundaries, or
deployment behavior, and has a clear narrow validation command. If any of those
conditions is uncertain, stop and route the work through `spec-workflow`.

## Task ownership

When the SPEC has ordered unchecked tasks, use `implement-next` to select the
first dependency-ready task and preserve its red/green/refactor gates. Do not
choose a later task or implement several SPEC tasks in one pass. If that
companion is unavailable, require the same exact-SPEC, first-task, approval,
and TDD checks directly; do not silently select a task from repository
context. If tasks are missing, hand back to `spec-workflow`.

`implement-next` owns task selection, task execution state, task completion,
and the `SESSION_STATE.md` handoff. This skill owns only the selected backend
implementation and task-specific tests/checks, then returns its evidence; it
does not select another task or mark work complete independently.

## Context loading

Read only:

- root `AGENTS.md` and `SESSION_STATE.md` when present
- the active SPEC, selected task, and its execution context
- applicable repository rules discovered from `AGENTS.md`, `docs/rules/`,
  existing project conventions, and user-owned legacy rule locations in an
  existing repository
- database, API, authentication, contracts, security, and testing rules only
  when the change touches those areas

Use an available repository structural index, such as CodeGraph, for indexed
structural questions. Use normal reads/search for docs, configuration, and
non-indexed details.

Never read secrets, credentials, private keys, browser state, or `.env`
contents. Do not edit generated files directly; use the documented generator or
report that the generator is unavailable. Do not install dependencies or
tooling without approval.

## Implementation

1. Confirm the exact SPEC, selected task, affected area, current worktree
   state, and validation target before editing.
2. Use `test-driven-development` for testable behavior.
3. If persistent data changes, ensure the SPEC's data-design decision is
   recorded and any required `schema-design` review is complete before
   services/routes.
4. Implement only the selected task and the smallest coherent change it needs.
5. Validate external input at the transport boundary, enforce authorization
   server-side at the resource/action scope, and keep persistence models out of
   public responses when the task crosses those boundaries.
6. Keep public API shapes in the repository's shared contracts package only
   when clients genuinely share them.
7. Keep controllers/transports thin and business rules in the proper
   application/domain layer.
8. Use `systematic-debugging` for unexplained failures instead of speculative
   fixes.
9. Do not refactor unrelated code, change generated files directly, or broaden
   the selected task when validation reveals unrelated work; report it instead.

Do not create branches or issues, change remotes, push, deploy, publish, or
run production operations as part of implementation.

## Verification

Run the narrowest relevant tests first, then required repository checks. For
behavioral changes, preserve the TDD evidence or record an explicit exception
with alternative verification in the same SPEC's `# Execution` section. Do not
create or use a separate planning or execution-tracking artifact. Use configured
deterministic tools only when relevant. Return the task-scoped evidence to
`implement-next` and stop; do not run the SPEC-level review or final
`verification-before-completion` gate for one task. After all SPEC tasks are
complete, `spec-workflow` routes `code-review` or `review-diff` when appropriate
and then the final verification gate.

Report the selected SPEC task, changed files, validation evidence, untested
paths, assumptions, and handoff; do not mark the SPEC completed from this
skill.
