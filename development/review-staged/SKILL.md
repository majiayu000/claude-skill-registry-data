---
name: review-staged
description: Workflow to review the staged Git diff for verified bugs and then prepare a clean Conventional Commit. Use when the user directly asks to review staged changes or prepare a commit proposal. Do not trigger on a direct commit instruction without a review request.
metadata:
  website: "https://photostructure.com/coding/claude-code-review/#review-staged"
---

# Review Git Staged Changes

Review the **staged** diff (`git diff --cached`) for potential issues and
improvements, then prepare the commit. When the user supplies a proposed commit
message, use it as context for the intended change, not as a correctness
requirement.

## User direction

A direct "commit" or "approved, commit" instruction authorizes the understood
scope and takes precedence over this skill's review and approval defaults.
Unless the user also requests review first, use [stage](../stage/SKILL.md) to
verify and commit that scope without starting or resuming a review or asking
for approval again. This also applies after findings or a review verdict; a
reviewer's recommendation does not overrule the user's commit instruction.
When project instructions require review before every commit, a commit
instruction for changes that review has not finished on since they last
changed runs the review first, and only an explicit instruction to skip review
skips it.

## Run the review

Size the scope before reading it: `git diff --cached --stat`. Review all staged
content as supplied. The size or coherence of a proposed commit does not affect
the review verdict.

With the staged diff as the scope, read and follow
[`../review/references/single-pass.md`](../review/references/single-pass.md).

After the findings, use the shared `Commit notes` section for optional message
or grouping advice. If a split would improve reviewability or make later reverts
safer, identify the files or hunks in each independently committable batch and
give a complete Conventional Commit message for every batch. State the specific
reason for the split; size alone is not enough. These notes never receive a
priority and never change the verdict. If they are the only concerns, return
`Verdict: LAND` and `No issues found.`

## Post-review commit flow

If the verdict is DISCARD, explain why the change should not land and stop the
review. A later user instruction to commit takes precedence as described in
**User direction**.

Otherwise:

1. List the files (and line ranges, if partial) that are staged for commit.
2. Present the recommended commit message, or the batches and messages from the
   `Commit notes` section. When no note was warranted, confirm the supplied
   message or draft one. Emphasize motivation or consequence rather than
   restating the diff.
3. If the user already authorized committing this scope, such as "review, then
   commit", proceed within those instructions without asking again. Otherwise,
   ask the user to approve or edit the proposal and wait for commit authorization.

## Scratch files

Any copy this workflow makes — of the repo, of a build-output directory, of a
file you replay edits onto — belongs in the operating system's temporary
directory, in a fresh directory named for the project and the purpose. Never
inside the checkout, and never under a home directory.

Delete it before you finish. A repo or build-output copy runs to gigabytes,
nothing reaps a home directory, and the out-of-disk failure that eventually
follows surfaces somewhere unrelated — a test suite that hangs, a build that
dies mid-link — costing far more to diagnose than the copy ever saved.
