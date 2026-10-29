---
name: tca-ios
description: >-
  Build, review, modernize, or diagnose iOS 16+ applications that use modern
  Point-Free Composable Architecture (TCA 1.25+) or sibling libraries:
  ComposableArchitecture, Dependencies, SwiftNavigation, Sharing, Perception,
  CasePaths, IdentifiedCollections, CustomDump, SQLiteData, StructuredQueries,
  SnapshotTesting, MacroTesting, IssueReporting. Use whenever the user mentions
  TCA, Composable Architecture, @Reducer, @ObservableState, StoreOf, TestStore,
  @Dependency, StackState, Destination enums, @Shared, @FetchAll, @Table,
  @Column, @CasePathable, WithPerceptionTracking, WithViewStore (legacy
  removal), ReducerProtocol (legacy removal), is working on an iOS app that
  imports any of those modules, or asks whether TCA is the right architecture
  for an iOS project.
---

# TCA iOS

## Posture

For new guidance, target modern TCA 1.25+ and account for live 2.0-prep deprecation traits. Verify the project’s installed version before recommending APIs. Treat older APIs as migration inputs, not current patterns. Prioritize product correctness, clear state ownership, testability, and maintainability; make broad rewrites only with the user’s authorization.

## Mode banner

At the top of every response that invokes this skill, declare exactly one active mode:

`**Mode: tca-ios/build**`

Choose one of these banners: `**Mode: tca-ios/build**`, `**Mode: tca-ios/review**`, `**Mode: tca-ios/modernize**`, `**Mode: tca-ios/diagnose**`, or `**Mode: tca-ios/decide**`.

## Route the request

Use `build` by default when the request triggers this skill without choosing a mode.

- **Build:** For feature implementation, load `references/core/modern-tca-anatomy.md`, `references/core/state-shape.md`, `references/core/action-vocabulary.md`, `references/core/naming-conventions.md`, `references/core/reducer-composition.md`, `references/core/view-integration.md`, `references/effects/effect-run.md`, `references/effects/dependencies.md`, and `references/testing/teststore-basics.md`. Also load navigation, persistence, or app-architecture guides for touched areas.
- **Review:** For a review, audit, health check, or idiom question, load `references/review/coordinator.md`, `references/review/survey.md`, `references/review/finding-format.md`, `references/review/synthesis.md`, the focused review agents for the code, and relevant technical guides from `references/index.md`.
- **Modernize:** For migration, upgrade, legacy API removal, Swift 6 adoption, or 2.0 preparation, load `references/modernize/version-probe.md`, `references/version-ledger.md`, and a migration recipe for each detected API.
- **Diagnose:** For a failure, warning, leak, re-render storm, TestStore diff, cancellation or dismissal bug, Sendable warning, or database tracing problem, load `references/version-ledger.md`, the matching guide from `references/index.md`, and relevant guides under `effects`, `testing`, `navigation`, `ui`, or `persistence`.
- **Decide:** For whether to use or adopt TCA, an architecture recommendation, or a comparison with MVVM, `@Observable`, or SwiftUI `@State`, make no edits. Load `references/app-architecture/observable-vs-tca.md` and `references/app-architecture/adoption-fit.md`.

When a prompt spans modes, choose the mode for the current response, state which mode the next turn should use, and identify remaining work. Before changing modes, write a transition line, for example:

`Switching from tca-ios/review to tca-ios/diagnose: user requested a fix for finding N.`

## Check the installed generation

Before changing or judging code:

1. Find the `swift-composable-architecture` version in `Package.swift`, `Package.resolved`, `.xcodeproj/project.pbxproj`, Tuist manifests, XcodeGen specs, or local package pins.
2. Classify the code from its API markers:
   - **Modern:** `@Reducer`, `@ObservableState`, `StoreOf<Feature>`, direct store observation, `@Dependency`, `Effect.run`, `@Presents`.
   - **Transitional:** `@Reducer` mixed with `ViewStore`, `@PresentationState`, Combine schedulers, or older navigation helpers.
   - **Legacy:** `ReducerProtocol`, top-level `reduce(into:)`, `Reducer.combine`, Environment structs, `WithViewStore`, `IfLetStore`, `ForEachStore`, `SwitchStore`, `NavigationStackStore`, `Effect.task`, or `Effect.publisher`.
3. When version or API generation matters, load `references/version-ledger.md`. Load `references/index.md` to select optional or supporting references.
4. Leave stable legacy code in place unless the user requests modernization or an old API creates a concrete risk.

