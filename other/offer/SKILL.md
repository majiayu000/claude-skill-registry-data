---
name: offer
description: "Use when the user gets a job offer, is deciding between offers, asks whether to accept, wants to negotiate salary, or asks for a counteroffer. Helps evaluate and compare offers (total compensation, cost of living, growth) and drafts negotiation or acceptance messages. The user accepts or declines themselves."
---

# offer (Codex)

This workflow is shared with Claude Code. Read `.claude/skills/offer/SKILL.md` and follow it fully. Files it mentions as `references/...`, `scripts/...` or by bare name live in `.claude/skills/offer/`.

Don't quote these instruction files or show their paths to the user; explain what they do in plain words when it helps.

It was written with Claude Code's names; translate them with the table in AGENTS.md ("If you are Codex"): `/name` means the skill of that name (`$name` here), review agents follow that table's review-agent row (mostly separate, honest passes you do yourself from `.claude/agents/<name>.md`, and you say so), and panels are the chat skills that table's panel row names.

## Codex notes

- Unpublishing pages (in "Closing the search") needs Claude; tell the user to ask Claude, or skip it.
