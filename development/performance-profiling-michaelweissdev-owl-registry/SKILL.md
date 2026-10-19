---
name: performance-profiling
description: >
  Profile system and application CPU, memory, and I/O bottlenecks across Linux,
  Go, Python, Java, and Node.js environments. Use when diagnosing high CPU
  utilization, memory leaks, GC pressure, slow endpoint latency percentiles (p95/p99),
  analyzing flamegraphs, running microbenchmarks, or tracing kernel/system calls
  with perf, pprof, py-spy, async-profiler, and eBPF.
compatibility: >
  Agent Skills-compatible coding agents with access to Linux/Unix shell, perf,
  pprof, eBPF, or language profiling runtimes. Tooling is required only for executable validation.
metadata:
  author: michaelweissdev
  version: "1.0.0"
  tags: "performance, profiling, flamegraphs, perf, pprof, py-spy, ebpf, latency, microbenchmarking, cpu, memory"
  topics: "devtools"
---

# Performance Profiling & Optimization Engineering

Performance profiling is the systematic empirical measurement of compute resource consumption—CPU cycles, heap allocations, garbage collection pauses, lock contention, and storage or network I/O. Effective profiling isolates hot execution paths and tail latencies without skewing runtime characteristics through observation overhead.

## Purpose & Overview

High-throughput and low-latency systems degrade under non-linear bottlenecks: lock serialization, cache misses, allocation churn, or off-CPU blocking. Guessing the root cause wastes engineering cycles and frequently introduces incorrect architectural changes.

This skill equips agents with standard methodologies to:
- Distinguish between on-CPU compute bottlenecks and off-CPU blocking states.
- Capture, parse, and interpret interactive flamegraphs and call graphs.
- Profile heap allocations, memory retention graphs, and garbage collection pressure.
- Trace kernel execution paths and thread scheduling using Linux `perf` and eBPF toolchains.
- Measure latency accurately using percentiles ($p50$, $p95$, $p99$, $p99.9$) rather than misleading averages.
- Design statistically sound benchmarks and microbenchmarks resistant to JIT/compiler dead-code elimination.

---

## Core Principles & Rules

1. **Profile in Production-Like Conditions**: Synthetic idle environments hide memory fragmentation, lock contention, and branch mispredictions. Always capture profiles under realistic concurrency and data distributions.
2. **Never Trust Averages for Latency**: Averages hide multi-modal distributions, outlier spikes, and long-tail degradations. Always evaluate $p50$, $p95$, $p99$, and maximum latencies.
3. **Differentiate On-CPU vs. Off-CPU Time**:
   - *On-CPU profiling* measures instructions actively executed by cores (sampling instruction pointers).
   - *Off-CPU profiling* measures threads waiting on I/O, sleep, mutex contention, or OS context switches. If CPU utilization is low but throughput is constrained, profile off-CPU time.
4. **Prefer Sampling over Heavy Instrumentation in Production**: Low-frequency timer sampling (99 Hz to 997 Hz) imposes minimal overhead (< 1-2%), whereas dynamic binary instrumentation can distort timings by orders of magnitude.
5. **Always Preserve Frame Pointers**: Compiling with `-fomit-frame-pointer` destroys stack unwinding reliability. Build profileable binaries with `-fno-omit-frame-pointer` or ensure debug symbols (DWARF) are accessible.
6. **Prevent Compiler and JIT Optimization Traps in Benchmarks**: Microbenchmarks must consume returned values via blackholes or sink variables to prevent dead-code elimination and loop hoisting.

---

## Standard Workflows & Procedures

### Workflow 1: Investigating High CPU Utilization

```
Identify Process PID
       │
       ▼
Sample CPU Stacks (perf / py-spy / async-profiler)
       │
       ▼
Generate Collapsed Stacks & Flamegraph
       │
       ▼
Identify Widest Towers on the Top Plateau (Hot Functions)
       │
       ▼
Determine Algorithmic vs. Mechanical Sympathy Bottleneck
```

1. **Verify overall system state**:
   ```bash
   # Inspect load averages, per-core utilization, and context switch rates
   mpstat -P ALL 1 5
   vmstat 1 5
   ```
2. **Sample CPU stack traces with Linux `perf`** (using an odd sampling frequency like 99 Hz to avoid harmonic lockstep with timer interrupts):
   ```bash
   # Record stacks with call-graph dwarf or fp for 30 seconds
   perf record -F 99 -p <PID> -g -- sleep 30
   
   # Inspect interactive terminal report
   perf report --stdio -n --sort comm,dso,symbol
   ```
