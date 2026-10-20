---
name: iru-android-dokka
description: Audit given Kotlin class(es)/file(s)/package scope for complete KDoc coverage — class/interface/object/enum/annotation-level doc, primary-constructor parameters (via `@property` for declared properties, `@param` for plain constructor parameters), every function (including private ones, per the discovered bar), every property, enum entries, companion-object members, top-level functions/properties, and nested/inner declarations — required tags `@param`/`@return`/`@throws`/`@sample`/`@see`, `@suppress` honored for intentionally hidden members, and Dokka `module.md`/`package.md` includes wired via `dokkaSourceSets { includes.from(...) }` for every module/package touched (creating them if missing) — generate any missing or incomplete KDoc grounded in the actual code and current changes, then run the project's `dokkaGenerate` Gradle task to confirm the generated Dokka V2 site is well-formed and report per-file gap counts plus the build outcome. Invoke as `/iru-android-dokka <scope>` where `<scope>` is a comma-separated list of class names, file paths, or a package glob, or `/iru-android-dokka` with no argument to scope to classes touched by uncommitted changes plus commits on the current branch not yet on the base branch. Works against any Kotlin/Android Gradle project using the Dokka V2 Gradle plugin — it discovers the project's own documentation bar (from a `detekt.yml`'s `UndocumentedPublicClass`/`UndocumentedPublicFunction`/`UndocumentedPublicProperty` rules, or observed practice when none is configured) rather than assuming a fixed style. Use whenever the user wants KDoc completeness checked and filled in for specific classes/modules, instead of relying on a full `dokkaGenerate` run to surface gaps (which, unlike Javadoc/TypeDoc, does not fail or warn on undocumented members by default).
model: sonnet
---

# Android Dokka

Make sure a set of Kotlin declarations — and the module(s)/package(s) they live in — carry complete, well-formed
KDoc, filling in whatever is missing, then prove the result actually builds via the project's own Dokka V2
tooling. This skill only adds/completes documentation comments (including creating missing `module.md`/
`package.md` includes and wiring them into `dokkaSourceSets`) — it does not change behavior, signatures, or
non-KDoc code. Test classes (`src/test/java`, `src/androidTest/java`) are out of scope for documentation
requirements — they don't need class/member-level KDoc added, even if named explicitly — but any KDoc a test
class already has must be left as-is; never strip or "clean up" existing comments in test code. It makes no
assumptions about this being any particular repository — discover the project's actual conventions and Dokka
setup fresh each run. The phrasing and tag conventions this skill defaults to when a project has nothing to learn
from are grounded in real Kotlin/Android KDoc as written in
[irurueta-android-glutils](https://github.com/albertoirurueta/irurueta-android-glutils) (genericized below — no
example names that specific package or project).

## Step 1 — Determine scope

**Kotlin Multiplatform projects are out of scope.** If the Kotlin Multiplatform plugin (`kotlin("multiplatform")`/`org.jetbrains.kotlin.multiplatform`, directly or via a `libs.versions.toml` alias) is applied anywhere in the build — a KMP app's Android host module included — stop and hand the request to `iru-kmp-dokka` instead (or tell the caller to, when it isn't installed); this skill assumes a plain Android `lib`/`app` layout.

- **Argument provided** (comma-separated class names, file paths, or a package glob): resolve each to its file. If
  given a simple class/object name, locate it via `find`/`grep` across every module's main source root
  (`src/main/java` and `src/main/kotlin`, whichever this project actually uses — both are valid for Kotlin) rather
  than guessing the module or package. If a resolved file turns out to live under a test source root
  (`src/test/java`, `src/androidTest/java` by convention), drop it from the scope audited/generated in Steps 3-6 —
  say so in the Step 7 report rather than silently ignoring it — since test classes carry no KDoc requirement
  here.
- **No argument**: default to every main-source `.kt` file touched by uncommitted changes plus commits on the
  current branch not yet on the base branch, same approach as `iru-update-docs`:
  ```bash
  git status
  git diff <base-branch>...HEAD --name-only
  git diff --name-only
  ```
  (determine the base branch via `git symbolic-ref refs/remotes/origin/HEAD` or `git branch -a` if unclear; ask
  the user only if genuinely ambiguous). Filter the changed-file list to a main Kotlin source root — skip test
  code, `build/` output (including `build/generated`), and non-Kotlin files.
- If the resulting scope is empty (no argument and no relevant changes), tell the user there is nothing to
  document and stop.
