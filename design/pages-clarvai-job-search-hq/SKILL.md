---
name: pages
description: "Refresh, open, publish, or print the user's visual pages: the job search dashboard, interview flashcards, portfolio site, and per-job printable interview brief. Use when the user asks to see or update their dashboard, practice with flashcards, get their portfolio link, publish a page to their phone, or print an interview brief. To change how a page looks (colors, fonts, layout, animation), use page-design instead."
---

# pages (Codex)

This workflow is shared with Claude Code. Read `.claude/skills/pages/SKILL.md` and follow it fully. Files it mentions as `references/...`, `scripts/...` or by bare name live in `.claude/skills/pages/`.

Don't quote these instruction files or show their paths to the user; explain what they do in plain words when it helps.

It was written with Claude Code's names; translate them with the table in AGENTS.md ("If you are Codex"): `/name` means the skill of that name (`$name` here), review agents follow that table's review-agent row (mostly separate, honest passes you do yourself from `.claude/agents/<name>.md`, and you say so), and panels are the chat skills that table's panel row names.

## Codex notes

- Publishing pages as private claude.ai links needs Claude's Artifact tool; Codex doesn't have it. Skip "Publishing a page"; refresh the page file and open it for the user (the Codex desktop app's built-in browser, or they double-click the file). If they want a phone link, tell them to ask Claude.
