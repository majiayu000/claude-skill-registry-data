---
name: iru-setup-kmp-repository
description: >-
  End-to-end bootstrap for a Kotlin Multiplatform (Android + iOS) app repository — collects `ui`
  (`compose` = Compose Multiplatform shared UI, `native` = Jetpack Compose on Android + SwiftUI on iOS over shared
  logic; asked via `AskUserQuestion` when absent), `branching` (`gitflow`/`main-only`), the app's identity
  (`app-name`, `application-id`, `bundle-id`, `namespace`, plus license and developer name/email/organization URL),
  and the shared pipeline parameters (integration branch `develop`, stable branch `main`, Java `17`, min SDK `26`,
  iOS deployment target, `open-source`, the repository `visibility` (detected via `gh repo view` or asked), `ci`,
  `ios-ci` (when the ~10×-cost macOS job runs: `all`/`stable`/`none`), `ci-tests` (`unit`, or `full` = also the
  iOS app's XCTest bundle on a simulator), `pages` (GitHub Pages vs. a workflow artifact for the Antora + Dokka
  docs), `distribution` (`none`/`internal`/`store` — Google Play/Firebase + TestFlight), `accessibility`
  (`enforce`/`report`/`off`/`none` — the UI tests' automated accessibility level, written by the scaffold to
  `.ui-quality.yml`), `sonar` plus its detail keys — each question stating the Actions-minutes / macOS-multiplier / SonarCloud / Pages cost facts for that
  visibility) once, prints a setup-mode statement (from scratch, or an inventory of the prior setup it found), then
  orchestrates `iru-setup-kmp-app` → `iru-setup-antora` → `iru-setup-kmp-gitignore` → `iru-setup-kmp-github-workflows`
  → `iru-setup-changelog` → `iru-setup-readme`, in that order, via `iru-isolated-skill-executor`, so nothing is
  asked twice — skipping the workflows step entirely (security block included) when `ci: no`. Invoke as
  `/iru-setup-kmp-repository`, optionally with `args` (`key: value` lines) to pre-resolve `ui`, `branching`, `mode`
  (`new`/`existing`), `open-source`, `visibility`, `ci`, `ios-ci`, `ci-tests`, `pages`, `accessibility`, `on-existing`
  (`ask`/`keep`/`update`/`replace`, forwarded only when supplied), `distribution`, `sonar` (+ `sonar-organization`/
  `sonar-project-key`/`sonar-host-url`), `integration-branch`, `stable-branch`, `java-version`, `min-sdk`,
  `compile-sdk`, `ios-deployment-target`, `runner`, `xcode-version`, `team-id`, and every identity field, skipping
  the matching question. On an existing repository every component sub-skill warns about the prior setup it owns
  and asks Update / Keep as is / Replace per file (unless `on-existing` decides), and the final report states the
  action taken per component. Use whenever bootstrapping (or catching up) a Kotlin Multiplatform mobile app
  repository's full Gradle/Xcode/docs/gitignore/CI/changelog/README scaffold in one pass, instead of running six
  skills separately and re-answering the same questions each time.
model: haiku
---

# Setup KMP Repository

Bootstrap a brand-new (or catch up an existing) Kotlin Multiplatform mobile app repository in one pass by
orchestrating six skills: `iru-setup-kmp-app` (the Gradle KTS project — `shared/` KMP module, `androidApp/`,
`iosApp/` XcodeGen project — with detekt/ktlint/Android Lint/Kover/Dokka/SwiftLint/Sonar wiring), `iru-setup-antora`
(Antora documentation site), `iru-setup-kmp-gitignore` (root and per-module `.gitignore`),
`iru-setup-kmp-github-workflows` (CI/CD + security workflows), `iru-setup-changelog` (root `CHANGELOG.md`), and
`iru-setup-readme` (root `README.md`). This skill does not duplicate any of their logic — it collects the shared
parameters once and passes each skill only the `args` keys that skill's own Step 0 actually accepts, so the user
isn't asked the same question twice and no sub-skill sees a key it doesn't recognize.

