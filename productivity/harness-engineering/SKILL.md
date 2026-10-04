---
name: harness-engineering
description: Use when an agent workflow needs production-like runtime controls for context, tools, permissions, observability, scheduling, evaluation, recovery, or maintenance.
metadata:
  version: "8.1.0"
  updated: "2026-08-18"
  profile: "high-risk"
  assumes: "The workflow uses tools or delegated actions whose environment, permissions, and event trail can be controlled."
  conflicts_with: "Prompt-only safety, broad credentials, hidden tool effects, or autonomous routines without finite budgets and rollback."
---

# Harness Engineering

<skill_contract>
  <input>An agent workflow, runtime environment, tools, data sensitivity, effects, cadence, risk, and operator constraints.</input>
  <output>An auditable runtime kernel with scoped permissions, scheduling, observability, recovery, and eval controls.</output>
  <done>An end-to-end trace and failure-path tests prove bounded, replayable, recoverable delegated action.</done>
  <non_goals>Business-task decomposition, prompt-only safety, broad credentials, or unbounded scheduled autonomy.</non_goals>

Treat the harness as the kernel around an LLM OS: context is RAM, durable state is disk, tools are system calls, skills are programs, the scheduler is control, and evals are verifiers. Load `references/runtime-control-patterns.md` for matrices and schemas. Start guarded automation from `references/runtime-envelope-example.json` and validate it with `scripts/validate_runtime_envelope.py --strict`.

## Usage Template

Provide: workflow, users, agent roles, environment, tools/connections, data sensitivity, delegated actions, cadence, throughput/SLA, failure history, and risk tolerance.

## Workflow

<intake>

Run the trace gate: the harness must be able to show what the agent saw, proposed, called, changed, and verified. Separate **Intent Plan** (human-reviewable source), **Compiled Contract** (validated runtime envelope), **Agent** (instructions/capabilities), **Environment** (network/files/credential broker), and **Session** (mounted context/events/state). Define one auditable control path for high-risk intent and final joins. Model output is never execution authority.

</intake>

<unknowns_gate>

If state ownership, credential scope, external side effects, retention, or approval authority is unclear, return `NEEDS_INPUT`. Probe tools with read-only discovery where possible; unknown side effects default to denied.

</unknowns_gate>

<execute>

1. Pass Four-C: **Context** truth/retrieval, **Connections** scoped accounts/APIs, **Capabilities** versioned skills/scripts/evals, **Cadence** trigger/receipt/anomaly/stop.
2. Compile the reviewed intent plan into a versioned runtime envelope. Validate
   plan hash, `tool_execution_owner: host`, filesystem/network/secret boundaries,
   output cardinality, legal no-op, budgets, approvals, audit paths, and
   rollback before execution.
3. Map runtime: stored program, control unit, hot context, durable disk, event bus, I/O tools, verifier, and garbage collector.
4. Choose the lowest-context primitive: deterministic script/hook, skill,
   static Graph, connector, dynamic workflow, or agent team. Load capabilities
   lazily. Graph Engineering owns dependency semantics; the harness owns the
   ready queue, leases, duplicate delivery, concurrency, and executor health.
5. Define each tool as a narrow host-owned system call with purpose, explicit inputs, bounds, timeout, idempotency, failure path, evidence, and audit location. Validate model-proposed arguments before dispatch.
6. Enforce zero trust and least privilege in the environment, not only prose:
   bind access to task, resource, operation, and time; use exact network
   allowlists and opaque secret handles; never expose raw credentials to model
   context. Stage and vet writes before external commit.
7. Normalize each model `termination_reason` into complete, tool request,
   checkpoint/truncation, refusal/error, or unknown. The host decides whether
   to execute, continue, checkpoint, or escalate; success prose cannot override
   the control signal or verifier.
8. For delegated action require mandate, scope, limit, preview, receipt, and rollback. Human approval governs irreversible/shared/financial/published/credentialed actions.
9. Define allowed output types, maximum external outputs, and a verifiable
   `NO_OP` condition. Quiet execution is success only when eligibility was
   checked and no side effect occurred.
