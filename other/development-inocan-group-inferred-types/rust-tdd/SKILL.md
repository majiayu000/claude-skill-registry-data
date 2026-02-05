---
name: rust-tdd
description: Test-Driven Development for Rust. Use when creating new functionality, writing tests, or fixing bugs through the Red-Green-Refactor TDD cycle.
allowed-tools: Read, Write, Edit, Bash, Grep, Glob
---

# Rust TDD Workflow

## Process (Red-Green-Refactor)

### 1. Red Phase
Write a failing test first that describes the desired behavior:

```rust
#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_new_feature() {
        let result = new_function(input);
        assert_eq!(result, expected_output);
    }
}
```

Verify the test fails: `cargo test -p <crate> <test_name>`

### 2. Green Phase
Implement the minimum code to make the test pass:
- Write only enough code to pass the test
- Don't over-engineer or add extra features
- Focus on correctness, not elegance

Verify: `cargo test -p <crate>`

### 3. Refactor Phase
Improve the code while keeping tests green:
- Remove duplication
- Improve naming
- Simplify logic
- Extract functions if needed

After each change: `cargo test -p <crate>`

## Test Commands

```bash
# Run specific test
cargo test -p <crate> <test_name> -- --nocapture

# Run all tests in crate
cargo test -p <crate> --all-features

# Run with output
cargo test -p <crate> -- --nocapture

# Run doc tests
cargo test -p <crate> --doc

# Continuous testing
cargo watch -x "test -p <crate>"
```

## Test Patterns

### Basic Test
```rust
#[test]
fn test_success_case() {
    let result = function_under_test(42);
    assert_eq!(result, 84);
}
```

### Result-returning Test
```rust
#[test]
fn test_with_result() -> Result<(), Box<dyn std::error::Error>> {
    let result = fallible_function()?;
    assert_eq!(result, expected);
    Ok(())
}
```

### Panic Test
```rust
#[test]
#[should_panic(expected = "index out of bounds")]
fn test_panic_case() {
    function_that_panics();
}
```

### Async Test
```rust
#[tokio::test]
async fn test_async_function() {
    let result = async_function().await;
    assert!(result.is_ok());
}
```

### Property-based Test (with proptest)
```rust
use proptest::prelude::*;

proptest! {
    #[test]
    fn test_property(x in 0..100i32) {
        let result = function(x);
        prop_assert!(result >= 0);
    }
}
```

## Final Verification

After completing TDD cycle:
```bash
cargo clippy -p <crate> -- -D warnings
cargo fmt -p <crate> -- --check
cargo test -p <crate> --all-features
```

## Nebula-specific Patterns

- Each crate has its own error type via `thiserror`
- Use `#[tokio::test]` for async tests
- Place unit tests in same file under `#[cfg(test)]` module
- Place integration tests in `tests/` directory of the crate
