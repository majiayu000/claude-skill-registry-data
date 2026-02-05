---
name: format
description: Format Rust and Meson code using justfile tasks (just fmt-rs, just fmt-meson). Use when editing .rs or meson files, mentions formatting, code style, rustfmt, cleanup, or before commits/PRs. Ensures consistent code style across the codebase.
allowed-tools: Bash(just --list:*), Bash(just fmt-rs:*), Bash(just fmt-rs-check:*), Bash(just fmt-meson:*), Bash(just fmt-meson-check:*)
---

# Code Formatting Skill

This skill provides code formatting operations for the nx-std monorepo, which is a Rust workspace with Meson build system.

## When to Use This Skill

Use this skill when you need to:

- Format code after editing Rust or Meson files
- Check if code meets formatting standards
- Ensure code formatting compliance before commits

## Available Commands

### Format Rust Code

```bash
just fmt-rs
```

Formats all Rust code using `cargo fmt --all`. This is the primary formatting command for Rust.

**Alias**: `just fmt` (same as `fmt-rs`)

### Check Rust Formatting

```bash
just fmt-rs-check
```

Checks Rust code formatting without making changes using `cargo fmt --all -- --check`.

**Alias**: `just fmt-check` (same as `fmt-rs-check`)

### Format Meson Files

```bash
just fmt-meson
```

Formats all Meson build files (`meson.build`, `meson.options`, `justfile`).

### Check Meson Formatting

```bash
just fmt-meson-check
```

Checks Meson file formatting without making changes.

## Important Guidelines

### MANDATORY: Format After Every Edit

**You MUST run formatting immediately after editing ANY Rust or Meson file.**

This is a critical requirement from the project's development workflow:

- Never skip formatting after file edits
- Format Rust files with `just fmt-rs` after editing `.rs` files
- Format Meson files with `just fmt-meson` after editing `meson.build`, `meson.options`, or `justfile`
- Run formatting before any check or test commands

### Example Workflow

**After editing Rust file**:
1. Edit a Rust file: `crates/nx-alloc/src/lib.rs`
2. **IMMEDIATELY** run: `just fmt-rs`
3. Then run checks: `just check-rs`

**After editing Meson file**:
1. Edit a Meson file: `subprojects/libnx/meson.build`
2. **IMMEDIATELY** run: `just fmt-meson`
3. Then run checks: `just configure`

## Common Mistakes to Avoid

### ❌ Anti-patterns

- **Never run `cargo fmt` directly** - Use `just fmt-rs`
- **Never run `rustfmt` directly** - The justfile includes proper configuration
- **Never skip formatting** - Even "minor" edits need formatting
- **Never format after multiple edits** - Format after EACH file type edit
- **Never commit unformatted code** - Always run `just fmt-rs-check` and `just fmt-meson-check` before commits

### ✅ Best Practices

- Format immediately after each edit
- Run `just fmt-rs` after editing Rust files
- Run `just fmt-meson` after editing Meson/justfile files
- Run `just fmt-rs-check` and `just fmt-meson-check` to verify formatting before commits
- Format before running build, check, or test commands

## Formatting Configuration

### Rust Formatting

Rust formatting uses:
- Nightly rustfmt (specified in `rust-toolchain.toml`)
- Configuration in `rustfmt.toml` with unstable features
- Import grouping: std, external crates, local
- Import granularity at crate level

### Meson Formatting

Meson formatting:
- Consistent indentation and style
- Applied to `meson.build`, `meson.options`, and `justfile`

## Next Steps

After formatting your code:

1. **Check compilation** → Run `just check-rs` for Rust
2. **Run clippy** → Run `just clippy` for linting
3. **Build targets** → See `.claude/skills/build/SKILL.md`
4. **Run tests** → Run `just build-tests`
