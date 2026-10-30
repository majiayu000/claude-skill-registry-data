---
name: rag-experiment
description: Run one controlled RAG experiment (chunking, embeddings, top-k, rerank, threshold, prompt or LLM) and save config, raw results, metrics and run IDs. Use when testing a hypothesis from docs/RESEARCH_PLAN.md.
---

Read and follow the shared methodology in `.agents/skills/rag-experiment/SKILL.md` (repository root).
It is the single source of truth; this file is only the Claude Code adapter.

Claude Code specifics: run commands from `lab1/` with `uv run`; respect AGENTS.md limits
(at most two concurrent subagents, writing agents in separate git worktrees).
