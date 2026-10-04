---
name: explore
description: "Deep-dive into a codebase area. Traces execution paths, maps architecture, documents dependencies and patterns."
argument-hint: "[feature-or-area]"
allowed-tools: Read Grep Glob Bash
model: gpt-5.3-codex
---

# /explore — Codebase Deep Dive

Analyze: **$ARGUMENTS**. See `agents/code-explorer.md`.

1. **Entry points** — Find main entry points for the feature/area
2. **Execution tracing** — Follow call chains, note branching and async boundaries
3. **Architecture mapping** — Identify layers, communication patterns, boundaries
4. **Pattern recognition** — Document patterns, naming conventions, abstractions
5. **Dependencies** — Map external libraries and internal module dependencies
6. **Recommendations** — Patterns to follow, utilities to reuse, anti-patterns to avoid
