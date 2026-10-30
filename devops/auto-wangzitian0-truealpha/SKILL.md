---
name: auto
description: Step 5 of the five-step flow. Drive a verified change to a merge on main with no owner prompts. Orchestrates review, gate, and merge. Stops at production.
---

# auto: deliver to main

Run this after `smoke` passes. Use `prr` for the review and gate mechanics.

## Definition of Stage 1 (Code Landed)

**Merge to main is Stage 1 (Code Landed), not task completion.** Landing on main is a physical prerequisite for Stage 2 (Staging) and Stage 3 (Prod). Task completion requires both code landing and physical reality verification (`ws-delivery-status --assert-complete`).

- Merge only through a PR. The owner grants merge authority when every gate passes.
- Merge when ready. Then continue from the latest main. Do not pile up divergent branches.

## Loop

1. Open the PR. An edit to merge-gate code, data or tests, to a required-check workflow, or to release code needs the independent review of the production reservation. Record it on the PR.
2. Run the `prr` gate. Fix each finding in the issue worktree. Do not touch unrelated files.
3. Run focused checks on every fix. Read the decision from the gate exit code. `ws-pr-gate` returns only exit 0, 1, 3 or 4; infra2's `pr_merge_gate` also returns 2.
   - Exit 0: Merge with `ws-pr-gate --merge`. It picks `--rebase`, `--merge` or `--squash` from the branch and the repository settings, and passes `--match-head-commit` with the verified head.
   - Exit 1 (Wait): End the turn. A `ci-monitor-event` or a background re-run of the gate wakes you; never poll in the foreground. If checks remain pending 45 minutes after they started, transition to `Suspend`, record the CI snapshot in the issue, and report `In review`. Do not spin indefinitely.
   - Exit 2 (Held): infra2's `pr_merge_gate` returns it for its review set (infra2 rule 4). A production change waits for the owner: report it and ask once. For any other hold, get the independent review. Merge only when the hold is the only reason in the verdict. The checks must be green on the same head (`gh pr merge --match-head-commit <sha>`). A gate that holds a non-production PR is a defect: open an issue for it.
   - Exit 3 (Action required): Resolve findings or fix conflicts, push, and re-run. If unresolved after two rounds, escalate to Senior or Suspend.
   - Exit 4 (Could not evaluate): The gate could not read a fact (gh, git, the PR head, or ws-publish). It is never a pass and never a wait. Fix the cause in `reasons[]`, then re-run. Do not merge.
4. Fix and merge every non-production change without a question to the owner.
5. Merge. Verify with `ws-delivery-status` that the commit is merged on `origin/main` (exit 0, `CODE_LANDED_STAGE1`).
   Transition to Reality Probe or deployment verification before declaring task complete.
6. When the delivery required rework (CI retry, gate rejection, or more than one review round), execute the post-delivery retrospective checks before closing the delivery.

## Post-delivery retrospective (Conditional Retrospective Swarm: M=3)

On a clean first-pass delivery (zero CI failures, zero gate rejections, at most one review round), skip the swarm and proceed directly to `ws-delivery-status` and `close`. When rework occurred, dispatch 1 Retrospective Swarm (M=3 Interns via `subagent_batch`) before concluding the delivery:

1. **Intern 1: Recurring mistake and harness constraint check**:
   - Check if any review comment, gate rejection, or CI retry occurred during this delivery.
   - If an error occurred, identify the mechanical guard (pre-commit check, linter, or local gate assertion) that catches it locally in under one second.
   - Do not resolve a problem only through repeated human or agent rework. Convert the lesson into a physical check or register an issue to reinforce harness constraints.

2. **Intern 2: Harness loading and context footprint audit**:
   - Inspect the size of always-loaded rules (`AGENTS.md`) and projected files.
   - Verify that always-loaded rules contain only decision invariants (boundaries, prohibitions, thresholds).
   - Verify that prompt context contains no duplicate clauses between host rules and repository projections.
   - Move operational instructions, historical incident narratives, and procedures to on-demand skills or SSOT documents.

3. **Intern 3: Delivery pipeline telemetry and acceleration**:
   - Record the runtime of each delivery phase: local tests, gate evaluation, and remote CI jobs.
   - Flag any remote CI job that exceeds 60 seconds (such as un-cached Docker builds or slow test shards).
   - Identify whether the slow job can be short-circuited by file path filters or accelerated with dependency caching.

## When to stop

Only the production reservation returns a decision to the owner (Root section `Production reservation`). Merge is not deploy. After the merge, report the merge SHA, the staging evidence and the production state. Then ask the owner once for "deploy" or "hold" on that production release.

Stop the action, but do not ask the owner, in two cases:

- **Another worker's issue lock**: an issue-prefixed worktree, an open PR, or a running process. Coordinate through the issue.
- **An irreversible step outside production**: for example a data deletion in a test or staging store. Find a reversible path first. A production deletion and a release that cannot be recalled are production changes.

A large impact or an unclear preference is not a stop reason. Choose, state the basis, and keep a way back.

Gate code, gate data and tests, required-check workflows and release code are the agent's. Merge them after the independent read-only review that the reservation requires. A gate exit code, a label or a rule that holds a non-production PR for the owner is a defect. Merge the PR after the review, then fix the gate or the text.

## Report rules

- State the root cause before you ask for a production decision.
- Do only what was asked; do not bundle unrequested changes.
- Keep committed text free of private names, internal hosts, and local paths so it is safe for public issues.
- Keep descriptions short, factual, and in ASD-STE100 style.
