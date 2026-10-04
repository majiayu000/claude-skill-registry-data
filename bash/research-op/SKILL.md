---
name: research-op
description: "Use when a governed research-state query, Package mutation, Research Plan update, knowledge registration, Run reconciliation, or self-evolve transition is required."
allowed-tools: Bash(python3 *), Read, Edit, Write, Grep, Glob
context: fork
---

# Research operation gateway

`research-op` is the narrow management-state gateway. One semantic command
writes its event, participant versions, current state, idempotency receipt, and
terminal audit outcome in one SQLite transaction.

## Read boundary

Prefer bounded queries:

```bash
python3 -m lib.research_state.cli --workspace <workspace> \
  show <aggregate-type> [aggregate-id]
python3 -m lib.research_state.cli --workspace <workspace> \
  context <package-id> [--experiment <id>]
python3 -m lib.research_state.cli --workspace <workspace> \
  history <type>/<id>
python3 -m lib.research_state.cli --workspace <workspace> \
  audit <command-id>
```

The compact context packet is action input, not a second authority store. Read
`next_refs` only as needed. Never query generated interface files.

## Write boundary

Every mutation requires:

- a stable actor;
- a stable idempotency key;
- the expected aggregate version when updating;
- a supported typed operation;
- validation before write.

Generic upsert, patch, or remove events cannot change Project, Direction, or
ExperimentSpec intent. User-owned working state uses typed transactions, and
the agent may prepare a transaction but the user owns its commit:

- `PROJECT_COMMIT`;
- `PACKAGE_ACTIVATE`;
- `RESEARCH_PLAN_UPDATE`;
- `PACKAGE_OUTCOME`;
- `PACKAGE_IDENTITY_RENAMED`.

`PACKAGE_ACTIVATE` is the compatibility/bootstrap transaction for the initial
Package, Direction, and ExperimentSpecs. It is not a recurring approval gate.
The transaction kernel still enforces optimistic versions, source receipts,
and atomic participant updates.

## User-owned working-state update

```bash
python3 skills/research-op/scripts/research_op.py \
  --workspace <workspace> \
  --pkg <package-id> \
  --op update \
  --target research-plan \
  --payload '<json>' \
  --actor-type user \
  --actor-id <user-id> \
  --idempotency-key <stable-key>
```

The payload may revise the current Direction, add or revise ExperimentSpecs,
retire ExperimentSpecs, and state one reason. Omit unchanged nodes. The agent
may prepare the payload, but the user owns the commit. Current versions advance
atomically; earlier Runs and Evidence remain immutable. Draft, phase, reopen,
readiness, and Scope labels do not add another approval or mutation surface.
An update may follow a Run, but it cannot rewrite that Run's frozen context or
finalized result.

## Reconcile after execution

The default is User-First Reconcile-After: execute the current working state,
record Run facts and finalized Evidence, then present an advisory reconciliation
for user acceptance. A reconciliation suggestion never rewrites Package,
Direction, or Experiment intent, a frozen Run/Evidence record, or a resource
allocation. It never commits a terminal Package outcome.

`scan-events` may repair a missing launch or terminal callback when the Run files
prove it. That mechanical repair is idempotent state maintenance, not an
advisory plan change. It cannot turn an observation into a verifier verdict or
release an allocation without the terminal evidence required by the resource
contract.

## Other operations

Use command help as the canonical argument reference:

```bash
python3 skills/research-op/scripts/research_op.py --help
```

Package implementation changes, results, learnings, Rules, resource records,
and self-evolve records retain their dedicated validated targets. A terminal
`PACKAGE_OUTCOME` still needs the user's explicit decision; `VERIFIER_VERDICT`
is a separate evidence decision and cannot be inferred from process exit.
A `lib/` helper without a live gateway, skill, CLI, dashboard, install, or test
caller does not belong in the repository.

## Failure contract

Rejected commands are audited with an exact rule and make no state change.
Never repair a rejection by editing SQLite, exported JSONL, `current.json`, Run
envelopes, or Control Panel files.
