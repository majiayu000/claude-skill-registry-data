---
name: testing-rust
description: Writes tests following TDD (using cargo test, proptest, and insta) best practices. Use when writing unit tests, integration tests, or property-based tests in Rust.
compatibility: Designed for Claude Code
metadata:
  allowed-tools: Read, Grep, Glob, Edit, Write, Bash
  argument-hint: [test-scope or component-name]
  stability: stable
  content-hash: sha256:05ca1842234b8ba0cdd00693b47ee16fec6d4b15d498c867d29cd74a44779ff0
---

# Rust Testing

**Target**: $ARGUMENTS

Writes **focused, behavior-driven tests** following project testing strategy.

## Quick Reference

**TDD methodology** (language-agnostic): See `tdd-core` plugin (`testing-tdd` skill)

**Rust-specific documentation**: `references/`

- `references/testing-strategy.md` — Rust tools (cargo test, proptest, insta, mockall)
- `references/tdd-best-practices.md` — Rust TDD examples (extends tdd-core)

## Quick Decision

**cargo test (default)**: Use `#[test]` for known cases, `#[tokio::test]` for async. Works at unit/integration levels.

**proptest (edge cases)**: Use for invariants that must hold for ALL inputs.

See `references/testing-strategy.md` for full methodology comparison.

## TDD Essentials (Quick Reference)

**Cycle**: RED (failing test / compile error) -> GREEN (minimal pass) -> REFACTOR (clean up)

**Structure**: Arrange-Act-Assert (AAA)

```rust
#[test]
fn test_order_calculator_sums_item_prices() {
    // ARRANGE
    let items = vec![Item { price: 10, qty: 2 }, Item { price: 5, qty: 1 }];
    let calculator = OrderCalculator::new();

    // ACT
    let total = calculator.total(&items);

    // ASSERT
    assert_eq!(total, 25);
}
```

## proptest Priorities (Edge Cases within TDD)

| Priority | Area | Example |
| -------- | ---- | ------- |
| CRITICAL | Math formulas | Score always in bounds |
| CRITICAL | Parsers | Arbitrary input never panics |
| HIGH | Serialization | Round-trip encode/decode lossless |
| HIGH | Invariant sums | Total equals sum of parts |

## What to Test (KISS/DRY/YAGNI)

**High-Value**: Business logic, error paths, integration points, contracts

**Avoid**: Compiler behavior, derive implementations, trivial assertions, default values

See `references/testing-strategy.md` -> "Patterns to Remove" for full list.

## Naming Convention

**Format**: `test_{module}_{component}_{behavior}`

```rust
test_user_service_creates_new_user()
test_order_processor_validates_items()
test_score_always_in_bounds()  // property test
```

## Execution

```bash
cargo test                          # All tests
cargo test test_order               # Filter by name
cargo test --lib                    # Unit tests only
cargo test --test integration       # Integration tests only
cargo watch -x test                 # Watch mode (cargo-watch)
```

## Quality Gates

- [ ] All tests pass (`cargo test`)
- [ ] TDD Red-Green-Refactor followed
- [ ] Arrange-Act-Assert structure used
- [ ] Naming convention followed
- [ ] Behavior-focused (not implementation)
- [ ] No compiler/library behavior tested
- [ ] Mocks use `mockall` with `.times()` constraints
