---
name: iru-android-coverage
description: Generate an Android/Kotlin module's unit-test line/branch coverage report — preferring the Kover Gradle plugin's `koverXmlReportDebug` task when it's applied, falling back to the Android Gradle Plugin's own `createDebugUnitTestCoverageReport` (enabled by `buildTypes { debug { enableUnitTestCoverage = true } }`) when Kover isn't wired, and falling back further to running `testDebugUnitTest` and converting the raw `.exec` (globbed under `build/outputs/unit_test_code_coverage/` first, then `build/jacoco/`) with a vendored `jacoco-*/lib/jacococli.jar` when neither Gradle-native path emits XML — then parses the resulting JaCoCo-format XML report to report exact line/branch coverage percentages and uncovered line numbers for the requested scope. Invoke as `/iru-android-coverage [scope]`, where `[scope]` is one or more class simple names or `src/main/...` source paths (comma-separated), or with no argument to report the whole module's (`lib` by default) coverage. Detects which of the three coverage paths is actually wired before running anything and reports "coverage not wired" (naming exactly what's missing) rather than a false 0%/100% when none is configured. Never runs instrumented (`connectedAndroidTest`) coverage unless the prompt explicitly asks for it with a device attached; an existing `build/reports/coverage/androidTest/debug/connected/report.xml` is only read and reported for information when it's already on disk. Use whenever the user wants to check, or verify a bar (e.g. "at least 80% line coverage") for, an Android/Kotlin class, source path, or whole module, instead of eyeballing Gradle console output.
model: haiku
---

# Android Coverage

Run whichever unit-test coverage path a module actually has wired and report the exact, measured line/branch
coverage percentage for the scope the user cares about. This skill only measures and reports coverage — it does
not add tests or modify source/test code unless asked to as a follow-up.

## Step 0 — Resolve inputs

**Kotlin Multiplatform projects are out of scope.** If the Kotlin Multiplatform plugin (`kotlin("multiplatform")`/`org.jetbrains.kotlin.multiplatform`, directly or via a `libs.versions.toml` alias) is applied anywhere in the build — a KMP app's Android host module included — stop and hand the request to `iru-kmp-coverage` instead (or tell the caller to, when it isn't installed); this skill assumes a plain Android `lib`/`app` layout.

`[scope]` is a comma-separated list of class simple names (`Foo`, `Foo,Bar`) or `src/main/...` source paths, or
absent (whole-module report). If the calling skill/prompt passes explicit `key: value` lines (e.g. `module: app`,
a baseline percentage/bar), honor them and skip the matching inference below. Resolve the module the same way
`iru-android-test` does: infer `:lib` (default) or `:app` from a path in `[scope]`, or from an explicit `module:`
line.

Prerequisites are the same as `iru-android-test`'s Step 1: `JAVA_HOME` on JDK 17+, `ANDROID_HOME`/
`local.properties` set, `./gradlew` present — check before running anything, since a missing one produces a
configuration-time failure that looks like a coverage problem but isn't.

## Step 1 — Detect which coverage path is wired, in priority order

A module can have more than one of these present; check in this order and use the first that's actually wired —
this also decides what "coverage not wired" means if none is:

1. **Kover** — `org.jetbrains.kotlinx.kover` (or its `alias(libs.plugins.kover)` form) applied to the module's
   `build.gradle.kts`. Confirm by grepping the build file for the plugin id/alias, or
   `./gradlew :<module>:tasks --all | grep -i kover`.