Each of Steps 4–9 invokes its sub-skill via the `iru-isolated-skill-executor` agent (`subagent_type:
"iru-isolated-skill-executor"`, always naming the full `iru-`-prefixed skill inside the prompt, e.g.
`Skill({skill: "iru-setup-kmp-app", args: "..."})`) rather than calling `Skill(...)` directly — every sub-skill
re-derives what it needs from the files the previous steps wrote, so only a short completion summary flows back,
keeping the scaffold's very long template listings out of this orchestrator's context. Every sub-agent is launched
with `run_in_background: false` — each step depends on the previous one's files being on disk.

Unlike `iru-setup-android-repository`/`iru-setup-swift-repository`, there is no `flavor` question: this catalog's
KMP setup only scaffolds **apps** (a shared KMP module consumed by an Android app and an iOS app). A KMP *library*
published to Maven Central is out of scope — say so if the user asks for one, and suggest
`iru-setup-java-library-repository`/`iru-setup-android-repository` for the publishing pipeline shape instead.

## Step 0 — Resolve inputs

Invoked stand-alone (`/iru-setup-kmp-repository`) or by the catalog's `iru-setup-repository` front door (project
type `kmp-app`), so parse `args` first, as `key: value` lines, one per line, e.g.:

```
ui: compose
branching: gitflow
mode: new
open-source: yes
visibility: public
ci: yes
ios-ci: all
ci-tests: full
pages: yes
distribution: store
accessibility: enforce
sonar: cloud
sonar-organization: example-org-github
sonar-project-key: example-org_my-kmp-app
sonar-host-url: https://sonarcloud.io
integration-branch: develop
stable-branch: main
java-version: 17
min-sdk: 26
ios-deployment-target: 18.0
```

Recognized keys:

- **Shape and mode**: `ui` (`compose`/`native`), `branching` (`gitflow`/`main-only`), `mode` (`new`/`existing`).
- **Shared pipeline vocabulary**: `open-source` (`yes`/`no`), `visibility` (`public`/`private`/`internal`), `ci`
  (`yes`/`no`), `ios-ci` (`all`/`stable`/`none`), `ci-tests` (`unit`/`full`), `pages` (`yes`/`no`), `on-existing`
  (`ask`/`keep`/`update`/`replace` — never asked; forwarded to the component sub-skills only when it arrived here
  via `args`), `distribution` (`none`/`internal`/`store`), `accessibility` (`enforce`/`report`/`off`/`none` — both `ui`
  values render UI, so it always applies), `sonar` (`cloud`/`self-hosted`/`none`) plus, only when
  set, `sonar-organization`/`sonar-project-key`/`sonar-host-url`, `integration-branch`, `stable-branch`,
  `java-version`, `runner` (macOS runner label), `xcode-version`.
- **Identity fields** named in Step 2: `app-name`, `application-id`, `bundle-id`, `namespace`, `project-name`,
  `version-name`, `version-code`, `team-id`, `license`, `developer-name`, `developer-email`, `organization-url`.
- **Platform toggles**, passed through to the scaffold untouched if supplied, otherwise left to its defaults:
  `min-sdk`, `compile-sdk`, `target-sdk`, `ios-deployment-target`.
- `publish` is accepted and ignored (an app has no Maven Central path) — note it in the report if supplied.

Every key found here is resolved — skip the matching question in Steps 1–3. If `args` is absent or doesn't look like
this format, treat everything as unset and ask normally.

## Step 1 — Resolve the UI shape, branching model and mode

Survey the repository root first — `settings.gradle.kts`, `shared/build.gradle.kts`, `androidApp/build.gradle.kts`,
`composeApp/build.gradle.kts`, `iosApp/project.yml`, `iosApp/*.xcodeproj` — since their presence decides `ui` and
`mode` without a question in the common cases.

Unless `ui` was supplied via `args`, resolve it:

- `shared/build.gradle.kts` applies `org.jetbrains.compose` (or `composeApp/` exists — the JetBrains wizard's
  Compose Multiplatform layout) → `compose`; `shared/` exists without it, and `iosApp/` has SwiftUI views over
  `import Shared` → `native`. Confirm the detected value with the user rather than assuming it silently.
