---
name: draft-commit-message
description: Draft a conventional commit message when the user asks for help writing a commit message.
metadata:
  short-description: Draft an informative commit message.
---

Draft a conventional commit message that matches the change summary provided by the user.

Requirements:

- Use the Conventional Commits format: `type(scope): summary`
- Use the imperative mood in the summary (for example, "Add", "Fix", "Refactor")
- Keep the summary under 72 characters
- If there are breaking changes, include a `BREAKING CHANGE:` footer