---
name: research-run
description: "Use when the user invokes /research-run or asks to execute, continue, monitor, verify, or finish an existing research package."
allowed-tools: Bash(python3 *), Bash(node *), Read, Edit, Write, Grep, Glob, Agent
---

# research-run

## Purpose

`/research-run` executes an existing Package one Experiment at a time. Under
User-First Reconcile-After, workflow gaps become advisories; launch freezes the
selected working revision before execution.

Continue until an evidence-backed terminal result, a named decision, or a
concrete external blocker with a next action. Never invoke git.

## Authority boundary

Management state lives in `.research/state/research.sqlite3`; Run measurements
live under `.research/experiments/`. JSONL and interface files are exports.
`research-run` does not read them; a missing interface does not block execution.

`research-run` may:

- query the selected Package, Experiment, open Runs, Decisions, Rules, and evidence;
- dispatch implementation, review, launch, monitoring, and verification work;
- launch or inspect a Run through `lib.experiments`;
- emit commands for `research-op`;
- reconcile experiment callbacks with `research-op --op scan-events`.

It may not:

- commit Project, Direction, or Experiment intent on the user's behalf;
- materialize a Package;
- append management events directly;
- treat generated HTML or JavaScript as state;
- copy a measured value into an Experiment gate.

Admission and dispatch use `ResearchPaths` and `StateQuery`; Run operations use
`lib.experiments` and `research-op`. All commands share one workspace and
optional `--research-root`.

## Admission

Run admission checks structured state in this order:

| State | Meaning | Handoff |
| --- | --- | --- |
| `NO_PROJECT` | no active Project | `/research-onboard` |
| `NO_DIRECTION` | no active Direction | `/research-brainstorm` |
| `NO_EXPERIMENT` | no Experiment belongs to the active Direction | `/research-package` |
| `NO_PACKAGE` | no active Package owns the Direction and Experiment | `/research-package` |
| `NOT_READY` | compatibility/readiness observation is incomplete | report an advisory |
| `READY` | the selected Experiment can enter the execution loop | continue |

Use:

```python
import sys

sys.path.insert(0, "skills/research-run/scripts")
import admission

state = admission.detect_admission_state(workspace, pkg_id=package_id)
result = admission.run_front_door(
    workspace,
    pkg_id=package_id,
    readiness_ok=True,
    role_sequence=roles,
    adapters=adapters,
)
```

The source directory is not a Python package in every installation, so script callers may import it by
adding `skills/research-run/scripts` to `sys.path`, as the local tests do.

Admission returns `source_seq` and `source_hash`. Keep both on every dispatched role report. A report
from an older state snapshot is rejected.

The interface is deliberately absent from this state machine. Do not add an interface-init handoff to
the run path.

## Procedure

### 1. Read bounded context

Read only the selected Package context:

```bash
python3 skills/research-op/scripts/research_op.py \
  context <package-id> --experiment <experiment-id> --action launch \
  --workspace . --research-root .research
```

For a precise record or history:

```bash
python3 skills/research-op/scripts/research_op.py \
  show experiment '<package-id>::<experiment-id>' \
  --workspace . --research-root .research

python3 skills/research-op/scripts/research_op.py \
  history 'package/<package-id>' \
  --workspace . --research-root .research
```

Context is an in-memory projection. Do not persist a package-level context pack. The launcher freezes
the exact input used by a Run in that Run's `context.json`.

### 2. Select one Experiment

Choose a Package-owned Experiment and read its `spec` directly from state.
Readiness, review, phase, reopen, and Scope are advisory compatibility metadata.
Purpose, config, and gate are desirable working fields; a missing gate limits
the Run to diagnostic or unmeasured claims.

- `purpose`;
- `config_ref`;
- `gate`.

Do not infer a missing field from page order, filenames, or another Experiment.

`Package.execution_mode` controls interaction. `USER_GUIDED` requires an
accepted Run authorization; `AUTONOMOUS` resolves ordinary execution within its
declared boundary. Neither mode changes the Project charter, verifier
independence, budget authority, destructive/external authority, or terminal
outcome.

### 3. Build the workflow snapshot

`driver.load_workflow_snapshot(paths, package_id)` reads:

- Package lifecycle, blocker, and version;
- Package-owned Experiment statuses;
- management-open Runs;
- each Run's canonical `status.json`.

Choose launch, monitoring, result analysis, repair, Plan update, or a user
decision directly from those typed facts. Dashboard server health is
informational and a pending advisory does not block a legal execution.

### 4. Apply research-op envelopes

