---
name: pr-cleanup
description: >-
  Audit and resolve open or stale GitHub pull requests across an explicit
  repository or organization scope. Use when asked to clean up PRs, merge all
  work that remains valid, revive or complete unfinished work against current
  main, close superseded PRs, or run that workflow on a schedule. Enforces a
  live census, current-head readiness gates, safe parallel ownership, branch
  retention, post-merge verification, and a final zero-open census.
---

# PR cleanup

For a cleanup request, bring the exact requested scope to zero open pull
requests or identify a genuine authority blocker. For a read-only request,
produce a complete current census and classification without changing state.
Preserve useful intent even when the original patch can no longer be merged
safely.

## Establish scope and authority

- Resolve every named owner, organization, and repository before changing
  state. For an organization-wide request, include every non-archived,
  non-disabled repository unless the user narrows the scope. Include named
  repositories outside that organization exactly as requested.
- Treat an explicit request to clean up, reconcile, revive, complete, merge,
  or close PRs as authority to update in-scope branches, create successor PRs,
  merge ready PRs, close superseded PRs, and leave concise audit comments.
- Treat inspect, review, report, or audit-only requests as read-only. Stop
  before the first write unless the user has granted mutation authority.
- Do not infer authority to force-push, delete branches, cancel another
  actor's work, create tags or releases, deploy production, mutate providers,
  or change archived repositories. Ask when one of those actions is required.
- Read the governing `AGENTS.md`, contribution guide, branch policy, and CI
  commands in each repository before acting. Preserve dirty user worktrees and
  unrelated changes; use an isolated clean worktree or clone for recovery.

## Build a live census

1. Verify GitHub authentication and read access for the requested scope. When
   mutation is authorized, verify write access before the first write.
2. Enumerate repositories and open PRs from the live GitHub API with complete
   pagination. Do not trust a cached list or a previous run. Include drafts,
   bot PRs, and cross-repository head branches.
3. Record, for every PR, its repository, number, URL, title, author, draft
   state, base branch and SHA, head repository, branch and SHA, update time,
   mergeability, reviews, unresolved threads, and check rollup.
4. Deduplicate by repository and PR number. Keep the initial count as evidence
   and rescan after each merge batch because new PRs may arrive while working.

Parallelize independent repository audits. Assign exactly one mutation owner
per repository and serialize merges within that repository. A separate agent
may independently review a risky recovery, but it must not mutate the same
repository.

## Classify from current main

Inspect each PR's commits and complete diff against the current remote base,
then classify it with concrete evidence:

- **Ready or current:** the intent is still needed, the implementation fits
  current architecture, and the branch can satisfy today's readiness gate.
- **Recoverable:** the intent remains relevant, but drift, conflicts, partial
  implementation, or obsolete mechanics make the original patch unsafe. The
  work must be completed or recreated from current main.
- **Superseded:** current main or another delivered change already provides the
  intended outcome, the owning feature was intentionally removed, the PR is a
  duplicate, or the request is no longer valid.
- **Blocked:** the intent may be valid, but required authority, credentials,
  an external decision, or a non-transient dependency is unavailable.

Age alone never makes a PR superseded. Historical green checks are not current
evidence. Search current code, history, issues, linked PRs, and repository
instructions before discarding intent. Preserve archives, compatibility
fixtures, and historical contracts unless current policy explicitly replaces
them.

## Recover relevant work

For a current PR, prefer the smallest non-force update that preserves its
review history. For a heavily drifted or conflicted PR, start a successor from
the exact current remote base and reconstruct the intended outcome:

1. Extract the behavioral requirement from the PR description, discussion,
   commits, tests, and linked issues.
2. Separate that requirement from obsolete implementation choices.
3. Reimplement or selectively replay only the still-valid changes on current
   main. Resolve conflicts semantically; do not accept a mechanical conflict
   resolution without reviewing both sides.
4. Add or update focused tests for the recovered behavior and run the closest
   repository-required gates.
5. Deliver through the repository's normal PR, merge queue, or direct-main
   policy. If the original head is a fork or cannot be updated non-forcibly,
   create a successor in a writable repository.

Keep the original PR open until its successor is merged and verified. Link the
two in both directions when possible.

## Enforce the readiness gate

Immediately before a merge, refresh the PR and require all of the following:

- the recorded head SHA still matches the reviewed commit and the base is the
  current intended branch;
- GitHub reports no unresolved merge conflict or unknown merge state;
- every required current-head check, including external preview or deployment
  checks, is terminal and successful;
- required approvals are present and no review or conversation thread remains
  unresolved;
- the resulting tree still fits current main and contains no unrelated,
  unreviewed work;
- repository-specific tests and policy gates pass at the exact candidate SHA;
  and
- recovered, security-sensitive, release-sensitive, or cross-cutting work has
  an independent final review when the repository does not already provide
  equivalent review.

Use the repository's required merge method. Match the exact reviewed head SHA
when the GitHub operation supports it. Never force a stale merge after the head
or base changes; refresh, re-review, and rerun affected evidence.

## Merge, supersede, and retain evidence

Merge ready PRs one at a time per repository. After each merge, refresh the
base and reassess every remaining PR in that repository.

Preserve source branches by default. Do not request branch deletion. If the
repository automatically deletes an in-repository head branch, recreate that
exact branch at its pre-merge head SHA with a non-force ref update, then verify
the ref. Report a fork branch that cannot be restored instead of widening
authority.

Before closing a superseded PR, leave one concise final comment that records:

- why the work is no longer applicable or where its outcome now lives;
- the successor PR, merge commit, or current-main evidence;
- original, recovery, and delivered SHAs when recovery occurred;
- the current checks or tests that support the decision; and
- that the source branch was retained, or the exact reason it could not be.

Close only after the replacement outcome is delivered and post-merge evidence
is green. Do not relabel a permissions or CI blocker as superseded merely to
reach zero.

## Verify post-merge state

Watch the exact default-branch commit produced by each merge until all
required post-merge workflows and provider checks are terminal. Distinguish a
product failure from a demonstrated transient infrastructure failure. Rerun a
confirmed transient job at most once unless repository policy explicitly says
otherwise; if the same failure repeats, diagnose or mark it blocked.

If a merge causes a real regression, repair it through the repository's normal
delivery path before merging the next dependent PR. Do not cancel unrelated
runs or mutate releases and deployments to manufacture a green result.

If another actor pushes, merges, tags, releases, or changes a relevant check
while work is in progress, pause mutation only for the affected repository,
take a fresh census, and revalidate the exact state. Never overwrite or undo
concurrent work without explicit authority.

## Finish from live state

After the final merge or closure, rerun the complete paginated census across
the original scope. Cleanup success requires zero open PRs, including drafts
and newly arrived work. Read-only success requires a complete fresh census and
classification; open PRs remain reported findings, not authority blockers. On
a recurring cleanup run, always rebuild the census from live state; if it is
already zero, report that and stop without creating work.

Report merged PRs, recovered successors, superseded closures, retained branch
refs, exact verification links or commands, and the final open count. In
cleanup mode, if the count is nonzero, name each remaining PR, the failed
predicate, the evidence, and the specific authority or external change needed
to continue.
