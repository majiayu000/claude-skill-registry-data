---
name: reviewing-go
description: Provides concise, focused Go code reviews matching exact task complexity requirements. Use when reviewing Go code quality, concurrency safety, or when the user asks for code review.
compatibility: Designed for Claude Code
metadata:
  allowed-tools: Read, Grep, Glob, WebFetch, WebSearch
  argument-hint: [file-or-directory]
  stability: stable
  content-hash: sha256:6f31b28e0cea1077916a248eab78da6e097af5d82ed346780e7b31823257fe5a
---

# Review Context

- Changed files: !`git diff --name-only HEAD~1 2>/dev/null || echo "No recent commits"`
- Staged files: !`git diff --staged --name-only`

## Code Review

**Scope**: $ARGUMENTS

Delivers **focused, streamlined** Go code reviews matching stated task
requirements exactly. No over-analysis.

## Go Standards

See `references/go-best-practices.md` for comprehensive Go guidelines.

## Workflow

1. **Read task requirements** to understand expected scope
2. **Check validation passes** before detailed review
3. **Match review depth** to task complexity (simple vs complex)
4. **Validate requirements** — does implementation match task scope exactly?
5. **Issue focused feedback** with specific file paths and line numbers

## Review Strategy

**Simple Tasks (single package)**: Error handling, requirements match,
basic quality

**Complex Tasks (multi-package)**: Above plus architecture, concurrency
patterns, context propagation, comprehensive testing

**Always**: Use existing project patterns, check goroutine lifecycle

## Review Checklist

**Safety & Security**:

- [ ] No ignored errors (every `err` handled or documented)
- [ ] SQL queries use parameterized statements
- [ ] JSON decoder uses `DisallowUnknownFields()` for untrusted input
- [ ] No hardcoded credentials

**Requirements Match**:

- [ ] Implements exactly what was requested
- [ ] No over-engineering or scope creep
- [ ] Appropriate complexity level

**Code Quality**:

- [ ] Follows project patterns
- [ ] Error wrapping uses `fmt.Errorf("context: %w", err)`
- [ ] Interfaces small and defined where consumed
- [ ] `context.Context` passed as first param, not stored in struct

**Concurrency**:

- [ ] Every goroutine has a stop signal (`ctx.Done()` or channel close)
- [ ] Shared state protected by mutex or channels
- [ ] No goroutine leaks

**Structural Health**:

- [ ] No function exceeds cognitive complexity threshold
- [ ] No copy-paste duplication across methods
- [ ] `internal/` used for crate-private packages

## Output Standards

**Simple Tasks**: CRITICAL issues only, clear approval when requirements met
**Complex Tasks**: CRITICAL/WARNINGS/SUGGESTIONS with specific fixes
**All reviews**: Concise, streamlined, no unnecessary complexity analysis
