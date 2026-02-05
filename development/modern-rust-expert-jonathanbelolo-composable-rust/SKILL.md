---
name: modern-rust-expert
description: Expert knowledge for writing cutting-edge, idiomatic Rust code with Rust Edition 2024, strict clippy compliance, and functional-but-pragmatic philosophy. Use when writing any Rust code, fixing clippy warnings, structuring modules or crates, reviewing or refactoring Rust code, or questions about Rust 2024 features, async patterns, documentation standards, or performance optimization.
---

# Modern Rust Expert

Expert knowledge for writing cutting-edge, idiomatic Rust code with Rust edition 2024, strict clippy compliance, and functional-but-pragmatic philosophy.

## When to Use This Skill

Automatically apply this knowledge when:
- Writing any Rust code in this project
- Fixing clippy warnings
- Structuring new modules or crates
- Reviewing or refactoring Rust code

## Rust Edition 2024 Specifics

### Version Requirements
- **Edition**: 2024
- **MSRV**: 1.85.0 (minimum for edition 2024)
- Always check `rustc --version` and update with `rustup update stable` if needed

### Edition 2024 & Rust 1.85+ Features Available

#### 1. Async Functions in Traits (Stable!)
Use `async fn` directly in trait definitions without `async-trait` crate:

```rust
// Modern Rust - async fn in traits (no macro needed!)
trait Database: Send + Sync {
    async fn save(&self, data: &[u8]) -> Result<(), Error>;
    async fn load(&self, id: &str) -> Result<Vec<u8>, Error>;
}

// Implementation
impl Database for PostgresDb {
    async fn save(&self, data: &[u8]) -> Result<(), Error> {
        // Direct async implementation
        sqlx::query("INSERT INTO ...").execute(&self.pool).await?;
        Ok(())
    }
}
```

**Use this for**: All async trait methods in Environment traits (Database, HttpClient, etc.)

#### 2. Return Position Impl Trait in Traits (RPITIT)
Return `impl Trait` from trait methods:

```rust
trait EventPublisher {
    // Can return impl Future instead of Box<dyn Future>
    fn publish(&self, event: Event) -> impl Future<Output = Result<()>> + Send;
}
```

**Benefit**: No heap allocation, better performance than `Box<dyn Future>`.

#### 3. Let-Else Statements
Early return with pattern matching:

```rust
// Modern pattern for error handling
fn process_order(action: OrderAction) -> Result<Order, Error> {
    let OrderAction::PlaceOrder { customer_id, items } = action else {
        return Err(Error::InvalidAction);
    };

    // customer_id and items are in scope here
    Ok(Order { customer_id, items })
}

// Compare to old style:
fn process_order_old(action: OrderAction) -> Result<Order, Error> {
    match action {
        OrderAction::PlaceOrder { customer_id, items } => {
            Ok(Order { customer_id, items })
        }
        _ => Err(Error::InvalidAction),
    }
}
```

**Use for**: Extracting enum variants with early return.

#### 4. Enhanced Const Generics
Use const generics in more contexts:

```rust
// Const generic for effect buffer size
struct EffectBuffer<Action, const N: usize> {
    effects: [Option<Effect<Action>>; N],
}

impl<Action, const N: usize> EffectBuffer<Action, N> {
    const fn new() -> Self {
        Self {
            effects: [const { None }; N],
        }
    }
}
```

**Use for**: Stack-allocated buffers with configurable size.

#### 5. Inline Const Expressions
Use `const { }` blocks in const contexts:

```rust
const DEFAULT_CAPACITY: usize = 16;

struct Cache<T> {
    // Inline const expression
    data: [Option<T>; const { DEFAULT_CAPACITY * 2 }],
}
```

#### 6. C-String Literals
Create `CStr` at compile time:

```rust
// Modern: c"string" literal
let path = c"/tmp/data";  // Type: &'static CStr

// Old way required:
use std::ffi::CString;
let path = CString::new("/tmp/data").unwrap();
```

**Use for**: FFI code and system calls.

#### 7. If/While Let Chains
Combine multiple patterns with `&&`:

