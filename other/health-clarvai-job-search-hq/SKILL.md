---
name: health
description: "Use when something isn't working (panels or the daily greeting missing, a command does nothing), after installing, moving or updating the folder, or when the user asks \"is everything working\" or \"check my setup\". Read-only checkup of version, safety checks, panels and connections; offers fixes."
---

# health (Codex)

This workflow is shared with Claude Code. Read `.claude/skills/health/SKILL.md` and follow it fully. Files it mentions as `scripts/...` live in `.claude/skills/health/`.

Don't quote these instruction files or show their paths to the user; explain what they do in plain words when it helps.

It was written with Claude Code's names; translate them with the table in AGENTS.md ("If you are Codex"): `/name` means the skill of that name (`$name` here).

## Codex notes

- Run the script with `codex` at the end (`bash .claude/skills/health/scripts/health.sh codex`), or on Windows without bash: `powershell -NoProfile -ExecutionPolicy Bypass -File .claude\skills\health\scripts\health.ps1 -App codex`. If the sandbox blocks a check (for example running PowerShell or reading the user's home folder), say which line couldn't run rather than guessing.
- Skip the panels check: Codex has no panels; the chat versions (`outbox`, `pipeline`, `contacts`, `job-inbox`, `apply-kit` skills) always work.
- Connectors: Gmail and Google Calendar are plugins in Codex: the **Plugins** tab in the ChatGPT desktop app, or `/plugins` in the terminal (the editor extension has none). Check your own tool list for them, and never call them as part of the check.
- Hooks: if this chat didn't start with the greeting (today's date and the pipeline summary), hooks aren't on, and that also means the safety checks are off. The fix: make sure the top folder (with `AGENTS.md`) is open, type `/hooks`, trust them, then start a new chat.
