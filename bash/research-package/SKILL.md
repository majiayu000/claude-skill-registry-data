---
name: research-package
description: "Use when converting a Brainstorm, maintaining user-owned Package working state, restructuring an Experiment plan, or recording its terminal outcome."
---

# Research package

Own one user-owned Package working state through execution, advisory
reconciliation, and the explicit terminal decision.

## Authority

Management authority is `.research/state/research.sqlite3`. Draft documents are
content-addressed NoteRefs. Runs and evidence live under
`.research/experiments/`. The Control Panel is read-only.

## Lifecycle

```text
Project -> Package working state -> execute current Experiment
  -> Run/Evidence -> advisory reconciliation -> user outcome
```

A Package, Direction, and ExperimentSpec are current working records. Typed
transactions may revise them and create new versions without rewriting earlier
Runs or Evidence. Draft, phase, reopen, and Scope labels are compatibility or
advisory metadata; they do not create a second execution gate. A legacy
readiness or activation ceremony is not a prerequisite for each later Run.

The existing activation command remains a compatibility/bootstrap path that
atomically writes:

- the existing Package as `ACTIVE`;
- one versioned `ACTIVE` Direction;
- the initial versioned ExperimentSpecs;
- `execution_mode`: `USER_GUIDED` or `AUTONOMOUS`.

There is no intermediate approval aggregate or execution lease.

## User-First Reconcile-After

The user owns the current working state. Execute that state, finalize the Run
Evidence, and then offer a reconciliation that explains what the evidence may
suggest changing. The user may accept, reject, or revise the suggestion through
`research-op`. The suggestion is advisory and never rewrites a frozen Run,
finalized Evidence, resource allocation, or terminal Package outcome.

Only a proven missing launch or terminal callback may be repaired mechanically.
That repair is not plan approval, a verifier verdict, or a terminal decision.

## Convert a Brainstorm

```bash
python3 skills/research-package/scripts/draft_package.py \
  --workspace <workspace> convert \
  --brainstorm-id <id> \
  --title "<title>" \
  --title-rationale "<why this identity is stable>" \
  --actor-id <agent-id>
```

This preserves Brainstorm provenance and creates the initial working state.
Any Draft label is advisory compatibility metadata.

## Revise working state

Read one compact context packet, then let the user revise only the changed
record fields or document body:

```bash
python3 skills/research-package/scripts/draft_package.py \
  --workspace <workspace> revise \
  --package-id <id> \
  --patch '{"problem":"...","objective":"..."}' \
  --body-file <proposal-fragment.html> \
  --actor-id <agent-id>
```

The proposal document is for human review. Direction and ExperimentSpec JSON
are the executable working intent. A phase or reopen record does not block a
user-authorized execution. The user still owns any resulting working-state
transaction.

## Bootstrap or confirm the working state

When a new workspace needs an initial state, the user may accept the exact
Direction, ExperimentSpecs, and execution mode in one command:

```bash
python3 skills/research-package/scripts/draft_package.py \
  --workspace <workspace> activate \
  --package-id <id> \
  --direction <direction.json> \
  --experiments <experiments.json> \
  --execution-mode USER_GUIDED \
  --actor-id <user-id>
```

Each ExperimentSpec requires:

```json
{
  "id": "experiment/example/p1",
  "local_id": "P1",
  "spec": {
    "purpose": "Test the claim.",
    "config_ref": "configs/p1.yaml",
    "gate": {
      "metric": "accuracy",
      "operator": ">=",
      "threshold": 0.8
    }
  }
}
```

Reject missing, textual, or ambiguous gates. Verify the resulting Package,
Direction, and ExperimentSpecs through structured state. Later execution does
not require another activation, phase, reopen, readiness, or reconciliation
approval. The launcher's current identity, version, numeric-gate, authorization,
and resource checks remain in force.

## Edit the working state

Use the `research-plan` target through `research-op` after explicit user
acceptance. Include only changed Direction fields, new or revised
ExperimentSpecs, explicit retirements, and a reason. The transaction versions
current intent atomically and preserves prior Runs and Evidence. Reconciliation
is advisory until the user accepts an update. Never copy a measured value into
the gate, mutate a frozen Run, or release a resource from this path.

Changing the display title keeps the technical Package id and route slug stable
and records the prior title. Changing the technical identity before any Run is
allowed only through the dedicated identity transaction. Once evidence exists,
keep that technical identity stable. Switching to `AUTONOMOUS` likewise
requires an explicit user transaction.

## Record the outcome

Prepare a hash-bound review:

```bash
python3 skills/research-package/scripts/draft_package.py \
  --workspace <workspace> review-outcome \
  --package-id <id> \
  --outcome SUCCESS \
  --reason "<evidence-backed reason>" \
  --evidence '["run:<id>","result:<sha256>"]' \
  --actor-id <agent-id>
```

Only the user commits `SUCCESS` or `FAIL` with the returned review hash:

```bash
python3 skills/research-package/scripts/draft_package.py \
  --workspace <workspace> commit-outcome \
  --package-id <id> \
  --outcome SUCCESS \
  --reason "<same reason>" \
  --evidence '["run:<id>","result:<sha256>"]' \
  --review-sha256 <sha256> \
  --review-id <conversation-review-id> \
  --actor-id <user-id>
```

Never treat process exit, a checkpoint, or an unverified metric as the terminal
decision. `SUCCESS` also requires an accepted `VERIFIER_VERDICT` that still
matches the current ExperimentSpec version, finalized Run event, result hash,
and gate.

## Stop conditions

Stop when the Project charter would change, evidence is missing, a destructive
or external action lacks authority, or the user has not made the terminal
decision. A pending Draft, phase, readiness, reopen, Scope, or advisory record
is not by itself a stop condition. A missing mechanical callback is repaired
through `research-op`; it is not used to manufacture evidence or a terminal
outcome.
