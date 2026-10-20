---
name: iru-setup-macos-app
description: >-
  Scaffold a new native macOS desktop app (Swift 6, Xcode 27, Apple silicon + Intel universal) at the repository
  root — an XcodeGen `project.yml` with one macOS app target `<AppName>` (scheme `<AppName>`), a hosted Swift
  Testing unit-test target `<AppName>Tests`, an XCUITest target `<AppName>UITests` and the local package's
  `CoreTests` in the same scheme; `MARKETING_VERSION`/`CURRENT_PROJECT_VERSION` in `settings.base` (where
  `iru-swift-bump-version` rewrites them), `SWIFT_STRICT_CONCURRENCY = complete`, hardened runtime, an
  entitlements file with the App Sandbox (`sandbox: yes`, default), a generated Info.plist (`INFOPLIST_KEY_*`); a
  UI-framework-free local package `Packages/Core` (Foundation + Observation only: `Models/`, `Services/`, plus
  `ViewModels/` for `architecture: mvvm` or `Controllers/` + a passive-view protocol for `architecture: mvc`) whose
  Swift Testing suite covers 100% of its lines; the `App/` UI layer per `ui` — `swiftui` (`WindowGroup` +
  `Settings` + a `Commands` menu driven by a focused value, MVVM with a per-window `@Observable` view model) or
  `appkit` (programmatic: `main.swift` + `AppDelegate`, the main menu built in code, `NSWindowController` +
  `NSViewController` with Auto Layout in `loadView()`; `mvc` Cocoa controller core or `mvvm` with AppKit
  Observation tracking in `viewWillLayout()`); a `--uitesting` launch argument and accessibility identifiers on
  every control; per the catalog's UI contract, a `.ui-quality.yml` at the root, the shared
  `App/Tests/Support/UIScreenshots.swift` capture helper compiled into both test targets, and UI tests capturing the
  main window in every left-to-right/right-to-left × light/dark cell into `.ui-screenshots/` plus a
  `performAccessibilityAudit()` test at the configured level; an empty AppIcon/AccentColor asset catalog; `ExportOptions-*.plist` per `distribution`
  (`none` = copy-app export, `internal` = Developer ID, `store` = App Store Connect upload); `scripts/make-dmg.sh`
  (hdiutil UDZO + optional codesign); `.swiftlint.yml` (with `missing_docs`), `.swift-format`, and
  `sonar-project.properties` (omitted when `sonar: none`). The generated `.xcodeproj` is never committed. Invoke as
  `/iru-setup-macos-app`. Accepts pre-resolved inputs via `args` (`key: value` lines) — `ui` (`swiftui`/`appkit`),
  `architecture` (`mvvm`/`mvc`; `mvc` only with `appkit`), `app-name`, `bundle-id`, `team-id`, `min-macos`,
  `generator` (`xcodegen` only), `sandbox` (`yes`/`no`), `version`, `build-number`, `category`, `license`,
  `developer-name`, `developer-email`, `organization-url`, `open-source`, `visibility`, `ci`, `sonar`
  (+ `sonar-organization`/`sonar-project-key`/`sonar-host-url`), `distribution` (`none`/`internal`/`store`),
  `branching`, `accessibility` (`enforce`/`report`/`off`, default `enforce`), `mode` (`new`/`existing`) and
  `on-existing` (`ask`/`keep`/`update`/`replace`) — so
  `iru-setup-macos-repository` can supply them without re-prompting; stand-alone it asks `open-source` first and
  derives the `sonar` default from it. Announces whether it is scaffolding from scratch or updating; for every file
  group it owns that already exists it warns and asks Update / Keep as is / Replace / Stop (unless `on-existing`
  decides) and never overwrites hand-written source. Versions are looked up at run time with a dated October 2026
  fallback table. Use whenever a new macOS desktop app repository needs its Xcode project, testable core,
  quality tooling, tests and packaging bootstrapped from this house template; use `iru-setup-apple-app` for a
  multi-platform (iOS/watchOS + macOS) app instead.
model: sonnet
allowed-tools: Read Write Edit AskUserQuestion Bash(git *) Bash(gh *) Bash(curl *) Bash(xcodegen *) Bash(xcodebuild *) Bash(xcrun *) Bash(swift *) Bash(swiftlint *) Bash(python3 *) Bash(plutil *) Bash(chmod *) Bash(mkdir *) Bash(sw_vers *) Agent
---

# Setup macOS App

Generate a complete, buildable native macOS desktop app — an XcodeGen manifest, a UI-free `Packages/Core` local
package holding all the testable logic, the `App/` UI layer in SwiftUI or AppKit, unit and UI tests, quality
configs and packaging helpers — from the templates in this skill's `reference/` files. Every template was rendered
into throwaway projects (`swiftui+mvvm`, `appkit+mvc`, `appkit+mvvm`, plus `appkit+mvvm` on macOS 15 without the
sandbox) and proven against the real toolchain on 2026-10-16 (Xcode 27.1, Swift 6.4, XcodeGen 2.46.0, SwiftLint
0.65.1, macOS 27.0.1 arm64) — see **Known quirks / verification notes**.