Every management change is an envelope:

```json
{
  "op": "update",
  "target": "experiments-status",
  "payload": {"id": "P1", "to": "ACTIVE"},
  "idempotency_key": "run:P1:active"
}
```

Validate it with `driver.validate_mutation()`. Compile it with
`driver.research_op_argv(paths, package_id, envelope)`, then run the returned command. Do not write
state files yourself.

If `research-op` rejects the command, use its rule and detail fields to repair the input or select the
correct handoff. Do not patch a projection to hide the rejection.

### 5. Keep Implementation and Tracker current

Before the first code edit, follow the
[Design Guide contract](../research-package/references/design-guide.md).
Materialize each Change plan before its first code edit. After every logical
edit batch, synchronize its code-location predicates:

```bash
python3 skills/research-run/scripts/implementation_status.py sync \
  --workspace . --research-root .research \
  --package <package-id>
```

Run declared TDD checks through the same helper; it records PASS or FAIL
against the current dependency fingerprint:

```bash
python3 skills/research-run/scripts/implementation_status.py verify \
  --workspace . --research-root .research \
  --package <package-id>
```

If a dependency changes after a passing check, the next sync marks that check
STALE and unchecks it. Before implementation review or launch readiness, run
`implementation_status.py check`; it fails unless every planned code location
and verification is currently PASS. Do not add a watcher, edit checkbox state
by hand, or infer completion from the generated page.

After every completed `To-Do` task, update its owner before selecting the next
task: synchronize and verify a Change, or reconcile the Run with `scan-events`.
Tracker then derives the same status automatically. Never write a separate
Tracker row, completion boolean, or current-task marker.

For a configuration-only replacement of a running Experiment, read
[Replacement Run cutover](references/config-replacement.md).

### 6. Check readiness and launch

Before launch, require existing Package/Direction/Experiment ownership,
positive selected versions, `USER_GUIDED` authorization or `AUTONOMOUS`
authority, and any exact resource binding. The launcher freezes that revision.
Readiness, blockers, review, version drift, and a missing numeric gate produce
advisories; without a gate the Run cannot support a verified `PASS`.

The launcher enforces these conditions again:

```bash
python3 lib/experiments/launch.py \
  --workspace . \
  --research-root .research \
  --pkg <package-id> \
  --exp <experiment-id> \
  --tmux-session <name> \
  -- bash <command>
```

Use `--foreground` for a short command. Long runs should use the default tmux transport.

### 7. Monitor and reconcile

List management-open Runs:

```bash
python3 lib/experiments/report.py \
  --workspace . --research-root .research --open
```

Inspect one Run with:

```bash
python3 lib/experiments/report.py \
  --workspace . --research-root .research \
  --run .research/experiments/<package>/<experiment>/<run>
```

Use `status.json`, `events.jsonl`, `metrics.jsonl`, and `log.txt` from that Run. Raw tmux scrollback is
only a debugging aid.

At every check and after completion:

```bash
python3 skills/research-op/scripts/research_op.py \
  --workspace . --research-root .research \
  --pkg <package-id> --op scan-events --payload '{}'
```

This only repairs proven callbacks. It cannot change intent, frozen Evidence,
verifier truth, or resource ownership.

### 8. Extract and finalize results

For a table-backed Run, finalize with `python3 -m lib.experiments.extract` and
its comprehensive metrics CSV. Never hand-write `result.json` or generated HTML.

### 9. Verify and route

Read measured values from the verified `result.json` and its EvidenceRefs.
Compare them with the Experiment gate. Record the result through `research-op`;
the verifier must not rewrite the gate. A success route requires a state-backed
`VERIFIER_VERDICT` Decision bound to the finalized Run event, result hash,
ExperimentSpec version, gate, and measured value.

If another Experiment remains, select it without a legacy readiness or reopen
approval. Otherwise ask the user for the terminal Package outcome.

## Role reports

Reports include role, assigned action, `source_seq`, `source_hash`, Direction,
`sourceExperiment`, status, evidence, blockers, next action, and mutations. The
controller decides; implementation review uses a separate reviewer.

## Stop condition

A tick may stop when:

- every completed Run has its facts, finalized Evidence, and required
  mechanical callbacks recorded;
- no `scan-events` action remains pending;
- each open Run has a scheduled next check;
- the Package is terminal, waiting on a named decision, or blocked by a concrete external condition.

An advisory may remain pending. Waiting is not terminal, and only the user may
commit the Package decision.

The interface can be deleted and rebuilt without changing this procedure.
