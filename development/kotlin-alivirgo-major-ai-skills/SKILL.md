---
name: kotlin
description: "Write Kotlin with null-safe types, coroutines, flows, and data classes; integrate with Java and Android APIs."
category: development
risk: safe
source: self
source_type: self
date_added: "2026-08-26"
tags: ["kotlin", "coroutines", "android", "jvm", "null-safety", "claude"]
tools: ["claude", "cursor", "gemini", "codex"]
---

# Kotlin Language AI Skill Guide

## Overview & Engine Architecture

Kotlin targets JVM/Android (and multiplatform) with null-safety in the type system, concise data modeling (`data class`), and structured concurrency via coroutines. Agents prefer immutable data by default, use `suspend` functions instead of callback pyramids, cancel coroutines with scopes, and treat Java interop platform types as nullable until proven otherwise.

```
Caller scope (viewModelScope / runBlocking tests)
        |
   suspend functions
        |
  Dispatchers (Main/IO/Default)
        |
   Flow / Channel streams
```

## When to use this skill

- Writing Kotlin services or Android app logic
- Refactoring callbacks to coroutines/Flow
- Modeling domain types with sealed hierarchies
- Fixing nullability bugs at Java boundaries

## Operational directives

1. Prefer `val` and immutable collections unless mutation is required.
2. Launch coroutines in a supervised scope - never `GlobalScope` in apps.
3. Use `withContext(Dispatchers.IO)` for blocking I/O; keep CPU work on Default.
4. Model UI/domain states with `sealed class` / `sealed interface`.
5. Avoid `!!` except as a last resort with a clear invariant comment.

## Coroutines sketch

```kotlin
data class Item(val id: String, val sku: String, val qty: Int)

sealed interface ItemsState {
  data object Loading : ItemsState
  data class Ready(val items: List<Item>) : ItemsState
  data class Error(val message: String) : ItemsState
}

suspend fun loadItems(repo: ItemRepository): ItemsState =
  try {
    ItemsState.Ready(repo.fetchItems())
  } catch (e: Exception) {
    ItemsState.Error(e.message ?: "unknown error")
  }
```

## Commands

```bash
./gradlew test
kotlinc hello.kt -include-runtime -d hello.jar
# Android:
./gradlew :app:assembleDebug
```

## Common pitfalls

| Pitfall | Why it hurts | Fix |
| --- | --- | --- |
| `GlobalScope.launch` | Leaks / lost cancel | Scoped coroutines |
| Blocking Main thread | ANRs / jank | IO dispatcher |
| Ignoring Java platform types | NPEs | Explicit null checks |
| Huge `data class` copies | Hidden cost | Smaller models |

## Best practices

- Use `Result` or sealed errors for expected failures; reserve exceptions for exceptional cases.
- Prefer `Flow` for cold streams; collect with lifecycle awareness on Android.
- Enable useful compiler flags (`-Xcontext-receivers` only if team adopts them).
- Keep public APIs binary-stable for libraries (`explicit API` mode).

## Limitations

- Kotlin Multiplatform sharing has platform expect/actual complexity.
- Coroutines testing needs `runTest` and virtual time awareness.
- Spring/Java frameworks may still feel more idiomatic in Java for some teams.

## Related skills

- `@android-studio` - IDE and Gradle Android workflows
- `@spring-boot` - Kotlin on the server
- `@swift` - peer mobile language on iOS
