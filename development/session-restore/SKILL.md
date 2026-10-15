---
name: evi-session-restore
description: Use when a fresh session should start with memory already loaded — a SessionStart hook that injects the memory index and recent daily log into context.
---

# Session restore

A `SessionStart` hook that injects the agent's persistent memory into every new
session, so it wakes up with context instead of a blank slate. (The same hook
also drives cron re-registration — that half is documented in the
`cron-self-revival` skill; this skill covers the memory-injection half.)

## What it guarantees

Every fresh session begins with the memory index (`memory/MEMORY.md`) and the
tail of today's daily log injected into context. The agent does not start each
session having forgotten who its owner is or what happened today. A `clear`
source is respected — if the user intentionally wiped context, nothing is
re-injected.

## How it works

On SessionStart the hook reads the `source` field (`startup` / `resume` /
`compact` / `clear`). For every source except `clear` it builds an
`additionalContext` block from `memory/MEMORY.md` and the last ~40 lines of
`memory/daily/YYYY-MM-DD.md`, and returns it as
`{"hookSpecificOutput":{"hookEventName":"SessionStart","additionalContext":...}}`.
Claude Code injects that string into the session context.

## Implement in your project

Reference implementation: [`../../scripts/hooks/session-start-restore.py`](../../scripts/hooks/session-start-restore.py)

Wire it on `SessionStart` (see
[`../../.claude/settings.json`](../../.claude/settings.json)):

```json
"SessionStart": [
  {
    "matcher": "",
    "hooks": [
      { "type": "command", "command": "EVI_PROJECT_DIR=$CLAUDE_PROJECT_DIR EVI_TMUX_BIN=$EVI_TMUX_BIN EVI_TMUX_TARGET=$EVI_TMUX_TARGET EVI_SELF_POKE_DELAY=$EVI_SELF_POKE_DELAY python3 $CLAUDE_PROJECT_DIR/scripts/hooks/session-start-restore.py" }
    ]
  }
]
```

You need `memory/MEMORY.md` to exist (it can start as a short index) and the
daily log convention from the `daily-diary` skill.

## Adaptation points

- **Different memory layout:** change the two file paths the hook reads. The
  contract is just "produce an `additionalContext` string"; what you put in it is
  yours.
- **Inject more/less:** tune `DAILY_TAIL_LINES`, or add a third source (e.g. an
  open-tasks file). Keep it small — injected context costs tokens every session.
- **Memory-only (no scheduler):** if you do not want the cron self-poke, set
  `EVI_TMUX_*` to empty / ignore them; the memory injection works standalone. The
  poke only fires on `startup` when a cron registry exists.

**Unconfigured = silent no-op.** The cron-reregistration block and the tmux
self-poke only run when a `.env` exists in the project dir, so an unconfigured
clone injects no schedule and pokes nothing. Memory injection is independent —
it is simply empty until you have a `MEMORY.md` / daily log.

## Verify

1. `python3 -m py_compile scripts/hooks/session-start-restore.py` exits 0.
2. `echo '{"source":"startup"}' | EVI_PROJECT_DIR=$PWD python3 scripts/hooks/session-start-restore.py`
   prints JSON containing `additionalContext` (given a non-empty MEMORY.md).
3. `echo '{"source":"clear"}' | python3 scripts/hooks/session-start-restore.py`
   prints nothing (clear is respected).

## Rollback

Remove the `SessionStart` entry from `.claude/settings.json`.