3. **Generate a Flamegraph**:
   ```bash
   perf script | ./stackcollapse-perf.pl | ./flamegraph.pl > cpu-flamegraph.svg
   ```
4. **Interpret the Flamegraph**:
   - The x-axis represents the population of samples (alphabetical order, not passage of time).
   - The y-axis represents call stack depth.
   - Look for the widest horizontal plateaus at the top: these functions are directly executing on-CPU most frequently.

### Workflow 2: Investigating Off-CPU Blocking and Thread Contention

When application throughput drops but CPU utilization remains low (< 30%), threads are blocked waiting for locks, database queries, disk I/O, or remote RPCs.

1. **Measure Off-CPU Time using eBPF (`bpftrace` or BCC `offcputime`)**:
   ```bash
   # Trace off-CPU stacks for 10 seconds for process <PID>
   sudo offcputime-bpfcc -p <PID> -f 10 > offcpu.stacks
   ./flamegraph.pl --color=io --title="Off-CPU Time Flamegraph" offcpu.stacks > offcpu.svg
   ```
2. **Inspect System Call Latencies**:
   ```bash
   # Profile syscall latency distribution across all threads of a process
   sudo syscount-bpfcc -p <PID> -L -i 5
   ```

### Workflow 3: Memory Profiling and Leak Detection

Memory problems manifest in two forms: continuously growing retained heap (memory leaks) or rapid temporary allocations driving high GC overhead.

1. **Track Heap Allocation Rate vs. In-Use Objects**:
   - *Allocations profile*: shows every allocation regardless of whether it was subsequently freed. Useful for GC optimization.
   - *In-use heap profile*: shows memory remaining reachable at sample time. Essential for leak identification.
2. **Go Memory Diagnostics with `pprof`**:
   ```bash
   # Capture baseline in-use heap profile
   curl -s http://localhost:6060/debug/pprof/heap > base.pprof
   # Run workload, then capture second heap profile
   curl -s http://localhost:6060/debug/pprof/heap > current.pprof
   # Compare growth between snapshots
   go tool pprof -base base.pprof current.pprof
   ```
3. **Python Memory Profiling with `tracemalloc` or `memray`**:
   ```bash
   # Profile allocations and identify file/line responsible for peak memory
   memray run -o mem_profile.bin application.py
   memray flamegraph mem_profile.bin
   ```

---

## Real-World Examples & Patterns

### Pattern 1: Go Production Profiling (`net/http/pprof`)

```go
package main

import (
	"log"
	"net/http"
	_ "net/http/pprof" // Exposes /debug/pprof endpoints automatically
	"time"
)

func runHeavyTask() {
	// Allocate buffers in hot loops - candidate for sync.Pool optimization
	buf := make([]byte, 1024*64)
	_ = buf
}

func main() {
	// Run diagnostics server on dedicated internal management port
	go func() {
		log.Println("Pprof diagnostic server listening on :6060")
		if err := http.ListenAndServe("127.0.0.1:6060", nil); err != nil {
			log.Fatalf("pprof server failed: %v", err)
		}
	}()

	for {
		runHeavyTask()
		time.Sleep(10 * time.Millisecond)
	}
}
```

Capturing CPU and Mutex Contention profiles:
```bash
# Capture 30s CPU profile and open interactive web visualizer
go tool pprof -http=:8080 http://127.0.0.1:6060/debug/pprof/profile?seconds=30

# Capture lock contention profile
go tool pprof -http=:8081 http://127.0.0.1:6060/debug/pprof/mutex
```

### Pattern 2: Python Low-Overhead Sampling with `py-spy`

`py-spy` attaches to a running Python process out-of-process using kernel `process_vm_readv`, without modifying code or stopping the interpreter.

```bash
# Record interactive SVG flamegraph directly from production process
sudo py-spy record --pid 14205 --rate 100 --duration 60 --output python_flame.svg

# Live top-like terminal view showing hot functions and GIL wait time
sudo py-spy top --pid 14205
```

### Pattern 3: High-Fidelity Java Profiling with `async-profiler`

Unlike standard JVM profilers that suffer from "Safepoint Bias" (sampling only when threads reach safe stop points), `async-profiler` leverages `AsyncGetCallTrace` and OS `perf_events`.

```bash
# Profile CPU execution, avoiding safepoint bias, outputting native HTML flamegraph
./async-profiler/bin/asprof -d 30 -f /tmp/jvm_flame.html <JVM_PID>

# Profile Java object allocation directly to locate GC pressure culprits
./async-profiler/bin/asprof -d 30 -e alloc -f /tmp/jvm_alloc.html <JVM_PID>

# Profile thread lock contention
./async-profiler/bin/asprof -d 30 -e lock -f /tmp/jvm_locks.html <JVM_PID>
```

