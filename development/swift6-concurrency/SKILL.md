---
name: swift6-concurrency
description: 'Swift 6 language mode with complete concurrency checking from the first line of a new Apple-platform project; `MainActor` default isolation per the Xcode 26 template, `Sendable` only where a value crosses an isolation boundary; `@preconcurrency import` for lagging deps. Use when setting `swiftLanguageModes` / `swiftSettings` in Package.swift or SWIFT_STRICT_CONCURRENCY / default actor isolation in Xcode build settings, when a build setting or new dependency raises Sendable / isolation errors at a module boundary, or when asked "should I turn on strict concurrency". Does NOT own deployment targets → apple-platform-targets; fixing the concurrent code itself → apple-skills:guide-swift-concurrency; API reference → apple-skills:swift-concurrency.'
---

# Swift 6 / Strict Concurrency

## When to invoke

- Starting a new Swift iOS / macOS App project and deciding the language mode.
- Writing `Package.swift` and setting `swiftLanguageModes` / `SWIFT_STRICT_CONCURRENCY`.
- Adding a new third-party dependency and hitting concurrency warnings / errors.
- User asks "how do I configure Swift 6 / complete concurrency / Sendable / actor / `@preconcurrency`".

## Default decisions

- **Swift 6 language mode + complete concurrency checking**, applied from the first line of code.
- **Default actor isolation is `MainActor`**, following the Xcode 26 App project template (`SWIFT_DEFAULT_ACTOR_ISOLATION = MainActor` + `SWIFT_APPROACHABLE_CONCURRENCY = YES`; the SwiftPM equivalent is `swiftSettings: [.defaultIsolation(MainActor.self)]`, which requires `// swift-tools-version: 6.2`). Under this default an unannotated in-house type never leaves the main actor, so it does **not** need `Sendable` on its own account — `Sendable` is required only for a type that crosses into `nonisolated` code, an actor, or a module with a different isolation default. Declare it explicitly when it does (`struct Foo: Sendable` or `final class Foo: Sendable` — the latter only valid when the class is non-inheritable and every stored property is both `Sendable` and `let`; for classes with mutable state, prefer `actor Foo` or `@unchecked Sendable` with manual synchronisation).
- **Layer the isolation default per module** (see `swiftpm-modularization`): keep `MainActor` as the default for UI/App modules; Engine/Domain modules that are pure logic set `swiftSettings: [.defaultIsolation(nil)]` so they stay `nonisolated` by default and avoid needless main-actor hops. Work that must run off the main actor is marked explicitly with `@concurrent` (SE-0461) rather than left to inference.
- Protocols that cross actor boundaries (DI injection points) are declared `Sendable`, with methods `async throws`. Keep that requirement even when the implementation is an actor: the protocol's `Sendable` is not what fails when a non-`Sendable` framework type (`AVAssetTrack`, `VNRequest`) is involved — what fails is the **value crossing the boundary**:

  | Symptom | Wrong fix | Right fix |
  |---|---|---|
  | `non-Sendable type 'X' cannot be returned from actor-isolated implementation to caller of protocol requirement` | Dropping `: Sendable` from the protocol — does not silence it (verified on Swift 6.3.2, the same error appears with and without) | `@preconcurrency import` the framework whose type you don't own, or convert to a `Sendable` value type at the actor boundary and never return the framework object itself (preferred — makes the isolation real rather than asserted) |
- For third-party deps that don't support Swift 6 complete checking, in order of preference:
  1. `@preconcurrency import X` to isolate the import
  2. Switch packages
  3. Defer adoption

## Rationale

- A greenfield project has no legacy code to migrate, so the pain of complete checking gets amortised — solved once per actor / Sendable as you write — rather than as a one-shot big-bang migration later.
- Swift 6 is the long-term direction of the language; early adoption avoids technical debt.
- Complete checking catches data races at compile time, more than minimal / targeted can.

## Deviation considerations

- **Migrating existing Swift 5 code**: switch to minimal or targeted concurrency checking and upgrade in stages; ramp up one file / module at a time, allowing `@preconcurrency` during transition.
- **Significant third-party lag**: if a critical dep doesn't support it, put only the target that imports it in Swift 5 language mode (`.swiftLanguageMode(.v5)`; in Xcode, Swift 5 mode with `SWIFT_STRICT_CONCURRENCY = targeted`) and move it back to `.v6` once the dep catches up — don't drop the whole project: in Swift 6 mode strict concurrency is always `complete`, so setting `targeted` there does nothing.
- **Teaching / demo projects**: if the goal is to demonstrate older API behaviour, keeping Swift 5 mode is fine.

## Related skills

- `apple-platform-targets`: the catalog toolchain is Xcode 26; Swift 6 language mode has been available since Xcode 16, so the language-mode choice does not constrain the deployment floor.
- `swiftpm-modularization`: `swiftLanguageModes: [.v6]` sets the default for the whole package; individual targets can opt down with `swiftSettings: [.swiftLanguageMode(.v5)]` (available since swift-tools-version 6.0) — useful when migrating a legacy dependency without blocking the rest of the package.
- `apple-skills:guide-swift-concurrency` (aggregated external): fixing the concurrent code itself — actors, structured concurrency, cancellation, strict-concurrency diagnostics. This skill stops at the build settings and the dependency boundary.
- `apple-skills:swift-concurrency` (aggregated external): API reference for `async`/`await`, `Task`, `TaskGroup`, `AsyncSequence`.
- Official sources: when verifying or updating a factual or version-sensitive claim, read `references/official-docs.md`.
