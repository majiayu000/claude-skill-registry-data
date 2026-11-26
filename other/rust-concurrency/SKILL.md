---
name: rust-concurrency
description: Pick the concurrency model from the workload shape — rayon for data parallelism, scoped threads for borrowed stack data, channels for handoff, shared state last — and use the weakest correct atomic ordering. Use when writing or reviewing threaded Rust, when Mutex, RwLock, atomics, or manual Send/Sync appear, when a deadlock or data race is suspected, or when the user asks how to parallelize Rust code.
---

# Rust Concurrency

The shape of the workload picks the model. This skill owns that pick for
threads, and it stops where task concurrency begins — runtime, executors,
`spawn_blocking`, and cancellation live in `/async-rust`.

## The shape picks the model

- The same operation over many independent items: data parallelism, `rayon`.
- Independent units of work that are mostly waiting: task concurrency,
  `/async-rust`, not here.
- State several threads read and write: shared state — the one to reach for
  last, because it is the only one of the three that can deadlock.

## Data parallelism

`par_iter()` is a one-word change to an iterator chain that already exists —
exactly why the chain was worth writing. The precondition: the per-item work
has to be large enough to pay for the scheduling. A `par_iter` over a million
cheap closures is often slower, and is the standard disappointment.

## Scoped threads

`std::thread::scope` lets a thread borrow stack data, because the scope
guarantees the join before the stack unwinds — which is what removes the
`'static` bound that otherwise forces an `Arc`:

```rust
fn sum_halves(data: &[u64]) -> u64 {
    let (left, right) = data.split_at(data.len() / 2);
    std::thread::scope(|s| {
        let a = s.spawn(|| left.iter().sum::<u64>());
        let b = s.spawn(|| right.iter().sum::<u64>());
        a.join().unwrap() + b.join().unwrap()
    })
}
```

Reach for a scope before an `Arc` or a clone buys the second thread.

## Channels for handoff

A channel moves ownership with the message — no lock to hold, nothing to
poison. Sender-drop is the shutdown signal: `recv` reports disconnection.
Bounded versus unbounded is backpressure: an unbounded channel silently
converts a throughput problem into a memory problem.

## Shared state

The compiler's guarantee is narrower than it feels: `Send`, `Sync`, and the borrow
checker rule out data races in safe code. They do not rule out deadlocks, nor
logic races — two threads each doing a correct step in an order the program did
not intend. Message passing sidesteps most of this, so it is the first choice
before a lock.

`Mutex` is the default; `RwLock` pays off only with genuinely read-heavy
access, and can starve writers. Rules for using a lock well:

- Put data whose parts must stay consistent with each other under one lock. Two
  locks for two halves of one invariant let another thread see them out of sync.
- Hold the guard for the shortest possible scope, and never across a call into
  code that might lock again. That includes invoking a closure or callback while
  the guard is live: the caller decides what it does.
- Do not return a `MutexGuard` to a caller. It leaks the locking discipline across
  an API boundary; return the value, or take a closure that runs inside the lock.
- If two locks must be held together, take them in one agreed order. Fall back to a
  written lock hierarchy only once restructuring to need one lock, or none,
  has failed.

A `Mutex` whose holder panicked is poisoned, and `lock()` hands back an `Err`.
Three positions exist, and which applies depends on what the protected data
looks like after the panic:

| Position | When it applies |
|---|---|
| Propagate the error, or recover with `into_inner()` and a written reason | The default. The holder panicked, but the data is still consistent (a counter, a cache that can be rebuilt); say so in a comment |
| Never touch the data behind a poisoned lock | The stricter line, for state where a half-finished update could be mistaken for a good one |
| Panic on poison (`lock().unwrap()`, `expect`) | A deliberate stop when the state cannot be trusted and nothing can repair it. Write the reason; it is a decision, not a shortcut |

What is ruled out is the reflexive `unwrap` that was never weighed.

## Libraries and threads

Library code does not start threads of its own. Spawning is a program-level
decision about cost and shutdown; a library that does it hides threads from the
caller and cannot be embedded in a runtime or sandbox that forbids them. Take a
closure, an executor handle, or run work on the caller's thread, and let the
binary decide.

## Atomics and orderings

The rule: `Relaxed` for a counter nobody synchronises on, `Acquire`/`Release`
for a paired handoff where one thread publishes and another observes,
`SeqCst` when unsure and the cost is acceptable. The pair is the one that is
wrong most often:

```rust
use std::sync::atomic::{AtomicBool, AtomicU64, Ordering};
use std::sync::Arc;

fn main() {
    let value = Arc::new(AtomicU64::new(0));
    let ready = Arc::new(AtomicBool::new(false));
    let (v, r) = (Arc::clone(&value), Arc::clone(&ready));
    let publisher = std::thread::spawn(move || {
        v.store(42, Ordering::Relaxed);
        r.store(true, Ordering::Release);
    });
    while !ready.load(Ordering::Acquire) {
        std::thread::yield_now();
    }
    assert_eq!(value.load(Ordering::Relaxed), 42);
    publisher.join().unwrap();
}
```

The `Release` store orders the write to `value` before `ready` flips, and
the `Acquire` load pairs with it. If the ordering argument cannot be
written down in two sentences, the code wants a `Mutex`.

## Manual `Send`/`Sync` is an unsafe claim

`unsafe impl Send for T` asserts what the compiler could not prove; the
`// SAFETY:` comment must hold an actual argument. The soundness review
goes to `/unsafe-rust` — this skill only insists the claim is written. It is never a way to silence a `Send` bound error that the code really violates; fix the data crossing the thread instead.

## `thread_local!` over `static mut`

`static mut` is effectively unusable in current editions and was never
sound to share; `thread_local!` is the per-thread answer. Avoid it where one
consistent value across threads is the point — each thread sees its own copy.
Passing state explicitly beats hiding it in a global, which has no visible owner.

## Deferrals

Task concurrency, executors, `spawn_blocking`, and cancellation are
`/async-rust`. Whether the state should be shared at all is
`/ownership-not-clone`. The soundness of an `unsafe impl` is `/unsafe-rust`.
Throughput of the parallel version is `/rust-performance`.

## Verification

```bash
cargo test                    # including the ignored-by-default stress tests, if the repo has any
cargo clippy --all-targets    # at the level the repo configures
cargo miri test               # where atomics or unsafe Send/Sync are involved
```

Deadlocks are timing-dependent and rarely fail an ordinary run. Where the code
holds more than one lock, add a deadlock-detection job to CI — for instance
`parking_lot` with its `deadlock_detection` feature polled by a watchdog thread
during the stress tests, or `loom` models of the lock order — so a cycle in the
lock order becomes a red build instead of a production hang.

Clippy runs at the lint level the target repo configures; `-D warnings`
is the fallback only when the repo configures no lints at all. Lock-free
structures and non-trivial ordering arguments want `loom` — it explores
interleavings exhaustively rather than hoping the scheduler picks the
bad one; it runs under its own cfg, and the model has to be small.
