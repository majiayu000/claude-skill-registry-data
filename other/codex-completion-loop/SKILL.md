---
name: codex-completion-loop
description: Use when the user wants Codex to carry a task through implementation, verification, cleanup, and final evidence instead of stopping at a partial fix; native Codex completion loop inspired by Ralph/Ultrawork/Ultragoal.
---

# Codex Completion Loop

Drive the task to a real stopping point: implemented, verified, cleaned up, and explained with evidence.

This is the native Codex adaptation of OMX `$ralph` plus the reusable parts of `$ultrawork` and `$ultragoal` as of upstream `oh-my-codex` main `f947e3a`: keep persistence, outcome-first framing, evidence lanes, completion audits, goal honesty, and cleanup; replace OMX mode state, tmux panes, `.omx/ultragoal` ledgers, and Stop-hook continuation with native Codex tools and repo-local work traces when needed.

## Completion Contract

At intake, state:

- Outcome: what must be true at the end.
- Scope: what files, artifacts, or workflows are in play.
- Evidence: the minimum commands, screenshots, rendered files, diffs, or source checks that can prove completion.
- Stop conditions: real blockers, user cancellation, or verified completion.

If the task is too ambiguous to define done, first run a short `$codex-deep-interview` style pass.

## Loop

1. Inspect enough context to avoid blind edits.
2. Preserve user work: never revert unrelated changes; isolate touched files in dirty worktrees.
3. Make focused changes.
4. Run the smallest meaningful verification.
5. Diagnose failures and retry with bounded fixes.
6. Add broader verification when the blast radius, shared contracts, or user-facing output requires it.
7. Clean up temporary harnesses, logs, dev servers, or generated debris unless they are intentional artifacts.
8. Finalize only after a prompt-to-artifact audit passes.

## Evidence Lanes

Use direct tool work for the critical path. Add background evidence lanes only when they can run independently and materially improve confidence, such as docs lookup, regression mapping, rendered-output inspection, or test discovery. Use `$codex-native-subagent-team` only for explicit native subagent coordination.

For visual/UI/PDF output, evidence must include screenshot/render inspection through `$codex-visual-acceptance` or equivalent browser/PDF checks.

For long-running or reportable work in a repo with task/work-trace rules, write progress and final evidence to the repo's source-of-truth files.

## Goal Mode

When goal tools are active:

- Use `get_goal` to keep the objective in view.
- Call `create_goal` only when the user/system explicitly requested a new goal and no active goal exists.
- Call `update_goal({status:"complete"})` only after the completion audit proves the objective is actually achieved.
- Do not treat passing tests, a plan, a subagent result, or a partially updated ledger as proof of goal completion unless it covers the whole user objective.

## Completion Audit

Before final answer, map every user requirement and named workflow gate to evidence:

- changed files or generated artifacts
- commands and results
- rendered screenshots/PDF pages when relevant
- source parity/hash checks when syncing
- task-state or work-trace writeback when required
- unrun checks and why they were not run
- residual risk and next owner if any

## Failure Handling

- If a command fails, inspect the error and try a bounded fix.
- If output is misleading, contradictory, or stale, treat that as a failure scenario and verify through another route.
- If credentials, missing data, unavailable services, or a repeated blocker prevents completion, preserve useful intermediate work and report diagnosis, evidence, and next action.
- Do not invent successful verification.

## References

Read `references/completion-evidence.html` when deciding what evidence is enough for code, paper, figure, or workflow tasks.
