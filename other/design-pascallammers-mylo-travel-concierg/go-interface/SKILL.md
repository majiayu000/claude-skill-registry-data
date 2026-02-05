---
name: go-interface
description: Go interface design standards. Use when writing, generating, or reviewing Go interfaces, repository patterns, or service abstractions.
allowed-tools: Read, Grep, Glob, Bash
---

# Go Interface Design Expert

Expert guidance for designing Go interfaces following best practices and idiomatic patterns.

## Core Principles

### 1. Keep Interfaces Small and Focused
Follow the Interface Segregation Principle. Interfaces should define the **minimal behavior** necessary:

```go
// Good - small, focused interfaces
type Reader interface {
    Read(p []byte) (n int, err error)
}

type Writer interface {
    Write(p []byte) (n int, err error)
}

// Bad - monolithic interface
type FileSystem interface {
    Read(p []byte) (n int, err error)
    Write(p []byte) (n int, err error)
    Close() error
    Seek(offset int64, whence int) (int64, error)
    Stat() (os.FileInfo, error)
    // ... 10 more methods
}
```

### 2. Define Interfaces at the Consumer Level
Interfaces belong in the package that **uses** them, not where they're implemented:

```go
// In your service package (consumer)
type UserRepository interface {
    GetByID(ctx context.Context, id string) (*User, error)
}

type UserService struct {
    repo UserRepository  // accepts interface
}
```

This reduces coupling and makes testing easier.

### 3. Accept Interfaces, Return Structs

```go
// Good
func NewService(repo Repository) *Service {
    return &Service{repo: repo}
}

// Avoid
func NewService(repo Repository) ServiceInterface {
    return &Service{repo: repo}
}
```

Accepting interfaces provides flexibility; returning concrete types gives callers full access to the implementation.

### 4. Use Interface Composition
Build complex interfaces from smaller ones:

```go
type Reader interface {
    Read(p []byte) (n int, err error)
}

type Closer interface {
    Close() error
}

// Composed interface
type ReadCloser interface {
    Reader
    Closer
}
```

### 5. Naming Conventions
One-method interfaces use the method name + `-er` suffix:

```go
type Reader interface { Read(p []byte) (n int, err error) }
type Writer interface { Write(p []byte) (n int, err error) }
type Closer interface { Close() error }
type Stringer interface { String() string }
```

### 6. Leverage Implicit Implementation
Go's structural typing means types don't need to declare what they implement:

```go
// No "implements" keyword needed
type FileReader struct{}

func (f *FileReader) Read(p []byte) (n int, err error) {
    // implementation
}
// FileReader automatically satisfies io.Reader
```

### 7. Design for Testing
Interfaces enable easy mocking:

```go
// Production
type DBStore struct { db *sql.DB }

// Test mock
type MockStore struct {
    users map[string]*User
}

// Both satisfy the same interface
type Store interface {
    GetUser(id string) (*User, error)
}
```

### 8. Avoid Empty Interfaces
Use `interface{}` (or `any`) sparingly—it sacrifices type safety:

```go
// Avoid when possible
func Process(data interface{}) {}

// Prefer typed interfaces
func Process(data Processor) {}
```

### 9. Interfaces Should Have No Knowledge of Satisfying Types
Don't add methods that check for specific implementations:

```go
// Bad
type Vehicle interface {
    Speed() int
    IsTruck() bool  // Anti-pattern
}

// Good - use sub-interfaces or type assertions
type Truck interface {
    Vehicle
    LoadCapacity() int
}
```

### 10. Standard Library Alignment
Reuse standard interfaces like `io.Reader`, `io.Writer`, `io.Closer` for maximum interoperability.

## Review Checklist

When reviewing or designing interfaces, verify:

- [ ] Interface has 1-3 methods (prefer smaller)
- [ ] Interface is defined where it's consumed, not implemented
- [ ] Functions accept interfaces, return concrete types
- [ ] Naming follows `-er` convention for single-method interfaces
- [ ] No methods that check for specific implementing types
- [ ] Standard library interfaces used where applicable
- [ ] Interface enables easy testing/mocking

## Anti-Patterns to Avoid

1. **Premature abstraction** - Don't create interfaces until you need them
2. **God interfaces** - Interfaces with 5+ methods are a code smell
3. **Interface pollution** - Not every type needs an interface
4. **Marker interfaces** - Zero-method interfaces are discouraged in Go
5. **Implementation leakage** - Interfaces shouldn't expose implementation details

## References

- [Go Interfaces: Five Best-Practices](https://victorpierre.dev/blog/five-go-interfaces-best-practices/)
- [Best Practices for Interfaces in Go | Boot.dev](https://blog.boot.dev/golang/golang-interfaces/)
- [Interface Composition and Best Practices | Leapcell](https://leapcell.io/blog/interface-composition-and-best-practices-in-go)
- [Effective Go](https://go.dev/doc/effective_go)
