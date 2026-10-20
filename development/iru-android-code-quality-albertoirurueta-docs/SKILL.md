---
name: iru-android-code-quality
description: Run an Android/Kotlin module's wired static-analysis tools — Android Lint (always available via AGP's `lintDebug` task), Detekt (only when `io.gitlab.arturbosch.detekt` is applied), and ktlint (only when wired, either through Spotless's `spotlessCheck` task or the standalone `org.jlleitschuh.gradle.ktlint` plugin) — then read the generated `<module>/build/reports/lint-results-debug.xml` (Android Lint), `<module>/build/reports/detekt/detekt.xml` (Detekt, Checkstyle-format) or its SARIF sibling, to report every issue found (file, line, rule/issue id, severity, message), grouped by tool and classified by id/severity (Fatal/Error/Warning/Informational). Invoke as `/iru-android-code-quality` to check the whole module (`lib` by default), or `/iru-android-code-quality <scope>` where `<scope>` is a file/class name or path to scope the *reported* summary — Lint/Detekt/Spotless always analyze the whole module in one Gradle invocation (none of them expose a per-file CLI selector the way Surefire's `-Dtest` does), so a scoped invocation still runs everything and only filters the report. Verifies each tool is actually wired (plugin applied, config file present) before trusting a "zero issues" result from it, and explicitly reports a tool as "not wired" instead of silently omitting it or claiming it found nothing. When the prompt supplies a baseline (a prior per-id/severity issue count or list from an earlier run of this skill), reports only the new-vs-baseline diff instead of the full current list. Use whenever the user wants a lint/static-analysis pass called out separately from `iru-android-test`/`iru-android-coverage`, instead of eyeballing `./gradlew lintDebug` console output.
model: haiku
---

# Android Code Quality

Run whichever static-analysis tools a module actually has wired and report every issue they find. This skill
only runs static analysis and reports results — it does not fix issues or modify source/lint/Detekt/Spotless
configuration unless asked to as a follow-up.

## Step 0 — Resolve inputs

**Kotlin Multiplatform projects are out of scope.** If the Kotlin Multiplatform plugin (`kotlin("multiplatform")`/`org.jetbrains.kotlin.multiplatform`, directly or via a `libs.versions.toml` alias) is applied anywhere in the build — a KMP app's Android host module included — stop and hand the request to `iru-kmp-code-quality` instead (or tell the caller to, when it isn't installed); this skill assumes a plain Android `lib`/`app` layout.

`<scope>` (optional) is a file path or class/file simple name used to filter the report in Step 3 — not a Gradle
selector, since none of these tools accept a per-file CLI argument in this project shape. No `<scope>` → report
everything project-wide. If the calling skill/prompt passes explicit `key: value` lines (e.g. `module: app`, a
baseline list), honor them and skip the matching inference below. Resolve the module the same way
`iru-android-test`/`iru-android-coverage` do: infer `:lib` (default) or `:app` from a path in `<scope>`, or from
an explicit `module:` line.

Prerequisites are the same as the other two Android gate skills: `JAVA_HOME` on JDK 17+, `ANDROID_HOME`/
`local.properties` set, `./gradlew` present.

## Step 1 — Verify which tools are wired

Check every one of these before running anything — a "zero issues" result from a tool that was never actually
configured is meaningless and must not be reported as a clean pass:

