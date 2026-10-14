---
name: ground-orientation
description: Context loading. Solves cold start.
---

# Skill: Orientation

> "A craftsman measures twice before cutting once."

## When

Run this at session start or when you feel lost.

## The Protocol

1. **Read Memory**: `$MEMORY_DIR/working.md`, `$MEMORY_DIR/blueprint.md`.
2. **Read Decisions**: `ls docs/*/ADR`, read relevant ADRs.
3. **State**: "Oriented. Mode: [Planning/Execution]. Task: [Name]."

## The Anti-Patterns

- **Diving in**: Starting to code without reading context.
- **Assuming**: Guessing project conventions instead of discovering them.
- **Forgetting**: Not re-orienting after context switches.

## The Output

State: "Oriented. Mode: [X]. Active Task: [Y]. Constraints: [ADR-001]."