- Nothing on disk yet → `AskUserQuestion` with two options:
  - **Compose Multiplatform (Recommended)** (`compose`) — "One Compose UI in `shared/commonMain`, rendered natively
    on Android and embedded on iOS through `ComposeUIViewController`. Most code shared; the iOS look is Material,
    not UIKit."
  - **Native UI** (`native`) — "`shared/` holds only logic/state; Android's UI is Jetpack Compose in `androidApp/`,
    iOS's is SwiftUI in `iosApp/`. Platform-native look and feel, two UIs to maintain."

A `composeApp/` single-module layout (the older wizard output) is **not** this skill's scaffold —
`iru-setup-kmp-app` will warn and offer to add its own modules alongside or stop; mention it now so the user isn't
surprised.

Unless `branching` was supplied via `args`, resolve it with `AskUserQuestion` (two options):

- **gitflow** (recommended, this catalog's house pattern) — an integration branch (`develop`, carrying
  `VERSION_NAME=x.y.z-SNAPSHOT` in `gradle.properties`) plus a stable branch (`main`, releases only);
  `iru-setup-kmp-github-workflows` generates `build.yml`/`release.yml`/`sync.yml`, and `sync.yml` opens the
  post-release version-bump PR back into the integration branch.
- **main-only** — a single stable branch; no `sync.yml`. Step 3's integration-branch question is skipped.

If `mode` wasn't supplied, check whether `settings.gradle.kts` (or any other artifact in the inventory below)
exists: if `settings.gradle.kts` does, default to `existing` and confirm with `AskUserQuestion` (`existing`
pre-selected; `new` as the other option, noting that either way every sub-skill still asks Update / Keep as is /
Replace for each file it owns that already exists); if nothing exists, default to `new` without asking.

### Setup mode

Right after resolving `mode`, print a short **Setup mode** statement:

- `mode: new` → "Setting up this repository **from scratch** — no prior setup found."
- `mode: existing` → "**Updating an existing repository** — prior setup found:" followed by an inventory table of
  every component this run owns, each marked **absent / present / partial** with the evidence (file paths):

  | Component | Evidence checked |
  |---|---|
  | Gradle build | `settings.gradle.kts`, root `build.gradle.kts`, `gradle.properties` (`VERSION_NAME`/`VERSION_CODE`), `gradle/libs.versions.toml`, the wrapper |
  | Shared module | `shared/build.gradle.kts` + `shared/src/{commonMain,commonTest,androidMain,androidHostTest,iosMain,iosTest}` (or a legacy `composeApp/`) |
  | Android app | `androidApp/build.gradle.kts` + `androidApp/src/` |
  | iOS app | `iosApp/project.yml`, `iosApp/Configuration/Config.xcconfig`, `iosApp/iosApp/`, `iosApp/iosAppTests/`, any committed `iosApp/*.xcodeproj` |
  | Quality config | `detekt.yml`, `.editorconfig`, `iosApp/.swiftlint.yml` |
  | UI quality config | `.ui-quality.yml` (`accessibility`/`directions`/`themes`) |
  | Sonar config | a `sonar {` block in the root `build.gradle.kts` |
  | Antora docs | `docs/antora.yml`, `docs/antora-playbook.yml`, `docs/modules/ROOT/` |
  | `.gitignore` | root `.gitignore`, `shared/.gitignore`, `androidApp/.gitignore` |
  | Workflows | each of `.github/workflows/build.yml`/`release.yml`/`sync.yml`/`security.yml`, `.github/scripts/sync_versions.py` |
  | Dependabot | `.github/dependabot.yml` |
  | `CHANGELOG.md` | root `CHANGELOG.md` |
  | `README.md` | root `README.md` |
  | `LICENSE` | root `LICENSE*` (reported only — no sub-skill here writes it) |

  Then: "For each component that already exists you'll be asked whether to keep it, update it, or replace it."
  Those questions are asked by the component sub-skills (Steps 4–9) — never by this orchestrator too.

## Step 2 — Collect the app's identity

