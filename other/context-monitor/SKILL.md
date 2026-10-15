---
name: evi-context-monitor
description: Use when an agent should warn at context and rate-limit thresholds without spamming — a quiet monitor that speaks only when a new threshold is crossed.
---

# Context monitor

A monitor, not a guard — it blocks nothing. It reads the harness status file and
emits a short notification only when a new usage threshold is crossed, so it can
be wired to a frequent event and still stay quiet almost all the time.

## What it guarantees

The agent (and owner) get a heads-up before context fills or a rate window
drains — once per threshold step, never on every tool call. At 80% context the
message suggests `/compact`. State resets when the session changes, so each new
session starts with fresh thresholds.

## How it works

`check-context.sh` reads `/tmp/claude-status.json` and compares current usage
against the last-fired thresholds stored in `/tmp/claude-threshold-state.json`:

- context window: warn at 50%, then every 10%; suggest `/compact` at 80%
- 5-hour rate: warn at 30%, then every 10%
- 7-day rate: warn at 30%, then every 10%

It prints a line only when a step is newly crossed; otherwise it prints nothing
and exits 0. State is keyed on session id and reset on a new session.

## Implement in your project

Reference implementation: [`../../scripts/hooks/check-context.sh`](../../scripts/hooks/check-context.sh)

Wire it on a frequent event such as `PostToolUse` (see
[`../../.claude/settings.json`](../../.claude/settings.json)):

```json
"PostToolUse": [
  {
    "matcher": "",
    "hooks": [
      { "type": "command", "command": "EVI_TZ=$EVI_TZ bash $CLAUDE_PROJECT_DIR/scripts/hooks/check-context.sh" }
    ]
  }
]
```

It depends on a statusline component writing `/tmp/claude-status.json` with
`context_window.used_percentage` and `rate_limits.*`.

## Adaptation points

- **No statusline writing the status file:** this is the hard dependency. Either
  wire your own statusline to emit `/tmp/claude-status.json`, point
  `EVI_STATUS_FILE` at your equivalent, or skip this skill — it is the most
  optional of the set.
  Minimal schema: `{"context_window":{"used_percentage":N},"rate_limits":{"five_hour":{"used_percentage":N,"resets_at":epoch}}}`
  Written by the statusline component. If the file is absent this skill skips silently.
- **Different thresholds:** edit the `current_threshold` start values (50/30/30)
  and the `/compact` trigger (80) to taste.
- **Reset-time display:** `EVI_TZ` controls the timezone shown for rate-window
  resets; defaults to UTC.

## Verify

1. `bash -n scripts/hooks/check-context.sh` exits 0.
2. With no status file present, running it exits 0 and prints nothing.
3. With a crafted status file at 85% context, it prints a `/compact` suggestion
   once; a second run prints nothing (threshold already fired).

## Rollback

Remove the `PostToolUse` entry from `.claude/settings.json`.
