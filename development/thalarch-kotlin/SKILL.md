---
name: thalarch-kotlin
description: >
  Project-aware Kotlin engineering for JVM, Android, server, and multiplatform code. Use for
  Kotlin source, coroutines/Flow, Gradle Kotlin projects, Compose when present, KMP boundaries,
  testing, performance, interoperability, and Kotlin-specific refactoring.
---

# Thalarch Kotlin

Use the Kotlin version, target platforms, compiler options, and libraries declared by the
repository. Do not assume Android, Compose, KMP, coroutines, KSP, or a specific architecture.

## Preflight

Identify:

- Kotlin/compiler/plugin version;
- JVM/Android/Native/JS/multiplatform targets;
- Gradle wrapper and version catalogs;
- coroutine/serialization/Compose/KSP/KAPT usage;
- test libraries and configured lint/static-analysis tools;
- Java interoperability requirements.

Preserve the existing build model unless the task explicitly changes it.

## Idiomatic Kotlin

Prefer language features when they improve clarity rather than merely shorten code:

- null-safe operators and explicit boundary validation instead of routine `!!`;
- data/value classes for real value semantics;
- sealed types for closed state/result models;
- exhaustive `when` where it strengthens correctness;
- collection operators for clear transformations;
- sequences only when laziness materially avoids work/allocation;
- scope functions only when receiver/return semantics stay obvious.

Do not nest scope functions until ownership becomes difficult to read. Do not replace a
simple loop with a chain that hides control flow or allocates unnecessarily on a hot path.

## Coroutines and Flow

Structured concurrency is the default.

Review explicitly:

- scope owner and lifetime;
- dispatcher ownership/injection;
- cancellation propagation;
- exception supervision semantics;
- concurrent mutation/shared state;
- backpressure/buffering;
- hot vs cold stream semantics;
- replay and event-loss behavior;
- blocking work on inappropriate dispatchers.

Avoid `GlobalScope` and detached jobs unless the lifecycle is deliberately process-wide and
documented. Do not launch work from constructors/init blocks without a proven owner.

Never swallow `CancellationException`; if caught by a broad handler, rethrow it unless the
runtime/library contract requires a different explicit mechanism.

Use `async` only for genuine concurrency. An immediate `async { ... }.await()` is usually just
a suspending call with extra machinery.

For state, preserve atomic update semantics and understand whether the code needs `StateFlow`,
`SharedFlow`, Channel, or a cold Flow. Do not treat them as interchangeable.

## Android / Compose overlay

When Android or Compose is actually present, combine this skill with `thalarch-android` and
`thalarch-ui` as appropriate.

Review:

- state ownership/hoisting;
- lifecycle-aware collection;
- effect keys and cancellation;
- `remember`/`derivedStateOf` only where they provide real stability/work savings;
- lazy-list stable keys;
- snapshot state boundaries;
- unnecessary recomposition or expensive work during composition;
- semantics, touch targets, insets, adaptive layouts, localization.

Runtime UI claims require emulator/device/render evidence when possible.

## Multiplatform

For KMP projects:

- keep common code platform-neutral;
- inspect actual source-set hierarchy;
- use `expect/actual` only for true platform boundaries;
- avoid leaking Android/JVM APIs into common code;
- verify at least the affected target(s), not only the host target.

## Java interoperability

Use JVM annotations only when a Java caller/framework actually needs them. Preserve nullability,
SAM, overload, checked-exception, and binary-compatibility behavior across public boundaries.

## Testing

Use repository-native libraries. When present/appropriate:

- `runTest` for suspend/coroutine tests;
- virtual time instead of real sleeps;
- Flow assertions that prove ordering/cancellation/completion;
- Turbine only when it is already installed or justified;
- instrumentation/device tests for Android runtime behavior.

Avoid tests whose only proof is that a mocked collaborator returned the value configured in
the mock.

## Verification

Run the actual Gradle tasks/configured linters/tests for the affected module and target.
Report Kotlin/compiler/target context for any version-sensitive claim.