- **Android Lint** — always available via AGP on an Android module; no extra plugin to check for. Confirm the
  module actually builds a `lint`/`lintDebug` task: `./gradlew :<module>:tasks --all | grep -i lint`. On a
  **library** module the task is `lintDebug` (the reference scaffold's `com.android.library` plugin, variant-
  aware); plain `lint` also exists as an aggregate alias but `lintDebug` is what this skill runs, to match the
  variant whose coverage/reports this catalog otherwise scopes to (`debug`). Recommend (don't silently assume) the
  scaffold sets `lint { abortOnError = false; xmlReport = true; sarifReport = true }` in the module's
  `build.gradle.kts` — without `abortOnError = false`, a single `Fatal`-severity issue aborts the build before the
  XML report is written at all, which this skill would otherwise misreport as "Lint not wired" instead of "Lint
  found a fatal issue"; check for this setting and note its absence in the report if the XML file never appears
  despite Lint clearly having run.
- **Detekt** — `io.gitlab.arturbosch.detekt` (or `alias(libs.plugins.detekt)`) applied in the module's
  `build.gradle.kts`. A `detekt.yml` config file at the repo root is common but not required (Detekt runs with
  its bundled default ruleset without one) — note whether a custom `detekt.yml` exists, since that changes what
  "detekt found nothing" actually means (bundled defaults vs. this project's own bar).
- **ktlint** — either (a) Spotless (`com.diffplug.spotless`) applied with a `kotlin { ktlint(...) }` block (its
  check task is `spotlessCheck`, not a ktlint-named task), or (b) the standalone
  `org.jlleitschuh.gradle.ktlint` plugin (its check task is `ktlintCheck`). These are two different Gradle plugins
  wrapping the same ktlint engine — detect which one (if either) is applied and use its own task name; don't
  assume Spotless just because ktlint formatting is enforced.

If a tool's plugin/config isn't found, **skip running it and say so in the report** (e.g. `"Detekt: not wired (no
io.gitlab.arturbosch.detekt plugin applied)"`) instead of silently omitting it or reporting a misleading "0
issues" — this is the one hard rule this skill exists to enforce (per this catalog's gate-skill convention: never
let an absent tool look like a passing one).

## Step 2 — Run each wired tool

```bash
./gradlew :<module>:lintDebug                 # always, AGP-provided
./gradlew :<module>:detekt                    # only if Detekt is wired
./gradlew :<module>:spotlessCheck             # only if Spotless/ktlint is wired via Spotless
./gradlew :<module>:ktlintCheck               # only if the standalone ktlint plugin is wired instead
```

Combine the wired ones into a single invocation when convenient (`./gradlew :<module>:lintDebug :<module>:detekt
:<module>:spotlessCheck`) — Gradle runs each task once regardless of how many are named on one command line, and
this avoids re-configuring the project per tool. **Lint and Detekt tasks succeed even when they find issues** (the
build only fails on a `Fatal`-severity Lint issue when `abortOnError` isn't relaxed, or when Detekt's own
`ignoreFailures`/max-issues threshold is exceeded) — a non-zero exit here is itself informative (issues at/above
the configured failure threshold exist), not necessarily "the tool is broken"; always still go on to parse the
report rather than stopping at the exit code. `spotlessCheck`/`ktlintCheck` **do** fail on any formatting
violation by design — same handling: parse the report anyway.

If a wired tool's underlying compile step fails outright (unrelated to lint/style rules — e.g. a real Kotlin
compile error), report that and stop for that tool; its report wasn't meaningfully (re)generated, so don't read a
stale copy from an earlier run.

## Step 3 — Parse each generated report, scoped to `<scope>` if given

**Android Lint** — `<module>/build/reports/lint-results-debug.xml`:

```xml
<issue id="NewApi" severity="Error" message="Call requires API level 30 (current min is 26): `Foo#bar`" ...>
    <location file="/abs/path/Foo.kt" line="42" column="9"/>
</issue>
```

```python
import xml.etree.ElementTree as ET

scope = None  # a path/filename substring, or None for everything
root = ET.parse("<module>/build/reports/lint-results-debug.xml").getroot()
for issue in root.findall("issue"):
    loc = issue.find("location")
    f = loc.get("file") if loc is not None else "?"
    if scope and scope not in f:
        continue
    print(f"{f}:{loc.get('line') if loc is not None else '?'} [{issue.get('severity')}] "
          f"{issue.get('category')}/{issue.get('id')}: {issue.get('message')}")
