---
name: merge-policy
description: The software-factory rule that main must always be green, and how to land PRs under it — when a bypass/admin merge is and is not allowed, how to handle a hung required check, and what to do when main goes red. Use before merging or landing any PR, before running `gh pr merge --admin` or any merge that skips required checks, when a required check is stuck or failing, or when a test fails on main.
---

# Merge policy: `main` must always be green

`main` must never carry a genuinely failing test, type error, or lint violation.

## The rule

Never use `gh pr merge --admin`, or any merge that bypasses required status checks, to get past a check that is actually `FAILURE`. Fix the failure instead.

## The only two legitimate bypasses

1. **The factory's own auto-merge.** It bypasses the review-approval requirement, which a bot cannot obtain. Its CI gate (`waitForMerge` in `packages/cli/src/cli/index.ts`) still refuses to merge unless CI reported a real `success`. It never merges on a failure or an unresolved or hung outcome.
2. **A human confirms a required check is hung, not failed** (for example the #739 CI deadlock). Before merging:
   1. Run `bash scripts/verify.sh --no-e2e` locally and get it green.
   2. Run targeted checks for anything the fast path skips (coverage: `npm run test` then `npm run coverage-ratchet`).
   3. Say explicitly in the merge or PR comment that the check was hung and what you ran instead.

A bypass under case 2 is a workaround for an infra bug, not a norm. Open or link the issue that fixes the hang.

History: the multi-hour `ci` hang of #739/#755 was an unbounded microtask-only spin loop in `router/index.test.ts`, not the integration tests. CI jobs now carry a `timeout-minutes` ceiling so a future spin cannot strand open PRs.

## When `main` is red

1. Treat it as the top-priority task. A red `main` blocks every open PR, and every PR's diff is measured against it.
2. Reproduce on a fresh branch off `origin/main` with `bash scripts/verify.sh`.
3. Fix the root cause in a small PR. Do not skip or delete the failing test to get green.
4. Land the fix with normal required checks. Rebase other open PRs afterwards.

## Landing a factory PR

- `factory ship` and `factory run-issue` stop at a ready-for-review PR. They never merge.
- `factory land <issue>` squash-merges a ready PR and cleans up its worktree.
- `factory run` merges only when auto-merge is on (`--auto-merge`, `.factory/config.yaml`, or `FACTORY_MERGE=1`), and only through the CI gate above.
