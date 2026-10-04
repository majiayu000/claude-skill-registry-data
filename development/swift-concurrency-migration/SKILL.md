---
name: swift-concurrency-migration
description: Plan, implement, debug, and verify migrations from callback-, delegate-, Dispatch-, or permissive-concurrency Swift code to Swift 6 strict concurrency, including target-specific build settings, approachable concurrency, default actor isolation, @concurrent work, actors, Sendable boundaries, cancellation, and structured tasks. Use for Swift 6 compiler diagnostics, concurrency adoption plans, legacy async bridges, or migration-focused tests in Apple-platform apps and Swift packages. Do not use for general Swift syntax, performance work without a concurrency finding, framework-specific threading rules without a Swift migration, or requests that merely contain an already-correct async function.
---

# Swift Concurrency Migration

Migrate from evidence, one isolation boundary at a time. Preserve behavior before changing architecture, and keep every target buildable between migration waves.

## Inspect before editing

Determine the compiler, language mode, deployment targets, and effective settings for every affected target. Do not infer them from the newest syntax in one file.

```bash
xcodebuild -version
xcrun swiftc --version
xcodebuild -list -project App.xcodeproj
xcodebuild -showBuildSettings -project App.xcodeproj -target App \
  | rg 'SWIFT_VERSION|SWIFT_STRICT_CONCURRENCY|SWIFT_DEFAULT_ACTOR_ISOLATION|SWIFT_APPROACHABLE_CONCURRENCY|IPHONEOS_DEPLOYMENT_TARGET|MACOSX_DEPLOYMENT_TARGET'
```

For a package, inspect `// swift-tools-version`, each target's `swiftSettings`, and the resolved compiler:

```bash
swift package dump-package
swift --version
```

Record separately:

- Xcode and Swift toolchain versions.
- Swift language mode and strict-concurrency level.
- Default actor isolation and approachable-concurrency setting.
- App, extension, test, and package deployment targets.
- Existing global actors, actors, locks, queues, callbacks, and suppression annotations.

If the request is diagnostic-driven, reproduce one exact compiler message before changing code. Read [the migration and diagnostic playbook](references/migration-workflow.md) before making a multi-target plan.

## Choose the isolation model

Use these defaults deliberately:

| Code | Preferred ownership | Reason |
|---|---|---|
| UI and UI-observed mutable state | `@MainActor` | Keep presentation state in one domain |
| Independent shared mutable subsystem | Custom `actor` | Serialize its state without a manual queue |
| Immutable values crossing domains | `Sendable` struct or enum | Make the boundary explicit and reviewable |
| CPU-heavy async operation that must leave the caller's actor | `@concurrent` | State the execution intent explicitly |
| General library operation whose caller chooses isolation | `nonisolated` where appropriate | Avoid imposing an app-specific actor |

Swift 6.2 approachable concurrency and main-actor default isolation can reduce annotations in app targets. Do not enable main-actor default isolation blindly in reusable library targets. Change one target at a time and capture the before/after effective settings.

`async` does not mean background. It permits suspension; actor isolation determines where synchronous portions execute. A main-actor-isolated async function still performs its synchronous CPU work on the main actor. Use `@concurrent` only with a Swift 6.2-or-newer toolchain and only for work that genuinely must run on the concurrent executor.

## Migrate in controlled waves

1. Establish a clean behavioral baseline and representative tests.
2. Enable warnings or complete checking for one leaf target.
3. Make boundary values `Sendable`; avoid sending framework objects or mutable reference types.
4. Isolate UI state to `@MainActor` and cohesive mutable services to actors.
5. Replace related queue/group work with `async let` or task groups.
6. Bridge remaining callbacks and delegates at narrow edges.
7. Add cooperative cancellation and explicit task ownership.
8. Enable Swift 6 language mode only after the target is clean, then repeat for dependents.

Prefer a small number of coherent isolation domains. Do not turn every class into an actor or add `Task` merely to silence an error.

## Resolve diagnostics by cause

- For a non-Sendable capture, send an immutable snapshot, keep the object inside its actor, or redesign ownership.
- For main-actor access from a nonisolated context, decide whether the whole caller belongs on `@MainActor` or whether only a narrow update should hop there.
- For captured mutable locals, establish a `let` snapshot or move mutation behind an actor.
- For task-isolated transfer errors, stop using the value after transfer or replace shared ownership with an actor/value boundary.
- For actor reentrancy, treat state as potentially changed after every `await` and revalidate invariants.

Treat `@unchecked Sendable`, `nonisolated(unsafe)`, and `@preconcurrency` as documented, temporary bridges. Require a concrete safety argument, the narrowest possible scope, a removal condition, and a test. Never apply them in bulk.

## Preserve structured cancellation

Use `async let` for a fixed number of sibling operations and task groups for a dynamic number. Their parent scope owns completion, errors, and cancellation. Use unstructured `Task` only at synchronous-to-asynchronous lifecycle boundaries, store long-lived handles, and cancel them explicitly.

Cancellation is cooperative. Check `Task.checkCancellation()` in CPU loops, allow cancellation-aware suspension points to throw, and do not convert `CancellationError` into a user-visible failure. A timeout race must cancel the losing child.

## Bridge legacy APIs narrowly

Use a checked continuation for exactly-one callbacks and an `AsyncStream` for repeated callbacks. Cover success, failure, cancellation, and the callback-never-arrives path. Resume a continuation exactly once.

For delegates, first establish the callback's documented executor. Capture Sendable values before hopping to an actor. Use `MainActor.assumeIsolated` only when the API contract guarantees main-actor delivery; it is a runtime assertion that traps when wrong. Read [testing and legacy bridge patterns](references/testing-and-bridges.md) before changing a delegate or continuation.

## Verify each wave

Compile using the real scheme or package settings, not only an isolated snippet. Add focused strict-concurrency typechecks for dependency-free examples, but treat them as a supplement to the full build.

Test:

- success, thrown error, and cancellation;
- actor state after suspension and reentrancy;
- delegate delivery from the executors the framework can use;
- task teardown when the owning feature disappears;
- the oldest supported OS and every affected app/extension target.

Use runtime race tools as supporting evidence, never as proof that unchecked isolation is safe.

## OS 27 beta boundary

Treat all OS 27-cycle APIs as beta unless the user explicitly opts into a beta toolchain. Keep beta code in an availability-gated branch or beta-only source file, compile it with that beta SDK, and retain a stable Xcode 26 fallback. An availability check cannot make an unknown symbol compile in an older SDK. Do not replace a stable cancellation or bridging pattern with an unverified beta API.

## Resources

- [Migration workflow and diagnostic playbook](references/migration-workflow.md)
- [Testing, cancellation, and legacy bridges](references/testing-and-bridges.md)
- [Strict-concurrency example](examples/ConcurrencyMigrationExample.swift)
- [Positive and negative prompt scenarios](examples/prompts.md)
