---
name: test-driven-development
description: >
  Enforce strict test-driven development with the Iron Law: no production
  code without a failing test first. Use when implementing any feature,
  fixing any bug, or modifying any behavior. Covers Red-Green-Refactor
  cycle, test pyramid, Prove-It Pattern for bugs, and DAMP test writing.
version: 1.0.0
permissions:
  - fs.read
  - fs.write
  - shell.exec
triggers:
  - context: "implementing a feature"
  - context: "fixing a bug"
  - context: "writing code"
  - context: "modifying behavior"
  - command: "/build"
  - command: "/test"
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
  - verification-before-completion@^1.0.0
model_variants:
  claude:
    enforcement_style: "human-partner collaborative"
    iron_law_phrasing: "Your human partner expects tests first. Write the failing test, show it fails, then implement."
  gemini:
    enforcement_style: "structured-checklist"
    iron_law_phrasing: "CHECKLIST: ☐ Write failing test ☐ Confirm RED ☐ Write minimal code ☐ Confirm GREEN ☐ Refactor"
  gpt:
    enforcement_style: "directive-imperative"
    iron_law_phrasing: "You MUST write a failing test before any production code. No exceptions. Violation = delete the code."
author: codehands-core
signed: true
tier: 0
---

## Overview

Test-Driven Development is the single most impactful engineering practice for AI coding agents. Without it, agents produce untested, unreliable code. CodeHands enforces the strictest TDD discipline: **the Iron Law**.

## When to Use

- When implementing ANY new feature or behavior
- When fixing ANY bug (use the Prove-It Pattern)
- When refactoring existing code (tests must pass before and after)
- When modifying API contracts (update contract tests first)
- NOT when writing documentation, configuration, or non-code files

## The Iron Law

> **NO PRODUCTION CODE WITHOUT A FAILING TEST FIRST.**
>
> If you wrote production code before writing a test, **delete it**. Not "save it as reference." Not "keep it and add a test." DELETE it. Then write the test. Then rewrite the production code to make the test pass.
>
> This is not a guideline. This is the law.

Why deletion, not "just add a test after"? Because:
1. Tests written after the code test the implementation, not the requirement
2. You cannot verify the test would have caught a real bug if it was written to match existing code
3. It reinforces the discipline that prevents the rationalization spiral

## Process

### Phase 1: RED — Write a Failing Test

1. **Understand the requirement.** What should the code do? What are the inputs and outputs?
2. **Write a test that describes the desired behavior.** Use DAMP names (Descriptive And Meaningful Phrases):
   ```
   GOOD: test_returns_404_when_user_not_found()
   BAD:  test_get_user_error()
   ```
3. **Run the test.** Confirm it FAILS. If it passes, your test is wrong — it's not testing new behavior.
4. **Read the failure message.** It should clearly describe what's missing.

### Phase 2: GREEN — Make It Pass

5. **Write the MINIMUM code** to make the test pass. Not elegant code. Not complete code. The minimum.
6. **Run the test.** Confirm it PASSES.
7. **Run the full test suite.** Confirm nothing else broke.

### Phase 3: REFACTOR — Clean Up

8. **Now improve the code.** Extract functions, rename variables, remove duplication.
9. **Run the test suite after every change.** If tests fail, your refactoring changed behavior — undo it.
10. **Commit.** The test and the code go in the same commit.

### Repeat

Each cycle should take 2-10 minutes. If a cycle takes longer than 15 minutes, you're writing too much at once — break it down.

## Test Pyramid

Follow the test pyramid for balanced coverage:

```
        ╱  E2E  ╲          5% — Full user journeys
       ╱─────────╲
      ╱Integration╲       15% — Component boundaries
     ╱─────────────╲
    ╱    Unit Tests  ╲    80% — Individual functions/modules
   ╱─────────────────╲
```

| Level | Scope | Speed | # of Tests |
|---|---|---|---|
| **Unit** | Single function/module | < 10ms | Many (80%) |
| **Integration** | Component boundaries, API contracts | < 1s | Moderate (15%) |
| **E2E** | Full user journeys | Seconds | Few (5%) |

