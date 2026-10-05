---
name: reviewing-typescript
description: Provides concise, focused TypeScript/React code reviews matching exact task complexity requirements. Use when reviewing TypeScript code quality, type safety, or when the user asks for code review.
compatibility: Designed for Claude Code
metadata:
  allowed-tools: Read, Grep, Glob, WebFetch, WebSearch
  argument-hint: [file-or-directory]
  stability: stable
  content-hash: sha256:b285fa9c65674635325a88669c5f6662ef5059d788e570b57ded2804eaf7b57e
---

# Review Context

- Changed files: !`git diff --name-only HEAD~1 2>/dev/null || echo "No recent commits"`
- Staged files: !`git diff --staged --name-only`

## Code Review

**Scope**: $ARGUMENTS

Delivers **focused, streamlined** TypeScript/React code reviews matching stated task
requirements exactly. No over-analysis.

## TypeScript Standards

See `references/typescript-best-practices.md` for comprehensive TypeScript guidelines.

## Workflow

1. **Read task requirements** to understand expected scope
2. **Check validation passes** before detailed review
3. **Match review depth** to task complexity (simple vs complex)
4. **Validate requirements** — does implementation match task scope exactly?
5. **Issue focused feedback** with specific file paths and line numbers

## Review Strategy

**Simple Tasks (single module)**: Type safety, error handling, requirements match,
basic quality

**Complex Tasks (multi-module)**: Above plus architecture, React patterns,
async correctness, comprehensive testing

**Always**: Use existing project patterns, check for `any` types

## Review Checklist

**Type Safety & Security**:

- [ ] No `any` types (use `unknown` with type guards)
- [ ] Proper generics and discriminated unions
- [ ] All external input validated at boundaries
- [ ] No secrets or credentials in source code

**React Patterns**:

- [ ] No unnecessary re-renders (proper memoization only when needed)
- [ ] Correct useEffect dependency arrays
- [ ] Custom hooks extracted for shared logic
- [ ] Accessibility: semantic HTML, ARIA attributes, keyboard navigation

**Bundle & Performance**:

- [ ] No barrel imports of large libraries (import specific modules)
- [ ] Dynamic imports for heavy components
- [ ] No blocking operations in render path

**Requirements Match**:

- [ ] Implements exactly what was requested
- [ ] No over-engineering or scope creep
- [ ] Appropriate complexity level

**Code Quality**:

- [ ] Follows project patterns in `src/`
- [ ] Proper error handling with Result types or try/catch
- [ ] Tests cover stated functionality
- [ ] ESM imports used consistently

**Structural Health**:

- [ ] No function exceeds cyclomatic complexity 12 (`complexity`) or cognitive complexity 15 (`sonarjs/cognitive-complexity`)
- [ ] No copy-paste duplication across modules
- [ ] Barrel exports used sparingly and intentionally

## Output Standards

**Simple Tasks**: CRITICAL issues only, clear approval when requirements met
**Complex Tasks**: CRITICAL/WARNINGS/SUGGESTIONS with specific fixes
**All reviews**: Concise, streamlined, no unnecessary complexity analysis
