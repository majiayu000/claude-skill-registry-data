---
name: git-commit-hygiene
description: "Draft and review Git commits and commit messages with an emphasis on atomic change sets and clean history. Use when asked to commit changes, propose commit messages, split/squash/rebase commits, or clean up a branch via fixup commits and interactive rebase/autosquash."
---

# Git Commit Hygiene

Use this skill as the playbook for producing reviewable commits and clean commit history.

## Default workflow

1. Confirm intent: should we commit now, and should history be cleaned (fixups/rebase) or left as-is?
2. Decide commit boundaries: identify independent changes and split them into separate commits.
3. Stage intentionally: stage only what belongs in the current commit.
4. Write the message: short imperative subject, optional body for rationale.
5. (Optional) Clean up history: fixup commits + rebase/autosquash when appropriate.

## Atomic commits

- Keep commits small, focused, and atomic.
- Avoid commits that mix unrelated changes (e.g., "Address feedback").

## History hygiene

Prefer fixups and rebasing when working on a branch that isn’t upstream yet, or on a PR that is still in draft.

- Create a fixup commit against the target commit: `git commit --fixup <sha>`
- Autosquash during interactive rebase: `git rebase -i --autosquash <base>`
- If there are multiple fixups, repeat and rebase again until the branch tells a clean, coherent story.

## Commit message guidelines

Follow these best practices when drafting commit messages:

1. Write a short subject line:
   - Up to 50 chars
   - Start subject with a capital letter, don’t end with a period
   - Use imperative mood (e.g. "Fix memory leak while scrolling widget")
   - If the project uses conventional commits, use them too
2. Leave a blank line between subject and body
3. Only when needed (don’t force it for trivial changes), write a body:
   - Wrap lines at 72 chars
   - Focus on "what" and "why", not the "how"
     - Explain the motivation
     - Mention side effects, trade-offs, or alternatives considered
     - Reference relevant issue IDs / tickets at the bottom if known
