---
name: go-patterns
description: 'Use when structuring Go packages or service layers, handling wrapped errors, or managing goroutines and context cancellation. Guides idiomatic Go package layout.'
---

# Go Development Patterns

Idiomatic Go patterns and best practices for building robust, efficient, and maintainable applications.

## When to Activate

- Writing new Go code
- Reviewing Go code
- Refactoring existing Go code
- Designing Go packages/modules

## Critical Rules

- Make the zero value useful.
- Accept interfaces, return structs; define interfaces where they are used.
- Wrap errors with context using `%w`; check with `errors.Is` / `errors.As`.
- Never silently ignore errors; handle them or document why ignoring is safe.
- Pass `context.Context` as the first parameter, never in a struct.
- Avoid goroutine leaks: handle cancellation (`ctx.Done()`) so goroutines never block forever.
- Inject dependencies instead of using package-level state.
- Format with `gofmt` / `goimports`.

## References

Paths are relative to this SKILL.md's directory. Read only the file that matches the task. If a file cannot be read, say so.

- [references/errors-and-concurrency.md](references/errors-and-concurrency.md)
  Read when: Core Principles (simplicity, zero value, accept interfaces/return structs), Error Handling Patterns (wrapping, custom errors, errors.Is/As, never ignore errors), Concurrency Patterns (worker pool, context, graceful shutdown, errgroup, goroutine leaks).

- [references/design-and-tooling.md](references/design-and-tooling.md)
  Read when: Interface Design, Package Organization, Struct Design (functional options, embedding), Memory and Performance, Go Tooling Integration (commands, linter config).

## Quick Reference: Go Idioms

| Idiom                                               | Description                                              |
| --------------------------------------------------- | -------------------------------------------------------- |
| Accept interfaces, return structs                   | Functions accept interface params, return concrete types |
| Errors are values                                   | Treat errors as first-class values, not exceptions       |
| Don't communicate by sharing memory                 | Use channels for coordination between goroutines         |
| Make the zero value useful                          | Types should work without explicit initialization        |
| A little copying is better than a little dependency | Avoid unnecessary external dependencies                  |
| Clear is better than clever                         | Prioritize readability over cleverness                   |
| gofmt is no one's favorite but everyone's friend    | Always format with gofmt/goimports                       |
| Return early                                        | Handle errors first, keep happy path unindented          |

## Anti-Patterns to Avoid

```go
// Bad: Naked returns in long functions
func process() (result int, err error) {
    // ... 50 lines ...
    return // What is being returned?
}

// Bad: Using panic for control flow
func GetUser(id string) *User {
    user, err := db.Find(id)
    if err != nil {
        panic(err) // Don't do this
    }
    return user
}

// Bad: Passing context in struct
type Request struct {
    ctx context.Context // Context should be first param
    ID  string
}

// Good: Context as first parameter
func ProcessRequest(ctx context.Context, id string) error {
    // ...
}

// Bad: Mixing value and pointer receivers
type Counter struct{ n int }
func (c Counter) Value() int { return c.n }    // Value receiver
func (c *Counter) Increment() { c.n++ }        // Pointer receiver
// Pick one style and be consistent
```

**Remember**: Go code should be boring in the best way - predictable, consistent, and easy to understand. When in doubt, keep it simple.
