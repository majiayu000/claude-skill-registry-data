---
name: context-manager
description: Use when a long-running agent task needs context budgeting, checkpointing, compaction, retrieval, or capability-based model routing.
metadata:
  version: "8.1.0"
  updated: "2026-08-18"
  profile: "stateful"
  assumes: "Runtime context limits, cost policy, and durable storage are available or can be bounded explicitly."
  conflicts_with: "Hard-coded vendor pricing, silent context loss, or retaining low-value history at the expense of execution state."
---

# Context Manager

<skill_contract>
  <input>An active objective, runtime context limits, decision-critical state, evidence, budgets, and durable storage.</input>
  <output>A bounded context manifest, checkpoint, compaction decision, and capability-routing receipt.</output>
  <done>The next decision can be resumed without losing constraints, permissions, provenance, or failure history.</done>
  <non_goals>Task orchestration, vendor-specific routing, hidden truncation, or retaining history that cannot change a decision.</non_goals>

Treat context as RAM, durable storage as disk, and tools as retrieval. Pay only for information that changes the next decision or prevents an execution error.

## Usage Template

Provide: objective, phase, runtime context limit, token/cost budget, active constraints, current evidence, durable state location, and expected next decisions.

## Workflow

<intake>

Measure available budget from runtime data; do not infer limits or prices from model names. Partition context into objective, constraints, active state, evidence, open unknowns, and history. Identify the next irreversible or high-cost decision.

</intake>

<unknowns_gate>

If runtime limits or durable state are unavailable, choose a conservative explicit budget or return `NEEDS_INPUT`. Never silently drop constraints, approvals, source provenance, failed attempts, or user decisions.

</unknowns_gate>

<execute>

Apply `KEEP / SUMMARIZE / DROP / RETRIEVE`:

- **KEEP:** objective, acceptance criteria, permissions, active files, current state, fresh evidence, blockers.
- **SUMMARIZE:** completed exploration, superseded plans, verbose tool output; retain decisions and locators.
- **DROP:** duplicated prose, stale speculation, irrelevant logs, and reconstructible boilerplate.
- **RETRIEVE:** load detailed references only when the next action needs them.

Checkpoint at phase boundaries or before compaction. Route work by capability requirements such as reasoning depth, tool use, latency, cost, multimodality, and context capacity; runtime policy selects the implementation. Keep stable prompt prefixes unchanged when caching is available.

Maintain one versioned shared-intent surface for objective, acceptance criteria,
decisions, and non-code constraints. Give each worker a private context manifest
containing only its required slice. Return summary, artifact locator/hash,
decision, unknowns, and verifier receipt; do not treat chat replay as durable
coordination. An independent critic receives the claim and raw artifact, not the
builder's desired conclusion.

For Graph workflows, treat each node context as private RAM and each typed edge
payload as a bounded transfer contract. Pass artifact locators, schemas,
decisions, and verifier receipts; do not concatenate all branch histories into
every successor. A join loads only the declared inputs needed for its decision.

</execute>

<evaluate>

Simulate the next action using only the checkpoint. It must recover objective, constraints, state, evidence, unknowns, last error, and next action without consulting lost chat. Compare estimated budget with runtime telemetry and correct drift.

</evaluate>

<state_contract>

Persist `{run_id, status, attempt, budget, evidence, unknowns, last_error, next_action}` plus phase, shared-intent hash, worker context manifests, decisions, permissions, normalized termination reason, active resources, completed work, rejected approaches, artifact/retrieval pointers, and budget telemetry. Version checkpoints; never replace the only recoverable state.

</state_contract>

## Failure Protocol

- `NEEDS_INPUT`: no reliable limit or cost policy exists and the choice changes execution.
- `INSUFFICIENT_EVIDENCE`: a proposed summary cannot preserve a material decision or locator; keep the source segment.
- `VERIFY_FAILED`: checkpoint replay loses required state; restore the prior version and recompact.
- `BUDGET_STOP`: reserve enough capacity for receipt and handoff, persist state, then stop.

## Output Contract

Return `status`, `result` (budget plan or checkpoint), `evidence` (runtime telemetry and replay check), `unknowns`, and `next_action` with required retrieval pointers.

## Edge Cases

- Runtime pricing changes mid-project: recompute from current policy; preserve earlier estimates as historical evidence.
- A long log contains one decisive error: keep the error signature and locator, summarize the surrounding output, and retain retrieval access.
- A Graph join receives three branch transcripts: retrieve the declared output
  artifacts and receipts, not the full private context of every branch.
- A subagent summary omits a non-code constraint: reject the handoff, reload the
  versioned shared-intent slice, and regenerate the summary before integration.

## Success Metrics

- A fresh agent can resume from the checkpoint without material context loss.
- Context use stays within the declared runtime budget.
- Routing depends on capabilities and policy, not fixed model names.

## Quality Gates

- [ ] Objective, constraints, permissions, evidence, and next action survive replay.
- [ ] Shared intent and private worker contexts remain separated with bounded summary IPC.
- [ ] Dropped content is duplicated, stale, or reconstructible.
- [ ] Budget estimates cite current runtime data or explicit conservative assumptions.
- [ ] Checkpoints are versioned and recoverable.

</skill_contract>
