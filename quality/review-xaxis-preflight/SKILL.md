---
name: review
description: Review the current diff for correctness, security, and convention drift before shipping. Use after finishing a unit of work and before opening a PR.
argument-hint: [optional base branch or path]
---

Review the working diff: $ARGUMENTS

## Steps

1. **Get the diff.** Default to `git diff HEAD` plus untracked files; if a base was given, use `git diff <base>...HEAD`. If the diff is empty, say so and stop — there is nothing to review.

2. **Delegate to the `code-reviewer` subagent.** Give it the diff scope and the base. It reads the diff and the surrounding code in its own context so the review costs you a report, not a repository.

3. **For a large or multi-concern diff, spawn several `code-reviewer`s with different lenses** and merge the findings. One reviewer holding an eight-file diff misses what a focused one catches — and identical reviewers miss the same things identically. Give each a distinct job:

   - *Break it*: assume the code is wrong; hunt a concrete input, ordering, or edge case that makes it fail.
   - *Check it*: assume it's right; take each claim it makes and trace it to the evidence. Report where the evidence doesn't support the claim.
   - *Simplify it*: only complexity this diff introduced — one-use abstractions, indirection, duplication.

   Two opposed lenses beat two more pairs of eyes.

4. **Check the rules yourself.** Read the `.claude/rules/` files whose `paths:` match the changed files and confirm the diff honors them. Path-scoped rules load when Claude *reads* a matching file — so a rule may not be in context just because the diff touched that path.

5. **Report** findings ranked most severe first, then a verdict: ship / ship with fixes / needs rework.

## Judging findings

Before you pass a finding to the human, try to disprove it. Read the code that would make it safe — the upstream guard, the caller that already validates, the framework behavior that handles it. Report what survives; drop what doesn't, silently.

Every finding needs a concrete failure: inputs or state → wrong result. A finding you can't make fail is a guess, and guesses train the reader to ignore real findings.

Don't report what a tool owns. Formatting belongs to the formatter, lint to the linter. If you keep hand-catching the same mechanical issue, that's a signal to write a hook, not a better review.

A clean diff gets a short review. Say it's clean and stop — manufacturing a finding to look thorough is a failure, not diligence.

## After

Fix what you're confident about, ask about what you're not, and report anything you chose not to fix and why. If tests are missing for a behavior change, that's a finding — write them before shipping.
