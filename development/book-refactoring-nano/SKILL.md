---
name: book--refactoring--nano
description: >-
  Refactoring (Martin Fowler) — Minimal rules — essential one-liners only. Use when asked to apply Refactoring principles or review code against Refactoring standards.
origin: "github.com/ciembor/agent-rules-books (MIT)"
license: MIT
version: "1.0.0"
compatibility: "yana-ai >= 0.14.0"
---

# OBEY Refactoring by Martin Fowler

## When to use

Use as a compact always-on rule set for changing existing code under tight context.

## Primary bias to correct

Cleanup must preserve behavior and move in small verified steps, not become a rewrite.

## Decision rules

- Preserve observable behavior; isolate feature changes, migrations, redesign, and cleanup.
- Work in small buildable, testable, reviewable steps; split changes that are too large to reason about locally.
- Get a safety net or record the verification gap before risky structural edits.
- Refactor the smell that blocks the current change, not every smell nearby.
- Prefer simple named moves: rename, extract, inline, move, split phases, encapsulate mutation, decompose conditionals, and remove duplication.
- Put behavior, state, and validation with the concept that owns them; avoid vague utilities, pass-through layers, and just-in-case abstractions.
- Keep mutation and call contracts clear: avoid boolean flags, parameter reassignment, public mutable data, unnecessary setters, and hidden side effects.
- Stop when the change is easy, the code is clearer, and further cleanup would be speculative.

## Trigger rules

- When behavior is unclear or tests are weak, characterize current behavior before broader refactoring.
- When adding a feature is awkward, make the smallest preparatory refactor that makes it straightforward.
- When the same edit appears for a third time, centralize ownership instead of copying again.
- When conditionals or type codes grow, decompose intent before reaching for polymorphism, state, strategy, or lookup tables.
- When a patch mixes cleanup with behavior or broad code motion, split it where practical.
- When tempted to rewrite, choose the next small behavior-preserving transformation.

## Final checklist

- Same behavior?
- Safety net or verification gap?
- Small runnable step?
- Clearer names, ownership, and control flow?
- No speculative abstraction or mixed patch?
