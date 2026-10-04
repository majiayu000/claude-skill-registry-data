---
name: agent-teams-command
description: Use when work has genuinely independent streams or distinct builder, evaluator, domain, and integration roles that require bounded multi-agent command scaled from 5 to 100+ agents.
metadata:
  version: "8.1.0"
  updated: "2026-08-18"
  profile: "high-risk"
  assumes: "The runtime supports isolated workers, durable shared task lists, token budgeting, and explicit integration ownership."
  conflicts_with: "Parallelism without pre-flight task lists, unbudgeted token burning, overlapping write ownership, or chat-only coordination."
---

# Agent Teams Command — 安德智能体集群指挥系统 (V8.1)

<skill_contract>
  <input>A mission with independently ownable workstreams, time SLA requirements, pre-flight task list, token budget, interfaces, permissions, and an integration owner.</input>
  <output>An isolated worker fleet (5 to 100+ agents), typed IPC ledger, pre-allocated token ledger, serial integration, cleanup, and evidence receipts.</output>
  <done>Pre-flight task list is 100% reconciled, integrated artifacts pass mission checks, token consumption is within TCLR boundaries, and cleanup gates pass.</done>
  <non_goals>Parallelism without a task list, unbounded token burn, overlapping writers, or worker self-certification.</non_goals>

Strategic intent and final integration remain serial; owned execution runs in dynamically scaled parallel squadrons (5, 10, 50, 100+ agents). Use the Ender lens for commander intent and squad autonomy, Palantir for operational objects/actions, and von Neumann for executable process architecture. Detailed patterns: `references/ender-palantir-command-patterns.md`; examples: `references/classic-campaigns.md`.

## Usage Template

Provide: mission, time SLA, task list candidate, workstreams, scaling tier (5/10/50/100+), dependencies, acceptance criteria, token budget (ETC limit), permissions, runtime capabilities, and integration owner.

## Workflow

<intake>

1. **Mission Intake & Scale Triage**: Analyze mission complexity and select the smallest supported tier: Tier 1 (Squad: 5 agents), Tier 2 (Squadron: 10 agents), Tier 3 (Battle Group: 50 agents), or Tier 4 (Fleet: 100+ agents). If the runtime exposes fewer slots, cap the active fleet to that observed limit.
2. **Pre-flight Task List & Token Gate**: Generate structured task list with explicit owner, territory, expected output, verification command, and token budget (ETC).
3. **Territory Mapping**: Partition work into non-overlapping directories or git worktrees. Every worker gets strictly exclusive write boundaries.

</intake>

<unknowns_gate>

If dependencies, write ownership, or verification commands are ambiguous, return `NEEDS_INPUT` or `INSUFFICIENT_EVIDENCE`. Do not launch parallel workers before pre-flight task list and token ledger are fully reconciled.

</unknowns_gate>

<execute>

1. **Launch Workers**: Dispatch workers in parallel across isolated worktrees. Each receives a typed `context_manifest` containing only its objective, dependencies, territory, inputs, output schema, budget, and verifier.
2. **Typed IPC & Command Board**: Workers report state transitions (`pending` -> `active` -> `review` -> `accepted` -> `closed`) to shared command board.
3. **Independent Verification**: Evaluator and reviewer agents verify worker outputs against objective criteria. No worker self-certification.
4. **Serial Integration & Join Gate**: Integrator aggregates verified artifacts and receipts in dependency order. Do not merge private branch transcripts into the integration context. Run regression tests.
5. **Durable Write-back & Cleanup**: Persist execution receipts, update system logs, and clean up temporary worktree branches.

For high-risk operations or cross-repo modifications, require independent review and human approval. Prepare a rollback plan before applying writes.

</execute>

<evaluate>

Audit total token consumption against the mission-declared TCLR: verified tasks resolved per 10,000 effective tokens consumed. Higher is better; do not invent a universal threshold. Verify all workstreams reached `accepted` or `closed` state, no file ownership conflicts occurred, and the declared regression suite passed.

</evaluate>

<retry_policy>

`max_attempts: 2`. Stop on repeated failure signature or `NO_PROGRESS`. If a worker stalls or fails, reassign territory or downgrade to serial execution rather than launching unbudgeted retries.

</retry_policy>

<state_contract>

Persist `{mission_id, run_id, status, attempt, budget, token_ledger, task_list, worker_fleet, context_manifest, command_board, evidence, unknowns, next_action}` in durable storage.

</state_contract>

## Failure Protocol

- `NEEDS_INPUT`: Ambiguous mission scope or overlapping territory; prompt for clarification before launch.
- `INSUFFICIENT_EVIDENCE`: Missing verification command or unverified worker output; reject merge.
- `BLOCKED_PERMISSION`: Worker lacks required tool or file write permission; escalate to commander.
- `BLOCKED_DEPENDENCY`: Upstream task failed; suspend dependent workers until resolved.
- `VERIFY_FAILED`: Artifact fails independent evaluation; reject and trigger bounded repair.
- `NO_PROGRESS`: Worker produces duplicate errors after 2 attempts; stop worker and flag for review.
- `BUDGET_STOP`: Token consumption exceeds allocated ETC budget; trigger automatic halt. `max_attempts: 2`.

## Output Contract

Return `status`, `result` (worker fleet summary, task resolution ledger, and verified artifacts), `evidence` (source receipts, lint receipts, and integration logs), `unknowns`, and `next_action` including approval or rollback when relevant.

## Edge Cases

- **File Collision**: Two workers attempt to modify the same file -> Integrator serializes execution and assigns one canonical owner.
- **Worker Runaway**: Worker exceeds token budget without progress -> Heartbeat monitor triggers instant `BUDGET_STOP` kill.
- **Context Drift**: Worker hallucinates outside its assigned territory -> Reviewer rejects output and logs territory violation.

## Success Metrics

- 100% of pre-flight tasks resolved with verifiable evidence.
- Zero file write collisions across concurrent workers.
- Total token expenditure remains within allocated ETC budget.
- Wall-clock time reduced significantly compared to single-agent baseline.

## Quality Gates

- [ ] Pre-flight task list and token ledger reconciled before execution.
- [ ] Exclusive write territories assigned to all active workers.
- [ ] Independent reviewer verified all deliverables (no self-certification).
- [ ] Integrator executed serial merge with passing regression suite.
- [ ] High-risk operations received independent review, human approval, and rollback readiness.
- [ ] Worktrees cleaned up and durable receipts written to system log.

</skill_contract>
