---
name: forge-heartbeat
description: Detects a dispatched agent gone silent mid-run from events.jsonl. Use during multi-agent runs or when a run feels quiet — silent agent, stalled run, heartbeat check, timeout.
---

# forge-heartbeat — stall/silence watchdog

Flags a dispatched Boss that went quiet mid-work — crashed, stuck in a loop, or waiting on something
nobody is watching. Read-only: it never touches a live agent, it only reads the real events already
logged.

## When to use

- **During a multi-agent `/forge` run** — periodically, or whenever the run "feels quiet" (no new
  dashboard activity for a while).
- **When the owner asks** "is anything stuck?" or "did that agent die?"
- **As a future forge-doctor check** — same read-only, evidence-only pattern as
  `forge-doctor`/`forge-verify`; can be wired in later without changing this tool's contract.

## How to run

```
node .claude/forge-bin/forge-heartbeat.cjs check <run_id>
  # print stalled agents (or "no stalled agents"), exit 0 clean / 1 stalled

node .claude/forge-bin/forge-heartbeat.cjs check <run_id> --window 15   # override the silence window (minutes)
node .claude/forge-bin/forge-heartbeat.cjs check <run_id> --root <projectRoot>
node .claude/forge-bin/forge-heartbeat.cjs check <run_id> --json        # full machine-readable result
```

## What STALLED means

- An agent is **tracked** once it has logged `agent_started` or `subagent_started`.
- An agent is **finished** — and never flagged, no matter how old its last event is — once it has
  logged `agent_completed`, `subagent_completed`, `agent_failed`, or `subagent_failed` anywhere in its
  history. Silence after a real completion/failure is expected, not a stall.
- An unfinished, tracked agent is **STALLED** when it has been silent for longer than the window
  (default 10 minutes) since its last real event.
- Within stalled agents, **NEVER PROGRESSED** is a stronger flag: the agent's start event is also its
  only event — it never logged a single progress/output event before going quiet.
- Events with no resolvable `timestamp` are never treated as "just happened" or invented a fake time for
  — they're tracked but excluded from the last-seen calculation, so a stall is never hidden or invented
  by a missing timestamp.

## Honesty

- Reads **only** real events from `<run>/events.jsonl` — it never pings a live agent process and never
  guesses at agent state.
- **Silence is a flag to CHECK the agent, not to auto-kill it.** This tool never cancels, restarts, or
  reassigns work — it surfaces a signal for the Lead (or the owner) to look at. A stalled agent might
  simply be doing something slow and legitimate; treat the flag as "go look", not "it failed".
- A malformed line in `events.jsonl` is skipped, never crashes the check, and is reported in the
  `malformed` count.
