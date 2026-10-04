---
name: tdd
description: Run red-green-refactor in vertical slices, emphasizing behavior-first tests and harness quality gates.
---

# tdd

Use test-driven development to deliver features/fixes in small behavior-focused increments.

## Core principles

- Test observable behavior via public interfaces.
- Avoid coupling tests to internal implementation details.
- Work in vertical slices: one failing test -> minimal passing code -> repeat.
- Refactor only while green.

## Workflow

### 1) Plan behavior and boundaries

Before coding:

- Confirm target behavior with the user (or issue AC)
- Identify public interface changes
- Select highest-value behaviors to test first
- Spot deep-module opportunities (simple interface, deep internals)

### 2) Tracer bullet first

Create one thin end-to-end test that proves a real path.

```
RED: write one failing behavior test
GREEN: write minimal code to pass
```

### 3) Incremental red-green loop

For each next behavior:

```
RED: next failing behavior test
GREEN: minimal implementation
```

Rules:

- One test at a time
- No speculative implementation
- Keep assertions on externally visible outcomes

### 4) Refactor pass

When all current tests are green:

- Remove duplication
- Deepen modules where complexity is leaking
- Tighten names/interfaces
- Re-run test suite after each refactor step

Never refactor while red.

## Test quality checklist

- Test describes behavior (not internals)
- Test uses public interfaces only
- Test survives internal refactor
- Added code is minimal for current failing test
- No dead code or TODO placeholders

## Harness verification gates

After meaningful changes, run:

```bash
bun run typecheck
bun run lint
bun test
```

If a sub-repo defines different commands, follow that sub-repo's `AGENTS.md`.

## Beads integration

Use beads to track TDD slices:

```bash
bd create --type task --title "TDD slice: <behavior>" --description "<expected behavior and test scope>" --priority 2 --repo .
bd comments add <id> "worklog: red->green completed for <behavior>"
```

## Deep-dive references

Bundled with this skill (self-contained — no external repos required):

- [tests.md](tests.md) — concrete good vs. bad test examples
- [interface-design.md](interface-design.md) — designing interfaces for testability
- [deep-modules.md](deep-modules.md) — small interface, deep implementation
- [mocking.md](mocking.md) — mock only at system boundaries
- [refactoring.md](refactoring.md) — refactor candidates after green

## Attribution

The bundled deep-dive docs ([tests.md](tests.md), [interface-design.md](interface-design.md),
[deep-modules.md](deep-modules.md), [mocking.md](mocking.md), [refactoring.md](refactoring.md)) are
vendored **verbatim** from the `tdd` skill in [mattpocock/skills](https://github.com/mattpocock/skills).
This `SKILL.md` is an Agent Forge adaptation of the same concepts (Beads tracking + harness quality
gates). Original work © 2026 Matt Pocock, MIT License:

> Permission is hereby granted, free of charge, to any person obtaining a copy of this software and
> associated documentation files (the "Software"), to deal in the Software without restriction,
> including without limitation the rights to use, copy, modify, merge, publish, distribute,
> sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is
> furnished to do so, subject to the following conditions: The above copyright notice and this
> permission notice shall be included in all copies or substantial portions of the Software.
> THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND.
