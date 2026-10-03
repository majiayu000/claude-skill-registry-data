---
name: debug
description: Systematically diagnose and resolve a bug or unexpected behavior — reproduce, isolate, hypothesize, instrument, and verify. Use when the user reports a bug, says "this doesn't work", "why is this broken", or encounters unexpected behavior.
allowed-tools: Read, Grep, Glob, Bash
---

# Systematic Debugging

Read `learnings.md` beside this file before starting; append an entry when a bug's root cause defied a category below.

## Governing Principle

> **Bugs are information gaps.** Debugging is not guessing — it is a systematic process of narrowing the gap between expected and actual behavior until the root cause is isolated and verifiable.

## Procedure

1. **Reproduce** — confirm the bug exists and is deterministic. If the user hasn't described exact steps, ask. If it's intermittent, instrument logging before proceeding.

2. **Isolate** — narrow the scope:
   - **Discover** the entry point: which route, server function, or component is involved?
   - Trace the data flow from trigger to symptom. Read the code path, don't guess.
   - Identify the boundary where expected behavior diverges from actual behavior.

3. **Hypothesize** — form exactly ONE testable hypothesis. State it as: "The bug occurs because [X] causes [Y] at [file:line]." Never hold multiple hypotheses simultaneously — test one, discard or confirm, then move to the next.

4. **Instrument** — add the minimum observation needed to confirm or reject the hypothesis:
   - Console.log at the divergence point (remove after)
   - Read error output carefully — the first error in a stack is usually the root cause
   - Check types: is the runtime value what the type signature claims?
   - Check timing: is an async operation completing before it's consumed?

5. **Fix** — apply the narrowest possible change that addresses the root cause, not the symptom. **Constrain** the fix:
   - Does it match the project's established patterns? (`/patterns`)
   - Does it introduce a new failure mode?
   - Is the fix in the right layer? (data bug → fix in service, not in component rendering)

6. **Verify** — confirm the fix resolves the original reproduction AND doesn't break adjacent behavior:
   - Run the project's linter and type-checker
   - If tests exist, run them
   - Manually trace the fixed code path once more

## Common Bug Categories

| Category | First thing to check |
|---|---|
| **Type mismatch** | Runtime value vs declared type — look for `as any` casts hiding the real type |
| **Async race** | Missing `await`, check-then-act without atomicity (TOCTOU) |
| **State desync** | Cache not invalidated after mutation, stale closure in a hook |
| **Boundary violation** | Server code imported client-side, env variable missing at runtime |
| **Null path** | Optional field accessed without guard, empty array not handled |

## Constraints

- **Never guess-and-check.** Read the code path before changing anything.
- Remove all debugging instrumentation (console.log, temp vars) before considering the fix complete.
- If the bug reveals a missing pattern or architectural gap, flag it — don't silently patch around it.

## Handoffs

- Bug reveals a design problem → `/system-design`.
- Fix needs to follow an established pattern → `/patterns`.
- User wants to understand why the bug existed → `/teach`.
- Fix complete → `/full-review` to validate.