```
`severity` is one of Lint's own four levels: `Fatal`, `Error`, `Warning`, `Informational` — report counts broken
down by this exact set, not collapsed into a generic error/warning pair. An `<issue>` can carry more than one
`<location>` (a secondary location explaining the primary one); the first is the reportable file:line, read
further ones only if the message references "also see"/similar. Each `<issue>` also carries a `category` attribute
(`Correctness`, `Performance`, `Usability:Icons`, `Accessibility`, …) — keep it: the `Accessibility` issues
(`ContentDescription`, `ClickableViewAccessibility`, `LabelFor`, `KeyboardInaccessibleWidget`, …) are what the catalog's UI contract asks to see called out (verified: an
`ImageView` without `contentDescription` reported `id="ContentDescription" severity="Warning"
category="Accessibility"`).

**Detekt** (Checkstyle format) — `<module>/build/reports/detekt/detekt.xml`:

```xml
<file name="/abs/path/Foo.kt">
    <error line="42" column="1" severity="error" message="This expression contains a magic number: 42."
           source="detekt.MagicNumber"/>
</file>
```

```python
import xml.etree.ElementTree as ET

scope = None
root = ET.parse("<module>/build/reports/detekt/detekt.xml").getroot()
for f in root.findall("file"):
    fname = f.get("name")
    if scope and scope not in fname:
        continue
    for err in f.findall("error"):
        rule = err.get("source", "").rsplit(".", 1)[-1]   # "detekt.MagicNumber" -> "MagicNumber"
        print(f"{fname}:{err.get('line')} [{err.get('severity')}] {rule}: {err.get('message')}")
