---
name: spell-schedule
description: |
  Schedule a moflo spell to run on the local machine via the moflo daemon (cron, interval, or one-time).
  Use when the user wants to schedule, automate, or recurringly run one of THEIR spells locally —
  e.g. "schedule the oap spell every hour", "run my audit spell every weekday at 9am", "fire X once tomorrow morning".
  This is the LOCAL daemon path. For remote Anthropic-cloud agents, use /schedule instead.
arguments: "<spell-name-or-alias>"
---

# /spell-schedule — Schedule a Local Spell

This skill walks the user through scheduling a moflo spell on the **local** moflo daemon.
Schedules live in moflo's memory store and are evaluated once per minute by the daemon's poll loop.
Execution goes through the same engine path as `flo spell cast`.

> Not the same as `/schedule`. `/schedule` creates **remote** Anthropic-cloud routines; this skill drives the **local** daemon scheduler.

**Arguments:** `$ARGUMENTS` (optional spell name/alias to pre-select)

## When to use

The user says any of:
- "schedule the X spell"
- "run X every <interval>"
- "fire X once at <time>"
- "set up a recurring run for X"
- "I want X to run every morning"

If the user wants a **cloud** agent (mentions "remote", "GitHub Actions", "Anthropic cloud", or specifies a repo to clone), redirect them to `/schedule`.

## Workflow

### Step 1 — Verify the daemon is running

```bash
npx flo doctor 2>&1 | grep -i daemon
```

If the daemon is not running, prompt the user:
- "The moflo daemon isn't running. Schedules only fire while the daemon is up. Start it now?"
- If yes: `npx flo daemon start`.
- If they decline, warn the user that the schedule will be created but won't fire until the daemon is started.

OS-native autostart (launchd / systemd / Task Scheduler) is **automatic**: the
first `flo spell schedule create` registers the daemon as a login service so
schedules survive reboot, and the cancel that takes the enabled-schedule count
to 0 unregisters it. Users only need to think about it in two cases:

- `--no-autostart` on `create` — skip registration (use in containers/CI where
  the daemon is already managed externally).
- `--keep-autostart` on `cancel` — keep the login service registered through a
  cancel-then-recreate dance.

### Step 2 — Identify the target spell

If `$ARGUMENTS` was provided, use it as the spell name/alias. Otherwise, list spells and let the user pick:

```bash
npx flo spell list 2>&1
```

The output is a markdown table with columns: name, alias, description, source. Both `name` and `alias` are valid for `flo spell schedule create -n <value>` — prefer the full name to avoid alias conflicts.

If the user-named spell is not in the list, stop and ask. Do NOT silently create a schedule for a missing spell — it will be auto-disabled on first fire.

### Step 3 — Pick the cadence

Use AskUserQuestion to offer four options:

| Option | When to suggest | CLI form |
|--------|-----------------|----------|
| **Cron** | Specific time of day, day of week, or month boundary | `--cron "<5-field cron>"` (UTC, 5 fields: minute hour day-of-month month day-of-week) |
| **Interval** | "Every N seconds/minutes/hours/days" with no specific clock anchor | `--interval <N><s\|m\|h\|d>` (e.g., `30m`, `6h`, `1d`) |
| **One-time** | "Run once at..." or "remind me to..." | `--at <ISO 8601 datetime>` |
| **Embedded in spell** | The schedule should travel with the spell definition (registered every daemon start) | Edit the spell YAML to add a `schedule:` block; no CLI |

#### Timezone conversion (CRITICAL)

Cron expressions and `--at` timestamps are **always UTC**. The user almost always means their local time.

1. **Look up the user's timezone** — derive from system. On Windows, `[System.TimeZoneInfo]::Local.Id` or read the auto-memory `currentDate` block. **Never** guess.
2. **Convert to UTC** explicitly using PowerShell (cross-platform-safe):
   ```powershell
   [System.TimeZoneInfo]::ConvertTimeToUtc((Get-Date "9:00am"), [System.TimeZoneInfo]::Local)
   ```
