---
name: rust-cargo
description: >
  Manage Rust packages, multi-crate Cargo workspaces, conditional compilation
  features, dependency graphs, benchmarks, and crates.io publishing. Use when
  structuring Cargo.toml, managing workspace dependencies with inheritance,
  configuring features additively, writing integration tests and benchmarks,
  or running cargo audit and cargo package checks.
compatibility: >
  Agent Skills-compatible coding agents operating on Cargo workspaces and
  Rust projects.
metadata:
  author: michaelweissdev
  version: "1.0.0"
  tags: "rust, cargo, workspaces, dependencies, crates, packaging, build"
  topics: "programming-languages, devtools, software-development"
---

# Cargo Workspace & Dependency Management

Cargo is Rust's official package manager, build system, and test runner. Effective Cargo architecture keeps builds fast, prevents dependency bloat, structures multi-crate workspaces cleanly, and prepares crates for reliable publishing on crates.io.

## Core Rules

1. **Features must be additive**: Enabling a feature must never disable functionality or remove public API types. Features should compose seamlessly.
2. **Commit `Cargo.lock` for binaries; omit/ignore for standalone libraries**: Applications require reproducible builds; libraries should test against the minimum and latest compatible ranges.
3. **Use workspace inheritance**: In multi-crate workspaces, centralize versions, lints, and common dependencies in the root `[workspace.dependencies]` table.
4. **Audit dependencies regularly**: Use `cargo audit` to detect known vulnerabilities (RUSTSEC advisories).
5. **Verify package before publishing**: Always run `cargo package --list` and `cargo test --all-features` before `cargo publish`.

---

## 1. Multi-Crate Workspace Architecture

Structure larger Rust systems into focused, independently testable crates:

```text
my-workspace/
├── Cargo.toml          # Workspace root manifest
├── Cargo.lock
├── crates/
│   ├── app-core/       # Core business logic (no UI or network dependencies)
│   │   ├── Cargo.toml
│   │   └── src/lib.rs
│   ├── app-cli/        # CLI binary frontend
│   │   ├── Cargo.toml
│   │   └── src/main.rs
│   └── app-storage/    # Database / I/O integration
│       ├── Cargo.toml
│       └── src/lib.rs
```

### Workspace Root `Cargo.toml`
```toml
[workspace]
resolver = "2"
members = ["crates/*"]

[workspace.package]
version = "0.4.0"
edition = "2021"
rust-version = "1.75.0"
authors = ["Michael Weiss <dev@example.com>"]
license = "MIT OR Apache-2.0"
repository = "https://github.com/example/my-workspace"

[workspace.dependencies]
serde = { version = "1.0.197", features = ["derive"] }
serde_json = "1.0.114"
tokio = { version = "1.36.0", features = ["full"] }
thiserror = "1.0.57"
tracing = "0.1.40"

# Local workspace crate references
app-core = { path = "crates/app-core" }
app-storage = { path = "crates/app-storage" }
```

### Subcrate `crates/app-cli/Cargo.toml`
```toml
[package]
name = "app-cli"
version.workspace = true
edition.workspace = true
license.workspace = true

[dependencies]
app-core.workspace = true
tokio.workspace = true
tracing.workspace = true
clap = { version = "4.5.1", features = ["derive"] }
```

---

## 2. Designing Additive Features

Declare optional features in `Cargo.toml`:

```toml
[features]
default = ["std"]
std = []
json = ["dep:serde_json", "dep:serde"]
async = ["dep:tokio"]

[dependencies]
serde = { version = "1.0", optional = true }
serde_json = { version = "1.0", optional = true }
tokio = { version = "1.36", optional = true }
```

---

## 3. Essential Cargo Commands

```bash
# Check code syntax and types without full code generation (fastest loop)
cargo check --workspace --all-targets

# Run tests across all workspace crates and features
cargo test --workspace --all-features

# Audit dependencies for known vulnerabilities
cargo audit

# Check for unused dependencies (requires cargo-machete)
cargo machete

# Dry-run package build to verify included files and metadata
cargo package --workspace
```

---

## 4. Common Mistakes and Anti-Patterns

| Anti-Pattern | Risk | Correct Practice |
| :--- | :--- | :--- |
| Non-additive features (Feature A breaks Feature B) | Compilation fails when both features are activated | Keep features strictly additive |
| Duplicated dependency versions across workspace | Bloats compilation time and binary size | Use `[workspace.dependencies]` |
| Missing `description` or `license` in published crate | `cargo publish` rejects the crate | Define in root `[workspace.package]` |
| Committing local paths in published dependencies | Crate cannot be built by third parties from crates.io | Use version specifier alongside path: `foo = { path = "../foo", version = "1.0" }` |

---

## 5. Verification Checklist

- [ ] `cargo check --workspace --all-targets` succeeds.
- [ ] `cargo test --workspace --all-features` passes completely.
- [ ] `cargo clippy --workspace --all-targets --all-features` returns no warnings.
- [ ] No duplicate dependencies or conflicting version locks in `Cargo.lock`.
- [ ] `cargo package` packages without uncommitted or unexpected files.
