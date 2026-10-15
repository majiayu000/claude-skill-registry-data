---
name: evi-cron-self-revival
description: Use when scheduled tasks must survive a session restart — a registry plus a SessionStart self-poke that re-registers in-session cron jobs unattended.
---

# Cron self-revival

In-session cron (`CronCreate`) dies with the session: a restart wipes the whole
schedule. This skill restores it without a human in the loop, by combining a
registry file (single source of truth), a SessionStart instruction injection,
and a `tmux send-keys` self-poke that converts the injected instruction into an
actual turn.

## What it guarantees

After any session restart, every recurring job in `tasks/cron-registry.json` is
re-registered automatically. The agent does not wake up having forgotten its
schedule, and no owner message is needed to trigger the restore.

## How it works

On `startup`, `session-start-restore.py`:

1. Reads `tasks/cron-registry.json` and injects a re-registration instruction
   block (run `CronList`, then `CronCreate` for any missing job) into
   `additionalContext` — the **fallback**.
2. Spawns a detached background process that, after `EVI_SELF_POKE_DELAY`
   seconds, sends `/recron` + Enter to the tmux pane — the **driver**.

The poke matters because **injected context is not a turn**: an agent that only
reads "please re-register your jobs" stays idle until something pokes it. The
`/recron` command ([`../../.claude/commands/recron.md`](../../.claude/commands/recron.md))
then reads the registry, runs `CronList`, registers what is missing, and writes
a `HOOK-FIRE → POKE-SCHEDULED → REGISTERED → DONE` audit trail.

### Field lessons (tmux / launchd send-keys automation)

These were paid for in real operation — keep them in any send-keys driver:

1. **A poke during an active turn loses the Enter.** While the REPL is busy the
   Enter keystroke is silently swallowed and the command never submits. Mitigation:
   re-poke until a **start marker** appears in the log (the driven command writes
   one as its first action); do not assume a single poke landed.
2. **tmux send-keys can hang under launchd.** A launchd-launched send-keys call
   has been observed to block for hours, starving the next interval. Mitigation:
   wrap every send-keys in a background **~10-second watchdog** that `kill -9`s on
   breach.
3. **Send the text and Enter as separate send-keys calls.** A `/`-prefixed input
   opens the slash-command autocomplete popup; sending Enter in the same call
   races the popup and is dropped. Send the text, sleep ~1.5 s, then send Enter.

## Implement in your project

Reference implementations:
- [`../../scripts/hooks/session-start-restore.py`](../../scripts/hooks/session-start-restore.py) (injection + self-poke)
- [`../../.claude/commands/recron.md`](../../.claude/commands/recron.md) (`/recron` procedure)
- [`../../tasks/cron-registry.json`](../../tasks/cron-registry.json) (registry schema)

Wire the SessionStart hook (shared with the `session-restore` skill — one entry
does both):

```json
"SessionStart": [
  { "matcher": "", "hooks": [
    { "type": "command", "command": "EVI_PROJECT_DIR=$CLAUDE_PROJECT_DIR EVI_TMUX_BIN=$EVI_TMUX_BIN EVI_TMUX_TARGET=$EVI_TMUX_TARGET EVI_SELF_POKE_DELAY=$EVI_SELF_POKE_DELAY python3 $CLAUDE_PROJECT_DIR/scripts/hooks/session-start-restore.py" }
  ]}
]
```

Set `EVI_TMUX_TARGET` (find it with `tmux list-panes -a`), `EVI_TMUX_BIN`, and
`EVI_SELF_POKE_DELAY` in `.env`. Populate `tasks/cron-registry.json` with your
jobs; point each `prompt` at a `tasks/<name>.md` procedure.

## Adaptation points

- **No tmux:** keep the `additionalContext` fallback and let the owner type
  `/recron` after restart, or trigger it from your own supervisor. You lose the
  unattended property but keep correctness.
- **systemd instead of launchd:** the hook itself is unaffected (it spawns a
  child process, not a service). Field lesson 2 still applies to any service-run
  send-keys.
- **Durable cron exists in your runtime:** the registry + `/recron` remain the
  recovery path; treat durable persistence as a bonus, not a guarantee.

### Supervise the process itself

This skill revives *schedules*. The REPL process and your MCP servers also
die — give them a supervisor: launchd `KeepAlive` (see `launchd/` for the
plist shape) or systemd `Restart=always`. Assume every process crashes;
design the resurrection path before you design the personality.

## Verify

1. `python3 -m py_compile scripts/hooks/session-start-restore.py` exits 0.
2. `python3 -c "import json; print(len(json.load(open('tasks/cron-registry.json'))['jobs']))"`
   prints the job count (registry is valid JSON).
3. Restart the session, wait `EVI_SELF_POKE_DELAY + 5` s, then check
   `docs/work-log/cron-reregister.log` for `REGISTERED ... / DONE N/N`.
   Note: the audit log (`docs/work-log/cron-reregister.log`) is created on first run by the session-restore hook — it does not need to pre-exist.

## Rollback

Remove the `SessionStart` entry from `.claude/settings.json` (and delete
`.claude/commands/recron.md` if you want the command gone).
