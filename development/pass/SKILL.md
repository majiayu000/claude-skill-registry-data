---
name: pass
version: 0.1.0
license: MIT
description: Use before opening a pull request, before running gh pr create, or before pushing follow-up commits to an existing PR. Also use when the user asks "is this PR ready", "should I file this", or wants a change inspected before it goes out for review.
---

# pass

The pass is where the chef inspects every plate before the runner carries it out. Nothing leaves half-cooked, mislabeled, or with a thumbprint on the rim. This skill is that inspection for a pull request: the gate between "the code works on my machine" and "this is in front of a reviewer." The PR is not filed until it clears the pass.

A PR is a request for someone else's time. The bar is not "it compiles," it is "a reviewer can understand it, trust it, and merge it without doing the work you skipped."

## The checklist

Run every check. Anything that fails holds the plate: tell the author which check failed and why, fix it, then re-run the pass. Do not file and do not silently start fixing without surfacing the hold first.

The sub-skills below are the preferred way to satisfy a check. If a referenced skill is not installed, perform its equivalent by hand, the gate still holds; the skill is the shortcut, not the requirement. Likewise `gh` assumes GitHub: on another platform, draft the artifacts and hand them to the author to file through their flow.

"Non-trivial" here means anything beyond a one-line, obviously-safe change (a dependency bump, a typo, a constant tweak). A small-looking change that touches behavior, like the timeout bump in the example below, is not trivial.

### 1. It is a real fix, not a bandaid
The change addresses the root cause, not the symptom. If it is a bugfix, you reproduced the bug, traced it to its source, and the fix targets that source. A change that silences an error, widens a timeout, or catches-and-ignores to make a symptom disappear is not ready. For an unclear defect, reproduce it and trace it to the root cause before you call it fixed ([refire](../refire/SKILL.md)).

### 2. It is tested and green
The change ships with a test that fails without it and passes with it ([taste](../taste/SKILL.md)); a bugfix ships with a regression test. Run the suite and the linter locally and read the output before claiming anything passes ([check](../check/SKILL.md)), do not assume. "CI will tell me" is not a substitute for green-on-your-machine.

### 3. It is one concern
One PR, one reason to exist. Unrelated cleanups, drive-by reformatting, and "while I was in there" changes belong in their own PRs; bundled, they bury the real change and stall the review. Split them out.

### 4. The diff is self-reviewed
Always read your own diff line by line before anyone else does. Remove debug prints, commented-out code, leftover TODOs, and stray files.

Then, only for a non-trivial change or any PR to a repo you do not own, get an independent review pass (a review skill, a bot, or a person) and resolve it before filing, not after. A trivial change skips this second pass.

### 5. The artifact is clean
- No secrets, internal hostnames, private IPs, or identifying content in the diff, the branch name, or the commit messages. For public repos, **REQUIRED SUB-SKILL:** use skillet's plate on the PR body and publish-readiness on the tree if there is any doubt.
- No AI-authorship trailers or `Co-Authored-By` lines unless the project asks for them.
- Commit messages describe the effect, follow the project's convention, and do not reference private context ("ask <name> about the prod box").

### 6. The PR body earns the reviewer's time
What changed, why, and how to verify it. Link the issue it closes. Call out anything risky or anything you want the reviewer to look at hardest. Draft it, show it to the author for approval, and only then `gh pr create`. Never auto-open a PR with an unreviewed body.

## Before pushing to an existing PR

Check the PR's state first: `gh pr view <n> --json state,mergedAt,closedAt`. A maintainer may have merged it, closed it, or carried the work forward in another PR. Pushing follow-up commits to a closed or superseded PR wastes everyone's time. A silent stall usually means closed, not lag, confirm before assuming it is still open.

## Rules

- The PR is not filed until the checklist clears. A failing check holds the plate.
- The author approves the PR body before it is opened. The skill drafts; it does not auto-file.
- Bot and heavyweight reviewers are opt-in. Use a second reviewer for non-trivial or upstream changes; do not bury a one-line dependency bump in three bot reviews.
- One PR, one concern. If you cannot describe the change in a sentence without "and", split it.

## Common mistakes

- Filing the symptom-mask because "the test goes green," when the test was the thing masking the bug.
- Opening a PR whose body is the commit log. Reviewers want the why and the how-to-verify, not the plumbing.
- Auto-creating the PR before the author has seen the description.
- Bundling an unrelated refactor into a bugfix PR, so the review stalls on the noise.
- Pushing follow-ups to a PR that was already closed or merged, because nobody checked its state.
