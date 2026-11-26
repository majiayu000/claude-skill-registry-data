---
name: test-designer
version: 1.1.1
description: Test suite design - separate logic tests (fast, in-process, deterministic) from e2e tests (few, real boundaries), ban sleep-based waits, injectable clocks, readiness polling, redundancy pruning, flake triage. Use when designing, splitting, reviewing or fixing a test suite, or when tests sleep, wait fixed times or flake.
---

# Test Designer

Designs the shape of a test suite: which behavior is proven by which tier, and how tests wait without waiting. Stack-agnostic. A test that passes because enough wall-clock time went by is a bug waiting for a slow CI runner. Companion to [tdd](../../workflows/tdd/SKILL.md) (the loop) and [performance-reviewer](../performance-reviewer/SKILL.md). Skeletons in [RECIPES.md](RECIPES.md).

## 1. When to invoke

- Designing the test layout of a new feature, service or repo.
- A suite is slow, flaky, or mixes unit-style and end-to-end checks in one file.
- A test contains `sleep`, a fixed timeout, or "wait a bit then assert".
- Reviewing a PR that adds tests, or deciding where a new test belongs.

## 2. Two tiers, never mixed

| | Logic tests | E2E tests |
|---|---|---|
| Proves | Rules, branching, transformations, state transitions, error mapping | A real user or client journey works across real boundaries |
| Runs | In-process; real code, fakes for I/O | Against a running system (real process, DB, browser, network) |
| Time | Milliseconds each; whole tier in seconds | Seconds each; whole tier in minutes |
| Count | Many; every rule and edge case | Few; one per critical journey |
| Determinism | Total: no network, no real clock, no randomness | Best effort; made stable by readiness signals, not delays |

- **One tier per test file.** Separate directories or tags (`tests/logic/`, `tests/e2e/`), separate CI jobs and separate commands. Logic runs on every save and commit; e2e runs on PR, merge or schedule.
- **Decide the tier by what the assertion needs.** If the claim is about a rule, a logic test must be able to prove it; reaching for e2e to prove a rule is a design smell in the code, not a testing need.
- **E2E never re-proves edge cases.** Edge cases live in logic tests; e2e asserts the journey wires together.
- **Test through the public interface**, as in [tdd](../../workflows/tdd/SKILL.md). Mock only at system boundaries (network, clock, filesystem, randomness), never your own modules.

## 3. No time-based waiting

A test must never pass or fail because of how long it waited.

- **Banned:** `sleep(n)`, fixed `setTimeout`/`waitForTimeout`, "retry 3 times with 1s pause then assert", asserting elapsed wall-clock time.
- **Replace with the thing you were actually waiting for**, in this order:
  1. **Await the signal** - a returned promise/future, a joined thread, a closed channel, a callback, an event the code under test emits.
  2. **Control the clock** - inject a fake clock and advance it explicitly (section 4).
  3. **Poll a condition with a deadline** - loop on the observable state (row exists, port accepts, element visible) with short intervals and one generous overall timeout. The deadline is a failure bound, never the expected duration.
- **Timeouts are ceilings.** A passing test should finish as soon as the condition holds; the timeout only bounds a hang. Name it (`READY_TIMEOUT`), keep it in one place.
- **Assertion framework waits count.** Web-first auto-waiting assertions (`expect(locator).toBeVisible()`) are condition polling and fine; a hand-written `wait 2000` before them is not.

## 4. Make time and randomness injectable

- **Inject a clock** (`now()`, `sleep()`, `timer`) into code with timeouts, retries, TTLs, debounce, schedules or backoff. Production passes the real one; logic tests pass a fake that advances on command.
- **Test the retry/backoff policy as arithmetic**: assert the sequence of requested delays from the fake clock, never real elapsed time.
- **Inject randomness and IDs** (seeded RNG, fixed UUID source) so output is reproducible.
- **Never read ambient time or env inside business logic**; take it as a parameter or dependency. That one change makes most time-based tests unnecessary.

## 5. Logic tests

- Pure or in-process only: no network, no real DB, no real clock, no filesystem outside a temp dir.
- Replace I/O with in-memory fakes that behave like the real thing (a repository backed by a map), not with call-counting mocks that assert implementation.
- One behavior per test, arranged as given / when / then; the name states the behavior.
- Table-driven cases for rule matrices; property-based tests for invariants when the stack supports them.
- Budget: the whole tier runs in seconds. A logic test over ~100 ms is suspect; find the hidden I/O or sleep.

