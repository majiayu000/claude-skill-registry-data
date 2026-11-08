---
name: routines
description: "Use when the user wants automatic checks: new jobs every morning, watching their inbox, daily follow-up drafts, a weekly review, checking saved postings are still open, or asks to 'automate', 'schedule' or 'run this every day'. Sets up opt-in routines on their own computer that only read, draft and track, and spots ones that stopped running."
---

# routines (Codex)

This workflow is shared with Claude Code. Read `.claude/skills/routines/SKILL.md` and follow it fully. Files it mentions as `references/...`, `scripts/...` or by bare name live in `.claude/skills/routines/`.

Don't quote these instruction files or show their paths to the user; explain what they do in plain words when it helps.

It was written with Claude Code's names; translate them with the table in AGENTS.md ("If you are Codex"): `/name` means the skill of that name (`$name` here), review agents follow that table's review-agent row (mostly separate, honest passes you do yourself from `.claude/agents/<name>.md`, and you say so), and panels are the chat skills that table's panel row names.

## Codex notes

- Give the Codex steps from step 3 (the **Scheduled** view in the ChatGPT desktop app, this folder's local project, not a worktree). In the terminal or editor extension, say scheduled tasks are managed in the ChatGPT desktop app, and offer to set them up there next time the user opens this folder in it.
- In scheduled mode, log as `Codex (routine)`. Where a step says the Job Inbox panel, results are in the `job-inbox` skill ("job inbox").
