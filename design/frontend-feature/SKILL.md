---
name: frontend-feature
description: Implement exactly one bounded frontend/web/admin task selected from an approved or in-progress SPEC using existing contracts, shared UI, and repository rules. Use for user-visible feature, bug, improvement, or maintenance work; do not use for SPEC authoring, repository bootstrap, or backend design.
license: MIT
---

# Frontend Feature

## Preconditions

For substantial work, require the exact approved or in-progress SPEC path or
identifier, valid `Approval: Explicit user approval — YYYY-MM-DD` evidence, and
the first eligible SPEC task selected through `implement-next` when that
companion is available. Require a matching SPEC scope; never infer approval
from the implementation request, a review verdict, or an existing task.

An explicitly requested trivial/localized fix may use the lightweight path only
when it is one bounded user-visible behavior or defect, does not change API
contracts, authentication/authorization, security boundaries, persistence, or
deployment behavior, and has a clear narrow validation command. If any of
those conditions is uncertain, stop and route the work through `spec-workflow`.

## Task ownership

When the SPEC has ordered unchecked tasks, use `implement-next` to select the
first dependency-ready task and preserve its red/green/refactor gates. Do not
choose a later task or implement several SPEC tasks in one pass. If that
companion is unavailable, require the same exact-SPEC, first-task, approval,
and TDD checks directly; do not silently select a task from repository
context. If tasks are missing, hand back to `spec-workflow`.

`implement-next` owns task selection, task execution state, task completion,
and the `SESSION_STATE.md` handoff. This skill owns only the selected frontend
implementation and task-specific tests/checks, then returns its evidence; it
does not select another task or mark work complete independently.

## Context loading

Read only:

- root `AGENTS.md` and `SESSION_STATE.md` when present
- the active SPEC, selected task, and its execution context
- applicable repository rules discovered from `AGENTS.md`, `docs/rules/`,
  existing project conventions, and user-owned legacy rule locations in an
  existing repository
- API, authentication, contracts, UI, security, and testing rules only when
  relevant

Use an available repository structural index, such as CodeGraph, for indexed
structural questions and blast radius. Use normal reads/search for docs,
configuration, and non-indexed details.

Never read secrets, credentials, private keys, browser profiles, cookies,
storage, or `.env` contents. Do not edit generated files directly; use the
documented generator or report that it is unavailable. Do not install
dependencies or tooling without approval.

## Implementation

1. Confirm the exact SPEC, selected task, affected UI, backend/shared
   contract, current worktree state, and validation target before editing. If a
   required contract is absent and not explicitly mocked by the approved task,
   stop and route the dependency to the backend/API workflow.
2. Use feature/domain-local API modules (for example, `features/auth/api.ts`)
   rather than a catch-all endpoint or API module.
3. Prefer the narrowest state scope: local → URL → server/query cache →
   global store only when genuinely shared.
4. Client validation improves UX; server validation remains authoritative.
5. Represent loading, success, empty, error, permission-denied, disabled, and
   retry states where they apply; preserve user input after recoverable errors
   and guard duplicate submissions.
6. Keep authorization-sensitive data access and all authorization decisions on
   the server; never treat hidden controls or browser state as authorization.
7. Reuse shared UI primitives; keep domain workflows out of a generic shared UI
   package.
8. Use `frontend-design` for genuinely new page, layout, responsive, interaction,
   or accessibility design work, and `ui-design-system` for product-wide visual
   system changes. Do not invent a parallel design system in a feature.
9. Use `test-driven-development` for testable behavior and
   `systematic-debugging` for unexplained failures.
10. Use browser/E2E skills only when relevant, through the existing
    repository-owned workflow and separately approved isolated localhost
    execution. Do not access remote sites or persistent browser state.

Do not redesign backend/domain behavior, modify unapproved shared contracts, or
create catch-all API modules. Do not create branches or issues, change remotes,
push, deploy, publish, or run production operations as part of implementation.

## Verification

Verify user-observable behavior, typecheck/lint/tests as required, and preserve
TDD evidence or record an explicit exception with alternative verification in
the same SPEC's `# Execution` section. Do not create or use a separate planning
or execution-tracking artifact. Use `verification-before-completion` before
claiming the SPEC complete only after all SPEC tasks are complete and the
SPEC-level review/final verification sequence succeeds. For this selected task,
return task-scoped evidence to `implement-next` and stop; do not run the
SPEC-level review or final verification gate here. After all SPEC tasks are
complete, `spec-workflow` routes `code-review` or `review-diff` when appropriate
and then `verification-before-completion`. For browser checks, record the
approved origin,
viewport/fixture scope, user-visible assertions, console/network observations,
and artifacts; do not claim untested states or cross-browser behavior. Report
the selected task, changed files, validation evidence, untested paths,
assumptions, and handoff; do not mark the SPEC completed from this skill.
