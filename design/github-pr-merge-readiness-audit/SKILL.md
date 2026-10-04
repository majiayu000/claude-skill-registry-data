---
name: github-pr-merge-readiness-audit
description: >-
  Use when deciding whether one or several open pull requests can merge — a PR shows green checks
  but will not merge, an AI reviewer approval was dismissed after a merge commit, an approval sits
  on a stale head SHA, `mergeStateStatus` reports BLOCKED, commitlint failed on a title, or a batch
  of PRs needs ordering by what actually blocks each one.
---

# GitHub PR merge readiness audit

## Profile keys consumed

- `project.repo`
- `make.pr_comments`
- `ci.required_checks`
- `review.request_changes_blocking`

## Overview

"All checks green" is not merge readiness. A pull request is ready only when every approval sits on
the current head, the branch is conflict-free, every non-conditional check succeeded, no review
thread is open, and whatever the repository's protection rules require is satisfied. Audit those
five independently; a green checks page hides four of them.

## When to use

- A PR looks passing but reports as blocked or not mergeable.
- Reviewer approvals were dismissed, or predate the newest commits.
- Several PRs need triage into a merge order with a named blocker for each one that is not ready.
- Not for: fixing the underlying failures — that is the job of the gate that failed.

## Applicability by repository shape

- **React SPA shape** (feature modules under the source root, a bootable app, an aggregate CI
  target): partial — CODEOWNERS is a single wildcard owner, commitlint enforces the
  `type(#issue): subject` task-number rule, and the target mapped by `make.pr_comments` lists
  unresolved threads; its agent-steering guide records that no branch protection or ruleset is
  configured, so a required-review verdict may not appear at all even though `ci.required_checks`
  names the expected checks.
- **Next.js app shape** (routed pages, no aggregate duplication gate): yes — path-scoped CODEOWNERS
  covers the agent-steering files, the same commitlint task-number rule applies, `make.pr_comments`
  maps to a real target, and `burn in changed e2e specs` is the conditional job that legitimately
  reports as skipped.
- **Component-library shape** (Storybook-first, no bootable app, published package): partial —
  CODEOWNERS is a single wildcard owner and the commitlint rule matches, but `make.pr_comments`
  maps to `null`, so skip that target with a recorded note and read unresolved threads through the
  GitHub API directly, resolving the repository from `project.repo`.

## The five checks

1. **Approvals on the current head.** For each required reviewer, take only its most recent review
   and confirm the review's `commit_id` equals the PR head SHA and the state is `APPROVED`, not
   `COMMENTED` or `CHANGES_REQUESTED`. A stale approval reads as an approval in the UI.
2. **Conflicts.** `mergeable` must be `MERGEABLE` with zero conflicts, and the branch should be zero
   commits behind the base.
3. **Checks.** Every check must be `SUCCESS`, except conditional jobs that are legitimately
   `SKIPPED`. A cancelled run followed by a later success on the same check is fine — read the
   latest attempt, not the first.
4. **Review threads.** Zero unresolved.
5. **Protection rules.** `reviewDecision` of `REVIEW_REQUIRED` means a human approval is
   outstanding; AI reviewer approvals do not satisfy a required-reviewer or CODEOWNERS rule. A PR
   touching an owned path needs the owner's review requested and granted. When
   `review.request_changes_blocking` is true, an outstanding `CHANGES_REQUESTED` review is itself a
   blocker regardless of the checks.

## Blockers and their fixes

| Blocker                        | Fix                                                        |
| ------------------------------ | ---------------------------------------------------------- |
| Approval dismissed after merge | Push a real commit, then re-request the review             |
| Approval on a stale SHA        | Re-request the review against the current head             |
| Stale `CHANGES_REQUESTED`      | Have the reviewer re-review the current head               |
| commitlint failed              | Reword to `type(#issue): subject` on the title and commits |
| Cancelled then passing check   | Read the later attempt; the cancelled one is not a failure |
| CODEOWNERS approval missing    | Request review from the owner of the touched path          |
| Open review threads            | Resolve each with a fix or a reasoned reply                |

Merging the base branch into a PR auto-dismisses prior approvals, and an AI reviewer will often
decline to re-review a pure merge commit because it has no reviewable diff. Plan the merge order so
each PR takes the base merge once, then lands.

## Reporting

Group by verdict and give a merge order, oldest and dependency-free first. For every PR that is not
ready, name the single blocker, the reviewer or check it belongs to, and the one action that clears
it. Flag as at-risk any PR whose approvals predate a base merge even when the state still reads
approved.

## Common mistakes

- Reading the checks tab and stopping there.
- Counting an approval without comparing its commit to the head.
- Treating a conditional skipped job as a failure, or a cancelled superseded run as one.
- Expecting AI reviewer approvals to clear a required-reviewer rule.