```rust
// Modern: let chains
fn handle_event(state: &State, action: Action) {
    if let OrderAction::PlaceOrder { items, .. } = action
        && !items.is_empty()
        && state.can_place_order()
    {
        // All conditions met
    }
}

// Old way required nested ifs or match
```

#### 8. Improved Pattern Matching

**Rest patterns in slices**:
```rust
match events.as_slice() {
    [first, .., last] => {
        // first and last are available
    }
    _ => {}
}
```

**Patterns in let statements**:
```rust
let [first, second, ..] = &events[..] else {
    return Err(Error::NotEnoughEvents);
};
```

#### 9. Expanded Const Fn Capabilities

More operations allowed in `const fn`:

```rust
const fn calculate_capacity(base: usize) -> usize {
    // These are all allowed in const fn now:
    if base < 16 { 16 } else { base }
}

const fn create_default<T>() -> Option<T> {
    None  // Can return generic types
}

// Use in const contexts
const CAPACITY: usize = calculate_capacity(10);
```

#### 10. Precise Capturing in RPIT
Control which lifetimes are captured:

```rust
trait Store {
    // Only capture 'a, not all lifetimes
    fn get_state<'a>(&'a self) -> impl Future<Output = State> + use<'a>;
}
```

### Features NOT Available (Require Nightly)

To avoid confusion, these are **NOT** in stable yet:
- ❌ `gen` blocks for generators
- ❌ Type alias impl trait (TAIT)
- ❌ Specialization
- ❌ Generic const expressions (full support)
- ❌ `#[derive]` on `enum` with generics in some cases

### Recommended Patterns for This Project

1. **Use async fn in traits** - No more `async-trait` dependency
2. **Prefer let-else** - Cleaner error handling
3. **Use RPITIT** - Return `impl Future` instead of `Box<dyn Future>`
4. **Const generics for buffers** - Stack allocation where possible
5. **Let chains** - Combine multiple conditions elegantly

## Clippy Configuration & Compliance

### Workspace Lint Configuration

Always configure lints at workspace level in root `Cargo.toml`:

```toml
[workspace.lints.rust]
unsafe_code = "forbid"
missing_docs = "warn"

[workspace.lints.clippy]
# Pedantic lints - USE LOWER PRIORITY so specific lints can override
pedantic = { level = "warn", priority = -1 }

# Deny common issues
unwrap_used = "deny"
expect_used = "deny"
panic = "deny"
todo = "deny"
unimplemented = "deny"

# Performance
missing_const_for_fn = "warn"

# Cognitive complexity
cognitive_complexity = "warn"

# Documentation
missing_errors_doc = "warn"
missing_panics_doc = "warn"
```

**Critical**: Lint groups like `pedantic` MUST have `priority = -1` to avoid conflicts with specific lints.

### Individual Crate Configuration

In each crate's `Cargo.toml`, inherit workspace lints:

```toml
[lints]
workspace = true
```

### Common Clippy Issues & Solutions

#### 1. Mixed Attributes Style
**Problem**: Having both outer (`///`) and inner (`//!`) doc comments on the same item.

**Wrong**:
```rust
/// Module for actions
///
/// This contains action types.
pub mod action {
    //! Action implementations
}
```

**Correct**:
```rust
/// Module for actions
///
/// This contains action types.
///
/// Action implementations.
pub mod action {}
```

**Rule**: Pick one style per item. For modules, use outer docs (`///`) and move inner content to the outer doc comment.

#### 2. Documentation Backticks
**Rule**: ALL type names, function names, trait names in documentation MUST be in backticks.

**Wrong**:
```rust
/// - Database: The database trait
/// - HttpClient: HTTP client
```

**Correct**:
```rust
/// - `Database`: The database trait
/// - `HttpClient`: HTTP client
```

#### 3. Missing `# Panics` Documentation
If a function can panic, document it:

```rust
/// Create a test clock
///
/// # Panics
///
/// Panics if the hardcoded timestamp fails to parse
/// (should never happen in practice).
#[allow(clippy::expect_used)]  // Justified in test utilities
pub fn test_clock() -> Clock {
    // ...
}
```

