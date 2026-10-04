---
name: go-structs-interfaces
description: "Golang struct and interface design patterns. Covers composition, embedding, interface segregation, and pointer vs value receivers."
metadata:
  model: models/gemini-3.1-pro-preview
  last_modified: Wed, 06 May 2026 05:30:00 GMT
---

## Core Principles

1. **Small Interfaces** — "The bigger the interface, the weaker the abstraction." Aim for 1-3 methods.
2. **Accept Interfaces, Return Structs** — Functions should accept interfaces for flexibility but return concrete types for clarity.
3. **Define where Consumed** — Interfaces should be defined in the package that uses them, not the package that implements them.
4. **Discover, don't Design** — Don't create an interface until you have at least two implementations or a specific testing need.
5. **Composition over Inheritance** — Use embedding to promote methods and fields from an inner type to an outer type.
6. **Pointer Consistency** — If any method of a type uses a pointer receiver, all methods should use pointer receivers.

## Composition and Embedding

```go
type Reader interface {
    Read(p []byte) (n int, err error)
}

type Writer interface {
    Write(p []byte) (n int, err error)
}

// ReadWriter is composed from two smaller interfaces
type ReadWriter interface {
    Reader
    Writer
}
```

### Struct Embedding
```go
type Logger struct {
    *slog.Logger
}

type Server struct {
    Logger // Embedding Logger promotes its methods to Server
    Addr   string
}

// Usage: s.Info("...") works directly on the Server
```

## Practical Patterns

### Compile-time Interface Check
Ensures that a type actually implements an interface without any runtime cost.
```go
var _ io.Reader = (*MyBuffer)(nil)
```

### Type Switches
Handle different types implementing the same interface.
```go
switch v := i.(type) {
case string:
    fmt.Println(v)
case int:
    fmt.Println(v * 2)
default:
    fmt.Printf("Unknown type: %T\n", v)
}
```

### Optional Behavior with Type Assertions
Check if an interface value supports extra features (e.g., flushing).
```go
if f, ok := w.(http.Flusher); ok {
    f.Flush()
}
```

## Pointer vs Value Receivers

- **Pointer Receiver** (`*T`): Use when the method modifies the receiver, if the struct is large (>128 bytes), or if the struct contains synchronization primitives like `sync.Mutex`.
- **Value Receiver** (`T`): Use for small, immutable types or basic types (int, string).

## Struct Field Tags
Always tag exported fields in structs used for serialization.
```go
type User struct {
    ID    string `json:"id" db:"id"`
    Email string `json:"email" db:"email"`
    Admin bool   `json:"-"` // Exclude from JSON
}
```

## Anti-patterns

- ❌ **Huge interfaces** (5+ methods) — Hard to implement and mock.
- ❌ **Returning interfaces from constructors** — Hides the concrete type's fields.
- ❌ **Defining interfaces in the producer package** — Couples the producer to every consumer.
- ❌ **Bare type assertions** — `i.(string)` can panic. Use `v, ok := i.(string)`.
- ❌ **Mixed receivers** — Mixing pointer and value receivers on the same type causes confusion.
- ❌ **Premature interface creation** — Creating an interface for a single implementation.
