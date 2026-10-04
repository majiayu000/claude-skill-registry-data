---
name: land-pr
description: "Use every time a change is ready to leave the machine. When the human says commit, push, open a PR, ship it, land it, or finish up, or when a task's last step is getting a change reviewed. Covers branch rules, the gate order, commit titles, PR descriptions, proof, and where it stops."
---

# Land PR

The last stretch of a change. Get it committed, gated, described, proven, and turned in. Then stop. A human merges.

## Branch rules

- Never commit to the default branch. Branch first.
- One task, one branch. Don't pile a second task onto a branch that's already carrying one.
- Commit and push only when the human asked, or when opening the PR is the task.

## The gates, in order

Cheap steps that change the code first, the expensive judgment last. Review reads the diff, so if the diff moves after review, you pay for review twice.

1. Format and lint, autofix. Always first.
2. Typecheck or compile.
3. Fast tests. Seconds to a couple of minutes.
4. `roast`, looped until it says well done. Run it bare, never with `--max-priority`; the threshold is the human's and the default is theirs. Rerun steps one to three before each round. Follow the roast skill for the scope fence.
5. The full suite, once, against the final review-clean diff.

If the full suite fails at the end, don't restart the review loop. Fix it, rerun the fast tier, review only the fix.

Use the project's own commands for each step. This is about the order, not the tools.

## Commit titles

For someone scanning history months from now. Conventional commit style. Name the outcome, not the mechanism. The mechanism is in the diff.

Bad: `perf(server): negotiate permessage-deflate on the websocket`
Good: `perf(server): cut websocket frame size by 70% with gzipping`

## The PR description

For a reviewer deciding what this change means for the product. Open with the problem in a sentence or two, then how you solved it. Plain words. No file-by-file tour.

Bad:

> Removed implicit workspace carry-over from every "new thread" entry point (cmd+n, sidebar buttons, command palette). New threads inherit only the project from context. Deleted buildContextualThreadOptions and the v1 sidebar's seed-context machinery.

Good:

> My "new worktree" default was ignored when starting new threads on existing worktrees. Super unintuitive. Now your preferences always apply.

Write it in the ticket shape from `tracker`: problem, fix, done when. Put the task id in it. End with a line naming the model and harness that made the change.

## Proof

Don't say it works, show it. Anything a user can see gets screenshots, including empty, loading, and error states. Anything that changes state gets receipts, the request and the stored result. Bug fixes show the broken state first, then the same capture fixed. Web flows get a keyboard-only pass.

All of it goes on the ticket at turn-in, the way `tracker` says for the repo's backend, never into git.

## After the PR is open

Check CI before calling it done. A red check is never "probably fine". Read the failing log to the real error.

## Where it stops

Turn the task in with the PR open, evidence attached, and the branch left standing. Then stop. A human reviews and merges. The task gets completed after the merge, and not by the agent that built it.

## Never

- Merge your own PR unless the human explicitly said to.
- Change the diff after review without rerunning the fast tier and reviewing the delta.
- Open a PR with failing or unread checks and call it done.
- Skip roast quietly. If it isn't installed, say so and point at tools.md.
