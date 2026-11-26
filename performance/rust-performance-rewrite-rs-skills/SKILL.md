---
name: rust-performance
description: Profile before optimizing, cut allocation out of hot paths, and treat LTO, codegen-units, PGO and target-cpu as the last five percent. Use when Rust code is too slow, when a benchmark regresses, when reviewing code that allocates or formats inside a loop, when release-profile or codegen flags come up, or when the user asks how to make Rust faster.
---

# Rust Performance

No change lands here that no measurement named: the profile is the entry ticket,
and the codegen flags are the last five percent, not the first move. Async
throughput is `/async-rust`; `unsafe` for speed is `/unsafe-rust`.

## Measure, then change

No optimisation lands without a measurement that named it. Skipping it costs
twice: the change that made nothing faster, and the change that made the code
worse in exchange for nothing. A profile finds the one function that holds the
time — almost never the one that looked expensive while reading.

First settle whether speed matters for this crate at all. A parser fed
bulk input or a service on the request path does; a one-shot setup tool does
not, and treating it as hot buys complexity for nothing. When it does, find
the hot paths, benchmark them, profile on a schedule rather than once, and
record each hot spot in a comment beside the code, so the next editor knows
which lines are load-bearing for speed and does not tidy them away.

## Benchmarks that mean something

`criterion` for a statistical comparison against a stored baseline; `divan` when
a lighter harness is enough. Benchmark the operation, not the setup around it.
Pass inputs and results through `std::hint::black_box`, or the optimiser may
see that the value is never used and delete the very work being timed.

Without it, the profiler shows addresses instead of function names:

```toml
[profile.bench]
debug = 1
```

A benchmark run on a laptop under thermal throttling produces a number, just not
a comparable one — the machine has to be quiet between the runs being compared.

## Allocation is usually the answer

The highest-yield category, and the one a profile names most often:

- `Vec::with_capacity` when the size is known — the default grows and copies.
- Clear-and-reuse over allocate-per-iteration: buffer outside, `clear()` inside.
- `Box<[T]>` and `Box<str>` for an owned sequence that will never grow.
- `mem::take` to move a value out of a `&mut` without cloning.
- No `format!` in a hot loop — every call allocates a fresh `String`.
- `Cow` for the borrow-or-own case — copy only when the value changed.

One complete example, joining with a known total size:

```rust
fn joined(parts: &[String]) -> String {
    let total = parts.iter().map(|p| p.len() + 1).sum();
    let mut out = String::with_capacity(total);
    for (i, part) in parts.iter().enumerate() {
        if i > 0 {
            out.push(' ');
        }
        out.push_str(part);
    }
    out
}
```

The reuse patterns and the buffer-passing shapes are in `ALLOCATION.md`.

## Pick the collection for the access pattern

`Vec` beats `HashMap` for small `n` because of cache behaviour, not
asymptotics. `BTreeMap` when iteration order matters. A sorted `Vec` plus
`binary_search` when built once and read many times. The crossover is a thing
to measure, not a constant to memorise.

## Hashing

The default hasher is DoS-resistant and correspondingly slow. Swapping it is
safe and worthwhile only when the keys are not attacker-controlled — internal
IDs, enum discriminants, interned strings. With attacker-controlled keys it is
a denial-of-service surface, and no lookup speed buys that back. For trusted keys, `foldhash` or `FxHash`
(the `rustc-hash` crate) are the usual faster choices. Say the risk
plainly rather than presenting the swap as a free win.

## Iterators and bounds checks

An iterator chain gives the optimiser the length invariant an index loop hides,
which is how bounds checks disappear: two `[i]` reads in one loop become
`iter().zip()`, and the optimiser can prove the accesses in range. This is the
one place where the idiomatic form is also the fast form — no tradeoff to
argue about. Where a hand-written loop looks faster, or the chain looks
expensive, settle it by benchmarking the two forms on real data rather than by
assertion; the result may go either way, and only the number decides.

## Batch entry points for bulk work

When a path handles many items, the figure that matters is items per CPU
cycle, not latency of one item. Offer a batched entry point beside the
single-item one, so a caller with a thousand inputs pays the fixed cost
(a lock, a syscall, a dispatch) once:

```rust
use std::sync::Mutex;

struct Counter(Mutex<u64>);

impl Counter {
    fn add(&self, n: u64) {
        *self.0.lock().unwrap() += n;
    }

    fn add_all(&self, items: &[u64]) {
        *self.0.lock().unwrap() += items.iter().sum::<u64>();
    }
}
```

Do not spin a thread waiting for work, and do not do per-item work (a lock,
an allocation, a log event) where one pass over the batch would do. Yielding
in long async work is `/async-rust`.

## Indirection on hot types

Every pointer hop on a hot value is a cache miss waiting to happen. Do not
stack `Arc<Mutex<Arc<...>>>` layers on a type touched in the hot path: one
shared handle at the right level is enough, and each extra layer is another
allocation and another dependent load. A small field read constantly, such as
a `retry_limit: u8` field, belongs directly in the owning struct, not behind a
shared pointer that each check must chase.

## The last five percent

LTO, `codegen-units = 1`, PGO, `target-cpu`. Per ADR 0007: application
decisions, never library defaults, each with the portability cost stated
alongside the gain — a knob is one line and a profile is an afternoon:

- `target-cpu=native` in committed config produces a binary that faults on an
  older machine.
- PGO needs a representative workload, or it optimises for the wrong path.
- LTO and `codegen-units = 1` buy a percentage, not a factor, at the cost of
  build time.
- For a server application, set `target-cpu` to the highest level the
  deployment guarantees, such as `x86-64-v3`, in the committed
  `.cargo/config.toml`. The guaranteed baseline is the rule: not `native`, and
  not a level some deployed host lacks. A library leaves the setting alone.
- An application may set `mimalloc` as its `#[global_allocator]`; gains of up
  to a quarter have been reported on allocation-heavy loads. Measure on the real
  workload before keeping it, and never set a global allocator from a library.

`panic = "abort"` is not a performance default: it is an application-level
choice, a library cannot assume unwinding, and it changes behaviour under
`#[should_panic]`.

## Deferrals

Async throughput, executor stalls, and `spawn_blocking` are `/async-rust` — the
runtime question, not the throughput one. Reaching for `unsafe` to skip a check
is `/unsafe-rust`, and the answer there is that the block needs a soundness
argument, not a benchmark. Whether the clone the profile found should exist at
all is `/ownership-not-clone`.

## Verification

```bash
cargo bench                  # against the recorded baseline where one exists
cargo clippy --all-targets   # at the level the repo configures; add -- -D warnings only if it configures none
cargo test --release
```

A benchmark with no stored baseline proves nothing about a change — record the
before, then measure the after, and compare against the noise the benchmark
reports. Clippy keeps the lint level the target repo configured; `-D warnings`
is the fallback for a repo that configures no lints at all.
