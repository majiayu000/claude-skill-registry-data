---
name: schedule
description: Use when the user asks to schedule, list, inspect, update, disable, or remove recurring Pi/agent jobs using local system timers. Covers systemd user timers, safe wrapper scripts, logs, lockfiles, and running `pi -p` unattended. Trigger on /schedule, schedule this, recurring task, daily/weekly/monthly agent job, timer, cron, or background Pi task.
---

# Schedule

You help create and manage local scheduled Pi jobs safely.

## Default scheduler on this machine

Prefer **systemd user timers** on Linux when `systemctl --user` is available. They are inspectable, robust, and already available on Fedora. Use cron only when `crontab` exists and the user asks for cron specifically.

Before installing or changing a job, verify availability:

```bash
systemctl --user is-system-running
command -v pi
```

Note: if `loginctl show-user "$USER" -p Linger --value` returns `no`, user timers generally run while the user session/user manager is active. Ask before enabling linger because it changes login/session behavior.

## Safety rules

- Do not install, overwrite, enable, disable, or delete a timer without showing the exact files/commands and getting explicit confirmation.
- Prefer a reviewed wrapper script over embedding a long `pi` prompt directly in a unit file.
- Use absolute paths for executables, working directories, logs, lockfiles, and prompt files.
- Use `pi -p` for non-interactive scheduled runs.
- Add a lock so runs do not overlap.
- Log stdout/stderr to a predictable directory.
- Use a stable job id: lowercase letters, numbers, hyphens only.
- Avoid destructive tasks unless the user explicitly confirms the scheduled prompt/script.

## File layout

Use this layout unless the user asks otherwise:

```text
~/.local/bin/pi-schedule-<job-id>
~/.config/pi-scheduler/<job-id>.prompt.md
~/.local/state/pi-scheduler/<job-id>.log
~/.local/state/pi-scheduler/<job-id>.lock
~/.config/systemd/user/pi-schedule-<job-id>.service
~/.config/systemd/user/pi-schedule-<job-id>.timer
```

## Create a job

1. Clarify:
   - job id/name
   - working directory
   - schedule, preferably a systemd `OnCalendar=` expression
   - exact task prompt
   - whether it may edit files or should be read-only
2. Draft the prompt file and wrapper script.
3. Draft the `.service` and `.timer` files.
4. Show the full plan and ask for confirmation.
5. Only after confirmation, write files and run:

```bash
systemctl --user daemon-reload
systemctl --user enable --now pi-schedule-<job-id>.timer
systemctl --user list-timers 'pi-schedule-*' --all
```

## Wrapper script template

```bash
#!/usr/bin/env bash
set -euo pipefail

JOB_ID="<job-id>"
WORKDIR="<absolute-project-dir>"
PROMPT_FILE="$HOME/.config/pi-scheduler/${JOB_ID}.prompt.md"
LOG_FILE="$HOME/.local/state/pi-scheduler/${JOB_ID}.log"
LOCK_FILE="$HOME/.local/state/pi-scheduler/${JOB_ID}.lock"
PI_BIN="<absolute-path-to-pi>"

mkdir -p "$(dirname "$LOG_FILE")"

{
  echo "===== $(date --iso-8601=seconds) ${JOB_ID} start ====="
  flock -n 9 || { echo "Another run is already active"; exit 0; }
  cd "$WORKDIR"
  "$PI_BIN" -p "$(cat "$PROMPT_FILE")"
  echo "===== $(date --iso-8601=seconds) ${JOB_ID} done ====="
} 9>"$LOCK_FILE" >>"$LOG_FILE" 2>&1
```

## systemd unit templates

Service:

```ini
[Unit]
Description=Scheduled Pi job: <job-id>

[Service]
Type=oneshot
ExecStart=%h/.local/bin/pi-schedule-<job-id>
```

Timer:

```ini
[Unit]
Description=Timer for scheduled Pi job: <job-id>

[Timer]
OnCalendar=<schedule>
Persistent=true
Unit=pi-schedule-<job-id>.service

[Install]
WantedBy=timers.target
```

## Inspect jobs

Use:

```bash
systemctl --user list-timers 'pi-schedule-*' --all
systemctl --user status pi-schedule-<job-id>.timer --no-pager
systemctl --user status pi-schedule-<job-id>.service --no-pager
journalctl --user -u pi-schedule-<job-id>.service --no-pager -n 100
```

Also read the job log:

```bash
tail -n 200 ~/.local/state/pi-scheduler/<job-id>.log
```

## Disable or remove a job

Show the exact commands and ask for confirmation first.

Disable but keep files:

```bash
systemctl --user disable --now pi-schedule-<job-id>.timer
```

Remove files:

```bash
systemctl --user disable --now pi-schedule-<job-id>.timer || true
rm -f ~/.config/systemd/user/pi-schedule-<job-id>.service
rm -f ~/.config/systemd/user/pi-schedule-<job-id>.timer
rm -f ~/.local/bin/pi-schedule-<job-id>
rm -f ~/.config/pi-scheduler/<job-id>.prompt.md
systemctl --user daemon-reload
```
