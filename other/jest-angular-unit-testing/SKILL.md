---
id: angular.testing.jest-angular-unit-testing
name: Angular Jest Unit Testing
description: >
  Write or review Angular tests in existing Jest projects, with narrow typed mocks, deterministic async behavior, and assertions that catch regressions.
stack:
  - Angular
  - TypeScript
  - Jest
category: testing
status: stable
version: 0.10.0
owner: NgAutoPilot
triggers:
  - jest angular testing
  - angular jest unit testing
  - unit testing
  - TestBed
  - jest testbed
  - angular component test
  - angular service test
  - mocking strategy
compatibility:
  angular:
    min: "12"
    recommendedModern: "17+"
---

# Angular Jest Unit Testing

## Purpose

Use this skill to design or review Angular unit tests when the project uses Jest.

Jest should support clear, maintainable tests for components, services, pipes, and helpers. The focus is not on forcing a testing style, but on keeping tests readable, deterministic, and aligned with the application's architecture.

The core rule is simple:

```txt
Test behavior at the boundary you own.
```

## When to Use

Use this skill when:

- the project already uses Jest
- unit tests need cleanup or structure
- TestBed usage needs guidance
- component or service mocking strategy is unclear
- test suites are becoming brittle or hard to read

## Do

Use TestBed for Angular-aware component and service tests:

```ts
beforeEach(() => {
  TestBed.configureTestingModule({
    providers: [MyService],
  });
});
```

Keep mocks narrow and intentional.

Assert behavior, not implementation details.

Prefer focused test names that describe user or service intent.

Use TestBed when injection, templates, or Angular lifecycle behavior is part of the contract. For a pure function or a class with explicit constructor dependencies, direct construction can keep the test smaller; do not cast a partial mock to a full service to bypass its type contract.

For timed RxJS flows, choose one clock owner: Jest fake timers or RxJS `TestScheduler`. Do not combine either with Angular `fakeAsync` in the same test. Subscribe before sending input, recreate mocks per test, and release subscriptions and restore timers in `afterEach` so a failing assertion cannot contaminate later tests.

Assert the time boundary and debounce reset, normalized arguments, duplicate suppression, obsolete response rejection, and error recovery. After a fallback emission, send a successful request through the same subscription; a single error assertion cannot prove the stream stayed usable.

For a search using `debounceTime` and `switchMap`, read [the search contract example](references/rxjs-search-contract.md). It distinguishes delayed cancellation from immediate invalidation and includes teardown assertions, not just output checks.

## Do Not

Avoid rewriting the entire test stack during a local fix.

Avoid snapshot-only testing for dynamic Angular behavior.

Avoid overspecifying internal method calls when DOM or service behavior is the real contract.

Avoid mixing unrelated framework migrations into the testing work.

Do not replace time-boundary assertions with `runAllTimers()`, or treat a mocked `Subject` as proof that the real HTTP transport aborts a request. Verify transport cancellation separately when that is a requirement.

## Review Checklist

- [ ] The project actually uses Jest.
- [ ] TestBed is used when Angular context is needed.
- [ ] Mocks are minimal and readable.
- [ ] Tests verify behavior, not private implementation details.
- [ ] The test suite remains maintainable.
- [ ] Timer boundaries, debounce reset, and stale responses are covered when relevant.
- [ ] Error fallback is followed by a successful request on the same stream.
- [ ] Mocks, subscriptions, and clock state are isolated between tests.

## Expected Output

1. Inspect the Jest-based test setup.
2. Recommend a maintainable TestBed strategy.
3. Define a minimal mocking approach.
4. Flag brittle or overspecified tests.
5. Produce focused test examples or refactors.
6. Report the tests actually run and any unverified transport or framework behavior.
