---
name: babysit-pr
description: >-
  Monitor a pull request through review and CI until it's green: verify every
  bot claim against the code, fix what's real, push back on what's wrong,
  rerun flaky checks. Use when the user asks to babysit, monitor, watch, or
  shepherd a PR, says "get this PR green" or "handle the review comments".
  Accepts an optional PR number/URL; defaults to the current branch's open PR.
---

# Babysit PR

The repos we work in have AI review bots. They're helpful, even if they are
not always right. Treat every bot comment as a hypothesis, not a finding:
read the code it points at before acting on it.

First check `gh pr view <n> --json isDraft`. Review bots skip draft PRs
(CodeRabbit posts "Review skipped: Draft detected"), so on a draft there is
no bot review to wait for. Either ask the user whether to mark it ready
(`gh pr ready <n>`), or trigger one manual review with a single
`@coderabbitai review` comment. Trigger ONCE and wait: repeat triggers do
nothing ("Already reviewed") or hit the fair-usage rate limit, and each
attempt leaves a spam comment on the PR. When babysitting several draft PRs,
stagger the triggers well apart (the limit is adaptive and shared across the
org); expect some reviews to take an hour or more to land, and just wait —
re-commenting does not speed it up.

If your harness offers tools to monitor a PR, use them so you can respond
when comments arrive. Otherwise, poll: `gh pr checks <n> --watch` in the
background covers CI, and check for new comments on a relaxed interval.

Only act on checks and comments newer than the latest push — anything older
is already handled or already obsolete.

For each comment: fix it if it's a real bug. If it's wrong, reply with
evidence (`file:line`, the actual behavior) and resolve the thread. If it's
real but beyond the PR's goal, acknowledge it and file a follow-up issue
instead. Human reviewers outrank bots — address their requests, and never
resolve their threads for them.

For CI failures, read the failing log (`gh run view <id> --log-failed`).
Fix what this PR caused. Rerun a flaky check once (`gh run rerun <id>
--failed`); if it fails again, it's real. If it's broken on the base branch
too, report it to the user — that's not this PR's job.

Push fixes as new commits; a reviewed branch keeps its history. Reply to
inline comments in their thread, never as a top-level PR comment
(`gh pr comment` can't do this — use GraphQL):

```bash
# list threads with resolution state
gh api graphql -f query='query($o:String!,$r:String!,$n:Int!){repository(owner:$o,name:$r){pullRequest(number:$n){reviewThreads(first:100){nodes{id isResolved path line comments(first:10){nodes{author{login} body createdAt}}}}}}}' -F o=<owner> -F r=<repo> -F n=<pr>

# reply in a thread
gh api graphql -f query='mutation($t:ID!,$b:String!){addPullRequestReviewThreadReply(input:{pullRequestReviewThreadId:$t,body:$b}){comment{url}}}' -F t=<thread-id> -f b='<reply>'

# resolve a thread
gh api graphql -f query='mutation($t:ID!){resolveReviewThread(input:{threadId:$t}){thread{isResolved}}}' -F t=<thread-id>
```

Screenshots and short recordings help when the fix is visual.

Do not let review feedback expand the PR beyond the user's original goal.
Address real shortcomings, but avoid scope creep.

If nothing has changed, stay quiet rather than posting filler comments. Stop
when the review bots and required checks are green on the latest commit.
Merge only when the user explicitly requested it; otherwise report that the
PR is ready.
