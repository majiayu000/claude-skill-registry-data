---
name: pi-automation
description: Design safe, observable scheduled and event-triggered Pi automation workflows. Use when the task concerns pi automation.
---
# Pi automation

1. Choose one trigger: systemd user timer, systemd path unit, CI webhook, or
   `agents-cron` (optional). Avoid stacking schedulers for the same job.
2. Specify project cwd, input, output artifact, max runtime, budget, and retry policy.
3. Use a read-only isolated invocation by default. `pi --print` can run headlessly;
   model tool availability/permissions must be deliberately restricted.
4. Validate arguments/paths. Persist run id, exit code, stdout/stderr redacted,
   timestamps, and a bounded report. Ensure repeated jobs are idempotent.
5. Do not grant unattended write/network-mutation capabilities by default.
6. Prefer `systemctl --user` timers on Arch Linux; `agents-cron` is an optional
   Pi-native scheduler requiring an external cron trigger.
7. Never paste provider secrets or environment contents into prompts or logs.

See `~/.pi/agent/examples/systemd/` for an opt-in sample user timer. It is disabled
until the operator installs/enables it.
