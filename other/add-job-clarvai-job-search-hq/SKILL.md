---
name: add-job
description: "Use whenever the user shares a job link (any job board or company careers page) or a pasted posting, says \"add this job\", or pastes several links. Saves each posting with every detail needed to apply, checks fit and scams, adds it to the tracker, and preps the application package for good fits."
---

# add-job (Codex)

This workflow is shared with Claude Code. Read `.claude/skills/add-job/SKILL.md` and follow it fully. Files it mentions as `references/...`, `scripts/...` or by bare name live in `.claude/skills/add-job/`.

Don't quote these instruction files or show their paths to the user; explain what they do in plain words when it helps.

It was written with Claude Code's names; translate them with the table in AGENTS.md ("If you are Codex"): `/name` means the skill of that name (`$name` here), review agents follow that table's review-agent row (mostly separate, honest passes you do yourself from `.claude/agents/<name>.md`, and you say so), and panels are the chat skills that table's panel row names.

## Codex notes

- Codex has no WebFetch tool: read postings with your web search, or open the link in the Codex desktop app's built-in browser (Handshake, for students, needs the user signed in there once). If a page still won't load, ask the user to paste the posting text.
