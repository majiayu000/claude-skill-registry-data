---
name: quick-recap
description: Use when the user wants each agent response to end with a red/yellow/green status line showing whether the work is finished, pending a follow-up, or blocked on input.
category: bdb-core
source: BuilderIO/skills
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

## Activation

The convention applies only while this skill is loaded or the user asks for it.
AOS does not inject a managed `AGENTS.md` / `CLAUDE.md` block for it.

Choose the status from the user's perspective: finished, pending a specific
non-routine step, or blocked.

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
