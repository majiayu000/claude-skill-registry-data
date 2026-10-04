---
name: worker-routing
description: Decide and execute native Codex worker delegation for the main coordinating agent. Use it for a substantial investigation, implementation, fix, or verification responsibility that can be handed over whole, and for continuing or reworking the same worker; a temporary worker, an explicit solo request, casual explanation, or tiny or nearly finished work does not trigger another delegation.
---

# Worker routing

This skill decides only who executes a block of work, and how that work is taken back. The current task, the repository contract, the engineering methods already in force, and real permissions remain the complete contract; do not open a second plan, acceptance, or reporting system, and do not modify Servotab, Oracle, or model configuration.

## Identify the role first

If you are a temporary worker that received a work order, read and follow [worker-role.md](references/worker-role.md), then complete the order; do not route again.

If you are the main coordinating agent, you always own the complete result the user accepted, its integration, and final delivery, and you keep the current main model. Reuse the goals, constraints, evidence, and worker state the current task has already established. `全权接住` and `从头做到位` allow internal delegation; when the user explicitly asks for `solo`, `亲自做`, `别派小弟`, or an end to internal delegation, stay on the main thread; if a writer already exists, first let it stop or wind down safely through whatever the host supports, then take over. Stopping progress monitoring does not cancel a worker.

After context loss or compaction, recover the responsibility, the child or thread identifier, and the existing evidence from the task record and native state you already have before deciding whether to create anything new. Missing memory does not mean an earlier worker no longer exists, and a new tracker does not replace that recovery.

## Delegate only when handing over a whole responsibility reduces main-thread work

Make one short judgement before heavy execution starts. Investigate far enough to state the goal, the key constraints, entry-point clues, and the acceptance evidence; do not write a per-function implementation plan just to delegate.

Protect the complete outcome, its quality, and the applicable permissions first. On that basis, prefer reducing execution consumption on the main subscription while keeping end-to-end duration and coordinator rework under control. Use an operator-specified, authorized route that reduces main-subscription quota consumption when it fits the responsibility. Do not delegate for the sake of delegating when no known benefit exists. Account for external worker API spend separately, and never silently fall back to a higher-cost route. Keep model and provider names in operator-owned configuration: no leaderboards, price lookups, evaluation matrices, or brand hardcoding.

Use the operator's current default when it fits. One configured worker is a complete setup; do not compare a catalog on every handoff or require capability biographies. A route means the actual authorized model, channel and execution environment, not just a model name. Consider another authorized route only for a concrete capability, quality or availability reason. An optional short experience note can inform that exception; do not invent specialties or split a coherent responsibility into specialist stages.

Keep changing preferences in the operator's existing local source, outside Git. Record a requested channel change there once, within the user's authority; do not duplicate it in this skill, plugin cache and SessionStart text. For configured ACP defaults, the normal run resolves the current choice itself; do not add a mandatory lookup or pin a stale `--route` from earlier context. Native workers keep their host tools and authorized local selection. Changing the default affects new responsibilities. Revoking a route also forbids subsequent continuation on it; coordinate an active writer's stop and preserve its work before takeover. A preference change alone must not rebind an existing session.

Fallback requires prior authorization for the actual route, task data and cost; registration or past use is not permission. Reuse a confirmed availability failure within the current task while its conditions remain unchanged. Before launch, use an authorized available alternative; after launch or ambiguous submission, recover the original execution and confirm it has stopped before handing over remaining work. Permission denials cannot be bypassed by changing routes. A quality failure follows same-worker rework. Without an authorized alternative, finish directly when the task permits it; ask only when an external-worker-only requirement or another real authority boundary prevents progress. No subscription calendar, recurring health probe or automatic provider-error diagnosis is required.

A suitable delegation is one coherent responsibility, such as a local investigation plus implementation, self-testing, and the necessary documentation. Tight internal coupling can sit with a single worker as a whole; use serial delegation by default. Parallelize only when the responsibilities and the shared write surface are genuinely independent. Finish the work directly when the change is tiny, the answer is nearly complete, handing over would amount to redoing it yourself, product semantics need continuous decisions from the main coordinating agent, or acceptance costs more than the execution gains.

Use the worker, agent role, model, and reasoning inventory the host offers live and has already authorized; do not bind to brands or model names, and do not infer a real route from a menu, configuration, or role name. Stay solo while no applicable worker is confirmed. `worker-role` is task semantics, not an OS sandbox, network isolation, or a permission system.

## Let go after the handoff

Read [handoff.md](references/handoff.md) and hand over a responsibility a worker can start on independently. A new independent work order explicitly uses `fork_turns='none'` on the current host by default, but that value controls only that API's conversation-fork choice; it does not prove that global or project instructions, skills, tools, or other host-attached context were isolated. With a third-party provider, no unauthorized private or account data transfer may be trial-run just to verify routing.

Read [context-boundary.md](references/context-boundary.md) and confirm the actual input boundary; do not assume from an old main session that private instructions were excluded.

The work order must state the temporary worker's role semantics, allowed write surface, shared resources, and permission boundaries. Every step authorized downstream comes from the current task; documentation, test results, tool availability, or upstream authorization cannot be used to derive new permission to commit, push, deploy, perform account operations, make paid calls, or transfer private data.

Once the worker has started, keep its real child or thread identifier. The main thread stops same-source investigation and any second version of the implementation; it may advance non-overlapping work, handle genuine coordination decisions, or wait. Keep one writer per overlapping file and per shared runtime state; a worktree does not automatically isolate ports, databases, services, or output directories.

When you use the collaboration tools, read [native-tools.md](references/native-tools.md). Waiting uses the host's blocking wait and completion messages: query the worker only to recover it, to resolve an ambiguous state, or when intervention is needed, and do not short-poll a healthy worker. A health-wait timeout, an active yield, or silence on the current host is not failure, and none of them justifies interrupting the worker or duplicating the same responsibility.

When a reference is already read and unchanged in the current context, do not read it again; re-read it after context loss or when its trigger materially changes. Reuse valid route and input-boundary evidence while the relevant host, configuration, and injection conditions are unchanged, and refresh only the affected part when a condition changes or evidence contradicts the earlier conclusion. Routine delegation does not run native probes, search model catalogs, run health checks, or request private transfers.

## Continuation, rework, and acceptance

When an active worker receives a new constraint that affects its work, send the increment promptly; do not wait for it to return under the old contract and then reject the result. When the same responsibility moves from a read-only investigation to authorized implementation, needs missing evidence, or requires local rework, prefer continuing the same worker and its evidence. Aggregate feedback around the actual failure, the expectation, and the scope, and preserve accepted artifacts; do not create a new worker for a phase name, and continue or rework through the existing child rather than starting a fresh one.

After a worker returns, the main coordinating agent checks the real diff, the key invariants, the permission scope, and the verification coverage. The main thread does not repeat the whole investigation or rewrite a qualified implementation to personal preference. Evidence from the final relevant code in the same environment can be reused; after the relevant code, dependencies, or runtime state change, add only the affected fresh check. Do not spawn a separate reviewer by default, and do not trigger Oracle for an ordinary return.

Re-divide or withdraw the responsibility when the same class of failure repeats without new evidence, when the task premise no longer holds, when permissions conflict, or when the original worker cannot recover. Before taking over or switching workers, confirm the old writer has stopped and preserve still-usable changes and evidence.

Report only results, material decisions, real blockers, and the evidence sufficient to support the conclusion. Do not routinely narrate routing steps, generate a standardized delegation report, or claim a savings ratio that was never actually measured.
