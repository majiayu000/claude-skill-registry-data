---
name: golang-expert
description: |
  Expert Go/Golang development guidance enforcing best practices, functional programming principles,
  KISS, DRY, and idiomatic patterns. Use when: (1) Writing new Go code, (2) Reviewing Go code for
  quality issues, (3) Refactoring Go code, (4) Designing Go architecture with interfaces and DI,
  (5) Writing or improving Go tests, (6) Debugging concurrency or performance issues,
  (7) User asks about Go best practices or patterns.
---

# Golang Expert

Expert guidance for writing clean, idiomatic, maintainable Go code.

## Table of Contents

1. [Core Principles](#core-principles)
2. [Quick Reference](#quick-reference)
3. [Detailed Guides](#detailed-guides)

## Core Principles

### The Go Philosophy

1. **Simplicity over cleverness** - Readable beats clever
2. **Explicit over implicit** - No magic, clear data flow
3. **Composition over inheritance** - Small interfaces, embed structs
4. **Errors are values** - Handle them, don't ignore them

### KISS - Keep It Simple

```go
// BAD - over-engineered
type ProcessorFactory interface {
    CreateProcessor(config Config) Processor
}

// GOOD - direct and simple
func Process(data []byte) (Result, error) {
    // Direct implementation
}
```

### DRY - Don't Repeat Yourself

```go
// BAD - duplicated logic
func ParseUserDate(s string) time.Time { /*...*/ }
func ParseOrderDate(s string) time.Time { /*...*/ } // Same code!

// GOOD - single source of truth
func ParseDate(s string) (time.Time, error) {
    return time.Parse(time.RFC3339, s)
}
```

### Functional Principles

1. **No global mutable state** - Use dependency injection
2. **Immutability** - Return new values, don't mutate inputs
3. **Pure functions** - Same input = same output, no side effects
4. **Constants over variables** - Use `const` when possible

```go
// BAD - global state
var logger *Logger
func SetLogger(l *Logger) { logger = l }

// GOOD - dependency injection
type Service struct {
    logger Logger
}
func NewService(logger Logger) *Service {
    return &Service{logger: logger}
}
```

## Quick Reference

### Interface Design

```go
// Small, focused interfaces (Interface Segregation)
type Reader interface { Read(p []byte) (n int, err error) }
type Writer interface { Write(p []byte) (n int, err error) }

// Compose when needed
type ReadWriter interface {
    Reader
    Writer
}

// Accept interfaces, return structs
func Process(r Reader) *Result { /*...*/ }
```

### Error Handling

```go
// Wrap errors with context
if err != nil {
    return fmt.Errorf("process user %d: %w", id, err)
}

// Sentinel errors for expected conditions
var ErrNotFound = errors.New("not found")

// Check with errors.Is/As
if errors.Is(err, ErrNotFound) { /*...*/ }
```

### Table-Driven Tests

```go
func TestParse(t *testing.T) {
    tests := []struct {
        name    string
        input   string
        want    Result
        wantErr bool
    }{
        {"valid input", "abc", Result{Value: "abc"}, false},
        {"empty input", "", Result{}, true},
    }
    for _, tt := range tests {
        t.Run(tt.name, func(t *testing.T) {
            got, err := Parse(tt.input)
            if (err != nil) != tt.wantErr {
                t.Errorf("Parse() error = %v, wantErr %v", err, tt.wantErr)
                return
            }
            if got != tt.want {
                t.Errorf("Parse() = %v, want %v", got, tt.want)
            }
        })
    }
}
```

### Concurrency

```go
// Always use context for cancellation
func Process(ctx context.Context) error {
    select {
    case <-ctx.Done():
        return ctx.Err()
    case result := <-work():
        return handle(result)
    }
}

// Use errgroup for parallel work
g, ctx := errgroup.WithContext(ctx)
for _, item := range items {
    item := item // capture loop variable
    g.Go(func() error { return process(ctx, item) })
}
return g.Wait()
```

## Detailed Guides

Load these references as needed:

| Topic | File | When to Use |
|-------|------|-------------|
| Functional Patterns | [functional-patterns.md](references/functional-patterns.md) | DI, immutability, pure functions |
| KISS & DRY | [kiss-dry.md](references/kiss-dry.md) | Simplification, code deduplication |
| Interface Design | [interface-design.md](references/interface-design.md) | API design, interface segregation |
| Testing | [testing.md](references/testing.md) | Tests, mocks, benchmarks |
| Error Handling | [error-handling.md](references/error-handling.md) | Error patterns, wrapping, types |
| Concurrency | [concurrency.md](references/concurrency.md) | Goroutines, channels, sync |
| Performance | [performance.md](references/performance.md) | Profiling, optimization |
| Code Review | [code-review-checklist.md](references/code-review-checklist.md) | Review checklist |

## Code Review Workflow

When reviewing Go code:

1. **Read** [code-review-checklist.md](references/code-review-checklist.md)
2. **Check** for KISS/DRY violations
3. **Verify** error handling is complete
4. **Assess** interface design
5. **Review** test coverage and quality
6. **Flag** concurrency issues
7. **Identify** performance concerns

## Refactoring Workflow

When refactoring:

1. **Ensure tests exist** before changes
2. **Apply KISS** - Remove unnecessary abstractions
3. **Apply DRY** - Extract duplicated code
4. **Improve interfaces** - Make them smaller
5. **Add DI** - Remove global state
6. **Run tests** after each change
