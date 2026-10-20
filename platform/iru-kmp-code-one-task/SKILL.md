---
name: iru-kmp-code-one-task
description: >-
  Implement a single task from a Kotlin Multiplatform (Android + iOS app) `implementation_plan.md`-style task list —
  just the implementation and its tests. Detects the project layout at runtime (this catalog's `iru-setup-kmp-app`
  layout — `shared/` KMP module + `androidApp/` + XcodeGen-generated `iosApp/` — or the JetBrains wizard's older
  single `composeApp/` module, and whether the shared module uses the Android-KMP library plugin
  `com.android.kotlin.multiplatform.library` or `androidTarget()` + `com.android.library`), whether UI is shared
  Compose Multiplatform (`ui: compose`) or native per platform (`ui: native` — Jetpack Compose in `androidApp`,
  SwiftUI in `iosApp`), and which module and source set the task belongs to (`commonMain` first, `androidMain`,
  `iosMain`, `androidApp`, or Swift in `iosApp`), then loads only the matching guidance from this skill's own
  `reference/` directory (always: mandatory rules — no platform API in `commonMain`, tests in the right source set, no
  `!!`, `@Throws` on Swift-facing throwing APIs, KDoc, no secrets, no edits to generated code — Kotlin code style with
  explicit API mode where enabled, and project structure with the default hierarchy template and `expect`/`actual` vs
  interface + DI; as needed: testing with `kotlin.test` + `runTest` + Turbine + fakes over mocks, shared logic —
  coroutines/`Dispatchers.IO`, Ktor with platform engines, kotlinx.serialization, kotlinx-datetime,
  SQLDelight/Room/DataStore, Koin or manual DI, multiplatform ViewModel — Compose Multiplatform with the `Res` class,
  navigation, previews and `MainViewController`, native UI over shared state, iOS interop as Swift sees it through the
  Objective-C header with SKIE/KMP-NativeCoroutines when present, KDoc/Dokka, security, and — for a task that adds or
  changes a screen, component or list — the catalog's UI contract mapped onto KMP: `Screen › Region › Component`
  decomposition reported back, stateless components over the shared view model's immutable state, `Lazy*` with
  `key`/`contentType` and SwiftUI `List`/lazy stacks for every collection, `runComposeUiTest` UI tests on the
  Android host (Robolectric) and the iOS simulator or Robolectric/`ImageRenderer` tests for native UI, capturing
  `.ui-screenshots/` across left-to-right/right-to-left × light/dark with an `--android`/`--ios` variant, and the
  accessibility check at the `.ui-quality.yml` level), re-checks the current
  code state, implements exactly what the task specifies, writes/updates tests in the right source set, compile-checks
  every target the touched source sets compile for with the Gradle wrapper (task names discovered via `./gradlew
  :<module>:tasks --all`; iOS targets only on macOS — never booting a simulator), regenerating the Xcode project with
  `xcodegen generate` when `iosApp/project.yml` changed, then — if the task didn't stop on a blocker — immediately
  checks off this task's own checkbox (and its sub-tasks') in `implementation_plan.md` with a "group validation
  pending" note, before handing back a short summary (layout/module/source sets detected, files touched, tests
  added/updated, compile-check result per target, any deliberate deviation from `reference/`, and any blocker). Does
  not capture a quality baseline, add license headers, update KDoc beyond the code it writes, run
  tests/coverage/detekt/ktlint/Lint/SwiftLint, or boot a simulator — those happen once per task group in
  `iru-kmp-code-one-task-group`, which invokes this skill once per task in a bucket (in parallel when the bucket
  allows it, through the `iru-isolated-skill-executor` agent). Invoke as `/iru-kmp-code-one-task <task description>`,
  passing the task's own text — including its exact `implementation_plan.md` checkbox line(s) — as the argument. The
  Kotlin Multiplatform counterpart of `iru-android-code-one-task`/`iru-swift-code-one-task`, for plan tasks tagged
  `kmp`.
