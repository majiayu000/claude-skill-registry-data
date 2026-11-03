---
name: tdd
description: Test-driven development for ASP.NET Core and EF Core with xUnit. Use when building a feature or fixing a bug test-first, when the user mentions TDD or red-green-refactor, or when adding integration tests for endpoints or data access.
---

# Test-Driven Development (.NET)

Loop rules adapted from Matt Pocock's `tdd` skill (https://github.com/mattpocock/skills, MIT), rewritten for .NET.

## Agree on the seams first

A seam is the public boundary a test observes behavior through: an HTTP endpoint, a service's public method, a domain type's public API. Before writing any test, list the seams you intend to test, with one line each on what the test catches and what it misses, and confirm them with the user.

Prefer the outermost seam that is still fast and deterministic:

| Seam | Test type | Tooling |
|---|---|---|
| HTTP endpoint | Integration | `WebApplicationFactory<Program>` (`Microsoft.AspNetCore.Mvc.Testing`) and `HttpClient` |
| Data access with real queries | Integration | Testcontainers module for the project's database, e.g. `Testcontainers.PostgreSql` or `Testcontainers.MsSql` |
| Domain logic with no I/O | Unit | Plain xUnit tests, no mocks |

Do not test EF Core queries against the in-memory provider or SQLite when production uses another database: translation and behavior differ.

## The loop

1. **Red.** Write one failing test at an agreed seam. Run it and confirm it fails for the expected reason, not a compile error or setup problem.
2. **Green.** Write the minimum production code to pass it. No speculative parameters, branches, or abstractions.
3. **Repeat** with the next test. One seam, one test, one minimal change per cycle. Each test should respond to what the previous cycle taught you.
4. **Refactor** only once the tests for the slice are green, and keep them green while you do.

Never write a batch of tests up front and then implement them all: that tests imagined behavior and locks in structure before you understand it.

## Changing existing code

- Before optimizing or refactoring code without tests, write tests that pin its current behavior, including odd cases like duplicates or malformed input.
- When fixing a bug, keep the test that reproduced it as a regression test.

## What a good test looks like

- **Behavior, not implementation.** It asserts on what a caller can observe: the response status and body, the returned value, the persisted state read back through the public API. It survives a refactor that keeps behavior the same.
- **Independent expected values.** The expected value comes from a literal, a worked example, or the spec, never recomputed the way the code computes it.
- **Arrange, Act, Assert**, with one behavior per test.
- **Named for the behavior**: `Method_Scenario_ExpectedResult`, e.g. `CreateOrder_WithEmptyCart_Returns400`.
- **Isolated.** No shared mutable state between tests. Integration tests reset or isolate their data (a fresh database per test class, or a transaction per test).

## Mocking

- Mock only what you don't own or can't run: third-party HTTP APIs, email, clocks (`TimeProvider`), randomness.
- Don't mock `DbContext`, repositories over it, or your own services to test their callers: test through the real thing at a higher seam instead.
- In endpoint tests, replace external dependencies in `WebApplicationFactory.ConfigureWebHost` via `ConfigureTestServices`.

## Anti-patterns

- Asserting that a mock was called instead of asserting the outcome.
- Testing private methods, or making members `internal` only so tests can reach them.
- `Assert.True(result != null)` style assertions that pass for wrong values.
- `Thread.Sleep` or timing-based waits; use `TimeProvider` or polling with a timeout.
- Catching exceptions in a test to make it pass.

## Practicalities

- Since .NET 10, a source generator makes the top-level `Program` class public, so `WebApplicationFactory<Program>` works without declaring `public partial class Program { }`. Add that declaration only on earlier versions.
- Pass `TestContext.Current.CancellationToken` (xUnit v3) to async calls in tests.
- Run the narrowest set of tests that covers the change while iterating, then the full suite before finishing.
