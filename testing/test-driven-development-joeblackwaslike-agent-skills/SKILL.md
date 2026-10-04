---
name: test-driven-development
description: >
  Use when implementing any feature, fixing any bug, or changing behavior in TypeScript
  or Python — and whenever the user mentions TDD, test-first, test-driven, red-green-refactor,
  "write tests", "add tests", unit/integration tests, pytest, vitest, jest, mocking/test
  doubles, coverage gates, or retrofitting tests onto a legacy codebase. Teaches the full
  TDD discipline (the Iron Law, red-green-refactor, the Three Laws, FIRST, AAA/GWT,
  triangulation), with extensive runnable TypeScript (Vitest) and Python (pytest) examples,
  test-double/mocking guidance and anti-patterns, how to bootstrap TDD into a new OR existing
  repo, advanced patterns (outside-in, double-loop, property-based, controlling time/IO), and
  WHY test-first produces better software specifically when an AI agent writes the code. This
  is the comprehensive companion to the terse `superpowers:test-driven-development` enforcer —
  use both: that one to stay disciplined in the loop, this one for depth, examples, and setup.
metadata:
  last_updated: "2026-06-25"
---

# Test-Driven Development

Write the test first. Watch it fail. Write the minimum code to pass. Refactor. Repeat.

**Core principle:** if you didn't watch the test fail, you don't know that it tests the
right thing. A test written after the code passes immediately — and passing immediately
proves nothing.

This skill is the deep reference. For the in-the-loop discipline enforcer (the short,
rigid version you re-read every time you're tempted to skip a step) use
`superpowers:test-driven-development`. They don't conflict: that skill keeps you honest,
this skill teaches you the craft and sets up your repo to make it cheap.

## The Iron Law

```
NO PRODUCTION CODE WITHOUT A FAILING TEST FIRST
```

Wrote code before the test? Delete it. Don't keep it as "reference", don't "adapt" it
while writing the test, don't even look at it. Implement fresh from the test. The deletion
feels wasteful (it's sunk cost); keeping code you never watched a test catch is the real
debt.

**Violating the letter of the rule is violating the spirit of the rule.** Every "this case
is different because…" is a rationalization. See `references/principles.md` for the full
rationalization table.

## Red-Green-Refactor

```
RED      Write ONE small failing test for the next behavior.
         Run it. Watch it FAIL — for the expected reason (feature missing, not a typo).
GREEN    Write the SIMPLEST code that makes it pass. No extra features (YAGNI).
         Run it. Watch it PASS. All other tests still green. Output pristine.
REFACTOR Remove duplication, improve names, extract helpers — tests stay green.
         Add NO new behavior here.
→ next failing test
```

The two "watch it" steps are mandatory and the most-skipped. Verifying RED proves the test
can fail; verifying GREEN proves your code is what made it pass. Skip either and you're not
doing TDD — you're writing code and hoping.

## Route first

Pick the reference that matches the task.

| Task | Read |
| --- | --- |
| The discipline in full — Iron Law, RGR, Three Laws, FIRST, AAA/GWT, triangulation, what makes a good test, the rationalization table | `references/principles.md` |
| **Why test-first matters *more* when an AI agent writes the code** — evidence, rationalization resistance, regression safety, design feedback | `references/why-tdd-with-ai-agents.md` |
| Worked, runnable TypeScript examples (Vitest; Jest deltas noted) — unit, async, DI vs mocks, integration, bug-as-test, refactor | `references/typescript-examples.md` |
| Worked, runnable Python examples (pytest) — fixtures, parametrize, mock vs DI, async, Hypothesis, bug-as-test | `references/python-examples.md` |
| Test doubles (dummy/stub/spy/mock/fake), London vs Detroit schools, when to mock, mocking anti-patterns | `references/test-doubles-and-mocking.md` |
| Setting up TDD in a **new** TS or Python repo, or **retrofitting** it onto a legacy untested codebase — configs, scripts, watch loop, coverage gate, CI | `references/bootstrapping-a-repo.md` |
| Outside-in vs inside-out, double-loop / acceptance TDD, property-based testing, controlling time/randomness/IO/databases, when NOT to TDD | `references/advanced-patterns.md` |
| Free, CC-licensed TDD books — condensed notes + how to get the full texts locally | `references/books/README.md` |

## When to use TDD (and the rare exceptions)

**Always:** new features, bug fixes, refactors, behavior changes.

**Exceptions (confirm with your human partner first):** throwaway spikes/prototypes
(then *delete the spike* and re-implement under TDD — don't adapt it), generated code, and
pure config files. "This one's too simple to test" is not an exception — simple code breaks
and the test costs 30 seconds.

## How TDD composes with the other disciplines

- **Bug?** → `superpowers:systematic-debugging`: find root cause, then write a failing test
  that reproduces it, then fix. The test proves the fix and prevents the regression. Never
  fix a bug without a test.
- **Claiming done?** → `superpowers:verification-before-completion`: run the full suite
  fresh, read the output, count failures. For a regression test, prove it red-green: revert
  the fix, watch the new test FAIL, restore the fix, watch it pass.
- **Building an agent/skill/MCP server?** → `best-practices-for-agentic-development`. The
  same test-first loop applies to process docs (see `why-tdd-with-ai-agents.md`).

## Completion criteria

Before marking TDD work done:

- [ ] Every new function/method has a test you watched fail first.
- [ ] Each test failed for the *expected* reason (missing behavior, not a typo/import error).
- [ ] You wrote the minimal code to pass each test (no speculative options/params).
- [ ] The full suite passes; output is pristine (no stray errors/warnings).
- [ ] Tests exercise real behavior; mocks only where unavoidable, and you don't assert on
      the mock itself (see `references/test-doubles-and-mocking.md`).
- [ ] Edge cases and error paths covered, not just the happy path.

Can't check every box? You skipped TDD. Start over.
