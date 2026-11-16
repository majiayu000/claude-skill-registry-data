---
name: modernize-pr
description: Reassess an old or stale pull request against the current base branch. Use when asked whether inherited work should still be rebased, revised, replaced, or closed.
---

# Modernize a Pull Request

1. Read the original goal, current PR diff, commit history, review comments, and current base branch.
2. Compare the original assumptions and affected interfaces with the current architecture and dependencies.
3. Determine whether the goal is still valid, already solved, superseded, or no longer needed.
4. Reproduce the original behavior and inspect current tests before rebasing or rewriting.
5. Choose the smallest suitable path: keep as-is, rebase, resolve conflicts, make a focused update, replace on a new branch, or recommend closing.
6. Preserve useful author credit and historical context. Identify conflicts that require human judgment.
7. Run relevant tests and review the final diff before recommending PR state changes.

Do not rebase or force-push shared history without permission. Do not close an old PR merely because it is old. Explain the decision and remaining risks.
