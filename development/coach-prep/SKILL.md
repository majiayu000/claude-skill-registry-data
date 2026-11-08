---
name: coach-prep
description: "Use when the user has (or wants) a meeting with a career coach, their school's career office, an advisor or a mentor, asks how to find one, says 'I'm seeing my career coach', or just had that meeting. Builds a one-page brief to bring (where they stand, what they've tried, what to ask, what to send ahead) and records the advice and next steps afterward."
---

# coach-prep (Codex)

This workflow is shared with Claude Code. Read `.claude/skills/coach-prep/SKILL.md` and follow it fully. Files it mentions as `references/...`, `scripts/...` or by bare name live in `.claude/skills/coach-prep/`.

Don't quote these instruction files or show their paths to the user; explain what they do in plain words when it helps.

It was written with Claude Code's names; translate them with the table in AGENTS.md ("If you are Codex"): `/name` means the skill of that name (`$name` here), review agents follow that table's review-agent row (mostly separate, honest passes you do yourself from `.claude/agents/<name>.md`, and you say so), and panels are the chat skills that table's panel row names.

## Codex notes

- The user finds and books the meeting themselves. When a thank-you draft is ready, tell the user to say "show my outbox".
