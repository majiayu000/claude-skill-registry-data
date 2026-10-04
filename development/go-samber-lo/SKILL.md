---
name: go-samber-lo
description: "Functional programming in Go with samber/lo. Covers slices, maps, channels, and concurrency helpers using generics."
metadata:
  model: models/gemini-3.1-pro-preview
  last_modified: Wed, 06 May 2026 07:05:00 GMT
---

## Core Philosophy

`samber/lo` is a Lodash-inspired library for Go that leverages **Generics** (Go 1.18+) to provide type-safe functional programming helpers. It aims to eliminate boilerplate manual loops for common data transformations.

- **Type-safe**: No reflection or `interface{}`.
- **Immutable**: Most functions return a new collection rather than modifying the input.
- **Composable**: Functions can be easily chained or combined.

## Common Operations

### Slices
| Function | Description |
| --- | --- |
| `lo.Map` | Transforms each element of a slice. |
| `lo.Filter` | Returns elements that satisfy a predicate. |
| `lo.Reduce` | Reduces a slice to a single value. |
| `lo.Uniq` | Returns unique elements. |
| `lo.GroupBy` | Groups elements by a key. |
| `lo.Chunk` | Splits a slice into smaller chunks of a fixed size. |
| `lo.Flatten` | Flattens a slice of slices. |

### Maps
| Function | Description |
| --- | --- |
| `lo.Keys` / `lo.Values` | Returns all keys or values of a map. |
| `lo.PickBy` / `lo.OmitBy` | Filters map entries by predicate. |
| `lo.Invert` | Swaps keys and values. |

### Utilities
| Function | Description |
| --- | --- |
| `lo.ToPtr` | returns a pointer to the value (useful for literals). |
| `lo.FromPtr` | returns the value of a pointer (or default if nil). |
| `lo.Ternary` | Inline ternary operator: `lo.Ternary(cond, a, b)`. |
| `lo.Must` | Panics if the error argument is non-nil. Use with caution. |

## Code Examples

### Map and Filter
```go
names := []string{"alice", "bob", "charlie"}
uppercased := lo.Map(names, func(s string, _ int) string {
    return strings.ToUpper(s)
})
// ["ALICE", "BOB", "CHARLIE"]

shortNames := lo.Filter(names, func(s string, _ int) bool {
    return len(s) <= 5
})
// ["alice", "bob"]
```

### GroupBy
```go
type User struct { Name string; Role string }
users := []User{{Name: "A", Role: "Admin"}, {Name: "B", Role: "User"}}
grouped := lo.GroupBy(users, func(u User) string {
    return u.Role
})
// map[Admin:[{A Admin}] User:[{B User}]]
```

## When to use `lo` vs Stdlib

- **Go 1.21+**: Use the built-in `slices` and `maps` packages for basic operations like `Sort`, `Contains`, `Delete`, `Keys`, and `Values`.
- **Use `lo`** for higher-level transformations like `Map`, `Filter`, `Reduce`, `GroupBy`, `Chunk`, and `Flatten` which are NOT in the standard library.

## Anti-patterns

- ❌ **Ignoring `slices` and `maps` packages** — Don't use `lo.Contains` if `slices.Contains` is available in your Go version.
- ❌ **Over-using `lo.Must`** — Can lead to unexpected panics in production. Use it only for initialization or in tests.
- ❌ **Deep Nesting** — Chaining too many `lo` calls can become hard to read. Break them up into intermediate variables if needed.
- ❌ **Using `lo` for performance-critical loops** — While fast, a manual loop is sometimes still faster and avoids intermediate allocations. Profile first.
