---
name: dependabot-triage
description: Drain open dependabot PRs per docs/MERGE-POLICY.md - classify each, run the area's tests for the risky ones, get one short fresh review per bump, merge the routine ones on green, and leave the rest (GitHub Actions bumps, majors, breaking changes, and auth-critical bumps, which wait for the maintainer's yes after their tests and a review) for the maintainer. Use when dependabot PRs have piled up or as routine housekeeping.
---

# Dependabot Triage

The policy is `docs/MERGE-POLICY.md` ("Who merges", grouped PRs, the auth-critical package list). The classification is `scripts/dependabot/classify.py`. If they disagree, the policy wins over the classifier, and both win over this skill. Do not edit the policy while triaging; file an issue for a gap.

## Before starting

Stop and tell the user if any of these hold:

- A release is in progress (a `release/*` branch exists or release tags are being pushed).
- `main` CI is red (every PR will fail the same checks; drain nothing). After any merge, a red `main` stops merging, for whoever merges, until it is fixed or reverted; the fix or revert is merged under the same tiers as any change.

## Procedure

1. List the PRs: `gh pr list --author "app/dependabot" --state open --json number,title,labels,headRefName,files,body,url`. None open: say so and stop.
2. Classify each PR with `scripts/dependabot/classify.py` (it returns a group and a reason): pipe the step 1 JSON array to it on stdin, `gh pr list ... | python scripts/dependabot/classify.py`, and it writes a JSON array of classifications to stdout. Groups:
   - **A, review then merge:** get one short fresh review (R1 in MERGE-POLICY.md: a fresh agent that gets the diff and the bump, not your reasoning). If it returns no must-fix finding, merge as in step 5.
   - **B, verify, review, then merge:** run the area's tests below, then do as for A. On failure, comment with the failing tests and stop on that PR. A bump of an auth-critical package is the exception: it is maintainer first (category 5 in MERGE-POLICY.md). Run its tests and get its review, then do as for C; it waits for the maintainer's yes.
   - **C, maintainer first:** do not merge and do not enable auto-merge. Comment with the group and the classifier's reason, and put the PR on the coordinating session's list of decisions waiting (D5 in docs/MAINTAINER-SESSION-RULES.md) so the maintainer can decide. Every GitHub Actions bump is C, and so is every major or breaking-change bump.
3. Every major bump is C, and so is every GitHub Actions bump. Any non-major bump of an auth-critical package (the list in MERGE-POLICY.md) is B in the classifier, patch included. It is still maintainer first (category 5 in "Who merges"): after the area's tests and one fresh review, it waits for the maintainer's yes. A grouped PR takes its most conservative member. Before you merge an A or B bump, check its diff against the "Maintainer first" categories in MERGE-POLICY.md; one that falls in any of them is C.
4. Close a PR as superseded only when a newer PR names it explicitly or strictly contains its version range. Otherwise leave both open and say so in the report.
5. Merge an A or B bump only when all of these hold on its head commit: it falls in no "Maintainer first" category (step 3), its review converged, the required checks are green, no review thread is open, and there is no new code-scanning alert. Wait for the code-scanning result before merging. Then run `gh pr merge <n> --squash --delete-branch --match-head-commit <reviewed sha>`. Do not use `--auto`, because it does not wait for that result.

## Verification commands (group B, one PR at a time, in a throwaway worktree)

- Touches `src/PPDS.Auth/**`: `dotnet test tests/PPDS.Auth.Tests --filter "Category!=Integration" -v q`
- Touches `src/PPDS.Dataverse/**`: `dotnet test tests/PPDS.Dataverse.Tests --filter "Category!=Integration" -v q`
- Other NuGet: `dotnet test PPDS.sln --filter "Category!=Integration" -v q`
- npm (extension): `( cd src/PPDS.Extension && npm test && npm run typecheck )`

Run them sequentially; they are heavy. Remove each worktree afterwards.

## Draining

While a reviewed PR's checks run, watch it with `gh pr view <n> --json state,mergeStateStatus,statusCheckRollup,headRefOid`.

- A new commit on the PR (Dependabot rebased it): the review no longer covers it. Review the new head before merging.
- A failed check or a merge conflict: comment on the PR and stop on it; do not retry.
- Thirty minutes in total. Then report where things stand and exit; do not hold the session open.

## Report

Finish with a table of PR, group, final state and reason. Call out failed verifications, stalled PRs, ambiguous classifications and PRs open more than 30 days (flag; do not close). For each PR you merged, give the coordinating session what it needs for the daily list ("Who merges" in MERGE-POLICY.md): the number, the reviewer's verdict and the commit it reviewed, and the squash commit to revert.

References: `.github/dependabot.yml`, `tests/scripts/dependabot/test_classify.py`.