model: sonnet
allowed-tools: Read Edit Write Bash(./gradlew *) Bash(gradle *) Bash(xcodegen *) Bash(xcodebuild *) Bash(xcrun *) Bash(xcode-select *) Bash(uname *) Bash(git status *) Bash(git diff *) Bash(git log *) Bash(find *) Bash(grep *) Bash(ls *) Bash(cat *)
---

# Implement one plan task (Kotlin Multiplatform)

Carry out a single task's implementation, tests, and checkbox update in a Kotlin Multiplatform mobile app — nothing
else. This is the narrowest execution unit for a `kmp` task in the `iru-code` pipeline: `iru-kmp-code-one-task-group`
calls it once per task in a bucket (potentially many at once, in parallel agents via `iru-isolated-skill-executor`),
then handles license headers, KDoc auditing, and all test/coverage/quality/iOS validation itself, once for the whole
bucket. It uses a medium model on purpose — the plan carries the hard reasoning; this skill executes one task against
code agreements that live in `reference/`.

Two things make it different from the Android and Swift equivalents:

1. **One source file can compile for several targets.** A change in `commonMain` must compile for Android *and* iOS;
   a missing `actual` or a JVM-only API in common code only shows up when the other target compiles. Step 5 therefore
   compile-checks every target the touched source sets feed, not just one module.
2. **Swift is a first-class consumer.** Any public declaration of the framework-exported module becomes Objective-C/
   Swift API; `reference/ios-interop.md` decides how it should be shaped.

## Step 0 — Detect the project shape once

Settle these from the files, never from assumptions (this skill is copied into other repositories):

- **Layout**: `settings.gradle.kts` `include(...)` and each module's `plugins {}`:
  - `shared/` applying `org.jetbrains.kotlin.multiplatform` + `androidApp/` (`com.android.application`) + `iosApp/` →
    the catalog layout (`iru-setup-kmp-app`).
  - a single `composeApp/` applying both the multiplatform plugin and `com.android.application` (plus `iosApp/`,
    possibly a `shared/` logic module) → the older JetBrains wizard layout.
  - Neither, but some module applies `org.jetbrains.kotlin.multiplatform`: use that module as "the shared module" and
    say so in the report. No KMP module at all → this isn't a KMP project; report it as a blocker (the task was
    mis-tagged) rather than writing Android-only or Swift-only code under a `kmp` tag.
