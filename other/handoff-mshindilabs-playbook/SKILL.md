---
name: handoff
description: >
  Write a handoff document that lets a fresh agent or session continue the current work. Use on request only: "write a handoff", "hand this off", "I'm starting a new session, summarise where we are". Saves outside the workspace and points at existing specs, plans, issues and commits instead of repeating them.
license: MIT
metadata:
  upstream: mattpocock/skills@49dd158d skills/productivity/handoff
---

# Handoff

Write a handoff document summarising the current conversation so a fresh agent can continue the work. Save it to the temporary directory of the user's OS (`$TMPDIR`, else `/tmp`; `%TEMP%` on Windows), not the current workspace, and tell the user the full path.

If the user said what the next session is for, tailor the document to that.

## What goes in

- **Goal**: what the user asked for, in their words where it matters.
- **State**: what is done, what is in progress, and what is not started. Name the branch, and say whether work is committed, pushed, or only on disk.
- **Decisions**: each decision the user made and the reason, so the next agent does not reopen it.
- **Next step**: the one thing to do first, concrete enough to start without asking.
- **Not verified**: anything claimed but not checked, and any check that is failing.
- **Suggested skills**: the skills the next agent should load for this work.

## What stays out

Do not repeat content that already lives in another artifact: a spec, a plan, an ADR, an issue, a commit, a diff. Reference it by path or URL.

Redact sensitive information: API keys, passwords, tokens, and personal data.
