---
name: menu
description: "List everything this job-search workspace can do, in plain English. Use when the user asks what they can do, what the commands are, or how something works."
---

# menu (Codex)

This workflow is shared with Claude Code. Read `.claude/skills/menu/SKILL.md` and follow it fully. Files it mentions as `references/...`, `scripts/...` or by bare name live in `.claude/skills/menu/`.

Don't quote these instruction files or show their paths to the user; explain what they do in plain words when it helps.

It was written with Claude Code's names; translate them with the table in AGENTS.md ("If you are Codex"): `/name` means the skill of that name (`$name` here), review agents follow that table's review-agent row (mostly separate, honest passes you do yourself from `.claude/agents/<name>.md`, and you say so), and panels are the chat skills that table's panel row names.

## Codex notes

- Show the same menu with `$name` instead of `/name` (for example `$today`, `$add-job`). Drop every "(panel)" tag and the line about the pop-up when a session opens (Codex has none; `$today` shows what's due). Describe the panel lines as chat commands: board: say "show my board" (`$pipeline`); drafts: "show my outbox" (`$outbox`); network: "show my contacts" (`$contacts`); new openings: "job inbox" (`$job-inbox`); while filling in a form: "apply kit" (`$apply-kit`). Interview practice runs right in the chat.
- Drop the closing line about panels working in chat.
- End with: "You can always just say what you want in plain English."