## Mode contracts

- **Build** may edit files and should add feature tests alongside feature code. Match local style and keep edits to the requested feature.
- **Review** is read-only. Use `references/review/finding-format.md` for severity, confidence, files, evidence, rationale, fix, and test. Report supported findings and prefer incremental fixes.
- **Modernize** probes the version through `references/modernize/version-probe.md`, then follows the relevant recipes incrementally. Tie each migration to risk reduction or compatibility.
- **Diagnose** starts from the reported symptom. Inspect or reproduce the smallest failing surface, then make one narrow fix in the files implicated by the diagnosis.
- **Decide** makes no code edits. Ground the recommendation in the two app-architecture guides and favor the least ceremony that fits the product and team.

## Design guidance

- Name reducers after the feature, such as `Settings`; name actions after user events or system results, such as `saveButtonTapped`, `searchResponse(Result<...>)`, and `delegate(.saved)`. Use delegate actions for child-to-parent communication.
- Keep state authoritative. Represent impossible combinations with enums, optional presentation state, or precise domain types.
- For modern code, use `@Reducer`, `@ObservableState`, `StoreOf<Feature>`, direct store observation, `@Bindable`, and `BindingReducer`. New code should use these APIs instead of `WithViewStore`, `ViewStore`, `IfLetStore`, `ForEachStore`, `SwitchStore`, `NavigationStackStore`, `ReducerProtocol`, old closure reducers, or top-level `reduce(into:)` reducers.
- Declare `@Dependency` properties directly in reducers. In `@Observable` classes, use `@ObservationIgnored @Dependency`. Control dates, UUIDs, clocks, randomness, network and file clients, analytics, notifications, and database clients through dependencies. Make live implementations `Sendable`; define deliberate test and preview values.
- Prefer `Effect.run` with async/await. Assign cancellation IDs to repeatable effects, including search, refresh, polling, subscriptions, and sheet-owned streams. Give each effect a lifecycle and cancel effects owned by dismissed features.
- Model child collections with `IdentifiedArrayOf<Child.State>` and `IdentifiedActionOf<Child>`. Use `@Presents` with `Destination` enum reducers for tree navigation, and `StackState` with `StackActionOf` for stack navigation.
- Where the ecosystem expects case-path access, pair `@CasePathable` with `@dynamicMemberLookup`. Use `@Shared` for shared or persisted values when they represent a real shared source of truth.
- For SQLiteData, call `bootstrapDatabase` from `prepareDependencies` in the app entry point.
- On iOS 16, wrap view bodies and lazy SwiftUI closures in `WithPerceptionTracking`; iOS 17 uses native Observation.
- In tests, prefer `expectDifference` for mutations: it identifies changed fields while comparing complete before-and-after values. Compare full values rather than transformations. Use a non-exhaustive `TestStore` when exhaustive assertions would mirror implementation noise.

## Architecture decision

TCA fits multi-screen flows, shared domain state, effect-heavy logic, deep links, cancellation needs, or teams that value reducer-level tests. Prefer SwiftUI state or an `@Observable` model for a small utility, isolated screens, mostly local UI state, or a team that will not maintain TCA conventions. For organization-level tradeoffs, use `references/app-architecture/adoption-fit.md`.

## Reference map

- `references/core/`: feature anatomy, naming, state, actions, reducer composition, views, and case paths.
- `references/effects/`: dependencies, effect lifecycles, cancellation, clocks, Sendable, and issue reporting.
- `references/navigation/`: destination enums, stacks, sheets, deep links, dismissal, global routers, and UIKit navigation.
- `references/testing/`: TestStore, dependency overrides, cancellation, navigation, shared state, custom dump, snapshots, and macros.
- `references/persistence/`: Sharing, SQLiteData, StructuredQueries, iCloud, and migrations.
- `references/app-architecture/`: app root, session, tabs, modules, Package.swift, Xcode integration, and adoption fit.
- `references/ui/`: SwiftUI idioms, observable models, and UIKit interop.
- `references/back-deploy/`: Perception support for iOS 16 deployments.
- `references/review/`: review coordinator and focused review-agent prompts.
- `references/modernize/`: migration recipes.
- `references/diagnose/`: symptom-to-cause-to-fix guides.
- `references/index.md`: mode routing and supporting-reference maps.
- `references/version-ledger.md`: TCA API generations and migration checkpoints.
