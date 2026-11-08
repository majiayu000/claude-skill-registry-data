---
name: page-review
description: "One-pass quality review of the user's pages, print templates and the Claude panels: accessibility, layout, readability, color contrast, motion, print, and interface copy. Use after any change to how one of them looks or behaves, or when the user asks whether a page looks right."
---

# page-review (Codex)

This workflow is shared with Claude Code. Read `.claude/skills/page-review/SKILL.md` and follow it fully. Files it mentions as `references/...`, `scripts/...` or by bare name live in `.claude/skills/page-review/`.

Don't quote these instruction files or show their paths to the user; explain what they do in plain words when it helps.

It was written with Claude Code's names; translate them with the table in AGENTS.md ("If you are Codex"): `/name` means the skill of that name (`$name` here), review agents follow that table's review-agent row (mostly separate, honest passes you do yourself from `.claude/agents/<name>.md`, and you say so), and panels are the chat skills that table's panel row names.

## Codex notes

- The panels only run inside Claude Code. Here you can review their code and copy by reading it, but you can't open them or run `claude plugin validate`/`test`; mark those checks "Not verified".
