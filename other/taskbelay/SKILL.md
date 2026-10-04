---
name: taskbelay
description: Assess development requests, then execute and resume complete TaskBelay tasks in ZCode with Core-owned state.
---

# TaskBelay for ZCode

Select this Skill from ZCode's `/` menu under Skills, or explicitly request TaskBelay. Invocation
requests assessment. ZCode performs repository work and authorized Host operations; Core owns Task
state, Actions, transitions, verification, blockers and recovery. Preserve valid user choices;
invocation does not authorize unconfirmed Git changes or approve an unseen plan.

| Request or state | Read and perform |
| --- | --- |
| New development request | [Admission](references/admission.md): assess read-only, obtain missing choices, then prepare every confirmed repository; default to a new local branch. |
| Retained launch | Read status/receipt, workspace identity and any saved task_id through admission before creation/resume. Opening a workspace does not prove Core creation. |
| Existing Task | Return to the original workspace and [connect/resume](references/connection.md), without preparing another workspace or creating another Task. |
| Current Action | [Action execution](references/node-payloads.md) and only the current node guide. |
| Rejection, lost result or blocker | [Response handling](references/tool-results.md) and its linked recovery procedure. |
| Installation, relocation, cancellation, abandonment or cleanup | [Host lifecycle](references/host-lifecycle.md). |

After provisioning or on resume, perform [server_info](references/connection.md#server-handshake)
first and require ZCode support. Discover actual tools through [transport](references/transport.md);
never derive names from another Host. Retain full responses, inspect `ok`, then recovery/blocker/outcome
and the entire Action.

Follow the Action procedure for requirements/design discussion, saved-plan approval, method steps and
submission. Use [artifacts](references/artifacts.md) before writes and every submission, and
[verification](references/verification.md) for checks. Required user decisions stay with the user.
The trusted plugin PreToolUse Hook protects Write/Edit. Do not bypass a denial or missing Hook;
shell/external writes are observed later and Host permissions still apply. Verify Hook changes in a
new session because configuration is captured at startup.

Follow current user/repository instructions. Confirm every repository (at most eight) and permissions
before preparation; never create a partial Task. Use requested available indexes or ordinary search,
without automatic installation. Before another workspace/session, read [handoff](references/task-handoff.md):
the Adapter returns UI instructions, not a session-launch CLI or proof that a session started.
DONE/CANCELLED preserves local work and grants no commit, push, publication or deletion authority;
dedicated worktree and branch deletion require their separate authorization after Core termination.

Implementation: `packages/zcode/lib/workspace.mjs`; `packages/zcode/bin/taskbelay-zcode.mjs`;
`packages/zcode/hooks/pre-tool-use.mjs`.
