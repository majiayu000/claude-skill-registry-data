---
name: clarify-before-acting
description: Stop when the owning repo, customer or outcome, or plan-versus-implement choice is missing. Ask at most two questions. Use at the start of Cursor sessions and before switching to implementation.
title: "Clarify Before Acting"
kind: "platform-adapter"
domain: "platforms"
status: "active"
owner: "APT"
last_updated: "2026-09-06"
source_paths: ["apt-principles-agents/platforms/cursor/source/skills/clarify-before-acting/SKILL.md"]
---

# Clarify Before Acting

Canonical procedure: `skills/thinking/clarify-before-acting/SKILL.md` (installed under `.apt/skills/thinking/clarify-before-acting/` or the source repo). This wrapper only adds Cursor mechanics.

## Cursor mechanics

- Prefer the structured question tool when it is available. Otherwise ask in chat.
- Ask at most one or two questions, then stop. Do not keep using tools behind the question.
- Do not spawn Task subagents until the stop condition is cleared.
- For product intent gaps, open Working Backwards intake. Do not draft requirements or code.
- Record `[OPEN - owner: name]` or `[BLOCKER - owner: name]`. Blockers prevent implementation.