3. **Echo back the conversion**: "9am America/Guatemala = 15:00 UTC, so the cron would be `0 15 * * 1-5`. Confirm?"
4. **Re-check current time before any `--at`** — long conversations drift. Run `date -u +%Y-%m-%dT%H:%M:%SZ` (or PowerShell equivalent) before computing the absolute timestamp. If the resolved time is in the past, ask for clarification — do not silently roll forward.

#### Constraints

- Minimum poll interval is 1 minute (the daemon polls once per `pollIntervalMs`, default 60000). Sub-minute schedules are rejected.
- Interval units: `s`, `m`, `h`, `d` ONLY. `--interval 1w` is rejected at load time.
- `--at` must be a valid ISO 8601 datetime in the future.
- Exactly one of `--cron`, `--interval`, `--at` per schedule.

### Step 4 — Confirm and create

Show the full plan to the user before creating:

```
Spell:    outlook-attachment-processor (alias: oap)
Cadence:  every weekday at 9am America/Guatemala (15:00 UTC)
Cron:     0 15 * * 1-5
Daemon:   running ✓
```

After user confirms, run:

```bash
npx flo spell schedule create -n <spell-name> --cron "<cron>" 2>&1
# or --interval <value>
# or --at <iso-datetime>
```

Capture the schedule ID from output and surface it to the user along with the next computed run time.

### Step 5 — Verify the wiring

Tail the actual execution history for this schedule so the user can confirm the daemon picked it up:

```bash
npx flo spell schedule executions --schedule <schedule-id> 2>&1
```

`executions` reads from the daemon-written `schedule-executions` namespace and shows started time, status (success/failed/running), duration, and whether the run was manual. This is the only command that proves a schedule actually fired — `flo spell schedule list` only shows the schedule definition.

If the user wants to wait for the first fire (interval ≤ 5m), poll `flo spell schedule executions --schedule <id>` or watch The Luminarium (the daemon's localhost UI). Otherwise, summarize and exit:

```
Scheduled: <schedule-id>
Next run:  <ISO datetime UTC> (<local-equivalent>)
Verify:    npx flo spell schedule executions --schedule <schedule-id>
Cancel:    npx flo spell schedule cancel <schedule-id>
```

## Sub-actions (when not creating)

If the user asks to **list** schedules:
```bash
npx flo spell schedule list 2>&1
```

If the user asks to **cancel** a schedule:
1. Run `flo spell schedule list` and let them pick.
2. `npx flo spell schedule cancel <schedule-id>`.
3. Confirm the entry is gone from the list.

If the user asks to **run now** without altering the cadence:
- Use the dashboard's "Run now" button if available, or the daemon's `runScheduleNow` API.
- The CLI does not currently expose this — surface that limitation if asked, and offer `flo spell cast -n <name>` as a manual alternative.

## Important — gotchas

- **Daemon prerequisite**: schedules only fire while the daemon is running. Tell the user this explicitly. OS autostart for reboot survival is now wired automatically — see Step 1.
- **Catch-up window** (default 1h, `scheduler.catchUpWindowMs` in `moflo.yaml`): if the daemon was offline when a run was due, runs within the window still fire on the next poll. Older missed runs are skipped with a `schedule:skipped` event.
- **maxConcurrent** (default 2): caps the number of scheduled spells running concurrently. Same-schedule overlap is never allowed.
- **No update CLI yet**: `flo spell schedule` exposes create/list/cancel only. To change a cadence, cancel + recreate.
- **Spell-required sandboxing**: when sandbox-required spells become enforced, scheduled runs will honor it just like manual casts — a missing sandbox skips the run with a `schedule:skipped` event.

## Output

End the session with a single-block summary:

```
Schedule Created
────────────────
Spell:       <name>
Cadence:     <human-readable>
Cron/At:     <UTC expression>
ID:          <schedule-id>
Next run:    <UTC + local>
Cancel:      npx flo spell schedule cancel <id>
Daemon:      running | needs-start
```

## Reference

- Full daemon scheduler docs: see `docs/SPELLS.md#scheduling` in the moflo source tree
