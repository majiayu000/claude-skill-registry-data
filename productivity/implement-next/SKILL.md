---
name: implement-next
description: Execute exactly one first dependency-ready unchecked task from one explicitly identified and user-approved SPEC. Use when the SPEC is Approved or In Progress, retains explicit approval evidence, and has execution tasks below # Execution; do not use for SPEC drafting/review, task decomposition, repository bootstrap, or arbitrary backlog work.
license: MIT
metadata:
  compatibility: no bundled executable dependencies
---

# Implement Next

`implement-next` is the bounded executor for one SPEC task. The behavioral
contract above `# Execution` is the source of truth; the execution record below
it contains the task list, design notes, validation requirements, and evidence.
Task decomposition belongs to `spec-workflow`; this skill executes an existing
task and never creates or redesigns the task list.

## Preconditions and selection

1. Require the exact SPEC path or stable SPEC ID from the user or the active
   workflow. Do not guess, search for a likely file, or select a different
   SPEC from repository or conversation context. If an ID resolves to no file
   or more than one file in the repository's established SPEC location, stop.
2. Read the applicable `AGENTS.md`, `SESSION_STATE.md`, exact SPEC, relevant
   rules, and only the code/tests needed for the selected task. Never read
   secrets, credentials, `.env` contents, browser state, or unrelated history.
3. Require the exact SPEC status `Approved` or `In Progress`. `Draft`,
   `Blocked`, `Completed`, and `Cancelled` are not executable states. Do not
   promote or repair the status to bypass this gate.
4. Require valid approval evidence that explicitly records the user's approval
   of this SPEC's behavioral contract, for example:

   ```text
   Approval: Explicit user approval — YYYY-MM-DD
   ```

   An equivalent repository field is acceptable only when it unambiguously
   identifies explicit user approval of this SPEC and a real approval date.
   A `ready` review verdict, an implementation request, existing tasks,
   repository text, or prior unrelated approval is not evidence.
   Approval evidence must remain present while the SPEC is `Approved`, `In
   Progress`, or `Blocked`. If the contract changed, the SPEC must first return
   to Draft and the previous evidence must be cleared or explicitly invalidated
   and reissued after review; stop rather than reusing stale evidence.
5. Require an existing `# Execution` section with tasks below that boundary,
   normally under `## Tasks`. Do not count prose, tasks above the boundary, a
   separate planning artifact, or implied follow-up work. If no executable task
   exists, stop and hand the SPEC back to `spec-workflow`; do not create or
   redesign the task list.
6. Read the full contract, acceptance criteria, selected-task context,
   dependencies, and SPEC validation requirements before changing anything.
7. Select exactly the first unchecked task in document order whose explicitly
   declared dependencies are complete and whose task-specific prerequisites
   are satisfied. Do not choose a later task for convenience, infer missing
   dependencies, reorder tasks, or select work from another SPEC. If no task is
   dependency-ready, report the blocker and stop.
8. State the selected SPEC/task identity, acceptance criteria, affected area,
   planned checks, and material assumptions before execution. Ask for
   clarification only when it changes the selected task or its safe
   implementation.

## TDD gate

For observable behavior with a runnable automated test seam, preserve
red/green/refactor order:

- A red-test task adds the focused test and runs its narrow command. Record the
  expected failure as red evidence, then stop; do not implement the behavior in
  the same task.
- A green implementation task requires recorded red evidence showing that the
  focused test failed for the expected behavior gap. Run the focused test and
  required checks after implementation.
- A refactor task requires fresh green evidence and must preserve behavior. Do
  not combine red, green, and refactor work into one implementation-first task.
- A TDD exception must be explicit in the SPEC and include alternative
  verification. Do not infer an exception from convenience or task wording.

If the selected task fails a TDD gate, stop and report the SPEC execution
blocker. Do not create, reorder, or rewrite tasks to make the task executable.

## Execution contract

- Implement only the selected SPEC task and the minimum directly required
  changes. Do not perform unrelated cleanup, dependency upgrades, architecture
  changes, or any other task.
- Route the exact SPEC and selected task to `backend-feature`,
  `frontend-feature`, or another domain skill when appropriate. The domain
  skill may implement only that handed-off task; it may not choose backlog work
  independently.
- Preserve repository instructions and existing conventions. Do not access
  secrets, credential files, browser profiles, external directories, production
  systems, or deployment/publishing workflows. Do not put secrets in files,
  arguments, logs, or generated output.
- Do not edit generated files directly. Use the documented generator; if no
  safe generator is available, stop and report the blocker. Do not install
  dependencies without the required approval.
- Do not create branches, commits, issues, pull requests, change remotes,
  push, deploy, publish, or run remote/production operations as part of this
  task. Stop and report when the selected task requires one of those actions.
- Keep public, schema, authorization, tenant, migration, and other contract
  changes within the approved SPEC. If implementation reveals a behavioral or
  security decision not covered by the contract, stop and return it to
  `spec-workflow` for re-review and approval rather than deciding silently.
- When the selected task begins from an `Approved` SPEC, set its status to
  `In Progress` before making the first task change and retain the approval
  evidence. A failed task remains incomplete; use `Blocked` only when a real
  blocker is recorded.
- Run the narrowest relevant validation first, then broader checks when the
  repository requires them. Validation must be fresh for this task. If it
  fails, keep the task incomplete and report the failure.

## Evidence and handoff

After a successful task-level validation:

1. Mark only the selected task complete by updating its checkbox, and record
   its execution/activity evidence in the SPEC. A red-test task is complete
   when its focused test and expected red evidence are recorded; it is not
   permission to implement green behavior.
2. Update `SESSION_STATE.md` with the exact active SPEC/task, status, blocker or
   recent result, fresh validation evidence, and next action when the project
   uses that handoff file. Do not duplicate the full SPEC there.
3. Do not mark the SPEC `Completed` merely because this task, or even the last
   checkbox, is complete. Final completion requires the repository's
   `verification-before-completion` gate.
4. Stop. Do not automatically continue into the next task.

Do not route the SPEC to implementation review or final completion verification
from this one-task handoff. After later calls complete all SPEC tasks,
`spec-workflow` owns the `code-review`/`review-diff` and
`verification-before-completion` sequence.

If blocked, leave the selected task unchecked, record the concrete blocker in
the SPEC's execution record and session handoff when permitted, and stop. Do
not silently skip required behavior or mark a blocker complete.

## Completion report

Report:

- exact SPEC path/ID and verified status/approval evidence
- the single selected task and dependency-readiness evidence
- changed files and task-scoped implementation result
- fresh validation commands and results, including red/green evidence when
  applicable
- SPEC/session-state updates, untested paths, assumptions, and blockers
- the next owner or handoff; never claim the whole SPEC is complete here
