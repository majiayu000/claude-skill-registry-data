---
name: tdd
description: Use when implementing features or bug fixes test-first.
---

# Test-Driven Development

Red then green. Consult this before and during the loop, not after.

Read `CONTEXT.md` if it exists so test names match the domain glossary. Respect ADRs.

## Good test

Tests verify behavior through public interfaces, not internals. A good test reads like a spec and survives refactors.

## Seams

A seam is the public boundary you test at. Test only at pre-agreed seams. Write the seams down before the first test. Confirm with the human if they are in the session. No test at an unconfirmed seam.

## Anti-patterns

- Implementation-coupled: mocks internals, private methods, or side channels.
- Tautological: expected value recomputed the way the code does.
- Horizontal slicing: all tests then all implementation. Use one test, one implementation, repeat.

## Loop

- Red before green.
- One seam, one test, one minimal implementation per cycle.
- Refactoring is not part of this loop. It belongs to `/code-review`.