```
A `<file>` with no `<error>` children is clean, same convention as `iru-java-code-quality`'s Checkstyle/PMD
handling. `severity` here is only `warning`/`error` (Checkstyle's two-level scale, not Lint's four) — keep Detekt
and Lint severities in clearly separate buckets in the report, don't merge them into one shared scale. If Detekt
was configured to emit SARIF instead (`sarifReport.required = true`, no `xml` counterpart), parse
`<module>/build/reports/detekt/detekt.sarif` as JSON instead: `runs[].results[]`, each with `ruleId`,
`level` (`error`/`warning`/`note`), and `locations[].physicalLocation.{artifactLocation.uri,
region.startLine}`.

**Spotless (`spotlessCheck`)** — has no separate XML report; a violation is reported straight in the Gradle
console output/failure as one line per non-compliant file, e.g. `The following files had format violations:
src/main/java/com/example/lib/Foo.kt`. Parse that from the captured Gradle output rather than a report file:
count of files listed, one `formatting` bucket (like Prettier in the TypeScript sibling skill) — Spotless doesn't
have per-line rule ids.

**Standalone ktlint (`ktlintCheck`)**, if that's the wired plugin instead — writes
`<module>/build/reports/ktlint/ktlintMainSourceSetCheck/ktlintMainSourceSetCheck.txt` (plain text, one
`<file>:<line>:<col>: <message> (<rule-id>)` line per violation) or a matching `.xml`/`.html` sibling depending on
the configured reporters; parse whichever text/XML file is present the same way as Detekt's Checkstyle format if
XML, or line-by-line if only the `.txt` reporter is enabled.

**Scoping**: with no `<scope>`, report every parsed entry from every tool that ran. With a `<scope>`, filter each
tool's parsed entries to ones whose file path contains `<scope>` — an empty result after filtering means that
tool found nothing in `<scope>`, not that it didn't run; say so rather than omitting the tool line entirely.

Verified against hand-written fixtures under `$TMPDIR/iru-verify/android/gates/`: `lint/lint-results-debug.xml`
(three issues — two `Warning`, one `Error`, across three files) parsed to the correct per-severity/per-id counts
both unscoped (`total: 3`) and scoped to `Foo.kt` (`total: 1`, the `NewApi` `Error`); `detekt/detekt.xml` (one
file with a `warning`-level `MissingKDocForPublicFunction` and an `error`-level `MagicNumber`, one clean file)
parsed to `by rule: {'MissingKDocForPublicFunction': 1, 'MagicNumber': 1}` and `by severity: {'warning': 1,
'error': 1}`.

## Step 4 — Classify, diff against a baseline if given, and report

Bucket every issue by **tool, then by id** (Lint's `id`, Detekt's `source` rule name, ktlint's rule id,
Spotless's single `formatting` bucket) — never merge buckets across tools even when an id/rule name looks similar,
the same convention `iru-typescript-code-quality` uses for ESLint vs. Oxlint. Within each tool, also report the
severity breakdown (Lint: Fatal/Error/Warning/Informational counts; Detekt/ktlint: error/warning counts).

**Report**: state an overall total across all tools at the top, then per tool: whether it ran or was skipped as
"not wired" (Step 1), a total issue count, the severity breakdown, and one line per id/rule bucket with its count
and (for a scope smaller than the whole module) the file:line list. For Android Lint, add one **Accessibility** line — the count of
`category="Accessibility"` issues and their ids (or "0 accessibility issues") — even when it is zero, so a UI
change's accessibility lint result is always visible.

**Baseline diff** — when the prompt supplies a baseline (a prior run's per-tool/per-id counts or itemized list,
the same contract `iru-java-code-one-task-group`/`iru-typescript-code-one-task-group` use for their language's
code-quality skill): compute the diff yourself — report only issues that are new since the baseline (an id whose
count increased, or one that appears now but didn't before; a specific new file:line entry when the baseline was
itemized). An id whose count decreased or stayed the same is not a regression and is omitted from the diff (it
still appears in the plain, non-baseline count above it). If a tool wasn't run in the baseline (it was unwired
then, or newly added since), treat every one of its current issues as new rather than silently skipping it.

Do not attempt to fix any of the issues found, or modify Lint/Detekt/Spotless/ktlint configuration — that's a
follow-up the user (or `iru-android-code-one-task`) drives explicitly.

## Known quirks / verification notes

- Gradle/AGP need **JDK 17+**; set `JAVA_HOME` explicitly rather than trusting the machine's default `java`.
- `ANDROID_HOME`/`local.properties` missing fails the build at configuration time before Lint/Detekt/Spotless run.
- **Lint on a library module** uses the variant-scoped `lintDebug` task, not the bare `lint` aggregate alias, to
  stay consistent with this catalog's `debug`-variant scoping for coverage; an `app` module's release-signing
  concerns don't apply to `lintDebug` either way.
- `lint { abortOnError = false }` must be set for the XML report to reliably exist after a run containing a
  `Fatal` issue — without it, the build aborts before writing `lint-results-debug.xml`, which looks identical to
  "Lint isn't wired" unless this is checked for explicitly (Step 1).
- `lintDebug`'s console output names only the HTML and SARIF reports (`Wrote HTML report to …`/`Wrote SARIF report
  to …`) — the XML report is written silently alongside them (verified against a generated `iru-setup-android-library` scaffold),
  so check that `lint-results-debug.xml` exists on disk rather than waiting for a console line that names it.
- Configuration cache can be incompatible with some third-party tasks (Detekt and Spotless have both shipped
  configuration-cache-incompatible releases historically); retry once with `--no-configuration-cache` if a
  run fails with a configuration-cache-specific error unrelated to the actual lint/style findings.
- Spotless/ktlint have no per-file CLI selector any more than Lint/Detekt do — `<scope>` only narrows the
  *report*, never the underlying Gradle invocation, for every tool this skill runs.
- This skill's XML parsing (Step 3) was verified against hand-written fixtures in
  `$TMPDIR/iru-verify/android/gates/{lint,detekt}/` only; the live `./gradlew :lib:lintDebug`/`:lib:detekt`/
  `:lib:spotlessCheck` invocations against a generated `iru-setup-android-library` scaffold, and whether
  Detekt/Spotless/ktlint are even opted into that scaffold by default, are **unverified locally by this skill's
  author; exercised by the scaffold and workflows skills' own verification passes**. The Android Lint report path (`build/reports/lint-results-debug.xml`) is taken directly from the
  reference repository's own `sonar.android.lint.report` property in
  [irurueta-android-glutils](https://github.com/albertoirurueta/irurueta-android-glutils)'s `lib/build.gradle.kts`
  — that repository itself does not wire Detekt/Spotless/ktlint, so their exact task/report names here follow
  each plugin's own documented defaults rather than an observed example in the reference repo.