The layout is the **scaffold contract** the Swift coding and gate skills (`iru-swift-code-one-task(-group)`,
`iru-swift-test`, `iru-swift-coverage`, `iru-swift-code-quality`, `iru-swift-docc`, `iru-swift-bump-version`) and
`iru-setup-macos-github-workflows` rely on — Step 8's contract table lists the confirmed names, commands and paths.
It follows `iru-setup-apple-app`'s conventions (XcodeGen, `.xcodeproj` never committed, `Packages/Core`,
SwiftLint/`swift format` configs, `sonar-project.properties`, versions in `project.yml` `settings.base`) and
`iru-setup-kmp-app`'s structure. Facts come from the author's docs (cited as "irurueta docs:
apps/apple/<page>.adoc"): `macos.adoc` (scenes, commands, Settings, MenuBarExtra, AppKit Observation tracking,
App Sandbox, Apple silicon only), `app-architecture.adoc` (MV vs MVVM with Observation, protocol-typed services and
test doubles), `uikit-and-appkit-interop.adoc` (`NSWindowController`, `NSMenu`, hosting), `testing-with-swift-testing.adoc`,
`ui-tests-test-plans-and-coverage.adoc`, `signing-capabilities-and-configuration.adoc`,
`macos-distribution-outside-the-app-store.adoc` (Developer ID, hardened runtime, archive/export, notarytool,
stapler, DMG) and `ci-cd-xcode-cloud-and-command-line.adoc` (App Store Connect export options, runners).
**No Fastlane** — Xcode's own `xcodebuild`/`notarytool`/`stapler`/`hdiutil` cover everything (irurueta docs:
apps/apple/macos-distribution-outside-the-app-store.adoc).

## Reference files — read only what this run needs

| Read | When |
|---|---|
| `reference/project-templates.md` | **Always.** `project.yml`, entitlements, asset catalog, `ExportOptions-*.plist`, `scripts/make-dmg.sh`, `.swiftlint.yml`, `.swift-format`, `sonar-project.properties`, the conditional `App/Info.plist`. |
| `reference/core-templates.md` | **Always.** `Packages/Core` (Package.swift, DocC catalog, Models/Services, ViewModels or Controllers) and its Swift Testing tests. |
| `reference/swiftui-templates.md` | `ui: swiftui` — the `App` with scenes, `ContentView`, `GreetingCommands`, `SettingsView`. |
| `reference/appkit-templates.md` | `ui: appkit` — `main.swift`, `AppDelegate`, `MainMenu`, `MainWindowController`, `MainViewController` (mvc or mvvm), `GreetingLayout`, `SettingsWindowController`. |
| `reference/test-templates.md` | **Always.** `LaunchOptions` (`--uitesting`), the app unit tests per `ui`/`architecture`, the XCUITest. |

**Conditional-marker convention used in every reference file**: a line `// >>> <condition>` (or `# >>>`,
`<!-- >>> … -->`) opens a block written only when the condition holds; the matching `<<< <condition>` closes it;
marker lines are never written. A file heading suffixed `(<condition>[, <condition>])` exists only when every
listed condition holds. Conditions: `ui: swiftui|appkit`, `architecture: mvvm|mvc`, `sandbox: yes|no`,
`distribution: none|internal|store`, `sonar` (= `sonar` is not `none`), `sonar: cloud`, and
`observation-tracking-opt-in` (= `ui: appkit` + `architecture: mvvm` + `min-macos` below `26`).
`<placeholder>` values come from Step 5's table and are substituted in headings (file paths) too.

## Step 0 — Resolve inputs

Invoked stand-alone (`/iru-setup-macos-app`) or by `iru-setup-macos-repository` / the `iru-setup-repository`
front door, which pass resolved answers as `key: value` lines, e.g.:

```
ui: appkit
architecture: mvc
app-name: My Mac App
bundle-id: com.example.mymacapp
team-id: ABCDE12345
min-macos: 26.0
sandbox: yes
version: 1.0.0
build-number: 1
category: public.app-category.productivity
license: MIT License
developer-name: Jane Doe
open-source: yes
visibility: public
ci: yes
sonar: cloud
sonar-organization: example-org-github
sonar-project-key: example-org_my-mac-app
sonar-host-url: https://sonarcloud.io
distribution: internal
branching: gitflow
accessibility: enforce
mode: new
on-existing: ask
```

Recognized keys (every key found is resolved — skip its question in Step 2):

