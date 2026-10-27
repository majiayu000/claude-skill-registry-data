---
name: iru-setup-android-app
description: "Invoked as /iru-setup-android-app with optional key: value args, usually by iru-setup-android-repository. Scaffolds a single-module Android application (Gradle Kotlin DSL, Compose or Views, signing, BuildConfig fields, unit-test and UI-test tooling, optional Sonar). Never generates Maven Central publishing; libraries use iru-setup-android-library."
model: sonnet
---

# Setup Android App

Generate a complete, buildable Gradle Kotlin-DSL Android application project — wrapper, root build files, and a
single `app/` `com.android.application` module — from explicit example templates embedded in this skill (Step 5)
that are genericized from **https://github.com/albertoirurueta/irurueta-android-glutils**, a real Android
repository whose Gradle toolchain (root `build.gradle.kts`, `settings.gradle.kts`, `gradle.properties`,
`gradle/libs.versions.toml`, `gradle/wrapper/gradle-wrapper.properties`) and `app/` module this skill's templates
are drawn from line for line, with only project-identity fields turned into `<placeholder>` markers. This skill is
self-contained: it does not read or reference `iru-setup-android-library`'s files at run time, even though a
companion `iru-setup-android-library` skill draws its own toolchain templates from the same reference repository —
if a repository ends up with both a `lib/` and an `app/` module, run each skill once and reconcile the two
generated `settings.gradle.kts`/root `build.gradle.kts` files by hand (Step 8 calls this out).

Exceptions to "genericized": `com.irurueta:irurueta-android-test-utils` (Gradle catalog alias `irurueta-test-utils`)
is kept as a real third-party Robolectric/MockK test-helper dependency, exactly as the reference repository uses
it — it is not a placeholder.

This skill produces only the `app/` module. It never writes a `mavenPublishing {}` block, a `sign`/publish CI
profile, or anything that assumes the output is redistributed as a library artifact — release builds are meant to
be installed on a device or uploaded to a store, not published to Maven Central.

## Step 0 — Resolve inputs

