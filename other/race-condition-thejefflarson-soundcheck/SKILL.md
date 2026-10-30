---
name: race-condition
description: Detects check-then-act sequences on shared state vulnerable to TOCTOU
  manipulation. Use when writing check-then-act sequences on shared state,
  file operations that check existence before read/write, balance updates
  without locking, or any code where two operations on the same resource are
  not atomic.
---

# Race Condition Security Check (CWE-362)

## What this checks

Protects against time-of-check-to-time-of-use (TOCTOU) and other race conditions where
concurrent access to shared state creates a window for attackers to manipulate data
between a check and its corresponding action. Exploitation leads to privilege escalation,
double-spend, and data corruption.

## Vulnerable patterns

- File existence checked before opening, deleting, or creating — the file can be swapped between the check and the operation.
- Balance, quota, or counter read into memory, modified, then written back without locking or a transaction — concurrent updates lose writes or double-spend.
- "Does this username exist? if not, create it" with no database-level uniqueness constraint — two concurrent callers both see "no" and both create.
- Privilege or ownership checked in one call, then a separate later call performs the action on the same resource — the resource may have changed between calls.

## Fix immediately

Flag the vulnerable code and explain the risk. Then suggest a fix that establishes
these properties. Translate each property into the audited file's language,
database driver, and filesystem API — use the platform's documented atomic
primitives.

1. **No check-then-act sequence on shared state runs without atomicity.** The
   check and the act collapse into a single atomic operation, or both sit
   inside a lock, transaction, or database-level guard. A read followed by a
   separate write is the exact bug — merge them into a conditional update that
   returns the affected row count.
2. **Balance, counter, and quota updates use atomic increments or
   compare-and-swap** — never a read-modify-write sequence in application
   code. Under concurrency the read-modify-write loses every interleaved
   update; the database or atomic type is the correct place for the mutation.
3. **File operations that depend on existence use atomic primitives** —
   exclusive-create flags, atomic rename, atomic link. A separate exists check
   followed by an open is TOCTOU-exploitable; the atomic flag short-circuits
   the window.
4. **Uniqueness constraints live in the database, not in application code.**
   An "exists then create" pattern races two ways with itself; a uniqueness
   index plus an insert-and-catch-duplicate pattern is race-free by
   construction.

## Verification

- [ ] No check-then-act sequence on shared state (files, database rows, in-memory counters) operates without atomicity — either a single atomic operation, a lock, or a database-level guard
- [ ] Balance/counter updates use atomic increments or compare-and-swap, not read-modify-write sequences
- [ ] File operations that depend on existence or state use atomic primitives (exclusive-create, atomic rename, atomic link) rather than check-then-act
- [ ] Uniqueness is enforced by a database constraint, not by an application-level exists-then-create pattern

## References

- CWE-362 ([Concurrent Execution Using Shared Resource with Improper Synchronization](https://cwe.mitre.org/data/definitions/362.html))
- CWE-367 ([TOCTOU Race Condition](https://cwe.mitre.org/data/definitions/367.html))
