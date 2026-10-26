---
name: kotlin
description: Use when writing Kotlin on the JVM with Gradle — command-line tools with clikt, data classes and sealed hierarchies, fair rotation or scheduling algorithms, kotlin.test or JUnit 5, and runnable distributions. Also use when Gradle Kotlin DSL configuration fails, or when choosing between clikt, kotlinx-cli and a plain main function.
---

# Kotlin (JVM)

Default: current Kotlin with the Gradle wrapper and Kotlin DSL, JVM toolchain pinned, `clikt` for CLIs, `kotlin.test` on JUnit 5, `application` plugin.

## Setup

1. `gradle init --type kotlin-application --dsl kotlin`; commit the wrapper.
2. `kotlin { jvmToolchain(21) }` so the JDK is chosen by the build, not by the machine.
3. `allWarningsAsErrors = true` in `compilerOptions`.

## CLI with clikt

```kotlin
class Rotate : CliktCommand() {
    private val members by option("--member").multiple(required = true)
    private val weeks by option().int().default(4)
    override fun run() = echo(plan(members, weeks).render())
}
fun main(args: Array<String>) = Rotate().main(args)
```

Keep `run()` thin; `plan(...)` is a pure function you test directly. (Check the clikt version you use: recent major versions changed how help text is declared.)

## Example: fair task rotation

- Give each task a weight (effort) and keep a history of who did what.
- Assign each slot to the person with the lowest accumulated weight who is available, breaking ties deterministically (e.g. least recently assigned, then name).
- Report the resulting totals per person and the maximum difference; that number is the fairness metric to test against.
- Never use unseeded randomness for tie-breaking — the same input must give the same plan.

## Language habits

- `data class` for values, `sealed interface` for closed variants with exhaustive `when`.
- Prefer `val` and immutable collections (`listOf`, `buildList`); expose `List`, not `MutableList`.
- Use `require`/`check` for preconditions with messages.
- Nullable types are part of the signature; avoid `!!` outside tests.

## Testing

- `kotlin.test` assertions with JUnit 5; parameterised tests for tables of members, weights and history.
- Test the invariant (max difference ≤ largest single weight) rather than one exact schedule when several are equally fair.

## Verification loop

1. `./gradlew build` — compiles with warnings as errors and runs tests.
2. `./gradlew run --args="--member a --member b"`.
3. `./gradlew installDist` and run the generated script.

## Pitfalls

- **Platform types from Java APIs** (`String!`) bypass null checks; annotate or check at the boundary.
- **`==` vs `===`:** `==` is `equals`, `===` is identity.
- **Data class `copy`** is shallow; nested mutable objects are shared.
- **Gradle Kotlin DSL** errors surface at configuration time; run `./gradlew help` to see them quickly.
- **Kotlin and Gradle plugin versions** must be compatible; upgrade them together.