- **Android plugin of the shared module** (`reference/project-structure.md`'s table):
  `com.android.kotlin.multiplatform.library` (`kotlin { android { … } }` or `androidLibrary { … }`) vs
  `androidTarget()` + `com.android.library`/`com.android.application`. Note whether an Android host-test source set is
  configured (`withHostTestBuilder` → `androidHostTest`; `androidUnitTest` under `androidTarget()`).
- **UI mode**: the shared module applies `org.jetbrains.compose` (+ `org.jetbrains.kotlin.plugin.compose`) and has
  composables in `commonMain` → `compose`; otherwise (`androidApp` holds Jetpack Compose UI, `iosApp` holds SwiftUI
  views over shared state) → `native`.
- **iOS project**: `iosApp/project.yml` → XcodeGen (the `.xcodeproj` is generated and gitignored); a committed
  `iosApp/*.xcodeproj` with no `project.yml` → hand-maintained. Note the framework `baseName` (`Shared` by default).
- **Interop/tooling present**: SKIE (`co.touchlab.skie`), KMP-NativeCoroutines (`com.rickclephas.kmp.nativecoroutines`),
  Mokkery (`dev.mokkery`), Koin, SQLDelight (`app.cash.sqldelight`), Room (`androidx.room` + KSP), Turbine, Robolectric
  on the host-test classpath, explicit API mode (`explicitApi()`), `-Xexpect-actual-classes`.
- **Host**: `uname -s` — iOS compilation needs macOS with Xcode (`xcode-select -p` pointing at `Xcode.app`). On any
  other host, iOS compile-checks are "unavailable", never "passed".
- **Test conventions**: two or three existing tests in `commonTest` (and in the platform test set the task will
  touch): naming, fake style, Turbine, Mokkery.

## Step 1 — Decide module and source set(s), then read only the reference material this task needs

Use `reference/project-structure.md`'s "Deciding the module and source set from a task's text": a path in the task
wins; otherwise infer (logic, state, networking, persistence → shared `commonMain`; Android/Apple framework needs →
`androidMain`/`iosMain` behind a common interface; `ui: compose` screens → shared `commonMain`; `ui: native` screens →
`androidApp`/`iosApp`); genuinely ambiguous → shared `commonMain`, and say so in Step 8. Record the set of
(module, source set) pairs the task touches — Step 5 derives the compile-checks from it.

This skill ships a `reference/` directory next to this file. Read `reference/README.md` first — it is short and routes
you to the rest — then read only what it points at. The routing, restated:

| Read | When |
|---|---|
| `reference/mandatory-rules.md` | **Always** — the non-negotiables. |
| `reference/code-style.md` | **Always** — Kotlin conventions, visibility, explicit API mode, naming. |
| `reference/project-structure.md` | **Always** — modules, source-set hierarchy, `expect`/`actual` vs interface + DI. |
| `reference/testing.md` | The task writes or updates tests — nearly every task. |
| `reference/kdoc.md` | The task adds or changes a public/internal declaration (Kotlin) or public Swift type. |
| `reference/shared-logic.md` | Coroutines/Flow, Ktor, serialization, dates, persistence, DI, shared ViewModel, non-UI resources. |
| `reference/compose-multiplatform.md` | A `@Composable` in the shared module (`ui: compose`), `Res` resources, navigation, previews, `MainViewController`, UIKit/SwiftUI interop. |
| `reference/native-ui.md` | `androidApp` Jetpack Compose or `iosApp` SwiftUI over shared state (`ui: native`). |
| `reference/ui-contract.md` + `reference/ui-implementation.md` | The task adds or changes a screen, component, list or other UI (either `ui` mode) — decomposition, inputs/events, the lazy-collection rule, UI tests, the screenshot matrix and accessibility checks. |
| `reference/ios-interop.md` | A declaration Swift calls changes (public API of the exported module), or Swift is written in `iosApp`. |
| `reference/security.md` | Credentials/tokens, sensitive storage, networking/TLS, logging of user data, R8 rules, `Info.plist`/ATS, external input. |

Read at most one of `compose-multiplatform.md`/`native-ui.md` for a given screen; any task that touches UI also
reads `ui-contract.md` and `ui-implementation.md`. If `reference/` is missing (the
skill directory was copied without it), proceed using the repository's own `CLAUDE.md` conventions and the
surrounding code's style, and say so in Step 8 — don't guess at what the reference would have said.

## Step 2 — Re-check the current code state

Read the actual current content of every file the task touches before editing — other tasks in the same bucket may be
landing concurrently. For an `expect` declaration, read **all** its `actual`s (`grep -rn "actual .*<Name>"` across the
module's `src/`); for a public declaration of the exported module, find its Swift callers
(`grep -rn "<Name>" iosApp --include=*.swift`) — a signature change may break Swift code that no Kotlin compile
check sees. Note what the surrounding code does about the things `reference/` has opinions on; a file that
consistently does something else wins (except `mandatory-rules.md`), and the divergence goes in Step 8.

## Step 3 — Implement exactly what the task specifies

Apply `reference/mandatory-rules.md` in full, `reference/code-style.md`, `reference/project-structure.md`, and whichever
optional files Step 1 selected, plus the repository's own `CLAUDE.md` where more specific. Work in dependency order:
`commonMain` types/interfaces/`expect`s → `androidMain` → `iosMain` → `androidApp` / `iosApp` callers.

Non-negotiable, because a later gate or the other platform enforces them:

- **`commonMain` first, no platform API in it**; every `expect` gets an `actual` for every target.
- **KDoc** on every public/internal declaration — `@throws` matching `@Throws` on Swift-facing APIs.
- **No `!!`**, `val` over `var`, read-only types in public signatures.
- **No new dependency, Gradle plugin, or Kotlin target** unless the task explicitly calls for it — a blocker to report
  (Step 6) otherwise.
- **Swift callers updated** in the same task when a public signature they use changes (`reference/ios-interop.md`);
  never edit the generated framework/header or the generated `iosApp.xcodeproj` — edit `iosApp/project.yml` instead
  and regenerate (Step 5).

- **UI tasks — decompose first** (`reference/ui-contract.md` §2): before writing UI code, write the
  `Screen › Region › Component` tree (inputs, events, visual states, what it reuses) and keep it for Step 8's
  report. Build leaves first; state and intents live in the shared view model; every collection goes through a
  lazy container with stable keys (`reference/ui-implementation.md`); navigation stays in the one graph.

Don't add anything the task didn't ask for — no speculative `expect`/`actual`, no unrelated cleanup, no restyling.

## Step 4 — Write or update the tests

Follow `reference/testing.md` and the existing test style: `commonTest` for platform-neutral behavior (it runs on
every target), the Android host-test set for `androidMain`, `iosTest` for `iosMain`, `androidApp/src/test` for
`androidApp`, `iosApp/iosAppTests` (XCTest) for Swift. `kotlin.test` + `runTest` + Turbine where present + fakes
(MockK never in `commonTest`). Cover the edge cases implied by the KDoc `@throws`/error-result contracts. Do not run
the tests — `iru-kmp-code-one-task-group` runs them once per bucket and per target.

For a UI task, also write the UI tests `reference/ui-implementation.md` describes: component/screen tests for every
visual state that applies (behaviour once, left-to-right + light), a capture of each state across the
`.ui-quality.yml` directions × themes through the module's screenshot helper (`uitest/UiScreenshots.kt` in
`commonTest` for `ui: compose`, `androidApp/src/test/…/uitest/UiScreenshots.kt` and
`iosApp/iosAppTests/UIScreenshots.swift` for `ui: native` — create it from `ui-implementation.md` only if the
module's test wiring already supports it, otherwise report the missing wiring), and the accessibility check. Never
add Robolectric, a test dependency or a test target to make a UI test fit — that is a blocker to report (Step 6).

## Step 5 — Compile-check every target the touched source sets feed

A broken compile in one task blocks every other task in a parallel bucket from validating, and a common-code change
can compile for one target and fail on the other. Set up the environment once:

```bash
export JAVA_HOME=$(/usr/libexec/java_home -v 21)   # macOS; or -v 17. Use any JDK 17+ the build accepts elsewhere.
export ANDROID_HOME=${ANDROID_HOME:-$HOME/Library/Android/sdk}   # or local.properties sdk.dir
```

Discover the module's real task names once — `./gradlew :<module>:tasks --all` — instead of trusting the defaults
below, then run **one** Gradle invocation with every applicable compile task (`./gradlew` when the wrapper exists,
`gradle` otherwise):

| Touched | Compile tasks (Android-KMP library plugin) | (`androidTarget()` setup) |
|---|---|---|
| `commonMain` / `commonTest` | Android **and** iOS rows below | same |
| Android side (`androidMain`, host tests, or via common) | `:<m>:compileAndroidMain`, `:<m>:compileAndroidHostTest` (if the host-test set exists) | `:<m>:compileDebugKotlinAndroid`, `:<m>:compileDebugUnitTestKotlinAndroid` |
| iOS side (`iosMain`, `iosTest`, or via common) — macOS only | `:<m>:compileKotlinIosSimulatorArm64`, `:<m>:compileTestKotlinIosSimulatorArm64` (`…IosX64` on an Intel Mac) | same |
| `androidApp` | `:androidApp:compileDebugKotlin` + its unit-test compile task (find it in `tasks --all`; e.g. `compileDebugUnitTestKotlin`) | same |

Notes:

- Compiling the iOS simulator target compiles the shared intermediate source sets (`iosMain`, `appleMain`,
  `nativeMain`) for it — enough to catch a missing `actual` or a non-common API. It does **not** link a framework or
  start a simulator; don't run `link*`, `*Test`, `allTests`, `check`, `build`, or `embedAndSignAppleFrameworkForXcode`
  here.
- **Compose resources** (`composeResources/`) changed: the compile tasks regenerate the `Res` accessors first — a
  resource referenced in code but missing on disk fails here, which is the point.
- **SQLDelight/Room/KSP** changes: the compile tasks run the generators; a generator error is the task's own error.
- **Not on macOS** (or no full Xcode): run only the Android rows, and report the iOS compile-check as **unavailable**
  — the group skill's iOS stage will mark it unverified rather than passed.
- **Swift in `iosApp` changed, or `iosApp/project.yml` changed** (macOS only): regenerate first if the manifest
  changed (`cd iosApp && xcodegen generate`), then build without running anything:
  `xcodebuild build-for-testing -project iosApp/iosApp.xcodeproj -scheme iosApp -destination 'generic/platform=iOS Simulator' -quiet`
  (scheme from `xcodebuild -list -project iosApp/iosApp.xcodeproj` if it isn't `iosApp`; `-workspace` if the project
  uses one). This runs the Gradle pre-build phase that builds the `Shared` framework, so it's slow — run it only when
  Swift or the manifest actually changed. It builds but never boots a simulator, so it needs no lock. Unverified
  locally by this skill's author (see "Verification notes").

Outcomes:

- **Failure in code this task wrote or edited**: fix it — it's the task's own code, not a finding to defer.
- **Failure outside the task's scope** (a sibling task's in-flight edit, a pre-existing error): don't fix unrelated
  code; re-run once if it looks like a transient race with a concurrently-writing sibling, then note it in Step 8.
- **Gradle can't run at all** (no SDK, no network for the first dependency/Kotlin/Native toolchain download, no
  wrapper): report "compile-check unavailable" with the reason — the group's validation still catches real errors.
  A first run downloads the Kotlin/Native toolchain (hundreds of MB) and can take many minutes; that is not a hang.