- From the in-scope files, derive the distinct set of Gradle modules (e.g. `lib`, `app`) and packages involved
  (each file's `package` declaration) — these feed Step 4, which checks each module has a `module.md` and each
  touched package has appropriate coverage in a `package.md`/module-level `# Package <fqn>` section.

## Step 2 — Discover this project's actual KDoc bar before auditing

Don't assume a fixed documentation scope — discover it from the project itself, since projects vary on whether
internal/private members need KDoc:

- Check for a contributor guide (`CLAUDE.md`, `AGENTS.md`, a top-level `README`, or a `CONTRIBUTING` file) for any
  stated KDoc convention.
- Check for a Detekt config (`detekt.yml`/`detekt.yaml`, referenced from `build.gradle.kts`'s `detekt { config.from(...) }` or the default `config/detekt/detekt.yml` location) for the `comments` rule set's `UndocumentedPublicClass`,
  `UndocumentedPublicFunction`, and `UndocumentedPublicProperty` rules — read their `active` flag and any
  `searchInNestedClass`/`searchInInnerClass`/`searchInInnerObject`/`searchInProtectedClass` overrides. A project
  with none of these active, or no Detekt config at all (common — the reference repository above ships no
  `detekt.yml`), gives no enforced bar from this source; fall back to the next check.
- Check the module's `build.gradle.kts` `dokka { dokkaSourceSets { named("main") { documentedVisibilities.set(...) } } }`
  setting (Dokka's own visibility filter for what appears in the generated site: default is `PUBLIC` only). If a
  project widens this to include `INTERNAL` or `PROTECTED`, treat those visibilities as in-scope for the audit
  too, since they're part of what actually gets published.
- If neither gives a clear answer, skim 2-3 existing classes near the ones in scope to see empirically whether the
  project already documents internal/private members, or only public ones — treat that observed practice as the
  bar, since a stated convention looser than what the codebase actually does would leave real gaps unaddressed.
- Reconcile any conflict between a stated/configured convention and the actually-enforced/observed one by
  following the **stricter** of the two.

Skim a couple of existing, well-documented classes/objects/enums in the project (prefer ones structurally similar
to what's in scope) to internalize the exact phrasing conventions before writing new KDoc: person and tense used,
whether summary sentences end in a period, how a rotation/coordinate-system caveat or similar cross-cutting note
is phrased as a follow-up paragraph after the summary, the `@param`/`@return`/`@throws` ordering, and whether
`[SquareBracketLinks]` are used for cross-references to other declarations instead of a bare name. If the project
has no existing KDoc to learn from, fall back to standard KDoc convention:

- **Summary first**: one concise sentence, third person present tense, followed by a blank KDoc line then any
  longer explanation.
- **`@param name description`** (no hyphen, no `{type}` — KDoc's own form, distinct from both Javadoc and TSDoc) —
  one per constructor/function parameter, in declaration order.
- **`@property name description`** — for every property declared directly in a primary constructor (`class Foo(val bar: Int)`), instead of `@param`, since Dokka renders these as documented properties, not parameters.
- **`@return`** — one sentence describing the returned value; omitted for `Unit`.
- **`@throws ExceptionType description`** — one per exception the implementation can actually throw or that is
  annotated via `@Throws(ExceptionType::class)`.
- **`@see OtherDeclaration`** — for a related declaration worth cross-referencing (e.g. a companion helper class),
  in addition to or instead of an inline `[OtherDeclaration]` link in the prose.
- **`@sample com.example.SampleFile.sampleFunction`** — only on a public entry point where a project already uses
  runnable samples (a function elsewhere whose body Dokka embeds as example code); never invent a sample function
  that doesn't exist just to satisfy this tag.
- **`@suppress`** — carried over verbatim on a member intentionally hidden from generated docs; never add it new
  (that's a decision only the code owner makes) — but if an existing gap looks like it might be an accidental
  omission mislabeled as suppressed, flag it in the Step 7 report rather than silently accepting it.
- **`[Declaration]`** — square-bracket KDoc links for cross-references instead of a bare name in backticks.

## Step 3 — Audit each in-scope declaration

Read the full file, then check every one of the following is present, non-empty, and actually describes the
member's purpose (not just restates its name), scoped per the bar established in Step 2:

- **Type-level**: a doc comment on the class/interface/object/enum/annotation/sealed-class itself, including
  `@param <T>` for each generic type parameter declared on the type.
- **Primary constructor**: `@property`/`@param` per parameter as described in Step 2, and `@throws` for any
  exception the constructor validation can throw.
- **Secondary constructors**: same treatment as a regular function, one doc block per overload.
- **Properties**: every `val`/`var` within the discovered scope, including ones with a custom getter/setter whose
  behavior isn't obvious from the type alone.
- **Functions**: every function within scope — top-level, member, extension, or companion — with `@param` per
  parameter, `@return` unless `Unit`, and `@throws` for every exception the implementation can actually throw.
- **Enum entries**: a doc comment on each entry whose meaning isn't self-evident from its name alone.
- **Companion object members**: same checks as any other member, since Dokka documents them as part of the
  enclosing type's page.
- **Nested/inner classes, interfaces, objects, enums**: recurse into these with the same checks as top-level
  types.
- **`@suppress`-tagged members**: excluded from the gap list (Step 2), but recorded as "suppressed" in the Step 7
  report rather than silently skipped.

For each item found incomplete or missing entirely, record: the member, what's missing (whole comment vs. a
missing `@param`/`@return`/`@throws` tag), and its current visibility.

## Step 4 — Ensure each touched module has a `module.md` and each touched package is covered

Dokka V2 wires narrative module/package documentation through `includes.from(...)` on a source set, not through a
per-directory file the compiler discovers on its own (unlike Java's `package-info.java`). For each module derived
in Step 1:

- Check the module's `build.gradle.kts` for a `dokka { dokkaSourceSets { named("main") { includes.from(...) } } }`
  block (or the module-level `dokka {}` block, whichever Dokka V2 DSL shape this project already uses). If one
  exists, read every file it lists and confirm at least one contains a `# Module <module-name>` heading (module
  overview) and, for each touched package, a `# Package <fully.qualified.name>` heading with a non-empty
  description beneath it — these can live in one combined file or be split as `module.md` + one `package.md` per
  package, whichever convention the project already follows.
- If the wiring or the file(s) are missing or the relevant heading is absent/placeholder-only, create/complete
  them:
  - `module.md` at the module root (e.g. `lib/module.md`), starting with `# Module <module-name>` followed by a
    short paragraph summarizing what the module provides, based on the in-scope classes' actual responsibilities.
  - A `# Package <fqn>` section (in the same file or a dedicated `package.md`) for every touched package that
    doesn't already have one, summarizing that package's classes.
  - If `includes.from(...)` isn't wired yet, add it to the module's `dokka { dokkaSourceSets { named("main") { ... } } }`
    block via the Edit tool — this is the one piece of build-file editing this skill performs, since without it
    the file(s) it just wrote are silently ignored by Dokka.
- For an existing package gaining new in-scope classes, extend the current description only if the new classes
  introduce a concept not yet mentioned; leave an already-accurate description untouched.

## Step 5 — Generate the missing KDoc

For every gap found in Step 3, write the KDoc directly grounded in:

- The member's actual implementation (parameter usage, return expression, thrown exceptions, the actual condition
  a property's custom accessor evaluates) — read the function/property body, don't infer purely from the
  signature/name.
- Any current uncommitted/branch changes to that member (`git diff` / `git log -p` for that file/hunk if the
  member was just added or modified) — if the change altered behavior, the new KDoc must describe the current
  behavior, not stale prior behavior a name alone might suggest.
- The phrasing conventions gathered in Step 2 — match voice, tense, and tag ordering/style exactly so the new
  comments are indistinguishable from hand-written ones in this codebase.

Apply the edits with the Edit tool. Do not modify code logic, signatures, formatting outside the added comments,
or reorder members — this skill only adds/completes KDoc comments (and, per Step 4, the `module.md`/`package.md`
includes wiring).

## Step 6 — Verify the KDoc actually builds

Determine the module(s) to build from the scope (Step 1) — `<module>` below is whichever Gradle module each
in-scope file lives in (`lib` for a library scaffold, `app` for an app-only repository, or both when the scope
spans them; run the task once per module). Prefer the narrowest Dokka V2 task that actually generates and
validates the site without a full multi-module aggregate:

```bash
export JAVA_HOME=$(/usr/libexec/java_home -v 21)   # or -v 17; Gradle/AGP may reject a newer default JDK
export ANDROID_HOME=$HOME/Library/Android/sdk
./gradlew :<module>:dokkaGenerate
```

Fall back to `./gradlew :<module>:dokkaGeneratePublicationHtml` if the module only configures a single (HTML)
publication and `dokkaGenerate`'s aggregate task isn't registered under that exact name in this Dokka version. If
the run fails with a configuration-cache-related error (a known Dokka V2 rough edge on some versions), retry once
with `--no-configuration-cache` and note that this project needs the flag.

This **fails the build** only on structural problems (unresolved `[Link]` references, malformed KDoc syntax that
Dokka's Kotlin-compiler-based parser can't parse, a misconfigured `dokkaSourceSets` block) — read any reported
warnings/errors, they name the exact file and declaration. If it fails or warns, fix the offending comment(s) and
re-run until it succeeds with no warnings tied to files in scope. Warnings in files outside the current scope are
pre-existing — note them in the report but don't fix them unless the user asks.

**This build succeeding does not by itself prove KDoc completeness** — unlike Javadoc or TypeDoc with
`--validation.notDocumented`, Dokka has no built-in flag that fails the build over an undocumented public member;
an undocumented class/function simply renders with just its signature and no description, silently. Step 3's
manual audit is the actual completeness gate here; Step 6 only proves the KDoc that *does* exist is well-formed.

## Step 7 — Report

Per class in scope, state: how many members were already fully documented, how many gaps were found and filled
(name each), and how many were `@suppress`-tagged and excluded. Separately, state per module/package whether its
`module.md`/`package.md` coverage already existed and was complete, was extended, or was newly created (and
whether `includes.from(...)` wiring had to be added). Report the final `dokkaGenerate` result (pass, or the exact
warning text and declaration names that failed) and the output location (`<module>/build/dokka/html`). If any
argument resolved to a test class (Step 1), name it and note it was excluded since test classes carry no KDoc
requirement here. If any out-of-scope pre-existing Dokka warning surfaced in Step 6, mention it separately as a
follow-up rather than silently leaving it out of the report.

Do not run a full multi-module Dokka aggregate beyond what Step 6 needs, fix Detekt/lint issues unrelated to
KDoc, or add/modify tests — those are `iru-android-code-quality` and `iru-android-generate-all-tests`'s jobs
respectively, not this skill's.

## Known quirks / verification notes

- **Dokka V2 task names differ from V1.** V2 (gated by `org.jetbrains.dokka.experimental.gradle.pluginMode=V2Enabled`
  in `gradle.properties`, the mode the catalog's Android scaffold — `iru-setup-android-library` — writes by
  default) registers `dokkaGenerate` as the aggregate task and `dokkaGeneratePublicationHtml` per publication,
  replacing V1's `dokkaHtml`. Look up the current Dokka Gradle plugin version at run time via
  `https://plugins.gradle.org/m2/org/jetbrains/dokka/org.jetbrains.dokka.gradle.plugin/maven-metadata.xml`;
  September 2026 fallback: **2.1.0** (the version actually pinned in the reference repository's
  `gradle/libs.versions.toml`).
- **Output path moved.** V2's default HTML output is `<module>/build/dokka/html` (V1 used `build/dokka` directly)
  — confirm the exact path from the task's own console output rather than assuming, since a custom `dokka { dokkaPublications.named("html") { outputDirectory.set(...) } }` override changes it.
- **`dokkaGenerate` needs the Android SDK configured** the same way a normal Android Gradle build does
  (`ANDROID_HOME`/`local.properties` `sdk.dir`, accepted licenses) even though Dokka itself never touches an
  emulator — the module's `com.android.library`/`com.android.application` plugin still configures Android
  variants during Gradle's configuration phase, before Dokka's own tasks run.
- **Warnings vs. errors**: Dokka reports unresolved link warnings and malformed-KDoc errors to the console but, by
  default, does not fail the build on warnings — only on outright parse failures. A project can opt into stricter
  behavior via `dokka { dokkaSourceSets { named("main") { failOnWarning.set(true) } } }`; check for this setting
  before assuming a clean exit code means zero warnings, and grep the console output for `WARN`/`warning:` lines
  regardless of exit code.
- **`suppressInheritedMembers`**: a Dokka source-set option (`dokkaSourceSets { named("main") { suppressInheritedMembers.set(true) } }`)
  that hides members inherited from a supertype/interface from the generated site without needing `@suppress` on
  each one individually — if a project sets this, don't flag inherited-but-undocumented overrides as gaps, since
  they're intentionally excluded from the published surface already.
- **No `dokka {}` block is required for the plugin to work at all** — applying `alias(libs.plugins.dokka)` alone
  (as the reference repository does, with no source-set customization) is a valid, buildable configuration; Step
  4's `module.md`/`package.md` wiring is something this skill adds on top when narrative docs are wanted, not
  something every project already has.
- **Verification of `dokkaGenerate`/`--no-configuration-cache` itself is unverified locally by this skill's
  author** — this task's author did not run Gradle (concurrent agents were exercising the heavy Android builds).
  The scaffold's own `:lib:dokkaGenerate` run is exercised by `iru-setup-android-library`'s verification against the
  real scaffold this catalog generates; this skill's Step 6 command and quirks above are grounded in the reference repository's actual
  `gradle.properties`/`gradle/libs.versions.toml` pins and Dokka V2's documented Gradle plugin behavior, not a
  local run of this exact skill.
