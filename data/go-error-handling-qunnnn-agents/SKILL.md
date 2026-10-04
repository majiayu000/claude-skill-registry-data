---
name: go-error-handling
description: "Idiomatic Golang error handling — creation, wrapping with %w, errors.Is/As, errors.Join, and best practices for structured logging."
metadata:
  model: models/gemini-3.1-pro-preview
  last_modified: Wed, 06 May 2026 04:15:00 GMT
---

## Best Practices

1. **Check every error** — NEVER discard with `_`.
2. **Wrap with context** — Use `fmt.Errorf("context: %w", err)` to add meaning while preserving the error type.
3. **Lowercase messages** — Error strings should be lowercase and not end with punctuation (e.g., `user not found`).
4. **Use `errors.Is` and `errors.As`** — Avoid direct comparison or type assertions.
5. **Log OR Return** — Never do both. Logging then returning leads to duplicate logs and confusion.
6. **Low cardinality** — Keep error strings static; put variable data (IDs, paths) in structured log fields or custom error fields.
7. **Sentinel errors** — Use `var ErrNotFound = errors.New("not found")` for expected conditions.
8. **Custom error types** — Use when you need to carry structured data back to the caller.

## Inspection Patterns

### errors.Is (Sentinel checks)
```go
if errors.Is(err, sql.ErrNoRows) {
    return nil, ErrUserNotFound
}
```

### errors.As (Type checks)
```go
var pathErr *os.PathError
if errors.As(err, &pathErr) {
    fmt.Println("Failed at path:", pathErr.Path)
}
```

### errors.Join (Multiple errors)
```go
err1 := validateName(name)
err2 := validateEmail(email)
if err := errors.Join(err1, err2); err != nil {
    return err
}
```

## Structured Logging (slog)

Prefer `log/slog` for structured logs.

```go
slog.Error("failed to process user",
    "user_id", userID,
    "error", err,
)
```

## Anti-patterns

- ❌ **Swallowing errors** by ignoring the return value.
- ❌ **Log and Return**: `log.Println(err); return err` (results in noisy logs).
- ❌ **Capitalized error messages**: `errors.New("Failed to Save")`.
- ❌ **Direct comparison**: `if err == sql.ErrNoRows` (breaks if error is wrapped).
- ❌ **Using `panic`** for control flow or expected errors.
