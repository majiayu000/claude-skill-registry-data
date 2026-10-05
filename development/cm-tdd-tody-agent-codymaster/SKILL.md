---
name: cm-tdd
description: Use when implementing any feature or bugfix. Routes to the core Red-Green-Refactor loop, test quality guidance, rationalization handling, examples, or stuck-state recovery.
token_budget: 1500
token_core: 380
token_refs:
  red-green-refactor: 620
  test-quality: 360
  rationalizations: 520
  bugfix-example: 340
  stuck-debugging: 260
compressed: true
deprecated: false
---

# Test-Driven Development (TDD)

## TL;DR
- **Use when** writing or fixing code
- **Cycle**: Red → Green → Refactor
- **Rule**: no production code without a failing test first
- **Next**: `cm-execution` or `cm-code-review`

## When to Use
- new features
- bug fixes
- refactors
- behavior changes

## The Iron Law
```text
NO PRODUCTION CODE WITHOUT A FAILING TEST FIRST
```

## Choose the Need

```
Need to execute the normal TDD loop?
└─ YES → Red-Green-Refactor

Need help designing or reviewing test quality?
└─ YES → Test Quality

Need to counter "skip TDD" rationalizations?
└─ YES → Rationalizations

Need a worked bug-fix example?
└─ YES → Bugfix Example

Are you blocked or unsure how to continue?
└─ YES → Stuck / Debugging
```

| Need | Summary | Load |
|---|---|---|
| Normal execution | core TDD loop and verification | `references/red-green-refactor.md` |
| Test quality | what good tests look like | `references/test-quality.md` |
| Reinforcement | anti-rationalization guidance | `references/rationalizations.md` |
| Example | concrete bug-fix walkthrough | `references/bugfix-example.md` |
| Recovery | how to proceed when stuck | `references/stuck-debugging.md` |

## Load Rules
- Load `red-green-refactor.md` for normal execution.
- Load `test-quality.md` when designing or reviewing tests.
- Load `rationalizations.md` only when the user or agent is trying to bypass TDD discipline.
- Load `bugfix-example.md` only for coaching or example use.
- Load `stuck-debugging.md` only when blocked.

## Non-Negotiables
- Watch the test fail before writing production code.
- Keep implementation minimal until green.
- Refactor only after green.
- Re-run verification after each meaningful change.

## The Bottom Line
**Write the failing test first. Pass it minimally. Refactor only after green.**
