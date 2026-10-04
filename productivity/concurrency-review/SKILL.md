---
name: concurrency-review
description: Review concurrency design for races, leaks, and cancellation bugs. Portable, language-agnostic. In-process concurrency is the default; process fan-out is not.
triggers:
  - concurrency review
  - race review
  - parallel agents architecture
  - thread safety review
tools:
  - read_file
  - list_dir
  - grep
  - glob
  - find_references
---

<!-- Provenance: generic, portable. It names no fixed language or concurrency runtime. -->

# Concurrency Review

## Purpose

Review a change's concurrency design for data races, resource leaks, cancellation gaps, and architectural fitness. Identify conditions under which concurrent execution fails, and confirm the architecture matches the project's intended concurrency model.

This skill is the **portable, reasoning-driven** concurrency reviewer. A repository may also provide a project-bound concurrency rule or contract (for example a rule that fixes in-process tasks as the default and bans `os/exec` fan-out). When one exists and the change is within its scope, defer to it for mechanical gates; use this skill when no project-specific contract applies, or for the invariant-driven reasoning and report it provides.

## Read First

- The diff or packages named by the user, and the baseline (branch/commit/HEAD) to compare against.
- The project's documented concurrency model, conventions, and constraints, when they exist (for example a rule that declares in-process tasks as the default).
- Workspace conventions for testing, race detection, and concurrency fixtures, when they exist.

## Method

1. Map the concurrency surface of the change: shared mutable state, synchronization primitives (locks, mutexes, semaphores, atomics, channels, queues), background workers or threads, cancellation or shutdown paths, and ordering assumptions.
2. Derive the invariants that must hold: mutual exclusion, happens-before ordering, resource lifetime, cancellation propagation, idempotency under retry, and freedom from deadlock.
3. For each invariant, search for an execution path that violates it. Prefer concrete counterexamples (interleavings, partial failure, retry storms, cancellation mid-operation, restart during a write) over general concerns.
4. Check the load-bearing failure modes:
   - data races on shared state without synchronization;
   - atomicity violations: compound read-modify-write operations that must be atomic but are not (check-then-act / TOCTOU is the security-relevant form: a permission or existence check that passes, then the state changes before the guarded action);
   - deadlocks from inconsistent lock ordering or holding a lock across a blocking call;
   - leaked workers, threads, or goroutines that never terminate on cancellation or timeout;
   - missing or partial cancellation propagation to children, I/O, or downstream work;
   - double-close, double-send-on-closed-channel, or use-after-free equivalents;
   - lost wakeups or missed signals in wait/notify patterns;
   - starvation, unfair scheduling, or livelock under contention;
   - thundering-herd or unbounded fan-out under load.
5. Check the durable-state failure modes. When concurrent workers coordinate through a
   shared store rather than through in-process memory, a race detector proves nothing:
   the interleaving happens between transactions, and the workers may be separate
   processes or separate hosts. Treat this surface as first-class, not as a variant of
   the in-memory one.
   - **Exclusion without a fence.** A boolean claim flag, an owner column, or a
     "running" status is not exclusion. Exclusion needs a monotonic fence token or a
     lease with an expiry, so a stale owner's next write fails instead of winning.
     Review the takeover path explicitly: owner A stalls, owner B takes over, owner A
     resumes and writes.
   - **Compare-and-set against a stale version.** The version must come from a live
     read, never from a constant or a value read before an intervening operation. A
     failed set must not fall through into the success path, and must not leave the
     caller running work the state no longer authorizes.
   - **Lost update through read-modify-write.** Two workers read, both compute, both
     write. Confirm the write is conditional on the version each worker read.
   - **Admission of duplicates.** Two callers submit the same logical work at the same
     time. Confirm exactly one unit of work exists afterwards, enforced by a unique
     constraint or a conditional insert, not by a prior existence check.
   - **Claim not released on a failure branch.** Trace every early return, refusal, and
     pre-flight rejection between claim and release.
   - **Interleaving between two durable writes.** A crash or a takeover can land in the
     gap. Name the state at each gap and confirm the recovery path handles it, and that
     recovery is idempotent under a repeat run.
   - **Effects that outlive the claim.** An external side effect (a publish, a message,
     a payment, a created resource) performed after a claim was lost is a double
     effect. Confirm the effect is fenced, or is idempotent by key.
   Prove these with deterministic fixtures that drive the interleaving through the
   store: two workers against one record, a takeover between two writes, a repeated
   recovery run. A race detector run is not evidence for this class.
6. Reject default architectures that fan out one OS process per concurrent task as the concurrency model. External subprocess calls are an adapter boundary with timeouts, cancellation, and allowlists, not the fan-out primitive.
7. Require tests that prove the load-bearing paths under the project's race
   detector or concurrency test mode. When the invoking agent has command
   execution, run them; otherwise report the run `PARTIAL`/`NOT_RUN` with the
   reason. A single green sequential run is not evidence for concurrent code;
   treat pass-once-fail-on-retry as a failure to investigate.
8. When a test or check fails and the invoking agent has command execution,
   reproduce against the baseline in the same environment: baseline-fails-too
   implies environmental or pre-existing; baseline-passes implies caused by the
   change. Without command execution, report the reproduction
   `PARTIAL`/`NOT_RUN` with the reason. Continue with all remaining safe checks
   either way.
9. Adversarially refute each finding: strongest innocent explanation, existing guards, reachability, and counterexample. Reject unsupported findings. Do not weaken them into vague advice.

## Language-mapping reference

The concepts are universal; the primitives differ by language. Discover the project's primitives from the workspace, do not assume them. Common mappings:

