---
name: review
description: Review procedure for task PRs — deterministic tool output first, LLM judgment second, verdict on the board. Use when reviewing a task's pull request or when asked for a task-agent review.
---

# Review

Review one draft PR produced by the task workflow. Output: PR comments plus a
single verdict. Reviewers never push fixes — they report.

## Order matters: tools before opinions

1. **Gather deterministic signal first** (in the PR's worktree or a fresh checkout
   of the branch):
   - `vendor/bin/pint --test` — style
   - `vendor/bin/phpstan analyse` — types/bugs (if installed)
   - `php artisan test` — behavior
   - `gh pr diff <number>` — the actual change
   Any gate failure is an automatic fail verdict; report the output, done.
2. **LLM review only for what tools can't catch**, anchored to diff lines:
   - does the change do what the task + approved plan say, nothing more?
   - missing test cases for the changed behavior (not style preferences)
   - security at trust boundaries: validation, authorization, mass assignment,
     query injection
   - N+1 queries, unbounded queries, missing indexes for new query paths
   - conventions: follows Laravel Boost guidelines, `docs/conventions.md`, and the
     code-standards skill (cite CS-n in findings)
3. **Skip entirely**: style nits Pint already enforces, hypothetical refactors,
   scope expansion ("while you're here…"), praise padding.

## Report

Post one PR comment via `gh pr comment` (or reply inline where supported):

```
task-agent review — TASK-<n>

Gates: pint ✓ / phpstan ✓ / tests ✓
Findings:
1. <file:line> — <problem> — <required fix>   (only real findings; empty is fine)

Verdict: PASS | FAIL — <one-line reason>
```

## Verdict → board

The reviewer never marks a PR ready and never merges — it returns a verdict and
the task-workflow skill acts on it.

- **PASS** → task-workflow step 9 finishes the task (human merge by default;
  gated merge only if the developer enabled it).
- **FAIL** → a fix round. The findings go back to the same implementation agent in
  the same worktree, up to `MAX_REVIEW_ROUNDS` (default 3), then `blocked`.

## Re-review rounds

Round 1 is the full review above. **From round 2 on, review the fixes, not the PR
afresh:**

1. Verify each finding from the previous round is actually resolved — cite the
   diff line that resolves it, or repeat the finding.
2. Look for regressions the fixes introduced.
3. Anything else you notice goes to `workflow/<TASK-id>-<slug>/backlog.md` and is
   named in the summary — **not** into this PR. A reviewer that finds six new
   things every round means the loop never converges and the human never gets a
   merge.

Write each round's report to `workflow/<TASK-id>-<slug>/review-<n>.md` as well as
posting it, so the next round can read what the last one asked for.
