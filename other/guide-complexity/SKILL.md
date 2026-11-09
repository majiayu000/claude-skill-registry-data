---
name: guide-complexity
description: "Use when code is written or changed that branches heavily, in any language: if/else or switch chains, type-check cascades, kind fields compared to strings, flag parameters, deep nesting. Produces the branching shaped before it lands, and the bar it must meet at merge. Not for auditing or reworking existing code (complexity-rework)."
---

# Guide: complexity

**Applies** to any code that adds or grows branching: a chain of conditions, a dispatch on a kind, a flag that changes what a function does, nesting past two levels.

## Shaping step

1. Before writing the branch, name what varies: the kinds, the cases.
2. Put each case behind one shape: a table, a map of handlers, a type per kind, one function per flag value.
3. Keep each function one level of decision; extract the rest.
4. The branching already exists and is to be reworked: run the `complexity-rework` skill.

## Ok at merge

- No new chain of more than three conditions on the same value.
- No kind compared to strings in more than one place; no boolean flag parameter.
- Nesting at most two levels in the changed code.
