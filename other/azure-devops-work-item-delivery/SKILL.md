---
name: azure-devops-work-item-delivery
description: Coordinate Azure DevOps Work Items through isolated worktrees, a shared understanding and design preflight with docs drafted by workers and asked by the coordinator, implementation, local reviews, PR publication, approved merge, and local cleanup. Use when the user requests this full delivery workflow for named Work Items; resume unfinished deliveries without repeating completed operations.
---

# Azure DevOps Work Item Delivery

Deliver each requested Work Item by composing the existing skills. Keep their
operational details and approval rules in those skills. IDs in examples or a
discussion about this skill are not work orders.

```text
Claude Code: /azure-devops-work-item-delivery 123 456
Codex:       $azure-devops-work-item-delivery 123 456
```

## Scope and Authorization

Use the current repository's Azure Boards Work Items and Azure Repos Git PRs on
Azure DevOps Services. Read `../azure-devops-common/references/context.md` before
resolving the target. Azure Boards with GitHub repositories and Azure DevOps
Server need a different workflow; report that boundary rather than choosing an
Azure Repos target for them.

Read component skills before their phases and call them under
[Delegated Authorization](../delivery-common/SKILL.md#delegated-authorization);
the exact target is the Work Item, branch, and worktree. An explicit full
delivery request selects the delegated shared understanding, preflight, local
review, and publication phases. Automatic discovery or a reference to this
skill selects none of them. Honor the publisher's approval model and governing
instructions for scoped checkpoint commits, normal pushes, and PR creation.
Prepare the concrete result before requesting missing approval.

Require explicit confirmation for the specific PR merge and the exact local
cleanup resources, combined only where Delivery Completion's Merge confirmation
allows. Work Item state transitions follow
[Work Item Links And State Transitions](../azure-devops-common/references/context.md#work-item-links-and-state-transitions);
include any proposed transitions in the merge confirmation. Preserve dependency,
history-rewrite, remote-write, and user-change protections. This workflow ends
its publication phase at the PR; it has no hosted AI review request or follow-up
cycle.

## Prepare and Coordinate

1. Resolve the requested IDs, organization, project, repository, instructions,
   dirty state, and matching worktrees/PRs. Require at least one actual Work
   Item. Check component skills and the local reviewers, including
   `change-security-review`, before starting. The normal installation is
   `base,azure-devops`; a missing one stops under
   [Missing Prerequisites](../delivery-common/SKILL.md#missing-prerequisites).
2. Use `azure-devops-work-item-start` with the per-item workflow below as its
   implementation brief, under
   [Worker Dialogue](../delivery-common/references/worker-dialogue.md)'s Assign
   the worker.
3. Follow Worker Dialogue for each item's shared understanding and preflight.
4. Keep a progress record per item under
   [Delivery Completion](../delivery-common/references/completion.md), adding
   the organization, project and repository IDs, the PR ID and source/target
   refs, the policy and merge state, and the Work Item state.

On resume, follow Delivery Completion's Resume with Azure DevOps state. Stop
and report the recorded branch unless it is a **safe branch name** before
running any command with it: run `node <script> -- '<branch>'`, where `<script>`
is [`check-branch-name.mjs`](../delivery-common/scripts/check-branch-name.mjs)
resolved from this skill's directory, and continue only on exit 0. Write a name
into this or any command only when it uses solely ASCII letters, digits, `/`,
`.`, `_`, and `-`; any other name is not safe, without running the check.

## Per-Work-Item Workflow

### 1. Preflight, implement, and verify

Use `design-preflight-with-docs` for this item, drafted by the worker and asked
by the coordinator under Worker Dialogue, then implement and verify under its
[Preflight and implementation](../delivery-common/references/worker-dialogue.md#preflight-and-implementation).

### 2. Run local reviews, assess, and repeat

Run the local reviews the
[Risk Tier](../delivery-common/references/risk-tier.md#tier-procedure) selects
under [Local Review](../delivery-common/references/local-review.md): the initial
full review, Assess findings, and Repeat and advance.

### 3. Publish the PR

Coordinate publication and show the decision summary under Delivery
Completion's Before publication.
Use `azure-devops-pr-publish` and honor its stop-on-failure behavior. Supply
known Work Item IDs, completion scope, and the user's state-transition intent.

Verify the returned PR's repository, source/target refs, and Work Item links.
Read the current remote source ref and compare its commit with the local
reviewed HEAD under Delivery Completion's
[After publication](../delivery-common/references/completion.md#after-publication),
and advance under it, adding that the PR has the intended Work Item links.

### 4. Confirm and perform the merge

Follow [Merge and Work Item State](references/merge-and-state.md) to check the
current source/target, required policies/CI, human approvals, discussion threads,
and mergeability. Keep source-HEAD concurrency limits explicit.

Check and present the merge under Delivery Completion's Merge confirmation,
adding the required policies and the proposed state-transition scope. When it
combines the confirmations, use `azure-devops-worktree-cleanup`'s caller preview
for the cleanup targets. Complete the PR as that reference describes.

### 5. Confirm cleanup and verify completion

After verifying actual PR completion and the merged source/merge commit, use
`azure-devops-worktree-cleanup` for the exact item branch/worktree. Pass merge
evidence and let it inspect runtimes, show exact resources including any remote
branch it proposes, obtain separate confirmation unless Delivery Completion's
Merge confirmation combined it, and perform its safety checks.
Preserve dirty, busy, or otherwise unsafe resources and report the blocker.

Verify that confirmed local targets are gone. Read the Work Item's actual state
and verify completion under its process; PR completion does not prove Work Item
completion. Follow the reference for pending transitions. Report open Work Item
completion or cleanup as unfinished; do not silently update, assign, tag, or
comment on the Work Item.

## Bounds and Handoffs

Apply Delivery Completion's Bounds; this workflow runs no hosted AI review
rounds.

Check policies when reaching merge or resuming; avoid indefinite polling. If the
user asks to wait, use a bounded window and report its limit; otherwise report
`Waiting for review/CI`. A verification, commit, push, or PR failure is a
publication failure.

Report each item, mark it `Complete`, and list follow-up candidates under
Delivery Completion, adding the state `Merged; Work Item completion pending`.
Task closure is the Work Item's verified completion under its process, and the
create skill is `azure-devops-work-item-create`.
