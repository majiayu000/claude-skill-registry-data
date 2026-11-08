---
name: cover-letter
description: "Write a short, specific, human-sounding cover letter for a job from the user's real experience. Use when the user asks for a cover letter or an application requires one."
---

# cover-letter (Codex)

This workflow is shared with Claude Code. Read `.claude/skills/cover-letter/SKILL.md` and follow it fully. Files it mentions as `references/...`, `scripts/...` or by bare name live in `.claude/skills/cover-letter/`.

Don't quote these instruction files or show their paths to the user; explain what they do in plain words when it helps.

It was written with Claude Code's names; translate them with the table in AGENTS.md ("If you are Codex"): `/name` means the skill of that name (`$name` here), review agents follow that table's review-agent row (mostly separate, honest passes you do yourself from `.claude/agents/<name>.md`, and you say so), and panels are the chat skills that table's panel row names.

## Codex notes

- The make-pdf script needs bash plus Chrome or Edge. On Windows without Git Bash, use the `make-pdf.ps1` command given in the skill. Run it exactly as the skill writes it, from the top folder: this folder's rules let that command run outside the sandbox once the folder is trusted. If the sandbox still blocks the browser, run the same command again asking to run it outside the sandbox (one approval for the user); only if that is refused or fails, or neither script can run at all, treat it as `no-browser` and give the user the manual Print → Save as PDF steps.
- Do the company-researcher pass yourself with your web search (spawn the `company-researcher` project agent only if the user asks).
