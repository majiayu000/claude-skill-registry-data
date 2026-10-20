---
name: conventions
description: "Apply these opinionated testing conventions whenever writing, reviewing, or planning tests: what earns a test and what is coverage theatre, asserting outputs rather than mock calls, the three modes (functional, performance, security), naming and isolation rules, where to mock, and reporting findings for coverage rather than self-filtering. Includes house Jest standards for NestJS unit and contract tests, TDD discipline, and test-report structure."
---

# Testing

House conventions for writing tests and test strategy.

## What a test is for

A test earns its place by failing when the behaviour breaks. That single criterion resolves most arguments about what to test: if you cannot name the bug a test would catch, it is coverage theatre — it costs maintenance on every refactor and reports success while the system is broken.

Two consequences run through everything below:

- **Assert on outputs — return values, thrown errors, persisted state.** A test whose only assertion is `expect(mock).toHaveBeenCalledWith(…)` verifies the wiring you just wrote, not the behaviour. Rewrite the implementation correctly in a different shape and it fails; break the behaviour while keeping the calls and it passes. Both are the wrong way round.
- **Test decisions, not lines.** Branches, error translation, state transitions, boundary conditions. A pass-through delegator or a field mapping with no conditional has nothing to get wrong, and a test for it only breaks when someone renames a method.

Coverage percentage is a floor signal — it finds untested files. It cannot tell a valuable test from a vacuous one, so treat a high number as "nothing is empty", never as "the tests are good".

## Three modes

Ask all three of a feature; the answers rarely come from the same test.

- **Functional** — does it do the right thing, including at its edges and when it fails? For anything with a UI, that includes reachability: tab order lands somewhere sensible, controls have accessible names, and an automated axe pass is clean. A keyboard-only user hitting a dead end is a functional bug, not a polish item.
- **Performance** — does it hold up at the load and data volume it will actually see?
- **Security** — the concrete asks, per endpoint: no credentials → 401; valid credentials but wrong role → 403; another tenant's object ID → 404 or 403, never the object; malformed or oversized input → 400, not a 500; repeated requests → 429; and the response carries `nosniff`, a frame policy, and HSTS. Each is one test, and each covers a class of bug that functional tests are structured not to find.

## Conventions

- **Name tests as behaviour**: `should [outcome] when [condition]`. When it fails in CI, the name alone should say what broke — a name like `it('works')` sends the next person to read the body.
- **Tests are independent and order-free.** Shared mutable state produces failures that only reproduce in one order, and those cost days.
- **Control time, randomness, and environment.** A test that reads the real clock fails on a date boundary, in another timezone, or during the leap second — always at the worst moment, always looking like a real bug.
- **Mock at the process boundary**, not between your own units. Every internal mock is a second implementation you now maintain, and it can drift from the real one until the tests pass against a system that no longer exists.
- **Mocks mirror the real response completely.** A stub returning `{ id, name }` when production returns fifteen fields passes the test and crashes on `user.email`. Use factories with realistic defaults.
- **Never add a method to production code for a test** (`_resetForTesting`). Build a fresh instance per test instead; test concerns in production code ship to users.
- **A flaky test is a failing test.** Quarantining it and moving on trains the team to ignore red, which is the state where a real regression walks through.
- **Tier the suite by how fast it has to answer.** Unit tests run on save and should stay under about five minutes; integration on commit, under fifteen; end-to-end on the pull request, under thirty; anything slower runs nightly. The number that matters is the one a developer waits for — once the inner loop crosses a few minutes, people stop running it locally and CI becomes the first place failures appear.

## Reporting findings

When reporting test results or reviewing coverage, report everything you find, including low-severity and uncertain items — rank by severity and confidence, and let a separate pass decide what to act on. Filtering at the point of discovery loses real defects silently, and the reader cannot tell the difference between "nothing found" and "found and dropped".

`references/test-reports.md` has the report structure and severity definitions.

## References

<!-- TDD Iron Laws and Testing Anti-Patterns adapted from obra/superpowers by Jesse Vincent (@obra), MIT License -->

| Reference | Load when |
| --- | --- |
| `references/tdd-iron-laws.md` | Working test-first; red-green-refactor discipline |
| `references/testing-anti-patterns.md` | Reviewing existing tests; diagnosing tests that catch nothing |
| `references/nestjs-jest-common.md` | Any Jest test in a NestJS backend — read before the two below |
| `references/nestjs-jest-unit-tests.md` | Writing `.spec.ts` |
| `references/nestjs-jest-contract-tests.md` | Writing `.contract-spec.ts` against a live external API |
| `references/test-reports.md` | Producing a test report or defect write-up |
