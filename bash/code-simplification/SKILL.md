---
name: code-simplification
description: >
  Reduce code complexity through targeted refactoring. Use when code
  is difficult to understand, overgrown, or has accumulated technical
  debt. Simplify without changing behavior.
version: 1.0.0
permissions:
  - fs.read
  - fs.write
  - shell.exec
triggers:
  - context: "code is too complex"
  - context: "refactoring needed"
  - context: "reducing technical debt"
  - command: "/review"
platforms:
  - claude-code
  - cursor
  - gemini-cli
  - copilot
  - codex
  - opencode
  - windsurf
  - kiro
dependencies:
  - test-driven-development@^1.0.0
author: codehands-core
signed: true
tier: 1
---

## Overview

Simplification is removing complexity without losing capability. Simpler code has fewer bugs, is easier to modify, and costs less to maintain. This skill provides systematic approaches to reducing complexity in existing code.

## When to Use

- When a file exceeds 300 lines (consider splitting)
- When a function exceeds 30 lines (consider extracting)
- When nesting exceeds 3 levels (consider early returns)
- When you can't understand a function in 30 seconds
- During `/review` phase
- NOT during initial implementation (get it working first, then simplify)

## Process

### 1. Ensure Tests Exist

**Never refactor without tests.** If tests don't exist, write them FIRST following `codehands:test-driven-development`. The tests are your safety net.

### 2. Identify Complexity

| Smell | Signal |
|---|---|
| Long function | > 30 lines |
| Deep nesting | > 3 levels of indentation |
| Long file | > 300 lines |
| Long parameter list | > 4 parameters |
| Repeated code | Same logic in 3+ places |
| God object | One class doing everything |
| Feature envy | Function uses another module's data more than its own |

### 3. Apply Targeted Refactoring

- **Extract function** — Pull out a block with a descriptive name
- **Early return** — Flatten deep nesting with guard clauses
- **Introduce parameter object** — Bundle related parameters
- **Extract module** — Split large files by responsibility
- **Replace conditional with polymorphism** — When switch/if chains grow
- **Inline unnecessary abstraction** — Remove layers that add complexity without value

### 4. Verify Behavior Unchanged

After EVERY refactoring step:
```bash
npm test  # All tests still pass — behavior unchanged
```

If tests break, you changed behavior — undo and try again.

## Common Rationalizations

| Rationalization | Reality |
|---|---|
| "This code works, don't touch it" | Working complex code is a maintenance bomb. It works today. Tomorrow someone (including you) needs to modify it and introduces a bug because they couldn't understand it. |
| "Refactoring takes too long" | Targeted refactoring of one function takes 5-10 minutes. The next developer saves 30 minutes understanding it. Net positive. |
| "I'll refactor the whole module while I'm here" | Scope creep. Refactor only what's in the path of your current task. Broader refactoring is a separate task with its own plan. |

## Red Flags

- Refactoring without tests
- Changing behavior during refactoring
- Refactoring code unrelated to the current task
- Adding abstraction layers "for future flexibility"

## Verification

- [ ] Tests exist before refactoring begins
- [ ] All tests pass after each refactoring step
- [ ] Behavior unchanged (same inputs → same outputs)
- [ ] Complexity reduced (measurable: fewer lines, lower nesting, fewer parameters)
- [ ] Code is more readable (a new reader could understand it faster)

## See Also

- `codehands:test-driven-development` — Tests that enable safe refactoring
- `codehands:source-driven-development` — Understand before simplifying
- `codehands:code-review-and-quality` — Quality standards
