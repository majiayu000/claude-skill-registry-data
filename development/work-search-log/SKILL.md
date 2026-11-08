---
name: work-search-log
description: "Use when the user mentions unemployment benefits, work search, a weekly certification or claim, their Universal Credit journal or work coach, or asks what they did this week. Builds the work-search record benefits programs ask for, from the tracker and contacts. The user files it themselves."
---

# work-search-log (Codex)

This workflow is shared with Claude Code. Read `.claude/skills/work-search-log/SKILL.md` and follow it fully. Files it mentions as `references/...`, `scripts/...` or by bare name live in `.claude/skills/work-search-log/`.

Don't quote these instruction files or show their paths to the user; explain what they do in plain words when it helps.

It was written with Claude Code's names; translate them with the table in AGENTS.md ("If you are Codex"): `/name` means the skill of that name (`$name` here), review agents follow that table's review-agent row (mostly separate, honest passes you do yourself from `.claude/agents/<name>.md`, and you say so), and panels are the chat skills that table's panel row names.

## Codex notes

- There's no page preview here: tell the user where the printable week is, and offer to open it in their browser.