| Key | Values / default |
|---|---|
| `ui` | `swiftui` / `appkit` — asked when absent |
| `architecture` | `swiftui` → `mvvm` only (never asked); `appkit` → `mvc` (default, recommended) or `mvvm`. `ui: swiftui` + `architecture: mvc` is rejected with an explanation (Step 2) |
| `app-name` | display name (`CFBundleDisplayName`), e.g. `My Mac App`; `<AppName>` (target, scheme, module, product) is its PascalCase form, e.g. `MyMacApp` |
| `bundle-id` | reverse-DNS, e.g. `com.example.mymacapp` |
| `team-id` | Apple Developer Team ID, default empty (local builds/tests don't need it; Developer ID/App Store exports do) |
| `min-macos` | default `26.0` (Step 4) |
| `generator` | `xcodegen` only — `tuist` is answered with "not supported by this skill; use `iru-setup-apple-app` for Tuist" and the run continues with XcodeGen |
| `sandbox` | `yes` (default; the Mac App Store requires it) / `no` |
| `version` / `build-number` | `MARKETING_VERSION` (default `1.0.0`, always numeric `x.y.z` — no `-SNAPSHOT`/`-dev`, App Store Connect and notarization reject suffixes) / `CURRENT_PROJECT_VERSION` (default `1`) |
| `category` | `LSApplicationCategoryType`, default `public.app-category.productivity` |
| `license`, `developer-name`, `developer-email`, `organization-url` | report + copyright line |
| `open-source`, `visibility`, `ci`, `sonar` (+ coordinates) | the `sonar` recommendation, as in `iru-setup-kmp-app` |
| `distribution` | `none` (copy-app export, local/QA builds) / `internal` (Developer ID + notarized DMG on GitHub Releases) / `store` (Mac App Store via App Store Connect); default `internal` (a notarized DMG on GitHub Releases is the natural public download, open source or not; `store` only when asked) |
| `branching` | `gitflow` / `main-only` — informational: the macOS app carries no pre-release marker in-tree (`iru-swift-bump-version` Step 5), so the files are identical either way |
| `accessibility` | `enforce` (default) / `report` / `off` — the UI tests' automated accessibility level, written to `.ui-quality.yml` (UI contract §8) |
| `mode`, `on-existing` | as in every catalog setup skill (default `ask`) |

Unknown keys from a full shared-args set (`publish`, `ci-tests`, `pages`, `integration-branch`, `stable-branch`,
`runner`, `macos-ci`, …) are ignored and named in the report. `mode: existing` never means "gap-fill silently":
Step 1 still warns about and asks about every pre-existing file group; only `on-existing` skips that question.
Orchestrators forward `on-existing` only when their own `args` received it.

## Step 1 — Survey the repository

Check for every file Step 6 would write: `project.yml`, `App/Sources/**`, `App/Resources/**`, `App/Info.plist`,
`App/Tests/**`, `App/UITests/**`, `Packages/Core/Package.swift`, `Packages/Core/Sources/**`,
`Packages/Core/Tests/**`, `ExportOptions-*.plist`, `scripts/make-dmg.sh`, `.swiftlint.yml`, `.swift-format`,
`.ui-quality.yml`, `sonar-project.properties`, plus any committed `*.xcodeproj`/`*.xcworkspace`, `Project.swift`, root `Package.swift`
and `fastlane/`. Then tell the user which of these this run is:

- **Scaffolding from scratch** — none exist: go to Step 2.
- **Updating an existing macOS app** — any exists: warn, listing every file found by path, that each existing file
  group is decided individually (missing files are still created). Groups (only those with a file present):
  **`project.yml`**, **`Packages/Core/Package.swift`**, **entitlements + asset catalog**, **export options +
  `scripts/make-dmg.sh`**, **quality config** (`.swiftlint.yml`, `.swift-format`, `.ui-quality.yml`),
  **`sonar-project.properties`**,
  and **the source skeleton** (`App/Sources`, `App/Tests`, `App/UITests`, `Packages/Core/Sources`/`Tests`). Unless
  `on-existing` decides, ask with `AskUserQuestion`, one question per group (batch up to 4 per call), naming each
  concrete conflict with this run's choices (e.g. "`project.yml` has no `ENABLE_APP_SANDBOX` but you chose
  `sandbox: yes`", "`Packages/Core/Sources/Core/Controllers/` exists but you chose `architecture: mvvm`",
  "`sonar-project.properties` exists but you chose `sonar: none`", "`MARKETING_VERSION` is `1.2.0-beta` — this
  scaffold keeps it numeric", "`.ui-quality.yml` says `accessibility: off` but you chose `enforce`"):
  - **Update (Recommended for `project.yml`, `Package.swift`, configs)** — "Merge: add what's missing and correct
    outdated parts using this skill's template as reference (targets, scheme test targets incl.
    `package: Core/CoreTests`, `settings.base` keys, hardened runtime/sandbox, `INFOPLIST_KEY_*`, rules); keep every
    target, setting, dependency and rule this skill doesn't own. You review a diff; customizations survive, but a
    part this skill owns may be rewritten." For the source skeleton, Update only creates missing files.
  - **Keep as is (Recommended for the source skeleton)** — "Leave the files untouched. Nothing you customized
    changes, but they may stay out of date or disagree with this run's choices — the report lists each mismatch."
  - **Replace** — "Regenerate from the template. Matches the house pattern exactly, but every customization is
    lost (recoverable only from git history)." Never the default. Even on Replace, never overwrite a Swift source
    file unless its content exactly matches this skill's original template (an untouched pre-UI-contract
    `App/UITests/<AppName>UITests.swift`, without the capture and audit tests, counts — Update may upgrade it).
  - **Stop** (first question only) — "End this skill now without changing any file." Report and end.

  When updating, read the current app name, bundle id, team id, deployment target, versions and the `ui`/
  `architecture` evidence (`import SwiftUI` + `@main … App` vs `main.swift`/`NSApplicationDelegate`;
  `ViewModels/` vs `Controllers/`) first and offer them as Step 2's defaults.
- **A foreign layout** — a committed `.xcodeproj` with no `project.yml`, a Tuist `Project.swift`, an
  `iru-setup-apple-app` multi-platform layout (`Targets/macOS/…`), a root `Package.swift` executable, or a
  `fastlane/` setup: not this skill's scaffold. Warn explicitly and ask (`AskUserQuestion`) whether to add only
  this skill's missing pieces alongside (quality configs, `Packages/Core`, export options, the DMG script — each
  still per-group Update/Keep/Replace) or stop. Never convert, move or delete an existing project, and never
  replace a committed `.xcodeproj` with an XcodeGen one without an explicit yes. A root `Package.swift` next to
  `project.yml` also makes `iru-swift-bump-version` ask which kind it is — say so.

## Step 2 — Collect the required inputs

For anything Step 0 didn't resolve, ask directly (pre-filled from Step 1 when updating): **app-name**,
**bundle-id**, **team-id** (optional — "leave empty to fill in later"), **min-macos**, **category**, developer
name/email/organization URL. Then the **license** via `AskUserQuestion` (MIT (recommended for an app) / Apache 2.0
/ No license / Other); remind the user in Step 8 to add a root `LICENSE`.

