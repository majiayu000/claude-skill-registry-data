---
name: langgraph-patterns-expert
description: Use for LangGraph agent design and refactors. Prefer explicit state, small nodes, and clear transitions.
---

## Guidelines

- Keep `State` explicit and typed.
- Keep nodes small, single-purpose, and testable.
- Make branching conditions explicit.
- Prefer idempotent steps where possible.
