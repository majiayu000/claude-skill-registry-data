---
name: go-sentinel-errors
description: Define package-level sentinel errors using errors.New
---

# Sentinel Errors

## Pattern
Define package-level errors as exported variables for expected error conditions.

## CORRECT
```go
package user

import "errors"

// Sentinel errors - define at package level
var (
    ErrNotFound      = errors.New("user not found")
    ErrInvalidEmail  = errors.New("invalid email format")
    ErrDuplicate     = errors.New("user already exists")
)

func Get(id int) (*User, error) {
    u, ok := db[id]
    if !ok {
        return nil, ErrNotFound
    }
    return u, nil
}
```

## WRONG
```go
// Bad: Creates new error each time (can't use errors.Is)
func Get(id int) (*User, error) {
    if _, ok := db[id]; !ok {
        return nil, errors.New("user not found")
    }
    return db[id], nil
}

// Bad: String comparison is fragile
if err.Error() == "user not found" { }
```

## Naming Convention
- Prefix with `Err`
- Use camel case: `ErrNotFound`, not `ERR_NOT_FOUND`
- Be specific: `ErrInvalidEmail`, not `ErrBadInput`

## When to Use
Use sentinel errors for:
- Expected business logic errors
- Public API boundaries
- Conditions callers need to handle differently

Avoid for:
- Unexpected/rare conditions
- Internal implementation details
