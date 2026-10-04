---
name: taskbelay
description: Assess development requests, then execute and resume complete TaskBelay tasks in Claude Code with Core-owned state.
---

# TaskBelay for Claude Code

Use `/taskbelay-claude:taskbelay` for assessment. Claude performs repository work and authorized Host
operations; Core owns Task state, Actions, transitions, verification, blockers and recovery.
Invocation does not authorize Git changes or approve an unseen plan. Reuse valid user answers.

| Request or state | Read and perform |
| --- | --- |
| New development request | [Admission](references/admission.md): assess read-only, obtain missing choices, then prepare every confirmed repository; default to a new local branch. |
| Saved launch | Read its status/receipt and actual workspace identity through admission before creation/resume; a requested Claude session does not prove Core creation. |
| Existing Task | Return to the original workspace and [connect/resume](references/connection.md), without preparing another workspace or creating another Task. |
| Current Action | [Action execution](references/node-payloads.md) and only the current node guide. |
| Rejection, lost result or blocker | [Response handling](references/tool-results.md) and its linked recovery procedure. |
| Installation, relocation, cancellation, abandonment or cleanup | [Host lifecycle](references/host-lifecycle.md). |

After provisioning or on resume, perform [server_info](references/connection.md#server-handshake)
first and require Claude support. Use actually visible tools through [transport](references/transport.md).
Retain full responses, inspect `ok`, then recovery/blocker/outcome and the complete Action.

Follow the Action procedure for requirements/design discussion, saved-plan approval, method steps and
submission. Use [artifacts](references/artifacts.md) before writes and every submission, and
[verification](references/verification.md) for checks. Required user decisions stay with the user.
Write/Edit/NotebookEdit require the trusted PreToolUse Hook; a denial or disabled gate cannot be
bypassed with another tool. Bash/external writes are observed later. Claude permissions still apply.

Follow current user and CLAUDE.md/AGENTS.md instructions. Confirm every repository (at most eight)
and its permissions before preparation; never create a partial Task. Indexes are optional and are
not installed automatically. Read [handoff](references/task-handoff.md) before another session.
DONE/CANCELLED preserves local work and grants no commit, push, publication or deletion authority;
dedicated worktree and branch deletion require their separate authorization.

Implementation: `packages/claude/lib/workspace.mjs`; `packages/claude/bin/taskbelay-claude.mjs`;
`packages/claude/plugin/hooks/pre-tool-use.mjs`.
