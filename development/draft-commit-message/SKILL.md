---
name: draft-commit-message
description: Draft a Conventional Commits message in markdown when the user asks for a commit message/commit msg (e.g., "commit msg?", "commit message", "msg in md"). Use for any request to write or format a git commit message.
---

# Draft Commit Message

## Overview

Draft a Conventional Commits message from a provided change summary. Always return the commit message in markdown format.

## Workflow

1. Read the user's change summary. If missing, ask for it.
2. Produce a Conventional Commits message in the format `type(scope): summary`.
3. Keep the summary under 72 characters and use the imperative mood.
4. If there are breaking changes, add a `BREAKING CHANGE:` footer.
5. Return the result in markdown (a fenced code block is preferred).

## Output Rules

- Always use `type(scope): summary`.
- Use a short, imperative summary (max 72 characters).
- Include `BREAKING CHANGE:` only when applicable.
- Keep to the user's requested scope if provided; otherwise infer a reasonable scope from the change summary.

## Examples (for internal guidance)

- User: "commit msg?"
  - Output in markdown with a Conventional Commit message.
- User: "msg in md for this change"
  - Output in markdown only.