## Step 6 — When to interrupt the user

Keep interruptions rare. Stop and use `AskUserQuestion` (or plain text if no real choice is offered) only when:

- The task is ambiguous in a way that changes correctness or scope and can't be safely inferred.
- The task's approach is infeasible against the real code (it names a type/member that doesn't exist, or demands a
  platform API in `commonMain`).
- The task needs a new dependency, Gradle plugin (SKIE, KMP-NativeCoroutines, Mokkery, Koin, SQLDelight, Room, a
  Ktor engine), Kotlin target, or an Android host-test source set the module doesn't configure.
- The task needs a secret embedded in the app (`reference/security.md`) — that's a design problem to report.
- A public API change would break Swift callers in a way the task didn't anticipate and the right Swift-side change
  isn't obvious.

Don't stop merely because the task is nontrivial. Don't report the task done to work around a blocker; report it as
blocked (Step 8). A conflict between `reference/` (other than `mandatory-rules.md`) and the surrounding code is not a
reason to stop: follow the surrounding code and report the divergence.

## Step 7 — Check off this task's checkbox now

If this task did not stop on a blocker, update `implementation_plan.md` at the repository root before reporting back.
Re-read it fresh (sibling tasks may be editing it), locate this task's own checkbox line by the exact text passed in,
flip `[ ]` to `[x]` for it and every sub-task the work covered, and add a short note naming the module(s)/source sets
and files touched, e.g.:

