---
name: code-quality-check
description: This skill should be used before committing code to ensure it meets Breenix quality standards. Use for running clippy checks, fixing compiler warnings, verifying no log side-effects, checking for dead code, and enforcing project coding standards from CLAUDE.md.
---

# Code Quality Checks for Breenix

Pre-commit code quality verification for Breenix kernel development.

## Purpose

Breenix enforces strict code quality standards. This skill provides the checks and fixes required before committing code.

## Core Quality Standards (from CLAUDE.md)

1. **Fix ALL compiler warnings before committing**
2. **Fix ALL clippy warnings**
3. **Use proper patterns** (e.g., `Once`) to avoid unsafe warnings
4. **Only `#[allow(dead_code)]`** for legitimate API functions

## Pre-Commit Checklist

Before every commit:

```bash
# 1. Build kernel and check for warnings
cd kernel
cargo build --target x86_64-unknown-none 2>&1 | grep warning

# 2. Run clippy
cargo clippy --target x86_64-unknown-none

# 3. Run tests (if modifying core subsystems)
cd ..
cargo test

# 4. Check for log side-effects (manual)
grep -R "log::trace!.*(" kernel/src/ | grep -vE '\".*\"' | grep -vE '\.(as_|to_|into_|len|is_|get)'
```

## Clippy Configuration

### Project-Specific Clippy Flags

```bash
cd kernel
RUSTFLAGS="-Aclippy::redundant_closure_for_method_calls" \
cargo clippy --target x86_64-unknown-none \
  -- -Dclippy::debug_assert_with_mut_call \
     -Dclippy::print_stdout \
     -Wclippy::suspicious_operation_groupings
```

### What These Check

- **`debug_assert_with_mut_call`**: Prevent side-effects in debug assertions
- **`print_stdout`**: No print!/println! in kernel (use log! macros)
- **`suspicious_operation_groupings`**: Catch likely logic errors

## Common Issues and Fixes

### Compiler Warnings

**Unused imports**:
```rust
// BAD
use x86_64::{VirtAddr, PageTable, PageTableFlags};  // PageTable unused

// GOOD
use x86_64::{VirtAddr, PageTableFlags};
```

**Unused variables**:
```rust
// BAD
let result = some_function();  // result unused

// GOOD
let _result = some_function();  // Explicitly unused
// OR
some_function();  // Don't capture if not needed
```

**Dead code**:
```rust
// BAD - function never called
fn helper_function() { ... }

// GOOD - remove it
// OR add #[allow(dead_code)] if it's part of a public API

// GOOD - legitimate API function
#[allow(dead_code)]  // Part of public allocator API
pub fn dealloc_stack(&mut self, stack_id: usize) { ... }
```

### Clippy Warnings

**Redundant closure**:
```rust
// BAD
items.map(|x| x.to_string())

// GOOD (but we allow this via RUSTFLAGS)
items.map(ToString::to_string)
```

**Debug assert with mutation**:
```rust
// BAD - side effect in assertion
debug_assert!(list.pop().is_some());

// GOOD - separate the effect
let item = list.pop();
debug_assert!(item.is_some());
```

### Log Side-Effects

**Problem**: Function calls in log statements execute even when logging disabled.

```rust
// BAD - get_state() called even if TRACE disabled
log::trace!("State: {:?}", get_state());

// GOOD - only format if needed
let state = get_state();
log::trace!("State: {:?}", state);

// BETTER - for expensive operations
if log::log_enabled!(log::Level::Trace) {
    let state = expensive_get_state();
    log::trace!("State: {:?}", state);
}
```

## CI Code Quality Workflow

The `.github/workflows/code-quality.yml` runs these checks automatically:

1. **Clippy checks** with project-specific flags
2. **Log side-effects scan** for trace statements with function calls
3. **Complex log expression check** for multi-argument format strings
4. **Log level regression guard** - ensures feature flags control log level

## Quick Reference

### Before Commit

```bash
# Full quality check
cd kernel
cargo build --target x86_64-unknown-none 2>&1 | tee /tmp/build-warnings.txt
cargo clippy --target x86_64-unknown-none 2>&1 | tee /tmp/clippy-warnings.txt

# Review warnings
grep warning /tmp/build-warnings.txt
less /tmp/clippy-warnings.txt

# Fix all warnings before committing!
```

### Common Warning Fixes

| Warning | Fix |
|---------|-----|
| unused import | Remove from use statement |
| unused variable | Prefix with _ or remove |
| dead code | Remove or add #[allow(dead_code)] for API |
| redundant closure | Allow via RUSTFLAGS or fix |
| print_stdout | Replace print! with log::info! |
| debug_assert mutation | Extract to separate statement |

## Integration with Git Workflow

```bash
# Before committing
git status  # See what you're about to commit
cd kernel
cargo clippy --target x86_64-unknown-none  # Fix all warnings

# Then commit
git add kernel/src/...
git commit -m "Fix: ..."
```

## Best Practices

1. **Fix warnings as you go**: Don't accumulate them
2. **Run clippy frequently**: Catch issues early
3. **Use proper logging**: log! macros, not print!
4. **Avoid side-effects in logs**: Especially in trace/debug
5. **Comment allowed dead code**: Explain why it's part of the API
6. **Use feature flags**: Control debug vs release behavior
7. **Test before committing**: cargo test if touching core code

## Summary

Code quality standards enforce:
- Zero compiler warnings
- Zero clippy warnings
- No side-effects in log statements
- Appropriate use of #[allow] attributes
- Proper logging practices

Run checks before every commit to maintain high code quality.
