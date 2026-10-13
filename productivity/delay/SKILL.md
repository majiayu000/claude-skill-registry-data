---
name: delay
description: "Schedule instructions to run ONCE at a later time in the current session, via a one-shot in-session cron job (CronCreate with recurring: false). Use when: (1) User invokes /delay, (2) User says 'in N hours/minutes do X', 'schedule X for later', 'do this at 16:30', 'remind me in an hour to X', or any other one-shot delayed-execution request. NOT for recurring intervals (use /loop) and NOT for schedules that must survive closing the terminal (use a cloud Routine — the Claude Code Remote `create_trigger` / `send_later` MCP tools, which persist server-side). This skill only schedules — it never executes the instructions immediately."
argument-hint: <time spec>, <instructions>
---

# Delay

Schedule the given instructions to fire exactly once at a future time in this session. Scheduling is the entire task of this turn — do NOT start executing the instructions now, even partially. That is the failure mode this skill exists to prevent: the task running immediately AND again at fire time.

Arguments: `$ARGUMENTS`

## Steps

1. **Parse arguments.** Split at the first comma: everything before it is the time spec ("1 hour later", "in 30 min", "at 16:30", "tomorrow 9am"), everything after is the instructions to run later (pass through verbatim — including slash commands like `/x-wt-teams foo bar`). If either part is missing or the time spec is ambiguous, ask instead of guessing.

2. **Compute the fire time.** Run `date '+%Y-%m-%d %H:%M'` for the current local time, then compute the target:
- Relative spec → add the delta to now.
- Absolute spec already past today → assume the next occurrence (tomorrow).
- Handle rollover: adding hours may cross midnight or month boundaries — the pinned day/month must match the actual target date.

3. **Create exactly one job** with the CronCreate tool:
- `cron`: fully pinned `"M H DOM MON *"` for the target time. Use the exact computed minute — don't round to :00/:30 (the harness fires those up to 90s early, and round marks cause fleet-wide load spikes).
- `recurring`: **false**. This makes the job auto-delete after firing. A recurring job (the default) stays alive and can fire again — the double-invoke bug.
- `prompt`: prefix the instructions so the future turn knows it is a scheduled firing, not a fresh request to schedule:

     ```
     [One-shot task scheduled earlier via /delay, firing now as planned. Do not reschedule or delay again — execute directly:]
     <instructions verbatim>
     ```

4. **Confirm to the user** (and stop — no other tool calls after this):
- The exact fire time and job ID (cancelable via CronDelete by ID).
- The session must stay open — the job is in-memory and dies silently if Claude Code exits.
- The job fires only while the session is idle, so it may start a bit late if work is in progress at the target time.

## Guardrails

- Exactly one CronCreate call per /delay invocation. Don't add wakeups, loops, or Monitor tasks alongside it.
- Never run any part of the instructions in the scheduling turn — not even "harmless prep" like a git pull.
- If the user actually wants a recurring cadence, hand off to /loop; if they need it to survive terminal close, hand it off to a cloud Routine (the Claude Code Remote `create_trigger` / `send_later` MCP tools), which persists server-side instead of dying with the session.
