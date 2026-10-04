---
name: research-exp-live
description: "Use when launching, monitoring, resuming, or stopping a long-running research Experiment with structured run evidence and scheduled live checks."
---

# research-exp-live

## Purpose

Use this skill for a long-running command that belongs to an existing Package and Experiment. It
authorizes the Run through management state, stores producer evidence in one Run directory, and keeps
monitoring decisions tied to measured status.

This skill does not create or activate Package intent, or treat a browser page
as state. It follows User-First Reconcile-After: execute the current working
state, finalize Run Evidence, then offer an advisory reconciliation for the
user. A pending advisory does not authorize or block another Run.

## Storage and authority

Resolve the managed root once:

```bash
export RESEARCH_ROOT="${RESEARCH_ROOT:-.research}"
```

`--research-root` overrides the environment variable. If neither is set, the default is
`.research`.

With the default root, the three managed areas are `.research/state/`,
`.research/experiments/`, and `.research/interface/`.

| Data | Location | Authority |
| --- | --- | --- |
| Package, Experiment, Run, and allocation lifecycle | `$RESEARCH_ROOT/state/research.sqlite3` through bounded queries | Management authority |
| Current folded state | `$RESEARCH_ROOT/state/current.json` | Rebuildable state projection |
| Run command and frozen context | `$RESEARCH_ROOT/experiments/<package>/<experiment>/<run>/run.json` and `context.json` | Immutable Run envelope |
| Live status and raw evidence | The same Run directory | Producer-owned runtime evidence |
| Human pages | `$RESEARCH_ROOT/interface/` | Read-only generated projection |
| Interface server process metadata | `$XDG_RUNTIME_DIR/trustworthy-research/<workspace-hash>/` | Ephemeral local runtime |

When `XDG_RUNTIME_DIR` is unset, `ResearchPaths` uses its per-user temporary runtime fallback. Server
metadata never belongs in `$RESEARCH_ROOT/state/` or `$RESEARCH_ROOT/interface/`.

The interface can be absent, stale, or rebuilt while an Experiment is running. Interface health
never authorizes a launch and never proves completion.

## Preconditions

Before launch, confirm the hard ownership and authority boundaries:

- the selected Package, Direction, and Experiment exist and own one another;
- their selected versions are positive and can be frozen atomically;
- `USER_GUIDED` mode has an unconsumed `RUN_AUTHORIZATION` bound to the
  current ExperimentSpec and Direction versions; `AUTONOMOUS` mode uses
  Package activation authority;
- a requested GPU allocation is open and bound to the same Package and Experiment.

Package lifecycle, blockers, Experiment readiness, implementation review,
version drift, and missing `purpose`, `config_ref`, or numeric gate are
advisories. A gate-less Run is diagnostic and cannot support verified `PASS`.
The launcher reads state again before freezing the Run context; that frozen Run
and its finalized Evidence remain authoritative.

The launcher checks these conditions again under the management-state lock. Do not bypass a rejected
launch by writing a Run directory yourself.

## Launch

Use the canonical launcher:

```bash
python3 -m lib.experiments.launch \
  --workspace . \
  --research-root "$RESEARCH_ROOT" \
  --pkg <package-id> \
  --exp <experiment-id> \
  --tmux-session <name> \
  --heartbeat-timeout 600 \
  -- bash scripts/run_experiment.sh
```

The default transport is a named tmux session. Use `--foreground` for a short command. Useful optional
flags include:

- `--metrics-regex` for named metric groups;
- `--total-steps` for progress normalization;
- `--wandb-run-id` and `--tensorboard-logdir` for external telemetry identifiers;
- `--expected-duration minutes|hours|days` for scheduling;
- `--gpu-sample` for GPU observations;
- `--server` and `--alloc` for a resource binding;
- `--retry-of <run-id>` for a replacement attempt.

External telemetry adds observations. It does not replace the Run directory or management callbacks.

The launcher writes:

```text
$RESEARCH_ROOT/experiments/<package>/<experiment>/<run>/
├── run.json
├── context.json
├── status.json
├── events.jsonl
├── metrics.jsonl
├── result.json
└── log.txt
```

`run.json` binds the command, context hash, selected Experiment, resource, and transport.
`context.json` freezes the state snapshot used at authorization.

## Optional human interface

Start or reuse the read-only interface server only when a human view is useful:

```bash
python3 -m lib.interface.serve \
  --workspace . \
  --research-root "$RESEARCH_ROOT" \
  ensure --json
```

The server serves `$RESEARCH_ROOT/interface/` and exposes narrow read-only APIs over state and Run
evidence. Its `dashboard_server.json` and log live under the XDG runtime directory. A failed
`ensure` call is interface debt, not a Run failure.

## Startup health gate

Check the new Run within 120 seconds unless the command has a documented slow start. Read
`status.json`. Startup is confirmed only when:

- the lifecycle is still open or a terminal status is mechanically recorded;
- `first_output_at` is set;
- `health.state` is `OK` or `WARN`.

