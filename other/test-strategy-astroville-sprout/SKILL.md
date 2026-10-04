---
name: test-strategy
description: Test strategy design covering the test pyramid, coverage ROI, test boundaries, and identifying gaps in existing codebases.
compatibility: opencode
metadata:
  audience: test-architect, delivery-leads
  purpose: test-strategy
---
## What I do

Provide guidance on designing test strategies that maximize confidence per unit of effort. This skill covers when to use each test type, where to draw test boundaries, and how to identify gaps in existing test suites.

## When to use me

Load this skill when designing a test strategy for new work, reviewing test coverage of existing code, or deciding what level of testing a spec's Validation section should require.

## The test pyramid

The pyramid is a budget allocation tool, not a rule. Invest most effort where the return is highest.

### Unit tests

**What they test**: A single function, method, or class in isolation. Dependencies are replaced with test doubles.

**When to use**: Always, for code that contains logic. Skip for pure delegation (functions that just call another function and return its result) and trivial data holders.

**Cost**: Cheap to write, cheap to run, cheap to maintain. Fast feedback.

**Pitfall**: High unit test coverage with no integration tests gives false confidence. Units pass, the system fails.

### Integration tests

**What they test**: Two or more components working together. A service calling a real database. An API endpoint processing a request through the full middleware stack.

**When to use**: For every boundary where components connect — database queries, API endpoints, message queue handlers, external service calls. These are where most production bugs live.

**Cost**: More expensive to write and run than unit tests. Require test infrastructure (databases, queues). Slower feedback.

**Pitfall**: Slow test suites. Mitigate by running integration tests in parallel, using per-test database transactions that roll back, and keeping the test database schema in sync with migrations.

### End-to-end tests

**What they test**: The full system from the user's perspective. Browser automation, API call sequences, complete workflows.

**When to use**: For critical user journeys only. Login, checkout, the core value-delivering workflow. Not for edge cases — that's what unit and integration tests are for.

**Cost**: Expensive to write, slow to run, brittle to maintain. A single UI change can break dozens of E2E tests.

**Pitfall**: Too many E2E tests create a slow, flaky test suite that nobody trusts. Keep the E2E suite small and focused on paths that, if broken, would mean the product is unusable.

### Contract tests

**What they test**: That a producer and consumer agree on the interface between them — API shape, message format, event schema.

**When to use**: When services communicate across a network boundary and are developed independently. Especially valuable when different teams own the producer and consumer.

**Cost**: Moderate setup cost (requires a contract testing framework like Pact), low ongoing cost.

**Pitfall**: Contracts test shape, not behavior. A contract-passing response can still be wrong if the data is incorrect.

## Coverage ROI

Not all code benefits equally from testing. Prioritize:

**High ROI (test thoroughly):**
- Business logic with branching conditions
- Data transformation and validation
- Error handling paths (especially error paths that recover or retry)
- Security-sensitive code (auth, authorization, input sanitization)
- Integration points (database queries, API calls, message handling)
- Code that's changed frequently (high churn = high regression risk)

**Low ROI (test lightly or skip):**
- Generated code
- Configuration constants
- Simple getters/setters with no logic
- UI layout (unless layout is the product's core value)
- Code that will be deleted soon

**Negative ROI (actively avoid):**
- Tests that duplicate implementation details (testing that a function calls another function in a specific order)
- Tests that mock so heavily they test the mocks, not the code
- Tests that are so brittle they break on every refactor without catching bugs

## Test boundaries

### What to mock

Mock things that are:
- **Slow**: External HTTP services, email delivery, file system operations
- **Non-deterministic**: Current time, random numbers, UUIDs
- **Side-effecting**: Payment processing, sending notifications, writing to external systems
- **Not yours**: Third-party APIs you don't control

### What to test against real dependencies

Test against real instances of:
- **Your database**: Use a real database (same engine as production) for integration tests. SQLite-in-test when production uses PostgreSQL is a recipe for false confidence.
- **Your cache**: If your code depends on cache behavior (TTL, eviction), test against the real cache.
- **Your message queue**: If message ordering or delivery guarantees matter, test against the real queue.

### The boundary rule

Mock at the boundary of your system, not inside it. If your system is a web service backed by a database, the boundaries are: incoming HTTP requests (test from here) and outgoing calls to external services (mock these). Everything between — your code, your database — runs for real.

## Property-based testing

### When it's worth the complexity

Property-based testing (generating random inputs and checking invariants) pays off when:
- The function has a wide input space that example-based tests can't cover (parsers, serializers, data transformers)
- There are algebraic properties to verify (encode/decode roundtrip, sort stability, commutativity)
- Past bugs have been caused by unexpected edge cases in input data
- The function is pure (deterministic, no side effects) — property tests are painful with stateful code

### When to skip it

- The function's behavior is better described by concrete examples than by abstract properties
- The input space is small and enumerable
- Setting up the generator is harder than writing the tests it would replace

## Test data management

### Fixtures

Static test data checked into the repository. Good for:
- Reference data that doesn't change (country codes, currency definitions)
- Known-good input/output pairs for parser or transformer tests
- Snapshot data for regression tests

Keep fixtures small and focused. A 10,000-line JSON fixture is a maintenance nightmare. If the test needs a lot of data, generate it.

### Factories

Functions that create test objects with sensible defaults and selective overrides. Preferred over fixtures for domain objects.

Good factory design:
- Defaults produce a valid object with no arguments
- Every field is overridable
- Related objects are created automatically (a factory for Order creates a Customer if one isn't provided)
- Names are descriptive: `createExpiredSubscription()` not `createSubscription({ expired: true })`

### Seeding

Pre-populating a test database with a known dataset. Use for integration and E2E tests that need a realistic data environment.

- Keep the seed dataset minimal — just enough to exercise the test scenarios
- Make seeding idempotent — running it twice doesn't create duplicates
- Version the seed data alongside the schema migrations
- Never seed with production data dumps unless they're anonymized and scrubbed

## Performance testing

### When to load test

- Before launching a new service or endpoint
- Before a major change to a critical path (database query rewrite, caching layer change)
- When the system has known scale targets it hasn't been validated against
- After an incident caused by load

### What thresholds matter

Define thresholds relative to your system's requirements, not abstract numbers. Useful metrics:
- **Throughput**: Requests per second the system sustains without degradation
- **Latency at load**: P50, P95, P99 under expected and peak load
- **Saturation point**: The load level where latency or error rate starts climbing non-linearly
- **Recovery time**: How quickly the system returns to normal after a load spike

### Load test hygiene

- Run against an environment that mirrors production (same instance sizes, same database, same network topology)
- Warm up caches and connection pools before measuring
- Run long enough to detect memory leaks and connection exhaustion (minutes, not seconds)
- Test failure modes: what happens when you exceed capacity? Graceful degradation or cascading failure?

## Identifying test gaps

When evaluating an existing codebase's test coverage:

1. **Find untested code paths.** Coverage tools show which lines execute during tests. Focus on uncovered branches in high-risk code (business logic, error handling, security checks).
2. **Find tested-but-wrong tests.** Tests that always pass regardless of behavior — usually caused by mocking the thing being tested, or assertions that are too loose.
3. **Find missing integration tests.** Look for database queries, API calls, and message handlers that are only unit-tested with mocks. These are the most common source of production bugs.
4. **Find missing negative tests.** Are error paths tested? Invalid input? Unauthorized access? Timeout handling? Most test suites over-index on happy paths.
5. **Find flaky tests.** Tests that pass sometimes and fail sometimes erode trust in the entire suite. Fix or delete them — a flaky test is worse than no test because it trains people to ignore failures.