10. Add deterministic feedback (tests, lint, LSP, policy checks) outside context when possible; add independent evaluator/red team for high-risk semantic output.
11. Persist an append-only session event log and checkpoint; define alerts, fallback, incident response, cleanup, permission review, and stale-context/rule review.
12. For scheduled work define Trigger, Context, Steering, Receipt, budget, stop, recovery, and executor health. A schedule firing is not task success.
13. For Graph execution, persist node/edge/join transitions before releasing
    successors, make delivery idempotent, recover from the last verified
    checkpoint, and test permission denial, worker loss, duplicate events, and
    compensation without relying on in-memory scheduler state.

</execute>

<evaluate>

Threat-model normal, denied, timeout, partial-write, stale-context, duplicate-trigger, compromised-input, evaluator-disagreement, and rollback paths. Verify permissions with actual environment boundaries and run an independent end-to-end trace. Adoption fails if operators cannot inspect or recover the system.

</evaluate>

<retry_policy>

`max_attempts: 3` per tool/failure class. Retry only idempotent or compensated actions after changing diagnosis/strategy. Use exponential delay for transient dependencies. Stop on repeated signature, permission denial, ambiguous side effect, or `NO_PROGRESS`.

</retry_policy>

<state_contract>

Persist `{run_id, status, attempt, budget, evidence, unknowns, last_error, next_action}` plus intent-plan hash, compiled-contract hash, agent/environment/session versions, context manifest, normalized termination reason, tool/permission/credential-lease registry, output quota, no-op receipt, event offsets, approvals, evals, alerts, recovery point, and rollback receipts. State transitions are auditable and replayable.

</state_contract>

## Failure Protocol

- `NEEDS_INPUT`: ownership, effect, retention, or approval authority is ambiguous.
- `BLOCKED_PERMISSION`: deny the call and continue with a safer read-only path when useful.
- `BLOCKED_DEPENDENCY`: checkpoint, back off, and expose executor health.
- `VERIFY_FAILED`: trace, eval, guardrail, or rollback test fails; block autonomy escalation.
- `NO_PROGRESS`: changed attempts repeat the signature. `max_attempts: 3`.
- `BUDGET_STOP`: stop scheduler/workers, checkpoint, and emit a recovery receipt.

## Output Contract

Return `status`, `result` (runtime architecture and controls), `evidence` (trace/eval/failure tests), `unknowns`, and `next_action` including approval or rollback.

## Edge Cases

- A connector exposes broad account access for a narrow task: create a scoped proxy/allowlist or keep the workflow manual; instructions alone are insufficient.
- A model emits plausible success text with a tool request: validate and execute
  the tool in host code, then verify its result; do not treat the text as task
  completion.
- A maintenance run finds no eligible change: emit a verified `NO_OP` receipt
  and zero external outputs rather than creating notification or PR noise.
- The scheduler ran on time but the state store was stale: block mutation, mark the run failed, and recover from the last verified checkpoint.
- A Graph worker completes twice after lease expiry: deduplicate by node/run
  identity and release successors only from one verified transition.

## Success Metrics

- Every delegated action is bounded, observable, independently verifiable, and recoverable.
- Runtime state can be replayed across sessions without relying on chat history.
- Autonomy level follows measured reliability and operator review capacity.

## Quality Gates

- [ ] Agent, Environment, Session, and serial control ownership are explicit.
- [ ] Intent plan and compiled runtime envelope are hash-bound and pass strict validation.
- [ ] Tool effects are enforced by real permissions and contracts.
- [ ] Termination routing, secret isolation, output limits, and legal no-op are host-enforced.
- [ ] Independent eval, approval, manual fallback, and rollback match risk.
- [ ] Schedules have executor receipts, hard budgets, stop, and recovery.
- [ ] Maintenance includes cleanup, permission audit, and rule half-life.

</skill_contract>
