---
name: kotlin-expert
description: House rules and load-bearing patterns for Kotlin 2.x / K2 / KMP. Covers K2 compiler migration (what breaks), Kotlin 2.x features (context parameters, explicit backing fields, multi-dollar interpolation, guard conditions, non-local break/continue, name-based destructuring), KMP (expect/actual, source sets, pitfalls), and house naming rules. **Does not** re-teach coroutines, scope functions, delegation, inline/reified, sealed types, value classes, contracts, type system, null safety, collections, operators, DSLs, testing, or Gradle — those are well-documented. Android UI patterns live in android-expert. Use when writing or reviewing any Kotlin 2.x code.
---

# Kotlin Expert

Opinion and house-rule reference for **Kotlin 2.x / K2 / KMP**. **Assumes baseline Kotlin knowledge** -- only what's house-specific, load-bearing, or new enough that training data is unreliable.

Non-negotiable defaults:
- **Kotlin 2.1+ with K2 compiler.** All new projects use K2. Existing projects must migrate.
- Every class `internal` unless part of public API. Minimize visibility.
- Full type annotations on public API. Inferred types for locals and private members only.
- `data class` for value types, `data object` for singletons in sealed hierarchies, `object` for stateless utilities.
- `sealed interface` over `sealed class` unless you need shared state. Exhaustive `when` -- no `else` on sealed types.
- One class/interface per file. Filename matches top-level declaration.
- No abbreviations: `connection` not `conn`, `certificate` not `cert`. camelCase acronyms: `updateMfa()` not `updateMFA()`.
- Singular package nouns: `adapter` not `adapters`. No `Impl` suffix: `PostgresDriver` not `DriverImpl`.

---

## 1. K2 compiler -- what breaks

```kotlin
// K2 is default in Kotlin 2.0+ -- remove obsolete flags:
// languageVersion = "2.0"       // already default
// freeCompilerArgs += "-Xuse-k2" // removed
```

- **Smarter type inference** -- narrows types more aggressively. May resolve to a different overload. Audit overloaded functions.
- **Stricter synthetic property resolution** -- Java getter/setter ambiguity resolves differently. `getFoo()` vs `foo` may pick different overload.
- **Builder inference** -- `buildList { }` / `buildMap { }` infer from all usages, not just the first. May need explicit type params.
- **`@JvmStatic` visibility** -- `private` companion member via `@JvmStatic` is now a compile error.
- **Smart casts survive** through contracts, lambdas, and property access (K1 pessimistically widened). Adopt immediately.
- **Annotation target resolution** -- K2 is stricter about annotation use-site targets. `@get:JvmName` may need explicit target where K1 inferred it.
- **SAM conversion precedence** -- when both SAM conversion and overloaded function match, K2 may pick differently. Explicit lambda typing resolves ambiguity.
- **Deprecation enforcement** -- K2 enforces `@Deprecated(level = ERROR)` more consistently. Previously-silenced deprecations may become compile errors.
- **Companion `invoke`** -- `MyClass()` that previously resolved to companion `invoke` may now resolve to constructor. Disambiguate with `MyClass.invoke()` or rename.

---

## 2. Kotlin 2.x features

### 2.1 Context parameters (2.2+, replacing context receivers)

```kotlin
// Old (deprecated): context(Logger, Transaction)
context(logger: Logger, transaction: Transaction)
fun transferFunds(from: Account, to: Account, amount: Long) {
    logger.info("Transferring $amount")    // by parameter name, NOT `this`
    transaction.execute { from.debit(amount); to.credit(amount) }
}
```

- Access by name, not `this`. Cannot have two context params of the same type.
- Context params propagate to callees that require the same context -- no explicit passing needed.
- Prefer context params for cross-cutting concerns (logging, transactions, auth). Use regular params for business data.
- Enable with `-Xcontext-parameters` compiler flag until stabilized.

### 2.2 Explicit backing fields (2.1+)

```kotlin
class Counter {
    val count: Int
        field = 0              // explicit backing field with initializer
        get() = field
    var name: String = ""
        set(value) { require(value.isNotBlank()); field = value.trim() }
}
```

Replaces the `_backing` + public getter pattern.

### 2.3 Multi-dollar string interpolation (2.1+)

```kotlin
val regex = $$"^\d+$$variable\d+$"   // $$ interpolates, bare $ is literal
val template = $$"""
    Dear $$name,
    Your balance is $100.00.         // no escaping needed
"""
```

### 2.4 Guard conditions in when (2.1+)

```kotlin
fun classify(response: Response) = when (response) {
    is Success if response.data.isEmpty() -> "empty"   // smart-cast in guard
    is Success                             -> "ok"
    is Error if response.code == 404       -> "not found"
    is Error if response.code in 500..599  -> "server error"
    is Error                               -> "client error"
}
```

### 2.5 Non-local break/continue in inline lambdas (2.1+)

```kotlin
for (file in files) {
    file.readLines().forEach { line ->
        if (line.startsWith("#")) continue    // outer for loop
        if (line == "END") break              // outer for loop
        process(line)
    }
}
// Only works with inline lambdas. Non-inline cannot use non-local break/continue.
```

