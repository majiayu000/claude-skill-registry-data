---
name: body-check
agent: none
description: Compose the AIgent's body state by reading existing signals. Lazy compute. Never polled. Reports the five pressures + recommended reflex.
allowed-tools: Read, Bash
user-invocable: true
triggers:
  - body check
  - body state
  - how am I doing
  - check pressure
  - context pressure
  - memory pressure
  - somatic check
  - vital signs
---

# /body-check

Reports current body state by reading existing signals — does NOT maintain a separate state. Computed on invocation, optionally cached to `memory/BODY_STATE.json` for the session.

## Sources read

- `memory/HEAT_INDEX.json` → attention/decay state
- `memory/usage_log.md` → token pressure (latest entry vs trailing 5)
- `memory/DECISION_LOG.md` + `DECISION_OUTCOMES.md` → decisions due (30/60/90 day intervals)
- `memory/ACTIVE_PRIORITIES.md` → tier-1 / mode
- `memory/DELEGATION_TRACKER.md` → open delegations
- `memory/MEMORY_CANDIDATES.md` → staged backlog count
- `memory/HESTIA_SWEEP_LOG.md` → last Hestia sweep date (v0.4.4)
- Comms API → unread count (only if invoked with `--full`)

## Output schema

Matches `memory/BODY_STATE.json` `_schema` block exactly. See `system/15_somatic_layer.md` for field definitions and pressure thresholds.

## hestia_last_sweep computation (v0.4.4)

Read `memory/HESTIA_SWEEP_LOG.md`. Find the most recent `### YYYY-MM-DD` entry (matches `^### (\d{4}-\d{2}-\d{2})` regex). The newest matching date becomes `hestia_last_sweep` as ISO8601 (`<date>T00:00:00Z`). If no matches, `hestia_last_sweep = null`.

## Recommended reflex logic

Priority order — first match wins:

1. `context_pressure: critical` → recommend `capsule`
2. `memory_candidate_backlog > 10` → recommend `digest`
3. `hestia_last_sweep` is null OR more than 7 days ago → recommend `sweep` (v0.4.4)
4. `decision_reviews_due > 0` → recommend (no action, surface in /open)
5. All low → `none`

## When to run

- On `/open` (auto, briefly)
- Before `/close` (to inform the close protocol)
- Anytime principal asks "how am I doing"
- Before dispatching a heavy multi-agent task (catches "you're already at high context pressure")

Do NOT run on a hook polling cadence.
