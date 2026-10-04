---
name: tdd
description: Use before writing any implementation code — enforces RED-GREEN-REFACTOR cycle.
---

# Test-Driven Development

## The Cycle

**RED → GREEN → REFACTOR**

Never skip RED. Never write code before a failing test exists.

## Steps

1. **Write the failing test** — specific, tests one behavior
2. **Run it and confirm it fails** — with the right error message
3. **Write minimal code to make it pass** — no more than needed
4. **Run it and confirm it passes**
5. **Refactor if needed** — tests still pass after refactor
6. **Commit** — small, frequent commits

## Anti-Patterns to Avoid

- Writing implementation before tests
- Tests that pass without any implementation (false green)
- Testing implementation details instead of behavior
- One giant test instead of small focused tests
- Skipping the refactor step

## Verification Command

Always show the exact command to run tests and expected output at each RED/GREEN step.
