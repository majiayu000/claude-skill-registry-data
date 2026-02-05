---
name: go-nil-map
description: Map nil safety - read OK, write panics
---

# Map Nil Safety

## Problem
Reading from nil map returns zero value. Writing to nil map panics.

## Pattern

### WRONG - Write to nil map
```go
var m map[string]int  // nil map
m["key"] = 42         // PANIC: assignment to entry in nil map
```

### CORRECT - Initialize with make
```go
m := make(map[string]int)
m["key"] = 42  // OK
```

### Reading is Safe
```go
var m map[string]int  // nil map
v := m["key"]         // OK, v = 0 (zero value)
v, ok := m["key"]     // OK, v = 0, ok = false
```

## Quick Fix
- [ ] Always initialize maps with make() before writing
- [ ] Check if map is nil before range/write
- [ ] Reading from nil map is safe but returns zero values

## Defensive Pattern
```go
if m == nil {
    m = make(map[string]int)
}
m["key"] = 42
```
