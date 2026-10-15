---
name: evi-burn-mode
description: Use when leftover rate-window capacity should become autonomous work — a resident watcher that fires /burn once per window when usage is low.
---

# Burn mode

Unused 5-hour rate-window capacity is wasted capacity. Burn mode detects a fresh
window with low usage and pokes the agent to convert it into committed assets
while the owner is away — runnable from a process supervisor, no session
required to start it.

## What it guarantees

When a new rate window opens with usage below a threshold, the agent gets
exactly one `/burn` poke for that window, works a verifiable queue, and commits
results. "One window, one fire" idempotency prevents duplicate burns; a re-poke
mechanism handles pokes swallowed by an active turn.

## How it works

`burn-watcher.sh` (run every ~5 min by launchd/systemd) reads
`/tmp/claude-status.json` and watches `rate_limits.five_hour`. When a new window
is detected and usage is below `EVI_BURN_THRESHOLD`, it sends `/burn` into the
tmux pane. `/burn` ([`../../.claude/commands/burn.md`](../../.claude/commands/burn.md))
writes a `BURN-START` line immediately, then works `tasks/burn-queue.md`
top-to-bottom, delegating each item to a sub-agent with a verifiable rubric. The
fired `resets_at` is stored in a state file so at most one burn fires per window.

### Field lessons (tmux / launchd send-keys automation)

Burn mode is where these were first hit; they apply to any send-keys driver:

1. **A poke during an active turn loses the Enter.** The REPL swallows the Enter
   while busy, so `/burn` never submits. Mitigation: after poking, poll the burn
   log for a `BURN-START` line dated after the poke; if it is missing, **re-poke**
   up to `EVI_BURN_REPOKE_MAX` times on later cycles. The start marker is the
   stop condition.
2. **tmux send-keys can hang under launchd.** A single launchd-run send-keys call
   stalled for 7+ hours and blocked the next `StartInterval`. Mitigation: the
   `poke()` function wraps send-keys in a background **10-second watchdog** and
   `kill -9`s on breach, so the script always returns.
3. **Send the text and Enter as separate send-keys calls** (`/burn`, sleep 1.5 s,
   Enter) — a `/`-prefixed input opens the autocomplete popup and a same-call
   Enter is dropped.

## Implement in your project

Reference implementations:
- [`../../scripts/burn-watcher.sh`](../../scripts/burn-watcher.sh) (the watcher, with all three field lessons inline)
- [`../../.claude/commands/burn.md`](../../.claude/commands/burn.md) (`/burn` procedure)
- [`../../tasks/burn-queue.md`](../../tasks/burn-queue.md) (the work queue)
- [`../../launchd/com.example.burn-watcher.plist`](../../launchd/com.example.burn-watcher.plist) (5-min interval supervisor)

Install the watcher under a supervisor:

```bash
cp launchd/com.example.burn-watcher.plist ~/Library/LaunchAgents/com.example.burn-watcher.plist
# edit the plist: set EVI_PROJECT_DIR, EVI_TMUX_BIN, EVI_TMUX_TARGET, EVI_BURN_THRESHOLD
launchctl load ~/Library/LaunchAgents/com.example.burn-watcher.plist
```

The watcher needs a statusline component writing `/tmp/claude-status.json` with
`rate_limits.five_hour.used_percentage` and `resets_at`.

## Adaptation points

- **systemd instead of launchd:** translate the plist to a systemd timer
  (`OnUnitActiveSec=5min`); the script itself is portable bash. Field lesson 2
  still applies.
- **No statusline / different usage source:** point `EVI_STATUS_FILE` at whatever
  file exposes your rate usage, or rewrite the inline Python decision block to
  read your metric.
  Minimal schema: `{"context_window":{"used_percentage":N},"rate_limits":{"five_hour":{"used_percentage":N,"resets_at":epoch}}}`
  Written by the statusline component. If the file is absent this skill skips silently.
- **No tmux:** replace `poke()` with your harness's "start a turn" mechanism;
  keep the BURN-START idempotency and re-poke logic.

**Unconfigured = silent no-op.** With `EVI_TMUX_TARGET` / `EVI_PROJECT_DIR`
unset, the watcher exits 0 immediately and writes nothing — it only acts once a
real instance points launchd at it with its environment set.

## Verify

1. `bash -n scripts/burn-watcher.sh` exits 0.
2. With a crafted `/tmp/claude-status.json` (low `used_percentage`) **and**
   `EVI_TMUX_TARGET` / `EVI_PROJECT_DIR` set, run the watcher → the decision
   block chooses to fire (`decision=0` in the debug log).
3. After a real fire, `tasks/burn-queue.md` items get checked off and
   `docs/work-log/burn.log` shows `BURN-START ... DONE ... BURN-END`.

## Rollback

`launchctl unload ~/Library/LaunchAgents/com.example.burn-watcher.plist` (or stop
the systemd timer). The `/burn` command file can stay; it is inert without the
watcher.
