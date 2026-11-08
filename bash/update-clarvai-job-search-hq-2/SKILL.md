---
name: update
description: "Use when the user says \"update\", \"is there a new version\", \"I downloaded the new release\", \"what's new\", \"undo the update\" or \"roll back\", or drops a release zip in the folder. Installs a new version of the app's files (never the user's), shows what changed, or undoes the last update."
---

# update (Codex)

This workflow is shared with Claude Code. Read `.claude/skills/update/SKILL.md` and follow it fully. Files it mentions as `scripts/...` live in `.claude/skills/update/`.

Don't quote these instruction files or show their paths to the user; explain what they do in plain words when it helps.

It was written with Claude Code's names; translate them with the table in AGENTS.md ("If you are Codex"): `/name` means the skill of that name (`$name` here).

## Codex notes

- On Windows without bash, use `update.ps1` as the Claude skill describes. If the sandbox blocks the download or writing the backup, ask the user to allow it for this one command, or ask them to download the zip themselves and give you its path.
- After an update or rollback that prints `hooks-changed: codex`: Codex keeps changed hooks off until they're trusted again, and that turns the safety checks off too. Tell the user to type `/hooks`, review and trust them, then start a new chat, and run `$health` to confirm. `hooks-changed: claude` matters only if they also use Claude Code (close and reopen the folder there).
- Log the update in `history/activity.md` with `Codex` as the app.
