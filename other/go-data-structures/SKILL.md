---
name: go-data-structures
description: "Golang data structures — slices, maps, arrays, and standard library collections. Covers internals, performance, and correct usage."
metadata:
  model: models/gemini-3.1-pro-preview
  last_modified: Wed, 06 May 2026 05:25:00 GMT
---

## Core Collections

### 1. Slices
A slice is a 3-word header: pointer, length, and capacity.
- **Preallocation**: Use `make([]T, 0, n)` if the final size is known to avoid multiple allocations and copies during `append`.
- **Growth**: Slices grow by doubling (if < 256) or by ~25% (if >= 256).
- **`slices` package**: Use `slices.Sort`, `slices.Contains`, `slices.Clone` (Go 1.21+).

### 2. Maps
Maps are hash tables with 8-entry buckets.
- **Initialization**: Use `make(map[K]V, n)` to pre-size the hash table.
- **Not thread-safe**: Use `sync.Mutex` or `sync.Map` for concurrent access.
- **Ordering**: Iteration order is random and changes.

### 3. Arrays
Fixed-size value types.
- Copied entirely on assignment.
- Useful for fixed-size data like hashes (`[32]byte`) or IPv4 addresses.

## Standard Library Containers

| Package | Structure | Best For |
| --- | --- | --- |
| `container/list` | Doubly-linked list | LRU caches, frequent middle insertions. |
| `container/heap` | Min/Max heap | Priority queues, scheduling. |
| `container/ring` | Circular buffer | Fixed-size rolling windows. |

## Specialized Builders

- **`strings.Builder`**: The most efficient way to concatenate strings in a loop.
- **`bytes.Buffer`**: Best for bidirectional I/O (reads and writes).

## Copy Semantics

| Type | Assignment Behavior |
| --- | --- |
| `int`, `string`, `struct`, `array` | Deep copy (value is copied) |
| `slice`, `map`, `chan`, `pointer` | Reference copy (shares underlying data) |

## Performance Tips

1. **Preallocate**: Always preallocate if you know the number of items.
2. **Avoid Pointer Chasing**: Slices have better cache locality than linked lists.
3. **Small Keys in Maps**: Using large structs as map keys can be slow; use pointers or simple types if possible.
4. **Strings are Immutable**: Converting `[]byte` to `string` (and vice versa) usually allocates. Use `strings.Builder` or `bytes.Buffer` to minimize this.

## Anti-patterns

- ❌ **Growing slices in a loop** without `make(..., capacity)`.
- ❌ **Using `container/list` by default** — slices are almost always faster due to cache locality.
- ❌ **Relying on map iteration order** — it is intentionally non-deterministic.
- ❌ **Storing pointers to short-lived data in maps** — can prevent GC from reclaiming memory.
- ❌ **Using `reflect.DeepEqual`** for comparing data structures in hot paths.
