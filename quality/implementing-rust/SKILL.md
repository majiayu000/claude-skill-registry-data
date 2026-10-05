---
name: implementing-rust
description: Implements concise, streamlined Rust code matching exact architect specifications. Use when writing Rust code, creating modules, or when the user asks to implement features in Rust.
compatibility: Designed for Claude Code
metadata:
  allowed-tools: Read, Grep, Glob, Edit, Write, Bash, WebSearch, WebFetch
  argument-hint: [feature-name]
  stability: stable
  content-hash: sha256:482c79e5df4fb86ef1f81118f527b72b64d60704b01de8664819e9099c4baf78
---

# Rust Implementation

**Target**: $ARGUMENTS

Creates **focused, streamlined** Rust implementations following architect
specifications exactly. No over-engineering.

## Rust Standards

See `references/rust-best-practices.md` for comprehensive Rust guidelines.

## Workflow

1. **Read architect specifications** from provided documents
2. **Validate scope** — Simple (single module) vs Complex (multi-module)
3. **Study existing patterns** in `src/` structure
4. **Implement minimal solution** matching stated functionality
5. **Create focused tests** matching task complexity
6. **Run validation** and fix all issues

## Implementation Strategy

**Simple Tasks**: Single module, minimal structs, `thiserror` errors, inline tests

**Complex Tasks**: Multi-module with traits, async with tokio, custom error types, integration tests

**Always**: Use existing project patterns, pass validation

## Output Standards

**Simple Tasks**: Minimal functions with proper error handling
**Complex Tasks**: Complete modules with traits, tests, and documentation
**All outputs**: Concise, streamlined, no unnecessary complexity

## Quality Checks

Before completing any task:

```bash
cargo test && cargo clippy -- -D warnings && cargo fmt --check
```

All tests, lints, and formatting must pass.
