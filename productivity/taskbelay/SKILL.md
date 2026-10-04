---
name: taskbelay
description: "Assess bounded Codex software development requests before choosing direct work or TaskBelay, then prepare confirmed TaskBelay Tasks in new local branches by default, current branches, or dedicated Git worktrees. It may be selected implicitly or explicitly with $taskbelay-codex:taskbelay; the selector never skips assessment. Explicit Task resume and receipt-backed confirmed bootstrap bypass duplicate assessment."
---

# TaskBelay for Codex

Codex performs repository work and authorized Host operations. Go Core owns Task state, Actions,
transitions, repository observation, verification, blockers and recovery.

## Choose the entry

Use `$taskbelay-codex:taskbelay` or implicit selection for assessment. Reuse valid user choices;
invocation alone does not authorize Git changes, Task creation or an unseen implementation plan.
Read only the guide for the current operation:

| Request or saved state | Next step |
| --- | --- |
| New development request | [Assess and prepare](references/admission.md); default to a new branch in the current directory after the user chooses TaskBelay. |
| Saved launch/bootstrap | [Resume the launch](references/admission.md#continue-a-saved-launch); inspect its surface and phase before provisioning, creating or resuming Core. |
| Explicit existing Task resume | Return to the original workspace and [connect/resume](references/connection.md); omit creation fields. |
| Current Action | Follow [Action execution](references/node-payloads.md) and only the current node guide. |
| Rejection, missing result or blocker | Read [response handling](references/tool-results.md), then its linked correction or recovery procedure. |
| Relocation, cancellation, abandonment, cleanup or installation diagnosis | Read [Host lifecycle](references/host-lifecycle.md). |
| Explanation, status question or design discussion | Answer or perform the authorized read; create no Task. Explicit review stays read-only until a later repair request. |

## Execute and continue

After provisioning or on Task resume, perform the [server handshake](references/connection.md#server-handshake)
before other Core calls. Use actually visible tools through [Codex transport](references/transport.md).
Keep complete responses, inspect `ok` before success fields, and handle recovery, blockers and outcome
before the returned Action. A shortened display does not lose a retained original response.

The [Action procedure](references/node-payloads.md) covers planning discussion, saved-plan approval,
current-node work, method steps, file preparation and submission. Before writes use
[artifacts and the Hook](references/artifacts.md); for checks use [verification](references/verification.md).
Only the current Core Action permits progress. Human approvals and comprehension verdicts must be real.
Continue authorized work when no required input is missing; progress updates need no acknowledgment.

## Repository and Host constraints

Follow current user/repository instructions, including required project indexes. Confirm participating
repositories before preparation; Scope is fixed after creation. Every needed root must remain within
Codex's authorized directories. When no instruction overrides `host_preferences.codex.codebase_memory`,
use an already usable index if preferred, otherwise ordinary Host search. An absent/incomplete index
gets at most one notice and immediate fallback. Do not install or repair an index through this Skill.

Choose `plain`, `spec-kit` or `openspec` from explicit intent, otherwise `plain`; retain an existing
Task's profile. [Method profiles](references/method-profiles.md) map current steps to visible tools.
A method result does not advance Core. A missing capability must be reported accurately.

DONE/CANCELLED retains files and grants no commit, push, PR, publication or deletion authority.
Use the lifecycle guide for separately authorized cleanup. Dedicated-worktree launch and discussion
handoff are linked from admission and loaded only for those operations.

Implementation: `packages/codex/lib/task-admission.mjs` — `validateSuitabilityAssessment`;
`packages/codex/lib/task-launch.mjs` — `prepareTaskLaunch`;
`packages/codex/lib/lifecycle.mjs` — `CODEX_MCP_INSTRUCTIONS`;
`internal/workflow/standard_process.go` — `StandardProcess`.