Then **ui** (unless resolved), `AskUserQuestion`:

- **SwiftUI (Recommended)** (`swiftui`) — native SwiftUI scenes: `WindowGroup`, `Settings` (⌘,), menu bar
  `Commands`; optional `MenuBarExtra`. The default for a new Mac app (irurueta docs: apps/apple/macos.adoc,
  "Native SwiftUI, Mac Catalyst, Designed for iPad or AppKit?").
- **AppKit** (`appkit`) — programmatic AppKit (`NSWindowController`/`NSViewController`, menus in code): for teams
  with AppKit experience, deep Mac-only behavior (text/canvas engines), or matching an existing AppKit codebase.

Then **architecture**, only when more than one is valid:

- `ui: swiftui` → `mvvm` without asking. Say why `mvc` isn't offered: SwiftUI has no controller layer — views are
  values driven by observable state — so the screen logic lives in a per-screen `@Observable` view model in
  `Packages/Core` (irurueta docs: apps/apple/app-architecture.adoc, "MVVM with Observation"); pick AppKit for MVC.
- `ui: appkit` → `AskUserQuestion`: **MVC (Recommended)** (`mvc`) — Cocoa's native pattern: the
  `NSViewController` owns widgets, target-action and lifecycle; a UI-free `@MainActor` controller in
  `Packages/Core/Sources/Core/Controllers/` decides what to show and drives the view through a protocol, so the
  logic is unit-tested headless. **MVVM** (`mvvm`) — an `@Observable` view model in `Core/ViewModels/`; the view
  controller renders it in `viewWillLayout()`, re-run by AppKit's Observation tracking (on by default from
  macOS 26; with `min-macos` below 26 the scaffold adds `NSObservationTrackingEnabled`).

Then **min-macos** (unless resolved): offer `26.0` (Recommended) — the docs' baseline (deployment minimum 26, Xcode
27 SDK); macOS 26 is the last release for Intel Macs, so Release builds stay universal (`arm64 x86_64`); AppKit
Observation tracking is on by default; and every SwiftUI API used here exists. Offer `15.0` as the lower option
(needs the `NSObservationTrackingEnabled` opt-in for AppKit MVVM; `UtilityWindow`/`defaultWindowPlacement` are 15+)
and `27.0` (Apple silicon only — the x86_64 slice can go). Never offer below `15.0`.

Then **sandbox** (unless resolved): **Yes (Recommended)** — required for the Mac App Store, kept for Developer ID
builds too (irurueta docs: apps/apple/macos.adoc, "The App Sandbox"); **No** — only for tools that need
unrestricted file/process access. `sandbox: no` + `distribution: store` is contradictory: warn and ask again.

Then **accessibility** (unless resolved), `AskUserQuestion` "Automated accessibility checks in UI tests?":
**Enforce (Recommended)** (`enforce` — every `performAccessibilityAudit()` issue fails the UI tests) / **Report
only** (`report` — issues attached and listed, never failing) / **Off** (`off` — the audit test skips; labels,
contrast and keyboard access are still coded). Written to `.ui-quality.yml`.

Then `open-source`, `sonar`, `distribution` (skip any resolved), exactly as `iru-setup-kmp-app` Step 2 does
(SonarCloud recommended only for public + open source; `ci: no` → recommend `none`). `distribution` explains:
`none` → `ExportOptions-copy.plist` (copy-app export, unsigned/ad-hoc, local QA — Gatekeeper blocks it when
downloaded); `internal` → `ExportOptions-developer-id.plist` + `scripts/make-dmg.sh` for a Developer ID signed,
notarized, stapled DMG (needs the Developer ID Application certificate and an App Store Connect API key — the
release job comes from `iru-setup-macos-github-workflows`); `store` → `ExportOptions-app-store.plist` (upload to
App Store Connect, `ITSAppUsesNonExemptEncryption = NO` written — change it if the app uses non-exempt
encryption). In-App Purchase, Sign in with Apple, Game Center and WeatherKit are App Store-only capabilities
(irurueta docs: apps/apple/macos.adoc).

## Step 3 — Infer repository information

Parse `git remote get-url origin` (`git@host:owner/repo.git` or `https://host/owner/repo.git`) for `<owner>`/
`<repo>` (Sonar defaults). No `origin` → ask.

## Step 4 — Look up toolchain versions

Look every version up at run time; fall back to this table (verified working together on 2026-10-16) only when a
lookup fails, and say so in Step 8.

| Component | Lookup | October 2026 fallback |
|---|---|---|
| Xcode / Swift / macOS SDK (never installed by this skill) | `xcodebuild -version`, `swift --version`, `xcodebuild -showsdks` | Xcode `27.1` (`27A9275`), Swift `6.4`, macOS SDK `27.0` |
| `<xcode-version>` (XcodeGen `options.xcodeVersion`) | `xcodebuild -version` major.minor | `27.1` |
| `min-macos` default | the docs' baseline (deployment minimum 26) bounded by the SDK major | `26.0` |
| XcodeGen (never installed) | `https://formulae.brew.sh/api/formula/xcodegen.json` `.versions.stable`, or `gh api repos/yonaskolb/XcodeGen/releases/latest --jq .tag_name` | `2.46.0` |
| SwiftLint (never installed) | `https://formulae.brew.sh/api/formula/swiftlint.json` `.versions.stable` | `0.65.1` |
| `swift-docc-plugin` (`<swift-docc-plugin-version>`) | `gh api repos/swiftlang/swift-docc-plugin/releases/latest --jq .tag_name` | `1.5.0` |
| `swift format` | bundled with the toolchain (`swift format --version`) | Swift 6.4's |
| `swift-tools-version` in `Package.swift` | the lowest that declares `.v<min-macos-major>`: `6.2` for `.v26`/`.v27`, `6.0` is enough for `.v15` (the template uses `6.2`) | `6.2` |

