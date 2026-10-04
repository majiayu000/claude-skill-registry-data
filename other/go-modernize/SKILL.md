---
name: go-modernize
description: "Guidelines for updating legacy Golang code to use modern features (Go 1.21+). Covers generics, slog, slices/maps packages, and more."
metadata:
  model: models/gemini-3.1-pro-preview
  last_modified: Wed, 06 May 2026 06:10:00 GMT
---

## Modern Go Checklist (1.21 - 1.24)

1. **Use `any`** instead of `interface{}` (Go 1.18+).
2. **Use `min` and `max`** built-in functions (Go 1.21+).
3. **Use `clear`** to empty maps and slices (Go 1.21+).
4. **Use `slices` and `maps`** packages for common operations (Sort, Contains, Clone, Keys) (Go 1.21+).
5. **Migrate to `log/slog`** for structured logging (Go 1.21+).
6. **Use `range` over integers** (e.g., `for i := range 10`) (Go 1.22+).
7. **Use `cmp.Or`** for concise default value assignment (Go 1.22+).
8. **Use `math/rand/v2`** for better performance and API (Go 1.22+).
9. **Use Iterators** (`iter` package) for custom collection traversal (Go 1.23+).
10. **Use `b.Loop()`** for benchmarks (Go 1.24+).
11. **Use `t.Context()`** for test-scoped cancellation (Go 1.24+).

## Modernization Examples

### 1. Slices and Maps (1.21+)
```go
// ✅ Modern
import "slices"
if slices.Contains(mySlice, "value") { ... }

// ❌ Old
for _, v := range mySlice {
    if v == "value" { ... }
}
```

### 2. Min/Max (1.21+)
```go
// ✅ Modern
val := min(a, b, c)

// ❌ Old
val := a
if b < val { val = b }
if c < val { val = c }
```

### 3. Range over Int (1.22+)
```go
// ✅ Modern
for i := range 10 {
    fmt.Println(i)
}

// ❌ Old
for i := 0; i < 10; i++ {
    fmt.Println(i)
}
```

### 4. Structured Logging (1.21+)
```go
// ✅ Modern (stdlib)
slog.Info("user logged in", "user_id", id)

// ❌ Old (third-party or non-structured)
log.Printf("user %d logged in", id)
```

## Deprecated Package Replacements

| Deprecated | Modern Replacement |
| --- | --- |
| `math/rand` | `math/rand/v2` |
| `io/ioutil` | `os` or `io` |
| `reflect.PtrTo` | `reflect.PointerTo` |
| `runtime.SetFinalizer` | `runtime.AddCleanup` (Go 1.24) |

## Strategy for Modernization

1. **Check `go.mod` version**: Ensure the project targets a recent Go version.
2. **Safety First**: Fix patterns that lead to bugs (e.g., loop variable shadowing in pre-1.22).
3. **Readability**: Replace manual loops with `slices`/`maps` functions.
4. **Tooling**: Use `golangci-lint` with the `modernize` linter enabled.
5. **Incremental**: Don't refactor the whole codebase at once; modernize as you touch files for other features.

## Anti-patterns

- ❌ **Mixing old and new styles** — e.g., using `interface{}` in some places and `any` in others.
- ❌ **Ignoring `log/slog`** — Sticking to `log.Printf` in new production services.
- ❌ **Manual `min`/`max` implementations** — Using custom helper functions instead of the built-ins.
- ❌ **Ignoring `go mod tidy`** — Not keeping the toolchain version updated in `go.mod`.
