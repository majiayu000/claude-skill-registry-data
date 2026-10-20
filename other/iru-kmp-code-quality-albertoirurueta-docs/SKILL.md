---
name: iru-kmp-code-quality
description: >-
  Run a Kotlin Multiplatform (Android + iOS) project's wired static-analysis tools across every KMP source set — detekt
  (1.x `io.gitlab.arturbosch.detekt`, whose KMP tasks are per compilation: `detektMetadataCommonMain`/
  `detektMetadataIosMain`/… plus the type-resolution `detektAndroidMain`, or a plain `detekt` task only when its
  `source` is configured to the KMP source directories; 2.x `dev.detekt`, whose tasks are per source set:
  `detektCommonMainSourceSet`/`detektAndroidMainSourceSet`/`detektIosMainSourceSet`/…), ktlint
  (`org.jlleitschuh.gradle.ktlint` `ktlintCheck`, one check per source set plus `ktlintKotlinScriptCheck`, or Spotless
  `kotlin { ktlint() }`), Android Lint (the Android app module's `lintDebug`, and the KMP module's `lint` when the
  `com.android.lint` plugin is applied to it — the AGP KMP library plugin registers no lint task otherwise), and
  SwiftLint on the iOS host app (`swiftlint lint --reporter json iosApp`) when `iosApp/.swiftlint.yml` exists and the
  binary is installed — detecting the detekt generation and every task name at runtime from `./gradlew <module>:tasks
  --all`. Parses the detekt/ktlint Checkstyle XML, the ktlint plain reports (ANSI-stripped), the Android Lint XML and
  the SwiftLint JSON into one per-tool, per-rule-id summary (file, line, rule id, severity, message). Invoke as
  `/iru-kmp-code-quality` for the whole project, or `/iru-kmp-code-quality <scope>` where `<scope>` is a file/class
  name, a path, a module, or a source set — the tools always analyze whole source sets, so a scope narrows the tasks
  run where possible and filters the report. Report-only: verifies each tool is wired before trusting a "zero issues"
  result (a plain detekt 1.x `detekt` task on a KMP module with no `source` configured analyzes nothing and writes no
  report — that is "not wired for KMP sources", never a clean pass), reports an unwired tool as "not wired", and never
  changes detekt/ktlint/Lint/SwiftLint configuration or installs a tool. When the prompt supplies a baseline (per-tool,
  per-rule-id counts or an itemized list from an earlier run), reports only the new-vs-baseline diff, matched on tool
  + rule id + file. Equivalent to `iru-android-code-quality`/`iru-kotlin-code-quality`/`iru-swift-code-quality` for
  KMP apps. Use whenever the user (or `iru-kmp-code-one-task-group` via `iru-gate-runner`) wants a lint/static-analysis
  pass over a KMP codebase instead of eyeballing `./gradlew check` output.
model: haiku
allowed-tools: Read Bash(./gradlew *) Bash(python3 *) Bash(swiftlint *) Bash(command -v *) Bash(find *) Bash(grep *) Bash(ls *) Bash(cat *) Bash(/usr/libexec/java_home *)
---

# KMP Code Quality

Run whichever static-analysis tools a KMP project actually has wired — over the shared module's every source set,
the Android app module, and optionally the Swift host app — and report every issue they find. This skill only runs
analysis and reports results: it never fixes issues, never runs `ktlintFormat`/`detektBaseline`/`lintFix`/
`swiftlint --fix`, and never adds or changes configuration (a missing tool is reported, not installed).

## Step 0 — Resolve inputs

`<scope>` (optional): a file path, a class/file simple name, a module (`:shared`, `androidApp`), or a source-set name
(`commonMain`, `iosMain`, `androidMain`). It narrows which tasks run when it maps to a module or source set (Step 2)
and filters the parsed report (Step 3) — none of these tools take a per-file selector. No scope → everything. Explicit
`key: value` lines win over inference: `module:`, `tools: <comma list>` (subset of `detekt,ktlint,lint,swiftlint`),
and a `baseline:` block — a prior per-tool/per-rule-id count or itemized list from an earlier run of this skill (Step
4); treat everything after `baseline:` as that prior result.

Prerequisites are `iru-kmp-test`'s Step 1 (JDK 17/21 on `JAVA_HOME`, Android SDK, `./gradlew`). Detect the modules
the same way (KMP modules: Kotlin Multiplatform plugin applied — `shared/`, or `composeApp/` in the wizard layout;
Android app modules: `com.android.application`; the iOS host app: `iosApp/`).

## Step 1 — Verify which tools are wired

