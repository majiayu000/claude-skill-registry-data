---
name: github-issue-delivery
description: Coordinate GitHub issues through isolated worktrees, a shared understanding and design preflight with docs drafted by workers and asked by the coordinator, implementation, local reviews, PR Codex review and fixes, approved merge, and local cleanup. Use when the user requests this full delivery workflow for one or more issues; resume unfinished deliveries without repeating completed operations.
---

# GitHub Issue Delivery

Deliver each requested issue through the following workflow. Compose the existing
skills; keep their operational details and approval rules in those skills.
Issue numbers in an example or a discussion about this skill are not work orders.

```text
Claude Code: /github-issue-delivery 12 36 56 60
Codex:       $github-issue-delivery 12 36 56 60
```

## Scope and Authorization

Use the current repository and explicitly requested issues. Read the component
skills before their phases and call them under
[Delegated Authorization](../delivery-common/SKILL.md#delegated-authorization);
the exact target is the issue, branch, and worktree. An explicit user request
for this full workflow selects its delegated shared understanding, preflight,
local review, and PR-cycle phases; their instructions recognize this caller.
Automatic discovery or a reference to this file does not select those phases.
If authorization is missing, prepare the concrete result and request only the
approval needed for the next operation.

The workflow includes the selected local review passes and the normal publication,
Codex review, and writeback cycle. It requires explicit confirmation for the
specific PR merge and for the exact local cleanup resources, combined only where
Delivery Completion's Merge confirmation allows. Preserve all
applicable dependency, history-rewrite, remote-write, and user-change protections.

## Prepare and Coordinate

1. Resolve issue numbers, repository instructions, dirty state, and existing
   worktrees/PRs. Require at least one actual issue target. Check that the
   component skills and the local reviewers, including `change-security-review`,
   are available. The normal installation is `base,github`; the GitHub profile
   alone does not supply the preflight and review skills. A missing one stops
   under [Missing Prerequisites](../delivery-common/SKILL.md#missing-prerequisites).
2. Use `github-issue-start` with the per-issue workflow below as its
   implementation brief, under
   [Worker Dialogue](../delivery-common/references/worker-dialogue.md)'s Assign
   the worker.
3. Follow Worker Dialogue for each issue's shared understanding and preflight.
4. Keep a progress record per issue under
   [Delivery Completion](../delivery-common/references/completion.md), adding
   the hosted review round count and the PR trigger and thread identifiers.

On resume, follow Delivery Completion's Resume with GitHub state. Stop and
report the recorded branch unless it is a **safe branch name** before running
any command with it: run `node <script> -- '<branch>'`, where `<script>` is
[`check-branch-name.mjs`](../delivery-common/scripts/check-branch-name.mjs)
resolved from this skill's directory, and continue only on exit 0. Write a name
into this or any command only when it uses solely ASCII letters, digits, `/`,
`.`, `_`, and `-`; any other name is not safe, without running the check.
Preserve successful writebacks. Pass the PR/head/trigger record to the cycle and
resume its earliest incomplete phase. A pending review on the same head resumes
waiting rather than posting another trigger.

## Per-Issue Workflow

### 1. Preflight, implement, and verify

Use `design-preflight-with-docs` for this issue, drafted by the worker and asked
by the coordinator under Worker Dialogue, then implement and verify under its
[Preflight and implementation](../delivery-common/references/worker-dialogue.md#preflight-and-implementation).

### 2. Run local reviews and verify fixes

Run the local reviews the
[Risk Tier](../delivery-common/references/risk-tier.md#tier-procedure) selects
under [Local Review](../delivery-common/references/local-review.md): the initial
full review, Assess findings, and Repeat and advance.

### 3. Publish and complete hosted Codex review

Coordinate publication and show the decision summary under Delivery
Completion's Before publication.
Use `github-pr-codex-review-cycle` for the exact issue branch/worktree. Honor its
publication approval model, actual-review completion criteria, Prepare -> publish
-> confirm remote head -> Writeback ordering, and stop-on-failure behavior; its
remote head confirmation is the check under Delivery Completion's
[After publication](../delivery-common/references/completion.md#after-publication).
Pass the earlier local and hosted dispositions from the progress record, and
have its follow-up assess hosted findings with Local Review's Assess findings.

After the cycle returns, record its Final Report's Not applied items in the
progress record and add their self-closures to the list under Local Review's
Assess findings. On resume, for each recorded hosted round, recover any
disposition missing from the progress record from the PR's review threads,
including resolved ones, before advancing, and add its self-closures to the
list; report history that cannot be recovered as a blocker to a complete
decision summary. Record the returned status, PR, published head, reviewed head,
dispositions, and unresolved items.

If hosted follow-up changed the implementation, return to the local review phase
for focused follow-up or a full review under Local Review's Repeat and advance.
Within the hosted rounds the Risk Tier's Tier procedure sets, obtain a fresh
hosted Codex review when the delta from the last hosted-reviewed head to the
published head contains a material change under Local Review's Triage, whether
it came from hosted or local follow-up; when uncertain, request it. Otherwise,
local focused follow-up covering the new head is sufficient; record the head the
hosted review covered and why the remaining delta did not need another hosted
round. To request another review,
reuse the existing PR and call the cycle again for that target; it does not
request another review automatically. Advance under Delivery Completion's After
publication, adding that the published head has completed hosted review or the
recorded non-material delta above, worthwhile fixes are verified and published,
and remaining thread dispositions clearly close them.

### 4. Confirm and perform the merge

Check and present the merge under Delivery Completion's Merge confirmation,
adding the hosted review outcome and its remaining review threads. When it
combines the confirmations, use `github-worktree-cleanup`'s caller preview for
the cleanup targets. After approval, merge through the available GitHub tool or
CLI.

### 5. Confirm cleanup and verify completion

Use `github-worktree-cleanup` for this issue's branch and worktree. Pass the
verified merge evidence. Let it inspect runtime resources, show exact
targets including any remote branch it proposes, obtain confirmation, and
perform its safety checks. Pass a combined confirmation only as Delivery
Completion's Merge confirmation allows; otherwise a merge confirmation alone
does not approve cleanup. Preserve a dirty, busy, or otherwise unsafe
worktree and report the blocker.

Verify the PR is merged and the confirmed local targets are gone. Read the issue
state and report whether it actually closed; do not silently close, label, or
comment on it. An open issue or unfinished cleanup remains an open item rather
than a fully completed issue delivery.

## Bounds and Handoffs

Hosted-fix follow-ups use the same local review budget.
Hosted Codex review rounds per issue follow the Risk Tier's Tier procedure
across this delivery, including resumes. A hosted round requires actual output. Apply
Delivery Completion's Bounds, adding a hosted limit reached with required work
remaining as a stop condition. At a hosted limit, include the remaining-findings
classification from Local Review's Assess findings. Ask before extending the
hosted budget or retrying a timed-out external review; do not repeatedly post
triggers.

Use the cycle's bounded waiting rules. A cycle failure is a publication failure.

Report each issue, mark it `Complete`, and list follow-up candidates under
Delivery Completion. Task closure is the issue's actual closed state, and the
create skill is `github-issue-create`.