**`mode: existing` with `settings.gradle.kts` already on disk**: skip every identity question — `iru-setup-kmp-app`
reads its defaults from the existing build files and `Config.xcconfig` when the user chooses Update or Replace
there, and `iru-setup-readme` derives identity from the files too. Resolve `license` only if `args` supplied it, and
record in the final report that identity was taken from the existing files.

Otherwise, for any field not resolved from `args`, ask directly (plain conversation — free text), using **exactly**
the key names `iru-setup-kmp-app` reads:

- **app-name** — the display name on both launchers (`strings.xml`'s `app_name`, `Config.xcconfig`'s `APP_NAME`).
- **application-id** — the Android `applicationId`, reverse-DNS (e.g. `com.example.myapp`).
- **bundle-id** — the iOS `PRODUCT_BUNDLE_IDENTIFIER`; offer `application-id` as the default.
- **namespace** — the Kotlin base package (shared code lives in `<namespace>`, the Android app in
  `<namespace>.android`); offer `application-id` as the default.
- **developer name**, **developer email**, **organizationUrl** — recorded by the scaffold's report and seen by
  `iru-setup-readme`/`iru-check-license`.
- Leave `version-name`/`version-code`/`project-name`/`team-id` unset unless `args` supplied them —
  `iru-setup-kmp-app` defaults them to `1.0.0-SNAPSHOT`/`1`/the repository name/empty (signing team picked in
  Xcode or supplied to CI later).

Then resolve the **license** with `AskUserQuestion`, unless `args` supplied one: MIT License (recommended for an
app) / Apache License 2.0 / No license (proprietary) / Other (ask name + URL afterward).

## Step 3 — Collect the pipeline parameters

Ask directly, presenting each default so a blank reply accepts it (skip any resolved from `args`, skip the
integration branch when `branching: main-only`, and skip every workflow-only row once `ci: no` is resolved — if
`ci` is still unresolved, ask the open-source/visibility/`ci` questions below first):

| Parameter | `args` key | Default | Consumed by |
|---|---|---|---|
| Integration branch | `integration-branch` | `develop` | `iru-setup-kmp-github-workflows` (gitflow only) |
| Stable branch | `stable-branch` | `main` | `iru-setup-kmp-github-workflows` |
| Java version | `java-version` | `17` | `iru-setup-kmp-github-workflows` (`actions/setup-java`) — the scaffold's JVM target is 17 |
| Min SDK | `min-sdk` | `26` | `iru-setup-kmp-app` |
| iOS deployment target | `ios-deployment-target` | resolved by `iru-setup-kmp-app` from the installed simulator runtimes | `iru-setup-kmp-app` — pass only if supplied |

Then resolve, with `AskUserQuestion`, in this order (skip any already resolved). Quote the cost facts "per GitHub's
current pricing" (verified October 2026 against docs.github.com) and tell the user to double-check their plan:

- **open-source** — Yes / No. Drives the recommended defaults below.
- **visibility** — if the repository has a GitHub remote, run `gh repo view --json visibility -q .visibility`
  (lowercase it) and tell the user the detected value; otherwise ask **Public** / **Private** (Public recommended
  when open source). Open source + private/internal is contradictory — warn and ask which is right. `internal`
  behaves like `private` below.
- **ci** — "Generate GitHub Actions workflows (CI/CD) for this repository?" Public: recommend **Yes** (standard
  GitHub-hosted runners are free for public repositories). Private/internal: offer **Yes** first but state that
  private repositories consume the account's included minutes — 2,000/month on GitHub Free, 3,000 on Pro and Team,
  50,000 on Enterprise Cloud — then are billed per minute (Linux 2-core $0.006, **macOS $0.062 — roughly 10×**), and
  that a KMP pipeline needs macOS for anything iOS. **No** = "no workflows — build, test and release locally
  (re-run `iru-setup-kmp-github-workflows` later)". `ci: no` ⇒ Step 7 is skipped entirely and `ios-ci`/`ci-tests`/
  `pages` aren't asked.
