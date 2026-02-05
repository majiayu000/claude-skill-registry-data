---
name: profile-engine
description: Profile the Rust simulation engine to identify performance bottlenecks. Use when optimizing engine performance or investigating slow code paths.
allowed-tools: Read, Bash, Edit, Grep, Glob
---

# Profile Engine

Profile the Rust simulation engine using `profile.py` to identify hot paths.

## Quick Start

```bash
cd ./crates/engine
./profile.py 5000          # Profile with 5000 iterations
./profile.py 10000 --top 30  # More iterations, show top 30 functions
./profile.py --json        # Output as JSON for parsing
```

## Prerequisites

```bash
cargo install samply
brew install binutils  # Optional: better symbol resolution
```

## What profile.py Does

1. Builds the engine with debug symbols
2. Runs samply profiler on the benchmark binary
3. Parses the profile and resolves symbols
4. Shows hot modules and functions by self time

## Reading the Output

```
HOT MODULES (by self time)
─────────────────────────────────────────────────────────────────
12.5% █████████████████████░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░ engine::sim::engine

HOT FUNCTIONS (by self time, excluding std/core)
─────────────────────────────────────────────────────────────────
 Self  Total  Function                                           Location
───── ─────  ──────────────────────────────────────────────────  ────────────
 8.2%  45.3%  run_simulation                                     engine.rs:123
 4.1%  12.5%  evaluate_rotation                                  engine.rs:456
```

- **Self time**: Time spent in the function itself (optimization target)
- **Total time**: Time including all called functions
- **High self time** = hot path to optimize

## Current Hot Paths

1. `run_simulation` - main simulation loop
2. `handle_gcd_ready` - GCD event processing
3. `evaluate_rotation` - spell availability checks
4. `cast_spell` - spell execution
5. `EventQueue::push/pop` - priority queue operations

## Baseline Performance

- 300s fights, 5000 iterations
- ~0.26M sims/sec (optimized build)
- ~0.22M sims/sec (profiling build with debug symbols)

## Advanced Usage

### Manual samply (with browser UI)

```bash
cd ./crates/engine
RUSTFLAGS="-C force-frame-pointers=yes" cargo build --release
samply record --rate 4000 ./target/release/bench 5000
```

Opens Firefox Profiler with interactive flame graph.

### Production Build Settings

After profiling, ensure production settings in `Cargo.toml`:

```toml
[profile.release]
lto = true
codegen-units = 1
panic = "abort"
```

## Sources

- [Rust Performance Book](https://nnethercote.github.io/perf-book/profiling.html)
- [samply](https://github.com/mstange/samply)
