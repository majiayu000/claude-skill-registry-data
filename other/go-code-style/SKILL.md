---
name: go-code-style
description: "Golang code style, formatting, and conventions. Focuses on clarity, readability, and idiomatic Go patterns."
metadata:
  model: models/gemini-3.1-pro-preview
  last_modified: Wed, 06 May 2026 04:45:00 GMT
---

## Core Style Principles

1. **Keep the happy path left** — Handle errors and edge cases first with early returns. Avoid deep nesting.
2. **Short and focused functions** — One function should do one thing. Aim for ≤4 parameters.
3. **:= vs var** — Use `:=` for non-zero initialization, `var` for zero-value initialization (signals "this will be set later").
4. **Initialize slices and maps** — Use `[]T{}` or `make([]T, 0)` instead of leaving them nil to avoid JSON serialization surprises (`null` vs `[]`).
5. **Named Booleans** — If a condition has 3+ operands, extract them into named variables for clarity.
6. **Eliminate unnecessary else** — If the `if` block returns, the `else` is redundant.
7. **Use `range`** — Prefer `for i, v := range slice` over index-based loops.
8. **Explicit field names** — Always use field names in composite literals (`User{Name: "Alice"}` not `User{"Alice"}`).

## Code Examples

### Happy Path Indentation
```go
// ✅ Good
func process(data []byte) error {
    if len(data) == 0 {
        return ErrEmptyData
    }
    
    res, err := parse(data)
    if err != nil {
        return err
    }
    
    return save(res)
}

// ❌ Bad (Deeply nested)
func process(data []byte) error {
    if len(data) > 0 {
        res, err := parse(data)
        if err == nil {
            return save(res)
        } else {
            return err
        }
    }
    return ErrEmptyData
}
```

### Slice and Map Initialization
```go
// ✅ Good
users := []User{} // serializes to []
m := make(map[string]int, len(items))

// ❌ Bad (unless nil is specifically intended)
var users []User // serializes to null
```

## Function Signatures

- Context first: `func Do(ctx context.Context, arg string)`.
- Error last: `func Do(...) (Result, error)`.
- Use pointer receivers (`*T`) when mutating or for large structs.
- Use value receivers (`T`) for small, immutable types.

## Formatting
- Use `gofmt` (or `gofumpt`) religiously.
- Break lines at semantic boundaries if they exceed ~120 chars.

## Anti-patterns

- ❌ **Magic numbers**: Use named constants instead.
- ❌ **Positional struct literals**: `User{"Bob", 20}` (breaks if fields are added).
- ❌ **Pointless `else`**: `if err != nil { return err } else { ... }`.
- ❌ **Naked returns** in long functions: `return` (hard to see what is returned).
- ❌ **Dot imports**: `import . "fmt"`.
