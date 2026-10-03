---
name: ls-kilo-boss-orchestrator
description: Orchestrate Kilo headless boss-worker execution with repo-local state, watchdog leases, consensus validation, and safety gates. Use when running multi-agent autonomous loops that require planning, delegation, verifier checks, and high/critical discrepancy adjudication.
metadata:
  version: "1.0"
compatibility: Python 3.12+, Kilo CLI 7.x, PyYAML via the LocalSetup dependency helper
---

# Kilo Boss Orchestrator

Purpose: run a durable boss-worker gentle loop for headless Kilo execution with explicit state, safety controls, and consensus validation.

## When to use

Use this skill when you need:

- Boss-led planning and worker delegation in headless Kilo mode.
- Persistent repo-local task state and lease-based stuck-job recovery.
- Required verifier pass for substantive execution.
- Frontier-tier tiebreaker routing for high/critical disagreements.
- Cron-driven orchestration ticks and watchdog checks.

## Core loop

1. Boss dequeues pending tasks.
2. Boss dispatches primary + verifier worker cards with a required shared `session_id`.
3. Workers run Kilo headless commands, preserve session identity, and write results.
4. Boss evaluates consensus.
5. If discrepancy severity >= High, route to tiebreaker.
6. Boss records verdict and advances queue state.

## Safety model

- Destructive/high-impact actions are gate-controlled and require approval.
- Guarded execution applies safe operations and skips destructive operations.
- Worker task commands must be structured `command_argv` lists beginning with `kilo run`; shell command strings are rejected.
- Finalization requires `gate_passed: true` and `requires_tiebreaker: false`.
- Watchdog checks enforce lease TTL by reclaiming expired locks and requeueing or deadlettering tasks.
- All results and errors are redacted for sensitive material before persistence.
- Mutable state is repo-local under `.kilo/state/orchestrator/`.

## State paths

- `.kilo/state/orchestrator/queue.jsonl`
- `.kilo/state/orchestrator/tasks/`
- `.kilo/state/orchestrator/results/`
- `.kilo/state/orchestrator/leases/`
- `.kilo/state/orchestrator/heartbeats/`
- `.kilo/state/orchestrator/sessions/`
- `.kilo/state/orchestrator/consensus/`
- `.kilo/state/orchestrator/deadletter.jsonl`
- `.kilo/state/orchestrator/events.log`

## Scripts

- `scripts/kilo_headless_runner.py`: execute a single worker card through `kilo run`.
- `scripts/boss_ctl.py`: queue, dispatch, status, consensus, watchdog, and completion flows.
- `scripts/kilo_retry_watchdog.py`: deterministic phase-1 recovery helper that detects failure markers, sends fixed resume prompts to tmux on 15s cadence (configurable), and emits Hermes outbox JSON on retry exhaustion.

### Phase-1.1 deterministic retry behavior

Use when orchestration has transient failure and no AI fallback/backstop is available:

1. detect failure markers from local orchestrator logs,
2. run deterministic recovery strategies in order (prompt nudge -> interrupt+prompt -> restart in-session -> recreate session+launch),
3. classify health edge cases (session missing, Kilo inactive, pane freeze/unresponsive),
4. enforce phase-1.1 single-instance lock guard to avoid concurrent watchdog races,
5. wait startup grace windows and re-probe health between strategies,
6. retry every N seconds for a fixed retry budget,
7. if still not recovered, emit structured Hermes notification payload with telemetry bundle (host/session/service/path/log metadata + tails).

This script is intentionally offline-capable and non-AI.

## Commands

```bash
python3 scripts/boss_ctl.py init
python3 scripts/boss_ctl.py enqueue --task-file references/examples/task.sample.yaml
python3 scripts/boss_ctl.py dispatch --max-dispatch 2
python3 scripts/boss_ctl.py status
python3 scripts/boss_ctl.py watchdog
python3 scripts/boss_ctl.py consensus --task-id <task-id>
python3 scripts/boss_ctl.py finalize --task-id <task-id>
```

## Cron integration

Recommended trigger strategy:

- every minute: boss dispatch tick
- every minute: watchdog lease recovery tick
- every 5 minutes: heartbeat and queue health summary

Use `ls-cron-orchestrator` with a user-created manifest, commonly `cron/manifest.yaml` in the target repo.

## Consensus policy integration

- Primary + verifier always for substantive tasks.
- Tiebreaker mandatory for High/Critical discrepancies.
- Write validation record for each adjudicated task.

## References

- `references/kilo-boss-orchestrator-runbook.md`
- `references/kilo-boss-state-schema.md`
- `references/kilo-headless-boss-worker-gentle-loop-architecture.md`
- `references/examples/task.sample.yaml`
