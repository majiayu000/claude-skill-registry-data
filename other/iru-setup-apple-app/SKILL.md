---
name: iru-setup-apple-app
description: >-
  Scaffold a new native Apple app (iOS/iPadOS/macOS/watchOS/visionOS, Swift 6) at the repository root — a generator
  manifest (XcodeGen's `project.yml`, or Tuist's `Project.swift` + `Tuist.swift`) declaring one application target
  `<AppName>-<Platform>` (scheme of the same name) per selected platform with `MARKETING_VERSION`/
  `CURRENT_PROJECT_VERSION`, `SWIFT_STRICT_CONCURRENCY = complete`, Info.plist keys and a pinned test host; a shared
  UI-framework-free `Packages/Core` local SwiftPM package (Foundation + Observation only: `Models/`, `Services/`, plus
  `ViewModels/` for `architecture: mvvm` or `Controllers/` + a passive-view protocol for `architecture: mvc`) whose
  Swift Testing suite covers 100% of its lines; per-platform `Targets/<Platform>/{Sources,Tests,UITests}` — SwiftUI
  `App` + MVVM screen, or for the iOS/iPadOS target with `ui: uikit` a programmatic UIKit app (`AppDelegate` +
  `UIWindowSceneDelegate` with a scene manifest, `UINavigationController` root, `UIViewController` laid out in code,
  `mvc` controller core or `mvvm` with UIKit Observation tracking, `UIObservationTrackingEnabled` below iOS 26);
  a `--uitesting` launch argument and accessibility identifiers on every control; a Swift Testing unit-test target
  and an XCUITest UI-test target per platform — per the catalog's UI contract, a `.ui-quality.yml` at the root, the
  shared `Tests/Support/UIScreenshots.swift` capture helper compiled into both test targets, and a UI test that
  captures the sample screen in every left-to-right/right-to-left × light/dark cell into `.ui-screenshots/` and runs
  `performAccessibilityAudit()` at the configured level — watchOS companion-app wiring when `ios` and `watchos` are both
  selected, `.swiftlint.yml`, `.swift-format`, an optional `fastlane/Fastfile` with lanes gated by `signing`/
  `distribution`, and `sonar-project.properties` (omitted when `sonar: none`). The generated `.xcodeproj`/
  `.xcworkspace` is never committed. Invoke as `/iru-setup-apple-app`. Accepts pre-resolved inputs via `args`
  (`key: value` lines) — `app-name`, `bundle-id-prefix`, `platforms` (multi-select: `ios`, `ipados`, `macos`,
  `watchos`, `visionos` — `ipados` widens the iOS target's `TARGETED_DEVICE_FAMILY` rather than adding a target;
  tvOS is not supported), `ui` (`swiftui`/`uikit`, iOS/iPadOS target only, default `swiftui`), `architecture`
  (`mvvm`/`mvc`; `mvc` only with `uikit`), `generator` (`xcodegen`/`tuist`), `min-deployment-target`,
  `distribution` (`none`/`internal`/`store`), `signing` (`fastlane-match`/`api-key`/`none`), `license`,
  `developer-name`, `developer-email`, `organization-url`, `open-source`, `sonar` (+ `sonar-organization`/
  `sonar-project-key`/`sonar-host-url`), `visibility`, `ci`, `accessibility` (`enforce`/`report`/`off`/`none`, default
  `enforce`), `on-existing` (`ask`/`keep`/`update`/`replace`) and `mode` (`new`/`existing`) — so an orchestrating skill can supply them without re-prompting; stand-alone it asks
  `open-source` first and derives the `sonar` default from it. Announces whether it is scaffolding from scratch or
  updating; for each owned file that already exists it warns and asks Update / Keep as is / Replace / Stop (unless
  `on-existing` decides) and never overwrites hand-written source. Versions are looked up at run time with a dated
  October 2026 fallback table. Equivalent to `iru-setup-android-app`/`iru-setup-react-native-app` for the native
  Apple stack; use `iru-setup-macos-app` for a macOS-only (SwiftUI or AppKit) desktop app and
  `iru-setup-swift-library` for a pure SwiftPM library. Use whenever a new native iOS/iPadOS/macOS/watchOS/visionOS
  application needs its project manifest, testable core, tests, lint/format config and Fastlane/Sonar tooling
  bootstrapped from this house template.
model: haiku
---

# Setup Apple App

Generate a complete, buildable native Apple application scaffold — a project-generator manifest declaring one
application target per selected platform, a UI-free `Packages/Core` local package holding all testable logic, the
per-platform UI layer (SwiftUI everywhere, or programmatic UIKit for the iOS/iPadOS target), unit and UI tests,
lint/format config, an optional gated `fastlane/Fastfile` and `sonar-project.properties` — from the templates in this
skill's `reference/` files. The XcodeGen path of every template was rendered into throwaway projects and proven
against the real toolchain on 2026-10-16 (Xcode 27.1, Swift 6.4, XcodeGen 2.46.0, SwiftLint 0.65.1) — see **Known
quirks / verification notes**.

