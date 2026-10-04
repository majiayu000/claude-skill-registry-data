---
name: pull-request
description: "Use when creating, reviewing, or responding to GitHub pull requests: opening a PR, addressing review feedback, resolving PR comments, running a code review, or getting a PR into a mergeable state. Triggers on phrases like 'open a PR', 'review this PR', 'address the comments', 'gh pr', or 'resolve review threads', even when the user doesn't say 'pull request' explicitly."
---

# Pull Requests

This skill is GitHub-specific. It assumes the `gh` CLI is authenticated (`gh auth status`). The exact commands for inline comments, code suggestions, resolving threads, and watching checks live in `references/github-cli.md`. Read that file whenever you need to post to or query a PR, since several of these operations are easy to get wrong from memory.

Everything this skill produces is read by a person: the PR description, the review comments, the replies. Invoke the `writing` skill with the Skill tool before drafting any of it.

## Creating pull requests

- Match the repository's PR template. It usually lives at `.github/PULL_REQUEST_TEMPLATE.md` (also seen at `.github/pull_request_template.md`, the repo root, or `docs/`). Read it first and fill in every section. A template exists because reviewers rely on those sections being present.
- Keep the description clear and concise. Write what changed and why; link the issue it closes.
- If the change touches multiple components or has non-obvious control flow, add a small **Mermaid** diagram. It renders inline on GitHub and saves reviewers from reconstructing the flow themselves.
- After opening, CI gates and autonomous review agents fire almost immediately. Give them time to run rather than declaring victory early, and poll with `gh pr checks --watch` (see references).
- The goal is a PR that's genuinely ready to merge: checks green, review threads addressed. When a check *fails* (as opposed to still running), read the logs and fix the cause. Don't merge, dismiss a human's review, or force-push over someone else's work without asking the user first. Those are hard to undo.

## Reviewing pull requests

This review checks the code for logical errors and correctness. Whether the change is the right change, and whether it matches the intent behind the PR, is the user's call.

If the change came from a plan, the `planning` skill's own review phase has already been over the diff. Don't re-raise what it fixed.

- Confirm the build gates are passing before spending time on the code; a red build often explains issues you'd otherwise flag by hand.
- Check that the PR template is filled in.
- Check logical correctness. Does the code do what it says, and does it hold up on the paths the author didn't walk? Off-by-one errors, unhandled nulls and failures, inverted conditions, races, leaks, and state left behind on the error path.
- Check the tests. Do they cover the edge cases, and are there gaps worth filling?
- Flag dead or unreachable code, and code that is wrong rather than merely different from how you'd have written it.
- Avoid nitpicking. Style the linter already enforces isn't worth a comment, and neither is a preference dressed up as a finding.

Anything about intent goes to the user, not to the PR: a description that doesn't match the diff, scope that looks wrong, or an approach you'd have taken differently. Say it in your summary and let the user decide whether it's worth raising.

Compile the issues you find into a list for the user, each linking to the relevant spot on the PR. Ask for permission before posting anything. The user may want to adjust or drop some.

Once approved, post them as **inline** comments anchored to the relevant line (not top-level PR comments). When a fix is small and unambiguous, use a GitHub **suggestion** block so the author can apply it in one click instead of a prose comment.

The verdict is the user's. They say whether the review goes up as **Approve**, **Request changes**, or **Comment**. Never choose one yourself, and if they haven't said, ask before posting. Label each comment with how much it matters (blocking, suggestion, nit, question) so the author can tell a real problem from a preference. See `references/github-cli.md` for the exact commands.

Each comment should follow this shape:

```markdown
This is a <bug | correctness issue | missing edge case | question>.

<what happens, concretely>

<a suggested fix>
```

## Responding to comments

- Fetch every comment on the PR (`gh pr view --comments`, and the review-thread query in references for unresolved threads).
- For each one, decide: address it, or push back. Both are legitimate. A well-reasoned disagreement is a valid response.
- Reply to the original comment with your resolution. If you made the change, reply with what you did and a link to the commit, then resolve the thread. If you're pushing back, reply with the reasoning and leave the thread open for the author.
- Stay in scope. If a comment asks for something beyond this PR's purpose, don't quietly expand the PR to cover it. Reply proposing it be tracked as a separate issue for later.
