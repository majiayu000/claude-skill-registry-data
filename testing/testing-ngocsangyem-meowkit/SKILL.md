---
name: mk:testing
description: Use when writing tests, running validation scripts, or (in TDD mode) enforcing red-green-refactor cycle. Activates during Phase 2 (Test) and Phase 3 (Build). NOT for coverage gap mapping (see mk:nyquist); NOT for sprint contract negotiation (see mk:sprint-contract).
keywords:
  - testing
  - unit-tests
  - tdd-red-green
  - validation-scripts
  - phase-2-test
when_to_use: Use when writing tests, running validation scripts, or enforcing TDD red-green-refactor cycle. NOT for coverage gap mapping (see mk:nyquist) or sprint contract negotiation (see mk:sprint-contract).
user-invocable: true
owner: testing
criticality: medium
status: active
runtime: claude-code
---

# Testing Toolkit

Reference guides for testing: TDD red-green-refactor, validation scripts, and visual QA.

## When to Use

- During Phase 2 (Test) for writing tests — failing tests first in TDD mode (`--tdd` / `MEOWKIT_TDD=1`), or any-order tests in default mode
- During Phase 3 (Build) for verifying implementation
- When the `tester` agent needs testing patterns
- For visual QA testing of web applications

## Workflow Integration

Operates in **Phase 2 (Test)** and **Phase 3 (Build)**. Output supports the `tester` agent.

In TDD mode the cycle is RED → GREEN → REFACTOR (failing tests required before implementation). In default mode (TDD off), tests may be written before, alongside, or after implementation — the developer chooses.

## References

| Reference | When to load | Content |
|-----------|-------------|---------|
| **[red-green-refactor.md](./references/red-green-refactor.md)** | Phase 2-3 | TDD cycle, test-first rules, refactoring guidelines |
| **[validation-scripts.md](./references/validation-scripts.md)** | After code changes | Running validation scripts, interpreting results |
| **[visual-qa.md](./references/visual-qa.md)** | UI testing | Browser-based visual QA, screenshot comparison, responsive testing |
| **[e2e-best-practices.md](./references/e2e-best-practices.md)** | When creating E2E tests | Tool preference, locator strategy, wait patterns, POM, flaky quarantine, success metrics |

## Gotchas

- **Mocks hiding integration failures**: All mocked tests pass but real service calls fail → Use integration tests for critical paths; mock only external third-party services
- **Test coverage metric gamed by trivial assertions**: 100% coverage with `expect(true).toBe(true)` → Measure mutation testing score alongside coverage; flag tests with zero assertions
- **Vue-specific test design/review**: for designing or auditing Vitest + Vue Test Utils tests (components, composables, Pinia, router, Suspense, Teleport) → use `mk:vue-testing-best-practices` (advisory/review only; this skill still owns running tests + TDD)
