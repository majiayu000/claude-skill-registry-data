---
name: requirements-to-issues
description: Turn a new or changed lab requirement into a GitHub Issue with dependencies, acceptance criteria and expected evidence. Use when docs/requirements.md gains a row or a requirement changes.
---

Read and follow the shared methodology in `.agents/skills/requirements-to-issues/SKILL.md` (repository root).
It is the single source of truth; this file is only the Claude Code adapter.

Claude Code specifics: run commands from `lab1/` with `uv run`; respect AGENTS.md limits
(at most two concurrent subagents, writing agents in separate git worktrees).
