---
name: component-check-leakage
description: Checks that any component that is being used by another component is only accessed through the component's interface and does not interact directly with the struct.
argument-hint: "[component-name, component-name, ...]"
---

# Component Leakage Check

This skill audits the codebase for **abstraction leakage** — cases where a component's concrete struct is used directly by another component instead of being accessed through its interface trait.

## The Rule

Each component in `components/` exposes:
- A **concrete struct** (e.g., `LoggerComponent`, `HelloWorldComponent`) — the implementation detail.
- An **interface trait** in `components/interfaces/` (e.g., `ILogger`, `IGreeter`) — the public contract.

When component A consumes component B, it must only interact through B's interface. Direct use of B's struct is leakage.

**Violation (leakage):**
```rust
use logger::LoggerComponent;                          // importing struct from another component
let logger = Arc::new(LoggerComponent::new_default()); // constructing it
let logger: Arc<LoggerComponent> = ...;               // holding a typed reference to the struct
```

**Correct (interface only):**
```rust
use interfaces::ILogger;
// logger injected via receptacle, typed as Arc<dyn ILogger + Send + Sync>
```

## Scope and Exceptions

- **Components under `components/`** are subject to this rule (excluding `interfaces/` and `component-framework/`).
- **Apps under `apps/`** are wiring points — they legitimately instantiate concrete structs. Flag them only as a note, not a violation.
- **Unit test files** (`#[cfg(test)]` blocks and files in `tests/`) may use concrete structs for test fixtures. These are warnings, not errors.
- **A component's own source files** constructing its own struct are fine — a component knows its own type.
- **Dynamic loading entry points** (`extern "C" fn create_component`) constructing and returning the struct as a trait object are fine.

## Detection Strategy

For each component under investigation (all components if no `$ARGUMENTS`, otherwise only those named):

### Step 1 — Identify the component's concrete struct name

Read the `define_component!` macro invocation in the component's `src/lib.rs`. The struct name is the identifier immediately following `pub` in the macro body (e.g., `pub LoggerComponent { ... }`).

### Step 2 — Find all other components that list it as a Cargo dependency

Search all `Cargo.toml` files under `components/` and `apps/` for a dependency entry whose crate name matches the component being checked. Use the package name (hyphenated) from the component's `Cargo.toml` `[package]` section.

### Step 3 — Check each dependent crate's source for leakage

For each crate that lists the target component as a dependency, grep its source files (`src/**/*.rs`) for:

1. **Direct import of the struct:**
   ```
   use <crate_name>::<StructName>
   use <crate_name>::{..., <StructName>, ...}
   ```
2. **Qualified path usage:**
   ```
   <crate_name>::<StructName>::
   Arc<dyn ... | Arc<<StructName>>   (type annotations containing the struct)
   ```
3. **Type annotations holding the struct** (not behind `dyn`):
   ```
   : Arc<<StructName>>
   : <StructName>
   ```

Exclude matches in:
- The component's own `src/` files (self-reference)
- Lines inside `#[cfg(test)]` modules and `tests/` directories (mark separately as warnings)
- `apps/` crates (mark separately as notes)

### Step 4 — Identify the correct interface

Cross-reference `components/interfaces/src/lib.rs` to find which interface trait(s) the component provides (look for `use <crate>::...; pub use` re-exports or the trait definitions). This helps frame the fix suggestion.

### Step 5 — Report

For each component checked, output a structured report:

```
## <ComponentName> (crate: <crate-name>)

### Violations (must fix)
- <file>:<line> — <dependent-crate> uses `<StructName>` directly
  Fix: replace with `Arc<dyn <IInterface> + Send + Sync>` via receptacle

### Warnings (test code — consider fixing)
- <file>:<line> — test uses `<StructName>` directly

### Notes (apps — acceptable but review)
- <file>:<line> — app wiring uses `<StructName>` to construct and bind

### Clean ✓
No leakage found.
```

If `$ARGUMENTS` are provided, only check components whose names (case-insensitive, hyphen/underscore normalised) appear in the argument list. Otherwise check all components.

At the end, print a summary line: `N violation(s) across M component(s)`.

## Example Run

```
/component-check-leakage logger
```

Expected: finds that `gpu-services` uses `LoggerComponent` directly in `src/lib.rs` (tests) and `src/bin/p2p_server.rs` (main code), reports violations and suggests using `ILogger` via a receptacle instead.
