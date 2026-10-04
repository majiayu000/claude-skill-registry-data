---
name: address-review
description: Turns PR review comments into a triaged change list, applies the accepted ones, and drafts replies to .workflow/<KEY>/review-response.md. Use when a PR has feedback to work through.
---

# address-review

```
wb <args>    # wb not on PATH: python <this skill's directory>/../../lib/wb.py <args>
```

## Steps

1. **Collect the comments.** This plugin talks to issue trackers, not code
   hosts, so use whatever the environment provides — `gh pr view --comments`,
   `gh api`, the Azure DevOps CLI, or text the user pastes. If none is
   available, ask for the comments rather than guessing what they said.

2. **Triage each one** into exactly one bucket, and say which:
   - **accept** — correct, will change.
   - **question** — cannot act until the reviewer clarifies; draft the question.
   - **disagree** — will not change, with a reason and evidence.
   - **out of scope** — real, but a separate ticket; name the follow-up.

   Do not silently drop a comment. A reviewer who gets no answer assumes it was
   missed, and asks again.

3. **Verify before agreeing.** A reviewer can be wrong about this codebase. Read
   the code the comment refers to before accepting it —
   `../../shared/code-search.md` — and quote the line in the
   reply when you disagree.

4. **Apply the accepted changes.** Same discipline as `implement-change`:
   smallest diff, existing patterns, tests updated with the code. If a comment
   pushes the change outside the plan's file list, that is a plan change — update
   `sdd.json` and re-run `sdd audit <KEY>`.

5. **Re-verify.** `impl verify <KEY>` if a plan exists, otherwise the repo's test
   command. Review feedback is exactly when a regression slips in.

6. **Re-review your own diff.** `review context` on the new changes.

7. **Write the replies** to `.workflow/<KEY>/review-response.md`, one per
   comment, each saying what was done or why not, citing code as
   `` `path:line` — `the line` ``. `cite check` that file (`--worktree` for
   uncommitted changes) before showing it; posting is the user's call.

## Rules

- **Every comment gets an answer**, including the ones you disagree with.
- **Disagreement needs evidence.** `file:line` and the actual line, not an
  assertion. If you cannot support it, the reviewer is probably right.
- **Never widen the change to satisfy a stylistic note.** Offer the follow-up
  ticket instead.
- **Do not weaken a test to make review feedback pass.** If the test now fails,
  say whether the change is wrong or the test encoded old behaviour.