```
- [x] Task 3. **Add `SecureStore` with Keychain/Keystore actuals** — commonMain interface + androidMain/iosMain
  implementations, commonTest fake + iosTest; group validation pending.
```

Keep the "group validation pending" wording — `iru-kmp-code-one-task-group` replaces it with the final outcome. Edit
only this task's own line(s). If this task stopped on a blocker, leave its checkbox untouched.

## Step 8 — Report the outcome

Hand back a short summary:

- **The layout, Android plugin, and UI mode detected** (Step 0), and **the module(s)/source sets touched** (Step 1)
  with the reference files actually read.
- **The files touched** (including Swift files and `project.yml`) and **the tests added/updated per source set** (not
  run).
- **For a UI task**: the `Screen › Region › Component` decomposition, and the UI tests and screenshot captures
  (kind/Id/states, which platforms) added — none of them run yet.
- **The compile-check result per target** (Android / iOS / androidApp / iosApp build-for-testing): passed, failed on
  this task's code and fixed, failed outside this task's scope, or unavailable (and why — e.g. not macOS).
- **Public API changes visible to Swift**, and whether Swift callers were updated.
- **Whether this task stopped on a blocker**, with enough detail for the caller to surface it.
- **Any deliberate deviation from `reference/`**, and **pre-existing `mandatory-rules.md` violations** noticed and
  left alone (a `!!`, MockK in `commonTest`, a platform import in `commonMain`, a secret in source).