- **ios-ci** (only with `ci: yes`) — "When should the macOS job (Kotlin/Native iOS tests + the iOS app build) run?"
  - **Every push and pull request** (`all`) — recommended for public: complete verification on every change, free
    on a public repository.
  - **Stable branch and manual runs only** (`stable`) — recommended for private/internal: the Linux job (JVM/Android
    tests, Kover, detekt, ktlint, Android Lint) still runs on every push/PR; the iOS side only runs on pushes to
    the stable branch and `workflow_dispatch` — a single macOS run costs as much as ~10 Linux runs.
  - **Never** (`none`) — no macOS job at all; iOS is verified locally only (state plainly that iOS breakage then
    goes unnoticed by CI).
- **sonar** — "Configure SonarCloud / SonarQube and send CI analysis and coverage reports to it?"
  `cloud`/`self-hosted`/`none`. Recommend **`cloud`** only when open source **and** public; otherwise state that
  SonarCloud is free only for public/open-source projects (a private project needs a paid plan) and recommend
  **`none`**, offering **self-hosted** (Community Build is free, but you run the server). With `ci: no`, say nothing
  would send reports (only a manual `./gradlew sonar` with a token) and recommend `none`. For `cloud`/`self-hosted`
  collect `sonar-organization`/`sonar-project-key`/`sonar-host-url` the way `iru-setup-kmp-app`'s Step 2 does
  (SonarCloud: suggest `<owner>-github` / `<owner>_<repo>` / `https://sonarcloud.io` from `git remote get-url origin`).
- **ci-tests** (only with `ci: yes` and `ios-ci` ≠ `none`) — "Which iOS tests should CI run?"
  - **Unit tests only** (`unit`, recommended for private/internal) — "Kotlin/Native `iosSimulatorArm64Test` plus an
    `xcodebuild build` of the iOS app (proves it compiles and links the `Shared` framework); the app's XCTest
    bundle stays local."
  - **Unit + app tests** (`full`, recommended for public) — "Also `xcodebuild test` of `iosAppTests` on a simulator —
    complete verification, several more macOS minutes per run."
  (The Linux job always runs every JVM/Android host test; `ci-tests` only changes the macOS job.)
