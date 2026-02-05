---
name: test-driven-development-framework
description: Practical TDD framework that teaches Red/Green/Refactor, outside-in and inside-out strategies, contract testing, characterization tests for legacy code, UI/API/data layers, concurrency/time/randomness handling, and anti-flakiness techniques. Includes actionable patterns, checklists, and language-specific quick starts.
allowed-tools: [Read, Write, Edit, Bash, Glob, Grep, WebFetch]
---

# Test-Driven Development Framework

## Purpose

Build features and fix bugs with confidence by writing tests first, using a disciplined Red/Green/Refactor loop, and choosing the right scope (unit, contract, integration, E2E) for fast, reliable feedback.

## When to Use This Skill

- New features where behavior can be specified via examples
- Bug fixes where a failing test can reproduce the issue
- Risky refactors where tests provide a safety net
- APIs and services that benefit from consumer-driven contracts
- Legacy code changes that need characterization tests before modification

## Quick Start: Red/Green/Refactor

1) Red: Write a small failing test that demonstrates desired behavior or reproduces a bug. Keep scope minimal and local.
2) Green: Write the simplest code to make the test pass. Avoid over-engineering.
3) Refactor: Improve design with tests staying green. Eliminate duplication, clarify names, and enforce boundaries.

Loop in tiny steps (1–5 minutes each). Commit after green. Prefer many small tests over few large ones.

## Choose Your Strategy

- Outside-In (London school): Start from the boundary (e.g., API/CLI/UI), drive design inward with mocks/fakes at service boundaries. Great for feature slices and collaboration across services.
- Inside-Out (Chicago/classic): Start from core logic; grow outward. Great for algorithms, data transforms, and domain rules.
- Hybrid: Use contract tests at boundaries + classic unit tests inside.

Guideline: Use fakes over mocks when possible; mock behavior, not implementation. Use real collaborators in-process if they are fast and deterministic.

## Test Scope and Speed

- Unit: Fast, isolated; no I/O. Highest volume.
- Contract: Verify producer/consumer agreements (e.g., Pact, schema tests).
- Integration: Real components together with minimal external systems.
- E2E/Scenario: Full path under production-like conditions; few and focused.

Balance using a Pyramid (more unit, fewer E2E) or Trophy (more integration/contracts) depending on your stack.

## Core Workflow Patterns

See PATTERNS.md for detailed playbooks:
- Outside-in feature slice with contract tests
- Inside-out domain rule or algorithm
- Bug fix via regression test first
- Legacy code change with characterization tests and seams
- UI component TDD with accessibility assertions
- Data layer TDD using in-memory fakes and repository boundary
- Async/concurrency with deterministic time and randomness

## Legacy Code and Seams

- Start with characterization tests to capture current behavior.
- Identify seams (injection points, adapters, feature flags) to isolate change.
- Introduce anti-corruption layers or ports/adapters to remove hard dependencies.
- Use strangler patterns to incrementally replace modules.

## Mocking and Test Doubles

Prefer: Fake > Stub/Spy > Mock. Use mocks only at architectural boundaries to specify interactions that matter to behavior. Avoid over-specifying call-order unless the order is part of behavior.

Test doubles quick guide:
- Dummy: placeholder, never used
- Stub: returns canned values
- Spy: records calls for later assertions
- Mock: pre-programmed expectations on interactions
- Fake: working but simplified implementation (e.g., in-memory DB)

## Managing Flaky Tests

- Control time via clock abstractions; never rely on wall-clock sleeps
- Control randomness via seeded RNG; inject PRNG into units
- Eliminate network and I/O; use fakes or local testcontainers with health checks
- Ensure test isolation; avoid shared mutable state and order dependence
- Set strict timeouts and fail fast; prefer retries at boundary tests only

## Metrics That Matter

- Test lead time (red→green→refactor cycle length)
- Mutation testing score (quality of assertions)
- Flake rate and mean time to green
- Coverage as a byproduct; optimize for behavior relevance, not %

## Best Practices

DO:
- Write the test name as a behavior: when/then or given/when/then
- Commit on green; refactor in small steps
- Assert one main behavior per test; keep arrange/act/assert clear
- Test public API or stable seams; use helpers to remove noise
- Keep tests fast and deterministic; parallelize when possible

DON'T:
- Test implementation details (private methods, internal locals)
- Overuse mocks; they couple tests to structure and cause brittleness
- Depend on real time, randomness, network, or global state
- Let E2E dominate your suite; keep few, critical paths only

## Additional Resources

- Patterns: See PATTERNS.md
- Knowledge base: See KNOWLEDGE.md
- Common pitfalls: See GOTCHAS.md
- Reference and quick commands: See REFERENCE.md

