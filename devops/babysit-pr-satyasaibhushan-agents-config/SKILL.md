---
name: babysit-pr
description: Monitor a pull request through review and CI. Use when the user asks to babysit, monitor, or watch a PR, or to see it through to green.
---

# Babysit PR

Our repos use GitHub Copilot as the review bot. It is helpful even when it is
not right. Your job is to drive the PR until Copilot has nothing actionable
left and every check is green, without letting the PR grow.

## The loop

1. Find the PR: the user's argument, else the open PR for the current branch
   (`gh pr view --json url,headRefName,reviews,reviewRequests,statusCheckRollup`).
2. If Copilot has neither reviewed nor been requested, start it:
   `gh pr edit <url> --add-reviewer Copilot`. If that fails, use the API:
   `gh api --method POST repos/<owner>/<repo>/pulls/<n>/requested_reviewers -f 'reviewers[]=copilot-pull-request-reviewer[bot]'`
3. Wait for the review to land. Poll roughly every minute; Copilot usually
   takes a few. Do not touch the branch while waiting.
4. When the review arrives, act only on comments and checks newer than the
   latest push. Verify every bot finding against the source before changing
   code. Fix real findings and CI failures; distinguish repository failures
   from infrastructure flakes and retrigger flakes instead of "fixing" them.
5. If a finding is not worth addressing, reply with a written reason and
   resolve the thread. Replies are team-visible: plain English, no AI
   references, no signatures.
6. Push the fixes, re-request Copilot (same command as step 2 retriggers a
   fresh review after new commits), and wait again.
7. Repeat until Copilot has no unresolved actionable comments and all checks
   pass. Then report: PR URL, checks green, review clear.

A Copilot review overview that says "Approval recommended" means the review
is clear: stop there. Low-severity findings, including ones listed under
"Previously missed", are not actionable; do not fix them or re-request a
review for them.

## Guardrails

- Do not let review feedback expand the PR beyond the user's original goal.
  Address real shortcomings, but avoid scope creep. When a finding is real
  but out of scope, note it in one line to the user instead of fixing it.
- Keep an eye on the base branch; merge it in when the PR falls behind or a
  check requires it.
- If an overlapping PR makes this one obsolete, stop monitoring, report to
  the user, and ask before closing. Never close a PR without explicit
  authorization.
- If the same finding survives two fix attempts, stop looping and bring it to
  the user with what you tried.
- Merging is not part of babysitting. Report green and stop; merge only if
  the user already said to.

## Resolving threads

List threads with GraphQL (`reviewThreads` on the PR), reply via
`gh api repos/<owner>/<repo>/pulls/<n>/comments/<id>/replies -f body='...'`,
then resolve with the `resolveReviewThread` mutation using the thread id.
