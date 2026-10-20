---
name: iru-kmp-dokka
description: >-
  Audit given Kotlin class(es)/file(s)/package scope in a Kotlin Multiplatform (Android + iOS) project for complete
  KDoc coverage across every source set — `commonMain`, `androidMain`, `iosMain`/`appleMain`/`nativeMain` (and
  `jvmMain` when present) of the shared module plus the Android app module's sources — with the KMP rule that an
  `expect` declaration carries the KDoc and its `actual`s inherit it (an `actual` gets its own KDoc only for genuinely
  platform-specific behavior), while platform-only public API (an `iosMain`-only helper, Compose `MainViewController()`,
  an `androidMain`-only extension) is documented where it lives. Checks type-level docs, `@property`/`@param`/
  `@constructor`, every function/property within the discovered visibility bar, enum entries, companion and nested
  declarations, `@return`/`@throws`/`@see`/`@sample`, `@suppress` honored, and the Dokka `module.md` (`# Module` /
  `# Package` sections) wired via `includes.from(...)` for every module/package touched (creating them if missing);
  generates any missing or incomplete KDoc grounded in the actual code and current changes, then runs the module's
  Dokka 2 multiplatform build (`dokkaGeneratePublicationHtml`, else `dokkaGenerate`; Dokka 1 `dokkaHtml` fallback) to
  confirm the KDoc is well-formed and reports its warnings — unresolved links per source set and, when the project
  enables `reportUndocumented`, `Undocumented:` lines tagged `(common)`/`(android)`/`(ios)`. Invoke as
  `/iru-kmp-dokka <scope>` where `<scope>` is a comma-separated list of class names, file paths, or a package glob, or
  `/iru-kmp-dokka` with no argument to scope to Kotlin files touched by uncommitted changes plus commits on the current
  branch not yet on the base branch. Swift code in `iosApp/` is out of scope (see `iru-swift-docc`). Discovers the
  project's own documentation bar (detekt `comments` rules, Dokka `documentedVisibilities`/`reportUndocumented`,
  contributor guides, observed practice) rather than assuming a fixed style. Equivalent to `iru-android-dokka`/
  `iru-kotlin-kdoc` for KMP apps. Use whenever the user (or `iru-kmp-code-one-task-group` via `iru-gate-runner`) wants
  KDoc completeness checked and filled in for KMP code, instead of relying on a Dokka run (which doesn't fail on
  undocumented members by default) to surface gaps.
model: sonnet
allowed-tools: Read Edit Write Bash(./gradlew *) Bash(git status *) Bash(git diff *) Bash(git log *) Bash(git symbolic-ref *) Bash(git branch *) Bash(find *) Bash(grep *) Bash(ls *) Bash(/usr/libexec/java_home *)
---

# KMP Dokka

Make sure a set of Kotlin Multiplatform declarations — and the module(s)/package(s) they live in — carry complete,
well-formed KDoc, filling in whatever is missing, then prove the result builds via the project's own Dokka
multiplatform setup. This skill only adds/completes documentation comments (plus missing `module.md` includes and
their wiring) — it never changes behavior, signatures, annotations, or non-KDoc code. Test source sets (`commonTest`,
`androidHostTest`/`androidUnitTest`/`androidInstrumentedTest`, `iosTest`, `src/test`, …) carry no KDoc requirement —
don't add KDoc there even if named explicitly — but never strip KDoc a test already has. Swift sources under
`iosApp/` belong to `iru-swift-docc`. Discover the repository's conventions and Dokka setup fresh each run.

## Step 1 — Determine scope

- **Source roots**: every KMP module's `src/<set>Main/kotlin` (`commonMain`, `androidMain`, `iosMain`, `appleMain`,
  `nativeMain`, `iosArm64Main`/`iosSimulatorArm64Main`, `jvmMain`) and every Android app module's `src/main/kotlin`/
  `src/main/java` (`androidApp/` in this catalog's layout; `composeApp/` is both in the JetBrains wizard's).
- **Argument provided** (comma-separated class names, file paths, or a package glob): resolve each to its file(s) with
  `find`/`grep` across those roots — a simple name can match an `expect` in `commonMain` *and* its `actual`s in
  `androidMain`/`iosMain`; take them all, since Step 3 audits them together. A file under a test source set, a `.swift`
  file, or a build script is dropped and named in the Step 7 report.
