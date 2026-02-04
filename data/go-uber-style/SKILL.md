---
name: go-uber-style
description: Use this skill when writing Go code following the Uber Go Style Guide. Provides comprehensive guidance on idiomatic Go patterns, error handling, concurrency safety, performance optimization, and test-driven development. Covers all critical Uber Go rules including channel sizing, goroutine management, interface design, and proper error handling. Appropriate for any task involving .go files, Go code reviews, refactoring, or implementing Go best practices.
---

# Go Uber Style Guide

## Overview

This skill provides comprehensive guidance for writing idiomatic Go code that strictly follows the Uber Go Style Guide. It emphasizes Test-Driven Development (TDD), proper error handling without exceptions, safe concurrency patterns, and Go's unique language idioms including zero values, composition over inheritance, and interface design.

## When to Use This Skill

Use this skill for any Go-related programming task:
- Writing new Go code or implementing new features
- Reviewing existing Go code for best practices and idioms
- Refactoring code to follow Uber Go Style Guide
- Debugging Go applications and fixing issues
- Optimizing Go code for performance
- Implementing concurrent/parallel operations safely
- Designing Go APIs and package structures

## Core Go Philosophy

### Mandatory Principles

**1. Test-Driven Development (TDD)**
- Always write tests first using the Red-Green-Refactor cycle
- Use table-driven tests for comprehensive coverage
- Tests must be in place before implementation code

**2. Explicit Error Handling**
- Go does not use exceptions - use error values exclusively
- Always handle errors explicitly, never ignore them
- Wrap errors with context using `fmt.Errorf` with `%w`
- Use sentinel errors for matching specific error conditions

**3. Single Exit Point Pattern**
- Use the `run()` pattern to centralize exit logic in `main()`
- This keeps `main()` functions clean and testable

**4. Go Idioms**
- Leverage zero values (e.g., `var mu sync.Mutex` is ready to use)
- Accept interfaces, return concrete types
- Use composition over inheritance
- Prefer nil slices over empty slices for "not found" cases

## Workflow

### For Writing New Go Code

1. **Write the test first** (TDD mandatory)
   - Define the function signature and expected behavior in a test
   - Run test to see it fail (Red)

2. **Implement minimal code to pass the test** (Green)
   - Write just enough code to make the test pass
   - Follow Uber Go Style Guide conventions

3. **Refactor while keeping tests green**
   - Improve code quality, readability, and performance
   - Ensure all tests still pass

4. **Verify quality standards**
   - Run `go fmt` to format code
   - Run `go vet` to catch common mistakes
   - Run `go test -race` to detect race conditions
   - Check function size (≤50 lines) and parameter count (≤4)

### For Code Review

1. **Check TDD compliance**
   - Verify tests exist and are comprehensive
   - Ensure table-driven test pattern is used where appropriate

2. **Review Uber Go Style Guide compliance**
   - Check file organization (imports, types, constructors, methods, functions)
   - Verify structural limits (function ≤50 lines, struct ≤200 lines, ≤4 parameters)
   - Confirm proper error handling patterns

3. **Validate interface design**
   - Ensure interfaces are small and focused
   - Check that compile-time interface verification is present
   - Verify "accept interfaces, return concrete types" pattern

4. **Check for Go-specific issues**
   - Look for improper error handling (ignored errors, panics in library code)
   - Verify concurrency safety (proper mutex usage, context handling)
   - Check for proper resource cleanup (defer patterns)

### For Refactoring

1. **Ensure tests exist first**
   - If no tests, write them before refactoring
   - Tests provide safety net during refactoring

2. **Identify anti-patterns**
   - Functions >50 lines
   - >4 parameters (use functional options pattern instead)
   - Ignored errors
   - Missing defer for cleanup
   - Improper interface design

3. **Refactor incrementally**
   - Make one change at a time
   - Keep tests passing after each change
   - Commit working code frequently

## Structural Limits (Uber Go Style Guide)

- **Functions**: ≤50 lines maximum (Go-specific override from general 20-line guideline)
- **Structs**: ≤200 lines maximum
- **Parameters**: ≤4 parameters per function (use functional options pattern for more)
- **Exception Rule**: Break limits only with clear documentation and explicit approval