## Step 5 — Reference templates

Read the reference files (table above). Placeholders:

| Placeholder | Source |
|---|---|
| `<AppName>` | PascalCase of `app-name` (words capitalized and concatenated, non-alphanumerics stripped) |
| `<app-name>` / `<bundle-id>` / `<team-id>` / `<category>` | Step 0/2 |
| `<min-macos>` / `<min-macos-major>` | Step 2/4 (e.g. `26.0` / `26`) |
| `<marketing-version>` / `<build-number>` | `version` / `build-number` (defaults `1.0.0` / `1`) |
| `<developer-name>` / `<year>` | Step 2 / current year (copyright line) |
| `<xcode-version>` / `<swift-docc-plugin-version>` | Step 4 |
| `<sonar-organization>` / `<sonar-project-key>` / `<sonar-host-url>` | Step 2 |
| `<accessibility>` | Step 0/2 (`enforce` by default) — `.ui-quality.yml` |
| `<ScreenType>` | the main window's content type, the UI contract `<Id>` of its captures: `ContentView` (`swiftui`), `MainViewController` (`appkit`) |

Directory layout produced (the **contract** the Swift coding skill detects):

```
project.yml                                  XcodeGen manifest (the .xcodeproj is generated, gitignored)
App/Sources/                                 the UI layer — swiftui: <AppName>App.swift, ContentView.swift,
                                             GreetingCommands.swift, SettingsView.swift | appkit: main.swift,
                                             AppDelegate.swift, MainMenu.swift, MainWindowController.swift,
                                             MainViewController.swift, GreetingLayout.swift,
                                             SettingsWindowController.swift — plus LaunchOptions.swift (both)
App/Resources/<AppName>.entitlements         App Sandbox (sandbox: yes) — CODE_SIGN_ENTITLEMENTS
App/Resources/Assets.xcassets/               AppIcon (empty placeholder), AccentColor
App/Info.plist                               only for observation-tracking-opt-in (NSObservationTrackingEnabled)
App/Tests/                                   <AppName>Tests (Swift Testing, hosted by the app)
App/Tests/Support/UIScreenshots.swift        UI contract helper (also compiled into <AppName>UITests)
App/UITests/<AppName>UITests.swift           XCUITest: behaviour + window captures (ltr/rtl × light/dark) + audit
Packages/Core/Package.swift                  library Core, test target CoreTests, swift-docc-plugin
Packages/Core/Sources/Core/Core.docc/Core.md DocC landing page
Packages/Core/Sources/Core/Models/           Greeting
Packages/Core/Sources/Core/Services/         GreetingProviding, GreetingService, GreetingError
Packages/Core/Sources/Core/ViewModels/       mvvm: GreetingViewModel (@MainActor @Observable)
Packages/Core/Sources/Core/Controllers/      mvc: GreetingController (@MainActor) + GreetingView (passive-view protocol)
Packages/Core/Tests/CoreTests/               Swift Testing, 100% line coverage of Core
ExportOptions-copy.plist | ExportOptions-developer-id.plist | ExportOptions-app-store.plist   per distribution
scripts/make-dmg.sh                          UDZO disk image from an exported .app (+ optional codesign)
.swiftlint.yml  .swift-format                quality configs
.ui-quality.yml                              UI contract settings (accessibility level, directions, themes)
sonar-project.properties                     sonar ≠ none
```

`Packages/Core` never imports AppKit or SwiftUI; `GreetingView` is the protocol the AppKit `NSViewController`
conforms to (`mvc`). `.xcodeproj`, `build/`, `DerivedData/`, `*.xcarchive`, `*.dmg`, `.build/` and `.ui-screenshots/`
are `iru-setup-swift-gitignore`'s job.

## Step 6 — Scaffold the project

Apply Step 1's per-group decision to every file that already exists (Keep as is → skip; Update → merge after
showing `git diff --no-index <current> <draft>`; Replace → overwrite within Step 1's source-file limit). Files that
didn't exist are always written.

1. Write `project.yml`, the entitlements, the asset catalog, the matching `ExportOptions-*.plist`,
   `scripts/make-dmg.sh` (`chmod +x`), `.swiftlint.yml`, `.swift-format`, `.ui-quality.yml`,
   `sonar-project.properties` (sonar ≠ none)
   and, for `observation-tracking-opt-in`, `App/Info.plist`, from `reference/project-templates.md`.
2. Write `Packages/Core` from `reference/core-templates.md` (only the `architecture`-matching files).
3. Write `App/Sources` from `reference/swiftui-templates.md` or `reference/appkit-templates.md`, and
   `App/Sources/LaunchOptions.swift`, `App/Tests`, `App/UITests` from `reference/test-templates.md`.
4. If `team-id` is empty, say that `project.yml`'s `DEVELOPMENT_TEAM` and the export plist's `teamID` must be filled
   in (or passed as `DEVELOPMENT_TEAM=<id>` on CI) before a Developer ID or App Store export; local builds/tests
   don't need it.

## Step 7 — Verify

