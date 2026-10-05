---
name: java-kotlin
description: Use when writing modern Java (17+) or Kotlin on the JVM. Covers records, sealed interfaces, pattern matching, coroutines, null safety, and JVM performance and memory tuning.
metadata:
  category: languages
  version: 1.0.0
  tags: [java, kotlin, jvm, coroutines, records]
---

# Java and Kotlin

## Purpose

Write JVM code that uses the modern language surface — records, sealed types, pattern matching, coroutines — instead of the 2010-era idioms most JVM codebases are still carrying.

## When to Use

- Writing or reviewing Java 17+ or Kotlin.
- Migrating a codebase off Java 8 idioms.
- Designing domain models with records and sealed interfaces.
- Introducing coroutines to replace callback or thread-pool code.
- Diagnosing JVM memory, GC, or startup problems.

## Capabilities

- Java: records, sealed interfaces, pattern matching for `switch`, virtual threads, `Optional` discipline.
- Kotlin: coroutines, structured concurrency, flows, null safety, delegation, DSL builders.
- Java/Kotlin interop, including platform-type null hazards.
- Build configuration for Gradle (Kotlin DSL) and Maven.
- JVM tuning: heap sizing, GC selection, JFR profiling.

## Inputs

- Source module, build file, and target JVM version.
- Whether the code is a library (binary compatibility matters) or an application.

## Outputs

- Modern, immutable-by-default domain types.
- Concurrency that is structured and cancellable.
- Build configuration pinned to a specific toolchain.

## Workflow

1. **Model** — Domain values as records (Java) or data classes (Kotlin). Variants as sealed interfaces.
2. **Match exhaustively** — Use pattern-matching `switch` / `when` so a new variant becomes a compile error.
3. **Structure concurrency** — Virtual threads (Java 21+) or coroutine scopes tied to a lifecycle.
4. **Guard nulls at the interop line** — Every value crossing from Java into Kotlin is a platform type; annotate or validate it.
5. **Gate** — Compile with warnings as errors; run SpotBugs/detekt and the test suite.

## Best Practices

- Never return `null` from a public API. Return `Optional`, an empty collection, or a sealed "absent" variant.
- Records are for data, not for behavior with hidden state. Keep them free of mutable references.
- In Kotlin, `!!` is a defect marker. If you cannot remove it, the type is lying.
- Never launch a coroutine in `GlobalScope`. It has no cancellation owner.
- Prefer `runCatching` only in application boundaries; libraries throw typed exceptions.
- Pin the toolchain in the build file so the JVM version is not an environment variable.

## Examples

**Sealed model with exhaustive matching (Java 21):**

```java
sealed interface Payment permits Card, Transfer, Wallet {}

record Card(String last4, YearMonth expiry) implements Payment {}
record Transfer(String iban) implements Payment {}
record Wallet(String provider, String token) implements Payment {}

static String describe(Payment payment) {
    return switch (payment) {
        case Card c      -> "Card ending %s".formatted(c.last4());
        case Transfer t  -> "Transfer to %s".formatted(t.iban());
        case Wallet w    -> "%s wallet".formatted(w.provider());
    };
}
```

**Structured concurrency in Kotlin:**

```kotlin
suspend fun loadDashboard(userId: String): Dashboard = coroutineScope {
    val profile = async { userService.profile(userId) }
    val orders  = async { orderService.recent(userId, limit = 10) }
    Dashboard(profile.await(), orders.await())
}
```

## Notes

- Virtual threads (Java 21) remove most reasons to use a reactive framework for I/O-bound work. They do not help CPU-bound work.
- `coroutineScope` propagates cancellation to children and rethrows the first failure; `supervisorScope` isolates failures. Choose deliberately.
- Kotlin's `Flow` is cold. Collecting it twice runs the producer twice — a common source of duplicated API calls.