**The Beyonce Rule:** "If you liked it, you should have put a test on it." If a behavior is important enough to keep, it's important enough to test.

## The Prove-It Pattern (Bug Fixes)

For every bug fix, follow this exact sequence:

1. **Reproduce** — Write a test that exposes the bug. Run it. It MUST fail.
2. **Fix** — Implement the minimal fix.
3. **Verify** — Run the reproduction test. It MUST pass.
4. **Regression** — Run the full test suite. Nothing else should break.

This proves the bug was real, the fix works, and nothing regressed. Skip any step and you haven't proven anything.

## Test Quality Standards

### DAMP Over DRY in Tests

Tests should be **D**escriptive **A**nd **M**eaningful **P**hrases, even at the cost of some repetition:

```python
# DAMP (preferred) — each test tells a complete story
def test_login_fails_with_expired_token():
    user = create_user(email="test@example.com")
    token = create_token(user, expired=True)
    response = login(token=token)
    assert response.status == 401
    assert response.error == "Token expired"

# DRY (avoid) — shared setup hides intent
def test_expired_token():
    response = self.login(self.expired_token)
    self.assert_unauthorized(response)
```

### What Makes a Bad Test

- **Tests implementation, not behavior.** If you can refactor without changing behavior and the test breaks, it's a bad test.
- **Flaky.** If it fails intermittently, fix or delete it. Flaky tests erode trust.
- **Non-deterministic.** Tests that depend on time, random numbers, or external services without mocking.
- **Snapshot abuse.** Snapshot tests for complex objects create maintenance burden with no behavioral insight.

## Common Rationalizations

| Rationalization | Reality |
|---|---|
| "I'll write the tests after the code works" | This is the #1 cause of untested production code. Once code "works," there's no incentive to test it. Write tests first. |
| "This function is too simple to test" | If it's too simple to test, it's too simple to break. But it CAN break — via integration, refactoring, or dependency changes. Test it. |
| "I need to see if the approach works first" | Use a spike branch. Throw the spike away. Then TDD the real implementation. Spikes that become production code are the enemy. |
| "The test would just be testing the framework" | If your code delegates to a framework, test the delegation — not the framework internals. Verify you're calling the right method with the right arguments. |
| "There's no existing test infrastructure" | Setting up the test framework IS the first task. Create the test runner, write one trivial test, verify it passes. Then proceed. |
| "I already know this code works" | You don't know it works. You believe it works. Belief is not evidence. Write the test. |
| "I'll keep the code as reference and add tests" | No. Delete the code. If you can't rewrite it from the test, you didn't understand it well enough to ship it. |
| "TDD doesn't work for UIs" | TDD works for UI logic, state management, and data transformation. Use component tests. Visual aspects can use snapshot tests sparingly. |

## Red Flags

- Production code committed without corresponding tests
- Tests that were clearly written after the code (test names mirror implementation, not behavior)
- Test file added in a DIFFERENT commit than the production code
- "I tested it manually" as justification
- Test suite not run before committing
- High code coverage but tests that don't assert meaningful behavior
- Zero test failures in a development session (suggests tests aren't being written first)
- Spike code that becomes production code without being rewritten via TDD

## Verification

- [ ] Every new behavior has a corresponding test committed in the same changeset
- [ ] Tests were written BEFORE production code (Red → Green → Refactor sequence followed)
- [ ] All tests pass: `npm test` / `pytest` / `go test ./...` / equivalent
- [ ] Test names describe behavior, not implementation (DAMP naming)
- [ ] Bug fixes include a reproduction test that proves the fix
- [ ] Test pyramid is balanced (not all E2E, not all unit)
- [ ] No flaky tests introduced

## See Also

- `codehands:verification-before-completion` — Confirm work is actually done
- `codehands:systematic-debugging` — When tests reveal deeper issues
- `codehands:code-review-and-quality` — Tests reviewed alongside code
- `references/testing-patterns.md` — Framework-specific test patterns
- `references/testing-anti-patterns.md` — Common testing mistakes
