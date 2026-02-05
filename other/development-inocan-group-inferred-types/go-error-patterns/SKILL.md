---
name: Go Error Patterns
description: This skill should be used when the user asks about "err113", "wrapcheck", "errorlint", "sentinel errors", "error wrapping", "errors.Is", "errors.As", "dynamic errors", or needs guidance on idiomatic Go error handling. Provides patterns for fixing error-related lint violations.
---

# Go Error Patterns

Idiomatic Go error handling patterns for lint compliance and maintainability.

## Overview

Three linters enforce Go error hygiene:

| Linter | Detects | Solution |
|--------|---------|----------|
| **err113** | `errors.New()` in return statements | Extract to sentinel errors |
| **wrapcheck** | Unwrapped errors from external packages | Wrap with `fmt.Errorf("ctx: %w", err)` |
| **errorlint** | `err == ErrFoo` comparisons | Use `errors.Is(err, ErrFoo)` |

## Pattern 1: Sentinel Errors (err113)

Dynamic errors prevent callers from checking error types. Extract to package-level sentinels.

### Problem

```go
func Validate(s string) error {
    if s == "" {
        return errors.New("input is empty")  // err113: dynamic error
    }
    if len(s) > 100 {
        return errors.New("input too long")  // err113: dynamic error
    }
    return nil
}
```

### Solution

```go
var (
    ErrEmptyInput = errors.New("input is empty")
    ErrInputTooLong = errors.New("input too long")
)

func Validate(s string) error {
    if s == "" {
        return ErrEmptyInput
    }
    if len(s) > 100 {
        return ErrInputTooLong
    }
    return nil
}
```

### Naming Conventions

- **Exported sentinels:** `ErrFoo` for errors callers should check
- **Unexported sentinels:** `errFoo` for internal errors
- **Semantic names:** `ErrNotFound`, not `ErrError1`

### When to Use Dynamic Errors

Dynamic errors are acceptable when:
- The message is unique and caller won't check type
- Used with `fmt.Errorf` wrapping: `fmt.Errorf("failed at %s: %w", loc, err)`

Add `//nolint:err113` with justification for intentional dynamic errors.

## Pattern 2: Error Wrapping (wrapcheck)

External package errors must be wrapped to provide context for debugging.

### Problem

```go
func LoadUser(id string) (*User, error) {
    row := db.QueryRow("SELECT * FROM users WHERE id = ?", id)
    var u User
    if err := row.Scan(&u.ID, &u.Name); err != nil {
        return nil, err  // wrapcheck: sql error not wrapped
    }
    return &u, nil
}
```

### Solution

```go
func LoadUser(id string) (*User, error) {
    row := db.QueryRow("SELECT * FROM users WHERE id = ?", id)
    var u User
    if err := row.Scan(&u.ID, &u.Name); err != nil {
        return nil, fmt.Errorf("load user %s: %w", id, err)
    }
    return &u, nil
}
```

### Wrapping Guidelines

1. **Context:** Include what operation failed
2. **Parameters:** Include relevant IDs/paths (sanitized)
3. **Verb form:** Use present participle: "loading", "parsing", "connecting"
4. **No duplication:** Don't repeat what lower layers already say

**Good:**
```go
return fmt.Errorf("parse config file: %w", err)
```

**Bad:**
```go
return fmt.Errorf("error: %w", err)  // Redundant "error"
return fmt.Errorf("parse config file: parse config file: %w", err)  // Duplicated
```

### When NOT to Wrap

- **Same package errors:** Already have context
- **Sentinel returns:** `return ErrNotFound` is already descriptive
- **Error transformation:** When converting to a different error type

## Pattern 3: Error Comparison (errorlint)

Direct comparison breaks with wrapped errors. Use `errors.Is()` and `errors.As()`.

### Problem

```go
if err == sql.ErrNoRows {  // errorlint: won't match wrapped error
    return nil, ErrNotFound
}
```

### Solution

```go
if errors.Is(err, sql.ErrNoRows) {
    return nil, ErrNotFound
}
```

### errors.Is vs errors.As

```go
// errors.Is: Check if error chain contains specific error
if errors.Is(err, os.ErrNotExist) {
    // Handle missing file
}

// errors.As: Extract specific error type from chain
var pathErr *os.PathError
if errors.As(err, &pathErr) {
    fmt.Printf("failed path: %s\n", pathErr.Path)
}
```

### Type Assertion Migration

**Before:**
```go
if e, ok := err.(*os.PathError); ok {
    // ...
}
```

**After:**
```go
var e *os.PathError
if errors.As(err, &e) {
    // ...
}
```

## Quick Reference

| Violation | Pattern | Fix |
|-----------|---------|-----|
| `errors.New("msg")` in return | err113 | Extract to `var ErrFoo = errors.New("msg")` |
| `return externalPkg.Func()` error | wrapcheck | `fmt.Errorf("ctx: %w", err)` |
| `err == ErrFoo` | errorlint | `errors.Is(err, ErrFoo)` |
| `err.(*Type)` | errorlint | `errors.As(err, &target)` |

## Verification

After fixes:

```bash
golangci-lint run --enable err113,wrapcheck,errorlint ./...
go test ./...
```
