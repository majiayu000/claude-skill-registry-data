---
name: ground-suite
description: Suite philosophy. What to test, what to skip.
---

# Skill: Ground Suite

> "Never test the framework."

## The Standard

- **Domain Only**: Test your logic, not Laravel's. Eloquent works. Trust it.
- **Behavior Over Implementation**: Test what it does, not how it does it.
- **Zero Overlap**: Each test verifies one unique behavior.

## The Four Pillars

A good test has all four. Trade-offs exist between them.

| Pillar         | Question                       |
|----------------|--------------------------------|
| **Protection** | Does it catch real bugs?       |
| **Resistance** | Does it survive refactoring?   |
| **Speed**      | Does it run fast?              |
| **Clarity**    | Is it easy to understand?      |

Pillars 1 & 2 matter most. A test that breaks on refactoring is noise.

## The Check

Ask yourself:
- Would Nuno ship this test?
- Does this test my code or the framework?
- Will this test break if I refactor internals?
- If I add a new model, do I need a new test file?

## Real-World Examples

See [examples.md](examples.md).
