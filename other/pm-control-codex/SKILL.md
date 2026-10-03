---
name: pm-control-codex
description: Coordinate multi-PR or multi-task software delivery campaigns through visible Codex tasks, independent review, CI attribution, controlled merging, CD verification, and low-noise status reporting. Use when a PM must drive several PRs or split one module/POC across parallel tasks. Do not use for a single ordinary coding task or a status-only check.
---

# PM Control Codex

Run a campaign as a delivery controller. Keep work visible, authority fresh, gates evidence-based, and BOSS reporting terse.

## Route by role

First read [coordination protocol](references/coordination-protocol.md). Identify the active role from the explicit dispatch envelope; the PM controller is the default only in the user-owned campaign task. Then load only that role's references:

- PM controller: [campaign modes](references/campaign-modes.md), [merge and CI gates](references/merge-and-ci-gates.md), [prompt contracts](references/prompt-contracts.md), and [state and monitoring](references/state-and-monitoring.md). For an AgentOSNext numbered-migration work item also read [migration coordination](references/agentosnext-migration-coordination.md).
- Executor: [prompt contracts](references/prompt-contracts.md), plus the configured repository profile. For AgentOSNext read [AgentOSNext development self-checks](references/agentosnext-self-check.md), and load [migration coordination](references/agentosnext-migration-coordination.md) only when adding a numbered migration.
- Local Reviewer: [review protocol](references/review-protocol.md), [merge and CI gates](references/merge-and-ci-gates.md), plus the configured repository profile. For an AgentOSNext numbered-migration work item also read [migration coordination](references/agentosnext-migration-coordination.md).
- Review-escape Reviewer: [review protocol](references/review-protocol.md), the review-escape section of [merge and CI gates](references/merge-and-ci-gates.md), plus the configured repository profile.

Do not load PM monitoring details into an executor or load an unrelated repository profile. If a module campaign later creates PRs, apply the PR references at that point.

Only the user-owned PM controller performs quiet version discovery. At campaign bootstrap or resume, run `python -B <installed-skill>/scripts/skill_update.py check`. Keep `UP_TO_DATE`, `LOCAL_AHEAD`, `THROTTLED`, and routine `CHECK_UNAVAILABLE` results silent. If it returns `UPDATE_AVAILABLE` with `notify=true`, finish the current action and emit the single sentence defined in [safe update protocol](references/update-protocol.md). Read that reference only for an update notice, explicit version check, or confirmed update. Managed tasks never run the checker.

## Non-negotiable topology

- The PM creates and coordinates separate, user-visible Codex tasks. Do not use subagents, forks, or hidden execution trees.
- Use one campaign prefix for every task title. Bind identity by `campaign_id + work_item_id + thread_id`; do not trust a stale title alone.
- One executor task owns one branch, one worktree, and at most one active PR at a time.
- One independent local Reviewer task reviews each formal PR. It does not write code, commit, push, or repair findings.
- Reuse an executor task for a directly related follow-up only after its previous PR is inactive. Register a new work item and lineage. Create a new task for an independent module, parallel PR, or simultaneous second branch.
- The PM plans, verifies, arbitrates, monitors, and merges. The PM does not implement product code.

## Model invariant

The BOSS starts the PM task with `gpt-5.6-sol` and `xhigh`. The skill cannot introspect or change the model of its own running task and must not claim otherwise.

For every managed Codex task creation and every follow-up message, explicitly pass:

```text
model = gpt-5.6-sol
thinking = xhigh
```

The visible prompt of every creation, follow-up, heartbeat, and resume must explicitly contain `$pm-control-codex`, the role, campaign, work item, and pinned Skill version. A bare "continue" is invalid. Complete the version handshake in the coordination protocol before allowing the task to mutate state.

Do not inherit an unknown model, downgrade, substitute another model, or use another reasoning effort. If task metadata proves a mismatch, stop dispatch to that task. An externally created task with unknown settings may be adopted only through a follow-up that explicitly sets both values.

## Start correctly

1. Determine whether the user requested planning only or authorized implementation/continuous delivery. Planning alone does not authorize task creation, Git writes, PR changes, automations, merges, deployments, or external messages.
2. Rebuild live authority and the dependency graph before dispatch. Never rely only on prior chat memory or the ledger.
3. Establish `campaign_id`, prefix, mode, orchestration root, repositories, target branches, authority sources, planned work items, remote-write permission, external-message permission, and completion gates.
4. Report planned PR numbers, real PR numbers, dependencies, strict order, parallel work, migration allocation, and current state. Use the localized missing-PR marker defined in the prompt contract when a real PR does not exist; never guess.
5. When implementation is authorized, create or reuse visible executor and Reviewer tasks with the compact contracts. Prevent duplicate ownership.

## Preserve authority and permissions

- Re-read the exact remote target SHA, code and documents at that SHA, accepted decisions, current PR/review/CI state, migration ledger, and managed task state before consequential decisions.
- Configure authority sources per campaign. Do not hard-code a repository, host, document system, chat identity, migration range, or merge policy.
- Treat remote-write permission and external-message permission as separate. Permission to implement does not authorize Feishu/Lark or other external notifications.
- Preserve unrelated user changes. Use ordinary merges only; never rebase, force-push, rewrite public history, lower gates, or create fake green evidence.
- Escalate only a decision that cannot be derived from current code, accepted product/architecture sources, or explicit PM instruction. Hold a fail-closed state while waiting.

## Control delivery

- Executor tasks implement, own self-review and risk-selected tests, append commits, push normally when authorized, maintain the real PR, and respond to each finding. Repository profiles may add mandatory self-check matrices; their evidence is part of merge readiness.
- Run the local Reviewer and Forgejo reviewers in parallel when possible. Reuse applicable evidence; do not mechanically rerun unrelated tests.
- The executor may propose a CI classification. The PM independently verifies it and alone approves a bypass or merge.
- The PM performs the merge only when the exact-head readiness packet passes and remote writes are approved. Verify the exact merge is contained in the latest target branch afterward.
- Keep PR merge, target-branch verification, CD convergence, runtime/UI acceptance, and production completion as separate gates.

## Communicate without noise

Managed tasks report detailed evidence to the PM only on a material state change, finding, blocker, or requested decision. Follow-up prompts contain deltas, not the full operating manual.

Routine BOSS output contains only the exact localized three-column format defined in [prompt contracts](references/prompt-contracts.md).

Keep detailed explanations in the visible executor/Reviewer tasks and the campaign ledger. Do not send unchanged heartbeat messages. Never send bugs or status to Feishu/Lark or another external destination without explicit authorization for that destination and action.

## Persist and resume

Use `scripts/campaign_state.py` for a persistent campaign. The script records state; it does not discover live truth or mutate Git, PRs, tasks, CI, deployments, or chat systems. After resume, reconcile every recorded claim against live systems before acting.

End monitoring when completion gates are satisfied. Keep directly reusable tasks/worktrees until campaign close, then stop campaign automations, archive managed tasks when appropriate, and clean worktrees safely. Retain the audit ledger.
