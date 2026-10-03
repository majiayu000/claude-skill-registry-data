---
skill_id: usage-aware-scheduler
name: Usage-Aware Scheduler
description: "Gate scheduled work on Claude usage limits — /mxm-tasks schedule, run-cycle, scheduled task fire time, background batch dispatch. Checks 5-hour and 7-day usage before firing and sleeps until reset when over threshold."
version: 1.0.0
category: automation
type: scheduler
frameworks: []
triggers:
  - "/mxm-tasks schedule *"
  - "/mxm-tasks run-cycle"
  - scheduled task fire time
  - background task batch dispatch
collaborates_with:
  - operator-profile
  - session-memory
  - executive-router
ethics_required: false
priority: high
tags: [automation, scheduling, oauth-usage-api, anthropic-limits, autonomous]
created: 2026-04-16
updated: 2026-04-16
---

# Usage-Aware Scheduler

## Purpose

Wrap `/mxm-tasks` scheduled execution with **Anthropic OAuth usage limit awareness**. Before firing any scheduled task, check current 5-hour / 7-day / 7-day-Opus utilization. If any threshold is exceeded, sleep until `resets_at` rather than slamming into a quota error.

**Maxim is the only multi-agent framework that prevents hitting Anthropic limits during overnight automation.**

Critical for portfolio operators running 21+ projects: a single overnight RAG ingest cycle could otherwise burn through quota for an entire 5-hour window mid-batch.

## When To Invoke

- `/mxm-tasks` runs a scheduled batch
- `/mxm-tasks schedule X` registers a new recurring task
- Manual: user asks "are we close to limit?" → triggers a status check
- Auto: every cycle of the scheduler loop

## Configuration

`config/scheduler-thresholds.json` — pinned global thresholds. Defaults:
- `five_hour_pause_at`: 80%
- `seven_day_pause_at`: 85%
- `seven_day_opus_pause_at`: 80%
- `min_sleep_seconds`: 300 (never sleep <5 min)
- `api_failure_retry_seconds`: 300

User can switch to a preset (`pro`, `max_5x`, `max_20x`) or tune individually.

## Workflow (one cycle)

```
1. FETCH usage from https://api.anthropic.com/api/oauth/usage
   Headers:
     Authorization: Bearer <oauth-token>
     anthropic-beta: oauth-2025-04-20
     User-Agent: claude-code/2.0.32

2. EXTRACT:
   five_hour.utilization, five_hour.resets_at
   seven_day.utilization, seven_day.resets_at
   seven_day_opus.utilization

3. CHECK THRESHOLDS (from config/scheduler-thresholds.json):
   IF five_hour >= five_hour_pause_at:
     sleep_until = five_hour.resets_at
   IF seven_day >= seven_day_pause_at:
     sleep_until = seven_day.resets_at
   IF seven_day_opus >= seven_day_opus_pause_at:
     route Opus tasks to fallback_model_on_opus_pause (or defer)

4. IF any threshold exceeded:
   sleep_seconds = max(min_sleep_seconds, (sleep_until - now))
   LOG sleep event to .mxm-skills/scheduler-events.jsonl
   sleep
   GOTO 1

5. IF all clear:
   LOAD task queue from .claude-sessions-memory/scheduled-tasks.jsonl
   filter: done == false AND (schedule == null OR schedule <= now)
   IF no tasks due:
     sleep no_tasks_due_sleep_seconds
     GOTO 1

6. RUN next due task via:
   claude --print -p "<prompt>" \
     --output-format stream-json \
     --model <task.model OR default_task_model> \
     --timeout <task_timeout_seconds>

7. PERSIST result:
   on success: mark done:true, completed_at:<now>
   on failure: leave done:false (retry next cycle), increment failure_count
   LOG to .mxm-skills/scheduler-events.jsonl

8. GOTO 1
```

## OAuth Token Sources

Per `config/scheduler-thresholds.json → auth.token_source`:

- **macOS**: Keychain — service `Claude Code-credentials`, key `claudeAiOauth.accessToken`
- **Linux / CI**: env var `ANTHROPIC_OAUTH_TOKEN`
- **Windows**: env var `ANTHROPIC_OAUTH_TOKEN` (Credential Manager planned)
- **CLI override**: `--oauth-token <token>`

On 401: refresh path or notify operator. Never proceed without valid token.

## Task Queue Schema

`.claude-sessions-memory/scheduled-tasks.jsonl` (one JSON object per line):

