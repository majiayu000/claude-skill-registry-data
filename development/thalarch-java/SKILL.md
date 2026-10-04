---
name: thalarch-java
description: >
  Project-version-aware Java/JVM engineering for production code, libraries, services, and
  enterprise applications. Use for Java source, Maven/Gradle JVM projects, Spring when actually
  present, concurrency, JVM performance, testing, persistence, or Java-specific refactoring.
---

# Thalarch Java

Use the Java version and ecosystem the repository actually declares. Never assume the
latest language level, Spring, GraalVM, Lombok, or any other framework is available.

## Preflight

Determine from the repository:

- Java toolchain/source/target/release level;
- Maven vs Gradle and wrapper availability;
- framework and library versions;
- test framework and configured quality tools;
- module boundaries and generated-code directories.

Prefer `./mvnw` / `mvnw.cmd` or `./gradlew` / `gradlew.bat` when provided.

## Language discipline

Use features only when supported by the configured language level.

Prefer, when they clarify the model:

- records for immutable data carriers;
- sealed hierarchies for closed domain variants;
- pattern matching and switch expressions when supported;
- generics that preserve type information rather than raw types/casts;
- try-with-resources for owned closeable resources;
- immutable collections/value objects at boundaries where mutation is not required.

Do not convert every loop to a stream. Streams are preferable when they make a
transformation pipeline clearer; imperative code is often better for early exits, complex
state machines, mutation-heavy hot paths, or debugging-sensitive control flow.

Use `Optional` intentionally. Do not introduce it mechanically into fields, parameters,
or serialization models when the existing framework/contracts use another nullability model.

## Exceptions and resources

- Catch the most specific useful exception.
- Preserve causal chains when translating exceptions.
- Do not log and rethrow the same failure at every layer.
- Do not swallow interruption/cancellation semantics.
- Close resources deterministically.
- Preserve transactional boundaries and rollback behavior.

## Concurrency

First identify the repository/runtime model: platform threads, executors, virtual threads,
reactive streams, coroutines via interop, or framework-managed execution.

For concurrent changes, explicitly review:

- ownership and lifetime;
- mutable shared state;
- atomicity and visibility;
- cancellation/interruption;
- blocking calls inside event-loop/reactive execution;
- executor saturation/backpressure;
- lock ordering and deadlock risk.

Virtual threads are not an automatic optimization. Use them only when supported by the
configured JDK and appropriate for the workload/framework. Measure behavior instead of
assuming improved throughput.

## Spring and enterprise frameworks

Only activate framework-specific reasoning when the dependency graph proves the framework
is present.

For Spring-family projects, inspect actual versions and conventions before changing:

- bean lifecycle/scope;
- MVC vs reactive execution;
- transaction boundaries;
- persistence/session loading;
- security filters and authorization;
- configuration binding;
- observability/Actuator;
- native-image constraints when relevant.

Do not migrate between MVC/reactive, JPA/another persistence stack, or annotation/config
styles as incidental cleanup.

## Persistence

When JPA/Hibernate or another ORM is present, check:

- N+1 queries and fetch boundaries;
- transaction scope;
- lazy-loading behavior outside sessions;
- equality/hash semantics for entities/value objects;
- optimistic/pessimistic locking where concurrency matters;
- migration compatibility and data safety.

## Testing

Use the framework already configured. Typical evidence may include:

- focused JUnit tests;
- parameterized tests for boundary matrices;
- integration tests for Spring/DB/container boundaries;
- Testcontainers only when already present or explicitly justified;
- contract tests for externally visible APIs;
- JMH only for performance hypotheses that require microbenchmarking.

A mocked repository call does not prove persistence integration.

## JVM performance

Profile before tuning. Depending on available tooling, use project/runtime evidence such as
JFR/JMC, async-profiler, allocation/GC data, application metrics, or a reproducible benchmark.

Review:

- allocation churn;
- boxing/copying in hot paths;
- unbounded collections/caches;
- blocking/thread contention;
- GC pressure;
- classpath/startup/native-image tradeoffs.

Do not tune GC flags or heap settings without workload evidence.

## Verification

Run repository-native commands. Typical layers are compile → targeted test → broader test →
static analysis/build, but discover exact tasks from the project.

Final Java claims must name the configured JDK/toolchain used for verification.