2. **AGP unit-test coverage** — no Kover plugin, but the module's `buildTypes { debug { enableUnitTestCoverage =
   true } }` is set (the reference scaffold's own setting — see
   [irurueta-android-glutils](https://github.com/albertoirurueta/irurueta-android-glutils)'s `lib/build.gradle.kts`).
   AGP then exposes a `createDebugUnitTestCoverageReport` task.
3. **Vendored JaCoCo CLI** — neither of the above Gradle-native tasks, but a `jacoco-<version>/lib/jacococli.jar`
   is checked into the repo root (as in the reference scaffold) and `enableUnitTestCoverage = true` is set (JaCoCo
   still needs the `.exec` file AGP's own test instrumentation writes during `testDebugUnitTest`; only the XML
   *conversion* step is manual here, not the instrumentation itself).

If none of the three is present, **stop and report "coverage not wired"**, naming exactly what's missing (no
Kover plugin; `enableUnitTestCoverage` not set on the `debug` build type; no vendored `jacococli.jar`) — never
report a percentage for an unwired module.

## Step 2 — Run the wired path

**Kover:**
```bash
./gradlew :<module>:koverXmlReportDebug
```
XML lands at `<module>/build/reports/kover/reportDebug.xml` — Kover emits the same JaCoCo-compatible
`<counter type="..." missed="" covered="">`/`<line nr="" mi="" ci="">` shape Step 4 parses.

**AGP `enableUnitTestCoverage`:**
```bash
./gradlew :<module>:createDebugUnitTestCoverageReport
```
This task's exact emitted file name/location is not fully pinned down here — whether it produces importable XML
at all (versus only an HTML report) was not verified by this skill's author against a generated scaffold, so
**glob for it rather than hard-coding one path**:
```bash
find <module>/build/reports/coverage/test/debug -iname 'report.xml' 2>/dev/null
find <module>/build/reports/coverage/test/debug -iname '*.xml' 2>/dev/null   # wider fallback if report.xml isn't the name
```
Expect the directory to be `<module>/build/reports/coverage/test/debug/` — the same path the
`iru-setup-android-library`/`iru-setup-android-app` scaffolds' `sonar.coverage.jacoco.xmlReportPaths` property and
`iru-setup-android-github-workflows`' workflows point at (`build/reports/coverage/test/debug/report.xml`). The
upstream reference repository's `lib/build.gradle.kts` still lists `build/reports/coverage/test/report.xml`, one
level up — that is the *converted* CLI report's path, from path 3 below, not this task's own output; if a consuming
repository's `sonar {}` block still carries that older path, flag the mismatch in the report (Sonar would import 0 %
coverage) rather than silently picking one. **If the glob finds no XML file at all, fall back to Step 2's third
path (vendored CLI) automatically and say in the report that you did.**

**Vendored JaCoCo CLI** (also the automatic fallback when path 2 above produces no XML):
```bash
./gradlew :<module>:testDebugUnitTest
# AGP's enableUnitTestCoverage (the scaffolds' configuration) writes the .exec under build/outputs/…; the
# reference repo's older AGP wrote it under build/jacoco/. Glob the AGP location first, then the legacy one —
# never hard-code the file name.
EXEC=$(find <module>/build/outputs/unit_test_code_coverage -name '*.exec' 2>/dev/null | head -1)
[ -n "$EXEC" ] || EXEC=$(ls <module>/build/jacoco/*.exec 2>/dev/null | head -1)
[ -n "$EXEC" ] || { echo "no .exec file found under <module>/build/outputs/unit_test_code_coverage or <module>/build/jacoco"; exit 1; }
mkdir -p <module>/build/reports/coverage/test/debug
java -jar jacoco-*/lib/jacococli.jar report "$EXEC" \
  --classfiles <module>/build/tmp/kotlin-classes/debug \
  --sourcefiles <module>/src/main/java \
  --xml <module>/build/reports/coverage/test/debug/report.xml
```
Mirrors the reference `.github/workflows/main.yml`'s "Convert unit tests coverage results" step (adapted: that
workflow runs the full `test` lifecycle task across both build variants and converts
`build/jacoco/testReleaseUnitTest.exec`; this skill only runs `testDebugUnitTest`, and with the scaffolds' AGP
configuration the raw file lands at
`<module>/build/outputs/unit_test_code_coverage/debugUnitTest/testDebugUnitTest.exec` — so glob
`build/outputs/unit_test_code_coverage/**/*.exec` first and only then `build/jacoco/*.exec`, for whichever name
actually lands there. The converted XML is written to the same `test/debug/report.xml` path the AGP task would have
produced, so the scaffolds' `sonar {}` block finds it either way.) Locate `jacoco-*/lib/jacococli.jar` by globbing the repo root —
don't hard-code the version directory (`jacoco-0.8.13` in the reference repo; a consuming repo may vendor a
different release).

If the underlying test run itself fails (compile error or test failure), report that failure and stop — don't
convert or parse a stale `.exec`/XML from an earlier run.

## Step 3 — Instrumented coverage: report-only, on request

Never run `connectedAndroidTest`-based coverage as part of this skill unless the prompt explicitly asks for it
*and* `adb devices` shows an attached device/emulator (same gate as `iru-android-test`'s Step 4) — instrumented
coverage is slow and this skill's default scope is unit-test coverage. If
`<module>/build/reports/coverage/androidTest/debug/connected/report.xml` already exists on disk from an earlier
run, read and report its totals **for information only**, clearly labeled as instrumented coverage, without
re-running anything to produce or refresh it.

## Step 4 — Parse the JaCoCo-format XML

Whichever path in Step 2 ran, the resulting XML is in JaCoCo's report schema (a `<!DOCTYPE report ... "report.dtd">`
declaration is present but never needs to resolve — `xml.etree.ElementTree` parses the file fine without fetching
it). Structure: `<report>` → one `<package>` per Kotlin/Java package → one `<class>` and one `<sourcefile>` per
compilation unit, each carrying `<counter type="INSTRUCTION|BRANCH|LINE|COMPLEXITY|METHOD|CLASS" missed="N"
covered="N"/>` at class/sourcefile/package/report level, plus per-line `<line nr="N" mi="missedInstr"
ci="coveredInstr" mb="missedBranches" cb="coveredBranches"/>` inside each `<sourcefile>` (`ci="0"` means that line
was never executed — the source of "uncovered lines").

```python
import xml.etree.ElementTree as ET

path = "<module>/build/reports/coverage/test/debug/report.xml"   # or kover's reportDebug.xml, etc.
scope = None  # e.g. "Foo" or None for the whole report

root = ET.parse(path).getroot()

def counter(elem, ctype):
    for c in elem.findall("counter"):
        if c.get("type") == ctype:
            return int(c.get("missed")), int(c.get("covered"))
    return 0, 0

def pct(missed, covered):
    total = missed + covered
    return 0.0 if total == 0 else 100.0 * covered / total

lm, lc = counter(root, "LINE")
bm, bc = counter(root, "BRANCH")
print(f"REPORT line={pct(lm,lc):.2f}% ({lc}/{lm+lc}) branch={pct(bm,bc):.2f}% ({bc}/{bm+bc})")

for pkg in root.findall("package"):
    for cls in pkg.findall("class"):
        cname = cls.get("name").replace("/", ".")
        if scope and scope not in cname:
            continue
        lm, lc = counter(cls, "LINE")
        bm, bc = counter(cls, "BRANCH")
        print(f"CLASS {cname} line={pct(lm,lc):.2f}% ({lc}/{lm+lc}) branch={pct(bm,bc):.2f}% ({bc}/{bm+bc})")
    for sf in pkg.findall("sourcefile"):
        sname = pkg.get("name") + "/" + sf.get("name")
        if scope and scope.split(".")[-1].split("/")[-1].replace(".kt", "") not in sname:
            continue
        uncovered = [line.get("nr") for line in sf.findall("line") if line.get("ci") == "0"]
        if uncovered:
            print(f"UNCOVERED {sname}: {','.join(uncovered)}")
```

Verified against a hand-written sample report at `$TMPDIR/iru-verify/android/gates/jacoco/report.xml` (one
package, one class `Foo` with a fully-covered `bar()` method and an uncovered `baz()` method): the unscoped run
printed `REPORT line=40.00% (2/5) branch=50.00% (2/4)`, `CLASS com.example.lib.Foo line=40.00% ...`, and
`UNCOVERED com/example/lib/Foo.kt: 11,20,21,22`; scoping to `Foo` produced the identical output (single-class
fixture) — confirming both the counter math and the scope-filtering logic. For several comma-separated scope
names, run the class/sourcefile loops once per name (or extend the `scope not in cname` check to a list) rather
than composing a combined regex.

If a named scope class doesn't appear in the report at all, it means no code in it executed during the run that
produced this XML (either dead code, or the coverage run didn't exercise it) — report 0%, not an error, the same
convention `iru-java-coverage` uses for JaCoCo.

## Step 5 — Report

State, per target class (or the whole module if unscoped), the line coverage percentage and branch coverage,
computed from the actual XML counters — never estimate. If the user's bar is "at least N%": say clearly whether
each class/the whole module meets it. For anything under the bar, give the uncovered line numbers from Step 4 so
the user (or `iru-android-generate-all-tests`) knows exactly where to add tests, without opening an HTML report.

If coverage wasn't wired (Step 1's "coverage not wired" case), report that clearly instead of a percentage,
naming the missing plugin/setting/jar. If Step 2 fell back from the AGP task to the vendored CLI because no XML
was found, say so in the report (it's a wiring quirk worth surfacing, not just a silent implementation detail).
If instrumented coverage was requested but skipped (no device, or the report doesn't exist on disk yet), say so
explicitly rather than only reporting unit-test coverage as if it answered the whole question.

Do not add tests, modify source/test/build code, or re-run anything to try to raise coverage — that's a follow-up
the user (or `iru-android-code-one-task-group`, `iru-android-generate-all-tests`) drives explicitly.

## Known quirks / verification notes

- Gradle/AGP need **JDK 17+**; set `JAVA_HOME` explicitly rather than trusting the machine's default `java`.
- `ANDROID_HOME`/`local.properties` missing fails the build at configuration time before any coverage task runs.
- Configuration cache can be incompatible with some third-party tasks (Kover, the vendored-CLI `java -jar` step
  running outside Gradle's own task graph is unaffected); retry with `--no-configuration-cache` if a
  configuration-cache-specific error appears.
- Whether AGP's `createDebugUnitTestCoverageReport` actually emits importable XML (versus HTML-only) for this
  stack's AGP version, and its exact output file name, is **unverified locally by this skill's author** — it is
  verified only by exercising the generated `iru-setup-android-library` scaffold; this skill globs defensively and falls
  back to the vendored JaCoCo CLI conversion (known-good, taken directly from the reference repository's own CI
  step) so a wrong assumption about the AGP task's output degrades gracefully instead of silently under-reporting.
- The vendored-CLI `.exec` file's location and name are not guaranteed — with the scaffolds' AGP
  `enableUnitTestCoverage` configuration it lands at
  `build/outputs/unit_test_code_coverage/debugUnitTest/testDebugUnitTest.exec`, while the reference repository's
  older CI globbed `build/jacoco/` (and its step name, `testReleaseUnitTest.exec`, differs from what this skill's
  `testDebugUnitTest`-only run produces) — so always glob `build/outputs/unit_test_code_coverage/**/*.exec` first
  and `build/jacoco/*.exec` second, never hard-code either.
- This skill's JaCoCo-XML parsing (Step 4) was verified against a hand-written fixture in
  `$TMPDIR/iru-verify/android/gates/jacoco/report.xml` only; the live Gradle/JaCoCo-CLI runs that would produce a
  real report from a generated `iru-setup-android-library` scaffold are **unverified locally by this skill's author;
  exercised by the scaffold and workflows skills' own verification passes**.