Run every command through the `iru-gate-runner` agent (never inline — the logs are long). macOS with a full Xcode
only; on any other host, or with Command Line Tools only, report every step "unverified (needs macOS/Xcode)". If
`xcodegen`/`swiftlint` aren't installed, say so (`brew install xcodegen swiftlint`), mark their steps unverified,
and never install them yourself. The first run resolves `swift-docc-plugin` from GitHub (network).

1. `cd Packages/Core && swift test --enable-code-coverage`, then `xcrun llvm-cov report
   "$(swift build --show-bin-path)/CoreTests.xctest/Contents/MacOS/CoreTests" -instr-profile
   "$(swift build --show-bin-path)/codecov/default.profdata" --ignore-filename-regex='(Tests/|DerivedSources|\.build/)'`
   — expect 100% lines.
2. `xcodegen generate`, then `xcodebuild build-for-testing -project <AppName>.xcodeproj -scheme <AppName>
   -destination 'platform=macOS' -derivedDataPath build/dd CODE_SIGN_IDENTITY=- CODE_SIGN_STYLE=Manual
   DEVELOPMENT_TEAM=` — zero warnings expected.
3. `xcodebuild test-without-building … -derivedDataPath build/dd -resultBundlePath build/test.xcresult` (CoreTests
   + `<AppName>Tests` + `<AppName>UITests`), serialized behind `.simulator-test.lock` like every app-kind run of
   the Swift gates; the UI tests take over the desktop session. Parse with `xcrun xcresulttool get test-results
   summary`. Then recover the UI contract captures with `iru-swift-test`'s `ui` run (or its `xcresulttool export
   attachments` step on `build/test.xcresult`) — expect 4 files in `.ui-screenshots/screen/<ScreenType>/` and the
   audit at the `.ui-quality.yml` level; without the Automation permission or a logged-in desktop session the UI
   tests are **unverified**, not passed.
4. `swiftlint lint --strict` and `swift format lint --strict --recursive App Packages/Core/Sources
   Packages/Core/Tests` from the root.
5. DocC: `cd Packages/Core && swift package --allow-writing-to-directory ../../build/docc generate-documentation
   --target Core --warnings-as-errors --output-path ../../build/docc` (create `build/docc` first), and
   `xcodebuild docbuild -scheme <AppName> -destination 'platform=macOS' -derivedDataPath build/dd-doc
   CODE_SIGNING_ALLOWED=NO`.
6. Archive/export/DMG: `xcodebuild archive -scheme <AppName> -destination 'generic/platform=macOS'
   -archivePath build/<AppName>.xcarchive CODE_SIGN_IDENTITY=- CODE_SIGN_STYLE=Manual DEVELOPMENT_TEAM=`;
   `xcodebuild -exportArchive -archivePath build/<AppName>.xcarchive -exportOptionsPlist ExportOptions-copy.plist
   -exportPath build/export` (for `internal`/`store`, export with a copy-app plist to prove the path, and report
   the Developer ID/App Store export itself as "unverified (needs certificates)" unless the machine has them);
   `scripts/make-dmg.sh build/export/<AppName>.app build/<AppName>.dmg`.

Report pass/fail per command; quote error output verbatim for a failure only.

## Step 8 — Report

Summarize: resolved `ui`, `architecture` (and why the other wasn't offered for SwiftUI), `app-name`/`<AppName>`,
`bundle-id`, `team-id` (or "empty — fill in before exporting"), `min-macos` (and why), `sandbox`, `category`,
`MARKETING_VERSION`/`CURRENT_PROJECT_VERSION`, license, and whether the run scaffolded from scratch, updated an
existing app, or stopped. Then, per Step 1 group, the action taken — **created / updated / replaced / kept as is**
— with each mismatch of a kept group and what a replaced one may have lost. State what was included versus omitted
and why (`sonar` coordinates or why `none`; `distribution` and its export plist; the release pipeline lives in
`iru-setup-macos-github-workflows`), which Step 4 versions were live versus fallback, the `accessibility` level
written to `.ui-quality.yml` (and its action — created / updated / replaced / kept as is), and any ignored `args`
keys.

### Scaffold contract (confirmed by running it — downstream skills depend on these)

| What | Exact name / path / command |
|---|---|
| Project | `project.yml` → `xcodegen generate` → `<AppName>.xcodeproj` (gitignored); one scheme `<AppName>`; targets `<AppName>` (app, module `<AppName>`, product `<AppName>.app`), `<AppName>Tests`, `<AppName>UITests`; local package product `Core` |
| Versions | `project.yml` `settings.base` `MARKETING_VERSION: x.y.z` (unquoted, numeric) / `CURRENT_PROJECT_VERSION: n` — `iru-swift-bump-version` app path (its regexes verified against this file). Kind = app: root has `project.yml` and no root `Package.swift` |
| Architecture marker | `Packages/Core/Sources/Core/ViewModels/` = MVVM; `Packages/Core/Sources/Core/Controllers/` (controller + `<Screen>View` protocol) = MVC; `App/Sources/main.swift` + `AppDelegate` = AppKit, `@main struct … App` = SwiftUI |
| Core tests + coverage (the bar) | `cd Packages/Core && swift test --enable-code-coverage` → `.build/out/Products/Debug/CoreTests.xctest`, `.build/out/Products/Debug/codecov/default.profdata` (`.build/debug` symlinks there); `llvm-cov report`/`export -format=lcov` as in `iru-swift-coverage`'s package path — 100% lines for every variant |
| All tests | `xcodebuild test -project <AppName>.xcodeproj -scheme <AppName> -destination 'platform=macOS' CODE_SIGN_IDENTITY=- CODE_SIGN_STYLE=Manual DEVELOPMENT_TEAM= -resultBundlePath <x>.xcresult` runs `CoreTests` + `<AppName>Tests` + `<AppName>UITests` (`-skip-testing:<AppName>UITests` for unit tests only — verified) |
| App coverage | `-enableCodeCoverage YES` + `xcrun xccov view --report --json` reports `<AppName>.app` (the UI layer — "not measured" for the bar) but **not** the statically linked `Core` sources: measure Core with `swift test` (row above) |
| Lint / format | `swiftlint lint --strict` (root; `.swiftlint.yml` includes `App`, `Packages/Core/Sources`, `Packages/Core/Tests`; `missing_docs` warning for open/public) · `swift format lint --strict --recursive App Packages/Core/Sources Packages/Core/Tests` |
| DocC | `swift package --package-path Packages/Core --allow-writing-to-directory <out> generate-documentation --target Core --warnings-as-errors --output-path <out>` (add `--transform-for-static-hosting --hosting-base-path <repo>/api` for Pages); `xcodebuild docbuild -scheme <AppName> -destination 'platform=macOS' -derivedDataPath <dd>` → `<dd>/Build/Products/Debug/{Core,<AppName>}.doccarchive` |
| Archive | `xcodebuild archive -project <AppName>.xcodeproj -scheme <AppName> -destination 'generic/platform=macOS' -archivePath build/<AppName>.xcarchive` (+ `CODE_SIGN_IDENTITY=- CODE_SIGN_STYLE=Manual DEVELOPMENT_TEAM=` without certificates) → universal `arm64 x86_64`, hardened runtime, entitlements without `get-task-allow` |
| Export | `xcodebuild -exportArchive -archivePath build/<AppName>.xcarchive -exportOptionsPlist ExportOptions-<copy\|developer-id\|app-store>.plist -exportPath build/export` → `build/export/<AppName>.app` (`app-store` uploads instead; add `-allowProvisioningUpdates -authenticationKeyPath/-ID/-IssuerID` on CI) |
| DMG | `scripts/make-dmg.sh build/export/<AppName>.app build/<AppName>.dmg ["<volume>"]` (`DMG_SIGN_IDENTITY="Developer ID Application: …"` signs it, identifier `<bundle-id>.dmg`); then `xcrun notarytool submit build/<AppName>.dmg --key … --key-id … --issuer … --wait` and `xcrun stapler staple build/<AppName>.dmg` |
| Entitlements | `App/Resources/<AppName>.entitlements`: `com.apple.security.app-sandbox` (sandbox: yes) else empty; `ENABLE_HARDENED_RUNTIME: YES`, `ENABLE_APP_SANDBOX` mirrors the sandbox |
| UI-test hooks | launch arguments `["-ApplePersistenceIgnoreState", "YES", "--uitesting"]` (`--uitesting` last); identifiers `nameField`, `greetButton`, `greetingLabel`, `errorLabel`, `greetsOnSubmitToggle` |
| UI contract | `.ui-quality.yml` (root, committed); helper `App/Tests/Support/UIScreenshots.swift` in both test targets; captures `.ui-screenshots/screen/<ScreenType>/default--<ltr\|rtl>--<light\|dark>.png`, attached to the `.xcresult` as `screen~<ScreenType>~…` (the sandboxed host can't write the repository — `iru-swift-test`'s `ui` run exports them); RTL `-AppleLanguages (ar) -AppleTextDirection YES -NSForceRightToLeftWritingDirection YES`, dark `-AppleInterfaceStyle Dark`; audit issues attached as `a11y~<ScreenType>~<rule>` |

### Known quirks / verification notes

- **UI contract additions (2026-10-16) are only partly verified**: `UIScreenshots.swift` and the new
  `<AppName>UITests.swift` pass `swift format lint --strict` with this skill's `.swift-format` and type-check for
  macOS 15 against the macOS 27 SDK; the helper ran under `swift test` on macOS in a throwaway package (ImageRenderer
  and `NSView` captures, RTL verified to flip leading/trailing, `.ui-quality.yml` read). Not run: a regenerated
  scaffold (no XcodeGen on that machine), so the manifest's extra UI-test source line, the macOS XCUITest matrix
  (`-AppleInterfaceStyle Dark` and the RTL launch arguments on a live app), the audit on the main window and SwiftLint
  on the helper are **unverified** — run Step 7 before trusting them.

- **Verified for real on 2026-10-16** in `$TMPDIR/iru-verify/macos/iru-setup-macos-app/{swiftui-mvvm,appkit-mvc,
  appkit-mvvm,appkit-mvvm-macos15-nosandbox}` (outside this repository) with Xcode 27.1 (27A9275), Swift 6.4,
  XcodeGen 2.46.0 and SwiftLint 0.65.1 (both run from a temp download, not installed): `swift test` (7–8 Core tests,
  **100.00% line coverage** of Core in every variant), `xcodegen generate`, `xcodebuild build-for-testing` (no
  warnings under Swift 6 strict concurrency), `xcodebuild test` with ad-hoc signing — swiftui-mvvm 14/14,
  appkit-mvc 23/23, appkit-mvvm 22/22 (both macOS-26 sandboxed and macOS-15 unsandboxed) **including the two
  XCUITest cases**, the sandboxed app hosting the unit tests — `swiftlint lint --strict` (0 violations),
  `swift format lint --strict` (clean), DocC (`generate-documentation --warnings-as-errors` and `xcodebuild
  docbuild`), `xcodebuild archive` (ad-hoc; universal binary, `flags=0x10002(adhoc,runtime)`, sandbox entitlement
  only), `-exportArchive` with `ExportOptions-copy.plist`, and `scripts/make-dmg.sh` (UDZO, `hdiutil verify`
  VALID; also with `DMG_SIGN_IDENTITY=-`; `shellcheck` clean). Variants used `sonar: cloud`/`self-hosted`/`none` and
  `distribution: internal`/`store`/`none` (all export plists pass `plutil -lint`).
- **Signing for local test runs**: `CODE_SIGNING_ALLOWED=NO` builds and runs the unit tests (CoreTests +
  `<AppName>Tests` passed), but the UI-test runner is killed before it connects ("Early unexpected exit … Test
  crashed with signal kill before establishing connection") — arm64 needs a signed `XCTRunner`. Ad-hoc signing
  (`CODE_SIGN_IDENTITY=- CODE_SIGN_STYLE=Manual DEVELOPMENT_TEAM=`) runs everything, sandbox included.
- **XCUITest needs Automation Mode**: the first UI run failed with "The test runner failed to initialize for UI
  testing. (Underlying Error: Timed out while enabling automation mode.)" — `automationmodetool` reports "This
  device requires user authentication to enable Automation Mode". After the user authorized it at the system
  prompt, every later run passed. On a fresh machine expect that prompt (or run
  `sudo automationmodetool enable-automationmode-without-authentication` yourself on a CI/dedicated machine —
  this skill never runs it). The runner's macOS session must be unlocked.
- **`--uitesting` must come last in `launchArguments`**: the arguments domain reads `-key value` pairs, so
  `["--uitesting", "-ApplePersistenceIgnoreState", "YES"]` made `--uitesting` swallow the next flag; the SwiftUI
  app then restored the previous session and opened **no window** (both UI tests failed: `nameField` never
  appeared). The AppKit app opens its window explicitly and was unaffected.
- **Registered defaults are process-wide**: `UserDefaults.standard.register(defaults:)` (AppKit `AppDelegate`)
  also answers `object(forKey:)` on every suite, so tests assert on `persistentDomain(forName:)` instead.
- **A launched app bundle gets `com.apple.macl` protection**: rebuilding into the same DerivedData after the app
  or its UI-test runner ran failed with `ld: can't write output file: …-Runner.app/…` — use a fresh
  `-derivedDataPath` per build (or `test-without-building` after one `build-for-testing`).
