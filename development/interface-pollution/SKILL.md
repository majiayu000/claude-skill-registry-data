---
name: interface-pollution
description: Detect and avoid unnecessary interface abstractions
---

# Interface Pollution Detection

Interface pollution occurs when interfaces are created before they're needed. Define interfaces at consumption point, not production.

## Pollution Patterns

**WRONG** - Producer defines interface prematurely
```go
// In package "storage"
type UserRepository interface {
    GetUser(id int) (*User, error)
    SaveUser(u *User) error
}

type PostgresRepo struct{}

func (p *PostgresRepo) GetUser(id int) (*User, error) { ... }
func (p *PostgresRepo) SaveUser(u *User) error { ... }
```

**CORRECT** - Consumer defines minimal interface
```go
// In package "handler"
type UserGetter interface {
    GetUser(id int) (*User, error)
}

func HandleRequest(repo UserGetter) http.Handler {
    // Only needs GetUser, not entire repository
    return http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
        user, _ := repo.GetUser(123)
        // ...
    })
}

// Concrete type lives in storage package
// Handler depends on small interface, not full implementation
```

## Detection Checklist

**You have interface pollution if:**
- [ ] Interface defined in same package as implementation
- [ ] Only one implementation exists
- [ ] Interface has >5 methods
- [ ] Name ends in "Interface" or "Impl"

## Refactoring Strategy

**Before:**
```go
type DataService interface {
    Read() error
    Write() error
    Validate() error
    Transform() error
}
```

**After:**
```go
// Split by actual usage
type Reader interface { Read() error }
type Writer interface { Write() error }

// Compose where needed
type ReadWriter interface {
    Reader
    Writer
}
```
