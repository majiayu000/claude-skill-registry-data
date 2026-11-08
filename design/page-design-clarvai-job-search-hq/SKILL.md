---
name: page-design
description: "Use when the user asks to restyle, recolor, re-theme, change the look, use their brand or design system, or redesign their pages or resume template (\"make it navy and gold\", \"bigger text\", \"less motion\"). Changes theme, colors, fonts, text size, layout, animation and print. Not for wording."
---

# page-design (Codex)

This workflow is shared with Claude Code. Read `.claude/skills/page-design/SKILL.md` and follow it fully. Files it mentions as `references/...`, `scripts/...` or by bare name live in `.claude/skills/page-design/`.

Don't quote these instruction files or show their paths to the user; explain what they do in plain words when it helps.

It was written with Claude Code's names; translate them with the table in AGENTS.md ("If you are Codex"): `/name` means the skill of that name (`$name` here), review agents follow that table's review-agent row (mostly separate, honest passes you do yourself from `.claude/agents/<name>.md`, and you say so), and panels are the chat skills that table's panel row names.

## Codex notes

- The palette tools (`palette.mjs`, `tokens.mjs`) need Node. If it isn't installed, do what the Claude skill says: keep the current palette and tell the user colors can't be contrast-checked here. Font, layout and motion changes don't need Node (a layout switch is the one `data-layout` attribute per file; see "Without Node"); run a page-review pass after any change.
