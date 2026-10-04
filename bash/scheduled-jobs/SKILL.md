---
name: scheduled-jobs
description: >
  Conventions for authoring, installing, and instrumenting scheduled work on managed hosts.
  Use when adding a new cron job, recurring task, systemd timer, launchd agent, scheduled script,
  nightly job, timer unit, OnCalendar schedule, or when touching any existing scheduled job.
  Triggers: new cron job, recurring task, systemd timer, launchd agent, scheduled script,
  nightly job, "run this every", timer unit, OnCalendar, schedule a job.
allowed-tools: Read, Glob, Grep, Bash
---

# Scheduled Jobs

> **North star.** One place answers "who owns this unit", "did it run", and "is it installed
> safely". Keep the deployment inventory in the repository that owns the scheduled work; this
> skill carries the portable conventions that inventory enforces.

## Directory-and-manifest model (`packages/cron`)

Each repo that owns schedules keeps them in one directory with a manifest listing every job.
A node project can adopt this literally as a workspace package; a system-hosted job adopts the
same shape as unit files plus a manifest.

```
packages/cron/          # or scripts/install/<job>-timer/ for standalone units
  manifest.json         # job name, schedule, command, timeout, owner
  <job>.timer           # systemd unit (Linux)
  <job>.service         # paired service unit
```

The manifest is the human-readable index; the unit files are what systemd loads. Both stay in
the owning repo and deploy as **regular files** — never symlinks into a live git checkout.

## Naming: `<owner>-<job>`

| Good | Bad | Why |
| --- | --- | --- |
| `mesh-heartbeat` | `heartbeat` | Owner prefix makes namespace ownership recoverable |
| `search-sweep` | `sweep` | A service or repository prefix identifies the owner |
| `docs-ratchet` | `ratchet` | A descriptive owner prefix makes the unit portable |

When modifying any existing job whose name lacks a prefix, rename it as part of that change —
do not defer to a separate cleanup wave.

## Install kind: regular files only

**Never** install a timer as a symlink from a live checkout into
`~/.config/systemd/user/<unit>.timer`.

A symlinked unit points into a live git checkout. Any checkout, rebase, or branch switch can
momentarily unlink the target; systemd logs `Unit to trigger vanished`, fails the timer, and
**does not recover** reliably after `daemon-reload` or reboot.

Correct pattern: copy or `install -m 644` the unit into `~/.config/systemd/user/`, then
`systemctl --user daemon-reload && systemctl --user enable --now <unit>.timer`.

Record any known symlinked units in the owning repository's remediation backlog.

## Run record (guideline, not a gate)

Every run — scheduled or manual — appends one structured record. Minimum fields:

| Field | Meaning |
| --- | --- |
| `ts_start` | ISO-8601 start timestamp |
| `ts_end` | ISO-8601 end timestamp |
| `job` | Job name (`<owner>-<job>`) |
| `trigger` | `cron`, `manual`, or `systemd` |
| `host` | Hostname |
| `exit` | Exit code |
| `duration_s` | Wall seconds |
| `timed_out` | Boolean |

Reach for a structured-logging library that produces pino-shaped output where one exists for
the job's language. Where no library fits, emit the fields by any means (JSONL append, shell
heredoc) — the shape matters, not the library.

Manual runs MUST use the same entry point as scheduled runs. A job that bypasses the recorder
is invisible to every downstream health check.

## Mechanism stance

| Mechanism | Status |
| --- | --- |
| systemd user timers | **Standard** on Linux hosts |
| launchd | Documented macOS twin |
| cron / anacron / at | Environment-dependent; document daemon availability before use |
| GitHub Actions / Vercel crons | Document separately; out of scope for unit-file conventions |

## On-contact remediation

When you touch **any** existing scheduled job for any reason, bring that job to convention in
the same change:

1. Rename to `<owner>-<job>` if unprefixed
2. Convert symlink installs to regular-file copies
3. Wire run-record emission if missing

Do not open a separate cleanup wave for the touched job. Track unrelated units in the owning
repository's normal remediation backlog.

## Verify

```bash
# install kind for a unit
f=~/.config/systemd/user/<owner>-<job>.timer
[ -L "$f" ] && echo "FAIL: symlink" || echo "OK: regular file"

# last run record (shepherd jobs-run shape)
tail -1 ~/.local/state/shepherd/jobs/runs.jsonl | jq .
```