## 6. E2E tests

- **Pick journeys, not features**: sign-up to first value, checkout, the one flow that pages someone at 3 a.m. Typically 5-20 per product.
- **Start from readiness, not from a delay**: wait on a health endpoint, a log line, an open port or a visible element before the first step.
- **Own your data**: each test creates and cleans its own records with unique identifiers; no order dependence, no shared mutable fixtures.
- **Isolate from third parties**: stub external services you do not own at the network edge; keep your own services real.
- **Parallel-safe by default**: unique ports, schemas or tenants per worker.
- **Capture evidence on failure** (trace, screenshot, logs) instead of adding retries.
- **Retries are a diagnostic, not a fix.** One retry in CI may be allowed only with the flake reported and tracked; a test that needs it is quarantined with an owner and a deadline.

## 7. Shape and budget

- **Pyramid, not diamond or cone**: many logic tests, fewer integration tests at real seams (DB, queue, HTTP client), fewest e2e. If e2e count rivals logic count, rules are being proven at the wrong tier.
- **Integration tests** (one real dependency, e.g. a repository against a real database in a container) sit between the tiers; treat them as a third lane with their own directory and job, waiting on readiness like e2e.
- **CI order**: logic first (fail fast), then integration, then e2e. A logic failure skips the slower jobs.
- **Report durations.** Track the slowest tests; a test that grows slower without a reason is a regression.

## 8. Redundancy

More tests is not more safety. Each test costs run time and maintenance, so it must be able to fail for a reason no other test catches.

- **Prove each rule once, at the lowest tier that can.** If a logic test covers it, drop the integration or e2e assertion of the same rule.
- **A test must be able to fail for a real behavior change.** Delete tests that mirror the implementation: a mock asserting it was called, an expected value computed with the same code under test, a snapshot nobody reviews.
- **Merge near-duplicates** into one table-driven test; keep one case per distinct equivalence class and boundary, not ten similar inputs.
- **Skip trivial code with no logic**: plain getters/setters, pass-through wrappers, generated code, framework behavior. Cover them through the behavior that uses them.
- **Prune before adding.** When a bug lands, add the one test that would have caught it; if an existing test already should have, fix that test instead.
- **Coverage is a map, not a target.** A line executed by a test with no meaningful assertion is not covered.

## 9. Flake triage

When a test is intermittent, classify before touching it:

1. **Hidden wait** - sleep or timeout standing in for a signal. Fix: section 3.
2. **Shared state** - order dependence, leaked data, reused port. Fix: isolate per test.
3. **Ambient time/randomness** - midnight, DST, month-end, unseeded RNG. Fix: section 4.
4. **Real race in the product** - the test is right and the code is wrong. Fix the code.
5. **Environment** - resource starvation, version drift. Fix the environment, pin versions.

Never "fix" by raising a timeout or adding a retry unless the diagnosis is that the ceiling was too low for a genuinely slow, signalled operation.

## 10. Review checklist

- [ ] Every test file belongs to exactly one tier, by directory or tag.
- [ ] No `sleep`, fixed wait or elapsed-time assertion; waits are signals, fake clocks or deadline-bounded polling.
- [ ] Time, randomness and IDs are injected where behavior depends on them.
- [ ] Rules and edge cases are proven by logic tests; e2e covers journeys only.
- [ ] Logic tier has no network, real clock or shared state.
- [ ] E2E tests are readiness-gated, own their data and run in parallel safely.
- [ ] Logic and e2e run as separate commands and CI jobs.
- [ ] No duplicate, tautological or implementation-mirroring tests; each rule is proven once, at the lowest tier.
- [ ] No retry or raised timeout is hiding an undiagnosed flake.

## 11. Out of scope

- **Red-green-refactor workflow and test-first discipline** → [tdd](../../workflows/tdd/SKILL.md).
- **Runner, mocking-library and fixture specifics per language** → the matching `*-architect` skill (e.g. [go-architect](../../languages/go-architect/SKILL.md), [python-architect](../../languages/python-architect/SKILL.md), [react-architect](../../frameworks/react-architect/SKILL.md)).
- **Load, stress and soak testing** → [performance-reviewer](../performance-reviewer/SKILL.md).
