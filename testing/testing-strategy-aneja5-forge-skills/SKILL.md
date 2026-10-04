---
name: testing-strategy
description: Use when defining a project's test approach, when choosing what gets tested at unit vs integration vs e2e level, when setting per-component coverage targets, when reviewing test quality, or when CI is slow / flaky and tests need a strategy reset.
---

# Testing Strategy

## Overview

Define what gets tested, at what level, with what mocking — *before* tests proliferate. Output is `.forge/testing-strategy.md` — the test pyramid for this project (unit/integration/e2e ratio), what each level is responsible for, mocking philosophy, per-component coverage targets, the critical-path inventory, the flake quarantine policy, and CI gate definitions. Consumed by `incremental-implementation`, `tdd`, and `code-review-and-quality`.

## When to Use

- A new project is starting and needs test conventions before code lands
- The test suite has grown organically and is slow, flaky, or inconsistent
- Coverage % is being treated as a goal and producing meaningless tests
- A team is mocking everything internally and tests pass while features break
- CI takes >15 minutes and the team is starting to skip tests

## When NOT to Use

- Single-task work where `tdd` is the right skill (write the test, write the code)
- Reference implementations or learning projects where tests aren't shipped
- The strategy exists, is followed, and only one component needs adjustment

## Common Rationalizations

| Thought | Reality |
|---------|---------|
| "100% coverage is the goal" | Coverage measures lines hit, not behavior verified. 100% coverage of a deleted file is meaningless. |
| "Mock everything" | Mocking internals tests the mock, not the code. When the implementation changes, mocks lie. |
| "E2E is too slow, skip it" | One e2e test catches what 50 unit tests miss — integration between layers is where most bugs live. |
| "We'll add tests after" | Tests-after test imagined behavior, not actual behavior. They lock in accidents as decisions. |
| "Flaky tests just need a retry" | Retries hide bugs. A flaky test is a heisenbug — quarantine and fix the root cause. |
| "Test the implementation so refactors stay safe" | Refactors should change implementation freely. Tests on internals make refactoring expensive. |

## Red Flags

- "100% coverage" as the explicit target
- A test file with `expect(spy).toHaveBeenCalledWith(...)` and no other assertions
- Every external service mocked at function level (mock the boundary instead)
- Zero end-to-end tests for the primary user journey
- A test that takes >30 seconds and runs on every commit
- A test that passes when the underlying feature is manually broken (snapshot rot, weak assertions)
- A retry config on `pytest`/`vitest`/`jest` to "fix" flakes

## Core Process

### Step 1: Identify critical user paths

Read `.forge/prd.md` if present. List the 3-7 user journeys that, if broken, ship a broken product. Each is an e2e candidate. Everything else is unit/integration.

### Step 2: Decide test level per path

| Level | Tests | When |
|-------|-------|------|
| Unit | Pure functions, business logic, transformations | Single module, no I/O |
| Integration | Module + its real adapter (real DB, real HTTP via testcontainers) | Boundaries, contracts |
| E2E | Full stack, real browser if frontend | Critical user paths only |

Default ratio: 70% unit / 20% integration / 10% e2e. Adjust based on what's risky.

### Step 3: Define mocking boundaries

The rule: **mock at the seam, not inside the module.**
- Mock the HTTP client, not your service-that-calls-HTTP
- Mock the message broker, not the consumer-that-uses-the-broker
- Mock time, randomness, and the file system at the lowest seam (injected clock, seeded RNG, in-memory FS)
- Never mock the database in integration tests — use testcontainers

### Step 4: Set per-component coverage targets

Not "80% across the project." Per-component:
- Pure business logic: 90%+ line + branch coverage
- Adapters (HTTP/DB clients): integration-test coverage (line % less meaningful)
- UI components: behavior coverage (clicks, keyboard, screen reader), not snapshot
- Glue code: lower bar, but every error path tested

Document each target in `.forge/testing-strategy.md` with rationale.

### Step 5: Write golden tests for invariants

Identify 3-10 invariants per critical module (e.g., "ownership isolation never broken", "no negative balance possible", "no orphan rows after delete"). Write a property/golden test per invariant. These survive refactors.

### Step 6: Define flake quarantine policy

When a test flakes:
1. Quarantine immediately (skip with TODO + owner + deadline).
2. Find root cause within 5 business days (timing? shared state? real bug?).
3. Re-enable only after the root cause is fixed.
4. Quarantine over 5 days = delete or rewrite.

No retry-on-fail config in CI. Flakes are bugs, not noise.

### Step 7: Define CI gates

In `.forge/testing-strategy.md`:
- Which tests run on every push, every PR, nightly
- Total CI budget (e.g., <10 min PR, <30 min nightly)
- What's allowed to block merge (failing tests, coverage drop on critical modules)
- What's monitoring-only (flake rate, suite duration trend)

### Step 8: Header

Prepend a `forge:meta` header to `.forge/testing-strategy.md` (`generated_by: testing-strategy`, `generated_at: <ISO 8601 UTC with Z>`, `depends_on: [.forge/prd.md]` — paths only, never hashes, `generated_from: {.forge/prd.md: <upstream content_hash AT generation time>}`, `content_hash: <sha256 first 8 of THIS file's body>`). See [forge-dependency-graph](../../references/forge-dependency-graph.md).

## Verification

- [ ] `.forge/testing-strategy.md` written with per-component coverage targets and rationale
- [ ] Critical user paths each have at least one e2e test
- [ ] Boundary modules (HTTP / DB / queue) have integration tests against real dependencies (testcontainers or similar)
- [ ] Pure logic modules have unit tests with >90% branch coverage
- [ ] No mock of an internal collaborator (only mocks at seams)
- [ ] No test takes >5 seconds without a documented exception
- [ ] Flake rate <1% over the trailing 30 days (or quarantine policy active)
- [ ] CI runs in <10 minutes for PRs
- [ ] No `retries: N` config used to mask flakes