### Pattern 4: Microbenchmarking Methodology (Go & Criterion)

A robust microbenchmark must run warmups, iterate until statistical significance is reached, and prevent compiler dead-code elimination.

```go
package benchmark

import (
	"crypto/sha256"
	"testing"
)

// Global sink prevents the compiler from optimizing out the calculation
var BenchmarkResult [32]byte

func BenchmarkHasher(b *testing.B) {
	data := []byte("benchmarking-payload-sample-string")
	b.ReportAllocs() // Tracks allocations per operation and bytes allocated
	b.ResetTimer()   // Exclude fixture setup time

	for i := 0; i < b.N; i++ {
		// Assign to global variable sink
		BenchmarkResult = sha256.Sum256(data)
	}
}
```

Running and comparing benchmark iterations:
```bash
# Run benchmark 10 times with memory allocations
go test -bench=BenchmarkHasher -benchmem -count=10 > old.txt

# After optimization, re-run
go test -bench=BenchmarkHasher -benchmem -count=10 > new.txt

# Use benchstat for rigorous statistical confidence analysis
benchstat old.txt new.txt
```

---

## Common Anti-Patterns & Pitfalls

| Anti-Pattern | Operational Hazard | Correct Engineering Approach |
|:---|:---|:---|
| **Instrumenting hot loops with logging/timestamps** | Measuring `System.nanoTime()` or printing inside loops distorts cache lines and introduces massive observer effect. | Use non-intrusive sampling profilers (`perf`, `py-spy`, `pprof`) at an appropriate sampling rate. |
| **Profiling only on-CPU when latency spikes** | Threads blocked on mutexes, socket timeouts, or NVMe I/O consume zero CPU while users experience multi-second latency. | Run off-CPU analysis (`offcputime`, `syscount`, lock profiling). |
| **Reporting mean latency instead of percentiles** | A mean of 20ms can conceal 5% of users encountering 5-second timeouts. | Plot percentile distributions ($p50, p90, p99, p99.9$) and High Dynamic Range (HDR) histograms. |
| **Omitting frame pointers in production builds** | Disabling frame pointers (`-fomit-frame-pointer`) breaks stack walk unwinding in `perf` and eBPF. | Build with `-fno-omit-frame-pointer` or install debuginfo packages. |
| **Unconsumed benchmark return values** | LLVM/Go compilers detect unused results and optimize away entire function calls during dead-code elimination. | Assign results to package-level exported sinks (`blackhole`). |
| **Sampling at harmonic frequencies** | Sampling at exactly 100 Hz or 1000 Hz synchronizes with periodic OS timer interrupts or cron jobs, skewing sample counts. | Use prime sampling rates (e.g., 99 Hz, 199 Hz, 997 Hz). |

---

## Verification Checklist

- [ ] Baseline metrics captured before changes (RPS, $p50$, $p95$, $p99$ latency, CPU utilization %, memory RSS).
- [ ] Profiling method selected appropriately (Sampling for production; Allocation/Lock profiling for leaks/contention).
- [ ] Stack unwinding verified (symbols resolved; no missing `unknown` or `[vdso]` frames caused by omitted frame pointers).
- [ ] Flamegraph analyzed on both axes: horizontal width (sample share) and vertical depth (call recursion).
- [ ] Microbenchmarks include memory allocation metrics (`allocs/op`, `B/op`) and prevent dead-code elimination.
- [ ] Statistical significance validated across multiple benchmark iterations using comparative tooling (`benchstat` or Criterion confidence intervals).
- [ ] Post-optimization profile captured to confirm hot-path reduction without shifting bottleneck to secondary subsystem.

---

## Tooling & Reference Guides

- **perf**: Standard Linux performance counter and sampling profiler (`man perf`, `perf record`, `perf report`).
- **Brendan Gregg's Flame Graphs**: Canonical scripts and methodology for stack trace visualization ([brendangregg.com/flamegraphs.html](https://www.brendangregg.com/flamegraphs.html)).
- **eBPF BCC & bpftrace**: Kernel and userspace dynamic tracing utilities (`offcputime`, `biolatency`, `profile`).
- **Go pprof**: Native runtime execution, CPU, memory, and block profiler (`go tool pprof`, `net/http/pprof`).
- **py-spy**: Non-intrusive, out-of-process sampling profiler for Python applications.
- **async-profiler**: Low-overhead, accurate CPU and allocation profiler for JVM applications without safepoint bias.
- **benchstat**: Tool for statistical analysis and regression detection between benchmark samples.
