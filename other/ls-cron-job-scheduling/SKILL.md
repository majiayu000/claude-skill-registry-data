---
name: ls-cron-job-scheduling
description: "Use when managing cron from a repo-local manifest: time triggers, on-boot-with-delay, sequenced tasks; create, remove, reorder, install."
metadata:
  version: "1.2"
compatibility: "Linux cron; Python 3.12+ and PyYAML (framework). Manifest at cron/manifest.yaml."
---

# Cron orchestrator

Define triggers and tasks in a single YAML manifest. One trigger (for example, `midnight-utc`) runs multiple tasks in sequence; on-boot triggers can delay before execution. Tooling creates, removes, reorders, enables, disables, validates, and installs generated crontab fragments.

## Rule ownership

This skill owns cron manifest and scheduling behavior. Public harness docs may reference cron, but cron validation, argv command handling, install fragments, and sequencing rules live here.

- Prefer argv-list commands; string commands are parsed conservatively and shell operators are rejected.
- Validate manifests before installing crontab fragments.
- Coordinate with `ls-codex-heartbeat-checks` for heartbeat-specific scheduling instead of duplicating heartbeat activation rules here.

## Manifest (cron/manifest.yaml)

```yaml
triggers:
  midnight-utc:
    schedule: "0 0 * * *"
  after-boot:
    on_boot_delay_minutes: 5
tasks:
  - id: snapshot-daily
    trigger: midnight-utc
    sequence_order: 1
    command:
      - python3
      - ls/skills/ls-system-baseline-diagnostics/scripts/system_snapshot.py
      - --output-basename
      - reports/system-snapshots/daily
    enabled: true
    timeout_seconds: 3600
```

- **Triggers:** use either `schedule` with five numeric Linux cron fields (lists, ranges, and steps) or `on_boot_delay_minutes` from 0 to 1440.
- **Tasks:** require `id`, `trigger`, `sequence_order` (integer 0 to 86400), `command`, and optional `enabled` plus `timeout_seconds`.
- **Commands:** prefer an argv list. String commands are split with `shlex` and reject shell operators such as `&&`, `|`, redirects, backticks, and command substitution. Shell expansion is not performed.

## Commands (from repo root)

Use `python3 ls/skills/ls-cron-job-scheduling/scripts/cron_ctl.py --manifest cron/manifest.yaml <command>`.

| Command | Purpose |
|---------|---------|
| `validate` | Check manifest schema, trigger refs, command shape, timeouts, and schedules |
| `readiness` [--repo-root PATH] [--trigger NAME] [--log-dir PATH] | Print a read-only pre-activation report with ready, blocked, and unchecked checks plus next actions |
| `list` [--trigger NAME] | List tasks (optionally for one trigger) |
| `add-task --trigger NAME --command "..."` [--sequence-order N] [--id ID] | Add task |
| `remove-task --id ID` or `--trigger NAME` | Remove by id or all for trigger |
| `reorder --trigger NAME --order id1,id2,id3` | Set run order for that trigger |
| `enable --id ID` / `disable --id ID` | Toggle task |
| `install` [--repo-root PATH] [--output PATH] [--log-dir PATH] [--trigger NAME] | Generate a reviewable **user-crontab fragment**; it never modifies a live crontab. `--trigger` limits output to one existing trigger. `--output` writes the fragment, otherwise it prints to standard output. |

Generated runner commands use the absolute Python executable that generated the
fragment, preserving its installed dependencies instead of resolving `python3`
from cron's PATH. Regenerate the fragment when relocating that installation.
The harness's cron-control helpers and generated runner use `-I -B`: imports
ignore ambient Python paths and no bytecode is written into a sealed runtime.
The scripts load their own sibling manifest helper explicitly. Manifest task
commands retain their configured arguments and environment behavior.

Run `python3 ls/skills/ls-cron-job-scheduling/scripts/cron_ctl.py --manifest cron/manifest.yaml readiness --repo-root .` before enabling or preparing a schedule. The report checks the manifest, trigger definitions, runner, current command paths, working-directory access, and an optional log directory without creating or changing files. A blocked item includes the next action. The overall result stays `unchecked` when the target cron account or service, workload-specific settings and permissions, credentials, or recovery arrangements cannot be observed safely. Run it as the account that will own the crontab; current PATH and permission checks cannot prove a different cron account has the same access.

Readiness never runs task commands, changes each task's `enabled` value, installs a crontab, or infers success from run history. Activation state and past outcomes remain separate. If a task needs durable logs, include `--log-dir PATH` to check the existing or creatable path; readiness does not create it.

Runner (used by cron): `python3 ls/skills/ls-cron-job-scheduling/scripts/run_trigger.py --manifest PATH --repo-root PATH TRIGGER` runs that trigger's tasks in sequence with `subprocess.Popen(..., shell=False)`, relaying output while retaining bounded byte tails for logs.
Add `--log-dir PATH` when cron output may otherwise disappear; the runner appends
timestamped start, task exit, stdout tail, and stderr tail records to
`PATH/<trigger>.log`.
Because stdout/stderr tails can include sensitive data, use a protected log
directory with restricted permissions.

See `references/manifest.md` for the accepted manifest schema and security model.

## Patterns for agents

1. **Add a daily snapshot at midnight:** `add-task --trigger midnight-utc --command "python3 ls/skills/ls-system-baseline-diagnostics/scripts/system_snapshot.py --output-basename reports/system-snapshots/daily"`.
2. **Add on-boot trigger:** In manifest, add trigger with `on_boot_delay_minutes: 5`; then add tasks to it.
3. **Reorder:** `reorder --trigger midnight-utc --order snapshot-daily,cleanup,notify`.
4. **Remove one task:** `remove-task --id snapshot-daily`. Remove all for a trigger: `remove-task --trigger midnight-utc`.
5. **Prepare a fragment:** Run `install --output cron/crontab.generated`, inspect the generated user-crontab fragment, then merge it manually with the existing user crontab only after an explicit operational decision. Do not write `/etc/cron.d` or replace an existing crontab from this skill.
