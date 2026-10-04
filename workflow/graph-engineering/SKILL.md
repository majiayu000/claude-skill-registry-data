---
name: graph-engineering
description: Use when a workflow has explicit data dependencies, independently executable branches, typed joins, or node-local recovery needs that justify a bounded static dependency graph.
metadata:
  version: "8.1.0"
  updated: "2026-08-18"
  profile: "high-risk"
  assumes: "Nodes, payloads, writers, verifiers, budgets, and permission boundaries can be declared before execution."
  conflicts_with: "Dynamic or cyclic expansion, overlapping writers, whole-graph retries, hidden joins, or external effects without approval and compensation."
---

# Graph Engineering

<skill_contract>
  <input>A dependency-heavy objective with candidate nodes, data schemas, owners, effects, verifiers, joins, budgets, and durable state paths.</input>
  <output>A validated static DAG contract with typed edges, explicit joins, node-local recovery, and graph-level receipts.</output>
  <done>Static invariants and terminal acceptance checks pass with fresh node, join, budget, permission, and state evidence.</done>
  <non_goals>Temporal loop design, worker-team command, runtime-kernel implementation, dynamic graphs, or universal parallelism.</non_goals>

Use Graph Engineering for dependency width. Use `loop-engineering` for repeated
execution through time, `agent-teams-command` for process ownership and IPC,
and `harness-engineering` for scheduler, permission, lease, and observability
infrastructure. A graph node may contain a bounded Loop or Agent Team.

## Usage Template

Provide: objective/non-goals, candidate nodes, real data dependencies, payload
schemas, owners and write territories, join semantics, node/terminal verifiers,
effects and permissions, artifact/state paths, budgets, stop conditions, and
recovery. Load `references/graph-contract.md` for the full schema and boundary;
start from `references/diamond-graph-example.json`.

## Workflow

<intake>

Run the admission gate before drawing a graph:

1. Identify which steps actually consume another step's output.
2. Estimate independent width, critical path, scheduler overhead, and review
   load. Require measurable payback or stronger independent evaluation.
3. Keep one-shot or Loop execution when work is mainly sequential, small, or
   cheaper to review serially.
4. Limit V8.1 to a static DAG: sequence, pipeline, diamond, maker-checker, or
   bounded subgraph. Put repetition inside a `loop` node; reject graph cycles
   and dynamic expansion.

</intake>

<unknowns_gate>

Return `NEEDS_INPUT` when objective, graph owner, dependency direction, payload
schema, writer, verifier, permission boundary, budget, join, or recovery is
missing and cannot be discovered safely. Probe candidate independence with a
small dry run. Do not invent an edge merely because two steps are adjacent.

</unknowns_gate>

<execute>

1. Write the JSON contract and run
   `scripts/validate_graph_contract.py <contract.json> --strict`.
2. Give every node one owner, typed inputs/outputs, explicit reads/writes,
   verifier, timeout, attempt/tool caps, effect class, idempotency, and
   compensation.
3. Add only data, control, verification, failure, or compensation edges.
   Schema-bearing edges must match both endpoint contracts.
4. Enforce one writer per target. Agent workers use isolated artifacts or
   worktrees; the integration owner controls shared schemas and final writes.
5. Declare a join for every multi-input node. Choose `all`, `reduce`,
   `first-success`, `quorum`, `barrier-verifier`, or `human-gate`; name the
   exact input set and verifier.
6. Schedule only `READY` nodes whose dependencies are verified. Persist every
   transition and edge payload reference before releasing successors.
7. Retry the failed node or smallest invalid subgraph after a changed
   diagnosis. Preserve verified branches; never replay the whole graph merely
   for convenience.
8. Require human approval, a compensation route, and verified rollback before
   any external, shared, destructive, published, credentialed, or financial
   effect. In strict contracts, name the external node ID in
   `approval_required`, feed it a typed approval receipt directly from a
   `human-gate`, and list each exact write target as allowed and not denied.
9. At terminal nodes, verify the end-to-end objective and graph guardrails;
   node success alone cannot certify graph success.

</execute>

<evaluate>

Check static integrity: known endpoints, compatible schemas, reachability,
acyclicity, single writers, complete joins, finite budgets, and compensated
effects. Check runtime integrity: deterministic readiness, duplicate-delivery
idempotency, checkpoint replay, permission denial without mutation,
smallest-unit recovery, terminal evidence, and cleanup. Use an independent
reviewer for consequential graph behavior.

</evaluate>

<retry_policy>

`max_attempts` comes from each node and never exceeds the graph cap. Retry only
after changing diagnosis, input, owner, tool, or strategy. Stop on a repeated
signature, incompatible edge, permission denial, invalid checkpoint, exhausted
review budget, or `NO_PROGRESS`. Whole-graph retry is forbidden in strict V8.1.

</retry_policy>

<state_contract>

Persist `{run_id, graph_id, status, attempt, budget, evidence, unknowns,
last_error, next_action}` plus contract/implementation hashes, node states,
edge payload locators, join decisions, writer leases, approvals, checkpoints,
compensations, terminal receipts, and cleanup. Use append-only events and an
atomic current checkpoint; chat history is not graph state.

</state_contract>

## Failure Protocol

- `NEEDS_INPUT`: a mandatory graph contract or authority field is unresolved.
- `BLOCKED_DEPENDENCY`: keep affected nodes `WAITING`; run only independent
  ready nodes.
- `BLOCKED_PERMISSION`: deny the effect, preserve state, and request approval.
- `VERIFY_FAILED`: reject the node/join artifact and recover the smallest unit.
- `NO_PROGRESS`: the same failure repeats after a changed attempt.
  `max_attempts: 2` by default and always finite.
- `BUDGET_STOP`: stop scheduling, checkpoint, compensate active effects, and
  return a partial graph receipt.

## Output Contract

Return `status`, `result` (terminal decision and accepted artifacts), `evidence`
(validator, node, join, terminal, budget, approval, and cleanup receipts),
`unknowns`, and `next_action` (stop, retry node, compensate, approval, or
handoff).

## Edge Cases

- Two workers both write `report.md`: strict validation fails the single-writer
  invariant; isolate worker artifacts and let one reduce node own the report.
- A branch passes but its sibling times out: preserve the verified branch,
  retry only the failed node within cap, and do not release the join until its
  declared mode and verifier pass.

## Success Metrics

- The strict graph validator passes before execution.
- Graph admission shows bounded value beyond orchestration and review cost.
- Every node, edge, join, effect, and terminal claim has fresh evidence.
- Recovery replays the smallest failed unit from durable state.

## Quality Gates

- [ ] Static DAG scope and Loop/Teams/Harness boundaries are explicit.
- [ ] Owners, payload schemas, writers, joins, verifiers, and budgets are exact.
- [ ] State replay and duplicate delivery preserve graph invariants.
- [ ] External effects have independent review, approval, compensation, and rollback.
- [ ] Terminal verification supports the end-to-end claim.

</skill_contract>
