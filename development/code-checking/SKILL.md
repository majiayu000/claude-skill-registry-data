---
name: Code Checking
description: Check and lint Rust/TypeScript code using justfile tasks (just check-crate, just clippy-crate). Use after code changes, when user mentions compilation, type checking, linting, clippy warnings, or needs to validate code quality. Runs cargo check and clippy with proper flags.
---

# Code Checking Skill

This skill provides code validation and linting operations for the project codebase.

## When to Use This Skill

Use this skill when you need to:
- Validate Rust or TypeScript code after making changes
- Run compiler checks without building
- Lint code with clippy
- Ensure code quality before commits or PRs

## Available Commands

### Check Rust Code
```bash
just check-rs [EXTRA_FLAGS]
```
Checks Rust code using `cargo check --all-targets`. This runs the compiler without producing binaries.

**Alias**: `just check` (same as `check-rs`)

Examples:
- `just check-rs` - check all Rust code
- `just check-rs --release` - check with release optimizations

### Check Specific Crate
```bash
just check-crate <CRATE> [EXTRA_FLAGS]
```
Checks a specific crate with all its targets using `cargo check --package <CRATE> --all-targets`.

Examples:
- `just check-crate metadata-db` - check the metadata-db crate
- `just check-crate common --release` - check common crate with release mode

### Lint Rust Code (Clippy)
```bash
just clippy [EXTRA_FLAGS]
```
Lints all Rust code using `cargo clippy --all-targets`. Clippy catches common mistakes and suggests improvements.

Examples:
- `just clippy` - lint all code
- `just clippy -- -D warnings` - treat warnings as errors

### Lint Specific Crate
```bash
just clippy-crate <CRATE> [EXTRA_FLAGS]
```
Lints a specific crate using `cargo clippy --package <CRATE> --all-targets --no-deps`.

The `--no-deps` flag ensures clippy only analyzes the specified crate's code, not its dependencies. This provides:
- **Faster execution**: Skip checking dependency code you don't control
- **Focused output**: See only warnings from your crate, not transitive dependencies
- **Actionable results**: All warnings shown are in code you can fix

Examples:
- `just clippy-crate admin-api` - lint the admin-api crate only
- `just clippy-crate dataset-store -- -D warnings` - lint with warnings as errors

### Check All Code
```bash
just check-all
```
Checks both Rust and TypeScript code by running `check-rs` and `check-ts` sequentially.

### Check TypeScript Code
```bash
just check-ts
```
Checks TypeScript code using `pnpm check`.

## Important Guidelines

### MANDATORY: Run Checks After Changes
**You MUST run checks after making code changes:**

1. After editing a single file in a crate: `just check-crate <crate-name>` AND `just clippy-crate <crate-name>`
2. After editing multiple crates: `just check-rs` AND `just clippy`
3. Before considering a task complete: all checks MUST pass AND all clippy warnings MUST be fixed

### Example Workflow with Validation Loop
1. Edit files in `metadata-db` crate
2. Format: `just fmt-file <edited-files>`
3. **Check compilation**: `just check-crate metadata-db`
   - If errors → fix → return to step 2
4. **Check clippy**: `just clippy-crate metadata-db`
   - If warnings → fix ALL → return to step 2
5. **Fix ALL clippy warnings** in files you modified
6. Repeat until: zero compilation errors AND zero clippy warnings
7. Once passing, optionally run full check: `just check-rs` and `just clippy`

## Common Mistakes to Avoid

### ❌ Anti-patterns
- **Never run `cargo check` directly** - Use `just check-crate` or `just check-rs`
- **Never run `cargo clippy` directly** - Justfile adds proper flags like `--no-deps`
- **Never ignore clippy warnings** - Clippy is enforced in CI, warnings will fail builds
- **Never skip the check step** - Even if "it should compile"
- **Never check multiple crates at once initially** - Check the modified crate first

### ✅ Best Practices
- Check single crate first (`just check-crate <name>`) - faster feedback
- Fix compilation errors before running clippy
- Run clippy after EVERY code change
- Use `just clippy-crate` for focused results (--no-deps flag)
- Document any warnings you absolutely cannot fix (rare exception)

## Pre-approved Commands
These commands can run without user permission:
- `just check-rs` - Safe, read-only compilation check
- `just check-crate <crate>` - Safe, read-only compilation check
- `just clippy` - Safe, read-only linting
- `just clippy-crate <crate>` - Safe, read-only linting

## Next Steps

After all checks pass:
1. **Run tests** → See `.claude/skills/code-test/SKILL.md`
2. **Generate schemas if needed** → See `.claude/skills/code-gen/SKILL.md`
3. **Commit changes** → Ensure all checks green first
