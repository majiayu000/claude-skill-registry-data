---
name: incremental-implementation
description: >
  Build features in small, verifiable steps with continuous test validation.
  Use when implementing any feature from a plan. Each step should produce
  a working, tested increment. Prevents large, unverified code drops.
version: 1.0.0
permissions:
  - fs.read
  - fs.write
  - shell.exec
triggers:
  - context: "implementing a feature"
  - context: "following a plan"
  - command: "/build"
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
  - planning-and-task-breakdown@^1.0.0
model_variants:
  claude:
    enforcement_style: "human-partner collaborative"
  gemini:
    enforcement_style: "structured-checklist"
  gpt:
    enforcement_style: "directive-imperative"
author: codehands-core
signed: true
tier: 1
---

## Overview

Incremental implementation turns plans into code through small, verified steps. Each step adds ONE behavior, proves it works with a test, and leaves the codebase in a working state. No large code drops. No "I'll test it all at the end."

## When to Use

- When implementing tasks from an approved plan
- When building any feature larger than a single function
- When modifying existing code that has tests
- NOT for exploratory spikes (use a throwaway branch)

## Process

### The Increment Cycle

For every plan task, repeat this cycle:

```
1. Read the task → 2. Write failing test → 3. Implement minimum →
4. All tests pass → 5. Commit → 6. Next task
```

### Rules

1. **One behavior per increment.** Each increment adds exactly one testable behavior. Not two. Not "this and also while I'm here..."
2. **Tests pass after every increment.** The FULL test suite, not just the new test.
3. **Commit after every green increment.** Small commits with clear messages. Each commit is a valid rollback point.
4. **Never break existing tests.** If your change breaks an existing test, understand why before proceeding. Don't just update the test to match.
5. **Follow the plan order.** Tasks have dependency ordering for a reason. Don't skip ahead.

### When Things Go Wrong

- **Test won't pass → Use `codehands:systematic-debugging`** — Don't thrash.
- **Task is bigger than expected → Split it.** Re-plan mid-implementation if a task will take > 15 minutes.
- **Requirements are unclear → Ask.** Don't implement an assumption.
- **Existing code needs changes you didn't plan → Note it,** complete the current task, then add a cleanup task.

## Common Rationalizations

| Rationalization | Reality |
|---|---|
| "I'll implement the whole feature and test at the end" | Large code drops are where bugs hide. Every increment that isn't tested is a gamble. |
| "These two changes are related, I'll do them together" | Related is not the same as inseparable. Implement one, test it, commit, then implement the other. |
| "Committing after every small change creates noise" | Small commits are not noise — they're rollback points. `git log --oneline` is easy to read. Debugging a 500-line commit is not. |

## Red Flags

- Uncommitted changes spanning multiple unrelated behaviors
- Tests not run between increments
- "I'll add tests at the end" for any increment
- Skipping plan task order without re-planning

## Verification

- [ ] Each increment adds exactly one testable behavior
- [ ] All tests pass after every increment
- [ ] Each increment is committed with a descriptive message
- [ ] Plan tasks completed in dependency order

## See Also

- `codehands:test-driven-development` — TDD cycle within each increment
- `codehands:planning-and-task-breakdown` — Plan that drives increments
- `codehands:source-driven-development` — Read before writing each increment