```jsonl
{"id":"nightly-wiki-ingest","prompt":"/mxm-wiki ingest","schedule":null,"model":"claude-sonnet","done":false,"failure_count":0}
{"id":"weekly-wiki-lint","prompt":"/mxm-wiki lint","schedule":"2026-04-19T07:00:00Z","model":"claude-sonnet","done":false,"failure_count":0}
{"id":"daily-portfolio-sync","prompt":"Run sync_portfolio MCP tool and update .mxm-global/","schedule":"2026-04-17T05:27:00-05:00","model":"claude-haiku","done":false,"failure_count":0}
```

**Fields:**
- `id`: unique identifier
- `prompt`: instruction (slash command or natural language)
- `schedule`: ISO datetime; null = run immediately when ready; future = wait
- `model`: optional per-task model override
- `done`: boolean — true = permanently skipped
- `failure_count`: incremented on each failure
- `completed_at`: ISO timestamp on success

## Event Log Format

`.mxm-skills/scheduler-events.jsonl` (per cycle):

```jsonl
{"ts":"2026-04-16T07:00:00Z","event":"cycle_start"}
{"ts":"2026-04-16T07:00:01Z","event":"usage_check","five_hour":42,"seven_day":68,"seven_day_opus":55}
{"ts":"2026-04-16T07:00:01Z","event":"thresholds_clear"}
{"ts":"2026-04-16T07:00:01Z","event":"task_run","id":"nightly-wiki-ingest","model":"claude-sonnet"}
{"ts":"2026-04-16T07:02:34Z","event":"task_complete","id":"nightly-wiki-ingest","duration_s":153}
{"ts":"2026-04-16T07:02:35Z","event":"sleep","seconds":300,"reason":"no_tasks_due"}
```

```jsonl
{"ts":"2026-04-16T20:00:00Z","event":"usage_check","five_hour":85,"seven_day":72,"seven_day_opus":61}
{"ts":"2026-04-16T20:00:00Z","event":"threshold_exceeded","layer":"five_hour","value":85,"limit":80}
{"ts":"2026-04-16T20:00:00Z","event":"sleep","seconds":7200,"reason":"five_hour_threshold","until":"2026-04-16T22:00:00Z"}
```

## Output Format

```
Usage-Aware Scheduler Cycle:
Cycle ID: [uuid]
Started: [ISO timestamp]

Usage Snapshot:
  5-hour:        [X]%   (threshold: 80%)
  7-day:         [Y]%   (threshold: 85%)
  7-day Opus:    [Z]%   (threshold: 80%)

Decision: PROCEED | PAUSE_5H | PAUSE_7D | PAUSE_OPUS

If PAUSE:
  Sleep until: [resets_at ISO]
  Sleep seconds: [N]
  Reason: [layer name]

If PROCEED:
  Tasks due: [N]
  Task run: [task.id] (model: [model], timeout: [N]s)
  Result: SUCCESS | FAILURE | TIMEOUT
  Duration: [N] seconds

Confidence: 🟢 HIGH (clean usage check) | 🟡 MEDIUM (API estimated, not reachable) | 🔴 LOW (API failure, defaulting to safe wait)
```

## Why This Skill Exists

Per `FINAL_RELEASE_CHANGES/claude_scheduler_instructions.md`:

> The 5-hour window is a rolling window starting from your first message, not a fixed clock reset — always use the API's `resets_at` value, never calculate from the hour.
> All Claude usage (claude.ai, Claude Code CLI, IDE extensions) draws from the same shared pool — the API reflects total consumption across all surfaces.

For someone running Maxim across 21 projects with overnight RAG ingestion + daily portfolio syncs + weekly wiki lints, hitting limits mid-batch corrupts state and wastes the next 5 hours. This scheduler treats limits as a first-class constraint.

## Handoff

- Scheduled task fires → execute via Claude Code CLI per workflow
- Threshold exceeded → sleep then retry; notify operator if sleep > 4 hours
- Repeated task failures (failure_count >= 3) → escalate to operator with diagnostics
- Token expiry (401) → refuse to proceed; notify operator to re-auth

## Maxim Behavioral Layer

- **Confidence tagging**: 🟢 on clean usage check, 🟡 on cached/estimated, 🔴 on API failure with fallback
- **Anti-greed**: never override thresholds programmatically; user must edit config
- **Audit trail**: every cycle logged to `scheduler-events.jsonl` for post-hoc analysis

## Source References

- `config/scheduler-thresholds.json` — thresholds + auth + behavior config
- `FINAL_RELEASE_CHANGES/claude_scheduler_instructions.md` — original spec
- `.claude/commands/mxm-tasks.md` — entry point
- `.claude-sessions-memory/scheduled-tasks.jsonl` — task queue
- `.mxm-skills/scheduler-events.jsonl` — event log

---
_Copyright (c) 2026 iSystematic Inc. Maxim product. BSL 1.1._
