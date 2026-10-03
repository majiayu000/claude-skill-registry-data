---
name: commit
description: Inspect the current trading-bot worktree, summarize the meaningful changes, propose a semantic commit message, and warn about unsafe or misleading diffs. Use when preparing a commit after runtime, operator panel, experiment, analytics, or skill-system changes.
---

# Commit

## Binding sources

- **`AGENTS.md`** — if the change touches risk/execution/AI/learning, the commit message should not imply **live** enablement or **L7** bypass.
- **`docs/FINAL_SYSTEM_VISION.md`** — large architectural commits should name affected **layers** when relevant.

## Purpose

Use this skill to convert the current worktree into a clean operator-facing summary before committing.

It should understand the current repo shape:
- runtime bot changes
- experiment and scoped-trial changes
- operator panel and autonomous research workflow changes
- skill-system and documentation-only changes
- local state, generated logs, build artifacts, and secrets that must not be committed

## Use When

Use this skill when:
- a scoped task is complete and ready for commit
- you want one clear commit message instead of a vague summary
- the diff touches risky areas such as `app/risk`, `app/execution`, `app/operator_panel.py`, `scripts`, or `.env.example`

## Do Not Use When

Do not use this skill when:
- validation has not run yet
- the worktree still contains unrelated exploratory edits
- the requested output is a review rather than a commit-oriented summary

## Required Checks

- Group changes by operational purpose, not by file list alone.
- Call out risky edits in risk, execution, operator actions, config, startup, or secrets handling.
- Verify generated files, local data, logs, `dist/`, and `.env` are not staged.
- State what validation ran and what still needs to run.
- Propose one semantic commit message that matches the actual scope.

## Expected Output

- `Change Summary:` grouped by feature or workflow.
- `Unsafe Changes:` warnings or `none`.
- `Validation Status:` exact checks run and remaining gaps.
- `Suggested Commit:` one commit message.
