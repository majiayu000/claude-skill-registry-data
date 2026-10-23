---
name: rust-testing
description: 'Guides Rust testing with TDD and property checks. Use when adding Rust test coverage, testing async code, or writing proptest cases and benchmarks.'
---

# Rust Testing Patterns

Comprehensive Rust testing patterns for writing reliable, maintainable tests following TDD methodology.

## When to Use

- Writing new Rust functions, methods, or traits
- Adding test coverage to existing code
- Creating benchmarks for performance-critical code
- Implementing property-based tests for input validation
- Following TDD workflow in Rust projects

## How It Works

1. **Identify target code** — Find the function, trait, or module to test
2. **Write a test** — Use `#[test]` in a `#[cfg(test)]` module, rstest for parameterized tests, or proptest for property-based tests
3. **Mock dependencies** — Use mockall to isolate the unit under test
4. **Run tests (RED)** — Verify the test fails with the expected error
5. **Implement (GREEN)** — Write minimal code to pass
6. **Refactor** — Improve while keeping tests green
7. **Check coverage** — Use cargo-llvm-cov, target 80%+

## Critical Rules

- Unit tests in `#[cfg(test)]` modules next to the code; integration tests in the `tests/` directory.
- Prefer `Result`-returning tests with `?` over `#[should_panic]` when testing failures.
- Use `rstest` for parameterized tests, `proptest` for property-based tests, `mockall` for mocking.
- Use `#[tokio::test]` for async tests; never `std::thread::sleep` — use channels, barriers, or `tokio::time::pause()`.
- Doc tests run with `cargo test --doc`; keep examples in doc comments compiling.

## References

Paths are relative to this SKILL.md's directory. Read only the file that matches the task. If a file cannot be read, say so.

- [references/unit-and-integration.md](references/unit-and-integration.md)
  Read when: TDD workflow; `#[cfg(test)]` unit tests; error and panic testing (prefer `Result::is_err()` over `should_panic`); integration tests in `tests/`; async tests with `#[tokio::test]`.

- [references/advanced-testing.md](references/advanced-testing.md)
  Read when: test organization patterns; parameterized tests with `rstest`; property-based testing with `proptest`; mocking with `mockall`; doc tests; Criterion benchmarks; CI integration with `cargo-llvm-cov`.

## Test Coverage

### Running Coverage

```bash
# Install: cargo install cargo-llvm-cov (or use taiki-e/install-action in CI)
cargo llvm-cov                    # Summary
cargo llvm-cov --html             # HTML report
cargo llvm-cov --lcov > lcov.info # LCOV format for CI
cargo llvm-cov --fail-under-lines 80  # Fail if below threshold
```

### Coverage Targets

| Code Type                | Target  |
| ------------------------ | ------- |
| Critical business logic  | 100%    |
| Public API               | 90%+    |
| General code             | 80%+    |
| Generated / FFI bindings | Exclude |

## Testing Commands

```bash
cargo test                        # Run all tests
cargo test -- --nocapture         # Show println output
cargo test test_name              # Run tests matching pattern
cargo test --lib                  # Unit tests only
cargo test --test api_test        # Integration tests only
cargo test --doc                  # Doc tests only
cargo test --no-fail-fast         # Don't stop on first failure
cargo test -- --ignored           # Run ignored tests
```

## Best Practices

**DO:**

- Write tests FIRST (TDD)
- Use `#[cfg(test)]` modules for unit tests
- Test behavior, not implementation
- Use descriptive test names that explain the scenario
- Prefer `assert_eq!` over `assert!` for better error messages
- Use `?` in tests that return `Result` for cleaner error output
- Keep tests independent — no shared mutable state

**DON'T:**

- Use `#[should_panic]` when you can test `Result::is_err()` instead
- Mock everything — prefer integration tests when feasible
- Ignore flaky tests — fix or quarantine them
- Use `sleep()` in tests — use channels, barriers, or `tokio::time::pause()`
- Skip error path testing
