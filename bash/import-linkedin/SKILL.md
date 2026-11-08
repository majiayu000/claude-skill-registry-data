---
name: import-linkedin
description: "Use the user's own LinkedIn data export (not scraping) to check their profile against their resume and find contacts at target companies. Use when the user wants to use their LinkedIn, find who they know somewhere, or drops a LinkedIn export in imports/."
---

# import-linkedin (Codex)

This workflow is shared with Claude Code. Read `.claude/skills/import-linkedin/SKILL.md` and follow it fully. Files it mentions as `references/...`, `scripts/...` or by bare name live in `.claude/skills/import-linkedin/`.

Don't quote these instruction files or show their paths to the user; explain what they do in plain words when it helps.

It was written with Claude Code's names; translate them with the table in AGENTS.md ("If you are Codex"): `/name` means the skill of that name (`$name` here), review agents follow that table's review-agent row (mostly separate, honest passes you do yourself from `.claude/agents/<name>.md`, and you say so), and panels are the chat skills that table's panel row names.

## Codex notes

- Unzipping: Mac/Linux/Git Bash exactly `unzip -n "imports/<file>.zip" -d "imports/<file-name-without-.zip>"`; Windows PowerShell `Expand-Archive -LiteralPath "imports\<file>.zip" -DestinationPath "imports\<file-name-without-.zip>"` (no `-Force`, so nothing is overwritten). Keep the quotes: downloaded names often have spaces or `(1)`. Ask before any other form.
