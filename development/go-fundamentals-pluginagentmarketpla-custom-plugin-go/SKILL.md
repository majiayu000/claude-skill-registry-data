---
name: go-fundamentals
description: Core Go programming concepts - syntax, types, interfaces, error handling
sasmp_version: "1.3.0"
bonded_agent: 01-go-fundamentals
bond_type: PRIMARY_BOND
---

# Go Fundamentals Skill

Master core Go programming concepts for production-ready applications.

## Overview

Comprehensive skill covering Go syntax, type system, interfaces, and idiomatic error handling patterns following Effective Go and Google Go Style Guide.

## Parameters

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| topic | string | yes | - | Topic to learn: "types", "interfaces", "errors", "packages" |
| level | string | no | "intermediate" | Skill level: "beginner", "intermediate", "advanced" |
| include_examples | bool | no | true | Include code examples |

## Validation Rules

```go
func ValidateRequest(req SkillRequest) error {
    validTopics := []string{"types", "interfaces", "errors", "packages", "structs"}
    if !slices.Contains(validTopics, req.Topic) {
        return fmt.Errorf("invalid topic %q: must be one of %v", req.Topic, validTopics)
    }
    return nil
}
```

## Core Topics

### Types & Structs
```go
type User struct {
    ID        int64     `json:"id" db:"id"`
    Name      string    `json:"name" db:"name"`
    Email     string    `json:"email" db:"email"`
    CreatedAt time.Time `json:"created_at" db:"created_at"`
}

func (u *User) Validate() error {
    if u.Name == "" {
        return errors.New("name is required")
    }
    if !strings.Contains(u.Email, "@") {
        return errors.New("invalid email format")
    }
    return nil
}
```

### Interface Design
```go
// Small, focused interfaces
type Reader interface {
    Read(p []byte) (n int, err error)
}

type Writer interface {
    Write(p []byte) (n int, err error)
}

// Composition over inheritance
type ReadWriter interface {
    Reader
    Writer
}
```

### Error Handling
```go
// Sentinel errors
var (
    ErrNotFound     = errors.New("not found")
    ErrUnauthorized = errors.New("unauthorized")
)

// Error wrapping with context
func GetUser(id int64) (*User, error) {
    user, err := db.FindByID(id)
    if err != nil {
        if errors.Is(err, sql.ErrNoRows) {
            return nil, ErrNotFound
        }
        return nil, fmt.Errorf("get user %d: %w", id, err)
    }
    return user, nil
}

// Custom error types
type ValidationError struct {
    Field   string
    Message string
}

func (e *ValidationError) Error() string {
    return fmt.Sprintf("%s: %s", e.Field, e.Message)
}
```

## Retry Logic

```go
func withRetry[T any](fn func() (T, error), maxRetries int) (T, error) {
    var zero T
    backoff := 100 * time.Millisecond

    for i := 0; i < maxRetries; i++ {
        result, err := fn()
        if err == nil {
            return result, nil
        }
        if i < maxRetries-1 {
            time.Sleep(backoff)
            backoff *= 2
        }
    }
    return zero, fmt.Errorf("max retries exceeded")
}
```

## Logging & Observability

```go
import "log/slog"

func ProcessRequest(ctx context.Context, req Request) error {
    logger := slog.With(
        "request_id", ctx.Value("request_id"),
        "user_id", req.UserID,
    )

    logger.Info("processing request", "action", req.Action)

    if err := validate(req); err != nil {
        logger.Error("validation failed", "error", err)
        return err
    }

    logger.Info("request processed successfully")
    return nil
}
```

## Unit Test Template

```go
func TestUser_Validate(t *testing.T) {
    tests := []struct {
        name    string
        user    User
        wantErr bool
    }{
        {
            name:    "valid user",
            user:    User{Name: "John", Email: "john@example.com"},
            wantErr: false,
        },
        {
            name:    "empty name",
            user:    User{Name: "", Email: "john@example.com"},
            wantErr: true,
        },
        {
            name:    "invalid email",
            user:    User{Name: "John", Email: "invalid"},
            wantErr: true,
        },
    }

    for _, tt := range tests {
        t.Run(tt.name, func(t *testing.T) {
            err := tt.user.Validate()
            if (err != nil) != tt.wantErr {
                t.Errorf("Validate() error = %v, wantErr %v", err, tt.wantErr)
            }
        })
    }
}
```

## Troubleshooting

### Failure Modes
| Symptom | Cause | Fix |
|---------|-------|-----|
| `nil pointer dereference` | Uninitialized pointer | Check nil before use |
| `interface conversion panic` | Wrong type assertion | Use comma-ok idiom |
| `import cycle` | Circular dependencies | Extract to new package |

### Debug Checklist
1. Run `go vet ./...` for static analysis
2. Run `go build ./...` for compilation check
3. Check error handling covers all paths

## Usage

```
Skill("go-fundamentals")
```
