---
name: call-me-back
description: >-
  Resume this agent session on a completion signal instead of clock polling.
  Use when wiring external hooks/--exec/webhooks that must POST into this
  session (wake URL is already in Agent Runtime Identity), or waiting for
  process exit, ticket/job status, file watchers — "call me back when done",
  "끝나면 깨워줘", "subscribe --exec", "register hook", "완료되면 콜백",
  "webhook으로 깨워줘", "run in background with hook". NEVER for pure time
  reminders or cron ("5분 뒤", "매일 9시") — use loop (session) or schedule
  (global). "me" means this agent session, not a phone call.
---

# Call Me Back (event-driven resume)

Wait for an **external or process completion signal**, then continue this
session. Do not fake completion with `scheduleCallback` / `loop` delays.

**"me"** = this agent session (inject/resume here), not a user phone/SMS alert.

## vs `loop` / `schedule` (hard split)

| Signal | Skill |
| --- | --- |
| Process exit, job/ticket done, webhook, watcher, hook | **`call-me-back`** (this skill) |
| Relative delay / wall-clock / session cron | **`loop`** |
| Permanent app-wide cron | **`schedule`** |

If the user says "끝나면 알려줘" and names a **command, job, ticket, or external system**,
use this skill. If they only name a **clock time**, use `loop`.

## Typical jobs

- Heavy local jobs: builds, tests, training, long scripts
- Background process already started via `workspace__spawnProcess`
- External systems that fire on real events (hooks, webhooks, watchers)
- Waiting for a named job/ticket/status change (not a clock guess)

## Out of scope

- "Remind me in 10 minutes" / "내일 9시에" → `loop`
- Always-on global cron with no session binding → `schedule`
- Immediate child-session work with no wait → `delegate`

## Workflow

### A. Local long-running command

1. Start (or reuse) a background process:
   `workspace__spawnProcess` (or a sync tool that handed off a `processId`).
2. Block on completion — do **not** poll with `loop`:
   `workspace__waitForProcess(processId=..., timeout=...)`
   (`waitForProcess` wakes on process notify; it is the built-in call-me-back for shells.)
3. On finish, read output if needed:
   `workspace__readProcessOutput(processId=...)`
4. Continue the user task with the result (pass/fail, logs, next steps).

Prefer one `waitForProcess` over repeated short waits or clock callbacks.

### B. External systems (hooks / webhooks / watchers)

**Success** = a message lands in **this** LibrAgent session and the workflow resumes.
Stdout from an external gateway/hook process is **not** resume.

#### Contract (product-agnostic)

Whatever registers the external callback (hook command, webhook URL, watcher script)
must **wake this harness** by injecting into this session. Do **not** add per-product
recipes to this skill — read that system's own hook docs, then wire its payload here.

**Harness wake (SSOT):**

Agent Runtime Identity already injects the concrete wake URL for **this** session
(`External wake (this session): POST http://127.0.0.1:<port>/api/sessions/<id>/messages`).
Copy that URL — do not invent a path or leave `--exec` as `echo` / file-append only.

- Body: JSON `{"content":"<event summary>"}` (optional `"source":"api"`).
- Channel-style alternative: `POST …/channel` with `serverName` + `content` (+ optional `meta`).

Map the external event (env, stdin JSON, query, body) **into** that `content` / `meta`.
The external side only needs to run something that performs this inject.

#### Two phases

1. **Register** the external callback once (that system's register API).
2. **When woken** (this session receives the inject): continue the original task here.

Do not treat “callback registered” as done unless wake/inject is wired.
Do not assume work done only inside the external callback will appear in this chat.

#### Anti-patterns

- External callback that only logs, `echo`s, or appends a file — **no session inject**
- Registering `--exec` / a webhook without the Runtime Identity wake `POST`
- “Callback runs outside this process so it cannot reach this chat” — **false**; inject is the reach
- Blocking long-poll / foreground watchers when a non-blocking register-callback API exists
- Faking completion with `scheduled_task__scheduleCallback` / `loop` delays

#### If the system only offers coarse polling

Prefer its native wait/watch over LibrAgent clock loops, and keep poll intervals
honest in the reply. Prefer inject/wake whenever a callback hook exists.

### C. Ambiguous "끝나면 알려줘"

- Named process/command/job/ticket/system → this skill
- Only a duration or clock time → `loop`
- Still unclear → ask once: time-based reminder, or wait for a specific completion?

## Guardrails

- Do not use `scheduled_task__scheduleCallback` as a stand-in for job completion.
- Do not busy-poll via many tiny `loop` delays or LLM turn spam.
- Do not invent `processId` values; only use ids returned by workspace tools.
- Do not treat this skill as user push-notification / telephony.
- Keep session context: completion should resume **this** chat unless the user
  explicitly asked for a global scheduled worker (`schedule`).
- Do not invent per-product command catalogs in this skill; reuse the inject contract.

## Related skills

- **`loop`** — clock-based session reminders and recurring checks
- **`schedule`** — global cron automation
- **`delegate`** — spawn work in a child session now
- **`libragent-harness-reference`** — HTTP inject path / session id facts
- **`teamwork` / `org`** — multi-agent constitution; not required for a single wait
