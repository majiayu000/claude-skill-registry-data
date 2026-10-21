---
name: context-engineering
description: Assemble relevant context or explain an existing code path. Triggers on "agent lacks context", "解释这段代码".
---

# Context Engineering

## When to use

- Assemble relevant context or explain an existing code path.

**Not for:** handoff for transferring work; research for external investigation.

## Steps

1. Choose explanation or execution-context mode and identify audience and exact question.

2. Trace actual definitions, callers, entry points and tests; distinguish instructions from external or quoted data.

3. Explain purpose, inputs, meaningful calls and outputs, or provide task goals, constraints, selected paths and verification commands.

4. Reconcile conflicts or ask about unresolved decisions; preserve confirmed context during compaction.

## Verify

- Symbols and paths exist; the explanation follows actual calls and avoids irrelevant repository dumps.

## References

- [engineering-principles.md](../../../references/engineering-principles.md) — shared decision boundaries, scope and verification.
- [references/context-strategies.md](references/context-strategies.md) — context packing strategies (brain dump, selective include, hierarchical summary), MCP integration table, anti-patterns.
- [references/code-explanation.md](references/code-explanation.md) — explaining existing code and giving codebase tours to a user
