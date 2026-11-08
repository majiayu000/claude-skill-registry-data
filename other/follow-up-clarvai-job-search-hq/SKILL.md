---
name: follow-up
description: "Find every application and contact whose follow-up is due and draft the messages into the Outbox. Use when the user asks about follow-ups, says they haven't heard back, or /today shows items due."
---

# follow-up (Codex)

This workflow is shared with Claude Code. Read `.claude/skills/follow-up/SKILL.md` and follow it fully. Files it mentions as `references/...`, `scripts/...` or by bare name live in `.claude/skills/follow-up/`.

Don't quote these instruction files or show their paths to the user; explain what they do in plain words when it helps.

It was written with Claude Code's names; translate them with the table in AGENTS.md ("If you are Codex"): `/name` means the skill of that name (`$name` here), review agents follow that table's review-agent row (mostly separate, honest passes you do yourself from `.claude/agents/<name>.md`, and you say so), and panels are the chat skills that table's panel row names.

## Codex notes

- When drafts are ready, tell the user to say "show my outbox" (there's no panel in Codex). For LinkedIn messages they send by hand, ask them to tell you when each one went out (the `contacts` skill records it).
