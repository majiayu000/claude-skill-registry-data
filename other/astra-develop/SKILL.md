---
name: astra-develop
description:
  End-to-end software development workflow that plans a task, resolves material ambiguity, implements it, and verifies
  acceptance criteria while routing bounded work to an appropriate model/reasoning level. Use when the user asks Codex
  to implement, fix, refactor, migrate, or extend software and wants a plan-first workflow with efficient model usage.
---

# Astra Develop

Complete software tasks through:

```text
UNDERSTAND → PLAN → RESOLVE → IMPLEMENT → VERIFY → REPORT
```

Optimize for:

- correctness against acceptance criteria,
- strong reasoning at decision points,
- cheaper execution after decisions are stable,
- minimal relevant validation by default,
- low orchestration and context overhead.

Do not create a multi-agent swarm. Delegate only when a different model/reasoning profile or isolated context provides a
clear benefit.

## Operating rules

1. Inspect only enough repository context to understand the task.
2. Create a concise plan before editing code.
3. Ask the user only about material unresolved decisions.
4. Batch material questions into one concise message when possible.
5. If there are no material questions, continue without asking for plan approval.
6. Update the plan when new evidence invalidates an assumption.
7. If implementation reveals a new material product/architecture decision, return to planning before continuing.
8. Implement the accepted plan with the cheapest capable model.
9. Run the minimum meaningful checks needed to establish correctness unless the user requests full QA.
10. Explicitly verify every acceptance criterion before finishing.
11. Keep the final report concise: changes, validation, remaining risks/blockers.

## Material question gate

Ask the user only when a decision could materially change:

- externally visible behavior or UX,
- architecture or public contracts,
- persistent data shape or migration behavior,
- security/privacy/authorization behavior,
- destructive or difficult-to-reverse operations,
- an explicit acceptance criterion,
- a meaningful product trade-off.

Do not ask about low-impact implementation details that can be safely inferred from the repository or existing
conventions.

If the user explicitly asks you to use your judgment and not ask questions, record reasonable assumptions and continue
unless doing so would be unsafe or destructive.

## Smart routing

Choose a routing class from the task, not from task size.

### Routine/local

Examples: obvious bug, local component, endpoint, test, docs, mechanical refactor.

- Plan and execute in the parent when it is capable.
- Preferred execution model: GPT-5.6 Sol.
- Do not spawn a specialist merely to produce a trivial plan.

### Read-heavy exploration

Examples: locating ownership, tracing unfamiliar code paths, surveying a large module.

- Read `agents/explorer.md`.
- Delegate only if isolated exploration will reduce parent context or substantial reading is required.
- Preferred: GPT-5.6 Terra, medium.

### Hard but bounded

Examples: difficult local bug or implementation with known architecture.

- Preferred planning: GPT-6 Astra, low.
- Preferred execution: GPT-5.6 Sol; use Astra low only if implementation itself needs deeper reasoning.
- If delegation is useful, read `agents/deep-executor.md`.

### Cross-layer / materially ambiguous

Examples: frontend + API + DB, auth behavior, cache/jobs interactions, non-trivial product states.

- Read `agents/planner.md`.
- Preferred planning: GPT-6 Astra, medium.
- After the plan stabilizes, step down to Sol or Astra low for implementation.

### Architecture / consequential decision

Examples: service boundaries, durable data-model choices, auth architecture, consistency guarantees, queueing,
deployment topology, major UX/information architecture, irreversible migration strategy.

- Read `agents/architect.md`.
- Preferred planning: GPT-6 Astra, high.
- Persist the accepted decision before implementation.
- Step down for execution.

### Adversarial review

Use only when a consequential plan benefits from an independent challenge.

- Read `agents/critic.md`.
- Preferred: GPT-6 Astra, xhigh.
- Do not automatically run this after every High plan.

### Deep investigation

Examples: subtle concurrency/consistency failures, difficult production root cause, security-sensitive investigation.

- Read `agents/deep-debugger.md`.
- Preferred: GPT-6 Astra, xhigh.

### Max reasoning

- Read `agents/critical.md`.
- Never auto-use Max.
- Use only when:
  - the user explicitly requests maximum/deepest analysis, or
  - XHigh did not resolve a genuinely high-risk problem and the user approves escalation.

## How to delegate