Do not report a healthy launch before these facts exist. If the process exits or
`health.state=ERROR`, inspect a bounded log tail:

```bash
python3 -m lib.experiments.report \
  --workspace . \
  --research-root "$RESEARCH_ROOT" \
  --run "$RESEARCH_ROOT/experiments/<package>/<experiment>/<run>" \
  --tail 50
```

Route the verified failure to repair, implementation review, a user decision, or a recorded blocker.

## Monitoring cadence

During the first 30 minutes, check startup and early throughput closely. After
that, choose each check interval from the best available scheduling evidence:

1. measured progress and stable throughput from `status.json`;
2. recent progress changes and output heartbeat;
3. `expected_duration` from `run.json`;
4. unknown duration.

| Remaining duration | Next check |
| --- | --- |
| up to 15 minutes | 2 to 5 minutes |
| up to 1 hour | about 10 minutes |
| up to 6 hours | 15 to 30 minutes |
| over 6 hours | 30 to 60 minutes |
| unknown | 10 minutes |

No open Run goes unchecked for more than 60 minutes. Check immediately when status becomes `STALE`,
health becomes `ERROR`, anomaly count increases, or throughput drops sharply.

At every check:

1. Read `status.json` for each management-open Run. Use `log.txt` only to diagnose a problem.
2. Record the live-check observation through a `research-op` command envelope.
3. Record `Next Check` and arm re-entry before that time.
4. Reconcile missing management callbacks.
5. Run the Package artifact scan once. Do not create a second polling loop.

The live-check observation is not a plan update. It must not rewrite the
working state, the frozen Run context, finalized Evidence, or a resource
allocation.

```bash
python3 -m lib.experiments.reconcile \
  --workspace . \
  --research-root "$RESEARCH_ROOT"

python3 skills/research-op/scripts/research_op.py \
  --workspace . \
  --research-root "$RESEARCH_ROOT" \
  --pkg <package-id> \
  --op update \
  --target tracker-live-check-row \
  --payload '{"run_id":"<run-id>","action":"CONTINUE_RUN","next_check":"<ISO-8601>"}'
```

The observation fields come from `status.json`: `status`, `last_output_at`, `progress`,
`latest_metrics`, `resource`, and health. The agent supplies the action and next-check time. Do not
edit state or interface files to record a check. The runtime that invoked the agent remains
responsible for re-entry; the recorded deadline makes a missed check visible in the Control Panel.
Use `--op scan-events --payload '{}'` when reconciliation finds a missing callback.

## Liveness and failure

Liveness comes from the child `pid`, `harvester_pid`, `last_output_at`, and `heartbeat_timeout`.
`status.json` can become `STALE` even when the command is quiet. Verify the process before deciding
whether to wait, stop, or replace it.

Canonical terminal statuses are:

- `COMPLETED`
- `FAILED`
- `HALTED`
- `SKIPPED`

Completion requires a terminal `status.json` with `exit_code` and `ended_at`, followed by a matching
management callback. If the callback is missing, run the reconciler. Elapsed time, an expired
estimate, or a quiet log is not completion evidence.

After terminal status:

1. read `result.json` and its EvidenceRefs;
2. compare measured results with the immutable Experiment gate;
3. record result and Experiment status through `research-op`;
4. release any open resource allocation only after terminal evidence is
   verified and the allocation still matches the Package and Experiment;
5. run reconciliation and artifact scan again;
6. offer an advisory reconciliation. The user owns any accepted plan update.

Do not infer `SUCCESS` from process exit or a metric. A current exact-result
`VERIFIER_VERDICT` must still match the ExperimentSpec, finalized Run event,
result hash, and numeric gate. The user separately decides the terminal Package
outcome.

## Open-run stop gate

Before ending a session, list management-open Runs:

```bash
python3 -m lib.experiments.report \
  --workspace . \
  --research-root "$RESEARCH_ROOT" \
  --open
```

Every listed Run needs a scheduled next check. If a Run is already terminal on disk but still appears
open, reconcile it before stopping. A healthy interface server does not clear this gate.
An advisory reconciliation may remain pending after the mechanical callback is
repaired; it does not clear or create a Run and does not block the next legal
execution.

## Worked example

```text
status=RUNNING health=OK progress=1200/50000 latest_metrics={"loss":0.41}
Decision: continue
Next Check: 5 minutes, based on current startup progress and output cadence
Management: live-check command accepted
Reconcile: no missing callback
Artifact scan: no new event
```

Failure:

```text
status=FAILED health=ERROR exit_code=1 first_output_at=set
Decision: startup health refused
Evidence: bounded report tail shows ImportError
Route: FIX_IMPLEMENTATION
Replacement: launch with --retry-of <run-id> and resume adaptive monitoring
```

## References

- [status contract](references/status-contract.md)
- [telemetry sources](references/telemetry-sources.md)
- [live page contract](references/live-page-contract.md)