- **No argument**: every main-source `.kt` file touched by uncommitted changes plus commits on the current branch not
  yet on the base branch:
  ```bash
  git status
  git diff <base-branch>...HEAD --name-only
  git diff --name-only
  ```
  (base branch via `git symbolic-ref refs/remotes/origin/HEAD` or `git branch -a`; ask only if genuinely ambiguous).
  Keep `.kt` files under the main source roots above; skip tests, `build/` output (including generated
  Compose-resources/KSP/SKIE sources), `.kts` scripts, and Swift.
- **Pull in the other half of every expect/actual pair**: for each in-scope `expect` (or `actual`) declaration, add
  its counterparts in the other source sets (`grep -rn "actual fun <name>\|actual class <Name>\|actual object <Name>\|actual val <name>" */src/*Main`)
  so the pair is audited consistently.
- Empty scope → say there is nothing to document and stop.
- Derive the distinct modules and packages (each file's `package` line) for Steps 4 and 6.

## Step 2 — Discover this project's KDoc bar before auditing

Same discovery as `iru-kotlin-kdoc`'s Step 2 — follow the **stricter** of stated vs. observed practice:

- Contributor guides (`CLAUDE.md`, `AGENTS.md`, `README`, `CONTRIBUTING`).
- detekt's `comments` rule set (`UndocumentedPublicClass`/`UndocumentedPublicFunction`/`UndocumentedPublicProperty`,
  `OutdatedDocumentation`) in `detekt.yml`/`config/detekt/detekt.yml` or whatever `config.setFrom(...)` names.
- The Dokka configuration: `dokka { dokkaSourceSets.configureEach { documentedVisibilities(...) } }` (Dokka 2; may also
  be set per set via `named("commonMain") { … }`) — default `PUBLIC`; anything wider is in scope. `reportUndocumented`
  — when the project sets it, Step 6's `Undocumented:` lines are a cross-check of Step 3 (never turn it on yourself).
- Observed practice in 2-3 structurally similar, well-documented declarations — phrasing, tense, tag order, `[Link]`
  use. Defaults when nothing is learnable: summary sentence first (third person, present tense), `@param name`
  (KDoc form, no hyphen/type), `@property` for primary-constructor properties, `@constructor` when `init` does work,
  `@return` unless `Unit`, `@throws` per thrown exception (including `require`/`check`/`error`), `@see`/`[Link]` for
  cross-references, `@sample` only for samples that exist, `@suppress` only carried over, never added.