This skill can be invoked stand-alone (`/iru-setup-android-app`) or as a step inside another skill (e.g. a future
`iru-setup-android-app-repository` or the catalog's `iru-setup-repository` front door), which resolves these same
inputs itself and passes them through `args` as `key: value` lines, one per line, e.g.:

```
application-id: com.example.myapp
namespace: com.example.myapp
app-name: My App
min-sdk: 26
compile-sdk: 36
target-sdk: 36
version-name: 1.0.0
version-code: 1
license: Apache License 2.0
developer-name: Jane Doe
developer-email: jane@example.com
organization-url: https://github.com/example-org
open-source: yes
sonar: cloud
sonar-organization: example-org-github
sonar-project-key: example-org_my-app
sonar-host-url: https://sonarcloud.io
ui: compose
distribution: store
built-in-kotlin: no
junit: 4
coverage-tool: jacoco
static-analysis: lint
accessibility: enforce
visibility: public
ci: yes
mode: new
on-existing: ask
```

Parse any such lines from `args` now. Every field found here is resolved — skip asking about it in Step 2. Only
fields genuinely missing from `args` still need a question. If `args` is absent or doesn't look like this format,
treat everything as unset and ask normally.

Recognized keys: `application-id`, `namespace` (defaults to `application-id` if omitted), `app-name`, `min-sdk`
(default `26`), `compile-sdk`/`target-sdk` (default: the current stable Android API level, looked up in Step 4),
`version-name` (default `1.0.0`), `version-code` (default `1`), `license`, `developer-name`, `developer-email`,
`organization-url`, `open-source` (`yes`/`no`), `sonar` (`cloud`/`self-hosted`/`none`) plus, only when `sonar` is
`cloud` or `self-hosted`, `sonar-organization`/`sonar-project-key`/`sonar-host-url`, `ui` (`compose`/`views`),
`distribution` (`none`/`internal`/`store`), `built-in-kotlin` (`no`/`yes`), `junit` (`4`/`5`), `coverage-tool`
(`jacoco`/`kover`), `static-analysis` (`lint`/`lint+detekt+ktlint`), `accessibility` (`enforce`/`report`/`off`/`none`,
default `enforce` — the automated accessibility level of the UI tests, written to `.ui-quality.yml`), `visibility` (`public`/`private`/`internal` —
GitHub repository visibility, only used to pick the `sonar` recommendation in Step 2), `ci` (`yes`/`no` — whether
CI workflows will exist to send Sonar reports; only used by Step 2's `sonar` question), `mode` (`new`/`existing`),
and `on-existing` (`ask`/`keep`/`update`/`replace`, default `ask`).

`mode: existing` is this catalog's shared signal (set by a front door that already ran `iru-explore` and knows this
is an established repository). It no longer means "gap-fill silently": Step 1 still warns about, and asks about,
every pre-existing file group. Only `on-existing` skips that question — `keep` (create only missing files, leave
every existing one untouched — the old `mode: existing` behaviour), `update`, or `replace` is then applied to every
pre-existing file group without asking (the warning is still printed). `on-existing` is meant for scripted runs; an
orchestrator passes it only if its own `args` received it.

**Accessibility level `none` and assistive-technology templates.** `accessibility` takes `enforce`, `report`, `off` or
`none` (UI contract §8; the stand-alone question gains a fourth option, **None — opt out entirely**, e.g. a mandated
non-compliant design). With `none`: write `accessibility: none` to `.ui-quality.yml`, do not install or configure the
accessibility test tooling (the Accessibility Test Framework (ATF) audit), and omit the accessibility-specific attributes from the generated templates.
With `enforce`, `report` or `off`: include the assistive-technology attributes from the contract's §8 platform
subsections in every generated template — `contentDescription` (or `Modifier.semantics`) on icon buttons and images, `sp` font sizes, 48dp touch targets, TalkBack-friendly traversal — and, for `enforce`/`report` only, the automated checks. In
`mode: existing`, a prior `.ui-quality.yml` follows this skill's existing Update / Keep / Replace prompt and its
`accessibility` value is never silently flipped (**Update** sets it only when `args` supplied it).

**Templates.** The file templates of Step 5 are files under this skill's `templates/` directory, not inline text. Read only the template files for the `ui` variant resolved in Step 2 (`templates/common/` for both variants, plus `templates/compose/` or `templates/views/`; the index at the top of Step 5 says which applies); never read the other variant's files. The opt-in snippets (distribution, Detekt/Spotless, Kover, JUnit 5) stay inline in Step 5.

## Step 1 — Survey the repository

Check which of Step 5's files already exist at the repository root — above all `settings.gradle.kts` and
`app/build.gradle.kts`, but also root `build.gradle.kts`, `gradle.properties`, `gradle/libs.versions.toml`, the
Gradle wrapper files, `detekt.yml`, `.ui-quality.yml`, and the `app/` skeleton files (manifest, `proguard-rules.pro`, `res/` files,
`MainActivity.kt`/theme, test sources, `app/.gitignore`). Then tell the user which of the two this run is doing:

- **Scaffolding from scratch** — none exist: skip straight to Step 2. There is nothing to preserve.
- **Updating an existing Gradle project** — `app/build.gradle.kts` exists and applies `com.android.application`
  (this skill, or a hand-written equivalent, already owns this module), or any other of Step 5's files exists:
  warn the user, listing every file found by path, that each existing file group below will be decided
  individually (files that don't exist yet are still created from scratch alongside). This applies under
  `mode: existing` too.

  Group the existing files into these artifacts (only those with at least one file present):
  **`settings.gradle.kts`**, **root `build.gradle.kts`**, **`gradle/libs.versions.toml`**, **`gradle.properties`**,
  **the Gradle wrapper**, **`app/build.gradle.kts`**, **the `app/` skeleton** (manifest, `proguard-rules.pro`,
  `res/` files, `MainActivity.kt`/theme or layout, test sources including `testing/UiScreenshots.kt`,
  `app/.gitignore`), **`.ui-quality.yml`** (a conflict to name: its `accessibility` differs from this run's), and
  **`detekt.yml`** (only once
  Step 2 resolves `static-analysis: lint+detekt+ktlint` — ask about it after Step 2 in that case). Unless
  `on-existing` decides (Step 0), ask with `AskUserQuestion`, one question per artifact (batch up to 4 per call;
  further calls for the rest), naming any concrete conflict with this run's choices (e.g. "`app/build.gradle.kts`
  has a `sonar {}` block but you chose `sonar: none`", "it applies `com.google.firebase.appdistribution` but
  `distribution` is `store`"). Options, with the consequence in each description:
  - **Update (Recommended for the build files and the wrapper)** — "Merge: add what's missing and correct outdated
    parts using this skill's template as reference — missing plugins/version-catalog aliases, the `sonar {}` /
    `signingConfigs` / distribution-plugin blocks added or removed per this run's choices, toolchain versions
    bumped to Step 4's lookup; keep every dependency, product flavor, build type and option this skill doesn't
    own. You review a diff; your customizations survive, but a customized part this skill owns may be
    rewritten." For the `app/` skeleton, Update only creates its missing files.
  - **Keep as is (Recommended for the `app/` skeleton and `.ui-quality.yml`)** — "Leave the file(s) untouched. Nothing you customized
    changes, but they may stay out of date or disagree with this run's choices — the report will list each
    mismatch."
  - **Replace** — "Regenerate from this skill's template. Result matches this house pattern exactly, but every
    customization (dependencies, flavors, build types beyond Step 5's template) is lost — recoverable only from git
    history." Never the default. Even on Replace, never overwrite `app/src/main/java/**` application source beyond
    the placeholder files this skill created originally (detect by exact content match against Step 5's templates
    before overwriting any Kotlin file), and never touch `AndroidManifest.xml`'s `<application>` children beyond
    the one `<activity>` this skill adds.
  - **Stop** (first question only) — "End this skill now without changing any file." Report this and end here.

  Note in Step 8's report the action taken per artifact.
- **`settings.gradle.kts` exists but has no `app` module applying `com.android.application`, or `app/build.gradle.kts`
  exists and applies `com.android.library`**: this is not this skill's scaffold (a library-only or differently
  laid out project). Warn the user explicitly and ask whether to add an `app` module alongside the existing one, or
  stop. Don't attempt to convert an existing module.

## Step 2 — Collect the required inputs

For any field Step 0 already resolved from `args`, use that value directly and don't ask about it again. For
everything else, ask the user directly (plain conversation, pre-filling defaults found in Step 1 if updating an
existing scaffold):

- **application-id** — reverse-DNS application id, e.g. `com.example.myapp` (written to `defaultConfig.applicationId`
  and used to derive the Kotlin package path under `app/src/main/java/`).
- **namespace** — the module's Kotlin/resource namespace (`android.namespace`); defaults to `application-id` if the
  user gives none — offer that as the default rather than asking open-endedly. (`namespace` and `applicationId` are
  independent in modern AGP — a namespace change alone never changes what's installed on a device — but keeping
  them equal is the common case and this skill's default.)
- **app-name** — the display name shown under the launcher icon (`strings.xml`'s `app_name`).
- **min-sdk** — default `26` (Android 8.0). `26` is also the API level adaptive launcher icons were introduced at,
  which is why Step 5's icon template needs no legacy raster fallback (see that step's note).
- **compile-sdk**/**target-sdk** — default to the current stable Android API level, looked up in Step 4; offer that
  looked-up value as the default rather than asking open-endedly. `target-sdk` defaults to the same value as
  `compile-sdk` unless the user wants to target an older platform behavior deliberately.
- **version-name** — default `1.0.0` (Android apps don't use Maven's `-SNAPSHOT` convention; `iru-android-bump-version`
  is the skill that later rewrites this).
- **version-code** — default `1` (a plain monotonically increasing integer, not derived from `version-name`).
- **Developer name**, **developer email**, **organizationUrl** — recorded in Step 8's report only; unlike
  `iru-setup-android-library`, no `pom`/`mavenPublishing` block exists here to put them in.

Then, unless Step 0 already resolved a `license` value from `args`, ask about the **license** with
`AskUserQuestion` (mirrors this catalog's other setup skills):

- MIT License (recommended for app source not meant for redistribution as a library)
- Apache License 2.0
- No license (proprietary / all rights reserved)
- Other — ask for the license's display name and URL directly afterward

If a license is chosen (anything but "No license"), remind the user in Step 8 to also add a matching `LICENSE`
file at the repository root if one doesn't exist yet — `iru-check-license` can verify/backfill source headers
against it once it's there.

Then, unless Step 0 already resolved them, ask about **ui**, **built-in-kotlin**, **junit**, **coverage-tool**,
**static-analysis**, and **accessibility** as bounded choices (`AskUserQuestion`, max four options each):

- **ui** — `compose` (recommended default; Jetpack Compose Material 3, matches this catalog's other app-flavor
  skills like `iru-setup-react-native-app`) or `views` (classic `AppCompatActivity` + XML layout + ViewBinding, no
  Compose runtime at all — pick this only when the user explicitly wants the older View system, e.g. to match an
  existing design-system investment). Gates which of Step 5's `MainActivity`/layout templates get written, and
  whether `kotlin-compose`/`androidx-compose-bom`/`androidx-material3` are in the version catalog at all.
- **built-in-kotlin** — `no` (default, matches the reference project's `android.builtInKotlin=false`) or `yes` (opts
  into AGP's built-in Kotlin compilation support instead of the separate `org.jetbrains.kotlin.android` plugin —
  still experimental as of AGP 9.x; only recommend `yes` if the user explicitly wants to try it).
- **junit** — `4` (default; Robolectric + MockK + JUnit 4, exactly as the reference project) or `5` (adds the
  `de.mannodermaus.android-junit` plugin so `app/src/test` can also use JUnit 5 Jupiter alongside the JUnit-4-only
  Robolectric runner — see Step 5's opt-ins).
- **coverage-tool** — `jacoco` (default; AGP's built-in `create<Variant>UnitTestCoverageReport` task, no extra
  plugin) or `kover` (adds `org.jetbrains.kotlinx.kover` for a Kotlin-native coverage report/verification DSL
  instead).
- **static-analysis** — `lint` (default; Android Lint only, already built into AGP) or `lint+detekt+ktlint` (adds
  Detekt for Kotlin static analysis and Spotless-driven ktlint formatting — see Step 5's opt-ins).
- **accessibility** — "Support accessibility and assistive technologies?": `enforce` (Recommended — Accessibility Test
  Framework violations fail the UI tests), `report` (listed, never failing), or `off` (not run; the coding
  defaults still apply). Written to `.ui-quality.yml` (Step 5).

Then resolve `open-source`, `sonar`, and `distribution` — skip any of the three Step 0 already resolved from
`args`. When invoked stand-alone with none of them pre-resolved, ask `open-source` *first* (`AskUserQuestion`:
yes/no) and derive the recommended default for `sonar` from that answer, per this catalog's shared convention:

- **open-source** — is this repository open source? Yes / No.
- **sonar** — whether to wire up a SonarQube/SonarCloud scan (this house pattern runs it via the `org.sonarqube`
  Gradle plugin, invoked as `./gradlew :app:sonar` — typically from the CI workflow `iru-setup-android-github-workflows`
  generates, so it's worth setting up here even if that workflow comes later). Recommend **SonarCloud** (`cloud`)
  only when open-source is Yes **and** `visibility` is `public` (or unset — this skill doesn't resolve `visibility`
  itself when invoked standalone; an unset value is treated as matching `open-source`); otherwise state that
  SonarCloud is free only for public/open-source projects (a private project needs a paid plan) and recommend
  **None** (`none`), offering **self-hosted SonarQube** (free Community Build, but you run the server) as the
  second option. If `ci: no` was supplied, say plainly that no CI workflow would send reports — analysis would only
  run when someone runs `./gradlew :app:sonar` manually with a token — and recommend `none`; if the user still
  picks `cloud`/`self-hosted`, write the `sonar {}` block only and note in Step 8 that no CI step sends reports:
  - `cloud` — ask for the `sonar.organization` key, offering `<owner>-github` (the owner parsed in Step 3) as the
    suggested default. Default `sonar.projectKey` to `<owner>_<repo>` and `sonar.host.url` to
    `https://sonarcloud.io`, confirming both with the user rather than assuming silently.
  - `self-hosted` — ask for `sonar.host.url` directly (no sensible default), plus `sonar.organization` only if that
    server has organizations enabled, and `sonar.projectKey`.
  - `none` — skip the entire `sonar { properties {…} } }` block and the `org.sonarqube` plugin (Step 5/6).
- **distribution** — `none`/`internal`/`store`:
  - `none` — release builds are for local install/manual QA only. No distribution plugin is added; `signingConfigs`
    is still written (Step 5) so a signed release build remains possible whenever the signing secrets exist, but
    nothing uploads it anywhere.
  - `internal` — adds the **Firebase App Distribution** Gradle plugin (`com.google.firebase.appdistribution`,
    version looked up in Step 4) to `app/build.gradle.kts`, so `./gradlew :app:appDistributionUploadRelease` can
    push a build straight to Firebase's tester groups. This needs a Firebase project: `google-services.json` (the
    Firebase config file, unique per Firebase project) is referenced but **never written by this skill** — it must
    be downloaded from the Firebase console and placed at `app/google-services.json`, and Step 5 gitignores it (it
    contains project-specific API keys/identifiers that shouldn't be committed). Step 8 flags the `FIREBASE_APP_ID`
    and a Firebase service-account credential (JSON key, typically stored as a CI secret and referenced via
    `--service-credentials-file` or the `FIREBASE_TOKEN`/`GOOGLE_APPLICATION_CREDENTIALS` env var) that a CI-driven
    upload will need.
  - `store` — full Google Play production submission is intended. Ask via `AskUserQuestion` **how** the upload
    should happen (bounded choice, two options):
    - **Workflow-level action** (recommended default) — leave `app/build.gradle.kts` alone; the actual
      `r0adkll/upload-google-play@v1` GitHub Actions step is generated later by
      `iru-setup-android-github-workflows` when it renders the release workflow for `distribution: store`. This
      skill only records the choice (Step 8) so that skill doesn't have to ask again.
    - **Gradle Play Publisher plugin** — adds `com.github.triplet.play` (`com.github.triplet.play` id, version
      looked up in Step 4) to `app/build.gradle.kts` with a minimal `play { serviceAccountCredentials.set(file(<path>)) }`
      block (Step 5), so `./gradlew :app:publishBundle` can upload directly from any machine/CI runner that has the
      service-account JSON, without depending on the `upload-google-play` Action at all. Either choice needs the
      same underlying Google Play service-account JSON key — this skill never collects or stores it, only names it
      in Step 8's report.

## Step 3 — Infer repository information

Don't ask for these — derive them from the current repository, the same way `iru-setup-java-library` and
`iru-setup-react-native-app` do:

- **Owner/repo and host**: parse `git remote get-url origin` (handles both `git@host:owner/repo.git` and
  `https://host/owner/repo.git` forms). Used for Step 2's `sonar.organization`/`sonar.projectKey` defaults and
  `settings.gradle.kts`'s `rootProject.name`. If there's no `origin` remote yet, ask the user directly instead of
  leaving these blank.

## Step 4 — Look up toolchain versions

Every version below must be looked up at run time; fall back to the value in this table (what this skill's author
actually observed in September 2026) only when the lookup fails, and say so explicitly in Step 8's report.

| Component | Lookup | September 2026 fallback |
|---|---|---|
| Gradle | `https://services.gradle.org/versions/current` (`"version"`/`"checksum"` fields — `"checksum"` in that same JSON response is already the binary distribution's SHA-256, no second fetch needed; `"checksumUrl"` also works) | `9.7.1`, sha256 `acd53f1edaf02f1a8ff99879f8a34b302661a057d9b063ae9e35b552f804d20a` — **live-confirmed during this skill's verification**, and used as-is against AGP `9.0.1` below with no compatibility issue |
| Android Gradle Plugin (AGP) | `https://dl.google.com/dl/android/maven2/com/android/tools/build/gradle/maven-metadata.xml` (read the highest non-`-alpha`/`-beta`/`-rc` `<version>` entry — this AGP artifact's own metadata, not AAPT2's, and **not** its `<latest>`/`<release>` tags, which pointed at an alpha during this verification) | `9.0.1` — the reference project's own verified-working version; a live lookup during this verification found `9.4.0` already stable, but the fallback here is deliberately the older, *known-compatible-with-Kotlin-2.3.10* version actually built and tested for this skill (see the compatibility note below the table) |
| Kotlin | `https://repo1.maven.org/maven2/org/jetbrains/kotlin/kotlin-gradle-plugin/maven-metadata.xml` — **prefer this over `search.maven.org`'s `solrsearch` API**, confirmed stale below | `2.3.10` — likewise the version actually verified against AGP `9.0.1`/Compose BOM `2026.02.01` together, not the bare current release |
| Dokka | `https://repo1.maven.org/maven2/org/jetbrains/dokka/dokka-gradle-plugin/maven-metadata.xml` — same staleness caveat as Kotlin above | `2.1.0` |
| SonarQube Gradle plugin | `https://plugins.gradle.org/m2/org/sonarqube/org.sonarqube.gradle.plugin/maven-metadata.xml` | `7.2.3.7755` |
| JUnit 4 | `https://search.maven.org/solrsearch/select?q=g:junit+AND+a:junit&rows=1&wt=json` | `4.13.2` |
| AndroidX Test `junit`/`junit-ktx` | `https://dl.google.com/dl/android/maven2/androidx/test/ext/junit/group-index.xml` | `1.3.0` |
| AndroidX Espresso `espresso-core` | `https://dl.google.com/dl/android/maven2/androidx/test/espresso/espresso-core/group-index.xml` | `3.7.0` |
| AndroidX Compose BOM (only `ui: compose`) | `https://dl.google.com/dl/android/maven2/androidx/compose/compose-bom/group-index.xml` | `2026.02.01` |
| AndroidX `activity-compose` (only `ui: compose`; **not** covered by the Compose BOM, needs its own version) | `https://dl.google.com/dl/android/maven2/androidx/activity/group-index.xml` | `1.13.0` |
| `com.google.android.material:material` | `https://dl.google.com/dl/android/maven2/com/google/android/material/material/group-index.xml` | `1.13.0` |
| AndroidX Test `core-ktx` | `https://dl.google.com/dl/android/maven2/androidx/test/core/group-index.xml` | `1.7.0` |
| MockK (`mockk-android`) | `https://search.maven.org/solrsearch/select?q=g:io.mockk+AND+a:mockk-android&rows=1&wt=json` | `1.14.9` |
| Robolectric | `https://search.maven.org/solrsearch/select?q=g:org.robolectric+AND+a:robolectric&rows=1&wt=json` | `4.16.1` |
| `kotlin-reflect` | same as the Kotlin row above (kept in lockstep) | `2.3.10` |
| `com.irurueta:irurueta-android-test-utils` | `https://search.maven.org/solrsearch/select?q=g:com.irurueta+AND+a:irurueta-android-test-utils&rows=1&wt=json` | `1.3.2` |
| Current stable Android API level (`compile-sdk`/`target-sdk` default) | `sdkmanager --list` on the local SDK, or https://apilevels.com | `36` (Android 16) |
| Roborazzi (`roborazzi`, `roborazzi-compose` for `ui: compose`, `roborazzi-accessibility-check`; test scope only) | `https://repo1.maven.org/maven2/io/github/takahirom/roborazzi/roborazzi/maven-metadata.xml` (`<release>`) | `1.76.0` |
| Compose UI test (`ui-test-junit4`, `ui-test-manifest`, `ui-test-junit4-accessibility`; only `ui: compose`) | versioned by the Compose BOM above — no own row; `ui-test-junit4-accessibility` needs Compose 1.8+ (BOM 2025.04+) | — |
| Espresso accessibility (`espresso-accessibility`; only `ui: views`) | same version as `espresso-core` above (same `androidx.test.espresso` group-index) | `3.7.0` |
| Detekt (opt-in) | `https://plugins.gradle.org/m2/io/gitlab/arturbosch/detekt/io.gitlab.arturbosch.detekt.gradle.plugin/maven-metadata.xml` | `1.23.8` — **unverified locally**, confirm at run time |
| Spotless (opt-in) | `https://plugins.gradle.org/m2/com/diffplug/spotless/com.diffplug.spotless.gradle.plugin/maven-metadata.xml` | `7.2.1` — **unverified locally**, confirm at run time |
| Kover (opt-in, `coverage-tool: kover`) | `https://plugins.gradle.org/m2/org/jetbrains/kotlinx/kover/org.jetbrains.kotlinx.kover.gradle.plugin/maven-metadata.xml` | `0.9.2` — **unverified locally**, confirm at run time |
| `de.mannodermaus.android-junit` (opt-in, `junit: 5`) | `https://plugins.gradle.org/m2/de/mannodermaus/android-junit/de.mannodermaus.android-junit.gradle.plugin/maven-metadata.xml` `<release>` — the plugin id dropped its trailing `5` when the `mannodermaus/android-junit5` project was renamed `android-junit-framework`; a lookup against the old `de.mannodermaus.android-junit5` coordinate returns nothing (same finding as `iru-setup-android-library`) | `2.0.1` (the value `iru-setup-android-library` resolved) — **unverified locally by this skill**, confirm at run time |
| Firebase App Distribution plugin (opt-in, `distribution: internal`) | `https://plugins.gradle.org/m2/com/google/firebase/appdistribution/com.google.firebase.appdistribution.gradle.plugin/maven-metadata.xml` | `5.1.1` — **unverified locally**, confirm at run time |
| Gradle Play Publisher plugin (opt-in, `distribution: store` + plugin choice) | `https://plugins.gradle.org/m2/com/github/triplet/play/com.github.triplet.play.gradle.plugin/maven-metadata.xml` | `3.11.1` — **unverified locally**, confirm at run time |

**Compatibility over bare "latest", confirmed the hard way while verifying this skill:** looking up every artifact's
own individual latest version and combining them all is *not* the same as a combination someone has actually built.
This skill's fallbacks (AGP/Kotlin/Dokka/Compose BOM/etc.) are the reference project's own real, CI-verified
combination, not each package's independently-latest release — prefer that same discipline when a live lookup
succeeds too: resolve AGP/Kotlin/the Compose BOM together and sanity-check `./gradlew :app:assembleDebug` once with
the new versions before trusting them, rather than bumping each in isolation. `search.maven.org`'s `solrsearch`
API returned a stale `latestVersion` for both `kotlin-gradle-plugin` (`2.2.0`) and `dokka-gradle-plugin` (`2.0.0`)
during this verification, each already superseded by a newer stable release visible in Maven Central's own
`maven-metadata.xml` for the same artifact — treat `solrsearch` results as a hint, not ground truth, and prefer a
direct `maven-metadata.xml`/group-index fetch when precision matters (as it does for Kotlin/AGP compatibility).

## Step 5 — Reference templates

**Templates.** Every template below is a file under `templates/<variant>/<path of the generated file>` (`<package-path>` appears as `__package-path__` in directory names), holding the exact bytes of that generated file's template. Read only the files for the `ui` variant resolved in Step 2, each in full, before filling placeholders:

| Generated file | Template | Applies when |
|---|---|---|
| `gradle/wrapper/gradle-wrapper.properties` | `templates/common/gradle/wrapper/gradle-wrapper.properties` | always |
| `build.gradle.kts` | `templates/common/build.gradle.kts` | always |
| `settings.gradle.kts` | `templates/common/settings.gradle.kts` | always |
| `gradle.properties` | `templates/common/gradle.properties` | always |
| `gradle/libs.versions.toml (`[versions]` section)` | `templates/common/gradle/libs.versions.toml.versions` | always |
| `gradle/libs.versions.toml (`[libraries]` section)` | `templates/common/gradle/libs.versions.toml.libraries` | always |
| `gradle/libs.versions.toml (`[plugins]` section)` | `templates/common/gradle/libs.versions.toml.plugins` | always |
| `app/build.gradle.kts` | `templates/common/app/build.gradle.kts` | always (gated blocks inside it follow `ui`, `sonar`, `distribution`, `coverage-tool`) |
| `app/proguard-rules.pro` | `templates/common/app/proguard-rules.pro` | always |
| `app/src/main/AndroidManifest.xml` | `templates/common/app/src/main/AndroidManifest.xml` | always |
| `app/src/main/res/values/colors.xml` | `templates/common/app/src/main/res/values/colors.xml` | always |
| `app/src/main/res/values/strings.xml` | `templates/common/app/src/main/res/values/strings.xml` | always |
| `app/src/main/res/values/themes.xml (and, with darker colors, `values-night/themes.xml`)` | `templates/views/app/src/main/res/values/themes.xml` | `ui: views` |
| `app/src/main/res/values/themes.xml` | `templates/compose/app/src/main/res/values/themes.xml` | `ui: compose` |
| `app/src/main/java/<package-path>/ui/theme/Theme.kt` | `templates/compose/app/src/main/java/__package-path__/ui/theme/Theme.kt` | `ui: compose` |
| `app/src/main/res/mipmap-anydpi-v26/ic_launcher.xml and ic_launcher_round.xml (same content)` | `templates/common/app/src/main/res/mipmap-anydpi-v26/ic_launcher.xml` | both `ui` variants |
| `app/src/main/res/drawable/ic_launcher_background.xml` | `templates/common/app/src/main/res/drawable/ic_launcher_background.xml` | both `ui` variants |
| `app/src/main/res/drawable/ic_launcher_foreground.xml` | `templates/common/app/src/main/res/drawable/ic_launcher_foreground.xml` | both `ui` variants |
| `app/src/main/java/<package-path>/MainActivity.kt` | `templates/compose/app/src/main/java/__package-path__/MainActivity.kt` | `ui: compose` (default) |
| `app/src/main/res/layout/activity_main.xml` | `templates/views/app/src/main/res/layout/activity_main.xml` | `ui: views` |
| `app/src/main/java/<package-path>/MainActivity.kt` | `templates/views/app/src/main/java/__package-path__/MainActivity.kt` | `ui: views` |
| `app/src/test/resources/<package-path>/robolectric.properties` | `templates/common/app/src/test/resources/__package-path__/robolectric.properties` | always |
| `app/src/test/java/<package-path>/MainActivityTest.kt` | `templates/common/app/src/test/java/__package-path__/MainActivityTest.kt` | always |
| `app/src/androidTest/java/<package-path>/MainActivityInstrumentedTest.kt` | `templates/compose/app/src/androidTest/java/__package-path__/MainActivityInstrumentedTest.kt` | `ui: compose` |
| `app/src/androidTest/java/<package-path>/MainActivityInstrumentedTest.kt` | `templates/views/app/src/androidTest/java/__package-path__/MainActivityInstrumentedTest.kt` | `ui: views` |
| `.ui-quality.yml` | `templates/common/.ui-quality.yml` | always |
| `app/src/test/java/<package-path>/testing/UiScreenshots.kt` | `templates/common/app/src/test/java/__package-path__/testing/UiScreenshots.kt` | both `ui` variants |
| `app/src/test/java/<package-path>/GreetingTest.kt` | `templates/compose/app/src/test/java/__package-path__/GreetingTest.kt` | `ui: compose` |
| `app/src/test/java/<package-path>/MainActivityScreenTest.kt` | `templates/views/app/src/test/java/__package-path__/MainActivityScreenTest.kt` | `ui: views` |
| `app/.gitignore` | `templates/common/app/.gitignore` | always |

These templates are genericized from **https://github.com/albertoirurueta/irurueta-android-glutils**'s actual
toolchain files and `app/` module — kept as close to verbatim as possible, with only project-identity fields turned
into `<placeholder>` markers. Substitute using Steps 2–4; keep everything else exactly as shown unless a step below
says an opt-in changes it.

### `<placeholder>` resolution table

| Placeholder | Source |
|---|---|
| `<project-name>` | `settings.gradle.kts`'s `rootProject.name` — the repository name from Step 3 |
| `<application-id>` | Step 2 |
| `<namespace>` | Step 2 |
| `<app-name>` | Step 2 |
| `<min-sdk>` / `<compile-sdk>` / `<target-sdk>` | Step 2/4 |
| `<version-name>` / `<version-code>` | Step 2 |
| `<gradle-version>` / `<gradle-distribution-sha256>` | Step 4 |
| `<agp-version>` / `<kotlin-version>` / `<dokka-version>` / `<sonarqube-plugin-version>` / … | Step 4 |
| `<sonar-organization>` / `<sonar-project-key>` / `<sonar-host-url>` | Step 2 |
| `<owner>` / `<repo>` | Step 3 |
| `<accessibility>` | Step 2 (`enforce` by default) — only in `.ui-quality.yml` |
| `<roborazzi-version>` | Step 4 |

### Gradle wrapper — `gradle/wrapper/gradle-wrapper.properties`

Template: `templates/common/gradle/wrapper/gradle-wrapper.properties` — read it in full before filling placeholders

The reference project's own `gradle-wrapper.properties` predates `distributionSha256Sum` being set (it has none) —
this skill adds it anyway, since Gradle has supported wrapper checksum verification for years and it's a cheap
supply-chain hardening with no downside. `gradlew`/`gradlew.bat`/`gradle/wrapper/gradle-wrapper.jar` themselves are
binaries/scripts unfit for a Markdown template — obtain them one of two ways (Step 6 says which to try first):

1. If a local Gradle install exists (`gradle -v` succeeds), run `gradle wrapper --gradle-version <gradle-version>`
   at the project root, then overwrite the generated `gradle-wrapper.properties` with the block above (it adds the
   `distributionSha256Sum` line `gradle wrapper` alone doesn't add without `--gradle-distribution-sha256-sum`).
2. Otherwise, fetch the three files directly from the Gradle GitHub repository's matching tag:
   `https://raw.githubusercontent.com/gradle/gradle/v<gradle-version>/gradlew`,
   `.../gradlew.bat`, and `.../gradle/wrapper/gradle-wrapper.jar` (binary — fetch with `curl -fsSL -o`, not a text
   read), then `chmod +x gradlew`.

### Root `build.gradle.kts`

Template: `templates/common/build.gradle.kts` — read it in full before filling placeholders

The trailing `project.delete { … }` block is copied verbatim from the reference project — it runs at Gradle
*configuration* time (not as a `clean` task), deleting the root project's own (normally-empty) build directory on
every invocation. Harmless and intentional in the source repository; keep it for fidelity, but call it out in Step
8 since it surprises anyone expecting `build.gradle.kts` to only declare plugins.

### `settings.gradle.kts`

Template: `templates/common/settings.gradle.kts` — read it in full before filling placeholders

**Departure from the reference repository:** the reference lists `https://oss.sonatype.org/content/repositories/snapshots`
as its snapshots repository, but OSSRH (and that host with it) was decommissioned in mid-2025 — `-SNAPSHOT`
artifacts published through the Central Portal now land in
`https://central.sonatype.com/repository/maven-snapshots/`, which is what this template uses so an app can still
consume a `-SNAPSHOT` build of a library published by `iru-setup-android-library`'s `develop.yml`. Don't copy the
old URL back from the reference.

`FAIL_ON_PROJECT_REPOS` matches the reference project: it forbids any module-level `build.gradle.kts` from
declaring its own `repositories {}` block, forcing every dependency to resolve through this single
`dependencyResolutionManagement` block instead — Step 5's `app/build.gradle.kts` template relies on this and never
declares repositories itself.

### `gradle.properties`

Template: `templates/common/gradle.properties` — read it in full before filling placeholders

`<built-in-kotlin-flag>` is `false` unless Step 2's `built-in-kotlin` answer was `yes`, in which case **both**
lines become `true` — the same coupling `iru-setup-android-library`'s `gradle.properties` template uses, since
AGP's built-in Kotlin support is what the new DSL is paired with (the reference project opts out of both together,
`false`/`false`). Copied verbatim from the reference project's `gradle.properties` otherwise (no real
repository/org names appear in this file, so nothing else needed genericizing).

### `gradle/libs.versions.toml`

Template: `templates/common/gradle/libs.versions.toml.versions` — read it in full before filling placeholders

Template: `templates/common/gradle/libs.versions.toml.libraries` — read it in full before filling placeholders

**Both of the last two are required, not optional — confirmed while verifying this skill:** the Compose BOM
(`platform(libs.androidx.compose.bom)`) only pins versions; it doesn't pull either artifact in transitively via
`androidx.compose.material3:material3`. Omitting `androidx.activity:activity-compose` fails
`MainActivity.kt`'s `setContent { }` call with `Unresolved reference 'setContent'`; omitting
`androidx.compose.ui:ui-tooling-preview` fails the `@Preview` composable with `Unresolved reference 'tooling'` /
`Unresolved reference 'Preview'`. `androidx.activity:activity-compose` isn't part of the `androidx.compose` BOM
group at all, so it needs its own version (Step 4) even though `ui-tooling-preview` is covered by the BOM's
version pin once the artifact itself is declared.

Template: `templates/common/gradle/libs.versions.toml.plugins` — read it in full before filling placeholders

Aliases match the reference project's naming exactly (`android-application`, `kotlin-android`, `kotlin-compose`,
`dokka`, `sonarqube`, plus the library dependency names) so a repository that later also runs
`iru-setup-android-library` gets a version catalog with compatible alias spelling if the two files are merged by
hand. No `android-library` or `publish` alias/plugin is written here — this skill never scaffolds a library module
or a publishing block. Step 5's opt-ins (Detekt/Spotless/Kover/JUnit 5) each add their own `[versions]`/`[plugins]`
entries — see the "Opt-ins" subsection below.

### `app/build.gradle.kts`

Template: `templates/common/app/build.gradle.kts` — read it in full before filling placeholders

**Departures from the reference repository inside the `sonar {}` block** (mirroring `iru-setup-android-library`'s
templates — don't copy the reference's originals back):

- `sonar.coverage.jacoco.xmlReportPaths` lists `build/reports/coverage/test/debug/report.xml`, not the reference's
  `build/reports/coverage/test/report.xml` — the latter is never written. AGP's `createDebugUnitTestCoverageReport`
  emits the XML under the variant-suffixed `test/debug/` directory (see the verification notes after Step 8), which
  is also the path `iru-setup-android-github-workflows`' workflows produce before running `:app:sonar`; the
  reference's path would silently report 0 % coverage on every push.
- `sonar.junit.reportPaths` and `sonar.androidLint.reportPaths` replace the reference's `sonar.junit.reportsPath` and
  `sonar.android.lint.report` — those two are not keys the SonarQube/SonarCloud analyzer reads (unknown properties
  are ignored), so with the reference's spelling test results and Android Lint findings are silently never imported.

**`signingConfigs` safety, spelled out:** `hasReleaseSigning` is computed once, from four env vars, before `android
{}` runs. `signingConfigs { if (hasReleaseSigning) { create("release") { … } } }` means the `"release"`
`SigningConfig` object simply doesn't exist unless all four are present — and `buildTypes { release { if
(hasReleaseSigning) { signingConfig = signingConfigs.getByName("release") } } }` only looks it up in that same
case, so `getByName` never throws `UnknownDomainObjectException`. The net effect: `./gradlew :app:assembleDebug`
never needs signing secrets at all (debug builds use Android's auto-generated debug keystore, untouched by this
config); `./gradlew :app:assembleRelease`/`:app:bundleRelease` succeed with **no** env vars set too, producing an
**unsigned** release APK/AAB (Gradle only warns, it doesn't fail) — confirmed in Step 7's verification. Set all
four (`SIGNING_STORE_FILE` as an absolute or project-relative path to a `.jks`/`.keystore` file,
`SIGNING_STORE_PASSWORD`, `SIGNING_KEY_ALIAS`, `SIGNING_KEY_PASSWORD`) to get a signed release build — this
skill never generates or stores a keystore itself (Step 8 repeats this).

**`bundleRelease`/`assembleRelease` guidance:**

- `./gradlew :app:assembleRelease` — release APK, at `app/build/outputs/apk/release/`. Fine for direct install/
  Firebase App Distribution; **not** what Google Play accepts for new app submissions.
- `./gradlew :app:bundleRelease` — release Android App Bundle (`.aab`), at `app/build/outputs/bundle/release/`.
  This is what Google Play Console (and both the `r0adkll/upload-google-play@v1` Action and the Gradle Play
  Publisher plugin's `publishBundle` task) expect.

**`distribution: internal` addition** — insert into the `plugins {}` block:

```kotlin
    alias(libs.plugins.firebase.appdistribution)
```

and add to `[versions]`/`[plugins]` in `gradle/libs.versions.toml`:

```toml
firebaseAppdistribution = "<firebase-appdistribution-plugin-version>"
# [plugins]
firebase-appdistribution = { id = "com.google.firebase.appdistribution", version.ref = "firebaseAppdistribution" }
```

No further Gradle DSL block is required for a minimal setup — the plugin reads `app/google-services.json` (never
written by this skill; see Step 2) and defaults `appDistributionUploadRelease` off the `release` build type. Add a
`firebaseAppDistribution { releaseNotesFile = "..." ; groups = "..." }` block later by hand if release notes/tester
groups should be fixed rather than passed via `-P` properties.

**`distribution: store` + Gradle Play Publisher plugin chosen** — insert into `plugins {}`:

```kotlin
    alias(libs.plugins.triplet.play)
```

and add to `gradle/libs.versions.toml`:

```toml
tripletPlay = "<gradle-play-publisher-plugin-version>"
# [plugins]
triplet-play = { id = "com.github.triplet.play", version.ref = "tripletPlay" }
```

then, after the `dependencies {}` block:

```kotlin
play {
    serviceAccountCredentials.set(file("<path-to-service-account-json>"))
    defaultToAppBundles.set(true)
}
```

`<path-to-service-account-json>` is never a path this skill resolves or downloads — leave it as a placeholder
comment pointing at wherever CI decodes the `GOOGLE_PLAY_SERVICE_ACCOUNT_JSON` secret to (Step 8 flags this). If
the user instead chose the workflow-level action, skip this whole addition — `app/build.gradle.kts` stays exactly
as the base template above.

### `app/proguard-rules.pro`

Template: `templates/common/app/proguard-rules.pro` — read it in full before filling placeholders

### `app/src/main/AndroidManifest.xml`

Template: `templates/common/app/src/main/AndroidManifest.xml` — read it in full before filling placeholders

**No `package="<application-id>"` attribute on `<manifest>`, deliberately** — confirmed while verifying this skill:
current AGP no longer reads the application id/namespace from the manifest's `package` attribute at all; leaving
one in (as the reference project's manifest still does, predating this AGP behavior) produces a build-time warning
("Setting the namespace via the package attribute in the source AndroidManifest.xml is no longer supported, and the
value is ignored") for every build. `android.namespace`/`defaultConfig.applicationId` in `app/build.gradle.kts`
above are the only things that matter now — drop the attribute entirely rather than carry a dead, warning-generating
line forward from the reference.

`android:theme="@style/Theme.App"` is a placeholder style name kept short and generic (the reference project's own
manifest points at a theme name derived from its own repository name) — Step 5's theme templates below define
exactly `Theme.App` so the two always match; rename both together if the user wants a different style name.

### `app/src/main/res/**` — theme, colors, strings, launcher icon

`values/colors.xml`:

Template: `templates/common/app/src/main/res/values/colors.xml` — read it in full before filling placeholders

`values/strings.xml`:

Template: `templates/common/app/src/main/res/values/strings.xml` — read it in full before filling placeholders

**`ui: views`** — `values/themes.xml`:

Template: `templates/views/app/src/main/res/values/themes.xml` — read it in full before filling placeholders

(and the same block, with darker color values swapped in, under `values-night/themes.xml` — mirrors the reference
project's day/night pair exactly.)

**`ui: compose`** — no XML theme is required; the manifest's `android:theme="@style/Theme.App"` still needs *some*
style to resolve at inflation time before Compose takes over, so write a minimal one:

Template: `templates/compose/app/src/main/res/values/themes.xml` — read it in full before filling placeholders

(no `values-night` variant needed — `DayNight` already switches automatically) and a Kotlin Compose theme wrapper,
`app/src/main/java/<package-path>/ui/theme/Theme.kt`:

Template: `templates/compose/app/src/main/java/__package-path__/ui/theme/Theme.kt` — read it in full before filling placeholders

**Launcher icon (both `ui` variants)** — `mipmap-anydpi-v26/ic_launcher.xml` and `ic_launcher_round.xml`:

Template: `templates/common/app/src/main/res/mipmap-anydpi-v26/ic_launcher.xml` — read it in full before filling placeholders

`drawable/ic_launcher_background.xml` (flat brand-color fill):

Template: `templates/common/app/src/main/res/drawable/ic_launcher_background.xml` — read it in full before filling placeholders

`drawable/ic_launcher_foreground.xml` (a simple centered monogram placeholder — replace with real brand art):

Template: `templates/common/app/src/main/res/drawable/ic_launcher_foreground.xml` — read it in full before filling placeholders

**No raster (`.webp`/`.png`) launcher icons are generated, and none are needed.** `min-sdk` defaults to `26` — the
exact API level `<adaptive-icon>` was introduced at — so every device this app installs on resolves the vector
adaptive icon directly; legacy `mipmap-hdpi/mdpi/xhdpi/xxhdpi/xxxhdpi` raster fallbacks (present in the reference
project only because *it* targets pre-26 launchers in some configurations) are dead weight here. If a user later
lowers `min-sdk` below 26, generate real raster fallbacks with Android Studio's Image Asset Studio at that point —
this skill deliberately doesn't attempt to rasterize vector art itself.

### `app/src/main/java/<package-path>/MainActivity.kt`

**`ui: compose`** (default):

Template: `templates/compose/app/src/main/java/__package-path__/MainActivity.kt` — read it in full before filling placeholders

**`ui: views`** (ViewBinding-based alternative — write this instead when Step 2 chose `views`):

`res/layout/activity_main.xml`:

Template: `templates/views/app/src/main/res/layout/activity_main.xml` — read it in full before filling placeholders

`MainActivity.kt`:

Template: `templates/views/app/src/main/java/__package-path__/MainActivity.kt` — read it in full before filling placeholders

The constraints use `Start`/`End`, never `Left`/`Right`, so the layout mirrors in right-to-left locales (UI
contract §4). `viewBinding = true` (already in the `buildFeatures {}` block above) generates `ActivityMainBinding` from
`activity_main.xml`'s filename — no manual binding class to write. This variant needs
`androidx.appcompat:appcompat` and `androidx.constraintlayout:constraintlayout`, both pulled in transitively by
`com.google.android.material:material`'s own dependency graph, confirmed working with just the `material` alias
already in `dependencies {}` above (no extra explicit dependency line needed) — if that ever stops being true
upstream, add `androidx.appcompat:appcompat` and `androidx.constraintlayout:constraintlayout` explicitly.

### `app/src/test/resources/<package-path>/robolectric.properties`

Template: `templates/common/app/src/test/resources/__package-path__/robolectric.properties` — read it in full before filling placeholders

The reference project pins this one minor step behind its own `compileSdk` (`compileSdk = 36` → `sdk=35`) because
Robolectric's shipped Android SDK jars lag the very latest platform release by a few months after each Android
release — **always check the installed `robolectric` version's supported SDKs before trusting `<compile-sdk>`
directly here** (Robolectric errors clearly, naming which SDKs it has, if an unsupported one is requested); Step 7
records which value actually worked.

### `app/src/test/java/<package-path>/MainActivityTest.kt` — placeholder unit test

Template: `templates/common/app/src/test/java/__package-path__/MainActivityTest.kt` — read it in full before filling placeholders

A genuine first test exercises `MainActivity`'s `onCreate` via `Robolectric.buildActivity(MainActivity::class.java)`
— this skill ships only the arithmetic placeholder above (mirroring the reference project's own
`ExampleUnitTest.kt`) so `iru-android-generate-all-tests` has an obvious first target to replace.

### `app/src/androidTest/java/<package-path>/MainActivityInstrumentedTest.kt` — instrumented test skeleton

**`ui: compose`**:

Template: `templates/compose/app/src/androidTest/java/__package-path__/MainActivityInstrumentedTest.kt` — read it in full before filling placeholders

**`ui: views`** — the same `useAppContext` test plus Espresso's Accessibility Test Framework integration:

Template: `templates/views/app/src/androidTest/java/__package-path__/MainActivityInstrumentedTest.kt` — read it in full before filling placeholders

Runs only via `./gradlew :app:connectedAndroidTest` against a running emulator/device — Step 7 doesn't run this
(no emulator available in this skill's own verification environment); it was compile-checked
(`:app:compileDebugAndroidTestKotlin`) for both `ui` variants.

### `.ui-quality.yml` — UI test settings at the repository root

Template: `templates/common/.ui-quality.yml` — read it in full before filling placeholders

`<accessibility>` is Step 2's answer (default `enforce`). Exactly this shape — the catalog's UI contract §8 — read
by `UiScreenshots.kt` below, `iru-android-test`'s `ui` run, and the coding skills.

### `app/src/test/java/<package-path>/testing/UiScreenshots.kt` — shared UI-test helper

Resolves `UI_SCREENSHOTS_DIR` (else `<repository root>/.ui-screenshots`), reads `.ui-quality.yml`, builds the
capture matrix and the contract's file names, forces Roborazzi to record (its captures are no-ops otherwise), and
maps the accessibility level onto Roborazzi's ATF options. Identical for both `ui` variants:

Template: `templates/common/app/src/test/java/__package-path__/testing/UiScreenshots.kt` — read it in full before filling placeholders

### `app/src/test/java/<package-path>/GreetingTest.kt` (`ui: compose`) — sample UI test

Template: `templates/compose/app/src/test/java/__package-path__/GreetingTest.kt` — read it in full before filling placeholders

With a Compose BOM whose UI test artifacts are 1.11 or newer, `createComposeRule` is deprecated in favour of
`androidx.compose.ui.test.junit4.v2.createComposeRule` (same use) — switch the import then; the fallback BOM in
Step 4 predates it.

### `app/src/test/java/<package-path>/MainActivityScreenTest.kt` (`ui: views`) — sample UI test

Template: `templates/views/app/src/test/java/__package-path__/MainActivityScreenTest.kt` — read it in full before filling placeholders

### `app/.gitignore`

Template: `templates/common/app/.gitignore` — read it in full before filling placeholders

### `local.properties` guidance

Never write `local.properties` (it's machine-specific and always gitignored at the root — see
`iru-setup-android-gitignore`). Tell the user in Step 8 instead: on first checkout, either let Android Studio
generate it automatically, or create it by hand with one line, `sdk.dir=<path-to-android-sdk>` (e.g.
`sdk.dir=/Users/<you>/Library/Android/sdk` on macOS, `sdk.dir=/home/<you>/Android/Sdk` on Linux) — the SDK
components this scaffold needs (the `<compile-sdk>` platform, matching build-tools) are downloaded automatically by
AGP on first build as long as `android.builder.sdkDownload` isn't disabled and the SDK licenses are already
accepted (`sdkmanager --licenses`).

### Opt-ins

**Detekt + Spotless (`static-analysis: lint+detekt+ktlint`)** — add to `[versions]`/`[plugins]`:

```toml
detekt = "<detekt-version>"
spotless = "<spotless-version>"
# [plugins]
detekt = { id = "io.gitlab.arturbosch.detekt", version.ref = "detekt" }
spotless = { id = "com.diffplug.spotless", version.ref = "spotless" }
```

apply both in `app/build.gradle.kts`'s `plugins {}` and configure:

```kotlin
detekt {
    config.setFrom(files("$rootDir/detekt.yml"))
    buildUponDefaultConfig = true
}

spotless {
    kotlin {
        target("src/**/*.kt")
        ktlint()
        licenseHeaderFile(rootProject.file("spotless/license-header.kt"))
    }
    kotlinGradle {
        target("*.gradle.kts")
        ktlint()
    }
}
```

Write a minimal `detekt.yml` at the repository root (`build:\n  maxIssues: 0\ncomplexity:\n  active: true`, or
generate a fuller baseline with `./gradlew detektGenerateConfig`); Detekt's SARIF output
(`app/build/reports/detekt/detekt.sarif`) is what `iru-android-code-quality`/`iru-setup-android-github-workflows`'s
CodeQL-adjacent SARIF upload step consumes. Add `spotless/license-header.kt` only if a license was chosen in Step 2
(the file's content is that license's standard header comment).

**Kover (`coverage-tool: kover`, instead of the default AGP JaCoCo path)** — add to `[versions]`/`[plugins]`:

```toml
kover = "<kover-version>"
# [plugins]
kover = { id = "org.jetbrains.kotlinx.kover", version.ref = "kover" }
```

apply in `app/build.gradle.kts`'s `plugins {}`; no further DSL is required for a minimal setup — Kover's default
`koverXmlReportDebug`/`koverHtmlReportDebug` tasks work against the `debug` build type out of the box. When Kover is
chosen, drop `enableUnitTestCoverage = true` from the `debug {}` block above (Kover manages its own coverage
instrumentation and the two mechanisms shouldn't run simultaneously) and use `iru-android-coverage`'s Kover-XML
parsing path instead of the JaCoCo one.

**JUnit 5 (`junit: 5`, additive — Robolectric's runner itself stays JUnit 4)** — add to `[versions]`/`[plugins]`:

```toml
mannodermausAndroidJunit = "<mannodermaus-plugin-version>"
# [plugins]
mannodermaus-android-junit = { id = "de.mannodermaus.android-junit", version.ref = "mannodermausAndroidJunit" }
```

apply in `app/build.gradle.kts`'s `plugins {}` as `alias(libs.plugins.mannodermaus.android.junit)` (the same alias
`iru-setup-android-library` uses), and add the plugin's own BOM-pinned JUnit 5 test dependencies per
its README (`testImplementation(libs.junit.jupiter)`, `testRuntimeOnly(libs.junit.jupiter.engine)` — exact
coordinates come from that plugin's own version catalog recommendation at the version resolved in Step 4, since it
pins compatible JUnit 5 Jupiter/Platform versions together). Robolectric's `@RunWith(RobolectricTestRunner::class)`
tests keep using JUnit 4 exactly as before; JUnit 5 is for new tests that don't need Robolectric, written with
`@Test`/`org.junit.jupiter.api.Test` instead.

## Step 6 — Scaffold the project

Apply Step 1's per-artifact choice to every file this step would write that already exists: **Keep as is** —
skip it; **Update** — merge the filled-in template into it after showing the user the diff (for the `app/`
skeleton, only its missing files are created); **Replace** — overwrite it, within Step 1's application-source
limits. Files that didn't exist are always written.

1. Obtain the Gradle wrapper (Step 5's two-path recipe): try `gradle wrapper --gradle-version <gradle-version>`
   first, falling back to fetching `gradlew`/`gradlew.bat`/`gradle/wrapper/gradle-wrapper.jar` from the Gradle
   GitHub tag. Then hand-write `gradle-wrapper.properties` with Step 5's exact content (adding
   `distributionSha256Sum`, which neither path adds by default without an extra flag). `chmod +x gradlew`.
2. Write the root `build.gradle.kts`, `settings.gradle.kts`, `gradle.properties`, and `gradle/libs.versions.toml`
   from Step 5, with Step 2/3/4's values substituted and the `ui`/`sonar`/`distribution`/opt-in conditionals
   applied.
3. Create `app/src/main/java/<package-path>/` (from `<namespace>`, dots turned into path separators) and write
   `app/build.gradle.kts`, `app/proguard-rules.pro`, `app/src/main/AndroidManifest.xml`, the `res/` theme/color/
   string/icon files, `MainActivity.kt` (+ `ui/theme/Theme.kt` for `ui: compose`, or `res/layout/activity_main.xml`
   for `ui: views`), `app/src/test/resources/<package-path>/robolectric.properties`,
   `app/src/test/java/<package-path>/MainActivityTest.kt`, `app/src/test/java/<package-path>/testing/UiScreenshots.kt`,
   the sample UI test (`GreetingTest.kt` for `ui: compose`, `MainActivityScreenTest.kt` for `ui: views`),
   `app/src/androidTest/java/<package-path>/MainActivityInstrumentedTest.kt`, `app/.gitignore`, and
   `.ui-quality.yml` at the repository root (with Step 2's `accessibility`) — all from Step 5.
4. Apply whichever opt-in blocks Step 2 selected (Detekt/Spotless, Kover, JUnit 5, Firebase App Distribution,
   Gradle Play Publisher) to the files just written, per Step 5's "Opt-ins"/distribution subsections.
5. If `distribution: internal` was chosen, remind the user now (also repeated in Step 8) that
   `app/google-services.json` must be downloaded from the Firebase console and placed manually — this skill never
   fetches or writes it.

## Step 7 — Verify

Run through the `iru-gate-runner` agent (never inline in this skill's own context — its reports can be long):

1. `./gradlew --offline help` — confirms the wrapper, root/settings files, and version catalog all parse and
   resolve without touching the network (anything already cached from Step 6's own dependency resolution). If this
   fails offline only because a dependency genuinely isn't cached yet, retry without `--offline`.
2. `./gradlew :app:assembleDebug` — the real scaffold-sanity build. **Warn the user up front that the first run
   downloads the `<compile-sdk>` platform, matching build-tools, and every Gradle/AGP/Kotlin/AndroidX artifact
   above if they aren't already cached — this can take several minutes and needs `ANDROID_HOME`/`local.properties`
   pointing at a real SDK install with licenses accepted.**

3. `./gradlew :app:testDebugUnitTest` — runs the placeholder and the sample UI test; then confirm
   `.ui-screenshots/component/Greeting/` (`ui: compose`) or `.ui-screenshots/screen/MainActivity/` (`ui: views`)
   holds one `default--<ltr|rtl>--<light|dark>.png` per `.ui-quality.yml` cell (four by default).

Report pass/fail and any error output verbatim for a failure; don't dump a successful build's full log.

## Step 8 — Report

Summarize what was generated: the resolved `application-id`/`namespace`/`app-name`, `min-sdk`/`compile-sdk`/
`target-sdk`, `version-name`/`version-code`, the license chosen (or "none"), and whether this run scaffolded from
scratch, updated an existing project (per Step 1), or the user chose to stop.

State explicitly what was included versus omitted, and why:

- **`ui`**: `compose`/`views` — which `MainActivity`/theme template was written.
- **`open-source`**/**`sonar`**: as Step 2 resolved them; if `sonar` ≠ `none`, restate the `sonar.organization`/
  `sonar.projectKey`/`sonar.host.url` written into `app/build.gradle.kts`'s `sonar { properties {…} } }` block (and,
  with `ci: no`, that no CI step sends reports); if `none`, whether that's the expected default (not open source, a
  private/internal `visibility`, or `ci: no`) or a direct user choice.
- **`distribution`**: `none`/`internal`/`store` —
  - `internal`: restate that `app/google-services.json` must be downloaded from the Firebase console and placed at
    that exact path before any Firebase-related task runs, and that `FIREBASE_APP_ID` plus a service-account
    credential will be needed by CI.
  - `store`: restate which upload path was chosen (workflow-level `r0adkll/upload-google-play@v1`, or the Gradle
    Play Publisher plugin) and the Google Play service-account JSON key it depends on either way — this skill never
    collects or stores it.
  - `none`: no distribution plugin was added; `signingConfigs` is still present and usable whenever the four
    `SIGNING_*` env vars are supplied later.
- **`built-in-kotlin`**/**`junit`**/**`coverage-tool`**/**`static-analysis`**: as resolved, and which opt-in
  Gradle plugins/files that triggered.
- **`accessibility`** and the UI-contract files: `.ui-quality.yml` with its action (**created / updated / replaced /
  kept as is**) and level, the `testing/UiScreenshots.kt` helper, the sample UI test, and how many captures Step 7
  found under `.ui-screenshots/` (gitignored by `iru-setup-android-gitignore`).
- Which Step 4 versions came from a live lookup versus this skill's recorded fallback — call out explicitly any
  row marked "unverified locally" above that was used as-is without confirming it resolves.

Then report, per Step 1 artifact, the action actually taken — **created / updated / replaced / kept as is** — and
whether it came from the user's answer or `on-existing`; for each artifact kept as is, list any mismatch with this
run's choices. If existing toolchain files were replaced, explicitly list what could have been lost — any dependency,
flavor, or build-type customization beyond what Step 5's templates show — and tell the user to check `git diff` for
anything they need to re-add.

### Known quirks / verification notes

- Verified in `$TMPDIR/iru-verify/android/app` (outside this repository): `./gradlew :app:assembleDebug
  :app:testDebugUnitTest :app:lint` all pass in one invocation against the scaffold generated with
  `distribution: store` (workflow-level upload — no Gradle Play Publisher plugin applied), `sonar: cloud` (dummy
  org/key/host — the `sonar` task itself was never run, only that `app/build.gradle.kts` configures with the block
  present), `ui: compose`, `junit: 4`, `coverage-tool: jacoco`, `static-analysis: lint`. Versions actually used:
  Gradle `9.7.1` (fresh, from `services.gradle.org/versions/current` — newer than the `9.4.0` recorded as this
  file's fallback; sha256 looked up from the same response), AGP `9.0.1`, Kotlin `2.3.10`, Dokka `2.1.0`, SonarQube
  plugin `7.2.3.7755`, JUnit `4.13.2`, AndroidX `junit` `1.3.0`, Espresso `3.7.0`, Compose BOM `2026.02.01`,
  `material` `1.13.0`, `test-core-ktx` `1.7.0`, MockK `1.14.9`, Robolectric `4.16.1`, `kotlin-reflect` `2.3.10`,
  `irurueta-android-test-utils` `1.3.2` (the reference project's own verified-working combination — deliberately
  used as-is rather than every individual artifact's own bare "latest", since AGP/Kotlin/Compose-compiler version
  skew across a whole toolchain is the actual compatibility risk, not any single artifact being one minor behind).
  **`search.maven.org`'s `solrsearch` API returned stale `latestVersion` values for both `kotlin-gradle-plugin`
  (`2.2.0`) and `dokka-gradle-plugin` (`2.0.0`) during this verification — both were already superseded (Kotlin
  `2.4.20`, confirmed via `repo1.maven.org`'s own `maven-metadata.xml`, is real; Dokka likely similarly stale).**
  Prefer a direct `maven-metadata.xml`/group-index fetch over `solrsearch` for "current version" lookups; treat
  `solrsearch`'s `latestVersion` field as unreliable.
- `./gradlew :app:assembleRelease` **with none of the four `SIGNING_*` env vars set** was also run (separately, with
  `unset SIGNING_STORE_FILE SIGNING_STORE_PASSWORD SIGNING_KEY_ALIAS SIGNING_KEY_PASSWORD` first) and confirmed to
  succeed (`BUILD SUCCESSFUL`), producing `test-app-1.0.0-release-unsigned.apk` at
  `app/build/outputs/apk/release/` — proves the `signingConfigs`/`buildTypes.release` conditional guard above never
  fails configuration when signing secrets are absent, exactly as designed.
- The default JDK on this machine (JDK 26) is **not** used — `JAVA_HOME` was pinned explicitly to JBR 21
  (`export JAVA_HOME=$(/usr/libexec/java_home -v 21)`) for every `./gradlew` invocation; not re-tested against JDK
  17 in this pass (`iru-setup-android-library`'s verification exercises that fallback), but the same JBR distribution is
  present locally at `-v 17` too. Record JDK 21 (or 17) as a hard prerequisite, not just a suggestion — this AGP/
  Gradle combination was never tried against JDK 26.
- `app/build/reports/lint-results-debug.xml` (17 issues in this run, **all** `Warning`-severity "newer version
  available"/`GradleDependency`/`NewerVersionAvailable`/`AndroidGradlePluginVersion` — zero real correctness/
  security findings, expected since Step 4's fallback versions are all one or more minor releases behind by
  design) and the matching `.html`/`.txt` siblings are the Lint report paths (`iru-android-code-quality` reads the
  XML). `testDebugUnitTest` results land at `app/build/test-results/testDebugUnitTest/*.xml` (JUnit XML — 1 test,
  0 failures, confirmed — `iru-android-test` parses these) plus an HTML report at
  `app/build/reports/tests/testDebugUnitTest/`. The debug APK lands at
  `app/build/outputs/apk/debug/test-app-1.0.0-debug.apk` (`base.archivesName`'s `<project-name>-<versionName>[-<buildNumber>]`
  pattern, confirmed).
- **Coverage, confirmed working — no vendored JaCoCo CLI needed for the `app` module in this AGP version**:
  `./gradlew :app:createDebugUnitTestCoverageReport` runs (`app:createDebugUnitTestCoverageReport` is exposed for a
  `com.android.application` module exactly the same way it is for a library) and emits a real XML report at
  `app/build/reports/coverage/test/debug/report.xml` (standard JaCoCo-format XML — package/class/method-level
  `<counter type="..." missed="..." covered="...">`). The raw `.exec` file does **not** land at
  `app/build/jacoco/testDebugUnitTest.exec` (that's where the *reference* project's older-AGP/CI script expects it
  for its vendored-jar fallback) — in this verified AGP `9.0.1`, it's at
  `app/build/outputs/unit_test_code_coverage/debugUnitTest/testDebugUnitTest.exec` instead. Since AGP already emits
  the XML directly, this skill never needs `iru-setup-android-library`'s vendored `jacococli.jar` fallback path at
  all for the `app` module — `iru-android-coverage` should read `report.xml` from the path above directly.
- The Firebase App Distribution and Gradle Play Publisher plugin ids/versions were checked only by resolving
  `./gradlew help` with each plugin applied at its Step 4 fallback version (confirms the plugin id + version exist
  and configure without error) — **no distribution task was ever run** (`appDistributionUploadRelease`,
  `publishBundle`), since both need real Firebase/Google Play credentials this environment doesn't have. Mark both
  as "unverified locally" beyond that configuration-time check whenever a live plugin-portal lookup itself can't be
  reached from this machine.
- Detekt/Spotless/Kover/JUnit 5 opt-ins were **not** exercised in this verification pass (the representative inputs
  used `static-analysis: lint` and `coverage-tool: jacoco`/`junit: 4`, i.e. no opt-ins triggered) — their plugin
  ids/fallback versions above are unverified locally; confirm them the first time a user actually opts in.
- **The seven `gradle.properties` flags carried forward from the reference project
  (`android.usesSdkInManifest.disallowed`, `android.sdk.defaultTargetSdkToCompileSdkIfUnset`,
  `android.enableAppCompileTimeRClass`, `android.builtInKotlin`, `android.newDsl`,
  `android.r8.optimizedResourceShrinking`, `android.defaults.buildfeatures.resvalues`) each print an individual
  `WARNING: The option setting '<flag>' is deprecated ... It will be removed in version 10.0 of the Android Gradle
  plugin` on every build with AGP `9.0.1`.** They don't fail the build and are kept for fidelity to the reference
  project (which predates this deprecation), but note this explicitly to the user in Step 8 rather than leaving
  seven silent warnings on every single build — they'll need removing (or explicit new defaults set) before an
  eventual AGP 10 upgrade.
- **Separately, applying `org.jetbrains.kotlin.android` (`libs.plugins.kotlin.android`) itself now prints
  `⚠️ Deprecated 'org.jetbrains.kotlin.android' plugin usage ... no longer required for Kotlin support since AGP
  9.0`, recommending `built-in-kotlin: yes` instead.** This skill still defaults `built-in-kotlin` to `no` (Step
  2), matching the reference project and avoiding AGP's still-young built-in-Kotlin path — but both this and the
  `gradle.properties` deprecations above point the same direction, and a future revision of this skill should
  reconsider defaulting `built-in-kotlin: yes` once that path is less new.
- **`android:theme="@style/Theme.App"` still needed `package="<application-id>"` removed from the manifest's
  `<manifest>` tag** (see Step 5's `AndroidManifest.xml` note) — confirmed this produces a
  "Setting the namespace via the package attribute ... is no longer supported, and the value is ignored" warning on
  every build otherwise; the attribute contributes nothing once `android.namespace` is set in `build.gradle.kts`.
- **`androidx.activity:activity-compose` and `androidx.compose.ui:ui-tooling-preview` must both be declared
  explicitly** (see Step 5's dependency note) — omitting either fails Kotlin compilation
  (`Unresolved reference 'setContent'` / `Unresolved reference 'Preview'`) even with the Compose BOM and
  `androidx.compose.material3:material3` both present; neither pulls the other in transitively. This was the one
  real (not just deprecation-warning) defect found in this skill's first draft, fixed before this verification
  pass's second, successful run.
- `org.gradle.configuration-cache=true` (from `gradle.properties`) is compatible with `:app:assembleDebug`/
  `:app:testDebugUnitTest`/`:app:lint`/`:app:assembleRelease`/`:app:createDebugUnitTestCoverageReport`, all
  confirmed ("Configuration cache entry stored" on every run) — but **not** with `publishAndReleaseToMavenCentral`-
  style tasks in general (irrelevant here, since this skill never generates a publishing task) — if a future opt-in
  ever adds one that warns about configuration cache, pass `--no-configuration-cache` for that specific task the
  same way the reference project's `publish.yml` does for its library module.

- **UI-contract additions, verified** in `$TMPDIR/iru-verify/android/app-ui/{compose,views}` (outside this
  repository): both `ui` variants were generated straight from Step 5's templates with the fallback versions
  (AGP `9.0.1`, Kotlin `2.3.10`, Compose BOM `2026.02.01`, Robolectric `4.16.1`, Robolectric `sdk=35`) plus Roborazzi
  `1.76.0`, on Gradle `9.8.1` and JDK 21: `./gradlew :app:assembleDebug :app:testDebugUnitTest
  :app:compileDebugAndroidTestKotlin` (plus `:app:lintDebug` for `views`) passed, and the sample UI test wrote
  exactly four captures — `.ui-screenshots/component/Greeting/default--{ltr,rtl}--{light,dark}.png` (`compose`) and
  `.ui-screenshots/screen/MainActivity/default--…png` (`views`) — with the ATF check passing at `enforce`. The same
  helper and tests also passed on AGP `9.4.1`/Kotlin `2.4.21`/BOM `2026.09.00`/Robolectric `4.17` (which needs
  `compileSdk = 37` for that BOM, and prints a deprecation for the v1 `createComposeRule`). Robolectric `sdk=36` on
  JDK 21 fails Robolectric's `FileDescriptor` interceptor (`IllegalAccessException … jdk.internal.access`) — keep
  `robolectric.properties` one level behind, or add `all { it.jvmArgs("--add-exports=java.base/jdk.internal.access=ALL-UNNAMED") }`
  inside `testOptions.unitTests`. **The instrumented tests were compile-checked only** (no emulator); Compose's
  `enableAccessibilityChecks()` needs an API 34+ device and is a no-op guard below that.

Finish with an explicit **Warn explicitly** block:

- **The user must review every generated file before building, committing, or distributing.** In particular:
  confirm the license choice matches an actual repository-root `LICENSE` file (or that none is intended — suggest
  `iru-check-license` otherwise), replace the placeholder launcher icon/monogram vector art with real brand art
  before any real release, and never commit a real keystore — `*.jks`/`*.keystore` must stay gitignored
  (`iru-setup-android-gitignore` covers this) and `SIGNING_STORE_FILE` should point at a keystore kept outside
  version control (a CI secret decoded at build time, or a local, gitignored file).
- `app/google-services.json` (only relevant when `distribution: internal`) must stay gitignored — it carries
  project-specific Firebase identifiers that shouldn't be committed, even though they aren't traditional secrets.
- If `sonar: cloud` or `sonar: self-hosted` was chosen, a `SONAR_TOKEN` repository secret and an actual SonarCloud/
  SonarQube project matching `sonar.projectKey` still need to exist before a CI-driven `./gradlew :app:sonar`
  scan will succeed — this skill only writes the `sonar {}` block, it never runs a scan itself.
- If `distribution` ≠ `none`, the relevant credentials (Firebase `FIREBASE_APP_ID` + service-account JSON for
  `internal`; Google Play service-account JSON for `store`, however it's invoked) must exist as CI secrets — or be
  available locally — before any upload succeeds; this skill never collects or stores them.
- **Unverified locally, and never a blocker**: `connectedAndroidTest` (needs a running emulator/device — none
  available here), `appDistributionUploadRelease`/`publishBundle` (need real Firebase/Google Play credentials), and
  a genuinely signed `assembleRelease`/`bundleRelease` (needs a real keystore) — this skill only confirms the
  unsigned path builds. Everything else in the "Known quirks" section above was run for real while building and
  verifying this skill.
