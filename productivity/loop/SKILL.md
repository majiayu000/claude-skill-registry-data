---
name: loop
description: >-
  PRIMARY skill for clock-based session wakes via scheduleCallback. Use when the
  user asks for reminders, delays, or recurring checks inside the active
  conversation — "remind me in 5 minutes", "tomorrow at 9", "매일 아침 확인해줘",
  timers, and wall-clock recurrence bound to this chat. NEVER for process exit,
  build/test completion, kanban/ticket done, webhooks, or file-watcher
  completion — use call-me-back. Prefer this over global schedule for in-session
  time requests; escalate to schedule only for permanent app-wide cron.
---

# Loop (PRIMARY for clock-based session wakes)

Session loops inject a message into **the current session** at a **future clock
time** (delay or cron). They preserve conversation context, history, and
workspace, surviving tab switches and app restarts while staying bound to this
session's lifecycle.

The MCP tool is `scheduleCallback` (or `scheduled_task__scheduleCallback`).
The skill name is `loop`.

## vs `call-me-back` (hard split)

| Signal | Skill |
| --- | --- |
| Wall clock / relative delay / cron | **`loop`** (this skill) |
| Process exit, kanban/ticket status, webhook, watcher | **`call-me-back`** |

"끝나면 알려줘" / "작업 끝나고 깨워줘" that means **a job or external event finished**
→ `call-me-back`, not a guessed `delaySeconds`.

## Core Policy: Session-First by Default

When a user asks for a **time-based** reminder or recurring check inside an
active conversation, they almost always expect it **in this conversation**.
Wrong skill choice is usually selecting global `schedule` /
`createScheduledTask`, which drops session context.

**Always default to `loop`** for:
- "Remind me in X minutes / hours / days" ("X분 뒤에 알려줘")
- "Tomorrow at 9" / "내일 9시에 알려줘" when continuing this chat
- "Follow up on this later" ("나중에 확인해줘") when later means a **clock** time
- In-session recurring checks ("매일 아침 9시에 이 작업 현황 알려줘")
- Any relative delay or wall-clock reminder that should reuse this chat's history

### When to escalate to global `schedule`

Escalate to `schedule` (`createScheduledTask`) **ONLY** when:
- The user explicitly asks for independent, permanent, or app-wide automation
  ("even if I close this chat", "전역 백그라운드 작업으로 등록해줘").
- The run must be a standalone assistant task with no session context.
- It is multi-agent coordination driven by global scheduled tasks.

### Handling Ambiguous Requests

If intent is ambiguous (e.g., "매일 9시에 주가 체크해서 알려줘" with no
global/permanent wording):
1. **Proceed with `loop` immediately** — do not ask first by default.
2. **Ask only when** the request looks like always-on automation that should
   survive this chat. Then explain once:
   - **Loop (default)**: injects into this chat; invalidated if the session is deleted.
   - **Global Scheduled Task**: app-wide cron; survives closing/deleting this session.

If ambiguous between **time** and **completion event**, ask one clarifying
question, or prefer `call-me-back` when a concrete process/ticket/system was named.

## Routing decision

```text
Is the wake driven by a completion event (process / kanban / webhook / watcher)?
  Yes -> call-me-back
  No  -> Should the run stay bound to the current session?
           Yes / Unclear -> loop (scheduleCallback) [DEFAULT]
           Explicit global -> schedule (createScheduledTask)
```

Both one-shot (`delaySeconds`) and recurring (`cronExpression`) are supported.
Pick the timing mode, not a different skill — unless the signal is event-based.

## Workflow

### 1. Choose timing mode

Provide **exactly one** of:

- **`delaySeconds`** — one-shot delay (1–86400). Example: 300 for "check back in 5 minutes".
- **`cronExpression`** — recurring. Example: `0 9 * * *` for daily 09:00 local.

Do not pass both. Do not pass neither.

### 2. Create the schedule

```text
scheduleCallback(
  message="...",           // required instruction injected when it fires
  name="...",              // optional Planning panel label
  delaySeconds=300         // OR cronExpression="0 9 * * *"
)
```

Requirements:

- Must run from an **active session** (tool binds automatically).
- `message` must be self-contained for when the agent wakes.
- `assistantId` is NOT required.

### 3. Manage existing session schedules

- `getScheduledTask(taskId)`
- `toggleScheduledTask(taskId, enabled=false)`
- `deleteScheduledTask(taskId)`

Users can also manage these from the session Planning panel.

### 4. Set expectations honestly

- One-shot schedules are deleted after they fire.
- Deleting the session removes its loops; they do not recreate a session.
- Recurring loops keep firing until paused, deleted, or the session is removed.

## Guardrails

- Do not use `createScheduledTask` for in-session time reminders; use `loop`.
- Do not approximate job completion with `delaySeconds`; use `call-me-back`.
- Do not ask for `assistantId` when setting a session reminder.
- Do not require teamwork scaffolding for simple session loops.
- Prefer `delaySeconds` for relative delays; cron for named wall-clock recurrence.
- Give distinct `name` values when scheduling multiple loops.

## Related skills

- **`call-me-back`** — wake on process/kanban/webhook completion (not the clock)
- **`schedule`** — global cron that survives beyond the current session
- **`delegate`** — spawn a child session now
- **`teamwork`** — multi-agent workspace constitution; not needed for simple loops
