---
name: kotlin
description: Kotlin language skill covering null safety, coroutines, data classes, extension functions, and KMP. Use when building Kotlin applications.
trigger: kotlin, kt, kotlinx, kotlin coroutines, kotlin flows, ktor, kotlin multiplatform, kotlin compose
---

## kotlin

### Core Concepts
- Null Safety: nullable types (T?), safe call (?.), Elvis operator (?:), non-null assertion (!!), smart casts
- Data Classes: auto-generate equals/hashCode/toString/copy/componentN from primary constructor
- Extension Functions: add methods to existing types without inheritance, receiver parameter syntax
- Sealed Classes: restricted class hierarchies, exhaustive when branches, sum type pattern

### Coroutines & Flows
- Coroutines: suspend functions, launch/async builders, structured concurrency via scope
- Flows: cold asynchronous streams, terminal operators (collect/toList), intermediate (map/filter)
- Channels: hot streams for producer-consumer, rendezvous/buffered, ticker channels
- Dispatchers: Main (UI), IO (disk/network), Default (CPU), Unconfined (inherited)

### Multiplatform & Compose
- KMP: shared business logic across JVM, JS, Native; expect/actual for platform declarations
- Compose Multiplatform: declarative UI framework, @Composable functions, state hoisting
- kotlinx.serialization: @Serializable annotation, JSON/protobuf/CBOR formats, polymorphic serialization
- Build system: Kotlin DSL for Gradle, multiplatform plugin, source set hierarchy
