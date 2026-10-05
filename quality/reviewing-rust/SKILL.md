---
name: reviewing-rust
description: Provides concise, focused Rust code reviews matching exact task complexity requirements. Use when reviewing Rust code quality, safety, or when the user asks for code review.
compatibility: Designed for Claude Code
metadata:
  allowed-tools: Read, Grep, Glob, WebFetch, WebSearch
  argument-hint: [file-or-directory]
  stability: stable
  content-hash: sha256:e3c44dc62159fe501bb2d9ffd531773daf004d180c40f554efbb775b2fd8ce9d
---

# Review Context

- Changed files: !`git diff --name-only HEAD~1 2>/dev/null || echo "No recent commits"`
- Staged files: !`git diff --staged --name-only`

## Code Review

**Scope**: $ARGUMENTS

Delivers **focused, streamlined** Rust code reviews matching stated task
requirements exactly. No over-analysis.

## Rust Standards

See `references/rust-best-practices.md` for comprehensive Rust guidelines.

## Workflow

1. **Read task requirements** to understand expected scope
2. **Check validation passes** before detailed review
3. **Match review depth** to task complexity (simple vs complex)
4. **Validate requirements** — does implementation match task scope exactly?
5. **Issue focused feedback** with specific file paths and line numbers

## Review Strategy

**Simple Tasks (single module)**: Safety, error handling, requirements match,
basic quality

**Complex Tasks (multi-module)**: Above plus architecture, ownership patterns,
async correctness, comprehensive testing

**Always**: Use existing project patterns, check for unsafe blocks

## Review Checklist

**Safety & Security**:

- [ ] No unnecessary `unsafe` blocks (every block has `// SAFETY:` comment)
- [ ] No `unwrap()`/`expect()` in production paths
- [ ] All external input validated at boundaries
- [ ] `cargo audit` clean (no known CVEs)

**Requirements Match**:

- [ ] Implements exactly what was requested
- [ ] No over-engineering or scope creep
- [ ] Appropriate complexity level

**Code Quality**:

- [ ] Follows project patterns in `src/`
- [ ] Proper error handling with `?` and typed errors
- [ ] Ownership/borrowing patterns correct (no unnecessary clones)
- [ ] Tests cover stated functionality

**Structural Health**:

- [ ] No function exceeds cognitive complexity threshold
- [ ] No copy-paste duplication across methods
- [ ] `pub(crate)` used for crate-internal types

## Output Standards

**Simple Tasks**: CRITICAL issues only, clear approval when requirements met
**Complex Tasks**: CRITICAL/WARNINGS/SUGGESTIONS with specific fixes
**All reviews**: Concise, streamlined, no unnecessary complexity analysis