#### 4. Non-Debug Types
Some types (like `Future`) don't implement `Debug`. Manually implement it:

```rust
pub enum Effect<Action> {
    Future(Pin<Box<dyn Future<Output = Option<Action>> + Send>>),
}

// Manual Debug implementation
impl<Action> std::fmt::Debug for Effect<Action>
where
    Action: std::fmt::Debug,
{
    fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        match self {
            Effect::Future(_) => write!(f, "Effect::Future(<future>)"),
            // ... other arms
        }
    }
}
```

#### 5. Missing `const fn`
If clippy suggests a function can be `const`, make it const:

```rust
// Clippy will suggest this can be const
pub const fn merge(effects: Vec<Effect<Action>>) -> Effect<Action> {
    Effect::Parallel(effects)
}
```

#### 6. Wildcard Imports
**Avoid** wildcard imports in library code:

**Wrong**:
```rust
use super::*;
```

**Correct**:
```rust
use super::{Arc, Effect, Reducer, RwLock};
```

**Exception**: Wildcard imports are acceptable in tests and examples.

#### 7. Match Arm Consistency
Consolidate identical match arms:

**Wrong**:
```rust
match effect {
    Effect::None => {},
    Effect::Parallel(_) => {},
    Effect::Sequential(_) => {},
}
```

**Correct**:
```rust
match effect {
    Effect::None | Effect::Parallel(_) | Effect::Sequential(_) => {
        // Placeholder implementation
    },
}
```

#### 8. Doc List Indentation
Module docs must be indented or separated with blank lines:

**Wrong**:
```rust
pub mod mocks {
    //! Mock implementations
}
```

**Correct** (moved to outer):
```rust
/// Mock implementations
pub mod mocks {}
```

## Rustfmt Configuration

### Stable Features Only

Only use rustfmt features available in **stable** Rust. Many formatting options require nightly.

**Safe `rustfmt.toml`**:
```toml
edition = "2024"
max_width = 100
hard_tabs = false
tab_spaces = 4
newline_style = "Unix"
fn_params_layout = "Tall"
match_block_trailing_comma = true
chain_width = 60
use_try_shorthand = true
use_field_init_shorthand = true
force_explicit_abi = true
```

**Avoid** (require nightly):
- `imports_granularity`
- `group_imports`
- `wrap_comments`
- `format_code_in_doc_comments`
- `normalize_comments`
- `reorder_impl_items`
- `brace_style`
- `match_arm_blocks`

## Functional-but-Pragmatic Philosophy

### Core Principles

1. **Prefer immutability**, but allow `&mut self` when performance matters
2. **Prefer pure functions**, but recognize async/await patterns
3. **Prefer composition**, but allow practical escape hatches
4. **Favor readability** over theoretical purity

### Practical Applications

#### Effect-as-Value Pattern
Describe side effects as values, don't execute them immediately:

```rust
// Good: Return effect description
fn reduce(&self, state: &mut State, action: Action, env: &Env) -> Vec<Effect> {
    vec![Effect::Database(SaveOrder), Effect::PublishEvent(event)]
}

// Bad: Execute side effects directly
fn reduce(&self, state: &mut State, action: Action, env: &Env) {
    env.database.save(state);  // ❌ Side effect in reducer!
}
```

#### Mutable State in Reducers
It's OK to mutate state in place in reducers for performance:

```rust
trait Reducer {
    fn reduce(
        &self,
        state: &mut Self::State,  // ✅ Mutable for performance
        action: Self::Action,
        env: &Self::Environment,
    ) -> Vec<Effect<Self::Action>>;
}
```

This is pragmatic: tests are still fast and deterministic, and we avoid unnecessary cloning.

#### Static Dispatch Over Dynamic
Prefer generic types (static dispatch) over trait objects (dynamic dispatch):

