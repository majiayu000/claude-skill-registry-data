---
name: lcp-git-commit
description: When asked to commit, write clear git commit messages (50/72, present tense, subsystem prefixes like go-lcpd:).
metadata:
  short-description: Craft git commit messages for this repo
---

Use this skill only when the user explicitly asks you to create commits.

## Commit message style

Follow this structure:

- First line: short summary (aim for 50 chars or less).
- Blank line.
- Body (optional): wrap at ~72 columns; explain intent and rationale.

Guidelines:

- Use present tense (example: “Fix …”, not “Fixed …”).
- Include a subsystem/package prefix when it improves scanability:
  - Examples: `go-lcpd: …`, `apps/openai-serve: …`, `docs: …`, `docs/protocol: …`
  - For broad changes, combine prefixes with `+` (example: `go-lcpd+docs: …`).
- Prefer small, contained commits that build independently to support `git bisect`.
- Bullets are fine in the body; keep them readable and wrapped.

## When asked to commit

1. Confirm which files belong in the commit (avoid committing local/dev artifacts like `go.work.sum`).
2. Craft a commit message following the style above.
3. Create the commit(s) with clear boundaries (one topic per commit when practical).