Check every module's build file **and** the root build, `build-logic/`/`buildSrc/` convention plugins and
`gradle/libs.versions.toml` aliases, then list the tasks once per module (configuration is the slow part — reuse
the listing):

```bash
grep -nE 'io\.gitlab\.arturbosch\.detekt|dev\.detekt|libs\.plugins\.detekt|jlleitschuh\.gradle\.ktlint|libs\.plugins\.ktlint|com\.diffplug\.spotless|com\.android\.lint|lint \{' build.gradle.kts */build.gradle.kts gradle/libs.versions.toml 2>/dev/null
./gradlew :<module>:tasks --all > "$TMPDIR/iru-kmp-code-quality-tasks-<module>.txt"
grep -E '^(detekt|ktlint|lint|spotless)[A-Za-z0-9]*( |$)' "$TMPDIR/iru-kmp-code-quality-tasks-<module>.txt"
```

- **detekt** — identify the generation from the plugin id/version (`io.gitlab.arturbosch.detekt` = 1.x, `dev.detekt`
  = 2.x) and pick the tasks that analyze the KMP **main** source sets (add the test ones only when the project's CI
  runs them):
  - **1.x**: per-compilation tasks `detektMetadataCommonMain`, `detektMetadataIosMain` (and any other
    `detektMetadata<SharedSet>Main` with sources — `AppleMain`, `NativeMain`), `detektIosArm64Main`/
    `detektIosSimulatorArm64Main` only if those target-specific sets hold code, and `detektAndroidMain` (type
    resolution — "EXPERIMENTAL" in its task description; it compiles first). The plain `detekt` task covers KMP code
    **only** when the build sets `detekt { source.setFrom("src/commonMain/kotlin", "src/androidMain/kotlin",
    "src/iosMain/kotlin", …) }` — verified: without it, `:shared:detekt` "runs" on the JVM default `src/main/…`
    directories, finds nothing and writes no report. If the project relies on plain `detekt` without `source`, report
    **"detekt: wired but not covering KMP source sets (no `source` configured)"**, then run the per-compilation tasks
    instead so findings still surface — never report the empty plain run as clean. **When `source.setFrom(...)`
    is configured** (as `iru-setup-kmp-app`'s scaffold does, covering every KMP source directory), prefer the plain
    per-module `detekt` task — it writes `<module>/build/reports/detekt/detekt.{xml,sarif}` — and treat the
    per-compilation task names above as optional: with the AGP KMP library plugin some detekt 1.23.x builds expose
    no `detektMetadataCommonMain` at all (target-level `detektIosArm64Main`/`detektIosSimulatorArm64Main`/
    `detektAndroidMain` instead), which is why the task list must come from Step 1's `tasks --all` output, never
    from this list.
  - **2.x**: per-source-set tasks `detektCommonMainSourceSet`, `detektAndroidMainSourceSet`,
    `detektIosMainSourceSet` (and `detekt<Set>SourceSet` for every other set with sources), plus the
    type-resolution `detektMainAndroid`; the plain `detekt` task is `NO-SOURCE` on a KMP module.
  - Note whether a custom config (`detekt.yml`, `config/detekt/detekt.yml`, whatever `config.setFrom(...)` names),
    `buildUponDefaultConfig`, and a baseline file are in use — they change what "zero issues" means.
- **ktlint** — `org.jlleitschuh.gradle.ktlint`: `ktlintCheck` aggregates one `ktlint<SourceSet>SourceSetCheck` per
  KMP source set (target-specific sets without files are `SKIPPED`) plus `ktlintKotlinScriptCheck` for the `.kts`
  build scripts. Spotless instead: `spotlessKotlinCheck` (only when a `kotlin { ktlint() }` block targets the KMP
  source directories). Rules come from `.editorconfig` — note it if present.
- **Android Lint** — Android app module: `lintDebug` (always available with `com.android.application`). KMP module:
  with `androidTarget()` + `com.android.library`, `lintDebug`; with `com.android.kotlin.multiplatform.library`, a
  `lint` task exists **only** when `com.android.lint` is also applied (verified: without it only
  `lintAnalyzeAndroidHostTest` is registered and no report is produced) — then report shared-module Lint as "not
  wired (apply `com.android.lint` to lint the Android target)". Check `lint { abortOnError = false }`: without it a
  `Fatal` issue aborts before the XML is written (see `iru-android-code-quality`).
- **SwiftLint** — wired only when `iosApp/.swiftlint.yml` (or `.swiftlint.yaml`, or a root one covering `iosApp/`)
  exists **and** `command -v swiftlint` succeeds. Config present but binary missing → report "SwiftLint not
  installed" and offer, via `AskUserQuestion`, `brew install swiftlint` (only if `brew` exists) or skipping it —
  never install without that choice (the same courtesy as `iru-swift-code-quality`'s Step 1). No config → "not
  wired". Any OS other than macOS → not applicable.

A tool that isn't wired is **skipped and named** in the report (e.g. `"ktlint: not wired (no ktlint plugin or
Spotless kotlin block)"`) — never silently omitted and never counted as zero issues. If nothing at all is wired, say
"No Kotlin/Swift static analysis configured" and stop.

## Step 2 — Run each wired tool

One Gradle invocation for every wired task, with `--continue` so a failing check doesn't stop the others:

```bash
./gradlew :shared:detektMetadataCommonMain :shared:detektMetadataIosMain :shared:detektAndroidMain \
  :shared:ktlintCheck :shared:lint :androidApp:lintDebug --continue          # detekt 1.x; :shared:lint only with com.android.lint
./gradlew :shared:detektCommonMainSourceSet :shared:detektAndroidMainSourceSet :shared:detektIosMainSourceSet \
  :shared:ktlintCheck :androidApp:lintDebug --continue                       # detekt 2.x example
```

- Scope → tasks: a source-set scope runs just that set's detekt/ktlint tasks (e.g. `iosMain` →
  `detektMetadataIosMain`/`detektIosMainSourceSet` + `ktlintIosMainSourceSetCheck`); a module scope runs only that
  module's tasks; a file scope runs its source set's tasks and filters the report.