```rust
// Prefer this (static dispatch, zero-cost)
struct Store<S, A, E, R>
where
    R: Reducer<State = S, Action = A, Environment = E>
{
    reducer: R,
}

// Over this (dynamic dispatch, runtime cost)
struct Store<S, A, E> {
    reducer: Box<dyn Reducer<State = S, Action = A>>,
}
```

**Exception**: Use dynamic dispatch when you need runtime polymorphism (plugins, hot-swapping implementations).

### Error Handling

**Strict Rules**:
- **NEVER** use `unwrap()` or `expect()` in library code (deny by clippy)
- **NEVER** use `panic!()` in library code (deny by clippy)
- **NEVER** leave `todo!()` or `unimplemented!()` in production code (deny by clippy)

**Exceptions** (must be explicitly allowed):
```rust
// Test utilities can use expect with justification
#[allow(clippy::expect_used)]
pub fn test_clock() -> Clock {
    DateTime::parse_from_rfc3339("2025-01-01T00:00:00Z")
        .expect("hardcoded timestamp should always parse")
        .with_timezone(&Utc)
}
```

**Always document** why you're allowing it.

## Code Organization Patterns

### Module Documentation

**Pattern 1: Small modules** - Use outer docs only:
```rust
/// Action types and utilities
///
/// Actions represent all possible state transitions.
pub mod action {}
```

**Pattern 2: Large modules** - No inner docs if you have comprehensive outer docs:
```rust
/// Store runtime for coordinating reducer execution
///
/// Detailed explanation here.
///
/// Store runtime implementation details.
pub mod store {
    // No //! needed, everything is in outer docs
}
```

### Re-exports

Use `pub use` for convenience, but document what you're re-exporting:

```rust
// Re-export commonly used types from dependencies
pub use chrono::{DateTime, Utc};
pub use serde::{Deserialize, Serialize};

// Re-export from submodules for convenience
pub use mocks::{FixedClock, test_clock};
```

### Workspace Structure

For multi-crate projects:

```
project/
├── Cargo.toml          # Workspace root with [workspace.dependencies]
├── core/
│   ├── Cargo.toml      # Uses workspace.dependencies
│   └── src/lib.rs
├── runtime/
│   ├── Cargo.toml      # Depends on core
│   └── src/lib.rs
└── testing/
    ├── Cargo.toml      # Depends on core + runtime
    └── src/lib.rs
```

**Rules**:
- Share dependencies via `[workspace.dependencies]`
- Use `dependency.workspace = true` in crate manifests
- Shared package metadata via `[workspace.package]`
- Workspace lints via `[workspace.lints]`

## Common Gotchas & Solutions

### 1. Workspace Dependencies Cannot Be Optional

**Wrong**:
```toml
[workspace.dependencies]
sqlx = { version = "0.8", optional = true }  # ❌ Error!
```

**Correct**:
```toml
[workspace.dependencies]
sqlx = { version = "0.8" }  # Define without optional

# In individual crate Cargo.toml:
[dependencies]
sqlx = { workspace = true, optional = true }  # ✅ Make it optional here
```

### 2. Edition 2024 Requires Newer MSRV

If you get:
```
error: rust-version 1.83.0 is older than first version (1.85.0) required by edition 2024
```

**Solution**: Update MSRV:
```toml
[workspace.package]
rust-version = "1.85.0"  # Minimum for edition 2024
```

### 3. Future Doesn't Implement Debug

Pin<Box<dyn Future>> doesn't implement Debug. See "Non-Debug Types" section above for manual implementation.

### 4. Async Functions in Placeholders

Placeholders in async functions trigger `unused_async`:

```rust
#[allow(clippy::unused_async)]  // Justified: placeholder implementation
async fn execute_effect(&self, effect: Effect<A>) {
    // Will be implemented in Phase 1
}
```

## Testing Patterns

### Test Organization

```rust
#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_something() {
        // Unit test
    }

    #[tokio::test]
    async fn test_async_something() {
        // Async test
    }
}
```

### Property-Based Testing

Use `proptest` for property tests:

```rust
use proptest::prelude::*;

proptest! {
    #[test]
    fn property_holds(input: Vec<u8>) {
        prop_assert!(check_property(&input));
    }
}
```

