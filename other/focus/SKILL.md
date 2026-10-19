---
name: focus
description: Manage a Pomodoro focus timer. Use /focus start, /focus break, /focus long, /focus stop, or /focus for current status.
purpose: Runs a Pomodoro focus timer.
stage: desk
---

# Focus Timer

State file: `~/.claude/.pomodoro_state`
Notified flag: `~/.claude/.pomodoro_notified`

## Parse the argument

- No arg or `status` → show current status (read state file, calculate remaining)
- `start` → 25-min work session
- `break` or `short` → 5-min short break
- `long` → 15-min long break
- `stop` or `reset` → stop and clear

## Starting a session

Delete the notified flag, then write the state file:

```bash
rm -f ~/.claude/.pomodoro_notified
printf 'START_TIME=%s\nDURATION=%s\nTYPE=%s\n' "$(date +%s)" "<seconds>" "<type>" \
  > ~/.claude/.pomodoro_state
```

Durations and types:
| Command | TYPE | DURATION |
|---------|------|----------|
| `start` | `work` | `1500` |
| `break` / `short` | `short_break` | `300` |
| `long` | `long_break` | `900` |

Confirm to the user: "Focus timer started — 25 min" (or appropriate label).

## Stopping

```bash
rm -f ~/.claude/.pomodoro_state ~/.claude/.pomodoro_notified
```

Confirm: "Focus timer stopped."

## Status

Read the state file, source it, compute remaining:

```bash
source ~/.claude/.pomodoro_state
remaining=$(( DURATION - ($(date +%s) - START_TIME) ))
```

Report remaining time and session type. If expired, say "Session complete — start a break with /focus break or a new session with /focus start."
If no state file exists, say "No active focus session. Start one with /focus start."
