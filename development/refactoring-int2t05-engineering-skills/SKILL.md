---
name: refactoring
description: Execute an agreed structural move while preserving behavior. Triggers on "refactor structure", "重构结构".
---

# Refactoring

## When to use

- Execute an agreed structural move while preserving behavior.

**Not for:** codebase-design for choosing boundaries; simplify for local clarity.

## Steps

1. Define the move and behavior contract; establish tests or characterization evidence.

2. Plan incremental file, symbol, import and ownership changes; use automation for repetitive moves.

3. Move coherent units and run affected checks; separate features and use compatibility only for actual consumers.

4. Verify old references, exports, packaging, documents and runtime paths.

## Verify

- Contracts are preserved; moved symbols resolve and abandoned references are removed.

## References

- [engineering-principles.md](../../../references/engineering-principles.md) — shared decision boundaries, scope and verification.
- [references/refactoring-catalog.md](references/refactoring-catalog.md) — before→after examples + characterization-test guidance for each move (extract, move, split, merge, change-dependency)
