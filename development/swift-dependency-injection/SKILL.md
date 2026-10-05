---
name: swift-dependency-injection
description: 'Design injectable seams so Swift services can be swapped for fakes in tests. Use when a type reaches for `URLSession.shared`, `Date()`, `UUID()`, `random(in:)` or a singleton; when asked "how do I inject CloudKit / network / clock" or "should this be a singleton"; when choosing constructor vs `@Environment` / `EnvironmentKey` vs `@TaskLocal` injection; when writing the `makeApp()` composition root; when evaluating swift-dependencies or Factory. Does NOT choose the test framework or snapshot tooling (swift-testing-baseline) or the target layout that hosts the root (swiftpm-modularization).'
---

# Swift Dependency Injection

## When to invoke

- Designing a new service boundary (CloudKit, networking, clock, RNG, notifications).
- Asking "how do I make this testable", "how do I inject X", or "should I use a singleton here".
- Establishing a composition root for a new app target or module.
- Reviewing code that reaches out to global state, `URLSession.shared`, `Date()`, or `UUID()`.
- Choosing between constructor injection and SwiftUI environment injection.

## Scope

Owns how a seam is shaped and injected (protocol / struct witness / environment / task-local) and how a fake is written. Does NOT own the test framework, snapshot tooling, or where shared fake *types* live → `swift-testing-baseline` (`<Project>KitTesting`); nor the target layout that hosts the composition root → `swiftpm-modularization`.

## Inject via

Three routing decisions, front-loaded (details in the sections below):

| Situation | Inject via |
|---|---|
| Logic-heavy type (view model, service) | Constructor |
| Cross-cutting value deep in a view tree (theme, locale, flags, clock) | `@Environment` |
| Request-scoped override across an async call tree (trace id, logger) | `@TaskLocal` |
| Small, stable API surface; want partial fakes | Struct protocol witness |
| Team wants a shared, macro-driven convention | `pointfreeco/swift-dependencies` |
| Codebase already registers services in a container | `hmlongco/Factory` |

## Core principle: one composition root

All concrete implementations are wired in a single place — typically `makeApp(...)` or a `DependencyContainer` struct built in the `@main` entry point. Every layer below receives its dependencies through initialiser parameters, not by reaching up to a global. This makes the entire wiring visible in one screen of code and means tests can substitute any dependency without touching production paths.

```swift
// App entry point — the only place that knows about live implementations
@main struct MyApp: App {
    let root = makeApp()  // returns a pure value/struct carrying live deps
    var body: some Scene { ... }
}

func makeApp() -> AppRoot {
    AppRoot(
        storage: LiveStorage(),
        clock: ContinuousClock(),
        rng: SystemRandomNumberGenerator()
    )
}
```

No layer below `makeApp` imports `LiveStorage` or any other concrete type.

## Protocol-witness vs protocol-existential

Both are idiomatic Swift; the choice is a matter of callsite ergonomics:

- **Protocol existential (`any ServiceProtocol`)**: clear intent, straightforward generics. Works well for most app-layer seams. Requires the protocol to be `Sendable` if passed across actors, and the values it returns must be `Sendable` too.
- **Struct protocol witness (`struct ServiceClient { var fetch: @Sendable () async throws -> [Item] }`)**: eliminates dynamic dispatch, composes without `any`, easier to construct partial fakes. Favoured by pointfreeco/swift-dependencies. Good when a service has a small, stable API surface.

Either is fine. Pick the one that reads naturally; don't mix both styles for the same seam.

## SwiftUI environment injection

SwiftUI's `@Environment` and `EnvironmentValues` let you propagate dependencies down a view tree without threading them through every intermediate View:

```swift
// Define a key — `@Entry` (Xcode 16+, back-deploys to iOS 13) generates
// the EnvironmentKey and the get/set accessor for you.
extension EnvironmentValues {
    @Entry var storage: any StorageProtocol = NoopStorage()
}

// Inject at the root
ContentView()
    .environment(\.storage, LiveStorage())

// Consume deep in the tree — no init threading required
struct DetailView: View {
    @Environment(\.storage) var storage
}
```

**Trade-off vs constructor injection**: environment injection reduces boilerplate for deeply nested trees but makes the dependency implicit — a reader of `DetailView` must look up the environment key to understand what it needs. Constructor injection is explicit and compiler-enforced. For logic-heavy types (view-models, service objects), prefer constructor injection; reserve environment for cross-cutting concerns (theme, locale, feature flags, testable clocks).

In tests, inject the test double the same way:

```swift
DetailView()
    .environment(\.storage, FakeStorage())
```

## Test doubles: fakes over mocks

Prefer **fakes** (lightweight in-memory implementations) and **stubs** (hardcoded return values) over mock frameworks. Mocks couple tests to implementation details (call order, argument matching); fakes couple tests only to the contract.

```swift
// `save`/`loadAll` are `async throws`, so `actor` is the natural fit —
// a `struct` fake would need a mutating `save`, which the protocol's
// non-mutating `async throws` signature does not allow (it won't compile).
actor FakeStorage: StorageProtocol {
    private var items: [Item] = []
    func save(_ item: Item) async throws { items.append(item) }
    func loadAll() async throws -> [Item] { items }
}
```

**Injecting a controllable clock** eliminates time-dependent flakiness:

