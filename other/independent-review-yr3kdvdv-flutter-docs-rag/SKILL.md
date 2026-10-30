---
name: independent-review
description: Review a ready PR or commit against requirements with evidence. Use for review of a specific SHA; reports findings with priority, file/line, scenario, evidence and minimal fix.
---

Read and follow the shared methodology in `.agents/skills/independent-review/SKILL.md` (repository root).
It is the single source of truth; this file is only the Claude Code adapter.

Claude Code specifics: run commands from `lab1/` with `uv run`; respect AGENTS.md limits
(at most two concurrent subagents, writing agents in separate git worktrees).
