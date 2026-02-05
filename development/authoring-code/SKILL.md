---
name: authoring-code
description: Code quality standards for writing and reviewing. Use when writing new code, reviewing PRs, refactoring, or making architectural decisions.
---

# Code Authoring

Apply these requirements when writing or reviewing code.

## Architectural Principles

**Simplicity over cleverness.** Write obvious code the next developer understands immediately. Avoid premature abstractions.

Type safety is not cleverness. Use enums over magic strings, strongly-typed IDs where warranted, and proper error types over string parsing.

**Conventions over configuration.** Follow framework conventions and defaults. Do not invent custom patterns when standard ones exist.

**Pragmatism over purity.** Make practical trade-offs. Do not over-engineer for hypothetical requirements.

**YAGNI.** Implement only what is required. Do not add configuration for values that won't change, abstractions for single implementations, error handling for impossible states, defensive code against trusted internal callers, or features not requested.

**Delete freely.** Dead code, unused abstractions, and speculative features are liabilities. Remove them.

**Fewer dependencies.** Each package is maintenance burden. Prefer built-in framework features.

**Explicit over implicit.** Magic is hard to debug. Prefer clear, traceable code paths.

## CLI Tools for Generation

Use framework-provided commands for file generation:

- .NET: `dotnet new`, `dotnet add package`
- Rails: `rails new`, `rails generate`
- Node.js: `npm init`, `npx create-*`
- Python: `pip install`, `poetry init`

## Incremental Development

Implement the minimum required. Do not add error handling for conditions that cannot occur, resilience when infrastructure handles failures, validation for inputs guaranteed by upstream systems, or configurability for values that never change.

Before adding defensive code:
1. Is this a real possibility in this context?
2. What happens without handling? If the job retries automatically, do not add handling.
3. Did the spec explicitly require this?

### Execution Context

| Context | Failure Strategy |
|---------|------------------|
| HTTP endpoints | Handle errors, return appropriate status codes |
| Background jobs | Let exceptions bubble, scheduler retries automatically |
| Idempotent operations | Safe to fail and retry |
| Internal methods | Trust callers, do not re-validate |

For background jobs, assume retry-on-failure unless told otherwise. Do not add try/catch that swallows exceptions.

## Research Requirements

Training data is outdated. Libraries evolve. Verify before implementing.

Before writing code using external packages:

1. Check package versions in project files
2. Use WebSearch to find current documentation for that version
3. Verify async patterns—many libraries now have native async methods
4. Check for breaking changes in major versions

Do not wrap sync methods in `Task.Run()` when native async exists. Do not hand-roll retry logic when libraries like Polly exist and retries are actually needed.

When uncertain about any API:
```
WebSearch: "[package name] [version] async methods"
WebSearch: "[package name] [version] best practices 2025"
```

## Code Review

Before reviewing, identify packages and versions, then research current best practices.

Flag: sync-over-async patterns, deprecated APIs with modern replacements, manual implementations of built-in features.

### Review Checklist

| Principle | Check |
|-----------|-------|
| Current APIs | Modern async methods? No outdated patterns? |
| Simplicity | Obvious? Unnecessary abstractions? |
| Conventions | Following framework patterns? |
| Pragmatism | Over-engineered for hypotheticals? |
| Dead code | Anything unused to delete? |
| Dependencies | Can built-in features replace packages? |

### Issue Priorities

| Priority | Description |
|----------|-------------|
| Critical | Bugs, security issues, data loss risks |
| High | Performance problems, maintainability blockers |
| Medium | Convention violations, missing error handling |
| Low | Style preferences, minor optimizations |

### Review Output

Use `templates/code-review.md` if available. Otherwise structure as:

1. Summary (one paragraph)
2. Issues (grouped by priority)
3. Recommendations (prioritized list)
