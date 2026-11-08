---
name: find-jobs
description: "Search the web for new job postings that fit the user (at the level that matches their career stage, former employers always included). Use when the user asks to find jobs, look for openings, see what's out there, or search a company or role they haven't picked a posting for yet. When they already have specific links, use add-job."
---

# find-jobs (Codex)

This workflow is shared with Claude Code. Read `.claude/skills/find-jobs/SKILL.md` and follow it fully. Files it mentions as `references/...`, `scripts/...` or by bare name live in `.claude/skills/find-jobs/`.

Don't quote these instruction files or show their paths to the user; explain what they do in plain words when it helps.

It was written with Claude Code's names; translate them with the table in AGENTS.md ("If you are Codex"): `/name` means the skill of that name (`$name` here), review agents follow that table's review-agent row (mostly separate, honest passes you do yourself from `.claude/agents/<name>.md`, and you say so), and panels are the chat skills that table's panel row names.

## Codex notes

- Do the job-scout pass yourself with your web search (spawn the `job-scout` project agent only if the user asks).
