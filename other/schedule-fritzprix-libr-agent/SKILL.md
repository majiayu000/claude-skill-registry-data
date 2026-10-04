---
name: schedule
description: Create and manage app-wide global scheduled tasks in LibrAgent (cron-based). Use when automation must outlive the current session, run recurring background cron jobs independently of any session, or coordinate multi-agent scheduled workflows. NEVER use for in-session time reminders (use loop), or for process/kanban/webhook completion waits (use call-me-back).
---

# Schedule

Global scheduled tasks wake an assistant on a cron cadence without requiring the current session to stay open. They run app-wide, are not bound to any conversation session, and do not retain session context.

## Priority & UX Policy

When a user in an active chat session asks to schedule a **time-based** reminder or future check, their natural expectation is that it will happen **within the context of their current conversation**.

Therefore:
- **`loop` is the PRIMARY DEFAULT** for session-originated **clock** requests.
- **`call-me-back`** for process exit, kanban/ticket done, webhooks, or watchers (not cron).
- **`schedule` is strictly for GLOBAL / BACKGROUND cron** that must run independently of the current session.
- **If intent is ambiguous** (e.g., "매일 9시에 요약해줘" with no global/permanent wording):
  1. **Proceed with `loop` immediately** (do not ask first).
  2. **Ask only when** the request looks like always-on automation that should survive this chat (recurring wall-clock work with no tie to this conversation's task/context), and a wrong choice would strand the user. Then explain once and confirm:
     - **Loop (default)**: stays in this chat; dies if the session is deleted.
     - **Global Scheduled Task**: app-wide cron; survives closing/deleting this session; no session history.

## When NOT to use this

Do NOT use `schedule` (`createScheduledTask`) for:
- "remind me in 5 minutes" / "10분 뒤에 알려줘" → use `loop` (`scheduleCallback`)
- "let me know about this later" / "나중에 알려줘" → use `loop`
- "tomorrow at 9" / "내일 9시에 알려줘" when continuing this chat → use `loop`
- Any relative delay or timer (seconds, minutes, hours, or days) → use `loop`
- Any clock reminder where the user expects the response in the current chat → use `loop`
- "작업 끝나고 알려줘" / build·test·ticket completion → use `call-me-back`

## Routing decision

```text
Is the wake driven by a completion event (process / kanban / webhook / watcher)?
  Yes -> call-me-back
  No  -> Should the run stay bound to the current session?
           Yes / Unclear -> loop (scheduled_task__scheduleCallback) [DEFAULT]
           Explicit global -> schedule (scheduled_task__createScheduledTask)
```

Recurring vs one-shot is **not** the primary split for time-based work. Global tasks require cron. Session-bound clock wakes use `loop`; event completion uses `call-me-back`.

## Workflow

### 1. Confirm global scheduling is appropriate

- Use global tasks ONLY for cron-based wake-ups, background recurrence, heartbeat loops, or assistant-level automation that must survive session destruction.
- If the user asked for a time reminder or delay inside this chat, STOP and switch to `loop`.
- If the user asked to wake on process/ticket/webhook completion, STOP and switch to `call-me-back`.
- Do not require teamwork scaffolding for a standalone global task.
- If the user wants org-visible lineage or org-root resume behavior, stop and use `org`.

### 2. Create the task

**Single global task (default path):**

- Use `scheduled_task__createScheduledTask(name, cronExpression, assistantId, message)`.
- Optional: `scheduleTimezone`, `executionMode`, `workspaceOverride`.
- The tool returns a task ID. Keep it for follow-up calls.

### 3. Operate tasks deliberately

- `scheduled_task__listScheduledTasks()` — discover task IDs and enabled state
- `scheduled_task__getScheduledTask(taskId)` — read message, cron, and pinned session state
- `scheduled_task__updateScheduledTask(taskId, ...)` — retune cadence, message, or workspace
- `scheduled_task__toggleScheduledTask(taskId, enabled=...)` — pause or resume
- `scheduled_task__deleteScheduledTask(taskId)` — remove stale automation

### 4. Respect governance limits

- Backend policy enforces a minimum interval between runs.
- Do not assume unlimited frequency.
- If policy limits are reached, widen the cron cadence or request a limit increase through Settings.

### 5. Keep identity clean

- A scheduled task may wake a coordinator, but it is still not an org.
- Org lineage belongs in org tooling, not scheduled-task metadata.

## Teamwork integration (optional)

When the workspace already uses the scheduled teamwork substrate:

1. If the governing root session has not prepared the teamwork artifact directory yet, stop and use `teamwork` to call `agent__prepareTeamworkWorkspace()` first.
2. Read `.libragent/teamwork.json` if present.
3. Confirm `executionSubstrate.mode` is `"scheduled"` when the user expects recurring teamwork automation driven by scheduled tasks.
4. Ensure teamwork scaffold files (`agents.md`, `MISSION.md`, coordination files) are current before a scheduled coordinator wakes up.
5. Treat the app-local teamwork artifact directory as orchestration SSOT; use `workspaceOverride` only when a run must target a different implementation workspace.

If the user only wants one global cron job with no multi-agent constitution, skip teamwork entirely.

## Guardrails

- Do not use global scheduled tasks for simple in-session delays or reminders; use `loop`.
- Do not use global cron to wait for a single process or ticket completion; use `call-me-back`.
- Use `workspaceOverride` only when the scheduled run must target a specific existing workspace.
- Backend minimum-interval policy still applies. Do not assume unlimited frequency.
