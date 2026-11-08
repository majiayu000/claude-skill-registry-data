---
name: weekly-review
description: "Weekly check-in on the user's job search: activity vs goals, funnel conversion, what's working, skill gaps, what to change next week. Use on Fridays/Sundays, when the user asks how their search is going, or what skills to learn for the jobs they want."
---

# weekly-review (Codex)

This workflow is shared with Claude Code. Read `.claude/skills/weekly-review/SKILL.md` and follow it fully. Files it mentions as `references/...`, `scripts/...` or by bare name live in `.claude/skills/weekly-review/`.

Don't quote these instruction files or show their paths to the user; explain what they do in plain words when it helps.

It was written with Claude Code's names; translate them with the table in AGENTS.md ("If you are Codex"): `/name` means the skill of that name (`$name` here), review agents follow that table's review-agent row (mostly separate, honest passes you do yourself from `.claude/agents/<name>.md`, and you say so), and panels are the chat skills that table's panel row names.

## Codex notes

- Without panels, show the board in chat (see the `pipeline` skill) and the drafts list (see the `outbox` skill).