**Library-like visibility in an app**: in a KMP *app*, `shared`'s public API is consumed by `androidApp` and, through
the `Shared` framework, by Swift — treat every `public` declaration of the KMP module as documented API even when the
project has no detekt rule, because Dokka publishes it (the catalog's scaffold publishes the shared module's Dokka
HTML under the Antora site's `api/`). Declarations hidden from Swift (`@HiddenFromObjC`) or renamed for it
(`@ObjCName("…")`) are still Kotlin API — document them; mention the Swift name in the KDoc when `@ObjCName` changes
it.

## Step 3 — Audit each in-scope declaration

Read each full file and check every item below is present, non-empty, and describes purpose and behavior rather than
restating the name — scoped per Step 2's bar. Everything `iru-kotlin-kdoc`'s Step 3 lists applies (types with `@param
T`, primary/secondary constructors, properties incl. `lateinit`/`const`, functions incl. extension/operator/`suspend`
— state dispatcher/emission semantics for `suspend`/`Flow` only when non-obvious — enum entries, companion and nested
declarations, `@suppress` recorded as suppressed). KMP-specific rules:

- **`expect`/`actual`**: the **`expect` declaration in the common (or intermediate, e.g. `appleMain`) source set must
  carry the full KDoc** — Dokka shows it for every platform and the `actual`s inherit it (verified: an undocumented
  `actual fun` whose `expect` is documented produced no `Undocumented:` warning, and the expect's KDoc — including its
  links — was rendered for the `androidMain` and `iosMain` actuals). An undocumented `expect` is a gap even if an
  `actual` has KDoc. An `actual` needs its own KDoc only when its platform behavior differs in a way callers must
  know (different exceptions thrown, a blocking call, a unit/format difference, a main-thread requirement on iOS) —
  then write the full comment there (an `actual`'s own KDoc replaces the inherited one for that platform, it doesn't
  append), keeping the common facts identical. Don't copy the expect's KDoc onto every actual just to fill space.
- **`expect class`/`actual class`**: the same, member by member; an `actual typealias` (e.g. to a platform class) has
  nothing to document beyond what the `expect` says.
- **Platform-only public API** — a public declaration that exists only in `androidMain` or `iosMain` (no `expect`) is
  documented where it lives, like any other declaration. With Compose Multiplatform UI, `App()` in `commonMain` and
  `MainViewController()` in `iosMain` (the Swift entry point) are public API.
- **Composables** (`@Composable` functions in shared UI or the Android app): describe what the composable renders,
  each parameter (state, callbacks — when they fire, `modifier`), and side effects (`LaunchedEffect`, navigation),
  following the project's own practice for preview functions (usually `private`, out of the bar).
- **Android app module**: activity/application/ViewModel classes follow the same bar the project applies to app code
  (observed practice decides; Dokka usually isn't applied there, so Step 6 may only build the KMP module).

For each gap record: the declaration (with its source set), what's missing (whole comment vs. a tag), its visibility,
and — for an `actual` — whether the gap is really on its `expect`.

## Step 4 — Ensure each touched module and package has narrative docs

Dokka takes module/package documentation from Markdown `includes`, configured per source set. For each KMP module
with Dokka applied:

- Find the wiring: **Dokka 2** `dokka { dokkaSourceSets.configureEach { includes.from("module.md") } }` (or
  `named("commonMain") { includes.from(...) }`) in the module's build script or a convention plugin; **Dokka 1**
  `tasks.dokkaHtml { dokkaSourceSets { configureEach { includes.from("module.md") } } }`. `configureEach` is the
  right shape for KMP — the file then applies to every source set (verified: the `# Module shared` text rendered on
  the generated index).
- Confirm a `# Module <name>` heading with a real description (the name must match Dokka's module name — the Gradle
  project name, e.g. `shared`) and a `# Package <fqn>` section with a non-empty description for each touched package.
- Missing → create/complete `module.md` at the module root (summarizing what the shared module provides to both
  platforms, from the in-scope classes' actual responsibilities) and add the `includes.from("module.md")` wiring to
  the module's existing `dokka {}` block with Edit — the only build-file edit this skill makes. If Dokka isn't applied
  to the module at all, write the file, report "Dokka not configured for `<module>`", and skip Step 6 for it (never
  add the plugin). An Android app module without Dokka gets no `module.md`.
- An existing package gaining classes → extend its description only for a genuinely new concept.

## Step 5 — Generate the missing KDoc

Write each missing comment grounded in the actual implementation (read the body — and, for an `expect`, read **every**
`actual` so the shared KDoc is true on all platforms), in the current uncommitted/branch changes (`git diff`, `git log
-p`), and in the phrasing conventions from Step 2. Apply with Edit; never modify code, signatures, annotations,
imports, formatting outside the comment, or member order.

## Step 6 — Verify the KDoc builds

Identify the Dokka generation and task per module:

```bash
./gradlew :<module>:tasks --all | grep -iE '^dokka'
```

Dokka 2 (V2 mode — the default from 2.1) registers `dokkaGenerate`, `dokkaGenerateHtml`, `dokkaGenerateModuleHtml`,
`dokkaGeneratePublicationHtml`, and lists the V1 tasks as `[⚠ V1 tasks disabled]` — a listed `dokkaHtml` alone doesn't
mean V1 mode. Run the narrowest:

```bash
export JAVA_HOME=$(/usr/libexec/java_home -v 21)    # the default JDK may be newer than AGP/Kotlin support
./gradlew :<module>:dokkaGeneratePublicationHtml     # Dokka 2: HTML only
./gradlew :<module>:dokkaGenerate                    # Dokka 2 fallback: every configured publication
./gradlew :<module>:dokkaHtml                        # Dokka 1, or 2.x in V1 mode
```

Output: `<module>/build/dokka/html/index.html` unless `dokkaPublications.html { outputDirectory… }` moves it (the
catalog's scaffold copies it into the Antora site's `api/` — that's the docs pipeline's job, not this skill's). Retry
once with `--no-configuration-cache` on a configuration-cache error.

**Reading the result** — Dokka fails only on structural problems (or on warnings when `failOnWarning` is set). Read the
console regardless of the exit code: `w: [:<module>:dokkaGeneratePublicationHtml] Couldn't resolve link: [X] in
<File>.kt/<fqn> (:<module>/<sourceSet>)` — **one warning per source set the KDoc is shown in**, so a broken link in an
`expect`'s KDoc is reported once for `commonMain` and again for each `actual` (fix it once, on the `expect`); and,
with `reportUndocumented`, `Undocumented: <pkg>/<Class>/<member>/… (common|android|ios)` — the suffix names the source
set to fix. Fix every warning tied to an in-scope file and re-run until none remain; out-of-scope warnings are
pre-existing — list them, don't fix them.

**iOS source sets need macOS**: Dokka analyzes `iosMain` against the Kotlin/Native platform libraries, which are only
available on a macOS host (the first run downloads the Kotlin/Native toolchain). On another OS, iOS source sets may be
skipped or produce unresolved-platform-symbol warnings — report the `iosMain` part of the build as **unverified
(non-macOS host)** rather than clean.

**A clean Dokka run does not prove completeness** unless `reportUndocumented` is on — Step 3's audit is the gate; Step 6
proves the KDoc that exists is well-formed and its links resolve.

## Step 7 — Report

Per file/class in scope (grouped by source set): declarations already fully documented, gaps found and filled (name
each; for expect/actual pairs say which side got the KDoc and whether an `actual` received a platform-specific note),
and `@suppress`-tagged exclusions. Per module/package: whether `module.md`/`# Package` coverage existed, was extended,
or was created, and whether `includes` wiring was added. Then the Dokka result per module (task, Dokka version/mode,
pass with zero in-scope warnings or the exact warnings), the output location, any `iosMain` part reported unverified,
the arguments dropped (tests, Swift, build scripts), and pre-existing out-of-scope warnings as a follow-up.

Do not fix detekt/ktlint findings unrelated to KDoc, add or change tests, or apply/configure Dokka where it isn't
applied — those belong to `iru-kmp-code-quality`, the coding/test skills, and the user.

## Known quirks / verification notes

- **Verified** in `$TMPDIR/iru-verify/kmp/iru-kmp-dokka/` (October 2026, macOS, Gradle 9.8.1, JDK 21, Kotlin 2.4.21,
  AGP 9.4.1 with `com.android.kotlin.multiplatform.library`, `iosArm64` + `iosSimulatorArm64`, `org.jetbrains.dokka`
  **2.2.0**, no `gradle.properties` mode switch): `:shared:tasks --all` listed `dokkaGenerate`, `dokkaGenerateHtml`,
  `dokkaGenerateModuleHtml`, `dokkaGeneratePublicationHtml` and the V1 tasks as disabled;
  `:shared:dokkaGeneratePublicationHtml` (and `:shared:dokkaGenerate`) wrote `shared/build/dokka/html/index.html`
  with **BUILD SUCCESSFUL** despite warnings. With `dokka { dokkaSourceSets.configureEach { reportUndocumented.set(true);
  includes.from("module.md") } }`: a `[NoSuchThing]` link in an `expect fun`'s KDoc produced three `Couldn't resolve
  link` warnings, tagged `(:shared/commonMain)`, `(:shared/androidMain)` and `(:shared/iosMain)` (the actuals had no
  KDoc of their own — they inherited it); the undocumented actuals produced **no** `Undocumented:` line; an
  undocumented common member printed `Undocumented: com.example.shared/Greeter/magic/#kotlin.Int/ (common)` and an
  undocumented `iosMain`-only `fun` printed `Undocumented: com.example.shared/iosOnlyHelper/#/ (ios)`; the
  `module.md` text rendered on the index page.
- **Unverified locally**: Dokka 1 (`dokkaHtml`) on a KMP module, a non-macOS host's handling of `iosMain`, Dokka on
  the Android application module, and multi-module aggregation. Look up the current Dokka version at run time
  (Gradle plugin portal `org.jetbrains.dokka`); October 2026 fallback: **2.2.0** (2.3.0 was in Beta).
- `suppressInheritedMembers` (source-set option) hides inherited members — don't flag inherited-but-undocumented
  overrides when it's set.
