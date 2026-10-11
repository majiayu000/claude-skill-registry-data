---
name: commit-message
description: Write a conventional commit message from the actual diff — subject ≤50 chars, honest body.
trigger: when the user asks for a commit message or to commit changes
---
## When to use
The user asks for a commit message, or asks you to commit staged work.

## How
1. Look at the real change first: `git diff` / `git status` via the git tool
   (or read the files just edited). Never write from memory of the chat.
2. Format — Conventional Commits:
   - `type(scope): subject` — type ∈ feat/fix/docs/refactor/test/build/ci/chore.
   - Subject ≤50 chars, imperative mood ("add", not "added"), no period.
   - Body only when the *why* isn't obvious from the subject — wrap at 72.
3. One logical change per message; if the diff mixes concerns, say so and
   suggest splitting.
4. Breaking change → `!` after type/scope + `BREAKING CHANGE:` footer.

## Avoid
- Describing the diff line-by-line — the diff already shows *what*.
- Vague subjects: "fix stuff", "update code", "wip".
- Inventing scope names not used in the repo's history (`git log --oneline`
  shows the convention).

## Done well
`git log --oneline` reads like a changelog: each subject states one change
precisely, and bodies explain non-obvious whys.
