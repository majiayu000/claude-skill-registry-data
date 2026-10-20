---
name: iru-setup-kmp-gitignore
description: >-
  Create or update the root `.gitignore` plus a per-module `.gitignore` (`/build`) for each Gradle module of a
  Kotlin Multiplatform (Android + iOS) app — the layout `iru-setup-kmp-app` produces (`shared/`, `androidApp/`,
  `iosApp/`) or the JetBrains wizard's older single `composeApp/` module — covering Gradle/Kotlin noise (`.gradle/`,
  `build/`, the Kotlin 2.x root `.kotlin/` cache), `local.properties`, Android Studio/IntelliJ/Fleet files, APK/AAB
  outputs, keystores and Apple signing material (`*.jks`, `*.keystore`, `*.p8`, `*.p12`, `*.mobileprovision`,
  `*.cer`), `google-services.json`/`GoogleService-Info.plist`, Xcode output (`DerivedData/`, `*.xcresult`,
  `xcuserdata/`, `*.xcuserstate`), the XcodeGen-generated `iosApp/iosApp.xcodeproj/` (only when `iosApp/project.yml`
  exists — a hand-maintained `.xcodeproj` stays tracked), CocoaPods `Pods/` (only when a `Podfile` exists), Fastlane
  output (only when a `fastlane/` directory exists), the Antora docs build output, and the UI tests' screenshot
  directory `.ui-screenshots/` (never `.ui-quality.yml`, which is committed). Invoke as
  `/iru-setup-kmp-gitignore`, optionally with `args`: `mode: new|existing` (default: detected from whether a root
  `.gitignore` already exists), `modules: <comma/space-separated list>` (default: every `include(":…")` entry in
  `settings.gradle.kts`, falling back to whichever of `shared`/`androidApp`/`composeApp` exist), and
  `on-existing: ask|keep|update|replace` (default `ask`). Announces whether it is creating from scratch or updating
  existing files; if a root or per-module `.gitignore` already exists it never overwrites it silently — it warns,
  shows a diff, and asks per file whether to Update (merge in what's missing, keep hand-added lines), Keep as is, or
  Replace (regenerate from the template, dropping customizations), unless `on-existing` decides. Mirrors
  `iru-setup-android-gitignore` + `iru-setup-swift-gitignore` merged for the KMP stack. Use whenever a Kotlin
  Multiplatform app repository needs a `.gitignore` bootstrapped from scratch, or an existing one checked/gap-filled
  against this house template without touching it unless the user approves.
model: haiku
---

# Setup KMP Gitignore

Create or refresh the root `.gitignore` and each Gradle module's own `.gitignore` for a Kotlin Multiplatform
(Android + iOS) app. The templates are the union of this catalog's two existing mobile gitignore skills —
`iru-setup-android-gitignore` (Gradle/Android Studio, genericized from irurueta-android-glutils) and
`iru-setup-swift-gitignore` (Xcode/SwiftPM) — trimmed to what a KMP app actually produces. Never overwrite an
existing `.gitignore` without showing the user exactly what would change and getting explicit approval first — a
`.gitignore` can carry hand-added, project-specific entries that must not be silently dropped.

## Step 0 — Resolve inputs

Parse `args` as `key: value` lines, skipping any question already answered:

- `mode: new|existing` — if omitted, detect it: a root `.gitignore` already present means `existing`; its absence
  means `new`. `mode: existing` never means "update silently" — every pre-existing file still goes through Step 6's
  Update / Keep as is / Replace question (unless `on-existing` decides it).
- `on-existing: ask|keep|update|replace` — how Step 6 treats each `.gitignore` that already exists. Default `ask`
  (one question per file). `keep`/`update`/`replace` applies that choice to every pre-existing file without asking
  (the warning is still printed). Only meant for scripted runs; an orchestrator passes it only if its own `args`
  received it.
- `modules: <list>` — comma- or space-separated Gradle module directories to give their own `.gitignore`. If
  omitted:
  1. If `settings.gradle.kts` (or `settings.gradle`) exists at the repository root, derive the list from every
     `include(":<name>")` line, stripping the leading `:` (nested `:a:b` → `a/b`):
     ```bash
     grep -oE 'include\(?["'"'"']:[^"'"'"']+' settings.gradle.kts settings.gradle 2>/dev/null \
       | sed -E "s/.*:([^\"']+).*/\1/" | tr ':' '/' | sort -u
     ```
  2. Otherwise (this skill run ahead of `iru-setup-kmp-app`), default to whichever of `shared`/`androidApp`/
     `composeApp` exist as directories; if none does, ask via `AskUserQuestion` (default `shared, androidApp`).
  `iosApp/` is never a Gradle module and never gets its own `.gitignore` — its build output is covered by the root
  file.

## Step 1 — Survey the repository

Detect the following before composing content — each gates a Step 4 conditional section:

- `iosApp/project.yml` (or any `project.yml` under the repository) → XcodeGen manifest: the `.xcodeproj` next to it
  is generated (`iru-setup-kmp-app` never commits it, matching `iru-setup-apple-app`'s convention).
- Any `*.xcodeproj`/`*.xcworkspace` already tracked (`git ls-files -- '*.xcodeproj' '*.xcworkspace'`) — a project
  that predates XcodeGen; never propose ignoring it unless a `project.yml` sits next to it (then flag the needed
  `git rm -r --cached`).
- `iosApp/Podfile` (or any `Podfile`) → CocoaPods in use; a `*.podspec` under `shared/` (the Kotlin CocoaPods
  plugin) → same.
- `fastlane/` or `iosApp/fastlane/` → Fastlane in use.
- `docs/antora.yml` or `docs/antora-playbook.yml` → Antora (its lines are unconditional anyway, see Step 2).
- Root `.gitignore` and each module's `.gitignore` — read them if present.

Tell the user which of the two this run is doing:

- **Creating from scratch** — no root `.gitignore` and no module `.gitignore`: write everything in Step 7 without
  asking.
- **Updating existing** — anything already exists: warn the user up front, listing each existing file by path,
  that Step 6 will ask per file whether to Update, Keep as is, or Replace it (or apply `on-existing`) rather than
  overwrite anything silently. Files absent alongside existing ones are still created from scratch.

## Step 2 — The root `.gitignore` base template

Unconditional — include it verbatim:

```gitignore
# Gradle
.gradle/
build/

# Kotlin compiler cache (created at the repository root by every Kotlin 2.x build)
.kotlin/

# Local configuration file (sdk path, etc)
local.properties

# Log/OS files
*.log
.DS_Store

# Android Studio / IntelliJ / Fleet
*.iml
.idea/
.fleet/
captures/
.externalNativeBuild/
.cxx/
output.json
deploymentTargetDropDown.xml
render.experimental.xml

# Build outputs
*.apk
*.aab
*.ipa
*.dSYM.zip

# Signing material — never commit (Android keystores, Apple keys/certificates/profiles)
*.jks
*.keystore
*.p8
*.p12
*.mobileprovision
*.cer

# Google Services / Firebase config
google-services.json
GoogleService-Info.plist

# Android profiling
*.hprof

# Xcode build output
DerivedData/
*.xcresult
xcuserdata/
*.xcuserstate

# Antora documentation build output (see iru-setup-antora)
docs/build/
docs/node_modules/

# Repository-wide lock serializing simulator/emulator test stages (iru-kmp-test, iru-kmp-code-one-task-group)
.integration-test.lock/

# UI tests' screenshot captures (regenerated on every UI test run; the docs commit only the ones they use)
.ui-screenshots/
```

Notes on specific lines:

- `build/` is **unanchored**, as in `iru-setup-android-gitignore`: it matches `shared/build/`, `androidApp/build/`,
  `iosApp/build/` (the `xcodebuild -derivedDataPath`/archive output the CI workflows write) and the root project's
  `build/reports/kover/` aggregate alike. That includes `shared/build/xcode-frameworks/` — the `Shared.framework`
  `:shared:embedAndSignAppleFrameworkForXcode` produces for Xcode is always rebuilt from source, never committed.
- `.kotlin/` is unconditional: Kotlin 2.x writes this cache (and its `sessions/`/`errors/` subfolders) at the root on
  every build.
- **No `*.jar` pattern anywhere** — `gradle/wrapper/gradle-wrapper.jar` must stay tracked, and the same rule
  `iru-setup-android-gitignore` documents for a vendored `jacoco-<ver>/lib/jacococli.jar` applies here. Before
  proposing any new line that could match `*.jar`, check it with `git check-ignore -v gradle/wrapper/gradle-wrapper.jar`
  and refuse to add it if it matches.
- `*.p8`/`*.p12`/`*.mobileprovision`/`*.cer` are unconditional (not gated on Fastlane), because Xcode's automatic
  signing or a CI step decoding `APP_STORE_CONNECT_API_KEY_BASE64` into `AuthKey.p8` can produce them without any
  `fastlane/` directory. `*.jks` covers `androidApp/release.jks`, the path `iru-setup-kmp-github-workflows`'
  release workflow decodes its keystore secret into.
- `.integration-test.lock/` is the atomic-`mkdir` lock directory (with its owner file) that `iru-kmp-test` /
  `iru-kmp-code-one-task-group` create around every stage that boots an iOS simulator or Android emulator — always
  transient, never committed.
- `.ui-screenshots/` holds the UI tests' captures (`<kind>/<Id>/<state>--<dir>--<theme>--<android|ios>.png`) that
  `iru-kmp-test` clears and rewrites on every full UI run — evidence for review, never committed (the documentation
  skills copy the ones they use into the Antora module's `images/ui/`). `.ui-quality.yml` is **not** ignored: it is
  committed configuration.
- `.swiftpm/` is deliberately absent — `iru-setup-kmp-app`'s iOS app has no SwiftPM package of its own. If the
  project later adds a local Swift package, add `.swiftpm/xcode/` (never the whole `.swiftpm/`, for the reason
  `iru-setup-swift-gitignore` documents).

## Step 3 — Per-module `.gitignore`

For each module resolved in Step 0, its own `.gitignore` is the single line `iru-setup-android-gitignore` uses
(anchored to the module root):

```gitignore
/build
```

## Step 4 — Detect project-specific root additions

Only add a section when Step 1 found what it targets:

- **XcodeGen-generated Xcode project** (`iosApp/project.yml` found):
  ```gitignore
  # Xcode project generated by XcodeGen (iosApp/project.yml) — regenerate with `xcodegen generate`
  iosApp/iosApp.xcodeproj/
  ```
  Use the directory/name of the `project.yml` actually found (XcodeGen names the project after the manifest's
  `name:` key — `iosApp` in `iru-setup-kmp-app`'s template). Skip entirely when there is no `project.yml`: a
  hand-maintained `.xcodeproj` (e.g. the JetBrains wizard's committed `iosApp/iosApp.xcodeproj`) is source and must
  stay tracked.
- **CocoaPods** (`Podfile` or a `shared/*.podspec` found):
  ```gitignore
  # CocoaPods
  Pods/
  ```
  The generated `*.xcworkspace` is left tracked unless a `project.yml` also generates the project (then the
  `.xcworkspace` is regenerated by `pod install` and may be ignored too — ask).
- **Fastlane** (`fastlane/` or `iosApp/fastlane/` found):
  ```gitignore
  # Fastlane
  fastlane/report.xml
  fastlane/Preview.html
  fastlane/screenshots/
  fastlane/test_output/
  ```
  (prefix each with `iosApp/` when that's where the directory lives).
- Don't invent entries beyond what was detected.

## Step 5 — Compose the proposed content

- **Root**: Step 2's base template plus the Step 4 sections that matched, each under its comment header, every line
  written **flush-left** — the Step 4 snippets are indented only because they sit under Markdown list items; git does
  not trim leading whitespace, so `  iosApp/iosApp.xcodeproj/` (two leading spaces) silently matches nothing
  (confirmed during verification). If a root
  `.gitignore` exists, merge: keep every existing line not already covered (hand-added ignores survive) and don't
  repeat a line already present verbatim.
- **Per module**: Step 3's `/build` line becomes the whole file, or is appended when missing from an existing
  module `.gitignore` (when it's already there, that module is skipped from Step 6 entirely).

## Step 6 — If anything already existed, warn and ask Update / Keep as is / Replace

Skip for every file Step 1 found absent — write it straight away.

For each file that already existed and whose proposed content differs from disk:

- Show the proposed **Update** content as a diff (write the draft to a temp path and run
  `git diff --no-index <current> <draft>`), for the root and every affected module file together. Say which
  hand-added lines a **Replace** would drop, and name any conflicting existing line (e.g. an existing
  `*.xcodeproj` ignore with no `project.yml` present, or a `*.jar` pattern that would hide the Gradle wrapper jar).
- Unless `on-existing` is `keep`/`update`/`replace` (apply it, still printing the warning and diff), ask via
  `AskUserQuestion`, one question per file (batch up to 4 per call), with the consequence in each option:
  - **Update (Recommended)** — "Merge: add the template lines this file is missing; keep every hand-added line.
    Your customizations survive."
  - **Keep as is** — "Leave the file untouched. Nothing you customized changes, but the missing lines in the diff
    (e.g. `.kotlin/`, `iosApp/iosApp.xcodeproj/`, `*.p8`) stay unignored — the report lists them."
  - **Replace** — "Overwrite with this skill's template only. Matches the house pattern exactly, but every
    hand-added line is lost (recoverable only from git history)."
  If the user wants only some lines, let them say so in free text and revise the draft.

## Step 7 — Write and report

Write the composed content to `.gitignore` and to `<module>/.gitignore` for each module. Then summarize:

- Whether this run created from scratch or updated existing files, and per file (root, each module) the action
  taken — **created / updated / replaced / kept as is** — and whether it came from the user or `on-existing`; for
  each file kept as is, the template lines it still lacks.
- Which Step 4 sections were included vs. skipped and why (e.g. "no CocoaPods section — no `Podfile`", "XcodeGen
  section included — `iosApp/project.yml` found, so `iosApp/iosApp.xcodeproj/` is ignored and must be regenerated
  with `xcodegen generate` after every clone").
- Confirmation that `git check-ignore gradle/wrapper/gradle-wrapper.jar` still exits `1` (not ignored).

**Warn explicitly**:

- Review every generated/updated `.gitignore` before committing — detection is heuristic.
- Files already tracked under a newly ignored path (e.g. a previously committed `iosApp/iosApp.xcodeproj/`) need
  `git rm -r --cached <path>` — writing `.gitignore` alone never untracks anything.
- Never commit keystores, `.p8`/`.p12` keys, provisioning profiles or `google-services.json`/
  `GoogleService-Info.plist`; CI decodes them from secrets at build time.

## Verification notes

Verified on 2026-10-15 in `$TMPDIR/iru-verify/kmp/iru-setup-kmp-gitignore/` (outside this repository): wrote the
composed root `.gitignore` (base template + the XcodeGen section) and `shared/.gitignore`/`androidApp/.gitignore`
into a `git init`-ed directory seeded with one file per pattern, then ran `git check-ignore -v` on each path:

| Path | Expected | Result |
|---|---|---|
| `shared/build/xcode-frameworks/Debug/iphonesimulator/Shared.framework/Shared` | ignored | ignored — `shared/.gitignore:/build` |
| `androidApp/build/outputs/apk/debug/app.apk` | ignored | ignored — `androidApp/.gitignore:/build` |
| `build/reports/kover/report.xml` | ignored | ignored — `.gitignore:build/` |
| `iosApp/build/DerivedData/x` | ignored | ignored — `.gitignore:build/` |
| `.kotlin/sessions/x` | ignored | ignored — `.gitignore:.kotlin/` |
| `.gradle/x`, `local.properties`, `.idea/x`, `.DS_Store` | ignored | ignored |
| `iosApp/iosApp.xcodeproj/project.pbxproj` | ignored | ignored — `.gitignore:iosApp/iosApp.xcodeproj/` |
| `iosApp/iosApp.xcodeproj/xcuserdata/u.xcuserdatad/x`, `x.xcresult/Info.plist` | ignored | ignored |
| `androidApp/release.jks`, `AuthKey.p8`, `cert.p12`, `profile.mobileprovision`, `cert.cer` | ignored | ignored |
| `androidApp/google-services.json`, `iosApp/iosApp/GoogleService-Info.plist` | ignored | ignored |
| `docs/build/site/index.html` | ignored | ignored — `.gitignore:docs/build/` |
| `.integration-test.lock/owner` | ignored | ignored — `.gitignore:.integration-test.lock/` |
| `.ui-screenshots/screen/X/default--ltr--light--ios.png` (re-checked 2026-10-16) | ignored | ignored — `.gitignore:.ui-screenshots/` |
| `.ui-quality.yml` (re-checked 2026-10-16) | **tracked** | **not ignored** |
| `gradle/wrapper/gradle-wrapper.jar` | **tracked** | **not ignored** |
| `iosApp/project.yml`, `iosApp/Configuration/Config.xcconfig`, `iosApp/iosApp/Info.plist`, `iosApp/.swiftlint.yml` | **tracked** | **not ignored** |
| `shared/src/commonMain/kotlin/x/Greeting.kt`, `docs/antora.yml`, `detekt.yml`, `gradle/libs.versions.toml` | **tracked** | **not ignored** |

The `modules:` detection one-liner in Step 0 produced `androidApp`, `shared` against `iru-setup-kmp-app`'s generated
`settings.gradle.kts`. The CocoaPods and Fastlane sections are the sibling skills' verified patterns, reused
unchanged — re-checked here only with `git check-ignore` (`Pods/x` → `Pods/`, `fastlane/report.xml` → itself). One real
pitfall surfaced: the first pass copied the Step 4 snippets with their Markdown list indentation, and
`iosApp/iosApp.xcodeproj/project.pbxproj` and `Pods/x` were **not** ignored until the two leading spaces were stripped —
hence Step 5's flush-left rule.
