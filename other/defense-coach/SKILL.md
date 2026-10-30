---
name: defense-coach
description: Explain a finished stage to the student in Russian and check understanding with one question at a time. Use after a stage is completed or before the lab defense.
---

Read and follow the shared methodology in `.agents/skills/defense-coach/SKILL.md` (repository root).
It is the single source of truth; this file is only the Claude Code adapter.

Claude Code specifics: run commands from `lab1/` with `uv run`; respect AGENTS.md limits
(at most two concurrent subagents, writing agents in separate git worktrees).