### 2.6 Name-based destructuring (2.2+)

```kotlin
data class User(val name: String, val age: Int, val email: String)
val (email, name) = user   // matches by NAME, not position
// BREAKING CHANGE for existing positional destructuring. Audit all sites.
// Use underscore _ for unused components to avoid name collisions.
```

---

## 3. KMP patterns

### 3.1 Source set hierarchy

```
commonMain/           -- pure Kotlin, no platform APIs (default target)
androidMain/          -- Context, Lifecycle, etc.
iosMain/              -- UIKit, Foundation, Darwin
jvmMain/              -- JVM desktop
```

- Start in `commonMain`. Move to platform source set only when you must.
- No `expect` without a clear platform boundary. Intermediate source sets (`nativeMain`, `appleMain`) share cross-platform code.

### 3.2 Expect/actual

```kotlin
// commonMain
expect class PlatformFile(path: String) {
    fun readText(): String
    fun exists(): Boolean
}
// androidMain
actual class PlatformFile actual constructor(private val path: String) {
    actual fun readText(): String = java.io.File(path).readText()
    actual fun exists(): Boolean = java.io.File(path).exists()
}
```

Prefer `expect fun` for single functions. Consider `interface` + DI over expect/actual for complex implementations.

### 3.3 Common pitfalls

- `kotlinx.datetime` not `java.time` in common code. `kotlinx.io` not `java.io`.
- Ktor `HttpClient` needs per-platform engine. Declare engine in platform source sets, inject client.
- `Dispatchers.IO` is JVM/Android only. Use `Dispatchers.Default` or inject dispatcher in common code.
- `kotlinx.serialization` not Gson/Moshi (JVM-only).
- `expect`/`actual` with default parameter values: defaults only on `expect` declaration, not on `actual`.
- `actual typealias` cannot add members -- use `actual class` when the platform type doesn't match 1:1.
- Coroutine test dispatchers (`StandardTestDispatcher`, `UnconfinedTestDispatcher`) must be injected via constructor in common code -- never hard-code `Dispatchers.Main` in shared modules.

---

## 4. House build rules

- **`build-logic/` included build, not `buildSrc`** -- buildSrc invalidates entire build cache on change.
- Version catalogs (`gradle/libs.versions.toml`) for all dependency versions. Convention plugins for shared config.
- `jvmToolchain(21)` pins JDK. `allWarningsAsErrors = true` for all modules.
- `./gradlew spotlessApply` before every commit. CI runs `spotlessCheck`.
- KMP: declare platform engine dependencies in platform source sets, not common.

---

## 5. Anti-pattern catalog

House-specific and 2.x-related anti-patterns only. Well-known anti-patterns (GlobalScope, CancellationException swallowing, !! chains, platform type propagation) are omitted.

| # | Anti-pattern | Correct approach |
|---|---|---|
| 1 | `object Foo : SealedType` | `data object Foo : SealedType` |
| 2 | `sealed class` when no shared state | `sealed interface` |
| 3 | `else` on sealed type `when` | Omit -- let compiler enforce exhaustiveness |
| 4 | `SharingStarted.Eagerly` | `WhileSubscribed(5_000)` unless truly app-scoped |
| 5 | `updateMFA()` / `toJSON()` | `updateMfa()` / `toJson()` -- camelCase acronyms |
| 6 | `package com.example.validators` | `validator` -- singular nouns |
| 7 | `DriverImpl` / `ServiceImpl` | `PostgresDriver` / `HttpService` |
| 8 | Raw strings for closed sets | Enum or sealed interface |
| 9 | `data class` for entities with identity | Regular class with `equals`/`hashCode` on ID |
| 10 | `Dispatchers.IO` in common KMP code | Inject dispatcher or use `Dispatchers.Default` |
| 11 | `java.time` / Gson / Moshi in KMP | `kotlinx.datetime` / `kotlinx.serialization` |
| 12 | Positional destructuring in 2.2+ | Audit all sites -- name-based destructuring changes order semantics |
| 13 | `context(Logger, Transaction)` receiver syntax | `context(logger: Logger, transaction: Transaction)` parameter syntax |
| 14 | `-Xuse-k2` / `languageVersion = "2.0"` flags | Remove -- K2 is default in 2.0+ |
| 15 | Mutable collection in public API | `List<T>`, `Map<K,V>`, `Set<T>` -- immutable interface |
| 16 | `runBlocking` in production | `suspend fun` or `coroutineScope { }` |
| 17 | `var` accumulation in functional chains | `fold` / `buildList` / `buildMap` |
| 18 | `companion object { const val }` for config | Top-level `const val` or typed config object |
| 19 | `buildSrc` for convention plugins | `build-logic/` included build -- buildSrc invalidates entire build cache |
| 20 | Version strings in `build.gradle.kts` | Version catalogs (`gradle/libs.versions.toml`) |
| 21 | Inline function with large body | Only inline small HOFs and reified generics |
| 22 | `?.let { }` for simple null checks | `if (x != null)` -- smart cast in scope |