The files in `agents/` are skill-local routing profiles, not Codex auto-discovered custom-agent TOMLs.

When delegating:

1. Read only the selected profile.
2. Spawn one bounded subagent with the profile's requested model and reasoning effort.
3. Give it only the context needed for that phase.
4. Require a concise result.
5. Avoid status polling; wait for its result unless intervention is necessary.
6. Close/stop using the specialist when its bounded job is complete.

If the parent already has the appropriate model/reasoning and context isolation adds no value, do the work directly
instead.

## Phase 1 — Understand

Identify:

- requested behavior,
- likely affected systems/files,
- explicit acceptance criteria,
- relevant repository conventions,
- implicit constraints supported by existing code,
- material unresolved decisions.

Prefer targeted searches and file reads over repository-wide scanning.

If substantial read-heavy discovery is necessary, use the explorer profile.

## Phase 2 — Plan

Write a concise, actionable plan before making edits.

Prefer 3–8 steps. Include only what matters:

- goal,
- affected areas,
- important assumptions/decisions,
- implementation steps,
- acceptance criteria,
- validation approach,
- meaningful migration/rollback or operational concerns.

Do not write a long design document for routine work.

### Domain emphasis

For BE/Ops, consider as relevant:

- contracts/interfaces,
- data integrity and transactions,
- auth/security boundaries,
- migrations/rollback,
- queues/caching/consistency,
- failure recovery,
- observability/operations.

For UX/Product, consider as relevant:

- primary user/job-to-be-done,
- user flow/information hierarchy,
- loading/empty/error/success/permission states,
- responsive behavior,
- accessibility,
- interaction/content constraints.

For frontend engineering, escalate based on engineering complexity:

- state/data synchronization,
- SSR/hydration,
- performance,
- accessibility implementation,
- frontend/design-system architecture.

## Phase 3 — Resolve

After writing the initial plan:

- identify material unresolved questions,
- ask them in one concise batch when possible,
- wait for the user's answer,
- revise the plan accordingly.

If there are no material unresolved questions, proceed automatically.

Do not repeatedly interrupt execution for minor decisions.

## Persist the plan

If the repository already uses Backlog.md or another task/spec system and the relevant task is identifiable:

- update that task with the accepted plan,
- keep constraints and acceptance criteria there,
- use it as the handoff between planning and execution,
- later append deviations and verification results.

Do not install or introduce Backlog.md solely because this skill is active.

If no task system exists, keep the plan in the session unless the user asks for a persistent artifact.

## Phase 4 — Implement

Implement the accepted plan.

Prefer:

```text
mechanical/repetitive work → Terra or Sol
normal implementation → Sol
hard bounded implementation → Sol or Astra Low
unresolved cross-layer reasoning → Astra Medium
new architecture/product decision → return to planning
```

Avoid parallel code-writing agents unless work is genuinely independent and file ownership does not overlap.

Make the smallest coherent change that satisfies the plan and repository conventions.

If implementation invalidates the plan:

- update the plan,
- ask the user only if the new decision crosses the material-question gate,
- otherwise document the adjustment and continue.

## Phase 5 — Verify

Default to **minimal meaningful verification**, not zero verification and not automatic full QA.

Choose checks based on the changed surface:

```text
utility/local logic
→ focused unit tests

frontend component/flow
→ relevant tests + typecheck/lint when appropriate

API/DB behavior
→ targeted unit/integration tests

cross-layer feature
→ relevant integration/e2e path

migration/architecture-sensitive work
→ targeted checks appropriate to the actual risk
```

Also:

- verify acceptance criteria explicitly,
- inspect relevant diffs,
- do not repeatedly rerun already-passing broad suites unless subsequent changes can affect them,
- do not dump huge logs into context; retain the relevant failure section.

### Full QA

If the user explicitly requests "full QA", "full validation", "run everything", or equivalent:

- run the repository's prescribed full validation suite when available,
- include broader tests/lint/typecheck/build/e2e as defined by the project,
- report anything that could not be run.

Do not infer "full QA" from ordinary requests to test the change.

## Phase 6 — Report

Finish with a concise report containing:

- what changed,
- important plan deviations,
- checks/tests run and their result,
- acceptance-criteria status,
- remaining blocker/risk, if any.

Do not include a long narrative of the agent workflow unless requested.
