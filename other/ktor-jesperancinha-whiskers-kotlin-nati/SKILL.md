---
name: ktor
description: Conventions for Ktor Gradle modules
---

## 1. Keep the Kotlin Gradle plugin new enough to support the configured JVM toolchain

`compileKotlin` and `compileJava` must target the same JVM bytecode version. When a module sets:

```kotlin
kotlin {
    jvmToolchain(25)
}
```

Gradle applies toolchain `25` to both tasks, but the Kotlin compiler silently caps `compileKotlin` to
the highest JVM target *it* supports, which lags behind the JDK's own release cadence. An old
`kotlin("jvm")` plugin version (e.g. `2.1.21`) paired with a new toolchain (e.g. `25`) produces:

```
❌ Inconsistent JVM Target Compatibility Between Java and Kotlin Tasks
Inconsistent JVM-target compatibility detected for tasks 'compileJava' (25) and 'compileKotlin' (23).
```

Fix by bumping the Kotlin Gradle plugin version in `plugins { kotlin("jvm") version "..." }` to a
release that supports the toolchain's JVM target, rather than lowering the toolchain. Match the
Kotlin version already used by other modules in the repo that target the same JVM (e.g.
`online-product-shop` uses `2.3.0` with `JavaLanguageVersion.of(25)`).

### Checklist

[] `kotlin("jvm")` plugin version supports the JVM version set by `jvmToolchain(...)` / `JavaLanguageVersion.of(...)`
[] `./gradlew compileKotlin compileJava` succeeds with no "Inconsistent JVM Target Compatibility" error
