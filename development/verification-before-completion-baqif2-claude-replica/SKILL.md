---
name: Verification Before Completion
description: Before submitting code or creating a Pull Request, when about to claim that work is complete, fixed, or passed, you must run verification commands and confirm the output results before making any success claims; evidence must appear before any assertions---
---

## Overview

Claiming work is complete without verification is dishonest, not efficient.

**Core principle: evidence first, always.**

**Violating the literal wording of this rule is equivalent to violating its spirit.**

## Iron rule

```
No completion claims without fresh verification evidence.
```

If you did not run verification commands in this message, you cannot claim it passed.

## Gatekeeping mechanism

```
Before making any status claim or expressing satisfaction:

1. Identify: which command proves the claim?
2. Execute: run the full command (fresh, complete)
3. Read: review full output, check exit code, count failures
4. Verify: does the output confirm the claim?
   - If no: state the actual status and provide evidence
   - If yes: confirm the claim and attach evidence
5. Only then: make the claim

Skipping any step = lying, not verifying
```

## Common mistakes

| Claim | Needs | Not enough |
|------|------|------|
| Tests pass | Test output: 0 failures | Last run result, or "should pass" |
| Lint is clean | Lint output: 0 errors | Partial checks, or inference |
| Build succeeds | Build exit code: 0 | Lint passes, or logs look fine |
| Issue fixed | Original symptom test: passes | Code changed, but assumed fixed |
| Regression test valid | Red-green cycle verified | Test only passes once |
| Agent task done | VCS diff shows changes | Agent reports "success" |
| Requirements met | Checklist verified item by item | Tests pass |

## Red alert - stop!

- Using "should", "maybe", "looks like"
- Expressing satisfaction before verification ("Great!", "Perfect!", "Done!", etc.)
- Preparing to commit/push/create PR without verification
- Trusting an agent's success report
- Relying on partial verification
- Thinking "just this once"
- Tired and wanting to quit
- **Any wording that implies success without running verification**

## Prevent rationalization

| Excuse | Reality |
|------|------|
| "It should work now" | Must run verification |
| "I am confident" | Confidence != evidence |
| "Just this once" | No exceptions |
| "Lint passed" | Lint != compiler |
| "Agent said it worked" | Must verify independently |
| "I am tired" | Tired != exemption |
| "Partial checks are enough" | Partial checks prove nothing |
| "Different wording, so rule does not apply" | Follow spirit, not letter |

## Key patterns

**Tests:**
```
OK [run test command] [see: 34/34 passed] "All tests pass"
NO "It should pass now" / "Looks correct"
```

**Regression testing (TDD red-green cycle):**
```
OK Write -> run (pass) -> undo fix -> run (must fail) -> restore -> run (pass)
NO "I wrote a regression test" (without red-green verification)
```

**Build:**
```
OK [run build] [see: exit code 0] "Build passed"
NO "Lint passed" (lint does not compile)
```

**Requirement satisfaction:**
```
OK Re-read plan -> make checklist -> verify each -> report gaps or completion
NO "Tests pass, phase done"
```

**Agent delegation:**
```
OK Agent reports success -> check VCS diff -> verify changes -> report actual status
NO Trust agent report
```

## Why this matters

Based on 24 failure experiences:
- Teammate said: "I do not believe you" - trust is broken
- Shipped undefined functions -> crashes
- Shipped missing requirements -> incomplete feature
- Wasted time on false completion -> context switch -> rework
- Violated: "Honesty is a core value. If you lie, you will be replaced."

## When it applies

**Always before:**
- Any success/completion claim variants
- Any expression of satisfaction
- Any positive statement about work status
- Committing code, creating PR, task completion
- Switching to the next task
- Delegating to an agent

**This rule applies to:**
- Exact phrases
- Synonyms or paraphrases
- Implied success meaning
- Any communication that hints completion or correctness

## Summary

**There are no shortcuts in verification.**

Run the command, read the output, then make the claim.

This is non-negotiable.
