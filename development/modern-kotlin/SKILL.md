---
name: modern-kotlin
description: Use when writing, reviewing, or modernizing Kotlin code with recent language versions (2.0–2.4.x, including 2.4.10 and 2.4.20-Beta1), including context parameters, collection literals, guard conditions in when, multi-dollar interpolation, non-local break/continue, explicit backing fields, nested type aliases, name-based destructuring, data objects, Enum.entries, rangeUntil, unused-return-value checker, K2 smart casts, contracts, experimental -X compiler flags, exception-handling idioms (runCatching vs try/catch, Result), and stdlib APIs such as Uuid, Base64, HexFormat, kotlin.time Instant/Clock, and atomics.
---

# Modern Kotlin

Use this skill to write idiomatic Kotlin with the features added in the last four years (mid-2022 → 2026,
Kotlin 1.7 → 2.4.20-Beta1) and to know exactly which compiler flag or opt-in each preview feature needs.

State as of July 2026:

- **Latest stable: 2.4.10** (July 14, 2026). **EAP: 2.4.20-Beta1** (2.4.20 final planned September 2026).
- Default language version is 2.4. **K1 is gone**: 2.4.0 dropped `-language-version 1.9`; K2 has been the only
  compiler since 2.0.0 (May 2024).
- Context receivers (`-Xcontext-receivers`) were **removed in 2.3.20** — always migrate to context parameters.

Detailed per-version notes with full stdlib/tooling changes live in `references/` (linked at the bottom). Older
pre-2022 features (sealed interfaces, value classes, `fun interface`, Duration API, …) are in
[references/kotlin-1.4-1.6.md](references/kotlin-1.4-1.6.md).

## Release timeline

| Version | Date | Language headliners |
|---|---|---|
| 1.7.0 / 1.7.20 | Jun / Sep 2022 | K2 Alpha; builder inference, `T & Any`, opt-in stable; `..<` and `data object` previews |
| 1.8.0 / 1.8.20 | Dec 2022 / Apr 2023 | old JVM backend removed; `Enum.entries` preview, Base64/AutoCloseable experimental |
| 1.9.0 / 1.9.20 | Jul / Nov 2023 | `entries`, `data object`, `..<`, time API stable; K2 Beta; KMP stable |
| 2.0.0 / 2.0.20 | May / Aug 2024 | **K2 stable**, smart-cast upgrades; `copy()` visibility migration; `Uuid` |
| 2.1.0 / 2.1.20 | Nov 2024 / Mar 2025 | previews: guard conditions, non-local break/continue, `$$` interpolation; atomics, `Instant` |
| 2.2.0 / 2.2.20 | Jun / Sep 2025 | guards + `$$` + non-local break/continue **stable**; context parameters preview; contracts previews |
| 2.3.0 / 2.3.20 | Dec 2025 / Mar 2026 | return-value checker, explicit backing fields; name-based destructuring; context receivers removed |
| 2.4.0 | Jun 3, 2026 | **context parameters stable**, collection literals, `@IntroducedAt`; K1 dropped |
| 2.4.10 | Jul 14, 2026 | bug fixes only — current stable |
| 2.4.20-Beta1 | Jun 24, 2026 | explicit context arguments stable; `when` via invokedynamic default (JVM 21+) |

## Stable language features (no flags needed on 2.4.x)

### Context parameters — stable 2.4.0

Declare dependencies implicitly available from the calling context; parameters are named and referenced explicitly.
Replaces context receivers. Preview since 2.2.0 (`-Xcontext-parameters` needed on 2.2–2.3 only).

```kotlin
interface UserService {
    fun log(message: String)
}

context(users: UserService)
fun outputMessage(message: String) = users.log("Log: $message")

context(users: UserService)
val firstUser: String get() = users.findUserById(1)
```

