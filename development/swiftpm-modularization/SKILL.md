---
name: swiftpm-modularization
description: 'Default module shape for Apple-platform Swift Apps — one Swift Package, multiple targets, a thin App target (`@main` + DI root), CloudKit / GameKit / StoreKit imports confined to service targets, one test target per production target. Use when laying out targets in Package.swift, deciding where a new module or framework import lives, planning core portability (Swift on Android), when `.xcassets` go missing in a package target, or when asked "single package or multi-package". Does NOT own `platforms:` → apple-platform-targets, `swiftLanguageModes` → swift6-concurrency, or the test framework → swift-testing-baseline.'
---

# SwiftPM Modularization

## When to invoke

- Starting a new Swift App project and deciding how to split modules.
- Writing the first version of `Package.swift`.
- Wanting to reserve the option of shipping core logic to Android / cross-platform later.
- Introducing CloudKit / GameKit / StoreKit and deciding the import scope.
- User asks "single Package or multiple", "should the App target be thin", "how do I wire DI".

## Default decisions

### Single Package + multiple targets

- **Put all modules in one Swift Package**, splitting by target (named e.g. `<Project>Kit`).
- Don't start with multiple Packages — they only add `Package.swift` maintenance cost and CI resolution time.

### Very thin App target

- The App target only contains:
  - `@main`, the `App` struct
  - `Info.plist`, entitlements
  - Assets / Asset Catalog
  - A single DI composition root (wiring protocols to concrete implementations)
- All views, logic, and Storage live in the Package.
- The App target has no unit tests — keep it free of logic so nothing there needs one; end-to-end launch tests live in `host-driven-xcuitest-e2e`. All testable logic is in the Package.

### Dependencies flow upward, never downward

```
Core (pure Swift, no Apple frameworks)
   ↑
Domain (business logic / state)
   ↑
Service modules (CloudKit / GameKit / Storage / Telemetry)
   ↑
UI module (SwiftUI)
   ↑
App target
```

### Restricted Apple framework imports

- `CloudKit` is imported only in its designated service target.
- Same for `GameKit` / `StoreKit`.
- The UI and logic layers consume these **via injected protocols**, never importing the framework directly.
- This is the precondition for "core ports to Android / Linux" (Swift on Android can consume pure Swift modules directly).

### One test target per production target

- Each production target has a matching test target named `<Module>Tests`.
- Shared fakes / stubs can be factored into a separate `<Project>KitTesting` target imported by multiple test targets.

## Rationale

- Single Package: the App's modules have no need for external publication, so multi-Package's marginal cost outweighs the benefit.
- Thin App target: SwiftUI previews can run straight from the Package, yielding the fastest preview iteration loop.
- Restricted framework imports: enables unit testing, keeps previews free of permission dialogs, and preserves the portability path.
- One-to-one test targets: dependencies are clear, and CI can run only the modules that matter (paired with selective testing tooling).

## Deviation considerations

- **A module needs to be published externally**: upgrade to multi-Package; usually defer until the need is real.
- **A third-party dep is so heavy it harms build time**: pin it inside a single target and fan out from logic layers.
- **Sharing across multiple Apps**: extract into a standalone repo Swift Package.

## Example shape

```
<Project>/
├── App/                          # thin shell
│   ├── <Project>App.swift        # @main + DI composition root
│   └── (Assets, Info.plist, entitlements)
└── Packages/
    └── <Project>Kit/
        ├── Package.swift
        └── Sources/
            ├── <Core>/           # pure Swift, no Apple frameworks
            ├── <Domain>/         # domain logic
            ├── <Storage>/        # service module (CloudKit import restricted here)
            ├── <Telemetry>/      # Logger / Tracking facade
            └── <UI>/             # SwiftUI Views
        └── Tests/
            └── <Module>Tests/    # one-to-one
```

## Common footguns

### Pin parity across sibling apps (multi-app monorepos only)

- Without a committed `Package.resolved`, `swift package resolve` resolves to the newest version each dependency's range allows — it does not consult a sibling app's committed pins. Running it to "materialize" a fresh `Package.resolved` for a second app silently drifts its pins away from the first app's committed versions.
- To give app B pin-parity with app A: **copy** A's committed `Package.resolved` to B and swap only the `originHash` (obtained from one throwaway resolve on B), preserving the file's JSON formatting; then verify `swift build` leaves the file byte-identical (no churn). Diff the **full** pin list against the reference, not just the one dependency a task happened to mention. Optionally run `swift package resolve --force-resolved-versions` to check the copied pins still satisfy B's manifest — that flag does not update `originHash`, so it doesn't replace the swap.

### Renaming a target or test directory

- `swift build` plus an import-site `grep` are not sufficient verification for a target/test-directory rename. Non-Swift tooling — CI workflow files, task runners, code-gen scripts — often hard-code the **path string**, which compiles fine and passes the import grep but breaks at the tooling layer.
- Before pushing a rename, grep the repo's CI / task-runner / code-gen config for the old path string and run any gate that reads those paths locally to confirm it still resolves.

### `.xcassets` inside a package target

- `swift test` does not compile a package target's `.xcassets` at all — asset-catalog resources
  are silently invisible to the plain SwiftPM test runner.
- Adding a SwiftPM build-tool plugin to compile the catalog yourself then collides with Xcode's
  own `LinkAssetCatalog` step when the package is consumed from an Xcode project: both produce
  `Assets.car` for the same target, giving `Multiple commands produce …Assets.car`.
- The common guard of checking for a `/SourcePackages/plugins/` path does not reliably tell you
  whether the build is happening under Xcode — don't rely on it to skip the plugin conditionally.
- Keep asset catalogs in the App target; have package UI code read colors/images through injected tokens or `Bundle.module` resources that are not `.xcassets`.

## Related skills

- `swift6-concurrency`: Package applies `swiftLanguageModes: [.v6]` in one place. `swift-tools-version: 6.2` is the shared gate for both `platforms: [.iOS(.v26), ...]` (`apple-platform-targets`) and `swiftSettings: [.defaultIsolation(...)]` (`swift6-concurrency`) — 6.0/6.1 reject both.
- `apple-platform-targets`: Package `platforms:` aligned with App target.
- `swift-testing-baseline`: test target framework and location.
- `telemetry-facade-pattern`: why `Telemetry` is a standalone target.
- Official sources: when verifying or updating a factual or version-sensitive claim, read `references/official-docs.md`.
