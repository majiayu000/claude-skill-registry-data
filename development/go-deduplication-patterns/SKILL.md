---
name: Go Deduplication Patterns
description: This skill should be used when the user asks about "code duplication", "jscpd", "DRY principle", "duplicate code", "clone detection", "code consolidation", or needs guidance on when and how to consolidate duplicate Go code.
---

# Go Deduplication Patterns

Strategies for identifying and consolidating duplicate code in Go codebases.

## Overview

jscpd detects copy-pasted code blocks. Not all duplication is bad - the goal is intentional, documented decisions about when to share vs duplicate.

## When to Consolidate

### Consolidate When:
- Same operation with different inputs
- Types share same behavior (interface candidate)
- Changes would need to happen in multiple places
- >20 lines duplicated
- Code is complex enough that bugs could diverge

### Keep Duplicated When:
- Different domains that will evolve independently
- <10 lines of simple code
- Test fixtures (duplication aids readability)
- Consolidation would create artificial coupling
- Code is likely to diverge in the future

## Pattern 1: Extract Helper Function

**Use when:** Identical code blocks with different inputs.

### Before

```go
// handlers/user.go
func CreateUser(w http.ResponseWriter, r *http.Request) {
    var req UserRequest
    if err := json.NewDecoder(r.Body).Decode(&req); err != nil {
        http.Error(w, "invalid JSON", http.StatusBadRequest)
        return
    }
    if err := validate(req); err != nil {
        http.Error(w, err.Error(), http.StatusBadRequest)
        return
    }
    // ... user-specific logic
}

// handlers/order.go
func CreateOrder(w http.ResponseWriter, r *http.Request) {
    var req OrderRequest
    if err := json.NewDecoder(r.Body).Decode(&req); err != nil {
        http.Error(w, "invalid JSON", http.StatusBadRequest)
        return
    }
    if err := validate(req); err != nil {
        http.Error(w, err.Error(), http.StatusBadRequest)
        return
    }
    // ... order-specific logic
}
```

### After

```go
// handlers/helpers.go
func decodeAndValidate[T any](r *http.Request, validate func(T) error) (T, error) {
    var req T
    if err := json.NewDecoder(r.Body).Decode(&req); err != nil {
        return req, fmt.Errorf("invalid JSON: %w", err)
    }
    if err := validate(req); err != nil {
        return req, err
    }
    return req, nil
}

// handlers/user.go
func CreateUser(w http.ResponseWriter, r *http.Request) {
    req, err := decodeAndValidate[UserRequest](r, validateUser)
    if err != nil {
        http.Error(w, err.Error(), http.StatusBadRequest)
        return
    }
    // ... user-specific logic
}
```

## Pattern 2: Interface Extraction

**Use when:** Same operations on different types.

### Before

```go
func SaveUser(db *sql.DB, u *User) error {
    query := "INSERT INTO users (name, email) VALUES (?, ?)"
    _, err := db.Exec(query, u.Name, u.Email)
    return err
}

func SaveOrder(db *sql.DB, o *Order) error {
    query := "INSERT INTO orders (product, quantity) VALUES (?, ?)"
    _, err := db.Exec(query, o.Product, o.Quantity)
    return err
}
```

### After

```go
type Saveable interface {
    InsertQuery() string
    InsertArgs() []any
}

func Save(db *sql.DB, item Saveable) error {
    _, err := db.Exec(item.InsertQuery(), item.InsertArgs()...)
    return err
}

func (u *User) InsertQuery() string { return "INSERT INTO users (name, email) VALUES (?, ?)" }
func (u *User) InsertArgs() []any   { return []any{u.Name, u.Email} }
```

## Pattern 3: Generics for Type Safety

**Use when:** Same algorithm, different types, want compile-time safety.

### Before

```go
func FilterUsers(users []User, pred func(User) bool) []User {
    var result []User
    for _, u := range users {
        if pred(u) {
            result = append(result, u)
        }
    }
    return result
}

func FilterOrders(orders []Order, pred func(Order) bool) []Order {
    var result []Order
    for _, o := range orders {
        if pred(o) {
            result = append(result, o)
        }
    }
    return result
}
```

### After

```go
func Filter[T any](items []T, pred func(T) bool) []T {
    var result []T
    for _, item := range items {
        if pred(item) {
            result = append(result, item)
        }
    }
    return result
}
```

## Pattern 4: Functional Options

**Use when:** Similar code with many optional variations.

### Before

```go
// Multiple functions with slight variations
func NewClientWithTimeout(url string, timeout time.Duration) *Client
func NewClientWithRetry(url string, retries int) *Client
func NewClientWithTimeoutAndRetry(url string, timeout time.Duration, retries int) *Client
```

### After

```go
type ClientOption func(*Client)

func WithTimeout(d time.Duration) ClientOption {
    return func(c *Client) { c.timeout = d }
}

func WithRetry(n int) ClientOption {
    return func(c *Client) { c.retries = n }
}

func NewClient(url string, opts ...ClientOption) *Client {
    c := &Client{url: url, timeout: 30 * time.Second}
    for _, opt := range opts {
        opt(c)
    }
    return c
}
```

## Pattern 5: Documented Duplication

**Use when:** Consolidation would be worse than duplication.

```go
// NOTE: This validation logic is intentionally duplicated from orders/validate.go
// User validation and order validation share structure now but will diverge
// as we add user-specific rules (e.g., email format, age verification).
// See ADR-015 for discussion.
func validateUser(u *User) error {
    if u.Name == "" {
        return errors.New("name required")
    }
    // ...
}
```

## Placement Guidelines

| Duplication Scope | Placement |
|------------------|-----------|
| Within same package | unexported helper in same file |
| Across sibling packages | shared parent package |
| Across domains | `internal/common/` or domain-specific `internal/shared/` |
| Across repositories | Consider shared module |

## Metrics

| Metric | Good | Warning |
|--------|------|---------|
| Clone count | <5 | >15 |
| Clone % | <2% | >5% |
| Largest clone | <30 lines | >50 lines |

## Verification

After consolidation:

```bash
# Tests must pass
go test ./...

# Duplication reduced
jscpd --format go ./...

# No new lint issues
golangci-lint run ./...
```
