---
name: quick-recap
description: "Add or follow a red, yellow, or green status-line convention. Use for compact agent completion status."
license: MIT
compatibility: "Works in Claude Code, Codex, Cursor, and Agent Skills-compatible harnesses when the required host tools are available."
metadata:
  author: Builder.io
  source: BuilderIO/skills
  source-commit: fd8f20a879b507cf09feba08663a1edf7a949353
  owner: software-factory
  risk: medium
  capabilities: builderio,status-reporting
---

# Quick Recap

Make completion state obvious at the end of every response.

## Status Block

Every response that completes a unit of work must end with:

```md
🟢 Actual concise status sentence
```

Rules:

- Keep the status line under 100 characters.
- Use `🟢` when the requested work is finished.
- Use `🟡` when non-routine follow-up remains; name the pending item.
- Use `🔴` only when blocked on user input.
- Put the status line at the very end of the response.
- Do not add `---`, spacer lines, or any content after the status line.

## Installer Behavior

This convention is only automatic when it is present in project or user
instructions. When installing this skill, prefer adding the managed
`AGENTS.md` / `CLAUDE.md` block unless the user opts out.

If you are following the convention manually, choose the status from the user's
perspective: finished, pending a specific non-routine step, or blocked.

## Examples

Finished work:

```md
🟢 Updated quick recap docs with output examples
```

Non-routine follow-up remains:

```md
🟡 Code updated, set PROVIDER_WEBHOOK_SECRET before testing webhooks
```

Blocked on user input:

```md
🔴 Need the production API key to continue
```