Still experimental around it: explicit context arguments at call sites (`-Xexplicit-context-arguments`, stable in
2.4.20-Beta1) and callable references to context functions.
[Docs](https://kotlinlang.org/docs/context-parameters.html)

### Explicit backing fields — stable 2.4.0

Public read-only type, private mutable storage — without the `_x` naming convention. Experimental in 2.3.0 behind
`-Xexplicit-backing-fields`.

```kotlin
val city: StateFlow<String>
    field = MutableStateFlow("")

fun updateCity(newCity: String) {
    city.value = newCity // resolves to the MutableStateFlow field in private scope
}
```

[Docs](https://kotlinlang.org/docs/properties.html#explicit-backing-fields)

### Guard conditions in `when` — stable 2.2.0

Extra `if` after a branch condition (preview in 2.1.0 behind `-Xwhen-guards`):

```kotlin
when (animal) {
    is Animal.Dog -> animal.feedDog()
    is Animal.Cat if !animal.mouseHunter -> animal.feedCat()
    else -> println("Unknown animal")
}
```

### Multi-dollar string interpolation — stable 2.2.0

`$$"..."` — only `$$` interpolates; single `$` is a literal. Perfect for JSON schema, Gradle version catalogs, regex.
Preview in 2.1.0 behind `-Xmulti-dollar-interpolation`.

```kotlin
val jsonSchema = $$"""
{ "$schema": "https://json-schema.org/draft/2020-12/schema", "title": "$${title}" }
"""
```

### Non-local `break` and `continue` — stable 2.2.0

From lambdas passed to inline functions (preview in 2.1.0 behind `-Xnon-local-break-continue`):

```kotlin
for (element in elements) {
    val v = element.nullableMethod() ?: run {
        log.warning("skipping null"); continue
    }
}
```

### Data-flow-based `when` exhaustiveness — stable 2.3.0

Earlier checks and early returns count toward exhaustiveness — no redundant `else` (experimental in 2.2.20 behind
`-Xdata-flow-based-exhaustiveness`):

```kotlin
fun getPermissionLevel(role: UserRole): Int {
    if (role == UserRole.ADMIN) return 99
    return when (role) {
        UserRole.MEMBER -> 10
        UserRole.GUEST -> 1
    } // no else needed
}
```

### `return` in expression bodies — default 2.3.0

Allowed when the return type is explicit:

```kotlin
fun getDisplayNameOrDefault(userId: String?): String =
    getDisplayName(userId ?: return "default")
```

### Nested type aliases — stable 2.3.0

`typealias` inside classes/objects/functions (Beta in 2.2.0 behind `-Xnested-type-aliases`); cannot capture outer
type parameters.

### Annotation targeting — stable 2.4.0

- `@all:` meta-target applies an annotation to every applicable target of a property
  (`@all:Email val email: String`).
- New defaulting rules: an unqualified annotation propagates to `param` + `property` (or `field`), not just the
  first applicable target. Both previewed in 2.2.0 (`-Xannotation-target-all`, `-Xannotation-default-target`).

### 2.1.0 stable resolution/checks

- `@SubclassOptInRequired` — require opt-in to implement/extend an API.
- Sealed-upper-bound exhaustiveness: `fun <T : Result> render(result: T) = when (result) { ... }` without `else`.
- Generic-lambda overload resolution fixed (`store("") { 1 }` picks the lambda overload).

### K2 smart casts — 2.0.0

All default: boolean variables capturing type checks (`val isCat = animal is Cat; if (isCat) animal.purr()`),
`is A || is B` casts to the common supertype, implicit `callsInPlace` for inline functions, function-type `val`
properties, smart casts propagating into `catch`/`finally`, and correct types after `++`/`--`.

### 2022–2023 era (1.7–1.9), all stable since 1.9.0 or earlier

- **`data object`** — singleton with clean `toString()`/`equals()`/`hashCode()` for sealed hierarchies.
- **`Enum.entries`** — allocation-free `EnumEntries<E>` list replacing `values()`; `enumEntries<T>()` for reified
  generics (stable 2.0.0).
- **`..<` (rangeUntil)** — `in 0.0..<0.25` open-ended ranges, replacing `until`.
- **Definitely non-nullable `T & Any`** (1.7.0); **builder inference** without flags (1.7.0); **opt-in requirements**
  stable (1.7.0); secondary constructors with bodies in value classes (1.9.0); `data class` + Java records interop.

## Experimental and preview features (flag required on 2.4.10)

Full flag index with platform flags: [references/experimental-flags.md](references/experimental-flags.md).

### Collection literals — `-Xcollection-literals` (2.4.0)

```kotlin
val shapes: MutableList<String> = ["triangle", "square", "circle"]
val fruit = ["apple", "banana"] // List<String> by default

class Row(vararg val elements: Double) {
    companion object { operator fun of(vararg elements: Double) = Row(*elements) }
}
```

Type comes from the expected type; custom types opt in with `operator fun of`. Cannot construct Java collection
types. KEEP-0416.

### Explicit context arguments — `-Xexplicit-context-arguments` (2.4.0; stable in 2.4.20-Beta1)

`sendNotification(emailSender = defaultEmailSender)` — pass a context argument by name, e.g. to disambiguate
context-parameter overloads. KEEP-0448.

### Name-based destructuring — `-Xname-based-destructuring=<mode>` (2.3.20)

Modes: `only-syntax` (new syntax only), `name-mismatch` (warn on positional-name mismatch), `complete`
(parenthesized form becomes name-based). Square brackets are the new explicit positional form. Syntax-only planned
stable in 2.5.

```kotlin
(val mail = email, val name = username) = user // by name
val [username, email] = user                   // by position
```

### Unused return value checker — `-Xreturn-value-checker=check|full` (2.3.0)

Warns when a non-`Unit` result is silently discarded. `@MustUseReturnValues` scopes enforcement,
`@IgnorableReturnValue` exempts a function; suppress one call with `val _ = compute()`. In 2.4.0 the `returnsResultOf` contract
(`-Xallow-returns-result-of`) propagates the check through higher-order functions.

### Context-sensitive resolution — `-Xcontext-sensitive-resolution` (2.2.0, improved 2.3.0)

Omit the type name where it is inferable (enum entries, sealed subtypes): `when (problem) { CONNECTION -> ... }`.

### Contract extensions (2.2.20) — all with `@OptIn(ExperimentalContracts::class)`

- `-Xallow-contracts-on-more-functions` — contracts in property accessors and specific operators; generics in
  contract type assertions.
- `-Xallow-condition-implies-returns-contracts` — `(encoded != null) implies (returnsNotNull())`.
- `-Xallow-holdsin-contract` — `condition holdsIn block` for smart casts inside DSL lambdas.

### Reified types in `catch` — `-Xallow-reified-type-in-catch` (2.2.20)

`inline fun <reified E : Throwable> handle(block: () -> Unit) { try { block() } catch (e: E) { ... } }`

### Other experimental

- **Compile-time constants** — `-Xintrinsic-const-evaluation` (2.4.0): const evaluation for unsigned ops, string
  functions, enum `.name`.
- **`@IntroducedAt("1.1")`** — `@OptIn(ExperimentalVersionOverloading::class)` (2.4.0): hidden overloads for binary
  compatibility when adding optional parameters.
- **`when` via invokedynamic** — `-Xwhen-expressions=indy` (2.2.20); default for JVM target 21+ since 2.4.20-Beta1.
- **Data class `copy()` visibility** — `@ConsistentCopyVisibility` / `@ExposedCopyVisibility` /
  `-Xconsistent-data-class-copy-visibility` (2.0.20): aligns `copy()` visibility with a non-public primary
  constructor.
- **Warning management** — `-Xwarning-level=NAME:(error|warning|disabled)` (2.2.0), `-Xsuppress-warning=NAME`
  (2.1.0), `-Wextra` extra checks (2.1.0).

## Compiler and toolchain changes that affect code

- **2.2.0**: interface methods compile to JVM default methods by default; stable `-jvm-default`
  (`enable|no-compatibility|disable`) replaces `-Xjvm-default`. Gradle `kotlinOptions {}` is an error — use
  `compilerOptions {}`. REPL deprecated (`-Xrepl` to re-enable).
- **2.1.0**: JSpecify nullability violations are errors by default (`-Xnullability-annotations=strict`).
- **2.3.0**: Java 25 bytecode; `-language-version 1.8` dropped. **2.4.0**: Java 26; K1 fully removed.
- **2.3.20**: Kotlin/JVM builds run through the Build Tools API by default; JetBrains `@Unmodifiable` collections
  become read-only in Kotlin (warning → error in 2.5).
- **kapt** runs on K2 by default since 2.2.20 (opt-out deprecated).
- Machine-readable list of all compiler options: `org.jetbrains.kotlin:kotlin-compiler-arguments-description`.

## Modern stdlib quick map

| API | Since (experimental) | Stable |
|---|---|---|
| `kotlin.uuid.Uuid` | 2.0.20 | 2.4.0 (V4/V7 generators still experimental) |
| `kotlin.time.Instant` / `Clock` | 2.1.20 | 2.3.0 |
| `Base64` (`kotlin.io.encoding`) | 1.8.20 | 2.2.0 |
| `HexFormat` (`toHexString()`) | 1.9.0 | 2.2.0 |
| Common atomics (`kotlin.concurrent.atomics`) + `update()` | 2.1.20 / 2.2.20 | experimental |
| `AutoCloseable` + `use` (common) | 1.8.20 | 2.0.0 |
| Time API (`TimeSource.Monotonic`, `measureTime`) | 1.3.50 | 1.9.0 |
| `Path.walk()` / `visitFileTree()` | 1.7.20 | 2.1.0 |
| `Path.copyToRecursively()` / `deleteRecursively()` | 1.8.0 | experimental |
| `isSorted()` family, `UInt.toBigInteger()` | — | 2.4.0 |
| Map fallback (`getOrPutIfMissing`) | 2.4.0 | experimental |
| `StackTraceRecoverable` | 2.4.20-Beta1 | experimental |

Deprecated to error: `toLowerCase()`/`toUpperCase()` → `lowercase()`/`uppercase()`; `appendln()` → `appendLine()`
(2.1.0).

## Idioms

### `runCatching` is not the default — reach for `try`/`catch` first

`try`/`catch` is an expression in Kotlin, so it already yields a value. `runCatching` adds nothing to
`val x = try { parse(s) } catch (e: SerializationException) { default }` and costs three things:

- **It swallows `CancellationException`.** In a coroutine that breaks structured concurrency — the body keeps
  running after `cancel()`. If you must use it there, rethrow: `runCatching { … }.onFailure { if (it is CancellationException) throw it }`.
- **It catches every `Throwable`**, including `OutOfMemoryError` and `StackOverflowError`. `catch` names the one
  type you actually handle.
- **The error type leaves the signature.** `Result<T>` carries an opaque `Throwable`; nothing makes the caller
  discriminate it. Expected domain outcomes belong in a sealed hierarchy, not in `Result`.

It earns its place only when the failure has to outlive the block: `urls.map { runCatching { fetch(it) } }`,
or a function returning `Result<T>` so the caller decides. Rule of thumb — handled in the same block, `try`/`catch`;
carried out of it, `Result`.

## References

Detailed per-version descriptions, including pre-2022 history:

- [references/kotlin-2.4.md](references/kotlin-2.4.md) — 2.4.0, 2.4.10, 2.4.20-Beta1 in depth.
- [references/kotlin-2.3.md](references/kotlin-2.3.md) — 2.3.0, 2.3.20.
- [references/kotlin-2.2.md](references/kotlin-2.2.md) — 2.2.0, 2.2.20 (context parameters preview, contracts).
- [references/kotlin-2.0-2.1.md](references/kotlin-2.0-2.1.md) — K2 rollout, smart casts, 2.1 previews.
- [references/kotlin-1.7-1.9.md](references/kotlin-1.7-1.9.md) — 2022–2023: data objects, entries, rangeUntil.
- [references/kotlin-1.4-1.6.md](references/kotlin-1.4-1.6.md) — 2020–2021 history: sealed interfaces, value
  classes, `fun interface`, Duration.
- [references/experimental-flags.md](references/experimental-flags.md) — every `-X` flag and opt-in with status.

Canonical upstream: [What's new index](https://kotlinlang.org/docs/whatsnew24.html) ·
[Releases](https://kotlinlang.org/docs/releases.html) · [EAP](https://kotlinlang.org/docs/whatsnew-eap.html) ·
[Compiler options](https://kotlinlang.org/docs/compiler-reference.html) ·
[Components stability](https://kotlinlang.org/docs/components-stability.html)
