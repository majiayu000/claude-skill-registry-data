---
name: refactor-code
description: Refactor Python code to improve quality while keeping functionality intact. Use when cleaning up complexity, removing duplication, or tightening structure.
license: MIT
compatibility: claude cursor opencode
metadata:
  version: "1.0.0"
  languages: python
  audience: developers
  workflow: refactor
  since: "2026-02-25"
---

# Refactor Code

Improve readability, maintainability, and testability without changing behavior.

## When to run this skill

- You’ve been asked to clean up tangled logic or long functions
- Technical debt (duplication, inconsistent naming) is slowing future work
- Tests are hard to reason about, or core modules mix responsibilities

## Steps

1. **Code quality improvements**
   - Break large functions or classes into smaller helpers
   - Extract reusable utilities and keep them pure when possible
   - Rename variables/functions to clearly express intent
   - Replace `dict`/`tuple` blobs with Pydantic BaseModels where appropriate

2. **Reduce complexity**
   - Flatten deeply nested conditionals (guard clauses, early returns)
   - Replace repetitive code with loops/fixtures/generator helpers
   - Favor composition over inheritance; inject dependencies explicitly
   - Replace boolean flags with clear strategy objects or enums

3. **Enhance maintainability**
   - Add or strengthen type hints and docstrings
   - Centralize configuration/timeouts/paths in constants or settings modules
   - Align with SOLID principles when refactoring services or handlers
   - Improve logging and error handling so future debuggers have context

4. **Optimize but stay Pythonic**
   - Use list/dict comprehensions when they improve clarity
   - Avoid premature micro-optimizations—profile before optimizing loops
   - Keep dependencies explicit instead of hiding global state

## Checklist
- [ ] Extracted reusable functions or helpers
- [ ] Removed duplication and improved naming
- [ ] Simplified nested logic and guard clauses
- [ ] Added or improved type hints/docstrings
- [ ] Tuned logging/error handling to clarify intent
- [ ] Ensured tests cover refactored paths
