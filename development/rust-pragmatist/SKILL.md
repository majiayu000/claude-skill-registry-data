---
name: Rust Pragmatist
description: Automatically review Rust code after edits to .rs files, providing pragmatic suggestions for idiomatic patterns, performance, safety, and code organization. Activate when Rust source files are modified or when explicitly requested.
allowed-tools: Read, Grep, Edit
---

# Rust Pragmatist

Pragmatic code review skill for Rust projects that provides actionable improvement suggestions.

## Instructions
Review the modified code against the Pragmatic Rust Guidelines in @/Users/ccustine/Downloads/pragmatic_rust.md

## Output Format

Provide feedback as an **actionable checklist** with this structure:

```markdown
## 🦀 Rust Code Review

### ✅ What's Good
- [Specific positive patterns observed]

### 🔧 Suggested Improvements

**[Category: Universal, Libraries, Interoperability, UX, Resilience, Building, Applications, FFI, Safety, Performance, Documentation, AI]**
- [ ] **[File:Line]** - [Issue description]
  - **Current**: `[problematic code snippet]`
  - **Suggested**: `[improved code snippet]`
  - **Why**: [Brief explanation of the benefit]

[Repeat for each issue found]

### 📊 Summary
- Issues found: [count by category]
- Priority: [High/Medium/Low issues]
```

## Review Priorities

Use this severity guide:
- **🔴 High**: Safety issues, panics, data races, unsound unsafe code
- **🟡 Medium**: Performance problems, non-idiomatic code, missing error handling
- **🟢 Low**: Style preferences, minor optimizations, documentation improvements

## Examples

### Example 1: Clone to Borrow

**Current**:
```rust
fn process_data(data: String) -> usize {
    data.len()
}
// Called with: process_data(my_string.clone())
```

**Suggested**:
```rust
fn process_data(data: &str) -> usize {
    data.len()
}
// Called with: process_data(&my_string)
```

**Why**: Avoids allocation; function doesn't need ownership.

### Example 2: Iterator Efficiency

**Current**:
```rust
let mut results = Vec::new();
for item in items.iter() {
    if item.is_valid() {
        results.push(item.process());
    }
}
```

**Suggested**:
```rust
let results: Vec<_> = items.iter()
    .filter(|item| item.is_valid())
    .map(|item| item.process())
    .collect();
```

**Why**: More idiomatic, potentially more efficient through iterator fusion.

### Example 3: Error Handling

**Current**:
```rust
let file = File::open("config.txt").unwrap();
```

**Suggested**:
```rust
let file = File::open("config.txt")
    .map_err(|e| format!("Failed to open config: {}", e))?;
```

**Why**: Graceful error propagation instead of panicking.

## Best Practices Reference

### Common Anti-Patterns to Flag
1. `.clone()` used to satisfy borrow checker without understanding ownership
2. `unwrap()` in production code without explicit panic documentation
3. String concatenation in loops using `+` instead of collecting into a buffer
4. Manual index iteration when iterators would work
5. `Arc<Mutex<T>>` when `&T` or channels would suffice
6. Public struct fields without accessor methods
7. Missing `#[derive(Debug)]` on public types

### Rust-Specific Optimizations
1. Use `Cow<str>` when sometimes cloning, sometimes borrowing
2. Consider `SmallVec` or `ArrayVec` for small, bounded collections
3. Use `Box<str>` instead of `String` for immutable strings
4. Leverage `std::mem::replace` or `std::mem::take` to avoid clones
5. Use `OnceCell` or `lazy_static` for one-time initialization

## Activation Context

This skill activates when:
- User edits `.rs` files (auto-trigger after modifications)
- User explicitly requests code review
- User asks about Rust best practices or patterns
- User is about to commit Rust code changes

**Do not activate for**:
- Reading existing code without modifications
- Documentation-only changes
- Cargo.toml or config file edits

## Tool Usage

- **Read**: Examine the modified Rust files and surrounding context
- **Grep**: Search for patterns across the codebase (e.g., finding all `.unwrap()` calls)
- **Edit**: Only when explicitly requested to apply suggestions

**Note**: Present suggestions but let the user decide whether to apply them unless they explicitly ask you to make the changes.