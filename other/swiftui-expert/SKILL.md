---
name: swiftui-expert
description: >-
  This skill should be used when SwiftUI work requires judgment about
  Observation and state ownership, view identity or lifecycle, navigation,
  app-target concurrency, persistence, Apple-platform behavior, accessibility,
  performance, or architecture. Trigger on "review this SwiftUI screen", "why
  isn't this view updating", "should this have a ViewModel", "fix this SwiftUI
  navigation", "why does this list scroll badly", "fix this main-actor warning
  in my app target", "review my Mac app", or "which persistence approach fits".
  Not for server-side Swift or routine Swift syntax. Pair it with an available
  platform validator when running-app evidence matters.
---

# SwiftUI Expert

Inspect the project before applying a default. Read its deployment targets,
Swift language mode, existing state patterns, platform targets, dependencies,
and nearby code. Look up current Apple documentation before making a
load-bearing claim about API behavior or availability.

If a missing target, isolation setting, ownership fact, deep-link/restoration
need, sync topology, offline behavior, or minimum-OS decision would materially
change the answer, ask one focused question or present conditional
recommendations.

## Opinions worth carrying

- **Use SwiftUI's data flow directly by default.** Let views compose sources of
  truth with `@State`, `@Environment`, `@Bindable`, and query wrappers. Add a
  ViewModel when it owns real orchestration: a state machine, retries,
  pagination, optimistic updates, lifecycle independent of one view, or a
  valuable test seam. Do not introduce one merely to move properties out of a
  view.
- **Own shared observable state at a clear ancestor.** App-wide
  `@Observable` instances normally originate in `App` and enter the environment.
  Keep ownership distinct from observation and binding extraction.
- **Model navigation as state when the product needs restoration, deep links,
  or independent tab histories.** Prefer typed destinations and keep one
  navigation history per independent surface. Do not force a router into a
  small linear flow that gains nothing from it.
- **Treat view identity and lifecycle as correctness concerns.** Work tied to a
  view belongs in lifecycle-aware tasks; structural changes, unstable IDs, and
  hidden side effects can recreate state or repeat work unexpectedly.
- **Use modern concurrency deliberately.** Match recommendations to the
  project's Swift mode and isolation settings. App targets often benefit from
  main-actor defaults; reusable non-UI packages often should remain
  nonisolated. Treat `@unchecked Sendable` as a synchronization claim that must
  be visible in the code.
- **Respect the platform.** A Mac app needs menus, keyboard behavior, windows,
  and AppKit bridges where SwiftUI is weak. An iOS app needs real accessibility,
  lifecycle, permission, privacy, and background-behavior review. Do not infer
  one platform's conventions from another.
- **Do not modernize for sport.** Preserve coherent working patterns on older
  deployment targets unless the current change benefits from migration.

## High-value traps

Pay special attention to state wrappers whose semantics change under
Observation, unstable identity in collections, asynchronous work launched from
rendering code, navigation state shared by unrelated tabs, persistence models
without a migration story, secrets stored in UserDefaults, inaccessible
icon-only actions, fixed typography that breaks Dynamic Type, and platform
features recommended without checking availability.

## Load details only when the request or project signals them

| Signal | Reference |
|---|---|
| State ownership, Observation, ViewModels, TCA | `references/state-and-architecture.md` |
| Routes, sheets, identity, repeated work | `references/lifecycle-and-navigation.md` |
| Actors, tasks, Sendable, isolation | `references/concurrency.md` |
| Tokens, layout, animation, platform materials | `references/visual-system.md` |
| VoiceOver, Dynamic Type, rendering cost | `references/accessibility-and-performance.md` |
| SwiftData, Core Data, SQLite, GRDB | `references/persistence.md` |
| iOS/visionOS privacy or macOS platform fit | `references/platform.md` |
| Tests, previews, logging, API availability | `references/testing-and-api.md` |

Do not load every reference for a general review. Follow evidence from the
request, project, failure report, or a consequential unknown and load only the
topics that could materially affect the answer.

When reviewing, prioritize user-visible bugs, state and lifecycle correctness,
data safety, accessibility, and platform integration over stylistic migration.
Explain the consequence of each finding and verify recommendations against the
actual target and toolchain.
