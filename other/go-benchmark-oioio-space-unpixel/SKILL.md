---
name: go-benchmark
description: Use when writing Go benchmarks or when asked to measure/optimize/improve the performance of a function — establishes correct benchmarks, measures with -benchmem and pprof, optimizes hot paths, and proves the gain (and no regression) with benchstat.
---

# Go Benchmarking & Performance

Goal: **only optimize what's measured.** Write a correct benchmark, measure, optimize, and
**prove** the improvement with `benchstat` before/after.

## When to benchmark (the right targets)

Benchmark a function when: it's on a hot path (called in tight loops — e.g. the candidate-search
and image-distance core of the port), it allocates heavily, or someone claims it's "slow". Do NOT
micro-optimize cold code — clarity wins there (see go-style-guide).

## Writing a correct benchmark (Go 1.24+)

```go
func BenchmarkDistance(b *testing.B) {
    img := loadFixture()      // setup OUTSIDE the loop
    b.ReportAllocs()          // always report allocs
    b.ResetTimer()            // if setup was non-trivial
    for b.Loop() {            // Go 1.24+: not `for i := 0; i < b.N; i++`
        sink = distance(img)  // assign to a package-level sink…
    }
}

var sink int // …to stop the compiler eliminating the call
```

- `b.Loop()` (Go 1.24+) — keeps setup/cleanup out of the timed region automatically.
- `b.ReportAllocs()` — allocs/op is usually the real lever.
- Prevent dead-code elimination: store results in a package-level `sink`.
- Table-driven sub-benchmarks with `b.Run(name, …)` for input sizes.
- `b.RunParallel` for contention; `b.SetBytes(n)` for throughput (MB/s).

## Measure

```bash
mise run bench                 # go test -bench -benchmem ./...
go test -bench=Distance -benchmem -cpuprofile cpu.prof -memprofile mem.prof ./internal/...
go tool pprof -top cpu.prof    # find the hot frames / allocations
```

## Optimize (typical levers, cheapest first)

1. **Reduce allocations**: preallocate slices/maps with known size, reuse buffers
   (`sync.Pool`, `bytes.Buffer`), avoid `[]byte`↔`string` copies (`strings.Builder`).
2. **Avoid reflection / interface boxing** on hot paths; use generics or concrete types.
3. **Hoist work out of loops**; precompute; use `slices`/`maps` helpers.
4. **Algorithmic** improvement (better complexity) beats micro-tuning — escalate to
   `algo-architect` if the win is algorithmic.

## Prove the gain (mandatory)

```bash
mise run bench:baseline        # save baseline BEFORE changing code
# …optimize…
mise run bench:compare         # benchstat baseline vs new → shows %delta + significance
```

Keep a change only if `benchstat` shows a **statistically significant** improvement (and no
regression in allocs or other benchmarks). Commit the benchmark alongside the optimization.

## Notes

- Benchmark artifacts (`bench*.txt`, `*.prof`) are gitignored and cleaned by `repo-janitor`.
- Don't sacrifice clarity for a tiny gain — measure first, and only optimize where it matters.
