---
name: cron-timers
description: "Use when scheduling a recurring task on a machine. Choosing crontab, a systemd timer or launchd, OnCalendar and Persistent, flock against overlaps, logging, env in files instead of the schedule, and how to list and verify schedules."
version: 1.0.0
author: iCLONE / CLONE FRAME
license: MIT
platforms: [macos, linux]
metadata:
  hermes:
    tags: [iclone-os, cron, systemd, timers, launchd, scheduling]
    related_skills: [watchdog-keepalive, backups-restore, server-agent-service, consent]
---

# Cron and timers — recurring work that runs once, on time, with logs

## When to use
- The owner wants something to run on a schedule: a backup, a report, a token refresh, a health check.
- A scheduled job ran twice, never ran, or ran without its environment.

`crontab`, `systemctl`, `systemd-analyze`, `flock` and `launchctl` are system tools: their man pages are the truth.

## Prerequisites
- A script with absolute paths that works when run by hand as the user that will run it.
- Any new or changed schedule is a scheduled task: ask through the consent door (`~/.iclone-os/bin/acp consent request scheduledTasks --reason "…"`), state what runs, as which user and how often, and wait for the owner's yes.

## Quick reference
| Machine | Use | Why |
|---|---|---|
| Linux server | systemd timer | logs in journald, `Persistent=true` catches missed runs, sandboxing |
| Linux, simple user job | crontab | one line, no root |
| macOS | launchd `StartCalendarInterval` | cron on macOS lacks permissions and misses runs while asleep |

Pick the slowest interval that does the job; every-minute jobs are almost never needed.

## Procedure
1. systemd timer (Linux). The service runs the script once, guarded by `flock` so two runs never overlap:
```ini
# example: /etc/systemd/system/<job>.service
[Service]
Type=oneshot
User=<user>
ExecStart=/usr/bin/flock -n /run/lock/<job>.lock <script>
```
```ini
# example: /etc/systemd/system/<job>.timer
[Timer]
OnCalendar=*-*-* 03:30:00
RandomizedDelaySec=300
Persistent=true
[Install]
WantedBy=timers.target
```
2. Check the calendar expression, then enable:
```sh
systemd-analyze calendar '*-*-* 03:30:00'  # example
sudo systemctl daemon-reload && sudo systemctl enable --now <job>.timer  # example
```
3. crontab (Linux user job; macOS has no `flock`, use launchd in step 5). Save the current table first, append, install from the file. The line logs the job's exit code so a run can be proven, not guessed:
```sh
crontab -l > <crontab-file> 2>/dev/null; echo '30 3 * * * /usr/bin/flock -n /tmp/<job>.lock <script> >> <log-file> 2>&1; echo "exit=$? $(date -u +\%FT\%TZ)" >> <log-file>' >> <crontab-file> && crontab <crontab-file>  # example
```
4. Environment: cron and timers start with an almost empty `PATH` and no shell profile. Use absolute paths and load secrets inside the script from a 0600 file:
```sh
set -a; . /etc/<job>/<job>.env; set +a  # example
```
5. launchd (macOS): `~/Library/LaunchAgents/<label>.plist` with `ProgramArguments`, `StartCalendarInterval` (`Hour` 3, `Minute` 30), `StandardOutPath` and `StandardErrorPath`, then:
```sh
plutil -lint ~/Library/LaunchAgents/<label>.plist && launchctl bootstrap gui/$(id -u) ~/Library/LaunchAgents/<label>.plist  # example
```
6. Logs:
```sh
journalctl -u <job>.service -n 50 --no-pager  # example
```

## Pitfalls
- `%` is special in crontab lines: write `date +\%F`, or move the command into the script.
- Cron uses the system time zone; a systemd `OnCalendar` can name one (`*-*-* 03:30:00 UTC`) — say which in the job.
- A machine that was off at 03:30 skips the cron run; `Persistent=true` runs a missed timer at boot.
- Two hosts with the same job (old server still on) do the work twice; list schedules on both.

## Never
- Never `crontab -r` (deletes the whole table) and never overwrite a crontab without saving it first.
- Never put tokens or passwords inside a crontab line or a unit's `ExecStart`.
- Never schedule anything the owner did not approve, and never a job that spends without its own limit.

## Verification
```sh
systemctl list-timers <job>.timer --no-pager; crontab -l | grep -F '<script>'  # example
launchctl print gui/$(id -u)/<label> | grep -E 'state =|last exit code'  # example
```
```sh
tail -n 1 <log-file>  # example
```
Pass = the timer shows a NEXT time and LAST result success (`systemctl show -p Result <job>.service` = `success`), or the crontab line is present and, after the first run, the last line of `<log-file>` is `exit=0 <UTC time>` — any other exit is a failure: read the log lines above the marker for the cause (`exit=1` with no output = the lock was held; util-linux `flock` reports a missing `<script>` as `exit=69`, a shell reports a missing command as `127` — read the message, do not map codes blindly), or (macOS) `launchctl print` finds the label and shows `last exit code = 0` after the first run.
