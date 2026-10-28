---
name: pr-feedback
description: Check review feedback added after the latest push on the current PR. Judge each finding through three gates, address findings that do not need a user decision, push any changes, and request another review in one summary comment. Use when the user asks to check or address PR feedback.
---

# PR feedback

## Check feedback

Find the current PR and its latest push. Read all reviewer feedback added after that push, including review bodies, inline comments, and top-level comments.

If there is no new reviewer feedback, state that there is no new feedback yet, check later.

If the newest reviewer feedback clearly says that there are no major issues, all is good, the PR is approved, or similar, state that there are no further issues and finish. Do not change code or add a PR comment.

## Apply the gates

Judge all findings before you change code. Apply these gates in order to each finding:

1. **Is it correct?** Verify the claim in the code and its wider context. If it is wrong, do not change the code. Keep the evidence for the summary comment.
2. **Does it move the design?** Ask the user before you change an interface, dependency, agreed design, documented constraint, or core principle. Explain the finding, options, costs, and recommendation, then finish. Do not change code or add a PR comment.
3. **Is it worth fixing now?** Compare the impact with the cost and rarity. Fix worthwhile findings at the cause and add a regression test when useful. Defer other findings with a clear reason and record follow-up work where the project keeps it.

## Address feedback

Test the changes as required by the repository. Commit and push any changes.

Add one top-level PR comment that summarizes all findings and outcomes. Include important evidence, changes, tests, and deferred work. Do not reply to review threads. End the comment with `@codex review`, exactly once; do not use that tag elsewhere in the comment.
