---
name: speckit-autopilot-schedule
description: Schedule /speckit-autopilot-run to run unattended on a recurring launchd
  timer (default every 2 hours, configurable) so the backlog drains itself. Also unschedule,
  check status, or fire one pass now. macOS only. Opt-in — nothing recurring is installed
  until you run this.
compatibility: Requires spec-kit project structure with .specify/ directory
metadata:
  author: github-spec-kit
  source: autopilot:commands/speckit.autopilot.schedule.md
---

# Autopilot Scheduler

Put `/speckit-autopilot-run` on a **recurring launchd timer** so open issues get
worked without a human starting each pass. This is strictly **opt-in**: nothing is
scheduled until you run this command, and it only ever schedules *this* repo.

`$ARGUMENTS` may contain a subcommand and options:

- `install` *(default if you just say "schedule autopilot")* — schedule it.
  - `--interval-hours N` — cadence in hours (**default 2**, configurable to any
    positive integer).
- `uninstall` — stop the recurring runs and remove the agent.
- `status` — is it scheduled? show the interval, plist, and the tail of the log.
- `run-now` — trigger a single pass immediately (only if already scheduled).

All of these are thin wrappers over the script — run it, don't reimplement launchd
by hand:

```bash
BIN="$CLAUDE_PROJECT_DIR/.specify/extensions/autopilot/scripts/bash/autopilot-schedule.sh"
```

(If `$CLAUDE_PROJECT_DIR` isn't set, resolve the repo root with
`git rev-parse --show-toplevel` and use `<root>/.specify/extensions/autopilot/scripts/bash/autopilot-schedule.sh`.)

## What to do

1. **Parse `$ARGUMENTS`** into a subcommand (default `install`) and, for install, an
   `--interval-hours` value if the user named one ("every 3 hours" → `3`). If they
   gave no number, use the script's default of 2.

2. **Run the script** for this repo, passing the project explicitly so it works from
   a worktree too:

   ```bash
   # schedule every 2h (default)
   "$BIN" install --project "$CLAUDE_PROJECT_DIR"

   # schedule every N hours
   "$BIN" install --interval-hours N --project "$CLAUDE_PROJECT_DIR"

   # check / stop / run once
   "$BIN" status    --project "$CLAUDE_PROJECT_DIR"
   "$BIN" uninstall --project "$CLAUDE_PROJECT_DIR"
   "$BIN" run-now   --project "$CLAUDE_PROJECT_DIR"
   ```

3. **Report back** what the script printed — the label, cadence, plist path, and log
   path — and tell the user how to change or stop it (re-run `install
   --interval-hours N` to re-cadence; `uninstall` to stop). On `install`, remind
   them the first pass fires after the interval (RunAtLoad is off, so it won't
   surprise-run the moment it's scheduled); `run-now` triggers one immediately.

## How it runs (so you can explain it)

- A per-repo launchd agent (`~/Library/LaunchAgents/com.speckit.autopilot.<repo>.plist`)
  fires every `StartInterval` seconds and runs `autopilot-run.sh <repo>`, which
  invokes `claude -p "/speckit-autopilot-run" --dangerously-skip-permissions` inside
  the repo. The permission bypass is what makes an *unattended* pass possible — the
  session can use git/gh/file tools without a human clicking approve. Flag that to the
  user when they schedule, so it's a conscious choice.
- Runs are **single-flight**: if a pass outlasts the interval, the next tick is
  skipped rather than stacking two autopilots on the same repo.
- Output goes to `~/Library/Logs/speckit-autopilot/<repo>.log` (`status` tails it).

## Stop conditions

- **Not macOS** — launchd is macOS-only; the script exits with a clear message. On
  Linux, a `systemd --user` timer or cron would be the equivalent (not built here).
- **Not a git repo** — the script needs a repo root to label the agent; it refuses
  outside one.