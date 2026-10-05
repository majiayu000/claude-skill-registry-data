---
name: go
description: |
  Idiomatic programming style, patterns, and conventions for Go (Golang) development.
  Trigger when:
  - Writing, refactoring, reviewing, or debugging Go code.
  - Files matching the pattern **/*.go (including go.mod, go.sum) are in the workspace or referenced.
  - Tasks involve: go fmt, go test, go build, go vet, golangci-lint.
  - Prompt contains keywords: go, golang, goroutine, channel, select, interface, err != nil, defer, panic, gofmt, struct.
---

# Go Language Idioms

Go favors simplicity, readability, and explicit behavior. Work with the language's conventions, not against them.

---

## Core Philosophy

- **Simplicity over cleverness** — clear, boring code is better than clever, obscure code
- **Explicit over implicit** — errors are values, not exceptions
- **Composition over inheritance** — embed types, implement interfaces
- **Share by communicating** — don't communicate by sharing memory

---

## Formatting

Let `gofmt` handle it. Don't fight the formatter.

```bash
gofmt -w .        # Format all files
go fmt ./...      # Format package
```

All Go code in the ecosystem follows `gofmt`. There is no debate.

---

## Naming

### General Rules

| Scope      | Style                  | Example                                       |
| :--------- | :--------------------- | :-------------------------------------------- |
| Exported   | `PascalCase`           | `ReadFile`, `HTTPClient`                      |
| Unexported | `camelCase`            | `readFile`, `httpClient`                      |
| Packages   | lowercase, single word | `bytes`, `http`, `bufio`                      |
| Acronyms   | All caps               | `HTTP`, `URL`, `ID` (not `Http`, `Url`, `Id`) |

### Package Names

- Short, concise, evocative
- No underscores or mixedCaps
- The package name is part of the type name: `bufio.Reader`, not `bufio.BufReader`

### Getters and Setters

```go
// ❌ Don't prefix getters with "Get"
func (u *User) GetName() string

// ✅ Just use the field name
func (u *User) Name() string

// ✅ Setters use "Set" prefix
func (u *User) SetName(name string)
```

### Interface Names

One-method interfaces use method name + `-er` suffix:

| Method   | Interface  |
| :------- | :--------- |
| `Read`   | `Reader`   |
| `Write`  | `Writer`   |
| `Close`  | `Closer`   |
| `String` | `Stringer` |

---

## Functions

### Multiple Return Values

Go functions return `(result, error)` instead of throwing:

```go
func ReadFile(path string) ([]byte, error) {
    f, err := os.Open(path)
    if err != nil {
        return nil, err
    }
    defer f.Close()
    return io.ReadAll(f)
}
```

### Named Return Values

Use for documentation, but avoid naked returns in non-trivial functions:

```go
// Named returns document what's being returned
func ParseDuration(s string) (duration time.Duration, err error) {
    // ...
    return duration, nil  // Explicit, not naked
}
```

### Defer

Use `defer` for cleanup. Defers execute LIFO at function exit:

```go
func CopyFile(dst, src string) error {
    r, err := os.Open(src)
    if err != nil {
        return err
    }
    defer r.Close()

    w, err := os.Create(dst)
    if err != nil {
        return err
    }
    defer w.Close()

    _, err = io.Copy(w, r)
    return err
}
```

---

## Interfaces

### Keep Interfaces Small

Accept interfaces, return concrete types:

```go
// ✅ Function accepts interface (flexible)
func Process(r io.Reader) error

// ✅ Function returns concrete type (useful)
func NewClient() *Client
```

### Interface Satisfaction

Interfaces are satisfied implicitly—no `implements` keyword:

```go
type Stringer interface {
    String() string
}

type User struct{ Name string }

// User satisfies Stringer automatically
func (u User) String() string {
    return u.Name
}
```

### Compile-Time Check

Verify interface satisfaction at compile time:

```go
var _ io.Reader = (*MyReader)(nil)
```

---

## Pointers vs. Values

### When to Use Pointer Receivers

| Use Pointer | When                                                 |
| :---------- | :--------------------------------------------------- |
| `*T`        | Method modifies the receiver                         |
| `*T`        | Struct is large (avoid copying)                      |
| `*T`        | Consistency (if any method uses pointer, all should) |

### When to Use Value Receivers

| Use Value | When                              |
| :-------- | :-------------------------------- |
| `T`       | Method doesn't modify receiver    |
| `T`       | Type is small (int, small struct) |
| `T`       | Type is immutable by design       |

---

## Concurrency

### Goroutines

Lightweight, start with `go`:

```go
go func() {
    // runs concurrently
}()
```

### Channels

Use channels for communication between goroutines:

```go
ch := make(chan int)       // Unbuffered
ch := make(chan int, 100)  // Buffered

ch <- value   // Send
v := <-ch     // Receive
```

### Share by Communicating

> "Don't communicate by sharing memory; share memory by communicating."

```go
// ❌ Shared state with mutex
var count int
var mu sync.Mutex

// ✅ Channel-based coordination
type result struct{ value int }
results := make(chan result)
```

### Common Patterns

| Pattern           | Use Case                          |
| :---------------- | :-------------------------------- |
| `sync.WaitGroup`  | Wait for N goroutines to complete |
| `context.Context` | Cancellation and timeouts         |
| `select`          | Multiplex channel operations      |
| `sync.Once`       | One-time initialization           |

---

## Error Handling

### Errors Are Values

Check explicitly. Never discard with `_`:

```go
// ❌ Never ignore errors
result, _ := doSomething()

// ✅ Always check
result, err := doSomething()
if err != nil {
    return fmt.Errorf("doing something: %w", err)
}
```

### Error Wrapping

Use `%w` to wrap errors with context:

```go
if err != nil {
    return fmt.Errorf("failed to parse config %s: %w", path, err)
}
```

### Custom Errors

For libraries, define sentinel errors or custom types:

```go
// Sentinel errors
var ErrNotFound = errors.New("not found")

// Custom error types
type ValidationError struct {
    Field   string
    Message string
}

func (e *ValidationError) Error() string {
    return fmt.Sprintf("%s: %s", e.Field, e.Message)
}
```

### When to Panic

| Context           | Panic?        | Alternative       |
| :---------------- | :------------ | :---------------- |
| Library code      | ❌ Never      | Return `error`    |
| Impossible states | ✅ Acceptable | Assert invariants |
| Init failures     | ✅ Acceptable | `log.Fatal`       |

---

## Anti-Patterns

| Anti-Pattern            | Description                                  | Remedy                                             |
| :---------------------- | :------------------------------------------- | :------------------------------------------------- |
| **Ignoring errors**     | Using `_` to discard errors                  | Always check or explicitly document why ignored    |
| **Naked returns**       | `return` without values in complex functions | Use explicit return values                         |
| **Interface pollution** | Defining interfaces before needed            | Define interfaces at point of use                  |
| **Premature channels**  | Using channels when mutex suffices           | Start simple; add concurrency primitives as needed |
| **Giant interfaces**    | Interfaces with many methods                 | Keep interfaces small; compose when needed         |

---

## Tooling

```bash
go fmt ./...           # Format code
go vet ./...           # Static analysis
golangci-lint run      # Comprehensive linting
go test ./...          # Run tests
go test -race ./...    # Detect race conditions
```

---

## Quick Reference

- **Errors are values** — check explicitly, wrap with context
- **Accept interfaces, return structs** — flexible inputs, concrete outputs
- **Use `gofmt`** — no formatting debates
- **Prefer composition** — embed types, small interfaces
- **Channels for coordination** — share by communicating
- **`defer` for cleanup** — runs at function exit, LIFO
- **No naked returns** — be explicit in non-trivial functions

> These idioms refine but are subordinate to the [Code-Edit Constraints](../../ambient.md#code-edit-constraints).