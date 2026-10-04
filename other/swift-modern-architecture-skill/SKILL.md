---
name: Swift Modern Architecture Skill
description: Use when designing new or intentionally modernized SwiftUI app architecture targeting Swift 6 with strict concurrency and iOS/iPadOS 18 or macOS 15, especially Observation ownership, dependency boundaries, SwiftData, structured concurrency, navigation state, and test seams. Do not use for arbitrary Swift questions, older deployment targets, UIKit-only work, or migrations where the existing Core Data, Combine, Dispatch, or XCTest design is not being reconsidered.
---

# Swift Modern Architecture Skill

Design feature boundaries for the product's actual constraints. “Modern” means safe, testable, compatible, and maintainable—not replacing supported frameworks by reflex.

## Declared baseline

- Xcode 16 or later
- Swift 6 language mode with complete strict concurrency checking
- iOS/iPadOS 18 or macOS 15
- SwiftUI, Observation, and structured concurrency for new feature code where they fit

Ask for the real targets before generating code. For iOS 17, Observation and SwiftData are available, but this package's complete examples intentionally use the iOS 18 baseline. For older deployments, retain supported compatibility paths. OS 27-cycle APIs are beta relative to stable Xcode 26.6; include them only when explicitly requested, clearly labeled, gated with availability checks, and paired with a stable fallback.

## Activation boundary

Activate when the user asks to design or modernize an app/feature architecture under the baseline above. Do not activate merely because a prompt mentions Swift, networking, persistence, concurrency, navigation, Core Data, Combine, Dispatch, or XCTest.

Before recommending a migration, establish:

1. Deployment targets and Xcode/Swift versions.
2. Existing persistence schema and migration history.
3. Cloud sync, extensions, widgets, background work, and offline requirements.
4. Team ownership, test suite, and staged-rollout constraints.
5. Which user problem the migration solves and how success will be measured.

## Technology decisions

| Concern | Good default for a new baseline app | Supported alternatives and reasons to keep them |
|---|---|---|
| UI observation | `@Observable` | `ObservableObject`/Combine for older targets, existing APIs, or publisher semantics |
| Persistence | SwiftData for a compatible model and requirements | Core Data for mature stores, established migrations, or capabilities the app already relies on; SQLite/GRDB or files when requirements fit better |
| Async work | `async`/`await`, task groups, actors | Dispatch and operation queues for C/Obj-C interop, queue-specific APIs, existing scheduling, or measured low-level needs |
| Unit tests | Swift Testing for new unit/integration tests | XCTest remains supported and is still needed for UI tests and common performance-test workflows |
| Navigation | Value-driven `NavigationStack`/`NavigationSplitView` | Existing coordinators or UIKit navigation when the app's platform/UI architecture requires them |

SwiftData can coexist with Core Data during an incremental migration. Swift Testing and XCTest can coexist in the same test target. Never present a supported framework as categorically obsolete.

## Feature boundaries

Organize by feature and dependency direction, not by one global layer for every type:

```text
App/
Features/
  Weather/
    WeatherScreen.swift
    WeatherFeature.swift
    WeatherClient.swift
Domain/
Persistence/
Networking/
```

- Views render state and send user intent.
- A feature model coordinates UI state only when the feature needs that coordination; small views do not require a view model.
- Domain logic stays independent of SwiftUI and storage frameworks where practical.
- Protocols create meaningful seams at side effects or ownership boundaries, not around every type.
- Dependencies enter through initializers or a deliberate environment composition root.

## Observation ownership and isolation

- Put UI-observed mutable models on `@MainActor` explicitly. Do not rely on a project's optional default-actor-isolation setting.
- Store a view-created `@Observable` reference in `@State` so SwiftUI owns its lifetime.
- Pass injected observable references as plain properties for reading. Create `@Bindable` locally when child UI needs bindings.
- Use `@Environment` only for intentionally subtree-scoped dependencies.
- Keep non-UI services `Sendable` or actor-isolated as their shared mutable state requires.

```swift
import Observation
import SwiftUI

@MainActor
@Observable
final class SignInFeature {
    var email = ""
    private(set) var isSubmitting = false
}

@MainActor
struct SignInScreen: View {
    @State private var feature = SignInFeature()

    var body: some View {
        @Bindable var feature = feature
        TextField("Email", text: $feature.email)
    }
}
```

See [the complete ownership example](examples/observable_ownership.swift).

## Structured concurrency and request identity

- Prefer child tasks, `async let`, and task groups when work belongs to an async operation.
- Store an unstructured `Task` only when an object truly owns work across calls; cancel it on replacement and teardown.
- After every suspension, check cancellation or current request identity before publishing results.
- Do not launch an uncancelled task from `didSet` for rapidly changing selection/search input.
- Keep UI state changes on `@MainActor`; isolate shared mutable service state with actors.
- Bound fan-out for large collections and propagate cancellation.

See [the complete latest-request-wins example](examples/weather_request_cancellation.swift).

## Persistence and errors

- Register every SwiftData model in the app's `ModelContainer`.
- Treat `ModelContext.save()` as throwing. Propagate the error or present it; never use `try?` for user data writes.
- Roll back failed edits when continuing with the same context, while recognizing that rollback affects all unsaved changes in that context.
- When a visible list is filtered or sorted, map deletion offsets through the exact displayed collection before deleting.
- Use stable model identity and test add/edit/delete failures.
- Use `VersionedSchema` and `SchemaMigrationPlan` for schema changes. An ad hoc launch-time loop is not a substitute for a migration plan.
- Test migrations from copies of every shipped schema, plus interrupted migration and sync scenarios.

See [the complete filtered-delete example](examples/todo_filtered_delete.swift) and [migration guidance](references/modern-patterns.md#migration-discipline).

## Networking and errors

- Define a small `Sendable` client protocol around the feature's need, not an unbounded generic API client.
- Validate status codes and decode typed responses in the service layer.
- Preserve cancellation errors; do not convert cancellation into a user-facing failure.
- Model idle, loading, content, empty, and failure states deliberately.
- Make retry idempotence and offline behavior explicit.
- Avoid displaying raw internal error strings when they are unstable or expose implementation details.

## Navigation

- Use stable, `Hashable` route values and value-driven destinations.
- Keep route mutation at the owning feature or scene boundary.
- Test deep links, invalid routes, restoration, compact/split transitions, and signed-out state changes.
- A coordinator remains reasonable when bridging UIKit, complex cross-feature flows, or existing navigation infrastructure.

## Testing

- Test domain rules without UI or persistence when possible.
- Inject deterministic clocks, IDs, clients, and stores at side-effect boundaries.
- Use Swift Testing for suitable new unit/integration tests; retain XCTest for existing suites, UI automation, and performance tests.
- Test cancellation and stale-response suppression, not only the success path.
- Exercise SwiftData with an isolated in-memory container and migration fixtures.

## Modernization sequence

1. Add characterization tests and field metrics.
2. Choose one bounded feature or seam.
3. Introduce compatibility adapters so old and new implementations can coexist.
4. Migrate data with a versioned, tested plan.
5. Roll out incrementally with rollback criteria.
6. Remove the old path only after usage and correctness evidence supports it.

Do not combine persistence, observation, navigation, networking, and test-framework migrations into one unreviewable rewrite.

## Package map

- [Quick start](docs/QUICK_START.md)
- [Balanced impact comparison](docs/IMPACT_COMPARISON.md)
- [Pattern reference](references/modern-patterns.md)
- [Failure patterns](references/anti-patterns.md)
- [Complete examples](references/examples.md)
- [Documentation index](docs/INDEX.md)
