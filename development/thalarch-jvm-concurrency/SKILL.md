---
name: thalarch-jvm-concurrency
description: >
  Java/JVM concurrency and asynchronous-execution specialist. Use when code touches threads,
  executors, virtual threads, CompletableFuture, locks, atomics, shared mutable state, ThreadLocal
  or ScopedValue, Spring @Async, blocking work, cancellation, or thread-safety/performance risks.
  Requires version-aware API verification and evidence for race/deadlock/performance claims.
---

# Thalarch JVM Concurrency

Concurrency changes are correctness changes first and performance changes second.

Do not prescribe a concurrency primitive until the repository's actual JDK, framework, execution
model, and ownership boundaries are known.

## 1. Establish the execution model

Before editing, identify:

- configured JDK/runtime version;
- platform threads, virtual threads, executor pools, ForkJoin/common pool, framework-managed
  executors, reactive/event-loop execution, or mixed model;
- task owner and task lifetime;
- mutable shared state;
- cancellation/interruption contract;
- request/security/context propagation;
- blocking vs CPU-bound work;
- shutdown/resource ownership.

Verify preview/incubator/final API status against the actual JDK and current primary documentation.
Never copy a virtual-thread/structured-concurrency/ScopedValue example from another Java version
without checking the project version.

## 2. Safety invariants

For each shared state transition answer:

- Who can read it?
- Who can write it?
- What makes the operation atomic?
- What establishes visibility/happens-before?
- Can callbacks or external code execute while a lock is held?
- What ordering constraints exist between locks/resources?
- What happens when the operation runs twice, concurrently, partially, or is cancelled?

Prefer immutable ownership or message-passing/isolated state when it naturally fits the existing
architecture. Do not replace a clear synchronized design with a more exotic mechanism merely for
novelty.

## 3. Common race patterns

Actively inspect for:

- check-then-act sequences on shared state;
- compound operations performed on a thread-safe collection as separate non-atomic calls;
- lazy initialization without a safe publication mechanism;
- visibility loops waiting on non-safely-published state;
- mutable keys/equality used by concurrent maps/sets;
- read-modify-write counters without atomicity;
- listener/subscription mutation during callback dispatch;
- callback completion racing cancellation/timeout cleanup.

Use atomic collection operations (`compute*`, `putIfAbsent`, etc.) only when their callback
semantics are understood. Avoid calling unknown/recursive map operations from compute callbacks
without checking implementation guarantees.

## 4. Locks and deadlocks

Map lock acquisition order for code that can hold more than one lock.

Review:

- consistent ordering;
- external I/O or callbacks while locked;
- lock scope that is larger than the protected invariant;
- `Lock` release on all paths;
- blocking while holding a lock;
- lock inversion through helper methods/callbacks;
- starvation/fairness requirements.

A deadlock concern is a finding only when a credible wait cycle or violated ordering contract can
be shown.

## 5. Executors and task lifetime

Every executor/task needs an owner.

Check:

- bounded vs intentionally unbounded submission;
- queue/backpressure/rejection behavior;
- shutdown/close lifecycle;
- thread naming/observability if the project relies on it;
- error propagation from fire-and-forget work;
- timeout/cancellation propagation;
- blocking work placed on an event-loop or unsuitable shared pool;
- CPU-bound work oversubscribed by excessive concurrency.

Do not assume “more threads” is faster.

## 6. CompletableFuture / async chains

Trace both success and failure paths.

Check:

- which executor each stage uses;
- whether returned futures are observed/awaited;
- exception wrapping/propagation;
- timeout semantics;
- cancellation behavior;
- context propagation;
- accidental sequential behavior from immediate joins/gets;
- shared mutation from multiple completion stages.

Do not add fallback values that convert a real failure into false success unless the API contract
explicitly defines that behavior.

## 7. Virtual threads and modern JVM features

Virtual threads can be excellent for high-concurrency blocking I/O on supported JDKs, but they are
not a universal upgrade.

Before adopting them:

- verify the exact JDK and framework compatibility;
- identify whether the workload is I/O-bound;
- inspect thread-local/context assumptions;
- inspect synchronization/native/library behavior relevant to that JDK;
- measure throughput, latency, memory, and downstream saturation;
- preserve external rate limits/backpressure.

For structured concurrency, ScopedValue, or other evolving APIs, current primary documentation and
the project's preview flags are mandatory evidence.

## 8. Spring / proxy-managed async

When Spring or another proxy/interceptor framework is actually present, verify its exact version
and interception model.

Review:

- whether the annotated method is interceptable;
- self-invocation/proxy bypass;
- configured executor behavior;
- exception handling for void/fire-and-forget methods;
- security/request/context propagation;
- transaction boundaries across async calls.

Do not introduce self-injection as a reflex; follow the repository's existing architecture and
framework-recommended pattern for the proven version.

## 9. Testing concurrency

Prefer deterministic coordination over sleeps.

Use project-appropriate tools such as barriers/latches, controlled executors, virtual/test clocks,
repeat/stress tests, race detectors where available, thread dumps, JFR, or workload traces.

For a concurrency regression test:

1. state the interleaving/invariant being tested;
2. coordinate that interleaving deliberately when possible;
3. fail on the broken invariant rather than on timing alone;
4. repeat/stress only as supplementary evidence.

A test that passes once under timing luck is not proof of thread safety.

## 10. Performance evidence

For claims about concurrency performance, combine with `thalarch-performance`.

Measure the same workload before/after and inspect secondary effects:

- downstream saturation;
- queueing;
- contention;
- context switching;
- allocation/GC;
- tail latency;
- cancellation cleanup.

## Review output

For every material issue or change state:

- invariant at risk;
- concrete interleaving/failure path;
- exact code location;
- JDK/framework assumption and evidence;
- minimal remediation;
- verification command/scenario;
- remaining `UNVERIFIED` runtime assumptions.
