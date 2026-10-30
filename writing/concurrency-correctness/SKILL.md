---
name: concurrency-correctness
description: Detects multi-threaded code where a lock is held across a blocking operation, lock acquisition order risks deadlock, lock-free atomics use the wrong memory ordering, or double-checked locking is missing the necessary barrier. Use when writing or modifying code that acquires multiple locks, uses atomic operations with explicit memory orders (std::memory_order_*, atomic.LoadAcquire, Ordering::Relaxed), implements lazy initialization with double-checked locking, or calls a blocking operation (I/O, sleep, await, blocking channel send) inside a locked region.
---

# Concurrency Correctness (CWE-833, CWE-820, CWE-667)

## What this checks

Concurrency bugs that read clean in isolation but produce deadlocks, lost wakeups, or
data races in production. Race detectors catch *triggered* races but not structural
mistakes. Flags local patterns: lock-around-blocking-call, lock-order in nested
acquires, atomic memory order, double-checked locking. Not a replacement for
whole-program ownership analysis (borrow checker, lockdep, model checking).

## Vulnerable patterns

- Lock held across a blocking operation — `await`, `sleep`, blocking I/O, or a blocking channel send — so every other waiter blocks on the slow thing
- Inconsistent lock order across call sites — one path acquires `(L1, L2)`, another acquires `(L2, L1)`, producing classic AB-BA deadlock
- Recursive acquisition of a non-recursive mutex on the same thread
- Atomic flag published with relaxed ordering where acquire/release is required — the reader can observe the flag set before the writer's payload writes are visible
- Double-checked locking where the outer read of the published pointer or flag uses no acquire barrier
- Acquiring a lock and then sending on an unbuffered channel whose receiver needs the same lock to make progress
- Async cancellation that interrupts a critical section without restoring invariants

## Fix immediately

Flag the vulnerable code, explain the risk, and suggest a fix establishing these
properties. Translate to the concurrency primitives of the audited file — use that
language's documented lock, atomic, once-cell, and channel APIs; do not import a recipe
from a different language.

1. **No blocking operation inside a held lock.** Snapshot whatever state is needed under the lock, release the lock, then perform the I/O, `await`, or `sleep` on the snapshot. The critical section stays bounded by CPU work only.
2. **Lock order is canonical and total.** Every code path that acquires two or more locks acquires them in the same sequence — sorted by address, by name, or via a scoped/multi-lock primitive that handles ordering. Document the ordering rule near the lock declarations.
3. **Memory ordering on atomics matches the synchronization need.** Use acquire on the read and release on the write whenever an atomic publishes a pointer, flag, or sequence that the reader will then dereference. Relaxed ordering is reserved for counters and statistics where no other state depends on the value.
4. **Lazy initialization uses a primitive that is correct by construction** — a one-shot init helper, a function-local static where the language guarantees thread-safe initialization, or an atomic with explicit acquire/release on both the outer and inner reads. Hand-rolled double-checked locking without a barrier is not acceptable.
5. **Non-recursive mutexes are never re-entered on the same thread.** When a recursive call site genuinely needs to take the lock again, use the recursive variant explicitly.

## Verification

Criteria apply only to constructs the audited file actually contains;
mark inapplicable bullets N/A rather than skipping silently.

- [ ] No `await`, sleep, blocking I/O, or blocking channel send appears inside a held-lock scope
- [ ] When a function acquires two or more locks, the order is total — every code path that holds both acquires them in the same sequence
- [ ] Every relaxed-ordered atomic operation is paired with a comment explaining why relaxed is sufficient (e.g. statistics counter, not a synchronization flag)
- [ ] Lazy initialization uses a once-helper, a thread-safe function-local static, or an atomic with explicit acquire/release on both reads — not hand-rolled double-checked locking without a barrier
- [ ] No recursive lock attempt on a non-recursive mutex

## References

- CWE-833 ([Deadlock](https://cwe.mitre.org/data/definitions/833.html))
- CWE-820 ([Missing Synchronization](https://cwe.mitre.org/data/definitions/820.html))
- CWE-667 ([Improper Locking](https://cwe.mitre.org/data/definitions/667.html))
- CWE-362 ([Race Condition](https://cwe.mitre.org/data/definitions/362.html))
