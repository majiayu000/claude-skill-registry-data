---
name: go-performance
description: "Golang performance optimization patterns. Covers allocation reduction, CPU efficiency, memory layout, and benchmarking methodology."
metadata:
  model: models/gemini-3.1-pro-preview
  last_modified: Wed, 06 May 2026 04:55:00 GMT
---

## Core Philosophy

1. **Profile before optimizing** — Never guess where the bottleneck is. Use `pprof`.
2. **Reduce Allocations** — Go's GC is fast, but reducing allocations is often the highest ROI optimization.
3. **Measure, Change, Re-measure** — Use `benchstat` to confirm that changes are statistically significant.
4. **Document Optimizations** — Explain *why* a pattern is used, preferably with benchmark results.

## Optimization Methodology

1. **Write a benchmark** — Isolate the function in a `_test.go` file.
2. **Baseline** — Run `go test -bench . -benchmem -count 5 > old.txt`.
3. **Identify** — Use `go tool pprof` to find hot spots in CPU or heap.
4. **Optimize** — Apply one change at a time.
5. **Compare** — Run benchmarks again and use `benchstat old.txt new.txt`.

## Common Performance Patterns

| Technique | Goal | Example |
| --- | --- | --- |
| **Preallocation** | Avoid re-allocating backing arrays | `make([]int, 0, length)` |
| **sync.Pool** | Reuse objects to reduce GC pressure | Reuse buffers or large structs |
| **struct alignment** | Minimize padding (smaller memory footprint) | Place larger fields before smaller ones |
| **Avoid reflection** | Speed up operations | Use code generation or explicit types |
| **Fast String Concatenation** | Reduce allocations in loops | Use `strings.Builder` |
| **Pointers vs Values** | Minimize copying or GC tracking | Use pointers for large structs (>128 bytes) |

## Standard Library Tools

- **`go test -bench`**: Running benchmarks.
- **`net/http/pprof`**: Profiling running services.
- **`runtime.MemStats`**: Checking memory usage at runtime.
- **`sync.Pool`**: Reusing temporary objects.
- **`strings.Builder`**: Efficiently building strings.

## Benchmarking Snippet

```go
func BenchmarkProcess(b *testing.B) {
    data := prepareData()
    b.ResetTimer() // Don't count setup time
    for i := 0; i < b.N; i++ {
        Process(data)
    }
}
```

## Anti-patterns

- ❌ **Optimizing without profiling** — Wasting time on things that don't matter.
- ❌ **Using `reflect.DeepEqual`** in hot paths — It's very slow. Use typed comparisons.
- ❌ **Ignoring `GOMEMLIMIT`** in containers — Can lead to OOM kills.
- ❌ **Logging in hot loops** — Logging allocates and can be very slow.
- ❌ **Unbounded goroutine spawning** — Can exhaust memory and CPU.
- ❌ **Speculative preallocation** — `make([]T, 0, 10000)` when the common case is 5.