- **`xccov` does not attribute the statically linked `Core` sources** in the app scheme's result bundle (only the
  test bundles and `<AppName>.app`'s own files appear); the Core bar is measured with `swift test` + `llvm-cov`.
  The app target reported 88.8% (swiftui-mvvm) but is never part of the bar.
- **`INFOPLIST_KEY_*` only works for keys Xcode knows**: `INFOPLIST_KEY_ITSAppUsesNonExemptEncryption: NO` landed
  in Info.plist, but `INFOPLIST_KEY_NSObservationTrackingEnabled` was silently dropped — hence the committed
  `App/Info.plist` (merged via `INFOPLIST_FILE` with `GENERATE_INFOPLIST_FILE: YES`) for the opt-in case,
  verified to produce `NSObservationTrackingEnabled => true`.
- **swift-format vs SwiftLint**: swift-format adds trailing commas to multi-line collection literals, which
  SwiftLint's `trailing_comma` rejects — `.swiftlint.yml` disables that rule. Without `.swift-format` the
  formatter defaults to 2-space indentation.
- **`main.swift` for programmatic AppKit**: `@main` on an `NSApplicationDelegate` calls `NSApplicationMain`, which
  without a main nib never instantiates the delegate; `main.swift` installs it (top-level code is main-actor
  isolated in Swift 6). `NSPrincipalClass = NSApplication` comes from `INFOPLIST_KEY_NSPrincipalClass`.
