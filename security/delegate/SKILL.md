---
name: delegate
description: "Choose responsibility for substantial work before deep execution: keep one responsibility's coupled parts in a single lane, and hand a bounded or independent lane to a worker when clean context, an unknown cause, independent review, or coordinator attention materially improves the outcome."
---

# Delegate

Choose responsibility before deep execution. Worker lanes move a bounded responsibility into clean agent contexts without confusing delegation with permission. Use the fewest work surfaces that materially improve the outcome.

## Responsibility choice

Decide, before committing to a deep implementation or investigation path, whether this task stays in the Coordinator lane or becomes a worker lane. This is a responsibility decision, not a parallelism switch.

- A user request to work solo, or any instruction that forbids subagents, ends the question. Do not delegate.
- Keep the coupled parts of one responsibility together in one coherent lane. Coupling alone does not force the Coordinator lane: that one lane may be a worker lane when the responsibility is substantial, uncertain, or noisy enough to repay the handoff.
- Frequent unresolved decisions that cross ownership boundaries count against delegation; those decisions need the Coordinator's context rather than a handoff.
- Serial delegation is valid. Complete one bounded lane, integrate its return, and dispatch the next only when it still repays the coordination cost. Parallelism is a separate decision about concurrency, not a condition for delegating.
- Servotab sets no model, budget, provider, or transport policy; the host and the work order own those choices.

Do not delegate an otherwise trivial task because a lane, an idle worker, or a coordination benefit happens to be available. A task must first have left the clear/direct path because the responsibility is substantive, uncertain, noisy, or otherwise meaningfully handoff-shaped.

## Capability and routing boundary

- The host and current instructions decide whether subagent tools exist, how much concurrency is available, and whether delegation is permitted. Servotab cannot create or override that capability.
- Select this method from task topology: independent substantial lanes, one noisy responsibility that benefits from clean context, a bounded unknown-root-cause investigation, distinct evidence questions after localization, or a genuinely useful independent review. Model or reasoning tier, idle slots, and a harness-initiated spawn are not evidence that this method was selected.
- In ordinary-language work, the implicit `servotab` router reads this reference and applies its contract. The explicit `delegate` leaf is a manual entry point; its name need not appear in the UI for the method to govern a delegation.
- If delegation is unavailable or forbidden, keep the same ownership boundaries while sequencing the work locally. State that the work stayed local; do not claim a lane or a parallel execution that did not occur.

## Responsibility model

- The **Requester** sets the objective and grants authority.
- The current user-facing agent is the **Coordinator**. It decomposes the outcome, protects boundaries, remains the integration owner, and accepts or rejects returns.
- A **Task Worker** owns one coherent engineering, research, audit, validation, or review lane and makes ordinary in-scope decisions. A worker does not delegate again; recursive delegation and delegation trees are out of contract.

These are responsibilities, not ranks. A fresh context is a clean workbench; it creates neither a new objective nor new permission. Keep the main conversation as the coordination and judgment surface rather than replacing it with a worker dashboard.

## Delegation gate

When delegation is available, use a lane when at least one brings material value:

- Two or more substantial domains can proceed independently.
- A noisy research or long-running responsibility benefits from clean context.
- A bounded unknown-root-cause investigation has a fixed failure, expected behavior, entry evidence, return contract, and verification, and clean context or Coordinator attention has material value.
- An independent review would add genuinely different evidence.
- The Coordinator's context or attention is becoming too full for clean judgment.
- Parallel work saves meaningful time without write collisions.

Keep the work in the Coordinator when it is trivial or nearly completed, easier to finish directly, or when handoff and acceptance would largely repeat the direct work. Frequent unresolved decisions that cross ownership boundaries also count against delegation; those decisions need the Coordinator's context rather than a handoff. Reversibility and a likely common cause do not prevent delegation by themselves. Keep symptoms with a likely common cause under one investigation owner; that coherent owner may be a worker when the bounded responsibility otherwise repays the handoff. Do not split one feature by file, create duplicate reviewers, or spawn workers merely because they are available.

Serial lanes need no concurrency: finish one bounded lane, then dispatch the next after its return. Use at most three concurrent Task Workers by default, and no delegation tree. One independent review lane is normally enough.

## Work-order contract

Give every Task Worker a compact order with:

- **Outcome:** the concrete result and completion condition for this lane.
- **Scope:** included files, systems, questions, and explicit exclusions.
- **Context:** the smallest canonical sources and known current facts needed to begin.
- **Authority:** allowed reads, writes, tool side effects, external actions, approval gates, and stop conditions.
- **Return:** destination, required evidence, unknowns, changed surfaces, and concise report shape.

The order must support independent judgment without hidden parent context. Delegation changes where authorized work happens, not what may happen. An instruction such as “if needed,” “if safe,” or “after approval” remains a gate. A worker that needs broader scope or authority stops the affected path and returns the exact conflict plus the smallest proposed correction.

Keep the order proportional: normally one to three bullets per field. Link canonical sources instead of restating whole plans or global rules, and include a constraint only when this lane needs it to judge or act correctly. A work order is not a second specification.

Before dispatch, the Coordinator checks that outcome, acceptance criteria, dependencies, authority, stop conditions, writer ownership, and return evidence are compatible. Ask the worker to validate that chain at entry, then make normal in-scope decisions without escalating trivia.

## Dispatch and write ownership

Reuse an active worker or session that already owns the lane. Do not create a second lane for a responsibility a live worker is already handling, and do not implement the same work in the Coordinator while a worker owns it.

Create each lane once. If creation returns an error, timeout, or ambiguous result, inspect existing agents once before retrying; an error does not prove that no worker exists.

Keep one writer for every overlapping file, branch, database, or live-state surface. For concurrent writes, use genuinely non-overlapping file and index operations, or separate worktrees with clear ownership. Different branch names in one checkout do not isolate working files or the index; a stable interface alone does not prevent write collisions. Reuse a suitable existing task workspace before creating another, and apply the Worktree method when selecting or retiring one. Read-only workers normally need no extra checkout. Worktrees still share refs and may share ports, databases, services, or output directories; allocate those resources or sequence the work. Workers do not commit, push, merge, deploy, mutate production, or change public contracts unless the order explicitly grants that action.

After confirmed dispatch, continue a non-overlapping Coordinator responsibility or wait. Do not repeatedly poll healthy workers; resume on an explicit return, a concrete delivery problem, or a user status request.

## Return packet

Require one explicit return containing:

- Outcome and completion status
- Changed or inspected surfaces
- Evidence and verification
- Unknown or unverified items
- Risks or blockers
- Recommended next action

Treat the packet as claims, not proof. The Coordinator checks source evidence, authority compliance, acceptance criteria, unknowns, and the combined diff or runtime state before integration. Resolve conflicting assumptions and run the narrowest meaningful integration check.

Do not run another worker wave by default. Dispatch again only when returned evidence reveals a new bounded responsibility whose value repays the coordination cost.
