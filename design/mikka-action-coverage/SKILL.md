---
name: mikka-action-coverage
description: "Audit business command-to-UI reachability and UI-to-command behavior in Mikka. Use when an operation exists in APIs but has no button/menu, a state lacks a change path, different views disagree, a control is dead, or feedback claims success without a durable result."
---

# Mikka action coverage: capability <-> affordance

## Inputs and authority

Read `docs/design/glossary.md`, `docs/design/work-domain-api.md`, `scripts/entity-ui-policy.mjs`, `scripts/interaction-policy.mjs`, `lib/issue-meta.ts`, `lib/task-state.ts`, and the current public/hosted code. Preserve the one canonical writer and authorized state projection. Source presence is a candidate; actual imports show which renderer can mount the action. Establish reachability by navigating the running official build as the expected user.

**Separate business state from derived display state.** For Task, writable `IssueStatus` comes from `ISSUE_STATUS_CODES` (`backlog/todo/doing/review/done/canceled/duplicate`); `waiting/blocked/failed/running/queued` in `task-state.ts` are derived from Task/Run/Factory. Do NOT demand a button that directly sets derived `running`, or conflate stopping a Run with closing a Task.

## Forward trace: capability to UI

For each promised user job or business command:
1. Find its authoritative API/service, input, preconditions, ACL, valid business transitions and durable output. Record the exact module and source SHA.
2. Record legitimate roles: owner, member/lead, organization, read-only, revoked, Cloud and self-hosted where applicable. Decide which entry surfaces promise the action; not every compact list must duplicate a full detail panel. An explicit, reliable transition into canonical detail can satisfy reachability.
3. Follow actual imports/provider composition: `command -> controller/contract -> public adapter -> hosted slot/native variant -> user-reachable route`. A `TaskDetailRow.menu` declaration alone is not proof the view mounts it. Trace keyboard and touch affordances.
4. Flag `verified-missing` only after source + live-route/behavior evidence shows an expected authorized user has no discoverable completion path. Otherwise `source-only-candidate` or `not-tested`.

## Reverse trace: UI to business

For each actionable Button, menu, link, toggle, keyboard command or selection: inspect real accessible name, event handler, API/writer, preconditions, acknowledgement, persistence, refresh/side effect and error recovery. A handler, `setOpen`, toast or optimistic state alone is insufficient. Check that a disabled/unavailable action is explained, and that an authorized viewer can complete the action when conditions permit.

Check both role denial and permitted success. For concurrent writes, lost ACK and replay verify exactly-once business effect or a well-defined idempotent outcome; do not infer from frontend changes.

## Operation matrix (one row per distinct contract, not every visual pixel)

`entity | user job | command/authority | writable/derived state and precondition | role/permission | promised entry | actual reachable path | handler/API | success readback | negative/recovery test | platform | public/hosted SHA | evidence | classification | owner/issue`

Minimal Task example: `Task | set todo -> doing | saveIssue status | Task business status | authorized editor | Issues detail | TaskDetail -> FramedTask -> TaskDetailRow status menu -> hosted Value Dropdown | onStatus -> saveIssue | canonical read/PG | 403/409/conflict | Web | fixed pair | source-only until real click | source-only-candidate`. The current full TaskDetail source **already contains** this menu; do not file a blanket missing-Status issue based on the absence of a standalone Button.

Use the existing `#1979` entity source-of-truth and `#1980` guards to dedupe. Prefer a machine-readable authoritative operation contract owned near the service, with a targeted falsifiable test for each new must-reach operation. Never auto-generate expected outcomes from the same implementation being tested.

## Severity and exceptions

Distinct diagnoses: `missing-affordance`, `dead-control`, `misleading-feedback`, `action-parity-gap`, `state-model-drift`, `error-recovery`, `permission-mismatch`. An intentionally read-only summary, capability unavailable due to a legitimate permission or a derived runtime state is **not** a defect if the UI clearly communicates that constraint. Exceptions name owner, route, reason, expiry if temporary, and an independent regression.
