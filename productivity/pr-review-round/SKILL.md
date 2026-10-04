---
name: pr-review-round
description: Use when a pull request has review feedback to address — inline comments, a review with a body, or conversation comments — including a stacked PR, a single nit, or a round a GitHub notification announced.
user-invocable: true
---

# PR Review Round

**Read `<project>/.claude/workflow-overrides/pr-review-round.md` first, if it exists.** A project uses it to replace or add steps by name (for example a round doc copied from a template, a script that checks the doc's shape, a device run, or holding replies until Bryan has seen them). Every step it does not name runs as written here. Batching, dispute and reply-length rules stay in the fleet's workflow conventions.

## Steps, and the done-when line each one leaves

Put these on the task row as done-when lines when you start (`rewrite_task` keeps existing line ids), and report each with `report_done_when`. A line is `met` only with the proof named here.

| # | Step | Done-when line | Proof |
|---|---|---|---|
| 1 | Sweep all three comment surfaces and count each: inline (`gh api repos/O/R/pulls/N/comments --paginate`), review bodies (`.../pulls/N/reviews`, non-empty `body`), conversation (`.../issues/N/comments`). | All three surfaces swept | The three counts |
| 2 | Fix each comment on the branch of the PR it was left on. On a stack, a comment on a lower PR's diff is fixed on that PR's branch, then the upper PR is rebased. | Fixes on the right branches | Commit hashes, grouped by PR |
| 3 | Run the tests. Every new test is seen to fail without its fix. | Tests pass; new tests seen failing | Test output, and the failing run for each new test |
| 4 | Reply to every comment, including those you are not acting on, after the push. | Every comment answered | Replies per surface, matching the counts from step 1 |

**The notification's count is one surface.** "6 inline comments" says nothing about review bodies or the conversation tab, which is where the missed comments usually are. Step 1's proof is three numbers, never one.

**A one-comment nit still runs steps 1 and 4.** They are one command each, and a second comment elsewhere is the common miss. Steps 2 and 3 shrink to the fix and the existing test run.
