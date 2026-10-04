---
name: implement-issue
description: Implement one GitHub Issue using the repository's established development workflow.
argument-hint: "[issue-number]"
disable-model-invocation: true
---

Implement GitHub Issue $0.

1. Read `AGENTS.md`, then read the Issue and its acceptance criteria.
2. Inspect the current worktree and preserve unrelated user changes.
3. Inspect only the code and documentation needed for this Issue.
4. Create or reuse the Issue's primary working branch; never work directly on `main`.
5. Implement the smallest change that fully satisfies the Issue and existing contracts.
6. Add or update focused tests for concrete changed behavior.
7. Run focused tests plus the deterministic checks required by `AGENTS.md`. Do not run the full suite locally unless there is a concrete reason.
8. Self-review the branch diff against the Issue, repository boundaries, and `AGENTS.md`.
9. Commit and push the Issue branch.
10. Create or update the PR. Use `Closes #N` only if this PR completes the whole Issue; otherwise use `Refs #N`.
11. Make the PR Ready for review when appropriate. Do not merge it.

At completion, report the branch, head commit, PR, checks run, anything not verified, and remaining blockers.