```swift
// Production
let clock: any Clock<Duration> = ContinuousClock()

// Test — `TestClock` is from pointfreeco/swift-clocks (add the package),
// not the standard library.
let clock = TestClock<Duration>()  // advance manually
await clock.advance(by: .seconds(5))
```

**Injecting a seeded RNG** makes random behaviour deterministic:

```swift
// SplitMix64 or any var rng: RandomNumberGenerator
var rng: any RandomNumberGenerator = SystemRandomNumberGenerator()
// In tests:
var rng: any RandomNumberGenerator = SeededGenerator(seed: 42)
```

## `@TaskLocal` overrides

`@TaskLocal` is a lightweight alternative when you need to override a dependency for the duration of an async call tree without restructuring the call sites — useful for request-scoped values like loggers, trace IDs, or feature-flag snapshots:

```swift
enum Current {
    @TaskLocal static var clock: any Clock<Duration> = ContinuousClock()
}

// In test
await Current.$clock.withValue(TestClock()) {
    await systemUnderTest.run()
}
```

Avoid `@TaskLocal` for dependencies that should be visible in the public interface of a type; reserve it for cross-cutting infrastructure that every caller in the task tree shares implicitly.

## Swift 6 concurrency rules for dependencies

- Xcode 26's new-project template defaults to `SWIFT_DEFAULT_ACTOR_ISOLATION = MainActor` (SE-0466). Under that default: (1) every unannotated in-house type and protocol is implicitly `@MainActor`, so a view-model-shaped seam no longer needs `Sendable` on its own account; (2) a seam meant to be used from a background actor (`StorageProtocol`, `AnalyticsClient`) must be declared `nonisolated` explicitly, and only then does it keep the `async` + `Sendable` rules below; (3) if the SwiftPM target doesn't opt into this default (existing targets default to `nonisolated`), the rules below apply as written.
- Any type passed across actor boundaries — including a dependency — must conform to `Sendable`. When the implementation is an actor wrapping a non-`Sendable` framework type it doesn't own (`AVAssetTrack`, `VNRequest`), the fix is at the boundary, not on the protocol: return a `Sendable` value type instead of the framework object, or `@preconcurrency import` the framework. Do not drop the protocol's `Sendable` requirement — it does not silence the diagnostic (see `swift6-concurrency`).
- Protocol requirements that are called from concurrent contexts must be `async` (or the protocol itself must be `@MainActor`-isolated).
- Closures stored in a struct client must be `@Sendable`:

```swift
struct AnalyticsClient: Sendable {
    var track: @Sendable (Event) async -> Void
}
```

- Avoid global `var` singletons with mutable state; they require either an `actor` wrapper or `@unchecked Sendable` with manual synchronisation. Neither is free.
- For third-party dependencies that predate Swift 6 strict concurrency, use `@preconcurrency import ThirdPartyKit` at the import site to suppress errors during transition; file an issue or switch packages if the lag is long-lived.

## Library options

- **`pointfreeco/swift-dependencies`** (MIT, currently 1.17.x) — implements the struct-witness / environment / `@TaskLocal` pattern described above. `@Dependency` is a regular property wrapper, not a macro; the macro is `@DependencyClient` / `@DependencyEndpoint` from the `DependenciesMacros` target and generates `unimplemented` defaults for a struct client. Provides `withDependencies { ... }` for scoped test overrides. Worth adopting when the team wants a shared convention rather than hand-rolling keys.
- **`hmlongco/Factory`** (MIT, by Michael Long, currently 3.x) — registration-based container closer to traditional IoC. Factory 3 ships its API under the `FactoryKit` module (`import FactoryKit`, not `import Factory`). Useful when the codebase already organises dependencies as registered services rather than value-type structs. Its README notes that the `@Injected` property-wrapper family is currently unusable from a `nonisolated` service class under a global `MainActor` default (Swift 6.2); use the `dependency(\.key)` function call instead in that case.

Both are valid; they solve the same problem with different ergonomics. Evaluate against the existing codebase shape before adding a new dependency.

## Verification checklist

- No layer below the composition root imports a concrete implementation type (`Live*`, `URLSession.shared`, `Date()`, `UUID()`).
- All protocol types (or struct clients) used across actor boundaries declare `Sendable` — no exceptions; a non-`Sendable` framework type is handled at the boundary instead (see `swift6-concurrency`).
- Async protocol requirements are `async throws`; synchronous fakes return immediately (no `Task.sleep` in a fake).
- Each test constructs its own fake/stub — no shared mutable test state at module level.
- The composition root (`makeApp(...)`) is the only call site that knows about live implementations.
- A controllable clock / seeded RNG is injected wherever production code calls `Date()`, `UUID()`, or `random(in:)`.

## Related skills

- `swiftpm-modularization`: put each seam (protocol + fake) in its own target so test targets can import the fake without importing the live implementation.
- `swift6-concurrency`: `Sendable` requirements, `@preconcurrency`, and actor-isolated types that affect dependency design.
- `swift-testing-baseline`: shared fake targets (`<Project>KitTesting`), protocol injection for CloudKit / Game Center, and why integration tests never touch real networks.
- Official sources: when verifying or updating a factual or version-sensitive claim, read `references/official-docs.md`.