- **pages** (only with `ci: yes`) — public: **yes** without asking (say so in the report). Private/internal: ask —
  **No (Recommended)** ("CI still builds the Antora + Dokka docs and uploads them as a workflow artifact; nothing is
  published") vs **Yes** ("requires GitHub Pro, Team, or Enterprise Cloud; the site is PUBLIC unless you're on
  Enterprise Cloud with private Pages access control").
- **distribution** — `none`/`internal`/`store`. Default **`store`** when open source; otherwise ask with
  **`internal`** recommended. `internal` = Firebase App Distribution for Android + TestFlight (internal testers)
  for iOS; `store` = Google Play + TestFlight/App Store Connect; `none` = local installs only.

- **accessibility** — "Support accessibility and assistive technologies?" **Enforce (Recommended)** ("violations fail the
  UI tests") / **Report only** ("listed in test reports, never failing") / **Off** ("not run; the coding defaults
  still apply"). **None — opt out entirely** ("no accessibility rules, checks or docs"; written as `accessibility: none`). In `mode: existing`, pre-select from `iru-explore`'s `Accessibility:` line per `iru-setup-repository`'s `reference/accessibility-detection.md` (`present` → Enforce, `partial` → Report only with a mixed-compliance warning, `absent` → None) and never silently flip an existing `.ui-quality.yml` value. Written by `iru-setup-kmp-app` to `.ui-quality.yml`; asked once here alongside the other shared
  inputs, never again by the scaffold.

These values pass through unchanged to Step 4 (`iru-setup-kmp-app`) and Step 7 (`iru-setup-kmp-github-workflows`),
so neither re-asks them — and the workflows never run a `sonar` step against a build with no `sonar {}` block.

## Step 4 — Run `iru-setup-kmp-app`

Always invoke it, in either `mode`. When scaffold files already exist it announces that it is updating and asks,
per file group, Update / Keep as is / Replace / Stop itself (unless `on-existing` decides). Format Steps 2–3's
answers as `key: value` lines using exactly the keys it accepts:

```
Agent({
  description: "Run iru-setup-kmp-app",
  subagent_type: "iru-isolated-skill-executor",
  prompt: "Invoke Skill({skill: \"iru-setup-kmp-app\", args: \"ui: <ui>\\napp-name: <app-name>\\n
    application-id: <application-id>\\nbundle-id: <bundle-id>\\nnamespace: <namespace>\\n
    project-name: <..., only if supplied>\\nmin-sdk: <min-sdk>\\ncompile-sdk: <..., only if supplied>\\n
    target-sdk: <..., only if supplied>\\nios-deployment-target: <..., only if supplied>\\n
    version-name: <..., only if supplied>\\nversion-code: <..., only if supplied>\\nteam-id: <..., only if supplied>\\n
    license: <license display name, or 'none'>\\ndeveloper-name: <developer-name>\\n
    developer-email: <developer-email>\\norganization-url: <organization-url>\\nopen-source: <open-source>\\n
    visibility: <visibility>\\nci: <ci>\\nsonar: <sonar>\\nsonar-organization: <..., if set>\\n
    sonar-project-key: <..., if set>\\nsonar-host-url: <..., if set>\\ndistribution: <distribution>\\n
    accessibility: <accessibility>\\nmode: <mode>\\non-existing: <..., only if supplied via args>\"}). Report back: whether it scaffolded from scratch
    or updated an existing project, the action taken per file group (created / updated / replaced / kept as is, or
    that the user chose Stop), which toolchain versions came from a live lookup versus the recorded fallback, the
    compile-sdk and iOS deployment target it resolved, and the pass/fail/unverified result of each verification
    command it ran (Gradle check set, koverVerify, iOS framework link, xcodegen, xcodebuild).",
  run_in_background: false
})
```

Omit every `only if supplied` line whose value wasn't resolved (never send an empty key). It doesn't accept
`branching`, `integration-branch`, `stable-branch`, `java-version`, `ios-ci`, `ci-tests`, `pages`, `runner` or
`xcode-version` — those are Step 7's alone. If it reports **Stop**, stop here too — there's no coherent project to
build docs or CI around yet. Warn the user before launching: the first Gradle run downloads Gradle, the Android SDK
platform, the Kotlin/Native toolchain (~1 GB) and every dependency — this is the slow step.

## Step 5 — Run `iru-setup-antora`

`Agent({description: "Run iru-setup-antora", subagent_type: "iru-isolated-skill-executor", prompt: "Invoke
Skill({skill: \"iru-setup-antora\"}) with no args (or, only if `on-existing` arrived via this orchestrator's own args,
args: \"on-existing: <on-existing>\" — the only key it accepts) — it derives the component name, title, and version
itself (rootProject.name in settings.gradle.kts; VERSION_NAME in gradle.properties with -SNAPSHOT stripped), and
asks Update / Keep / Replace itself if docs exist. Report back: created vs updated, the action taken, and whether
the site build succeeded.", run_in_background: false})`.

Run it before Step 7 so the workflows skill's survey finds `docs/antora.yml`/`docs/antora-playbook.yml` in place for
its Antora + Dokka docs job. If it asks for a starting version, answer with `VERSION_NAME` minus `-SNAPSHOT`
(`1.0.0` for the defaults).

## Step 6 — Run `iru-setup-kmp-gitignore`

`Agent({description: "Run iru-setup-kmp-gitignore", subagent_type: "iru-isolated-skill-executor", prompt: "Invoke
Skill({skill: \"iru-setup-kmp-gitignore\"}) with no args (or, only if `on-existing` arrived via this orchestrator's
own args, args: \"on-existing: <on-existing>\") — it derives the module list from settings.gradle.kts and detects
iosApp/project.yml (XcodeGen) itself. Report back only, per root and per-module .gitignore, the action taken
(created / updated / replaced / kept as is).", run_in_background: false})`.

Its `mode`/`modules` keys are deliberately left to its own detection (the `.gitignore`-presence check and the
`settings.gradle.kts` Step 4 just wrote are the precise signals). Run it after Steps 4–5 and before Step 7, so
`build/`, `.kotlin/`, `local.properties`, the generated `iosApp/iosApp.xcodeproj/`, keystores/`.p8` keys and the
Antora output are ignored before any CI report appears locally.

## Step 7 — Run `iru-setup-kmp-github-workflows`

**Skip entirely when `ci: no`** — no `.github/workflows/*`, no `security.yml`, no `.github/dependabot.yml`, no
`sync.yml`/`sync_versions.py`. Record it in Step 10 as "skipped (ci: no)", noting that the shared security block
(Dependabot, dependency-review, CodeQL, OSV-Scanner, gitleaks) was skipped with it and that
`/iru-setup-kmp-github-workflows` adds it later.

Otherwise:

```
Agent({
  description: "Run iru-setup-kmp-github-workflows",
  subagent_type: "iru-isolated-skill-executor",
  prompt: "Invoke Skill({skill: \"iru-setup-kmp-github-workflows\", args: \"branching: <branching>\\n
    integration-branch: <integration-branch, gitflow only>\\nstable-branch: <stable-branch>\\n
    java-version: <java-version>\\nios-ci: <ios-ci>\\nci-tests: <ci-tests, if resolved>\\n
    runner: <..., only if supplied>\\nxcode-version: <..., only if supplied>\\nopen-source: <open-source>\\n
    visibility: <visibility>\\npages: <pages>\\ndistribution: <distribution>\\nsonar: <sonar>\\n
    sonar-organization: <..., if set>\\nsonar-project-key: <..., if set>\\nsonar-host-url: <..., if set>\\n
    mode: <mode>\\non-existing: <..., only if supplied via args>\"}). Report back: whether it created the pipeline
    from scratch or updated an existing one; per file (build.yml, release.yml, sync.yml + sync_versions.py,
    security.yml, .github/dependabot.yml) the action taken (created / updated / replaced / kept as is, with any
    mismatch listed for a kept file, or Stop); when the macOS job runs; whether docs go to GitHub Pages or a
    workflow artifact; any open gap it flagged (missing docs/antora.yml, Apple team id); and the full
    required-secrets/settings table it produced.",
  run_in_background: false
})
```

Omit `integration-branch` for `main-only`, and `ci-tests` when `ios-ci: none`. The `security-*` keys are never
passed — the workflows skill's own defaults apply (note this once in Step 10). The shared `license`/`developer-*`/
`organization-url` keys are never passed either. A **Stop** there is reported, not treated as a failure — Steps
4–6's output stands on its own.

## Step 8 — Run `iru-setup-changelog`

`Agent({description: "Run iru-setup-changelog", subagent_type: "iru-isolated-skill-executor", prompt: "Invoke
Skill({skill: \"iru-setup-changelog\"}) with no args (or args: \"on-existing: <on-existing>\" only if it arrived via
this orchestrator's own args), working from the repository's own tag/release history. Report back only the action
taken on CHANGELOG.md (created — with the version range reconstructed — / updated / replaced / kept as is).",
run_in_background: false})`. Independent of Steps 4–7; run it before Step 9 so the README's Documentation section
sees it.

## Step 9 — Run `iru-setup-readme`

`Agent({description: "Run iru-setup-readme", subagent_type: "iru-isolated-skill-executor", prompt: "Invoke
Skill({skill: \"iru-setup-readme\", args: \"sonar: <sonar>\\nci: <ci>\\npages: <pages; no when ci is no>\\n
on-existing: <..., only if supplied via args>\"}) — those are the only keys it accepts — deriving everything else
from the repository (settings.gradle.kts, gradle.properties, shared/androidApp build files, iosApp/project.yml and
Config.xcconfig, the Antora docs, the workflows, the sonar {} block, CHANGELOG.md). Report back only which sections
were included vs. omitted and why.", run_in_background: false})`. Run it last so badges/status table/documentation
links see the finished state. A KMP app has no dependency snippet — its Installation section is a "build and run
locally" (Android Studio / `./gradlew :androidApp:installDebug`; `xcodegen generate` + Xcode) or store-listing
section.

## Step 10 — Report

Summarize all six delegated skills together: repeat the **Setup mode**, the resolved `ui`, `branching` and `mode`,
the app identity and license, and the pipeline parameters actually applied. Then a per-component table — Gradle
build files, `shared/`, `androidApp/`, `iosApp/`, quality config, `.ui-quality.yml` (with the `accessibility` level it
holds), the Antora site, each `.gitignore`, each workflow
file + `sync_versions.py`, `.github/dependabot.yml`, `CHANGELOG.md`, `README.md` — with the action taken for each:
**created / updated / replaced / kept as is / skipped (ci: no)** (or not reached, after a Stop), and for anything
kept as is, the mismatches its sub-skill listed.

State explicitly what was wired or deliberately omitted, and why:

- **`ui`**: `compose` (shared Compose Multiplatform UI) or `native` (Jetpack Compose + SwiftUI).
- **`open-source`** / **`visibility`** (and whether visibility came from `args`, `gh repo view`, or a question).
- **`ci`**: with `no`, no workflows/`security.yml`/Dependabot were generated; `/iru-setup-kmp-github-workflows` adds
  them later.
- **`ios-ci`**: `all`/`stable`/`none` — when the macOS job runs, restating the ~10× macOS cost on private
  repositories (or, for `none`, that iOS is verified only locally).
- **`ci-tests`**: `unit`/`full` — whether CI runs the iOS app's XCTest bundle.
- **`pages`**: `yes` (Antora + Dokka deployed to GitHub Pages) or `no` (uploaded as a workflow artifact).
- **`distribution`**: which release jobs and signing secrets exist (Play/Firebase, TestFlight).
- **`accessibility`**: the level written to `.ui-quality.yml` (`enforce`/`report`/`off`/`none`) and that the UI tests
  capture `.ui-screenshots/` (gitignored; CI uploads it as a 7-day artifact).
- **`sonar`**: whether the root `sonar {}` block and the CI Sonar step were included; if `none`, whether that's the
  expected default or a user choice; if configured with `ci: no`, that no CI step sends reports.
- **Toolchain versions**: which came from a live lookup versus a recorded fallback (scaffold and workflows).

Unless Step 7 was skipped, reproduce the **required-secrets/settings table** `iru-setup-kmp-github-workflows`
reported, verbatim (it's already scoped to these options), plus its repository-settings notes (Pages source =
GitHub Actions for `pages: yes`; "Workflow permissions" allowing Actions to create pull requests for gitflow's
`sync.yml`). Add the local-only files the scaffold never writes: `local.properties` (`sdk.dir=`), and
`androidApp/google-services.json` if Firebase is later added.

List every decision made on the user's behalf: the MIT-first license recommendation, `bundle-id`/`namespace`
defaulted from `application-id`, `version-name`/`version-code`/`team-id` left to the scaffold's defaults,
`java-version` feeding only the workflows, the iOS deployment target resolved by the scaffold, `pages` defaulted
to `yes` for a public repository, `ios-ci`'s visibility-based recommendation, and the `security-*` flags left at
their defaults.

Finish with an explicit **Warn explicitly** block, repeating each sub-skill's closing warning:

- **Review every generated/updated file before building, committing, or relying on CI.** Confirm the license
  matches a root `LICENSE` (`iru-check-license` can generate one and backfill headers), and that
  `./gradlew build` and `cd iosApp && xcodegen generate` + an Xcode build succeed locally.
- `iosApp/iosApp.xcodeproj` is generated and gitignored — every clone (and CI) runs `xcodegen generate` first.
- Branch names, signing and store setup in the workflows were inferred — do a `workflow_dispatch` dry run before a
  real release.
- Every secret in the table, the SonarCloud project, the Google Play Console service account / Firebase project,
  and the App Store Connect API key + Apple Developer team must exist before CI can pass — nothing here creates
  accounts or credentials.
- If `java-version` was overridden from `17`, the scaffold's `jvmTarget`/`sourceCompatibility` still say 17.
- The Sonar scan, Play/Firebase/TestFlight uploads, CodeQL's analysis and the macOS runner jobs are never
  exercised locally by any of the six skills — only their YAML is validated.
