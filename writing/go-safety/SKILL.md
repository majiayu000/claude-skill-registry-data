---
name: go-safety
description: "Defensive Golang coding to prevent panics, silent data corruption, and subtle runtime bugs."
metadata:
  model: models/gemini-3.1-pro-preview
  last_modified: Wed, 06 May 2026 05:20:00 GMT
---

## Core Safety Principles

1. **Defense against Nil** — Nil-related panics are the #1 cause of crashes in Go.
2. **Interface Trap** — A typed nil pointer inside an interface is NOT equal to `nil`.
3. **Map Initialization** — Reading from a nil map is safe (returns zero value), but writing to one PANICS.
4. **Slice Aliasing** — `append` may reuse the backing array, leading to shared state and silent data corruption.
5. **Defer in Loops** — `defer` runs at the end of the function, not the loop iteration. This can lead to resource exhaustion.
6. **Numeric Safety** — Integer conversions (e.g., `int64` to `int32`) truncate silently. Always check bounds.

## Common Safety Patterns

### 1. Correct Interface Return
```go
// ✅ Good: Return untyped nil for the nil case
func getHandler(enabled bool) http.Handler {
    if !enabled {
        return nil
    }
    return &MyHandler{}
}

// ❌ Bad: Returns interface{type: *MyHandler, value: nil} which != nil
func getHandler(enabled bool) http.Handler {
    var h *MyHandler
    return h 
}
```

### 2. Defensive Slice Appending
```go
// Force a copy by limiting capacity of the source slice
b := append(a[:len(a):len(a)], 4)
```

### 3. Loop Resource Management
```go
// ✅ Good: Extract to function to ensure defer runs per iteration
for _, path := range paths {
    if err := process(path); err != nil { return err }
}

func process(path string) error {
    f, err := os.Open(path)
    if err != nil { return err }
    defer f.Close()
    return doSomething(f)
}
```

### 4. Safe Type Assertions
```go
// ✅ Good: Use comma-ok pattern
v, ok := i.(string)
if !ok {
    // handle error
}

// ❌ Bad: Panics if i is not a string
v := i.(string) 
```

## Zero-Value Design

Design your structs so they are usable in their zero state (`var x T`):
- `sync.Mutex` is usable without initialization.
- `bytes.Buffer` is usable without initialization.
- **Avoid** types that panic on first use if not initialized (like uninitialized maps in structs).

## Anti-patterns

- ❌ **Bare type assertions** — `x.(T)` without `ok`.
- ❌ **Ignoring integer overflow** during conversion.
- ❌ **Comparing floats with `==`** — Use an epsilon value.
- ❌ **Returning internal slices/maps** — Return a copy instead to prevent external mutation.
- ❌ **Using `init()` for complex setup** — Can't return errors and makes testing hard.