- **Symbol-graph audit**: `swift package dump-symbol-graph` lists `!=(_:_:)` and `localizedDescription` without
  doc comments — synthesized/inherited members, not gaps.
- **`ExportOptions-developer-id.plist` with an empty `teamID`** fails with `"teamID" should be non-empty`; with a
  team but no certificate, `No signing certificate "Developer ID Application" found`. Developer ID signing,
  notarization, stapling, Gatekeeper assessment and the App Store Connect upload are **unverified (needs
  certificates and an Apple Developer Program membership)**.
- `NSControl.Events` (`.valueChanged`, `.primaryActionTriggered`, tracking events) appear in the macOS 27 SDK;
  the templates use classic target-action. When adding them with `min-macos` below 27, guard with
  `if #available(macOS 27, *)`. Responder-chain `@objc` protocols adopted by an `NSViewController` must be
  `@MainActor` under Swift 6.
- The "CoreSimulator is out of date" and `appintentsmetadataprocessor` "Metadata extraction skipped" lines in
  `xcodebuild` output are harmless for a macOS-only project.

Finish with a **Warn explicitly** block:

- Review every generated file before building, committing or distributing; replace the `Greeting` sample, the
  empty AppIcon set and the Help menu target with real content.
- Run `iru-setup-swift-gitignore` — the `.xcodeproj`, `build/`, `DerivedData/`, `*.xcarchive`, `*.dmg`, `.build/`
  and `.simulator-test.lock/` must never be committed; every clone runs `xcodegen generate` first.
- Never commit certificates, `.p12` files or App Store Connect `.p8` keys; CI reads them from secrets.
- UI tests drive the real desktop: grant Automation Mode once per machine and never run two UI-test runs at once.
- With `sonar` ≠ `none`, a `SONAR_TOKEN` secret and the Sonar project must exist before a scan works.