- **shared state + exclusion:** Go `sync.Mutex` / `RWMutex`; Java `synchronized` / `ReentrantLock`; Rust `Mutex<T>` / `RwLock<T>`; Python `threading.Lock`; C# `lock` / `SemaphoreSlim`; JS/TS single-threaded but shared via async closures over mutable references.
- **cancellation:** Go `context.Context`; Java `InterruptedException` / `Future.cancel`; Rust `CancellationToken` (tokio) or drop; C# `CancellationToken`; Python `threading.Event` or `asyncio.CancelledError`; JS `AbortSignal` / `AbortController`.
- **background work:** Go goroutines + `sync.WaitGroup` / `errgroup`; Java `ExecutorService` / virtual threads; Rust `tokio::spawn` + `JoinHandle`; Python `asyncio.create_task` / `ThreadPoolExecutor`; C# `Task.Run`; JS `Promise` / `Worker`.
- **race detector:** Go `-race`; Java ThreadSanitizer (`-XX:+UseThreadSanitizer`); Rust (compile-time, `Send`/`Sync`); C# and Python have no built-in race detector, so deterministic concurrency fixtures and stress runs carry more weight.

This list is illustrative, not prescriptive. Use the primitives the workspace actually uses.

## Non-determinism and flakiness

A single green run is unreliable for order-, timing-, or concurrency-sensitive
paths. When the change touches shared state, cancellation, retries, caching, or
anything sensitive to interleaving:

- when the invoking agent has command execution, run the project's race
  detector or concurrency stress mode when one exists; without command
  execution, report the race/stress check `PARTIAL`/`NOT_RUN` with the reason;
- re-run the relevant tests a bounded number of times (3 to 10 is a practical
  default) when command execution is available;
- treat a test that passes once and fails on retry as a failure to investigate,
  not a pass;
- report non-determinism explicitly with the counts and the decisive failure,
  not a silent pass.

## Anti false-positive rules

Reject a candidate unless you can show a reachable failure in the shown code under the stated contract. In particular:

- A lock acquired and released via the language's scoped or deferred cleanup (Go `defer mu.Unlock()`, Java try-with-resources equivalent, Rust RAII `Drop`, C# `lock` block, Python `with` block) runs on all exits including early return. That is correct. Only report a leak when a lock or resource is acquired and a path continues without the scoped/deferred release.
- Holding a `Mutex` across an `.await` (async) is a real bug when the requirement forbids it; a scoped lock block that ends before the await is correct. Distinguish the two.
- `errgroup.WithContext` + `g.Wait()` returning the first error, with workers taking `ctx` into I/O, is correct for cancel-siblings-on-first-error. Same for bounded worker pools with correct capture.
- Disjoint index writes into a pre-sized slice/array from concurrent workers (each writes only `out[i]`) are not data races when indices do not overlap.
- A worker pool with a bounded semaphore or `SetLimit` is correct fan-out control, not a missing bound.
- Sequential code with no stated concurrent context is not a race, even if it uses shared state. Concurrency must be stated or implied by the requirement.
- Process-per-task as a deliberate, bounded adapter for a specific external tool is not the banned default-fan-out pattern, but only when it has explicit timeouts, cancellation, an allowlist, and a documented reason for why in-process execution is insufficient. The ban is on making process spawning the concurrency model for agent tasks generally.

## Severity calibration

Label each finding with a severity consistent with the bug-audit skill:

- **Critical** - exploitable or destructive: authz bypass enabled by a race, double-charge or non-idempotent money path, data corruption under concurrency.
- **High** - serious reliability: data race with stated concurrency, deadlock blocking unrelated work, leaked worker holding a resource indefinitely, cancellation that leaves external side effects running, a stale owner whose write wins after a takeover, or a durable state that a transient condition makes unrecoverable.
- **Medium** - degraded but recoverable: lost wakeup under specific timing, retry storm under load that degrades but does not corrupt.
- **Low** - minor defect with limited blast radius.

Never invent a **Low** finding about style on otherwise correct concurrent code. Severity never gates approval; it calibrates the report.

## Report shape

When a resource catalogue and its scoped reader are available, load
`report-template` before producing the review report. Without that capability,
use the inline report shape below.

### Result

`PASS`, `BLOCK`, `PARTIAL`, or `NOT_RUN`.

### Scope

- the concurrency surface reviewed and the files/packages covered;
- the project's concurrency model and primitives discovered (or `not documented`);
- baseline and toolchain in effect.

### Checks executed

- exact command or method (with exit status): race detector, stress run, concurrency fixture, diff review;
- summarized result, not full successful output;
- the invariant or failure mode covered;
- list a check as not run only if it was required and could not be executed; do not record checks that were not required for the change (for example a race detector run when the change has no concurrent surface), since that invents a gap and muddies the result.

### Findings

- material findings with severity, or `No material issues found within the reviewed diff`.

### Remaining risk

- skipped checks, unresolved non-determinism, undetected interleavings, or `None identified within the executed scope`.

Result semantics:

- `PASS` - no concurrency defect (race, atomicity violation, deadlock, leak, cancellation gap, lost wakeup, starvation, thundering-herd, unfenced durable-state exclusion, or process-fan-out-as-default-model) was found; the architecture uses in-process concurrency by default (or a bounded adapter with explicit justification for specific external tools); tests cover load-bearing paths under the race detector or concurrency fixtures.
- `BLOCK` - a concurrency defect of any severity in the reviewed scope remains: a race, atomicity violation, deadlock, leaked worker, cancellation bug, lost wakeup, starvation, thundering-herd, unfenced durable-state exclusion, or process-fan-out-as-default-model.
- `PARTIAL` - useful findings but the race suite, stress run, or a gated runtime proof could not complete.
- `NOT_RUN` - plan only, or review could not start.

Keep the report concise. Do not paste complete successful logs.
