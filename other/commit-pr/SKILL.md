---
name: commit-pr
description: Propose a short git commit subject and a copy-pasteable markdown PR description for the current changes.
---

# Commit and PR description

Provide the following for the current changes:

1. A git commit description **50 characters or fewer**.
2. A copy-pasteable markdown PR description **400 characters or fewer**.

Propose only; do not commit, push, or create a PR.

## Inspect

- Read `git status --short`, `git diff`, and `git diff --staged`.
- Read `git log --oneline -10` to match commit conventions.
- Describe staged changes when present; otherwise use the full working diff, inspecting relevant untracked files.
- If staged and unstaged changes differ, briefly state that the output covers staged changes.

## Write

1. **Commit description: 50 characters or fewer.**
   Use imperative mood, match the repository's prefix convention, and omit a trailing period.
   Describe the change, not a file list.
2. **PR description: 400 characters or fewer.**
   Start with one summary line explaining the purpose, then a blank line and short bullet points covering relevant behavior changes or reviewer context.
   Omit headings, badges, footers, and boilerplate.

## Verify and present

- Measure both strings with a command, counting all characters, including spaces, newlines, and markdown.
- Shorten and remeasure until both limits pass; report only measured counts.
- Put each output in a separate fenced code block, using a `markdown` fence for the PR description.
- Follow each block with its character count; exclude fences and count labels from the limits.
- Add at most one line of commentary.
