---
name: flutter-corpus-ingestion
description: Change or verify the Flutter docs grabber, cleaning or chunking. Use when the source, include/exclude rules, parser or chunking strategy changes; produces a manifest, a corpus diff and an idempotency check.
---

Read and follow the shared methodology in `.agents/skills/flutter-corpus-ingestion/SKILL.md` (repository root).
It is the single source of truth; this file is only the Claude Code adapter.

Claude Code specifics: run commands from `lab1/` with `uv run`; respect AGENTS.md limits
(at most two concurrent subagents, writing agents in separate git worktrees).
