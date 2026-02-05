---
name: cargo-build
description: Run cargo build with consistent flags and colorless output for CI/log parsing. Formats code first, then builds all workspace targets. Trigger when asked to build Rust projects or prepare binaries.
compatibility: Requires rustfmt, cargo
---

# Cargo Build

## Overview

Standardize `cargo build` runs with consistent flags, colorless output, and format-first workflow. Ensures reproducible builds across environments.

## Quick Start

1. Run `skills/cargo-build/scripts/run_build.sh` from repository root.
2. Fix formatting errors first, then address compiler errors.
3. Rerun script until build succeeds.

## Workflow

1. **Format first**: `cargo fmt --all` ensures code is formatted before building.
2. **Build command**: `cargo build --all-features --workspace --all-targets --message-format=short`
3. **Environment**:
    - `NO_COLOR=1` - Disables color output
    - `CARGO_TERM_COLOR=never` - Ensures cargo output is colorless
4. **Scope**: Builds all targets (lib, bin, tests, examples, benches) across entire workspace with all features enabled.
5. **Output format**: `--message-format=short` provides concise, parseable output.

## Best Practices

- **Always disable colors**: Use `cargo --color=never` or set `CARGO_TERM_COLOR=never` for consistent, parseable output.
- **Format before build**: Run `cargo fmt --all` to catch formatting issues early.
- **Use workspace builds**: Build entire workspace with `--workspace` unless targeting specific packages.
- **Enable all features**: Use `--all-features` to catch feature-gated compilation errors.
- **Run from root**: Execute from repository root to ensure proper workspace resolution.
- **Avoid ad hoc flags**: Use consistent, documented build commands rather than one-off invocations.

## Common Variations

### Target specific package

```bash
cargo --color=never build -p <package-name>
```

### Release build

```bash
cargo --color=never build --release --workspace --all-targets
```

### Check without building

```bash
cargo --color=never check --all-features --workspace --all-targets
```

## Failure Handling

1. **Formatting failures**: Fix code formatting issues reported by `cargo fmt`.
2. **Compilation errors**: Address errors in the order reported by the compiler.
3. **Rerun full script**: Don't run partial commands; always use the complete workflow.
