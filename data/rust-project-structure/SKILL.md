---
name: rust-project-structure
description: Rust project organization and structure. Use when creating new projects, organizing modules, setting up workspaces, configuring Cargo.toml, or migrating between editions.
allowed-tools: Read, Write, Edit, Bash, Grep, Glob
---

# Rust Project Structure and Organization

Modern Rust project organization following 2024 Edition best practices.

## Rust Editions

### Edition Overview

| Edition | Release | Resolver | Key Features |
|---------|---------|----------|--------------|
| 2015 | Rust 1.0 | 1 | Original edition, `mod.rs` required |
| 2018 | Rust 1.31 | 1 | `mod.rs` optional, `async`/`await` keywords, path changes |
| 2021 | Rust 1.56 | 2 | Disjoint capture, `IntoIterator` for arrays, feature resolver |
| 2024 | Rust 1.85+ | 3 | Async closures, RPIT lifetime capture, MSRV-aware resolver |

### Cargo.toml Edition Configuration

```toml
[package]
name = "my-crate"
version = "0.1.0"
edition = "2024"           # Use latest edition
rust-version = "1.92"      # Project MSRV (2024 edition minimum is 1.85)

[workspace]
resolver = "3"             # Required for virtual workspaces
```

### Edition Migration

```bash
# Check what changes are needed
cargo fix --edition --dry-run

# Apply automatic fixes
cargo fix --edition

# Update Cargo.toml manually after fixes
# edition = "2021" -> edition = "2024"
```

## Workspace Resolver

### Resolver Versions

| Version | Default For | Key Behavior |
|---------|-------------|--------------|
| 1 | 2015, 2018 | Basic dependency resolution |
| 2 | 2021 | Feature resolver, platform-specific deps, dev-deps isolation |
| 3 | 2024 | MSRV-aware, uses `rust-version` to select compatible deps |

### Resolver 3 (Recommended)

```toml
[workspace]
members = ["crates/*"]
resolver = "3"  # MSRV-aware dependency resolution

[workspace.package]
edition = "2024"
rust-version = "1.92"
license = "MIT"
repository = "https://github.com/user/project"
```

Resolver 3 benefits:
- Automatically selects dependency versions compatible with your `rust-version`
- Falls back to compatible versions instead of failing
- Reduces "dependency too new" errors

## Module Organization

### Modern Style (Recommended - 2018+)

```
src/
├── lib.rs              # Crate root
├── config.rs           # mod config
├── config/             # Submodules of config
│   ├── parser.rs       # mod config::parser
│   └── validation.rs   # mod config::validation
├── handlers.rs         # mod handlers  
└── handlers/
    ├── auth.rs         # mod handlers::auth
    └── api.rs          # mod handlers::api
```

**In `lib.rs`:**
```rust
pub mod config;
pub mod handlers;
```

**In `config.rs`:**
```rust
pub mod parser;
pub mod validation;

// Re-exports for convenience
pub use parser::Parser;
pub use validation::validate;
```

### Legacy Style (mod.rs) - Still Valid

```
src/
├── lib.rs
└── config/
    ├── mod.rs          # mod config (legacy)
    ├── parser.rs
    └── validation.rs
```

**Important:** Cannot mix both styles - `config.rs` and `config/mod.rs` cannot coexist.

### Private Modules

```rust
// In lib.rs
mod internal;           // Private module (no `pub`)
pub mod public_api;     // Public module

pub(crate) mod shared;  // Visible within crate only
```

## Workspace Structure

### Multi-Crate Workspace (Nebula Pattern)

```
project/
├── Cargo.toml              # Workspace root
├── CLAUDE.md
├── crates/
│   ├── core/
│   │   ├── Cargo.toml
│   │   └── src/lib.rs
│   ├── domain/
│   │   ├── parameter/
│   │   │   ├── Cargo.toml
│   │   │   └── src/lib.rs
│   │   └── action/
│   │       ├── Cargo.toml
│   │       └── src/lib.rs
│   └── ui/
│       ├── Cargo.toml
│       └── src/lib.rs
└── apps/
    └── cli/
        ├── Cargo.toml
        └── src/main.rs
```

### Workspace Cargo.toml

```toml
[workspace]
members = [
    "crates/core",
    "crates/domain/*",
    "crates/ui",
    "apps/*",
]
exclude = ["experiments"]
resolver = "3"

[workspace.package]
version = "0.1.0"
edition = "2024"
rust-version = "1.92"
authors = ["Your Name <you@example.com>"]
license = "MIT"

[workspace.dependencies]
# Shared dependencies - use workspace = true in member crates
tokio = { version = "1.43", features = ["full"] }
serde = { version = "1.0", features = ["derive"] }
thiserror = "2.0"
tracing = "0.1"

# Internal crates
nebula-core = { path = "crates/core" }
nebula-parameter = { path = "crates/domain/parameter" }
```

### Member Crate Cargo.toml

```toml
[package]
name = "nebula-parameter"
version.workspace = true
edition.workspace = true
rust-version.workspace = true
license.workspace = true

[dependencies]
nebula-core.workspace = true
serde.workspace = true
thiserror.workspace = true

[dev-dependencies]
tokio = { workspace = true, features = ["test-util"] }
```

## Crate Organization Patterns

