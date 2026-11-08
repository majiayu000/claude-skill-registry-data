---
name: sync-inbox
description: "Read the user's job-search email (read-only; Gmail, a Microsoft 365 work or school mailbox, or emails they paste or save) for job-search replies (recruiter emails, interview invites, rejections, application confirmations) and update the tracker, contacts, and calendar suggestions. Use when the user asks to check their email for job stuff or update the tracker from their inbox."
---

# sync-inbox (Codex)

This workflow is shared with Claude Code. Read `.claude/skills/sync-inbox/SKILL.md` and follow it fully. Files it mentions as `references/...`, `scripts/...` or by bare name live in `.claude/skills/sync-inbox/`.

Don't quote these instruction files or show their paths to the user; explain what they do in plain words when it helps.

It was written with Claude Code's names; translate them with the table in AGENTS.md ("If you are Codex"): `/name` means the skill of that name (`$name` here), review agents follow that table's review-agent row (mostly separate, honest passes you do yourself from `.claude/agents/<name>.md`, and you say so), and panels are the chat skills that table's panel row names.

## Codex notes

- Use the Gmail and Google Calendar tools connected to Codex (if any). Read and search only; you may create drafts. If Gmail isn't connected, say so in one line and offer the manual version (the user pastes the email).