- **Exit codes are information, not breakage**: detekt fails with `Analysis failed with N weighted issues.` (when
  `ignoreFailures` isn't set) but still writes its reports; `ktlint*Check` fails on any violation by design; Lint
  fails only on `abortOnError`. Always go on and parse. A real compile error, a dependency-resolution failure, or a
  Kotlin version detekt can't parse is different — report it as a tool failure for that tool and don't read a stale
  report (check the report's mtime against the run when in doubt). Retry once with `--no-configuration-cache` on a
  configuration-cache error unrelated to the findings.
- **SwiftLint**, when wired (no Gradle involved, report-only, from the repository root):

  ```bash
  swiftlint lint --reporter json --config iosApp/.swiftlint.yml iosApp > "$TMPDIR/iru-kmp-code-quality-swiftlint.json"
  ```

## Step 3 — Locate and parse the reports

Locate reports by listing rather than assuming one name — they depend on the detekt generation and task:

```bash
find <module>/build/reports/detekt -name '*.xml'        # 1.x: detekt.xml (plain), commonMain.xml, iosMain.xml, main.xml (detektAndroidMain)
                                                        # 2.x: commonMainSourceSet.xml, androidMainSourceSet.xml, iosMainSourceSet.xml
find <module>/build/reports/ktlint -type f              # <task>/<task>.txt (plain, ANSI-colored); <task>.xml with a CHECKSTYLE reporter
ls <module>/build/reports/lint-results*.xml             # lintDebug: lint-results-debug.xml; KMP `lint`: lint-results.xml + lint-results-androidMain.xml
```

Only read reports the tasks of this run produced. Note `main.xml` is detekt 1.x's name for `detektAndroidMain`'s
report (not a plain-JVM `main` source set). For the KMP module's Lint, read `lint-results-androidMain.xml` (the
`lint` aggregate's `lint-results.xml` repeats the same issues plus the JVM-only lint pass).

Parse everything with one stdlib script — `tool=path` per report, optional `--scope <substring>` first; identical
findings (same tool, file, line, column, rule) are de-duplicated because detekt 1.x and 2.x paths, or several report
formats, can describe the same issue:

```bash
python3 - [--scope <substring>] detekt=<xml> ... ktlint=<txt-or-xml> ... lint=<xml> ... swiftlint=<json> <<'PY'
import json, re, sys, xml.etree.ElementTree as ET
from collections import Counter

# argv: [--scope <substring>] <tool>=<report> ...   tool: detekt | ktlint | lint | swiftlint
args, scope = sys.argv[1:], None
if args[:1] == ["--scope"]:
    scope, args = args[1], args[2:]
issues = []  # (tool, file, line, col, rule, severity, message)
for spec in args:
    tool, path = spec.split("=", 1)
    if tool == "detekt" and path.endswith(".xml"):          # Checkstyle format (detekt 1.x and 2.x)
        for f in ET.parse(path).getroot().findall("file"):
            for e in f.findall("error"):
                issues.append((tool, f.get("name"), e.get("line"), e.get("column"), e.get("source", "").rsplit(".", 1)[-1],
                               e.get("severity"), e.get("message")))
    elif tool == "ktlint" and path.endswith(".xml"):         # ktlint CHECKSTYLE reporter
        for f in ET.parse(path).getroot().findall("file"):
            for e in f.findall("error"):
                issues.append((tool, f.get("name"), e.get("line"), e.get("column"), e.get("source"), e.get("severity"), e.get("message")))
    elif tool == "ktlint":                                   # plain reporter: <path>:<line>:<col>: <msg> (<rule>)
        for raw in open(path, encoding="utf-8"):
            line = re.sub(r"\x1b\[[0-9;]*m", "", raw).rstrip()
            m = re.match(r"^(.+?):(\d+):(\d+): (.*) \(([\w-]+:[\w-]+)\)$", line)
            if m:
                issues.append((tool, m.group(1), m.group(2), m.group(3), m.group(5), "error", m.group(4)))
    elif tool == "lint":                                     # Android Lint XML
        for i in ET.parse(path).getroot().findall("issue"):
            loc = i.find("location")
            issues.append((tool, loc.get("file") if loc is not None else "?",
                           loc.get("line") if loc is not None else None, loc.get("column") if loc is not None else None, i.get("id"), i.get("severity"), i.get("message")))
    elif tool == "swiftlint":                                # swiftlint lint --reporter json
        for v in json.load(open(path)):
            issues.append((tool, v.get("file"), str(v.get("line")), str(v.get("character")), v.get("rule_id"), v.get("severity"), v.get("reason")))
    else:
        sys.exit(f"unsupported report {spec}")
if scope:
    issues = [i for i in issues if scope in (i[1] or "")]
issues = sorted(set(issues), key=lambda i: (i[0], i[1] or "", int(i[2] or 0), int(i[3] or 0), i[4]))  # dedupe identical findings
print(f"TOTAL {len(issues)}")
for tool in sorted({i[0] for i in issues}):
    mine = [i for i in issues if i[0] == tool]
    print(f"{tool}: {len(mine)} by-rule={dict(Counter(i[4] for i in mine))} by-severity={dict(Counter(i[5] for i in mine))}")
    for t, f, line, col, rule, sev, msg in mine:
        print(f"  {f}:{line} [{sev}] {rule}: {msg}")
PY
```

Format notes, all verified on real reports (Step 5):

- **detekt** Checkstyle XML — `source="detekt.MagicNumber"` → rule `MagicNumber`. 1.x writes absolute paths and
  `warning` severity by default; 2.x writes repository-relative paths and `error`. Keep severities per tool.
- **ktlint** plain `.txt` — `<path>:<line>:<col>: <message> (<ruleset:rule-id>)` wrapped in ANSI color escapes,
  stripped before matching; a CHECKSTYLE-reporter `.xml`, when configured, parses like detekt's with the rule id kept
  whole (`standard:statement-wrapping`). Spotless has no report — parse its console as `iru-kotlin-code-quality`'s
  Step 3 describes.
- **Android Lint** XML — `<issue id severity message>` + first `<location file line column>`; severities `Fatal`/
  `Error`/`Warning`/`Information` — report the breakdown on Lint's own four-level scale.
- **SwiftLint** JSON — `rule_id`, `severity` (`Warning`/`Error`), `file`, `line`, `character`, `reason`; the shape is
  documented, not verified locally (see notes).

## Step 4 — Classify, diff against a baseline if given, and report

Bucket every issue by **tool, then rule id** — detekt rule name, ktlint `ruleset:rule-id`, Lint issue id, SwiftLint
`rule_id` — and never merge buckets across tools. Also group detekt/ktlint findings by **source set** (from the path:
`src/commonMain/` vs `src/iosMain/` …), since an issue only in `iosMain` matters to whoever owns the iOS `actual`s.

**Report**: an overall total first; then per tool: ran / skipped as "not wired" / "wired but not covering KMP source
sets" / "not installed — asked, user chose <choice>", which config/baseline/`.editorconfig` governed it, the issue
count, the severity breakdown, and one line per rule bucket with its count — plus the file:line list when the scope is
smaller than the whole project.

**Baseline diff** — when the prompt supplies one (the same contract `iru-android-code-quality`/`iru-kotlin-code-quality`
follow for `iru-*-code-one-task-group` callers): report only what's new — a rule whose count increased, a rule that
appears now and didn't before, or a new file:line entry when the baseline was itemized — matched on tool + rule id +
file, never on message text or shifting line numbers. Decreased/unchanged rules are not regressions and are omitted
from the diff (they still appear in the plain counts). A tool that wasn't run in the baseline (unwired then, or newly
wired) has all of its current issues treated as new — say so. A detekt generation change between baseline and now
(1.x `warning` → 2.x `error`, absolute → relative paths) is not a regression by itself — compare on rule id + file
name, and state the switch.

Do not fix anything or change any configuration — that's a follow-up the user, `iru-kmp-code-one-task`, or
`iru-kmp-code-one-task-group` drives.

## Step 5 — Known quirks / verification notes

Verified in `$TMPDIR/iru-verify/kmp/iru-kmp-code-quality/` and `…/iru-kmp-code-quality-detekt2/` (October 2026,
Gradle 9.8.1, JDK 21, Kotlin 2.4.21, AGP 9.4.1 with `com.android.kotlin.multiplatform.library`, `iosArm64` +
`iosSimulatorArm64`; detekt **1.23.8** and **2.0.0-alpha.6**, `org.jlleitschuh.gradle.ktlint` **14.2.0**):

- **detekt 1.23.8**: `:shared:tasks --all` listed `detekt`, `detektMetadataCommonMain`, `detektMetadataIosMain`,
  `detektMetadataAppleMain`, `detektMetadataNativeMain`, `detektMetadataMain`, `detektIosArm64Main`,
  `detektIosSimulatorArm64Main` (+ `…Test`), and EXPERIMENTAL `detektAndroidMain`/`detektAndroidHostTest`. With
  `detekt { source.setFrom("src/commonMain/kotlin", "src/androidMain/kotlin", "src/iosMain/kotlin") }`, `:shared:detekt`
  found the two `MagicNumber` issues in `commonMain` and wrote `build/reports/detekt/detekt.xml`; **without** `source`,
  the same task ran, found nothing and wrote no `detekt.xml`. `detektMetadataCommonMain` → `commonMain.xml`,
  `detektMetadataIosMain` → `iosMain.xml`, `detektAndroidMain` → `main.xml`; `detektIosArm64Main` was `NO-SOURCE`
  (the code lives in `iosMain`). Each failing task still wrote its report (`Analysis failed with 2 weighted issues.`).
- **detekt 2.0.0-alpha.6** (`dev.detekt`): per-source-set `detekt<Set>SourceSet` tasks plus `detektMainAndroid`/
  `detektHostTestAndroid`; plain `detekt` was `NO-SOURCE`; reports `commonMainSourceSet.xml`,
  `androidMainSourceSet.xml`, `iosMainSourceSet.xml` with relative paths and `error` severity. 2.x was still alpha
  in October 2026 — 1.23.8 is the current stable.
- **ktlint 14.2.0**: `ktlintCheck` ran `ktlintCommonMainSourceSetCheck`, `ktlintAndroidMainSourceSetCheck`,
  `ktlintIosMainSourceSetCheck`, the test-set checks and `ktlintKotlinScriptCheck` (target-specific sets without
  files `SKIPPED`); reports only `.txt` with ANSI escapes by default, e.g. `shared/build.gradle.kts:17:33: Missing
  newline after '{' (standard:statement-wrapping)`.
- **Android Lint**: `:androidApp:lintDebug` wrote `androidApp/build/reports/lint-results-debug.xml` (3 `Warning`
  issues). The KMP module had no `lint` task until `com.android.lint` was applied; then `:shared:lint` ran
  `lintAndroidMain` + `lintJvm` and wrote `shared/build/reports/lint-results-androidMain.xml` and
  `lint-results.xml`.
- The Step 3 parser ran on all of those real reports (unscoped, and `--scope Greeter`) and on a SwiftLint JSON
  fixture; it keeps both `MagicNumber` findings on line 12 apart by column.
- **Unverified locally**: SwiftLint (not installed here; the JSON shape follows `iru-swift-code-quality`, itself
  unverified for SwiftLint), Spotless on KMP source sets, the `androidTarget()` + `com.android.library` variant's
  `lintDebug` on the KMP module, and detekt type-resolution findings beyond the smoke run.
- Look up current versions at run time (Gradle plugin portal: `io.gitlab.arturbosch.detekt`, `dev.detekt`,
  `org.jlleitschuh.gradle.ktlint`); October 2026 fallbacks: detekt **1.23.8** (2.0.0-alpha.6 preview), ktlint plugin
  **14.2.0**, AGP **9.4.1**.
