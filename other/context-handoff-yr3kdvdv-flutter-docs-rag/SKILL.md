---
name: context-handoff
description: Write docs/handoffs/latest.md and update docs/PROJECT_STATE.md at the end of a task or before switching agents, following docs/HANDOFF_TEMPLATE.md.
---

Read and follow the shared methodology in `.agents/skills/context-handoff/SKILL.md` (repository root).
It is the single source of truth; this file is only the Claude Code adapter.

Claude Code specifics: run commands from `lab1/` with `uv run`; respect AGENTS.md limits
(at most two concurrent subagents, writing agents in separate git worktrees).
