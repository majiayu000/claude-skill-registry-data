---
name: codex-native-subagent-team
description: Use when the user explicitly asks for subagents, parallel agents, delegation, or a team-style split in native Codex; coordinate bounded native subagent lanes with leader-owned context, integration, verification, and Team Big Five style handoffs.
---

# Codex Native Subagent Team

Coordinate native Codex subagents safely. This skill is a recipe for explicit parallel work, not an automatic team runtime.

This adapts the useful parts of OMX `$team`, `$ultrawork`, and the Team Big Five / ATEM coordination layer as of upstream `oh-my-codex` main `f947e3a`: grounded context before delegation, independent lanes, ACK-readback handoffs, mutual monitoring, backup behavior, leader-owned integration, and evidence-first final reporting. It does not migrate tmux panes, `.omx/state`, worker mailboxes, Stop-hook continuation, `omx team api`, or automatic keyword routing.

## Use When

- The user explicitly asks for subagents, parallel agents, delegation, or a team-style split.
- Work can be split into independent lanes that materially help the main task.
- Each subtask has a clear output and, for edits, a disjoint write scope.
- The main thread can keep useful local work moving while lanes run.

## Do Not Use When

- The user has not explicitly authorized subagents or parallel delegation.
- The next local action is blocked on the delegated result.
- The task is small, sequential, or tightly coupled.
- Multiple agents would edit the same files without a clean ownership boundary.
- The task is still ambiguous enough that `$codex-deep-interview` or `$codex-consensus-plan` should run first.

## Leader Responsibilities

- Read enough context personally; do not become a blind dispatcher.
- Decide the local critical path before spawning lanes.
- Provide a grounded context snapshot to every lane: goal, relevant files, constraints, non-goals, current dirty-worktree caution, and expected evidence.
- Continue non-overlapping local work instead of immediately waiting.
- Integrate results, resolve conflicts, inspect diffs, and run verification.
- Own the final truth. Subagent completion is not task completion.

## Lane Design

Give each subagent one concrete question or implementation slice:

- goal
- scope
- allowed files/modules or read-only boundary
- expected output and evidence
- non-goals
- dependencies and handoff expectations
- cleanup expectations

Prefer read-only explorer lanes for context discovery and bounded worker lanes for disjoint edits. Omit model/reasoning overrides unless the user explicitly requested them or the task has a clear role-specific reason.

## Team Big Five / ATEM Coordination Gate

For isolated lanes, use a concise protocol: ACK, work, evidence, completion.

Activate the stronger coordination layer when there are shared files, dependencies, contracts, handoffs, integration work, blocked lanes, or changed assumptions:

- Team leadership: the main thread states priorities, ownership, and integration order.
- Mutual performance monitoring: lanes report risks, missing tests, peer impacts, and uncertainty.
- Backup behavior: if a lane blocks, the leader reassigns, narrows, or absorbs the work.
- Adaptability: update the plan when new evidence invalidates assumptions.
- Team orientation: optimize for the integrated outcome, not a locally impressive lane summary.
- Closed-loop communication: handoffs include ACK-readback of scope, affected artifact/path, owner, and next action.

## Workflow

1. State the local critical path.
2. Identify independent lanes and write boundaries.
3. Send each lane a grounded prompt.
4. Continue local non-overlapping work.
5. Poll or await results only when needed.
6. Review each returned claim against repo evidence.
7. Integrate patches or findings in the main thread.
8. Run verification proportional to risk.
9. Close unused lanes and report lane evidence.

## Delegation Template

```text
Use native subagents for these independent lanes:

Main thread:
- Own:
- Continue while lanes run:
- Do not duplicate:

Shared context:
- Goal:
- Constraints:
- Non-goals:
- Dirty worktree caution:
- Verification target:

Subagent A (<explorer|worker>):
- Goal:
- Scope:
- Files/modules:
- Output needed:
- Evidence:
- Non-goals:

Subagent B (<explorer|worker>):
- Goal:
- Scope:
- Files/modules:
- Output needed:
- Evidence:
- Non-goals:

Integration:
- Leader will reconcile results, inspect diffs, and run <verification>.
```

## Output Shape

When planning subagent work, report:

- Local critical path
- Delegated lanes
- Ownership boundaries
- Coordination gate level
- Verification plan
- Stop condition

When finishing, report:

- Main-thread changes
- Per-lane contribution and evidence
- Integration decisions
- Verification results
- Unrun checks or residual risk

## Safety Rules

- Do not use subagents as a substitute for reading relevant code yourself.
- Do not spawn multiple agents on the same unresolved write scope.
- Do not hand off destructive, credentialed, or external-production work unless the user explicitly authorized that exact action.
- Preserve unrelated dirty work.
- If a subagent result conflicts with current repo evidence, trust the repo and inspect before applying.
- Do not treat subagent completion as task completion; the leader must still verify the integrated outcome.

## References

Read `references/native-subagent-team.html` when you need concrete lane examples or prompt templates.
