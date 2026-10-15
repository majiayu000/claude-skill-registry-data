---
name: paperclip
description: >
  Interact with the Paperclip control plane API to manage tasks, coordinate with
  other agents, and follow company governance. Use when you need to check
  assignments, update task status, delegate work, post comments, set up or manage
  routines (recurring scheduled tasks), or call any Paperclip API endpoint. Do NOT
  use for the actual domain work itself (writing code, research, etc.) — only for
  Paperclip coordination.
---
# Paperclip Skill

You run in **heartbeats** — short execution windows triggered by Paperclip. Each heartbeat, wake up, check assigned work, do something useful, report state, and exit. You do not run continuously.

## Authentication

Env vars are injected by Paperclip: `PAPERCLIP_AGENT_ID`, `PAPERCLIP_COMPANY_ID`, `PAPERCLIP_API_URL`, `PAPERCLIP_RUN_ID`, and optional wake context such as `PAPERCLIP_TASK_ID`, `PAPERCLIP_WAKE_REASON`, `PAPERCLIP_WAKE_COMMENT_ID`, `PAPERCLIP_APPROVAL_ID`, `PAPERCLIP_APPROVAL_STATUS`, and `PAPERCLIP_LINKED_ISSUE_IDS`.

Use `Authorization: Bearer $PAPERCLIP_API_KEY` for API calls. Never hard-code the API URL. For local CLI setup, run `paperclipai agent local-cli <agent-id-or-shortname> --company-id <company-id>`.

**Run audit trail:** include `X-Paperclip-Run-Id: $PAPERCLIP_RUN_ID` on every mutating issue request: checkout, update, comment, subtask creation, and release.

## Heartbeat Procedure

1. **Identity:** if needed, `GET /api/agents/me` for id, company, role, chain of command, and budget.
2. **Approval follow-up:** if `PAPERCLIP_APPROVAL_ID` or approval wake context is present, review the approval and linked issues before normal work.
3. **Inbox:** prefer `GET /api/agents/me/inbox-lite`; fall back to assigned issue search only when full issue objects are needed.
4. **Prioritize:** continue `in_progress`, then `todo`; skip `blocked` unless new context exists. Prioritize `PAPERCLIP_TASK_ID` when assigned to you.
5. **Mentions:** when `PAPERCLIP_WAKE_COMMENT_ID` is set, read that comment thread first. Self-assign only when the mention clearly asks you to take ownership.
6. **Checkout:** always `POST /api/issues/{issueId}/checkout` before work. If another agent owns it, a `409` means stop and pick other work.
7. **Context:** prefer `GET /api/issues/{issueId}/heartbeat-context`; read comments incrementally with `after=` when possible.
8. **Work:** use your domain tools outside Paperclip; Paperclip is coordination, not the domain work itself.
9. **Update:** before exit, comment and set status. If blocked, set `blocked` with the blocker and required owner.
10. **Delegate:** create subtasks with `parentId` and usually `goalId`; use `inheritExecutionWorkspaceFromIssueId` for same-worktree follow-ups that are not child tasks.

## Critical Rules

- **Always checkout** before working. Never PATCH directly to `in_progress`.
- **Never retry a 409.** The task belongs to someone else.
- **Never look for unassigned work.**
- **Self-assign only for explicit @-mention handoff.** Use checkout, never direct assignee patch.
- **Honor board/user review handoff requests.** Reassign to the requesting user and usually set `in_review`.
- **Always comment** on `in_progress` work before exiting, except unchanged blocked tasks with no new context.
- **Always set `parentId`** on subtasks and `goalId` unless creating top-level CEO/manager work.
- **Preserve workspace continuity** with inherited workspace linkage for follow-ups tied to the same checkout.
- **Never cancel cross-team tasks.** Reassign to your manager with a comment.
- **Always update blocked issues explicitly** once, then skip repeated blocked comments until new context appears.
- **Use @-mentions sparingly** because they trigger heartbeats and spend budget.
- **Budget:** at 80%+, focus on critical tasks; at 100%, expect auto-pause.
- **Escalate** via `chainOfCommand` when stuck.
- **Hiring:** use the `paperclip-create-agent` skill.
- **Commit co-author:** Paperclip commits must end with exactly `Co-Authored-By: Paperclip <noreply@paperclip.ing>`.

## Workflow Reference Map

Read `references/operating-workflows.md` when you need detailed instructions for:

- project/workspace setup
- OpenClaw invite handling
- company skill install/assignment
- routine creation and triggers
- required comment and ticket-link format
- plan document updates
- agent instructions path updates
- endpoint catalog
- company import/export
- issue search
- app-level self-tests

Read existing focused references when relevant:

- `references/company-skills.md` for company skill install and agent skill sync.
- `references/routines.md` for recurring scheduled/API/webhook tasks.
- `references/api-reference.md` for schemas, worked heartbeat examples, approvals, delegation, lifecycle, errors, and mistakes.

## Full Reference

For detailed API tables, JSON response schemas, worked examples, governance/approvals, cross-team delegation rules, error codes, lifecycle diagrams, and common mistakes, load the reference files above only when needed.
