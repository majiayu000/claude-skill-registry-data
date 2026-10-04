---
name: autoresearch-goal
description: Use when a research mission should be managed as a Codex goal with professor/critic-style validation, durable repo-local mission/rubric/ledger/completion artifacts, and explicit goal completion audit; native adaptation with no dependency on OMX CLI, .omx goal state, tmux, hooks, or shell handoffs.
---

# Autoresearch Goal

Bind a research mission to Codex goal-mode focus, then complete it only after professor/critic-style validation passes.

This is a native Codex adaptation of OMX `$autoresearch-goal`: keep mission/rubric/ledger/completion discipline and safe goal handoffs; replace OMX CLI, `.omx/goals`, hooks, and shell reconciliation with Codex goal tools plus repo-local artifacts.

## Use When

- The research is substantial enough to deserve goal-mode focus.
- The user wants iterative research against a rubric, not a one-off answer.
- A critic, professor persona, evaluator, or review rubric must approve the result.
- The work may span several passes and needs durable evidence.

Use `$autoresearch` instead when the task needs a validator-gated deliverable but not Codex goal-mode management.

## Required Artifacts

Use the repo's existing convention. If none exists, prefer:

```text
reports/autoresearch-goals/<slug>/mission.json
reports/autoresearch-goals/<slug>/rubric.md
reports/autoresearch-goals/<slug>/ledger.jsonl
reports/autoresearch-goals/<slug>/completion.json
```

Artifact meanings:

- `mission.json`: objective, scope, non-goals, source boundaries, deliverable path.
- `rubric.md`: professor/critic criteria and pass/fail rules.
- `ledger.jsonl`: append-only attempts, source batches, critic verdicts, blockers, steering decisions.
- `completion.json`: final status, critic verdict, deliverable path, evidence summary, residual risks, goal snapshot when available.

## Goal Tool Rules

- Call `get_goal` when goal tools are available to understand active objective state.
- Call `create_goal` only when the user/system explicitly requested goal tracking and no active goal exists.
- Never create a new goal over a different active goal.
- Call `update_goal({status:"complete"})` only after critic validation passes and the completion audit proves no required work remains.
- If goal tools are unavailable, continue with repo-local artifacts and state that goal-tool evidence was unavailable.

## Flow

1. Confirm mission, rubric, deliverable path, and artifact directory.
2. Initialize or update mission/rubric/ledger/completion artifacts.
3. Start or reconcile Codex goal state if appropriate.
4. Research iteratively against the rubric.
5. Record every source batch, decision, failure, and critic verdict in the ledger.
6. When a critic verdict is `fail` or `blocked`, revise or report the blocker.
7. When verdict is `pass`, run a completion audit:
   - mission satisfied,
   - rubric criteria met,
   - deliverable exists,
   - evidence ledger sufficient,
   - residual risk explicit,
   - goal state updated only if appropriate.
8. Write `completion.json` and final response with evidence.

## Completion Gate

Assistant prose, partial source notes, or a failed/blocked critic verdict are not sufficient. Completion requires:

- `completion.json` with `status:"passed"` or equivalent,
- critic/professor approval evidence,
- deliverable path,
- ledger path,
- residual-risk statement,
- Codex goal completion only after the above is true.

## Output Shape

- Mission and goal status
- Artifact paths
- Research iterations
- Critic verdict
- Completion audit
- Final deliverable
- Residual risk / next action

## References

Read `references/native-autoresearch-goal-checklist.html` for the artifact and goal completion checklist.