The layout is the **scaffold contract** the Swift coding and gate skills (`iru-swift-code-one-task(-group)`,
`iru-swift-test`, `iru-swift-coverage`, `iru-swift-code-quality`, `iru-swift-docc`, `iru-swift-bump-version`),
`iru-explore` (which recognizes `Targets/<Platform>/Sources/` as this skill's layout) and
`iru-setup-swift-github-workflows` rely on — Step 8's contract table lists the confirmed names, commands and paths.
`Packages/Core`'s `ViewModels/` vs `Controllers/` layout is the same contract `iru-setup-macos-app` uses
(`iru-swift-code-one-task`'s `reference/architecture.md`). Facts come from the author's docs (cited as "irurueta docs:
apps/apple/<page>.adoc"): `app-structure-and-lifecycle.adoc` (SwiftUI `App`, UIKit scene life cycle and scene
manifest, mandatory with the 27 SDK), `uikit-and-appkit-interop.adoc` (view controllers, Auto Layout, UIKit
Observation tracking, storyboards as legacy), `app-architecture.adoc` (MV vs MVVM with Observation, protocol-typed
services and test doubles), `multiplatform-projects.adoc` (destinations, separate watchOS target, `#if os`),
`ipados.adoc` (multiple scenes, device families) and `visionos.adoc` (native visionOS vs "Designed for iPad").

This skill never commits generator output: `.xcodeproj`/`.xcworkspace` are regenerated on demand (`xcodegen
generate` / `tuist generate`) and gitignored by the companion `iru-setup-swift-gitignore` skill — run it right after
this one. It never installs XcodeGen/Tuist/SwiftLint itself (`brew install xcodegen`/`tuist`/`swiftlint`, or
`mint run …`, is the user's call).

**Not supported**: tvOS — the author's docs repository has no tvOS page, so there is no grounded template; say so if
asked and suggest adding a tvOS target by hand. Mac Catalyst and "Designed for iPad/iPhone" destinations are not
generated either (native targets only).

## Reference files — read only what this run needs

| Read | When |
|---|---|
| `reference/project-templates.md` | **Always.** `project.yml` (or `Project.swift` + `Tuist.swift`), `.swiftlint.yml`, `.swift-format`, `fastlane/Fastfile`, `sonar-project.properties`. |
| `reference/core-templates.md` | **Always.** `Packages/Core` (Package.swift, DocC catalog, Models/Services, ViewModels or Controllers) and its Swift Testing tests. |
| `reference/swiftui-templates.md` | Any SwiftUI target: iOS/iPadOS with `ui: swiftui`, and every `macos`/`watchos`/`visionos` target. Also `LaunchOptions.swift` (every target). |
| `reference/uikit-templates.md` | `ui: uikit` — the iOS/iPadOS target's `AppDelegate`, `SceneDelegate`, `GreetingViewController` (mvc or mvvm), `GreetingLayout`. |
| `reference/test-templates.md` | **Always.** Per-target unit tests (per `ui`/`architecture`) and the XCUITest. |

**Conditional-marker convention used in every reference file**: a line `// >>> <condition>` (or `# >>>`,
`<!-- >>> … -->`) opens a block written only when the condition holds; the matching `<<< <condition>` closes it;
marker lines are never written. A heading suffixed `(<condition>[, <condition>])` exists only when every listed
condition holds. Conditions: `platform: iOS|macOS|watchOS|visionOS` (inside a per-platform block: which platform it is
being rendered for), `ui: swiftui|uikit`, `architecture: mvvm|mvc`, `watchos-companion` (`watchos` + `ios`/`ipados`),
`watchos-standalone` (`watchos` alone), `observation-tracking-opt-in` (= `ui: uikit` + `architecture: mvvm` + an iOS
deployment target below `26`), `swiftui-screen` (= `architecture: mvvm` or any SwiftUI target), `distribution: none|internal|store`, `sonar` (= `sonar` is not `none`), `sonar: cloud`.
`<placeholder>` values come from Step 5's table and are substituted in headings (file paths) too.

## Step 0 — Resolve inputs

Invoked stand-alone (`/iru-setup-apple-app`) or by `iru-setup-swift-repository` / the `iru-setup-repository` front
door, which pass resolved answers as `key: value` lines, e.g.:

```
app-name: My App
bundle-id-prefix: com.example
platforms: ios,ipados,watchos,visionos
ui: uikit
architecture: mvc
generator: xcodegen
min-deployment-target: 26.0
distribution: store
signing: fastlane-match
license: MIT License
developer-name: Jane Doe
developer-email: jane@example.com
organization-url: https://github.com/example-org
open-source: yes
sonar: cloud
sonar-organization: example-org-github
sonar-project-key: example-org_my-app
sonar-host-url: https://sonarcloud.io
visibility: public
ci: yes
accessibility: enforce
mode: new
```

Parse any such lines from `args` now. Every field found here is resolved — skip asking about it in Step 2. If `args`
is absent or doesn't look like this format, treat everything as unset and ask normally.

| Key | Values / default |
|---|---|
| `app-name` | display name (`CFBundleDisplayName`), e.g. `My App`; `<AppName>` (target stem, module, product, `@main` type) is its PascalCase form, e.g. `MyApp` |
| `bundle-id-prefix` | reverse-DNS, e.g. `com.example`; the app's bundle id is this plus a slugified `app-name` (`com.example.myapp`) |
| `platforms` | comma-separated subset of `ios`, `ipados`, `macos`, `watchos`, `visionos` (Step 2 explains how `ipados` combines with `ios`). `tvos` is answered with "not supported by this skill" (see intro) and dropped |
| `ui` | `swiftui` (default) / `uikit` — applies **only to the iOS/iPadOS target**; ignored (and named in the report) when neither `ios` nor `ipados` is selected |
| `architecture` | `ui: swiftui` → `mvvm` only (never asked); `ui: uikit` → `mvc` (default, recommended) or `mvvm`. `ui: swiftui` + `architecture: mvc` is rejected with Step 2's explanation. The choice shapes `Packages/Core`; with `ui: uikit` + `mvc` and SwiftUI platforms (macOS/watchOS/visionOS) also selected, Core gets both `Controllers/` and `ViewModels/` (Step 2) |
| `generator` | `xcodegen` / `tuist` — asked when unset |
| `min-deployment-target` | the iOS deployment target, e.g. `26.0` (default from Step 4); other platforms get their equivalent from Step 5's table |
| `distribution` | `none` / `internal` / `store` |
| `signing` | `fastlane-match` / `api-key` / `none` |
| `license`, `developer-name`, `developer-email`, `organization-url` | report + copyright line |
| `open-source`, `visibility`, `ci`, `sonar` (+ `sonar-organization`/`sonar-project-key`/`sonar-host-url`) | the `sonar` recommendation (Step 2); `visibility` is only used for that; `internal` behaves like `private` |
| `accessibility` | `enforce` (default) / `report` / `off` / `none` — the automated accessibility level of the UI tests, written to `.ui-quality.yml` (UI contract §8) |
| `on-existing` | `ask` (default) / `keep` / `update` / `replace` — how Step 1 treats each already-existing file |
| `mode` | `new` / `existing` |

`mode: existing` is this catalog's shared signal that this is an update rather than a from-scratch run. It **never
means a silent gap-fill**: Step 1 still warns about and asks per already-existing file (unless `on-existing` says
otherwise). `mode: new` or an unset `mode` follows the same Step 1 survey — the files on disk decide whether each one is
created or updated. Unknown keys from a full shared-args set (`publish`, `ci-tests`, `pages`, `branching`, …) are
ignored and named in the report.

**Accessibility level `none` and assistive-technology templates.** `accessibility` takes `enforce`, `report`, `off` or
`none` (UI contract §8; the stand-alone question gains a fourth option, **None — opt out entirely**, e.g. a mandated
non-compliant design). With `none`: write `accessibility: none` to `.ui-quality.yml`, do not install or configure the
accessibility test tooling (`performAccessibilityAudit()`), and omit the accessibility-specific attributes from the generated templates.
With `enforce`, `report` or `off`: include the assistive-technology attributes from the contract's §8 platform
subsections in every generated template — `accessibilityLabel`/`accessibilityHint`/traits on icon buttons and images, Dynamic Type-safe text styles, VoiceOver-friendly ordering, Reduce Motion guards — and, for `enforce`/`report` only, the automated checks. In
`mode: existing`, a prior `.ui-quality.yml` follows this skill's existing Update / Keep / Replace prompt and its
`accessibility` value is never silently flipped (**Update** sets it only when `args` supplied it).

## Step 1 — Survey the repository

Check, at the repository root, for this skill's owned files: the manifest (`project.yml`, or `Project.swift` +
`Tuist.swift`), `Packages/Core/Package.swift`, `.swiftlint.yml`, `.swift-format`, `.ui-quality.yml`,
`fastlane/Fastfile`, and `sonar-project.properties`; plus the source skeleton (`Packages/Core/Sources`/`Tests`, `Targets/*/Sources`,
`Targets/*/Tests`, `Targets/*/UITests`) and any hand-maintained `*.xcodeproj`/`*.xcworkspace`. When updating, also
read the current evidence for Step 2's defaults: app name, bundle id prefix, platforms (`Targets/<Platform>/`
folders and manifest targets), deployment targets, `ui` (`Targets/iOS/Sources/SceneDelegate.swift` /
`UIApplicationDelegate` = `uikit`; `@main struct … App` = `swiftui`) and `architecture` (`Core/ViewModels/` = `mvvm`,
`Core/Controllers/` = `mvc`; neither = an older scaffold of this skill with the flat `Greeter` placeholder). Then tell
the user, before anything else, which of these this run is:

- **Nothing exists**: "**Scaffolding the Apple app from scratch** — none of this skill's files exist yet." Skip
  straight to Step 2; every file is *created*.
- **Only a hand-maintained `.xcodeproj`/`.xcworkspace` exists, with neither `project.yml` nor `Project.swift`**:
  this isn't this skill's scaffold — it's a project that predates any generator. Warn the user explicitly and ask
  whether to adopt XcodeGen/Tuist going forward (this skill can then write a manifest describing the *existing*
  targets as a starting point, best-effort) or stop. Don't attempt to reverse-engineer the `.xcodeproj` file
  automatically — confirm the target list with the user first. The remaining owned files then follow the per-file
  rule below.
- **An `iru-setup-macos-app` layout** (`App/Sources`, one macOS target): not this skill's scaffold — warn and suggest
  `iru-setup-macos-app` instead; continue only on an explicit yes, adding files alongside, never moving any.
- **Any owned file exists**: "**Updating an existing Apple app** — found: <list of paths>." For each existing owned
  file, **warn** and resolve what to do with it. If `on-existing` is `keep`/`update`/`replace`, apply it to every
  existing file without asking (still print the warning and the list). Otherwise (`on-existing: ask` or unset —
  and regardless of `mode`), ask with `AskUserQuestion`, one question per file, batching up to four per call, with
  these consequences stated in the option descriptions:
  - **Update (Recommended)** — merge: add what's missing and correct outdated parts using the reference template
    (e.g. a missing platform target triple, the pinned `TEST_HOST`/`BUNDLE_LOADER`, the watch app's `WKApplication`
    key, a UIKit scene manifest, `SWIFT_STRICT_CONCURRENCY = complete`, a Fastfile lane now gated in by
    `signing`/`distribution`, stale `sonar.*` keys), keeping every target, scheme, build setting, lane or key this
    skill doesn't own. You review a diff before it's written; customizations survive, but a part this skill owns may
    be rewritten.
  - **Keep as is** — leave the file untouched. Nothing customized changes, but it may stay out of date or disagree
    with this run's choices — say so concretely in the question when it does (e.g. "`fastlane/Fastfile` has a
    `release` lane but you chose `distribution: internal`", "`sonar-project.properties` exists but you chose
    `sonar: none`", "`project.yml` has no visionOS target but you selected `visionos`", "`project.yml`'s test targets
    have no `TEST_HOST` — `xcodebuild test` fails with *Could not find test host*", "`.ui-quality.yml` says
    `accessibility: report` but you chose `enforce`", "`project.yml`'s UI-test targets don't compile
    `Tests/Support/UIScreenshots.swift`"); Step 8 lists each mismatch.
  - **Replace** — regenerate from the template. The result matches this house pattern exactly, but every target,
    scheme, build-setting, lane or key customization in that file is lost — recoverable only from git history. Never
    recommended by default. When the manifest is replaced, first read its current values and offer them as the
    defaults for whichever Step 2 question Step 0 didn't already resolve.
  - **Stop** — end this skill now without changing anything. Report this and end here.

  Questions about `fastlane/Fastfile`/`sonar-project.properties` whose expected content depends on Step 2's
  `signing`/`distribution`/`sonar` answers are asked after Step 2 resolves those (or now, if `args` already did).

  The source skeleton is never part of this question: whatever the decision, never touch an existing file under
  `Targets/*/Sources`, `Targets/*/Tests`, `Targets/*/UITests`, or `Packages/Core/Sources`/`Packages/Core/Tests`
  unless its content exactly matches one of this skill's templates (current or the earlier flat `Greeter`/
  `ContentView`/`<AppName>App` placeholders, or the pre-UI-contract `<AppName>UITests.swift` without the capture
  and audit tests) — such an untouched placeholder may be upgraded to the current template.
  Missing files are created: a newly selected platform's `Targets/<Platform>/…`, a missing
  `Targets/<Platform>/Tests/Support/UIScreenshots.swift` helper (the UI-test targets then need the manifest's helper
  source line — part of the manifest's Update), the `Core/Models`, `Core/Services`
  and `Core/ViewModels`|`Core/Controllers` folders (added alongside a legacy `Greeter.swift`, which is never deleted).
  A requested `architecture`/`ui` that contradicts existing hand-written sources (e.g. `Core/Controllers/` exists but
  `architecture: mvvm` was asked) is reported, not converted — switching architecture is a coding task, not a
  scaffold step. Record each file's decision; Step 6 applies it and Step 8 reports it as **created / updated /
  replaced / kept as is**.

## Step 2 — Collect the required inputs

For any field Step 0 already resolved from `args`, use that value directly and don't ask about it again. For
everything else, ask the user (plain conversation, pre-filling defaults found in Step 1 when updating):

- **app-name** — the display name, e.g. `My App` (each target's `CFBundleDisplayName`; derives `<app-slug>` for the
  bundle id, e.g. `myapp`, and `<AppName>`, e.g. `MyApp`).
- **bundle-id-prefix** — reverse-DNS, e.g. `com.example`. The iOS/iPadOS/macOS/visionOS targets' bundle id is
  `<bundle-id-prefix>.<app-slug>` (one App Store Connect record, one product per platform); the watchOS companion
  target (only when both `ios`/`ipados` and `watchos` are selected) is `<bundle-id-prefix>.<app-slug>.watchkitapp` —
  a distinct, nested id required by Apple's watch-app rules even for the modern single-target watch app this skill
  generates (irurueta docs: apps/apple/multiplatform-projects.adoc, "The separate watchOS target").
- **platforms** — bounded multi-select (`AskUserQuestion`, at least one required): `ios`, `ipados`, `macos`,
  `watchos`, `visionos`. (tvOS isn't offered — see the intro.)
  - **`ipados` is not a separate Xcode target.** Selecting it alongside `ios` widens the one iOS application
    target's `TARGETED_DEVICE_FAMILY` to `"1,2"` (iPhone + iPad) instead of `"1"`. Selecting `ipados` **without**
    `ios` produces the same iOS-platform target with `TARGETED_DEVICE_FAMILY` `"2"` (iPad only) — there is no
    separate "iPadOS" SDK/platform value. With `ui: uikit`, `ipados` also sets `UIApplicationSupportsMultipleScenes`
    to `true` (several windows on iPad; irurueta docs: apps/apple/ipados.adoc, "Opting in to multiple scenes"). Say
    this back to the user so the choice isn't misread as adding a target.
  - `macos`, `watchos` and `visionos` each produce their own, fully separate application target.
  - `visionos` is a **native** visionOS SwiftUI app (`platform: visionOS`, SDK `xros`, `TARGETED_DEVICE_FAMILY` 7), not
    the "Designed for iPad" compatibility mode an iPad app gets automatically on Apple Vision Pro (irurueta docs:
    apps/apple/visionos.adoc, "Bringing iPad and iPhone Apps to visionOS"). Its simulator runtime is a separate
    download in Xcode (Settings › Components); without it the target still builds, but its tests can't run.
  - `watchos` **without** `ios`/`ipados` produces a standalone watch app (`WKWatchOnly`, no companion wiring) — state
    this is unusual but supported.
  - `macos` together with other platforms stays a **SwiftUI** target (this skill's multi-platform shape). For a
    macOS-only app — or one that should be AppKit, sandboxed, notarized as a DMG — point the user to
    `iru-setup-macos-app` instead.
- **ui** — only when `ios` or `ipados` is selected (`AskUserQuestion`):
  - **SwiftUI (Recommended)** (`swiftui`) — one `App`/`WindowGroup` and the same SwiftUI screen on every platform;
    Apple's default for new apps.
  - **UIKit** (`uikit`) — programmatic UIKit for the iOS/iPadOS target: `AppDelegate` + `UIWindowSceneDelegate` with
    a scene manifest (mandatory from the 27 SDK — an app without the scene life cycle fails to launch), a
    `UINavigationController` root and a `UIViewController` laid out in code with Auto Layout; **no storyboards**
    (irurueta docs: apps/apple/app-structure-and-lifecycle.adoc, "Mandatory with the 27 SDK";
    apps/apple/uikit-and-appkit-interop.adoc). For teams with UIKit experience or an existing UIKit codebase.
  - Say that the **watchOS and visionOS targets stay SwiftUI** either way: watchOS has no `UIViewController`-based app
    model (WatchKit apps are SwiftUI-only today), and a native visionOS app's windows, volumes and immersive spaces
    are SwiftUI scenes — UIKit there only runs as an iPad-compatible app. A selected `macos` target stays SwiftUI too
    (AppKit lives in `iru-setup-macos-app`).
- **architecture** — only when more than one is valid:
  - `ui: swiftui` → `mvvm` without asking. Say why `mvc` isn't offered: SwiftUI has no controller layer — views are
    values driven by observable state — so screen logic lives in a per-screen `@MainActor @Observable` view model in
    `Packages/Core/Sources/Core/ViewModels/` (irurueta docs: apps/apple/app-architecture.adoc, "MV with Observation vs
    MVVM"); pick UIKit for MVC.
  - `ui: uikit` → `AskUserQuestion`: **MVC (Recommended)** (`mvc`) — Cocoa Touch's native pattern: the
    `UIViewController` owns widgets, actions and lifecycle; a UI-free `@MainActor` controller in
    `Packages/Core/Sources/Core/Controllers/` decides what to show and drives the view through a passive-view protocol,
    so the logic is unit-tested headless. **MVVM** (`mvvm`) — an `@Observable` view model in `Core/ViewModels/`; the
    view controller renders it in `viewWillLayoutSubviews()`, re-run by UIKit's automatic Observation tracking (on by
    default from iOS 26; with an iOS deployment target below 26 the scaffold adds `UIObservationTrackingEnabled` to
    Info.plist).
  - With `ui: uikit` + `mvc` and other SwiftUI platforms selected (watchOS/visionOS/macOS), `Packages/Core` gets
    **both** `Controllers/` (the UIKit screen) and `ViewModels/` (the SwiftUI screens) — say so; the coding skill
    treats that as "mixed" and follows each feature's existing pattern.
- **generator** — `xcodegen` or `tuist`, asked with a stated recommendation when unset: **XcodeGen** for a
  single-target (or single-platform-family) app — a thin, fast, single-file manifest with the smallest learning
  curve, and the path this skill verifies end to end; **Tuist** for a modular app that already has (or will grow)
  multiple internal SwiftPM packages beyond `Packages/Core`, since Tuist's module graph, caching and `tuist generate`
  workflow pay off once there's more than one internal package (its manifest here is syntax-checked only).
- **min-deployment-target** — the **iOS** deployment target (e.g. `26.0`); every other selected platform gets its
  equivalent from Step 5's table (identical numbers from 26 on under Apple's year-based versioning; `18.0` maps to
  macOS 15 / watchOS 11 / visionOS 2). Offer Step 4's looked-up default (`26.0`, the docs' baseline) as the
  recommendation; offer `18.0` as the lower option (still supported; UIKit MVVM then needs the
  `UIObservationTrackingEnabled` opt-in, and `updateProperties()`/`isInteractivelyResizing` need `#available` guards)
  and the current SDK major (e.g. `27.0`) only when a matching simulator runtime is installed. Never offer below
  `18.0`.
- **Developer name**, **developer email**, **organizationUrl** — recorded in Step 8's report and in each Info.plist's
  `NSHumanReadableCopyright`.

Then, unless Step 0 already resolved a `license` value, ask about the **license** with `AskUserQuestion`: MIT License
(recommended for app source not meant for redistribution as a library) / Apache License 2.0 / No license
(proprietary) / Other (ask for the display name and URL). If a license is chosen, remind the user in Step 8 to add a
matching root `LICENSE` file if missing — `iru-check-license` can verify/backfill source headers against it.

Then resolve `open-source`, `sonar`, `distribution`, `signing` and `accessibility` — skip any already resolved. When invoked
stand-alone with none of them pre-resolved, ask `open-source` *first* (yes/no) and derive the recommended `sonar`
default from that answer, per this catalog's shared convention:

- **open-source** — is this repository open source? Yes / No.
- **sonar** — whether to wire up a SonarQube/SonarCloud scan (`sonar-project.properties`, consumed by a CI workflow
  such as `iru-setup-swift-github-workflows`). Recommend **SonarCloud** (`cloud`) only when open-source is Yes **and**
  `visibility` is `public` (or unknown); otherwise state that SonarCloud is free only for public/open-source projects
  and recommend **None** (`none`), offering **self-hosted SonarQube** (Community Build is free, but you run the
  server) second. **When `ci: no` arrived via `args`**, say plainly that no workflow will send reports and recommend
  `none`; if the user still picks `cloud`/`self-hosted`, write `sonar-project.properties` only and note in Step 8 that
  no CI step sends reports:
  - `cloud` — ask for `sonar.organization`, offering `<owner>-github` (Step 3) as the default; default
    `sonar.projectKey` to `<owner>_<repo>` and `sonar.host.url` to `https://sonarcloud.io`, confirming both.
  - `self-hosted` — ask for `sonar.host.url`, plus `sonar.organization` only if that server has organizations
    enabled, and `sonar.projectKey`.
  - `none` — skip `sonar-project.properties` entirely.
- **distribution** — `none`/`internal`/`store`:
  - `none` — local install/manual QA only (Xcode or `xcodebuild archive`). No TestFlight/App Store lanes.
  - `internal` — TestFlight internal testing; the Fastfile gets a `beta` lane (`build_app` + `upload_to_testflight`).
  - `store` — App Store production submission; the Fastfile gets `beta` and `release` lanes; Step 8 flags the App
    Store Connect credentials this needs.
- **signing** — `fastlane-match`/`api-key`/`none`, asked with the distribution answer in view (default `none` outright
  when `distribution: none` and the user doesn't want a signed local archive — confirm rather than assume):
  - **`fastlane-match`** — team-shared certificates and profiles in an encrypted private git repo synced by
    `fastlane match`; recommended when several people/machines sign. Needs `MATCH_GIT_URL`/`MATCH_PASSWORD` CI secrets
    — this skill never creates that repo or any certificate.
  - **`api-key`** — Xcode automatic signing (`-allowProvisioningUpdates`) authenticated by an **App Store Connect API
    key**; recommended for a single maintainer or CI-only signing. Needs `APP_STORE_CONNECT_API_KEY_ID`/
    `APP_STORE_CONNECT_API_KEY_ISSUER_ID`/`APP_STORE_CONNECT_API_KEY_BASE64` secrets. This path also works with **no
    Fastlane at all** (`xcodebuild -exportArchive -authenticationKeyPath …`), which is what the macOS desktop skills do.
  - **`none`** — no automated signing; the Fastfile only gets a `test` lane. Valid with `distribution` ≠ `none` but
    unusual — warn in Step 8 that nothing here produces a distributable build automatically.

- **accessibility** — asked only when unset: "Support accessibility and assistive technologies?" — **Enforce
  (Recommended)** (`enforce`: every `performAccessibilityAudit()` issue fails the UI tests) / **Report only**
  (`report`: issues are attached and listed, never failing) / **Off** (`off`: the audit test skips; the coding
  defaults — labels, Dynamic Type, contrast — still apply). Written to `.ui-quality.yml`.

**Fastlane is an intentional difference from the macOS desktop skills, and it stays optional.**
`iru-setup-macos-app`/`iru-setup-macos-github-workflows` use plain `xcodebuild`/`notarytool`/`stapler` because the
author's docs show everything working with Xcode alone (irurueta docs:
apps/apple/macos-distribution-outside-the-app-store.adoc, apps/apple/ci-cd-xcode-cloud-and-command-line.adoc). This
skill keeps its `fastlane/Fastfile` for teams that want `match` and TestFlight lanes, but nothing in the scaffold or
in `iru-setup-swift-github-workflows` requires it: every contract command in Step 8 is plain `xcodebuild`, so the
workflows skill can build, test, archive and upload without Fastlane.

## Step 3 — Infer repository information

Don't ask for these — parse `git remote get-url origin` (`git@host:owner/repo.git` or `https://host/owner/repo.git`)
for `<owner>`/`<repo>` (Step 2's Sonar defaults). No `origin` remote → ask.

## Step 4 — Look up toolchain versions

Look every version up at run time; fall back to this table (observed together on 2026-10-16) only when a lookup fails,
and say so explicitly in Step 8.

| Component | Lookup | October 2026 fallback |
|---|---|---|
| Xcode / Swift (informational, never installed) | `xcodebuild -version`, `swift --version` | Xcode `27.1` (`27A9275`), Swift `6.4` |
| SDKs (ceiling) | `xcodebuild -showsdks` | iOS `27.1`, watchOS `27.0`, visionOS `27.0` (`xros`), macOS `27.0` |
| Installed simulator runtimes | `xcrun simctl list runtimes` | iOS `18.5`/`26.4`/`27.0`, watchOS `11.5`/`26.5`/`27.0`, **no visionOS runtime** |
| `min-deployment-target` default | `26.0` (the docs' baseline: deployment minimum 26, latest SDK) — lowered to the highest installed iOS runtime major only if no ≥ 26 runtime is installed; never higher than an installed runtime, or the scaffold's own tests can't run locally | `26.0` |
| `<xcode-version>` (XcodeGen `options.xcodeVersion`, Tuist `compatibleXcodeVersions`) | `xcodebuild -version` major.minor | `27.1` |
| XcodeGen | `https://formulae.brew.sh/api/formula/xcodegen.json` `.versions.stable`, or `gh api repos/yonaskolb/XcodeGen/releases/latest --jq .tag_name` | `2.46.0` |
| Tuist | `https://formulae.brew.sh/api/cask/tuist.json` `.version` — **not** `gh api repos/tuist/tuist/releases/latest` (monorepo tags such as `helm@…`/`server@…` come first) | `4.208.0` |
| SwiftLint | `https://formulae.brew.sh/api/formula/swiftlint.json` `.versions.stable` | `0.65.1` |
| `swift format` | bundled with the toolchain | Swift 6.4's |
| `swift-docc-plugin` (`<swift-docc-plugin-version>`) | `gh api repos/swiftlang/swift-docc-plugin/releases/latest --jq .tag_name` | `1.5.0` |
| `swift-tools-version` in `Package.swift` | the lowest that declares every `.v<N>` used: `6.2` for `.v26`/`.v27` | `6.2` |
| xcbeautify / Periphery / SwiftFormat (informational) | `formulae.brew.sh/api/formula/<name>.json` | `3.2.1` / `3.8.0` / `0.63.0` |
| Fastlane (gem) | `https://rubygems.org/api/v1/versions/fastlane/latest.json` (no install) | `2.240.1` |

The Homebrew JSON API (`formulae.brew.sh/api/formula|cask/<name>.json`) is a plain HTTPS endpoint — it works without
`brew` installed.

## Step 5 — Reference templates

Read the reference files (table above). Placeholders:

| Placeholder | Source |
|---|---|
| `<app-name>` / `<app-slug>` / `<AppName>` | Step 2 (`My App` / `myapp` / `MyApp`; PascalCase = words capitalized and concatenated, non-alphanumerics stripped) |
| `<bundle-id-prefix>` / `<bundle-id>` | Step 2 / `<bundle-id-prefix>.<app-slug>` |
| `<watch-bundle-id>` | `<bundle-id>.watchkitapp` — only for `watchos-companion` |
| `<platform-bundle-id>` | `<watch-bundle-id>` for a companion watchOS target, else `<bundle-id>` |
| `<Platform>` | `iOS` (for `ios`/`ipados`), `macOS`, `watchOS`, `visionOS` — one per selected platform |
| `<device-family>` | `"1"` (`ios`), `"2"` (`ipados`), `"1,2"` (both) |
| `<supports-multiple-scenes>` | `true` when `ipados` is selected, else `false` (UIKit scene manifest) |
| `<ios-deployment-target>` … `<visionos-deployment-target>`, `<platform-deployment-target>` | from `min-deployment-target` via the table below |
| `<ios-major>` / `<macos-major>` / `<watchos-major>` / `<visionos-major>` | integer majors of the above, for `Package.swift`'s `.v<N>` |
| `<xcode-version>` / `<swift-docc-plugin-version>` / tool versions | Step 4 |
| `<marketing-version>` / `<current-project-version>` | `1.0.0` / `1` (`iru-swift-bump-version` rewrites them later) |
| `<first-available-simulator-name>` | first device under the newest installed iOS runtime in `xcrun simctl list devices available` (a literal, resolved at scaffold time) |
| `<owner>` / `<repo>` | Step 3 |
| `<sonar-organization>` / `<sonar-project-key>` / `<sonar-host-url>` | Step 2 |
| `<developer-name>` / `<developer-email>` / `<organization-url>` | Step 2 |
| `<accessibility>` | Step 0/2 (`enforce` by default) — `.ui-quality.yml` |
| `<ScreenType>` | the sample screen's type, the UI contract `<Id>` of its captures: `GreetingViewController` (`platform: iOS`, `ui: uikit`), else `ContentView` |
| `<platform-variant>` | the capture's platform variant: `ios`, `macos`, `watchos`, `visionos` |

Per-platform deployment targets (`Packages/Core` always declares macOS too, so `swift test` runs on the host):

| iOS (`min-deployment-target`) | macOS | watchOS | visionOS |
|---|---|---|---|
| `26.0` or later (`N.0`) | `N.0` | `N.0` | `N.0` |
| `18.0` | `15.0` | `11.0` | `2.0` |

Directory layout produced (the **contract**):

```
project.yml                              XcodeGen manifest (generator: xcodegen) — or Project.swift + Tuist.swift
Packages/Core/Package.swift              library Core, test target CoreTests, swift-docc-plugin
Packages/Core/Sources/Core/Core.docc/    DocC landing page
Packages/Core/Sources/Core/Models/       Greeting
Packages/Core/Sources/Core/Services/     GreetingProviding, GreetingService, GreetingError
Packages/Core/Sources/Core/ViewModels/   mvvm (and every SwiftUI target): GreetingViewModel (@MainActor @Observable)
Packages/Core/Sources/Core/Controllers/  mvc: GreetingController (@MainActor) + GreetingView (passive-view protocol)
Packages/Core/Tests/CoreTests/           Swift Testing, 100% line coverage of Core
Targets/iOS/                             when ios and/or ipados is selected (one target either way)
  Info.plist                             generated by xcodegen from project.yml's info: block
  Sources/  swiftui: <AppName>App.swift, ContentView.swift
            uikit:   AppDelegate.swift, SceneDelegate.swift, GreetingViewController.swift, GreetingLayout.swift
            both:    LaunchOptions.swift
  Tests/    LaunchOptionsTests.swift + swiftui: <AppName>Tests.swift | uikit: GreetingViewControllerTests.swift,
            AppShellTests.swift; Support/UIScreenshots.swift (UI contract helper, also compiled into UITests)
  UITests/<AppName>UITests.swift          behaviour + screen captures (ltr/rtl × light/dark) + accessibility audit
Targets/macOS/ | Targets/watchOS/ | Targets/visionOS/   per selected platform — SwiftUI shape (App, ContentView,
                                         LaunchOptions; LaunchOptionsTests, <AppName>Tests; <AppName>UITests)
.swiftlint.yml  .swift-format
.ui-quality.yml                          UI contract settings (accessibility level, directions, themes)
fastlane/Fastfile                        optional (see Step 2)
sonar-project.properties                 sonar ≠ none
```

`Packages/Core` never imports SwiftUI, UIKit, AppKit or WatchKit. `.xcodeproj`, `build/`, `DerivedData/`, `.build/`,
`*.xcresult` and `.ui-screenshots/` are `iru-setup-swift-gitignore`'s job.

## Step 6 — Scaffold the project

Apply Step 1's per-file decision to every file below: write a file that doesn't exist yet (*created*); for an
existing one merge per **Update** (show `git diff --no-index <current> <draft>` and write on approval — *updated*),
leave it per **Keep as is**, or overwrite per **Replace** (within Step 1's source-file limit).

1. Write the manifest from `reference/project-templates.md` — `project.yml` or `Project.swift` + `Tuist.swift` —
   with one app/unit-test/UI-test triple and one scheme per selected platform, the watchOS embed/companion keys,
   `TARGETED_DEVICE_FAMILY`, the UIKit scene manifest and the `observation-tracking-opt-in` key applied.
2. Write `Packages/Core` from `reference/core-templates.md` (`ViewModels/` when `architecture: mvvm` or any SwiftUI
   target exists; `Controllers/` when `architecture: mvc`), with only the selected platforms (plus macOS) in
   `platforms:`.
3. For each selected platform, write `Targets/<Platform>/Sources` from `reference/swiftui-templates.md` (or, for the
   iOS target with `ui: uikit`, `reference/uikit-templates.md`) plus `LaunchOptions.swift`, and `Tests`/`UITests` from
   `reference/test-templates.md`.
4. Write `.swiftlint.yml`, `.swift-format` and `.ui-quality.yml` (`project-templates.md`, `accessibility` from
   Step 0/2).
5. Write `fastlane/Fastfile` with exactly the lanes `signing`/`distribution` (and the iOS/iPadOS target) gate in —
   never a lane the chosen method can't back, and no `platform :ios` lane without an iOS/iPadOS target.
6. Write `sonar-project.properties` only when `sonar` ≠ `none`, scoped to the selected platforms.
7. Remind the user that the `.xcodeproj`/`.xcworkspace` doesn't exist until `xcodegen generate` / `tuist generate`
   runs from the repository root (every clone runs it first).

## Step 7 — Verify

Run every command through the `iru-gate-runner` agent (never inline — the logs are long). macOS with a full Xcode
only; elsewhere, or with Command Line Tools only, report every step "unverified (needs macOS/Xcode)". If
`xcodegen`/`tuist`/`swiftlint` aren't installed, say so, mark their steps unverified, and never install them. Serialize
every simulator run behind `.simulator-test.lock` like the Swift gates, and shut down any simulator this run booted.

1. `cd Packages/Core && swift test --enable-code-coverage`, then `xcrun llvm-cov report
   "$(swift build --show-bin-path)/CoreTests.xctest/Contents/MacOS/CoreTests" -instr-profile
   "$(swift build --show-bin-path)/codecov/default.profdata" --ignore-filename-regex='(Tests/|DerivedSources|\.build/)'`
   — expect 100% lines.
2. `xcodegen generate` (or `tuist generate --no-open`).
3. Per selected platform, `xcodebuild test -project <AppName>.xcodeproj -scheme <AppName>-<Platform> -destination
   '<destination>' -derivedDataPath build/dd -resultBundlePath build/test-<Platform>.xcresult` (destinations in Step
   8; macOS adds `CODE_SIGN_IDENTITY=- CODE_SIGN_STYLE=Manual DEVELOPMENT_TEAM=` and needs Automation Mode for its UI
   test). Parse with `xcrun xcresulttool get test-results summary`. A platform whose simulator runtime isn't
   installed (typically visionOS) is reported **"unverified (no <platform> simulator runtime installed)"** after
   `xcodebuild build-for-testing -scheme <AppName>-<Platform> -destination 'generic/platform=<Platform> Simulator'`
   proves it compiles — never download a runtime yourself. The UI tests' captures land in `.ui-screenshots/screen/
   <ScreenType>/` (written directly from the simulator; on macOS recovered from the `.xcresult` by
   `iru-swift-test`'s `ui` run, which the verification uses: `/iru-swift-test ui` with the scheme/destination) — expect
   4 files per platform (2 on watchOS: dark only) and an accessibility audit at the `.ui-quality.yml` level.
4. `swiftlint lint --strict` and `swift format lint --strict --recursive Targets Packages/Core/Sources
   Packages/Core/Tests` from the root.

Report pass/fail per command; quote error output verbatim for a failure only.

## Step 8 — Report

Summarize: resolved `app-name`/`<AppName>`, `bundle-id-prefix`/`<bundle-id>`, `platforms` (how `ipados` combined with
`ios`; that watchOS/visionOS/macOS targets are SwiftUI), `ui` and `architecture` (and why the others weren't offered),
`min-deployment-target` and each platform's equivalent, `generator`, license, and whether the run scaffolded from
scratch, updated an existing app, or stopped. State what was included versus omitted and why: `sonar` coordinates (or
why `none`) and which platforms' paths `sonar-project.properties` lists; `distribution`/`signing` → exactly which
Fastfile lanes exist and which CI secrets each needs (this skill never collects them), and that Fastlane is optional;
which Step 4 versions were live versus fallback; the `accessibility` level written to `.ui-quality.yml`; ignored
`args` keys. Then, per file, **created / updated / replaced /
kept as is**, each mismatch of a kept file, and what a replaced one may have lost (tell the user to check `git diff`).

### Scaffold contract (confirmed by running it — downstream skills depend on these)

| What | Exact name / path / command |
|---|---|
| Project | `project.yml` → `xcodegen generate` → `<AppName>.xcodeproj` (gitignored). Per platform: targets `<AppName>-<Platform>` (app; product `<AppName>.app`, module `<AppName>`), `<AppName>Tests-<Platform>` (hosted, `TEST_HOST` pinned), `<AppName>UITests-<Platform>`; scheme `<AppName>-<Platform>` testing `CoreTests` + both test targets; local package product `Core` |
| Schemes | `<AppName>-iOS` (ios/ipados), `<AppName>-macOS`, `<AppName>-watchOS`, `<AppName>-visionOS` |
| Destinations | iOS: `platform=iOS Simulator,name=<device>` (e.g. `name=iPhone 18 Pro,OS=27.0`; add `OS=` when several runtimes have that device); watchOS: `platform=watchOS Simulator,name=Apple Watch Series 12 (46mm)`; visionOS: `platform=visionOS Simulator,name=Apple Vision Pro` (needs the visionOS runtime); macOS: `platform=macOS`; builds: `generic/platform=iOS Simulator` / `…=watchOS Simulator` / `…=visionOS Simulator`, archives `generic/platform=iOS` / `visionOS` / `watchOS` / `macOS` |
| Versions | `project.yml` `settings.base` `MARKETING_VERSION: x.y.z` (unquoted) / `CURRENT_PROJECT_VERSION: n` — `iru-swift-bump-version`'s app path. Kind = app: root has `project.yml` (or `Project.swift`) and no root `Package.swift` |
| Architecture marker | `Packages/Core/Sources/Core/ViewModels/` = MVVM; `Packages/Core/Sources/Core/Controllers/` (controller + `GreetingView` protocol) = MVC (both = mixed: UIKit MVC + SwiftUI platforms); `Targets/iOS/Sources/SceneDelegate.swift` + `AppDelegate` = UIKit, `@main struct … App` = SwiftUI; `Targets/<Platform>/Sources/` = this skill's layout |
| Core tests + coverage (the bar) | `cd Packages/Core && swift test --enable-code-coverage` → `CoreTests.xctest` + `codecov/default.profdata` under `swift build --show-bin-path`; `llvm-cov report`/`export -format=lcov` — 100% lines for every variant |
| All tests | `xcodebuild test -project <AppName>.xcodeproj -scheme <AppName>-<Platform> -destination '<destination>' -resultBundlePath <x>.xcresult` runs `CoreTests` + `<AppName>Tests-<Platform>` + `<AppName>UITests-<Platform>`; `-skip-testing:<AppName>UITests-<Platform>` for unit tests only |
| App coverage | the UI layer (`Targets/**`) is "not measured" for the bar (also `sonar.coverage.exclusions`); measure Core with `swift test` |
| Lint / format | `swiftlint lint --strict` (root; `included: Targets, Packages/Core/Sources, Packages/Core/Tests`; `reporter: json`) · `swift format lint --strict --recursive Targets Packages/Core/Sources Packages/Core/Tests` |
| UI-test hooks | launch argument `--uitesting` (last; macOS also `-ApplePersistenceIgnoreState YES` before it) → `LaunchOptions.apply()` (animations off on iOS/visionOS); identifiers `nameField`, `greetButton`, `greetingLabel`, `errorLabel` |
| UI contract | `.ui-quality.yml` (root, committed); helper `Targets/<Platform>/Tests/Support/UIScreenshots.swift` in both test targets; captures `.ui-screenshots/screen/<ScreenType>/default--<ltr\|rtl>--<light\|dark>--<platform-variant>.png` (also attached to the `.xcresult` as `screen~<ScreenType>~…`, `UI_SCREENSHOTS_DIR` passed as `TEST_RUNNER_UI_SCREENSHOTS_DIR`); audit issues attached as `a11y~<ScreenType>~<rule>` |
| UIKit specifics | Info.plist `UIApplicationSceneManifest` → `$(PRODUCT_MODULE_NAME).SceneDelegate`; `UIObservationTrackingEnabled: true` only for `mvvm` below iOS 26; no `UIMainStoryboardFile` |
| Fastlane (optional) | `fastlane test` = `<AppName>-iOS` on `<first-available-simulator-name>`; never required by the workflows |

### Known quirks / verification notes

- **Verified for real on 2026-10-16** in `$TMPDIR/iru-verify/apple/iru-setup-apple-app/{ios-swiftui-mvvm (ios+watchos),
  ios-uikit-mvc, ios-uikit-mvvm, ios-uikit-mvvm-ios18, ios+ipados+visionos-swiftui, ios+macos-swiftui-extra, ios-uikit-mvc+visionos-mixed}`
  (outside this repository) with Xcode 27.1 (27A9275), Swift 6.4, XcodeGen 2.46.0 and SwiftLint 0.65.1 (run from a
  temp download, not installed): `swift test` (7–8 Core tests, **100.00% lines/regions/functions** of Core in every
  variant), `xcodegen generate`, `xcodebuild test` on an iOS 27.0 iPhone 18 Pro simulator — ios-uikit-mvc 18/18,
  ios-uikit-mvvm 17/17, ios-swiftui-mvvm 11/11, ios+ipados+visionos 11/11, **including the XCUITest** — the watchOS
  scheme on an Apple Watch Series 12 (46mm) watchOS 27.0 simulator (11/11 incl. UI test, watch app embedded in the iOS
  app), the macOS scheme's unit tests (10/10, ad-hoc signed; the macOS UI test needs Automation Mode — see
  `iru-setup-macos-app`), `swiftlint lint --strict` (0 violations), `swift format lint --strict` (clean); the mixed UIKit-MVC + visionOS variant (both `Controllers/` and `ViewModels/`) builds for testing on both platforms with 12 Core tests at 100%.
- **visionOS**: `xcodebuild build-for-testing -scheme MyApp-visionOS -destination 'generic/platform=visionOS Simulator'`
  succeeds against the visionOS 27.0 SDK (`xrsimulator`, universal arm64/x86_64, `MinimumOSVersion` 26.0); its tests
  are **unverified (no visionOS simulator runtime installed)** — `-destination 'platform=visionOS Simulator,name=Apple
  Vision Pro'` fails with "Unable to find a device matching the provided destination specifier".
- **UIKit Observation opt-in proven**: `ios-uikit-mvvm` with `min-deployment-target: 18.0` passes 17/17 on an iOS 18.5
  simulator with `UIObservationTrackingEnabled`; the same project **without** the key fails three view-controller
  tests (the view never re-renders) — the key is required below iOS 26. The UI test passed even without it (other
  layout passes refresh the screen), so only the unit tests catch a missing opt-in. `strings` on the iOS 18.5
  runtime's UIKitCore shows the `UIObservationTrackingEnabled` key; the 27.1 SDK declares `updateProperties()` as
  `API_AVAILABLE(ios(26.0), tvos(26.0), visionos(26.0)) API_UNAVAILABLE(watchos)` — hence `viewWillLayoutSubviews()`.
- **`TEST_HOST` must be pinned** — fixed in this version: XcodeGen derives a unit-test target's `TEST_HOST` from the
  app *target* name (`<AppName>-iOS.app/<AppName>-iOS`), but `PRODUCT_NAME: <AppName>` builds `<AppName>.app`, so
  `xcodebuild test` failed with "Could not find test host for <AppName>Tests-iOS". Older scaffolds need the Update.
- **Embedded watch app needs `WKApplication: true`** — fixed in this version: without it, installing the iOS app on
  the simulator failed with "Found WatchKit 2.0 app … but it does not have a WKWatchKitApp or WKApplication key set to
  true in its Info.plist". A standalone watch app sets `WKWatchOnly: true` instead of the companion id.
- **`Packages/Core` always declares `.macOS`**: `swift test` (the coverage bar) builds for the macOS host, where
  `@Observable` needs macOS 14+; an iOS-only `platforms:` list would fall back to the old default macOS target.
- **swift-format vs SwiftLint**: swift-format wants unconditional imports (incl. `@testable import`) above any
  `#if … import` block (`OrderedImports`) and adds trailing commas that SwiftLint's `trailing_comma` rejects — that
  rule is disabled. Without `.swift-format` the formatter defaults to 2-space indentation.
- **Simulator-name ambiguity**: several runtimes ship the same device names (e.g. `iPhone 17` on 26.4 and 27.0) — add
  `OS=<version>` to the destination. The "Metadata extraction skipped, no AppIntents.framework dependency" lines in
  `xcodebuild` output are harmless.
- If the iOS Simulator destination fails with `Loaded CoreSimulatorService is no longer valid`, run
  `xcodebuild -runFirstLaunch` once.
- **Tuist**: `Project.swift`/`Tuist.swift` pass `swiftc -parse` only; `tuist generate` was not run (Tuist isn't
  available in the verification environment) — the `ProjectDescription` API calls are unconfirmed.
- **UI contract additions (2026-10-16) are only partly verified**: `UIScreenshots.swift` and the new
  `<AppName>UITests.swift` pass `swift format lint --strict` with this skill's `.swift-format` and type-check for
  iOS 18, macOS 15, watchOS 11 and visionOS 2 (`swiftc -typecheck` against the 27.x SDKs); the helper itself ran under
  `swift test` (macOS) and `xcodebuild test` on an iOS 27 simulator in a throwaway package, writing the contract files
  and recovering them from the `.xcresult`. Not run: a regenerated scaffold (no XcodeGen on that machine), so the
  manifest's extra UI-test source line, the XCUITest matrix run, `XCUIDevice.appearance`/`-AppleInterfaceStyle`
  switching, the accessibility audit on the sample screen and SwiftLint on the helper are **unverified** — run Step 7
  before trusting them.
- **Fastlane** lanes (`test`, `build`, `beta`, `release`, `sync_signing`, `connect_api_key`, `notarize_release`) are
  written, never executed; `match`, TestFlight/App Store uploads and notarization need Apple Developer Program
  credentials.

Finish with a **Warn explicitly** block:

- Review every generated file before building, committing or distributing; replace the `Greeting` sample with real
  logic and confirm the license matches a root `LICENSE` (suggest `iru-check-license`).
- Run `iru-setup-swift-gitignore` — `.xcodeproj`/`.xcworkspace`/`DerivedData`/`build/`/`.xcresult`/`xcuserdata`,
  `.ui-screenshots/` and `.simulator-test.lock/` must never be committed (`.ui-quality.yml` is); every clone runs `xcodegen generate` (or `tuist generate`) first.
- visionOS tests need the visionOS simulator runtime (Xcode › Settings › Components); this skill never downloads it.
- With `sonar` ≠ `none`, a `SONAR_TOKEN` secret and the Sonar project must exist before a scan works.
- With `signing` ≠ `none`, the Apple Developer Program membership, certificates/profiles (or the API key) and — for
  `fastlane-match` — the certs repo must exist before any `build`/`beta`/`release`/`notarize_release` lane works;
  never commit certificates, `.p12` files or `.p8` keys.
