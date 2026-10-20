---
name: iru-kmp-coverage
description: >-
  Generate a Kotlin Multiplatform (Android + iOS) project's unit-test line/branch coverage with the Kover Gradle
  plugin (`org.jetbrains.kotlinx.kover`) — the root-aggregated `./gradlew koverXmlReport` (`build/reports/kover/report.xml`,
  covering every module listed in the root `dependencies { kover(project(":x")) }`) when the root aggregates, else
  each module's own report (`:<kmp-module>:koverXmlReport` → `<module>/build/reports/kover/report.xml`, or the
  Android-only `koverXmlReportAndroid` → `reportAndroid.xml`; an Android app module's `koverXmlReportDebug` →
  `reportDebug.xml`) — then parses the JaCoCo-format XML into exact totals, per-module and per-class line/branch
  percentages (each class mapped back to its module and source set — `commonMain`, `androidMain`, the app's `main`),
  and uncovered line numbers for classes under the bar. Coverage comes from the JVM test runs only (Android host
  tests, `jvmTest`, the Android app's `testDebugUnitTest`, which Kover runs itself): Kotlin/Native has no coverage
  tool, so `iosMain`/`appleMain`/`nativeMain` code is listed as "not measurable" and never fails the gate, and
  `commonMain` code is measured through the JVM targets' runs of `commonTest`. Invoke as `/iru-kmp-coverage [scope]`,
  where `[scope]` is one or more comma-separated class simple names, source paths, or a module (`:shared`), or with
  no argument for the whole project; optional `key: value` lines: `tests: <pattern>` to narrow the test run (the
  same `--tests` syntax as `iru-kmp-test`), `bar: <percent>` (default 80), `module:`, and `ios-app: yes` to also
  collect informational Xcode coverage of the SwiftUI host app's Swift code (`xcodebuild test -enableCodeCoverage
  YES` + `xccov`, behind the shared `.integration-test.lock`). Detects whether Kover is applied before running
  anything and reports "coverage not wired" (naming what's missing) instead of a false 0%/100% or a clean pass.
  Report-only: never adds tests or changes build files. Equivalent to `iru-android-coverage`/`iru-java-coverage`'s
  Kover path for KMP apps. Use whenever the user (or `iru-kmp-code-one-task-group` via `iru-gate-runner`) wants to
  check, or verify a bar (e.g. "at least 80% line coverage") for, KMP classes or modules.
model: haiku
allowed-tools: Read Write Bash(./gradlew *) Bash(python3 *) Bash(xcodebuild *) Bash(xcrun *) Bash(uname *) Bash(git rev-parse *) Bash(find *) Bash(grep *) Bash(ls *) Bash(cat *) Bash(date *) Bash(rm -rf *iru-kmp-coverage-*) Bash(mkdir .integration-test.lock*) Bash(rmdir .integration-test.lock*) Bash(rm -f .integration-test.lock/owner) Bash(/usr/libexec/java_home *)
---

# KMP Coverage

Run the Kover coverage a KMP project has wired and report exact, measured line/branch coverage for the scope the
user cares about — per class, per module, and for the whole project. This skill only measures and reports; it never
adds tests or modifies source, test, or build files.

## Step 0 — Resolve inputs

- `[scope]` — comma-separated class simple names (`Greeter`), source paths (`shared/src/commonMain/…/Greeter.kt`),
  or a module (`:shared`, `androidApp`). No scope → the whole project.
- `key: value` lines (explicit keys win): `tests: <pattern>` (a Gradle `--tests` pattern to narrow the test run —
  coverage then only reflects those tests; see Step 3), `bar: <percent>` (default **80**, line coverage — the
  catalog-wide gate), `module: <gradle path>`, `ios-app: yes|no` (default `no`, Step 5), `lock: held` (the caller
  already holds `.integration-test.lock`).

Prerequisites are `iru-kmp-test`'s Step 1 (JDK 17/21 on `JAVA_HOME`, Android SDK via `ANDROID_HOME` or
`local.properties`, `./gradlew` present) — check them first; a missing one fails at configuration time and looks
like a coverage problem.

## Step 1 — Detect whether Kover is wired, and where

```bash
grep -nE 'org\.jetbrains\.kotlinx\.kover|libs\.plugins\.kover|kotlinx-kover|id\("kover"\)' build.gradle.kts */build.gradle.kts gradle/libs.versions.toml 2>/dev/null
grep -nE 'kover\(project\(' build.gradle.kts 2>/dev/null
```

- **Root aggregation** — the root build applies Kover and declares `dependencies { kover(project(":shared"));
  kover(project(":androidApp")) }` (this catalog's `iru-setup-kmp-app` layout). Use the root `koverXmlReport`: one
  report for every aggregated module. Note which modules are *not* listed — their code isn't in the total.
- **Per-module only** — Kover applied in module build files but not aggregated at the root. Run each module's report
  task (Step 2) and report them separately; never sum percentages across reports.
- **Not wired** — no Kover anywhere. Look for a JaCoCo alternative before giving up: the Android app module's
  `enableUnitTestCoverage = true` (AGP's `createDebugUnitTestCoverageReport`) — if present, measure that module the
  way `iru-android-coverage`'s Step 2 does and say the KMP module itself is unmeasured. Otherwise **stop and report
  "coverage not wired"**: no `org.jetbrains.kotlinx.kover` plugin in any build file (and no AGP unit-test coverage) —
  never a percentage, never "0%", never a pass.

Confirm task names before running (they depend on the targets and the Kover version):

```bash
./gradlew tasks --all | grep -E '^([a-zA-Z]+:)?koverXmlReport'
```

## Step 2 — Run the report task

| Setup | Command | XML |
|---|---|---|
| Root aggregation | `./gradlew koverXmlReport` | `build/reports/kover/report.xml` |
| KMP module, all JVM targets | `./gradlew :shared:koverXmlReport` | `shared/build/reports/kover/report.xml` |
| KMP module, Android target only | `./gradlew :shared:koverXmlReportAndroid` | `shared/build/reports/kover/reportAndroid.xml` |
| Android app module, debug variant | `./gradlew :androidApp:koverXmlReportDebug` | `androidApp/build/reports/kover/reportDebug.xml` |

Kover's report tasks depend on the test tasks they measure (verified: the root `koverXmlReport` ran
`:shared:testAndroidHostTest` and `:androidApp:testDebugUnitTest` itself), so no separate test run is needed. They
never run Kotlin/Native tests — iOS code isn't instrumentable — so this skill needs no simulator and no lock unless
Step 5 runs.

If the underlying test run fails (compile error or failing test), report that failure and stop — don't parse a
report left over from an earlier run. Retry once with `--no-configuration-cache` on a configuration-cache error
unrelated to coverage.

## Step 3 — Narrowing the test run (`tests:`)

```bash
./gradlew :shared:testAndroidHostTest --tests '<pattern>' :shared:koverXmlReport
```

The `--tests` filter binds to the test task named right before it (`iru-kmp-test`'s Step 3), so name the test task
explicitly with the filter, then the report task. Verified: filtering to `*.AndroidPlatformTest` produced a report in
which `Greeter` (only exercised by `GreeterTest`) dropped to 0% — coverage only reflects the tests that ran. A
caller gating on a class's coverage must include every test class that exercises it, or omit `tests:` and run the
whole suite; when in doubt, prefer the broader run (the same caution as `iru-java-coverage`'s Step 1).

## Step 4 — Parse the Kover XML

Kover writes JaCoCo's XML schema (`<report>` → `<package>` → `<class name="…" sourcefilename="…">` with `<counter
type="LINE|BRANCH|INSTRUCTION|METHOD" missed covered/>`, plus `<sourcefile>` → `<line nr mi ci mb cb/>`). The parser
below maps every class back to `<module>:<sourceSet>` by locating its source file, prints totals, per-class and
per-module figures with uncovered lines for classes under the bar, and lists the Kotlin/Native source sets as not
measurable. Run it from the repository root:

```bash
python3 - <report.xml> <bar> [scope ...] <<'PY'
import glob, sys, xml.etree.ElementTree as ET
from collections import defaultdict

# argv: <report.xml> <threshold %> [scope ...]   (scope = class simple name or path fragment)
report, bar, scopes = sys.argv[1], float(sys.argv[2]), sys.argv[3:]

def counters(elem):
    return {c.get("type"): (int(c.get("missed")), int(c.get("covered"))) for c in elem.findall("counter")}

def pct(c, kind):
    m, v = c.get(kind, (0, 0))
    return None if m + v == 0 else 100.0 * v / (m + v)

def fmt(c, kind):
    p = pct(c, kind)
    m, v = c.get(kind, (0, 0))
    return "n/a" if p is None else f"{p:.1f}% ({v}/{m + v})"

def locate(pkg, filename):
    # map a report entry back to <module>/src/<sourceSet>/... so the summary can group by module and source set
    hits = glob.glob(f"**/src/*/kotlin/{pkg}/{filename}", recursive=True) + \
           glob.glob(f"**/src/*/java/{pkg}/{filename}", recursive=True)
    hits = [h for h in hits if "/build/" not in h]
    if not hits:
        return "?", "?"
    parts = hits[0].split("/")
    i = parts.index("src")
    return "/".join(parts[:i]) or ".", parts[i + 1]

root = ET.parse(report).getroot()
tot = counters(root)
print(f"TOTAL line={fmt(tot, 'LINE')} branch={fmt(tot, 'BRANCH')} bar={bar:.0f}% "
      f"{'MEETS' if (pct(tot, 'LINE') or 0) >= bar else 'BELOW'}")
per_module = defaultdict(lambda: [0, 0, 0, 0])
for pkg in root.findall("package"):
    pname = pkg.get("name")
    uncovered = {sf.get("name"): [l.get("nr") for l in sf.findall("line") if l.get("ci") == "0"]
                 for sf in pkg.findall("sourcefile")}
    for cls in pkg.findall("class"):
        fqcn = cls.get("name").replace("/", ".")
        src = cls.get("sourcefilename", "")
        module, source_set = locate(pname, src)
        c = counters(cls)
        lm, lc = c.get("LINE", (0, 0)); bm, bc = c.get("BRANCH", (0, 0))
        acc = per_module[module]; acc[0] += lm; acc[1] += lc; acc[2] += bm; acc[3] += bc
        if scopes and not any(s in fqcn or s in f"{module}/src/{source_set}/{pname}/{src}" for s in scopes):
            continue
        p = pct(c, "LINE")
        flag = "" if p is None or p >= bar else "  BELOW"
        print(f"CLASS {fqcn} [{module}:{source_set}] line={fmt(c, 'LINE')} branch={fmt(c, 'BRANCH')}{flag}")
        if flag and uncovered.get(src):
            print(f"  UNCOVERED {pname}/{src}: {','.join(uncovered[src])}")
for module, (lm, lc, bm, bc) in sorted(per_module.items()):
    c = {"LINE": (lm, lc), "BRANCH": (bm, bc)}
    print(f"MODULE {module} line={fmt(c, 'LINE')} branch={fmt(c, 'BRANCH')}")
# Kotlin/Native source sets never reach a JVM coverage report - list them as not measurable
native = sorted({f.split("/src/")[0] + ":" + f.split("/src/")[1].split("/")[0]
                 for f in glob.glob("**/src/ios*Main/kotlin/**/*.kt", recursive=True)
                 + glob.glob("**/src/apple*Main/kotlin/**/*.kt", recursive=True)
                 + glob.glob("**/src/native*Main/kotlin/**/*.kt", recursive=True) if "/build/" not in f})
for n in native:
    print(f"NOT MEASURABLE {n} (Kotlin/Native - no coverage tool)")
PY
```

Notes on reading it:

- A `[scope]` class that doesn't appear at all was never loaded by the JVM runs (Kover, unlike JaCoCo, usually lists
  unloaded classes at 0%, but a file containing only `expect` declarations or only iOS code has no JVM class) — check
  whether its source file lives in an iOS source set (→ not measurable) before reporting 0%.
- `expect`/`actual`: the `expect` declaration has no bytecode; its Android `actual` (`Platform_androidKt` for a
  top-level `actual fun` in `Platform.android.kt`) is measured under `androidMain`, its iOS `actual` is not
  measurable. Kotlin file-level classes appear as `<File>Kt`; companion objects, lambdas and coroutine state
  machines as `$`-suffixed classes — call compiler-generated gaps out as noise, as `iru-java-coverage` does.
- The `BELOW` flag and the gate use **line** coverage against `bar`; branch coverage is reported for information.
  Kotlin/Native code is excluded from the denominator by construction and never counts against the bar — report it
  separately so nobody reads the total as "the whole app".

## Step 5 — Optional: iosApp Swift coverage (`ios-app: yes`, information only)

The SwiftUI host app's own Swift code (`iosApp/iosApp/`) can be measured by Xcode, never by Kover. Only on request,
only on macOS with Xcode, and only behind `.integration-test.lock` (acquire/release exactly as `iru-kmp-test`'s
Step 4 — it boots a simulator):

```bash
rm -rf "$TMPDIR/iru-kmp-coverage-ios.xcresult"
xcodebuild test -project iosApp/iosApp.xcodeproj -scheme iosApp \
  -destination 'platform=iOS Simulator,name=<device>' -enableCodeCoverage YES \
  -resultBundlePath "$TMPDIR/iru-kmp-coverage-ios.xcresult"
xcrun xccov view --report --json "$TMPDIR/iru-kmp-coverage-ios.xcresult"
```

Read it the way `iru-swift-coverage`'s "App: `xccov`" section does (per-target/per-file `lineCoverage`; no branch
coverage exists for Swift), report only the `iosApp` target's files, label the figure **informational — not part of
the gate**, and ignore the embedded `Shared` framework's entry (Kotlin/Native code compiled into a framework carries
no Swift coverage mapping). When the project isn't generated or the simulator is unavailable, say this part was
skipped and why.

## Step 6 — Report

- The engine and setup used (Kover version if visible, root aggregation or per-module), the report path(s), and the
  test pattern if `tests:` narrowed the run.
- The total line/branch %, per-module line/branch %, and per in-scope class line/branch % — all from the XML
  counters, never estimated — and whether each meets `bar`. For each class under the bar, its uncovered line numbers
  so the caller (or `iru-kmp-generate-all-tests`) knows where to add tests.
- **Not measurable**: every Kotlin/Native source set with code (e.g. `shared:iosMain`), stated as excluded from the
  gate, never as 0% and never as failing.
- **Coverage not wired**, when Step 1 found no Kover — naming what's missing — instead of any percentage.
- Step 5's informational iosApp figure, or that it was skipped.

Do not add tests, touch build files, or re-run anything to raise the number — that's a follow-up for the user,
`iru-kmp-code-one-task-group`, or `iru-kmp-generate-all-tests`.

## Known quirks / verification notes

Verified in `$TMPDIR/iru-verify/kmp/iru-kmp-coverage/` (October 2026, Gradle 9.8.1, JDK 21, Kotlin 2.4.21, AGP 9.4.1
with `com.android.kotlin.multiplatform.library`, Kover **0.9.11** — the current release; look it up at
`https://plugins.gradle.org/m2/org/jetbrains/kotlinx/kover/org.jetbrains.kotlinx.kover.gradle.plugin/maven-metadata.xml`):

- Kover applied to `shared` + `androidApp` and aggregated at the root: `./gradlew koverXmlReport` ran
  `:shared:testAndroidHostTest` and `:androidApp:testDebugUnitTest` and wrote `build/reports/kover/report.xml`
  (`<report name="Kover Gradle Plugin XML report for :">`) with both modules' packages; `:shared:koverXmlReport`,
  `:shared:koverXmlReportAndroid` and `:androidApp:koverXmlReportDebug` wrote `shared/build/reports/kover/report.xml`,
  `…/reportAndroid.xml` and `androidApp/build/reports/kover/reportDebug.xml`. No iOS task ran.
- The Step 4 parser on the aggregated report printed `TOTAL line=62.5% (5/8) branch=50.0% (2/4) bar=80% BELOW`,
  `CLASS com.example.shared.Greeter [shared:commonMain] line=100.0% (3/3) branch=50.0% (1/2)`,
  `CLASS com.example.shared.Platform_androidKt [shared:androidMain] …`, `CLASS com.example.app.MainActivity
  [androidApp:main] line=0.0% (0/3) … BELOW` with `UNCOVERED com/example/app/MainActivity.kt: 7,9,10`, per-module
  lines, and `NOT MEASURABLE shared:iosMain`; scoping to `Greeter` printed only that class.
- `./gradlew :shared:testAndroidHostTest --tests '*.AndroidPlatformTest' :shared:koverXmlReport` honoured the filter
  (Greeter at 0%).
- **Unverified locally**: Step 5's `xcodebuild -enableCodeCoverage`/`xccov` path for an `iosApp` (no XcodeGen here
  to generate one — the commands and JSON shape are `iru-swift-coverage`'s, verified there), the AGP
  `createDebugUnitTestCoverageReport` fallback (see `iru-android-coverage`), and Kover with an `androidTarget()` +
  `com.android.library` module (its Android report task is then variant-named, e.g. `koverXmlReportDebug` — confirm
  with the Step 1 task listing).
