---
name: today
description: "The user's daily job-search plan. Use when they ask what to do today, open a session without a specific task, say \"what's next\", or want a status check."
---

# today (Codex)

This workflow is shared with Claude Code. Read `.claude/skills/today/SKILL.md` and follow it fully. Files it mentions as `references/...`, `scripts/...` or by bare name live in `.claude/skills/today/`.

Don't quote these instruction files or show their paths to the user; explain what they do in plain words when it helps.

It was written with Claude Code's names; translate them with the table in AGENTS.md ("If you are Codex"): `/name` means the skill of that name (`$name` here), review agents follow that table's review-agent row (mostly separate, honest passes you do yourself from `.claude/agents/<name>.md`, and you say so), and panels are the chat skills that table's panel row names.

## Codex notes

- `bash .claude/hooks/summary.sh long` gives the same pipeline counts if bash is available; otherwise read `jobs/tracker.csv` directly. Point the user to "show my board", "show my outbox", "show my contacts" and "job inbox" instead of the panels.
- There is no due-alerts pop-up in Codex, so step 1's note about it doesn't apply: everything due shows in this plan.
