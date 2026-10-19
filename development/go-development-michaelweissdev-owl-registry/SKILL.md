---
name: go-development
description: >
  Develop, test, and maintain idiomatic Go applications following official Go
  conventions. Use when writing Go packages and modules, implementing explicit
  error handling with wrapping, designing small consumer-owned interfaces, managing
  concurrency with goroutines, channels, and context.Context, or running golangci-lint.
compatibility: >
  Agent Skills-compatible coding agents operating on Go 1.20+ codebases
  with the Go toolchain.
metadata:
  author: michaelweissdev
  version: "1.0.0"
  tags: "go, golang, concurrency, interfaces, goroutines, context, testing"
  topics: "programming-languages, software-development"
---

# Idiomatic Go Development

Go emphasizes simplicity, readability, explicit error handling, and lightweight concurrency. Idiomatic Go code adheres to the official [Effective Go](https://go.dev/doc/effective_go) guide, avoids over-engineering, defines small consumer-driven interfaces, and propagates context throughout all I/O boundaries.

## Core Rules

1. **Errors are values, not exceptions**: Always check errors explicitly (`if err != nil`). Never ignore returned errors with `_` unless explicitly intended and documented.
2. **Accept interfaces, return structs**: Functions should accept the smallest interface required to do their work, and return concrete struct pointers or values.
3. **Consumers define interfaces**: Define interfaces in the package where they are consumed, not where the implementing struct is declared.
4. **Pass `context.Context` as the first parameter**: Every function performing network, database, or long-running operations must accept `ctx context.Context` as its first argument and respect cancellation.
5. **Never leak goroutines**: Every spawned goroutine must have a deterministic termination condition or cancellation path via `ctx.Done()`.
6. **Zero value must be useful**: Design structs such that their default uninitialized state is ready for use (e.g. `sync.Mutex`, `bytes.Buffer`).

---

## 1. Project and Package Structure

Standard Go repository layout:

```text
my-service/
├── go.mod
├── go.sum
├── cmd/
│   └── server/
│       └── main.go       # Entry point for the executable
├── internal/             # Code private to this module (cannot be imported by external repos)
│   ├── auth/
│   │   ├── auth.go
│   │   └── auth_test.go
│   └── storage/
│       └── store.go
└── pkg/                  # Public library code safe for external consumption
    └── client/
        └── client.go
```

---

## 2. Explicit Error Handling and Wrapping

Wrap errors with context using `%w` and inspect them using `errors.Is` and `errors.As`:

```go
package store

import (
	"database/sql"
	"errors"
	"fmt"
)

var ErrUserNotFound = errors.New("user not found")

type Store struct {
	db *sql.DB
}

func (s *Store) GetUserEmail(id int64) (string, error) {
	var email string
	query := "SELECT email FROM users WHERE id = $1"
	err := s.db.QueryRow(query, id).Scan(&email)
	if err != nil {
		if errors.Is(err, sql.ErrNoRows) {
			return "", fmt.Errorf("lookup user %d: %w", id, ErrUserNotFound)
		}
		return "", fmt.Errorf("query user %d: %w", id, err)
	}
	return email, nil
}
```

Caller inspection:
```go
email, err := s.GetUserEmail(42)
if err != nil {
	if errors.Is(err, store.ErrUserNotFound) {
		// Handle 404
	} else {
		// Handle 500 internal server error
	}
}
```

---

## 3. Concurrency with Goroutines, Channels, and Context

Always bind worker lifecycles to `context.Context` to prevent goroutine leaks:

```go
package worker

import (
	"context"
	"time"
)

func RunPeriodicSync(ctx context.Context, interval time.Duration) error {
	ticker := time.NewTicker(interval)
	defer ticker.Stop()

	for {
		select {
		case <-ctx.Done():
			// Context was canceled or timed out; clean up and return
			return ctx.Err()
		case t := <-ticker.C:
			if err := performSync(ctx, t); err != nil {
				// Log error and continue, or abort if fatal
			}
		}
	}
}
```

---

## 4. Consumer-Defined Interfaces

Do not create an interface in package `database` with 30 methods. Let callers declare what they need:

```go
package service

import "context"

// The service only requires these two methods, regardless of database backend
type UserRepository interface {
	FindUser(ctx context.Context, id string) (*User, error)
	SaveUser(ctx context.Context, user *User) error
}

type UserService struct {
	repo UserRepository
}

func NewUserService(repo UserRepository) *UserService {
	return &UserService{repo: repo}
}
```

---

## 5. Common Mistakes and Anti-Patterns

| Anti-Pattern | Bug / Risk | Correct Practice |
| :--- | :--- | :--- |
| `go func() { ... }()` without exit signal | Goroutine leak; leaks memory and CPU indefinitely | Pass `ctx` and listen to `<-ctx.Done()` |
| Ignoring returned errors: `res, _ := fetch()` | Silent failures in production | Always handle error: `if err != nil { return err }` |
| Exporting concrete types with public interfaces | Tight coupling across modules | Return structs; let callers define small interfaces |
| Mutex copy bug: passing `sync.Mutex` by value | Copies lock state, causing deadlocks or race conditions | Always pass structs containing mutexes by pointer (`*MyStruct`) |
| Unbuffered channels causing deadlock | Goroutine hangs waiting for receiver that never arrives | Use appropriate buffering or guarantee concurrent reader |

---

## 6. Verification and Tooling

```bash
# Format code following official standard
gofmt -s -w .

# Run static analysis
go vet ./...
golangci-lint run

# Run tests with race condition detector
go test -race -v -cover ./...

# Verify dependencies in go.mod and go.sum
go mod tidy
git diff --exit-code go.mod go.sum
```

---

## 7. Verification Checklist

- [ ] All public functions, structs, and methods have godoc comments starting with the symbol name.
- [ ] No unhandled errors (`if err != nil`).
- [ ] `go test -race ./...` runs without race condition warnings.
- [ ] Goroutines have clear termination paths via `context.Context`.
- [ ] `go mod tidy` leaves `go.mod` and `go.sum` clean and synchronized.
