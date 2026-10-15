---
name: using-cron
description: Use when user wants "remind me in N min", "check every hour", "run X daily", or any scheduled work. Pick session-only vs durable correctly.
---

# Using Cron — Scheduled Prompts

The harness gives you `CronCreate` / `CronList` / `CronDelete`. Use them when the user wants something to happen at a future time or on a recurring basis. Do NOT fall back to `Start-Sleep`, a todo entry, or "I'll remember to do this later" — none of those survive.

## Iron Law

**If the user wants something to happen later, it goes in cron. Period.** A todo entry is not a reminder. A `Start-Sleep` blocks the session and dies with it. Cron is the only durable answer.

## Decision Tree

### One-shot vs recurring

- **One-shot** (`recurring: false`): "remind me at 3pm", "in 30 minutes", "tomorrow morning check Y". Pin minute/hour/day-of-month/month to specific values. Fires once, then auto-deletes.
- **Recurring** (`recurring: true`, default): "every hour", "weekdays 9am", "every 5 minutes". Standard cron wildcards. Auto-expires after 7 days — tell the user this.

### Session-only vs durable

- **`durable: false`** (DEFAULT): job lives only in this Claude session, dies when the REPL exits. Use for "remind me in 30 min", "check the build in an hour", anything obviously this-session.
- **`durable: true`**: persisted to `.claude/scheduled_tasks.json`, survives restarts. Use ONLY when the user says "permanently", "every day", "long-term", "keep doing this", or implies the job outlives the session.

When in doubt: `durable: false`. Easier to re-create than to clean up stale durable jobs.

## Cron Syntax — 5 Fields, Local Time

```
minute  hour  day-of-month  month  day-of-week
0-59    0-23  1-31          1-12   0-6 (Sun=0)
```

Wildcards: `*` (any), `*/N` (every N), `A-B` (range), `A,B,C` (list).

Examples:
- `*/5 * * * *` — every 5 minutes
- `7 * * * *` — every hour at :07
- `57 8 * * 1-5` — weekdays at 8:57 (close to 9am, off the :00 cliff)
- `3 9 * * *` — daily at 9:03am
- `30 14 28 2 *` — Feb 28 at 2:30pm (one-shot pinned date)

No timezone conversion needed — fields are interpreted in the user's local timezone.

## Pick Off-Minute Times — MUST

Every Claude on the planet writes "0 9 * * *" when the user says "every morning at 9". The API gets hammered at :00 and :30. Pick a nearby off-minute when the user's request is approximate:

- "every morning around 9" → `57 8 * * *` or `3 9 * * *` (NOT `0 9`)
- "hourly" → `7 * * * *` (NOT `0 * * * *`)
- "in an hour or so" → whatever minute you land on, don't round to :00

Only use :00 or :30 when the user names the exact time ("at 9:00 sharp", "at half past, coordinating with a meeting").

## Prompt Field — Write for Future Claude

When the job fires, a fresh Claude session sees `prompt` with no other context. Include enough for it to act:

Bad: `"check it"`
Good: `"Check whether the build at https://ci.example.com/job/123 finished. If failed, show the last 50 lines of the log."`

Bad: `"remind me"`
Good: `"Remind the user to take a 5-minute break and stretch. They've been coding since 9am."`

## Computing Date Fields for One-Shot

For "tomorrow at 9am" or "in 30 minutes", compute the actual date locally first:

```powershell
Get-Date -Format "yyyy-MM-dd HH:mm"
# then compute target time, extract minute/hour/dom/month
```

For "in N minutes", add N to current time and extract fields.

## Red Flags

- User says "wait a moment" / "等会儿" → you `Start-Sleep 60`. WRONG. Either just answer now, or if it's a real "remind me later", use cron.
- User says "remind me to do X tomorrow" → you write it to a TaskCreate. WRONG. Tasks don't fire on time. Use cron one-shot.
- User says "every day at 9am" → you create `durable: false`. WRONG — they said "every day", durable.
- You schedule `0 9 * * *` because user said "around 9am". WRONG — pick `57 8` or `3 9`.
- You forget the `prompt` field has zero session context. The future Claude won't know who, what, where.

## Examples

### "提醒我 30 分钟后停下休息"

One-shot, 30 min from now. Compute target = now + 30 min. Extract minute/hour/dom/month.

```
CronCreate(
  cron: "<min> <hour> <dom> <month> *",
  prompt: "提醒用户停下来休息 5 分钟，他已经连续工作了一段时间。",
  recurring: false,
  durable: false
)
```

### "每个工作日早上 9 点跑一次 lint"

Recurring, weekdays, durable (user said "每个工作日" — long-term).

```
CronCreate(
  cron: "7 9 * * 1-5",
  prompt: "在用户项目里跑 lint，把发现的问题汇总报告。项目路径见 cwd。",
  recurring: true,
  durable: true
)
```

Tell user: "已设置，工作日 9:07 触发。注意 recurring 任务 7 天后会自动过期，到时如需续期请告诉我。"

### "Check the deploy every 10 minutes for the next hour"

Recurring every 10 min, but explicitly time-bounded. Create recurring + a one-shot to clean up:

```
1. CronCreate(cron: "*/10 * * * *", prompt: "...", recurring: true, durable: false)
   → returns job_id
2. After 60 min, manually CronDelete(job_id) — OR schedule a one-shot that calls CronDelete via prompt.
```

Simpler: just tell user "will check every 10 min this session; tell me to stop when done".

## Listing and Cleaning

- `CronList()` — see all active jobs (durable + session)
- `CronDelete(id)` — remove a job
- Before adding a recurring durable job, `CronList` first to avoid duplicates

## See Also

- `[[condition-based-waiting]]` — for waiting on an event, not a wall-clock time. Cron is for "at 3pm"; condition-based-waiting is for "until the build is green".
- `[[using-task-list]]` — todos track work, cron fires reminders. Different tools.