This skill never captures a quality baseline, adds license headers, runs tests/coverage/detekt/ktlint/Lint/SwiftLint,
runs Dokka, links the iOS framework, or boots a simulator/emulator.

## Verification notes

Exercised in `$TMPDIR/iru-verify/kmp/iru-kmp-code-one-task/` on macOS with JDK 21, Gradle 9.8.1 wrapper, Kotlin
2.4.21, AGP 9.4.1 (`com.android.kotlin.multiplatform.library`, `kotlin { android { … withHostTestBuilder {} } }`),
`iosArm64` + `iosSimulatorArm64` with a static `Shared` framework, kotlinx-coroutines 1.11.0, Turbine 1.2.1:

- `./gradlew :shared:tasks --all` listed `compileAndroidMain`, `compileAndroidHostTest`, `testAndroidHostTest`,
  `compileKotlinIosSimulatorArm64`, `compileTestKotlinIosSimulatorArm64`, `iosSimulatorArm64Test`, `allTests`,
  `linkDebugFrameworkIosSimulatorArm64`, `embedAndSignAppleFrameworkForXcode`, `embedSwiftExportForXcode`, and the
  default-hierarchy metadata tasks (`compileNativeMainKotlinMetadata`, `compileAppleMainKotlinMetadata`,
  `compileIosMainKotlinMetadata`).
- The Step 5 compile tasks succeeded for an `expect fun` with `androidMain`/`iosMain` actuals, a `commonMain` class
  using `Dispatchers.IO` (with `import kotlinx.coroutines.IO`), and `commonTest` tests with `runTest` + Turbine.
- `testAndroidHostTest` and `iosSimulatorArm64Test` ran the `commonTest` tests on both targets (JUnit XML under
  `shared/build/test-results/<task>/`); `iosSimulatorArm64Test` booted a simulator itself with none booted
  beforehand — the reason the group skill serializes it behind `.integration-test.lock`. `--tests` filters worked on
  both tasks. Backtick test names with spaces ran on both targets.
- `linkDebugFrameworkIosSimulatorArm64` produced `Shared.h`; the Objective-C mappings in `reference/ios-interop.md`
  (sealed → protocol + classes, `data object` → `.shared`, enum → class with statics, `doCopy`, dropped default
  arguments, `suspend` → completion handler, class-extension → category, interface-extension → static on the file
  class, `@ObjCName`, `@HiddenFromObjC`, `@Throws` documentation) were read from it. A `@Throws` on a `suspend`
  function without `CancellationException` compiled with no warning.
- Compose Multiplatform 1.12.2 (material3 1.9.0, components-resources): the `Res` class generated in
  `<rootProject>.<module>.generated.resources`, `stringResource(Res.string.x)` and
  `MainViewController() = ComposeUIViewController { App() }` compiled for iOS; a `runComposeUiTest` test in
  `commonTest` (with `org.jetbrains.compose.ui:ui-test`) passed under `iosSimulatorArm64Test` and failed with a
  `NullPointerException` under `testAndroidHostTest` (no Robolectric) — hence `reference/testing.md`'s placement rule.
- **Unverified locally**: the `androidTarget()` + `com.android.library` task names on AGP 9 (taken from the Kotlin
  docs), `androidApp`'s compile task names, `xcodebuild build-for-testing` against a real XcodeGen `iosApp` (no
  `iosApp` was generated here), SKIE/KMP-NativeCoroutines/Mokkery/Koin/SQLDelight/Room specifics (from their docs).