## Reference Materials

For detailed code patterns, examples, and guidelines, consult the reference files:

- `references/uber-go-patterns.md` - Comprehensive Uber Go Style Guide patterns and anti-patterns
  - Pointers to interfaces, receivers, embedding, mutable globals, init(), field tags
  - Time handling, enums, atomic operations
  - File organization and naming conventions
- `references/error-handling.md` - Error wrapping, sentinel errors, and error matching patterns
- `references/concurrency-safety.md` - Safe concurrent programming patterns in Go
  - **CRITICAL**: Channel sizing (unbuffered or size 1 only)
  - **CRITICAL**: No fire-and-forget goroutines
  - **CRITICAL**: No goroutines in init()
- `references/performance.md` - Performance optimization patterns
  - Prefer strconv over fmt for primitives
  - Avoid repeated string-to-byte conversions
  - Container pre-allocation strategies
- `references/testing-patterns.md` - Table-driven testing examples and TDD workflows

Use grep to search these files for specific patterns when needed:
```bash
grep -r "functional options" references/
grep -r "channel size" references/concurrency-safety.md
grep -r "strconv" references/performance.md
```

## Template Assets

Pre-built templates are available in `assets/templates/` for common Go patterns:

- `assets/templates/main_single_exit.go` - Single exit point pattern for main()
- `assets/templates/table_test.go` - Table-driven test template
- `assets/templates/functional_options.go` - Functional options pattern for >4 parameters
- `assets/templates/http_handler.go` - HTTP handler with proper error handling

Copy and customize these templates as starting points for new code.

## Quality Assurance Checklist

Before delivering Go code, verify:

**Critical Uber Go Rules:**
- [ ] No pointers to interfaces (`*io.Reader` is wrong)
- [ ] Channels are unbuffered or size 1 only
- [ ] No fire-and-forget goroutines (all have stop mechanism)
- [ ] No goroutines in `init()`
- [ ] No embedding types in public structs (unless method promotion is explicit)
- [ ] Field tags on all marshaled struct fields (`json:"field"`)
- [ ] No mutable global variables
- [ ] No shadowing of built-in names (error, string, etc.)
- [ ] Avoid `init()` unless truly necessary

**Code Quality:**
- [ ] Tests written first (TDD followed)
- [ ] Functions ≤50 lines, structs ≤200 lines
- [ ] ≤4 parameters per function (use functional options for more)
- [ ] Code compiles with `go build`
- [ ] Tests pass with `go test -race`
- [ ] Code formatted with `go fmt`
- [ ] No issues from `go vet`
- [ ] Linting clean (`golangci-lint run`)

**Error Handling:**
- [ ] All errors handled explicitly (no `_` discards)
- [ ] Errors wrapped with context (`%w`)
- [ ] Single exit point in main()

**Interfaces:**
- [ ] Interfaces are small and focused
- [ ] Interface compliance verified at compile time (`var _ Interface = (*Type)(nil)`)
- [ ] Accept interfaces, return concrete types
- [ ] Consistent receiver types (all pointer or all value)

**Performance (when relevant):**
- [ ] Use `strconv` for primitive string conversions (not `fmt`)
- [ ] Pre-allocate slices/maps when size is known
- [ ] Avoid repeated string-to-byte conversions in loops

**Time & Enums:**
- [ ] Use `time.Time` for instants, `time.Duration` for periods
- [ ] Enums start at 1 (unless zero is meaningful)

## Communication Guidelines

When providing Go coding assistance:
- Reference Uber Go Style Guide for rationale
- Provide working, tested code examples
- Explain trade-offs in Go context
- Suggest Go tools (`go vet`, `golangci-lint`, `staticcheck`)
- Point out Go-specific pitfalls and solutions
- Prioritize Go's philosophy of simplicity and explicitness

## Key Differences from General Coding Principles

This skill overrides some general coding principles with Go-specific rules:
- **Function length**: 50 lines (vs. general 20 lines) - Go's explicit error handling naturally leads to longer functions
- **Error handling**: No exceptions, only error values - completely different from exception-based languages
- **Testing approach**: TDD is mandatory, not optional - critical to Go development workflow
- **Parameter limits**: Strict ≤4 parameter limit with functional options pattern as solution