## Performance Considerations

### Zero-Cost Abstractions

With static dispatch, generics compile to optimal code:

```rust
// This generic code:
fn reduce<D: Database>(state: &mut State, db: &D) {
    db.save(state);
}

// Monomorphizes to:
fn reduce_with_postgres(state: &mut State, db: &PostgresDatabase) {
    db.save(state);  // Direct call, no vtable lookup
}
```

### Allocation Minimization

In hot paths, consider `SmallVec` for small collections:

```rust
use smallvec::SmallVec;

// Stack-allocated for ≤ 4 items, heap for more
fn reduce(&self, ...) -> SmallVec<[Effect; 4]> {
    let mut effects = SmallVec::new();
    effects.push(Effect::Save);
    effects
}
```

## Documentation Standards

### Crate-Level Documentation

Start `lib.rs` with comprehensive module docs:

```rust
//! # Crate Name
//!
//! Brief description.
//!
//! ## Overview
//!
//! Detailed explanation.
//!
//! ## Example
//!
//! ```ignore
//! // Example code here
//! ```
```

### Function Documentation

```rust
/// Brief one-line description
///
/// Longer detailed explanation if needed.
///
/// # Arguments
///
/// - `state`: Description
/// - `action`: Description
///
/// # Returns
///
/// What the function returns.
///
/// # Errors
///
/// When this function returns an error (if applicable).
///
/// # Panics
///
/// When this function panics (if applicable).
///
/// # Example
///
/// ```
/// // Example usage
/// ```
pub fn my_function(state: &State, action: Action) -> Result<(), Error> {
    // ...
}
```

### Type Documentation

```rust
/// Brief description of the type
///
/// # Type Parameters
///
/// - `S`: State type
/// - `A`: Action type
///
/// # Example
///
/// ```
/// // Example usage
/// ```
pub struct MyType<S, A> {
    // ...
}
```

## Quick Reference Checklist

Before committing Rust code:

- [ ] Run `cargo fmt --all`
- [ ] Run `cargo clippy --all-targets --all-features -- -D warnings`
- [ ] Run `cargo test --all-features`
- [ ] Run `cargo doc --no-deps --all-features`
- [ ] All type names in docs have backticks
- [ ] No `unwrap`/`panic`/`todo` in library code
- [ ] Functions that panic have `# Panics` section
- [ ] No wildcard imports (`use super::*`)
- [ ] Manual `Debug` impl for non-Debug types
- [ ] Const fn where applicable
- [ ] Static dispatch preferred over dynamic

## Common Commands

```bash
# Format code
cargo fmt --all

# Check without building
cargo check --all-features

# Build
cargo build --all-features

# Test
cargo test --all-features

# Lint
cargo clippy --all-targets --all-features -- -D warnings

# Documentation
cargo doc --no-deps --all-features --open

# Documentation with warnings as errors
RUSTDOCFLAGS="-D warnings" cargo doc --no-deps --all-features
```

## Project-Specific Guidelines

### This Project's Philosophy

1. **Functional Core, Imperative Shell**: Pure business logic, effects as values
2. **Explicit over Implicit**: All side effects are visible
3. **Type Safety**: Make invalid states unrepresentable
4. **Testability**: Business logic tests run at memory speed
5. **Performance**: Zero-cost abstractions via static dispatch
6. **Pragmatism**: Functional patterns, but practical when needed

### Architecture Patterns

- **Action**: Unified type for commands and events
- **Reducer**: Pure function `(State, Action, Env) → (State, Effects)`
- **Effect**: Values describing side effects (not execution)
- **Environment**: Trait-based dependency injection
- **Store**: Runtime that coordinates everything

### When in Doubt

- Check the architecture spec: `specs/architecture.md`
- Follow patterns from existing code
- Prefer explicitness over cleverness
- If clippy complains, there's usually a good reason
- Ask for clarification rather than guessing

---

**Remember**: This skill is automatically applied to all Rust code in this project. Follow these guidelines to write idiomatic, performant, and maintainable Rust code.