### Library Crate Structure

```
src/
├── lib.rs              # Public API, re-exports
├── error.rs            # Error types
├── types.rs            # Core types
├── builder.rs          # Builder patterns
└── internal/           # Private implementation
    ├── mod.rs
    └── helpers.rs
```

**`lib.rs` Pattern:**
```rust
//! Crate-level documentation
//!
//! # Examples
//!
//! ```rust
//! use my_crate::prelude::*;
//! ```

mod error;
mod types;
mod builder;
mod internal;

// Public API
pub use error::{Error, Result};
pub use types::{Config, Options};
pub use builder::ConfigBuilder;

/// Prelude for convenient imports
pub mod prelude {
    pub use crate::{Config, ConfigBuilder, Error, Result};
}
```

### Binary Crate Structure

```
src/
├── main.rs             # Entry point, minimal logic
├── cli.rs              # CLI argument parsing
├── app.rs              # Application logic
├── commands/           # Subcommands
│   ├── mod.rs
│   ├── run.rs
│   └── init.rs
└── config.rs           # Configuration
```

**`main.rs` Pattern:**
```rust
mod cli;
mod app;
mod commands;
mod config;

fn main() -> anyhow::Result<()> {
    let args = cli::parse();
    let config = config::load()?;
    app::run(args, config)
}
```

## Feature Organization

### Feature Flags in Cargo.toml

```toml
[features]
default = ["std"]
std = []
full = ["async", "serde", "validation"]
async = ["tokio", "async-trait"]
serde = ["dep:serde", "dep:serde_json"]
validation = ["dep:validator"]

[dependencies]
tokio = { version = "1.43", optional = true }
serde = { version = "1.0", optional = true }
serde_json = { version = "1.0", optional = true }
validator = { version = "0.18", optional = true }
```

### Conditional Compilation

```rust
#[cfg(feature = "async")]
pub mod async_api;

#[cfg(feature = "serde")]
mod serde_impl {
    use serde::{Serialize, Deserialize};
    
    impl Serialize for crate::Config { /* ... */ }
}

#[cfg(all(feature = "async", feature = "validation"))]
pub async fn validate_async(input: &str) -> Result<(), Error> {
    // Available only with both features
}
```

## Testing Organization

### Test Structure

```
src/
├── lib.rs
└── parser.rs

tests/                  # Integration tests
├── common/
│   └── mod.rs          # Shared test utilities
├── integration_test.rs
└── api_tests.rs
```

### Test Modules in Source

```rust
// In src/parser.rs
pub fn parse(input: &str) -> Result<Ast, Error> {
    // implementation
}

#[cfg(test)]
mod tests {
    use super::*;
    
    #[test]
    fn test_parse_empty() {
        assert!(parse("").is_err());
    }
    
    #[test]
    fn test_parse_valid() {
        let result = parse("valid input").unwrap();
        assert_eq!(result.nodes.len(), 1);
    }
}
```

### Integration Tests

```rust
// tests/integration_test.rs
use my_crate::prelude::*;

mod common;

#[test]
fn test_full_workflow() {
    let config = common::setup();
    // test implementation
}
```

## Documentation Structure

### Crate Documentation

```rust
// src/lib.rs

//! # My Crate
//!
//! Brief description of what this crate does.
//!
//! ## Features
//!
//! - Feature 1
//! - Feature 2
//!
//! ## Quick Start
//!
//! ```rust
//! use my_crate::Config;
//!
//! let config = Config::builder()
//!     .option("value")
//!     .build()?;
//! # Ok::<(), my_crate::Error>(())
//! ```
//!
//! ## Modules
//!
//! - [`config`] - Configuration types
//! - [`parser`] - Parsing utilities
```

## Best Practices

### Module Guidelines

1. **One concept per module** - Don't mix unrelated types
2. **Shallow hierarchies** - Prefer 2-3 levels max
3. **Clear public API** - Use `pub use` re-exports
4. **Private by default** - Only expose what's needed

### Naming Conventions

```
crate-name              # kebab-case for crate names
crate_name              # snake_case for module names (Rust converts automatically)
TypeName                # UpperCamelCase for types
function_name           # snake_case for functions
CONSTANT_NAME           # SCREAMING_SNAKE_CASE for constants
```

### Workspace Guidelines

1. **Group by domain** - `crates/domain/`, `crates/infra/`
2. **Shared dependencies** - Use `[workspace.dependencies]`
3. **Consistent metadata** - Use `version.workspace = true`
4. **Feature flags** - Coordinate across workspace

## Nebula-Specific Conventions

```
nebula/
├── Cargo.toml                  # Workspace root, resolver = "3"
├── CLAUDE.md                   # Project guidelines
├── crates/
│   ├── nebula-core/            # Identifiers, scope
│   ├── nebula-value/           # Runtime types
│   ├── nebula-parameter/       # Parameter definitions
│   ├── nebula-action/          # Action execution
│   ├── nebula-expression/      # Expression evaluation
│   └── nebula-ui/              # UI framework
└── apps/
    └── nebula-app/             # Main application
```

- Each crate has own error type (no shared `nebula-error`)
- Use `thiserror` for error definitions
- Prelude pattern for common re-exports
- Modern module style (no `mod.rs`)
