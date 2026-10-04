---
name: go-benchmark
description: "Golang benchmarking, profiling, and performance measurement methodology. Covers writing benchmarks, profiling with pprof, and analyzing results."
metadata:
  model: models/gemini-3.1-pro-preview
  last_modified: Wed, 06 May 2026 05:15:00 GMT
---

## Writing Benchmarks

Benchmarks are placed in `_test.go` files and start with `Benchmark`.

### `b.Loop()` (Go 1.24+)
The modern way to write benchmarks. It automatically handles timer resets and prevents compiler optimizations from removing "dead" code.

```go
func BenchmarkProcess(b *testing.B) {
    data := prepareData() // setup code (not timed)
    for b.Loop() {
        Process(data) // timed code
    }
}
```

### Traditional `for range b.N`
Used in older Go versions. Requires manual timer management.

```go
func BenchmarkProcessLegacy(b *testing.B) {
    data := prepareData()
    b.ResetTimer()
    for i := 0; i < b.N; i++ {
        Process(data)
    }
}
```

## Running Benchmarks

```bash
# Run all benchmarks with memory allocation stats
go test -bench=. -benchmem ./...

# Run a specific benchmark 10 times for statistical significance
go test -bench=BenchmarkProcess -count=10 ./... | tee bench.txt

# Run and generate a CPU profile
go test -bench=. -cpuprofile=cpu.prof
```

## Analyzing Results

### benchstat
Use `benchstat` to compare results before and after an optimization.

```bash
go install golang.org/x/perf/cmd/benchstat@latest
benchstat old.txt new.txt
```

### pprof
Interactive tool to visualize where time and memory are spent.

```bash
# Analyze CPU profile
go tool pprof cpu.prof

# Analyze Memory profile (allocations)
go tool pprof -alloc_objects mem.prof
```

## Key Metrics

- **ns/op**: Nanoseconds per operation (lower is better).
- **B/op**: Bytes allocated per operation.
- **allocs/op**: Number of distinct heap allocations per operation.

## Best Practices

1. **Reset Timer** — Use `b.ResetTimer()` if you have expensive setup code (in legacy benchmarks).
2. **Report Allocs** — Always use `-benchmem` or call `b.ReportAllocs()` to see GC pressure.
3. **Statistical Rigor** — Never rely on a single run. Use `-count=10` and `benchstat`.
4. **Prevent Compiler Optimization** — Ensure the result of the benchmarked function is used (e.g., assign to a package-level variable) if not using `b.Loop()`.
5. **Table-Driven Benchmarks** — Use `b.Run` to test different input sizes.

## Anti-patterns

- ❌ **Guessing bottlenecks** — Always profile first.
- ❌ **Benchmarking on a noisy machine** — Close other apps to ensure reproducible results.
- ❌ **Comparing single runs** — Small variations can look like improvements.
- ❌ **Dead code elimination** — The compiler might remove your code if it detects the result is unused.
- ❌ **Counting setup time** — Forgetting to reset the timer or stop it during setup.
