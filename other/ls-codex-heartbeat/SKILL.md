---
name: ls-codex-heartbeat
description: "Opt-in agent heartbeat harness for target repositories: initialize config, run transaction-safe checks, preserve artifacts, and wire cron only after explicit activation."
metadata:
  version: "1.0"
compatibility: "Python 3.12+, PyYAML, LocalSetup.4 harness CLI."
---

# Agent Heartbeat

Use this skill when a repository needs an explicit, auditable heartbeat harness for periodic checks run by a configured agent CLI. The runtime is client-neutral: each profile supplies its own executable argv, prompt transport, and launcher mode.

## Guardrails

- Installing this skill only makes the harness available. It does not create config, cron entries, or autonomous runs.
- Activate per target repo with `localsetup harness codex-heartbeat init` and `enable`.
- Ordinary transaction artifacts stay under the configured ignored target heartbeat
  state directory (default `.localsetup/state/codex-heartbeat/`). Reserved actions
  retain separate private attempt/accounting evidence as described in
  [artifacts](references/artifacts.md).
- `enable --install-crontab` refuses to install a live crontab unless `--yes` is also passed.
- Ordinary `run --no-agent` skips agent profile loading and launcher resolution entirely,
  then exercises configured hooks, lock acquisition, recovery, command logging,
  staged validation, and atomic promotion. Broken or missing agent configuration
  does not prevent this transaction check; normal agent runs still validate it.
  With reserved-action controller options, `--no-agent` instead returns an early
  skip before configuration, locks, hooks or transaction checks. See
  [reserved runs](references/config.md#running-a-reserved-action).
- An ordinary run acquires `heartbeat.lock` before inspecting or changing active and staged state. It reclaims only a same-host lock whose owner PID is absent and whose age meets `heartbeat.stale_after_seconds`, then unlinks that held stale pathname and retries exclusive acquisition. Ambiguous locks remain locked for manual review.
- Direct hooks reject `git commit`, `git push`, and blocked destructive executables unless their specific policy switches are enabled; Git global options are parsed before the subcommand check.
- Every executed or policy-blocked ordinary-run command receives a sidecar.
  Promotion validates hashes for the result, command log, and every logged
  sidecar. Reserved execution uses the same overlap lock but its own
  [protected result evidence](references/process-control.md#reserved-execution-owner).
- Agent profiles record execution; they are not a sandbox replacement.

## Rule ownership

This skill owns heartbeat harness behavior. `HARNESS_AUTOMATION.md` is the public reference for the same guardrails; changes to activation, artifacts, transaction handling, or cron wiring belong here first.

- Heartbeat is opt-in per target repo.
- New cron cadence must be faithfully representable: integer minute divisors of
  60, or whole-hour divisors of 24. Enabling rejects other intervals before
  changing configuration. Disabling preserves an existing trigger schedule.
  See the timezone and wall-clock limits in [configuration](references/config.md).
- Cron activation is delegated to explicit harness commands and should be coordinated with `ls-cron-orchestrator` when broader scheduling is involved.
- Runtime evidence stays in ignored target state, not public framework docs.

## Activation and evidence workflow

Use `ls-framework-compliance` for repository checks and `ls-cron-orchestrator`
for scheduling coordination. Preserve the explicit activation gates throughout
this lifecycle:

1. Inspect the target paths, configuration, cron manifest, and launcher with `plan`.
2. Use `init` to create `HEARTBEAT.md` and configuration with heartbeat disabled.
3. Use `enable` to update the heartbeat configuration and cron manifest while
   preserving unrelated tasks; retain the live-crontab confirmation gate above.
4. Validate a run with `--no-agent` when appropriate. Success requires validated
   staged artifacts and atomic promotion, as defined in `references/transactions.md`.
5. Inspect configuration, cron, lock, latest pointer, and run evidence with `status`.
6. Use `disable` to stop future heartbeat runs without deleting historical artifacts.

Record activation, validation, and artifact locations in the run ledger.

## Commands

```bash
localsetup harness codex-heartbeat plan
localsetup harness codex-heartbeat init
localsetup harness codex-heartbeat enable
localsetup harness codex-heartbeat status
localsetup harness codex-heartbeat budget
localsetup harness codex-heartbeat run --no-agent
localsetup harness codex-heartbeat disable
```

`budget` is read-only. It reports policy, summary, and task reservations from `heartbeat.task_queue_path` when configured; it does not spawn agents or enforce scheduling.

Standalone runtime script:

```bash
python3 ls/skills/ls-codex-heartbeat/scripts/codex_heartbeat.py --target-root . --no-agent
```

## References

- `references/config.md`
- `references/artifacts.md`
- `references/recovery.md`
- `references/command-logging.md`
- `references/process-control.md`
- `references/transactions.md`

## LSCli coding runs

The unselected `lscli-heartbeat` template profile uses an owned protected
registration, explicit provider configuration and task grant, stdin prompt, and
validated JSONL completion. Configure its absolute paths and bounded limits
using [the typed profile contract](references/config.md#typed-lscli-profile)
before selecting it. Planning and `--no-agent` do not call a provider.
Activation, credentials, delegated sandbox capability, and recurring authority
remain explicit. Generic client profiles retain their existing launcher modes.

## Controller accounting

Use [controller accounting commands](references/config.md#controller-accounting-commands)
for reviewed private policy initialization, resource inspection, and result-bound
progress dispositions. These commands neither run an agent nor close an external
issue. Keep accounting and controller inputs outside the writable workspace.
Use [explicit reserved actions](references/config.md#running-a-reserved-action)
for task-wide enforcement and compound compaction. Ordinary fresh profiles do
not acquire that authority from an accounting file's existence.
