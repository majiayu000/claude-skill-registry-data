---
name: iru-kotlin-code-quality
description: >-
  Run a JVM Kotlin project's wired static-analysis tools — detekt (Gradle `io.gitlab.arturbosch.detekt` 1.x / `dev.detekt` 2.x, or Maven `com.github.ozsie:detekt-maven-plugin`, or a project-provided detekt CLI) and ktlint (Gradle `org.jlleitschuh.gradle.ktlint` or Spotless `ktlint()`, Maven `com.github.gantsign.maven:ktlint-maven-plugin` or Spotless) — on Maven or Gradle (Kotlin DSL or Groovy, wrapper preferred), multi-module aware, then read the generated reports (detekt Checkstyle-format XML or SARIF, ktlint checkstyle/plain reporter output, Spotless console output) to report every issue found (file, line, rule id, severity, message), grouped by tool. Covers plain Kotlin libraries, Kotlin Spring Boot, and Kotlin Quarkus — not Android (use `iru-android-code-quality`); Java sources in a mixed Java+Kotlin module are covered by `iru-java-code-quality`, not here. Invoke as `/iru-kotlin-code-quality` to check the whole project, or `/iru-kotlin-code-quality <path-or-class-name>` to scope the *reported* summary to a file/class/module — detekt/ktlint always analyze whole modules (no per-file selector), so a scoped invocation narrows the build to the owning module and filters the report. Report-only: verifies each tool is actually wired before trusting a "zero issues" result, reports an unwired tool as "not wired" instead of a clean pass, and never adds or changes detekt/ktlint/Spotless configuration. When the prompt supplies a baseline (per-tool/per-rule counts or an itemized list from an earlier run), reports only the new-vs-baseline diff. Use whenever the user wants a Kotlin lint/static-analysis pass called out separately from `iru-java-test`/`iru-java-coverage`, instead of eyeballing `./gradlew detekt` or `mvn verify` console output.
model: haiku
allowed-tools: Read Bash(mvn *) Bash(./mvnw *) Bash(gradle *) Bash(./gradlew *) Bash(detekt *) Bash(detekt-cli *) Bash(ktlint *) Bash(python3 *) Bash(find *) Bash(grep *) Bash(ls *) Bash(awk *) Bash(command -v *) Bash(which *)
---

# Kotlin Code Quality

Run whichever Kotlin static-analysis tools a JVM project actually has wired — detekt and ktlint — and report every
issue they find. This skill only runs static analysis and reports results: it does not fix issues, and it never
adds or modifies detekt/ktlint/Spotless configuration (a missing tool is reported, not installed — that's a
follow-up the user drives). Android modules (`com.android.library`/`com.android.application` applied) are out of
scope — hand those to `iru-android-code-quality`, which also runs Android Lint — and so are Kotlin Multiplatform
modules (`kotlin("multiplatform")` applied), which belong to `iru-kmp-code-quality`.

## Step 0 — Resolve inputs and the build tool

`<scope>` (optional) is a file path, a class/file simple name, or a module name/path. It narrows the build to the
owning module(s) in Step 2 and filters the report in Step 3 — never a per-file tool selector, since neither detekt
nor ktlint is invoked per file here. No `<scope>` → every module, everything reported. If the calling
skill/prompt passes explicit `key: value` lines (e.g. `module: service`, `build: gradle`, a baseline list), honor
them and skip the matching inference below.

Detect the build tool from the repository root — never assume:

- **Gradle**: `settings.gradle.kts`/`settings.gradle` or `build.gradle.kts`/`build.gradle` present. Use
  `./gradlew` (`gradlew.bat` on Windows) when the wrapper exists, otherwise `gradle`. Modules come from
  `include(...)` lines in the settings file (`:service`, `:adapters:web`, …); a single-project build has none.
- **Maven**: `pom.xml` present. Use `./mvnw` (`mvnw.cmd` on Windows) when the wrapper exists, otherwise `mvn`.
  Modules come from the root pom's `<modules>` (recursively for nested aggregators).
- **Both present**: prefer whichever one the CI workflow (`.github/workflows/*.yml`) or contributor guide
  (`CLAUDE.md`, `README`, `CONTRIBUTING`) actually invokes; ask the user only if neither says.

For a `<scope>` naming a file/class, locate it with `find . -name '<Name>.kt' -not -path '*/build/*' -not -path
'*/target/*'` and map it to the module whose directory contains it. A `.java` scope target is not this skill's —
say so and point to `iru-java-code-quality`.

Skip any module that applies an Android Gradle plugin, and note it in the report as "Android module — use
`iru-android-code-quality`". If a Kotlin module also has Java sources (`src/main/java/**/*.java`), mention in the
report that those Java files are covered by `iru-java-code-quality` (Checkstyle/PMD/SpotBugs), not by detekt/ktlint.

Prerequisites: a JDK the build accepts on `JAVA_HOME` (check the toolchain/`<maven.compiler.release>`/`jvmTarget`
the project pins rather than trusting the machine's default `java`).

## Step 1 — Verify which tools are wired

Check the build files of every in-scope module **and** any parent/convention location (root `build.gradle.kts`
`subprojects {}`/`allprojects {}` blocks, `buildSrc/`/`build-logic/` convention plugins, `gradle/libs.versions.toml`
aliases, a parent pom's `<pluginManagement>`/`<plugins>`) before running anything — a "zero issues" result from a
tool that was never configured is meaningless and must not be reported as a clean pass:

**Gradle**

- **detekt** — plugin `io.gitlab.arturbosch.detekt` (1.x) or `dev.detekt` (2.x), applied directly, via
  `alias(libs.plugins.detekt)`, or through a convention plugin. Confirm with
  `./gradlew :<module>:tasks --all | grep -i detekt` (root project: `./gradlew tasks --all`).
- **ktlint** — either (a) `org.jlleitschuh.gradle.ktlint` (check task `ktlintCheck`), or (b) Spotless
  (`com.diffplug.spotless`) with a `kotlin { ktlint(...) }` block (check task `spotlessKotlinCheck`, aggregated by
  `spotlessCheck`). Two different plugins wrapping the same engine — detect which (if either) and use its own task
  name; a `spotless {}` block with only `java {}`/`kotlinGradle {}` does not lint Kotlin sources.

**Maven**

- **detekt** — `com.github.ozsie:detekt-maven-plugin` declared in the module's `<build><plugins>` or inherited
  from a parent's `<plugins>`/`<pluginManagement>`. Read its `<configuration>`/`<execution>` for `<config>`,
  `<baseline>`, `<report>` entries and `<failBuildOnMaxIssuesReached>` — they matter in Step 2.
- **ktlint** — either `com.github.gantsign.maven:ktlint-maven-plugin` (read its `<reporters>` block: a
  `checkstyle` reporter with an `<output>` gives a parseable XML file; without it, findings only reach the
  console), or `com.diffplug.spotless:spotless-maven-plugin` with a `<kotlin><ktlint/></kotlin>` block.

**detekt CLI fallback (either build tool)** — when no detekt plugin is wired but the project clearly runs the CLI
itself (a CI step, `Makefile`/script, or contributor guide invoking `detekt`/`detekt-cli` against a committed
`detekt.yml`), and `command -v detekt` (or `detekt-cli`) finds it installed, run it the way the project does.
Never download a detekt or ktlint binary to fill the gap; if the CLI isn't installed, report detekt as "wired via
CLI in <where>, CLI not installed locally — not run". The same applies to a standalone `ktlint` CLI.

Also note whether a custom detekt config exists (`detekt.yml`/`detekt.yaml`, `config/detekt/detekt.yml`, or
whatever `config.setFrom(...)`/`<config>` points to), whether a baseline file is in use (`detekt-baseline.xml`,
`<baseline>`), and whether `buildUponDefaultConfig` is set — those change what "detekt found nothing" means
(bundled defaults vs. this project's own bar vs. "only new issues beyond the baseline"). For ktlint, rules come
from `.editorconfig` (`ktlint_*` properties, `ktlint_code_style`) — note it if present.

If a tool isn't wired, **skip it and say so in the report** (e.g. `"detekt: not wired (no detekt plugin in any
build file, no CLI usage found)"`). If neither tool is wired anywhere, report exactly that — "No Kotlin static
analysis configured (detekt/ktlint not wired)" — and stop; do not add configuration.

## Step 2 — Run each wired tool

Neither detekt (without type resolution) nor ktlint needs compiled classes, so no `clean compile` is required —
unless the project only wires detekt's type-resolution tasks (`detektMain`/`detektTest`), which compile first.

**Gradle** (prefix each task with `:<module>` for a scoped run; omit the prefix to run every module that applies
the plugin):

```bash
./gradlew :<module>:detekt                 # detekt 1.x / 2.x, no type resolution
./gradlew :<module>:detektMain             # only if the project relies on type-resolution tasks instead
./gradlew :<module>:detektMainSourceSet    # detekt 2.x per-source-set task, if that's what the project/CI runs
./gradlew :<module>:ktlintCheck            # org.jlleitschuh.gradle.ktlint
./gradlew :<module>:spotlessKotlinCheck    # Spotless with kotlin { ktlint() }
```

Name every wired task in one invocation and add `--continue` so a failing ktlint/Spotless check doesn't stop
detekt from running (`./gradlew :service:detekt :service:ktlintCheck --continue`). If a run fails with a
configuration-cache error unrelated to the findings, retry once with `--no-configuration-cache` and note it.

**Maven** — use fully qualified `groupId:artifactId:goal` coordinates (the version comes from the pom's
`<plugins>`/`<pluginManagement>`, and it avoids prefix-resolution surprises in multi-module builds); scope with
`-pl <modules> -am` (comma-separated module paths; reports produced for upstream `-am` modules are ignored in
Step 3):

```bash
./mvnw -B -pl <modules> -am \
  com.github.ozsie:detekt-maven-plugin:check \
  com.github.gantsign.maven:ktlint-maven-plugin:check \
  -Ddetekt.failBuildOnMaxIssuesReached=false \
  '-Ddetekt.report=xml:${project.build.directory}/detekt.xml' \
  -Dktlint.failOnViolation=false
./mvnw -B -pl <modules> -am com.diffplug.spotless:spotless-maven-plugin:check   # if Spotless lints Kotlin
```

- `-Ddetekt.report=...` is only needed when the pom configures no `<report>` of its own (explicit pom
  configuration wins over the user property). Keep it single-quoted with `${project.build.directory}` — Maven
  interpolates it per module; a plain relative `xml:target/detekt.xml` resolves against the directory `mvn` was
  started in, so every module would overwrite the root's file.
- `failBuildOnMaxIssuesReached=false`/`failOnViolation=false` only keep the run going so every report gets
  written — they don't hide anything; a non-zero exit with them set means something else broke.
- ktlint-maven-plugin has no reporter user property: without a `checkstyle` reporter in the pom, parse the console
  lines instead (Step 3).
- detekt-maven-plugin's default `input` is `${basedir}/src` — test sources are analyzed too; that's the project's
  own choice, report them like any other file.

**Exit codes**: `detekt` (Gradle) fails when issues exceed `maxIssues` unless `ignoreFailures = true`;
`ktlintCheck`/`spotlessCheck`/`spotless:check` fail on any violation by design. A non-zero exit from a lint task is
information (violations at/above the configured threshold exist), not "the tool is broken" — always go on and parse
the report. If the build fails for an unrelated reason (compile error, dependency resolution, bad configuration),
report that and stop for the affected tool — don't read a stale report from an earlier run (check the report's
mtime against the run if in doubt).

## Step 3 — Parse each generated report, scoped to `<scope>` if given

Locate reports rather than assuming one fixed name — plugin versions and project overrides move them:

- **detekt, Gradle**: `find <module>/build/reports/detekt -name '*.xml' -o -name '*.sarif'` — 1.x writes
  `detekt.xml`/`detekt.sarif` (plus `.html`/`.md`/`.txt`) for `detekt` and `main.xml`/`test.xml` for
  `detektMain`/`detektTest`; 2.x (`dev.detekt`, checked on 2.0.0-alpha.6) calls the XML report "checkstyle" in its
  DSL/console but still writes `detekt.xml` — match by extension anyway, since a project can rename outputs.
- **detekt, Maven**: whatever `<report>` (or the `-Ddetekt.report` you passed) names — `<module>/target/detekt.xml`
  by this skill's default.
- **ktlint, Gradle plugin**: `find <module>/build/reports/ktlint -type f` — one directory per check task
  (`ktlintMainSourceSetCheck`, `ktlintTestSourceSetCheck`, `ktlintKotlinScriptCheck`), each holding
  `<task>.txt` (plain — the only reporter on by default) and, when `ktlint { reporters { reporter(ReporterType.
  CHECKSTYLE) } }` is configured, `<task>.xml` (also `.sarif`/`.json`/`.html` for those reporter types). Prefer the
  `.xml` when present.
- **ktlint, Maven plugin**: the `checkstyle` reporter's `<output>` (commonly `target/ktlint.xml`), else console.

**Checkstyle-format XML (detekt XML and ktlint checkstyle reporter)** — one parser for both:

```xml
<file name="/abs/path/Foo.kt">
  <error line="9" column="21" severity="warning" message="This expression contains a magic number..." source="detekt.MagicNumber"/>
</file>
<file name="src/main/kotlin/com/example/Foo.kt">
  <error line="5" column="15" severity="error" message="Newline expected after opening parenthesis" source="standard:class-signature"/>
</file>
```

```python
import xml.etree.ElementTree as ET
from collections import Counter

def parse_checkstyle(path, tool, scope=None):
    issues = []
    for f in ET.parse(path).getroot().findall("file"):
        fname = f.get("name")
        if scope and scope not in fname:
            continue
        for e in f.findall("error"):
            src = e.get("source", "")
            # detekt: "detekt.MagicNumber" -> "MagicNumber"; ktlint: "standard:class-signature" kept whole
            rule = src.rsplit(".", 1)[-1] if tool == "detekt" else src
            issues.append((fname, e.get("line"), rule, e.get("severity"), e.get("message")))
    return issues

issues = parse_checkstyle("<report.xml>", "detekt", scope=None)
print("total:", len(issues), "by rule:", dict(Counter(i[2] for i in issues)),
      "by severity:", dict(Counter(i[3] for i in issues)))
```

A `<file>` with no `<error>` children is clean. Paths vary — detekt 1.x (Gradle and Maven) and the Gradle ktlint
plugin write absolute paths; detekt 2.x and the Maven ktlint plugin write module-relative ones — so match `<scope>`
as a substring. Severity is Checkstyle's `error`/`warning`/`info` scale (detekt maps each rule's configured
`severity` — 1.x defaults to `warning`, 2.x to `error`; ktlint reports everything as `error`) — keep each tool's
severities in its own bucket.

**detekt SARIF** (when only `sarif` is enabled): JSON `runs[].results[]`, each with `ruleId` (e.g.
`detekt.style.MagicNumber` — report the last segment), `level` (`error`/`warning`/`note`), and
`locations[0].physicalLocation.{artifactLocation.uri, region.startLine}` (`uri` is a `file://` URL).

**ktlint plain output** (Gradle `.txt` report, the Maven `plain` reporter, or console lines): one issue per line,
`<path>:<line>:<col>: <message> (<rule-id>)`, e.g.
`src/main/kotlin/com/example/Foo.kt:8:36: Missing newline after '{' (standard:statement-wrapping)`. The Gradle
plugin's `.txt` file embeds ANSI color escapes (`\x1b[90m…\x1b[0m`) around the path and rule id — strip them
(`re.sub(r'\x1b\[[0-9;]*m', '', line)`) before splitting. The Gradle console echo of the same findings
(`<path>:<line>:<col> <message>`) omits the rule id — read the report file, not the console. The Maven
plugin's console echo without a `plain` reporter (`[ERROR] <path>:<line>:<col>: <message>`) carries **no rule
id** — bucket those lines under `unknown-rule` and say the rule ids need a `checkstyle`/`plain` reporter in the pom.

**Spotless** — no report file; parse the console. A formatting-only violation lists files under `The following
files had format violations:` followed by a diff per file (one `formatting` bucket, file count, no line/rule). A
lint error ktlint can't auto-fix carries a line and rule id — report it as such: Gradle prints `There were N lint
error(s), they must be fixed or suppressed.` then `<path>:L9 ktlint(standard:if-else-wrapping) <message>`; Maven
prints `Step 'ktlint' found problem in 'Foo.kt':` then `Foo.kt:L9 ktlint(standard:if-else-wrapping) <message>`.
Lint errors are reported instead of (not alongside) the format-violation list, so a file can still have
formatting violations hidden behind them — say so when only lint errors were printed.

For a scoped run, an empty extraction for a tool means that tool found nothing in scope, not that the report is
missing — only treat it as suspicious when no `<file>`/result entry matches the expected path shape at all.

## Step 4 — Classify, diff against a baseline if given, and report

Bucket every issue by **tool, then rule id** (detekt rule name, ktlint `ruleset:rule-id`, Spotless `formatting`) —
never merge buckets across tools even when names look alike, the same convention `iru-android-code-quality` uses.

**Report**: an overall total across all tools first, then per tool (and per module when more than one ran):
whether it ran or was skipped as "not wired" (Step 1), which config/baseline/`.editorconfig` governed it, the
total issue count, the severity breakdown, and one line per rule bucket with its count — plus the file:line list
when the scope is smaller than the whole project. For each issue in an itemized list give file:line, rule id,
severity, and message. Add the Step 0 notes (Android modules skipped, Java sources left to
`iru-java-code-quality`) at the end.

**Baseline diff** — when the prompt supplies a baseline (a prior run's per-tool/per-rule counts or itemized list,
the contract `iru-java-code-one-task-group`/`iru-android-code-one-task-group` use for their code-quality skill):
report only issues that are new since the baseline (a rule whose count increased, a rule that appears now but
didn't before, or a new file:line entry when the baseline was itemized). Decreased/unchanged rules are not
regressions and are omitted from the diff (they still appear in the plain counts). If a tool wasn't run in the
baseline (unwired then, newly wired since), treat all of its current issues as new.

Do not fix any issue, run `ktlintFormat`/`ktlint:format`/`spotlessApply`/detekt `autoCorrect`, create a detekt
baseline, or modify any configuration — those are follow-ups the user (or a coding skill) drives explicitly.

## Known quirks / verification notes

- **Maven path verified locally** (Maven 3.9, JDK 25, Kotlin 2.4.21) in `$TMPDIR/iru-verify/kotlin/iru-kotlin-code-quality/`:
  `detekt-maven-plugin` 1.23.8 `check` with the `-D` flags above wrote `detekt.xml`/`detekt.sarif` in the format
  shown (absolute paths, `source="detekt.<Rule>"`, SARIF `ruleId` `detekt.style.<Rule>`); `ktlint-maven-plugin`
  3.7.1 `check` with a `checkstyle` reporter wrote relative-path XML with `source="standard:<rule>"`, and without
  one only console lines with no rule id; Spotless maven 3.10.4 `kotlin { ktlint }` reported a non-auto-fixable
  ktlint error as `Step 'ktlint' found problem …`; a two-module reactor confirmed `-pl` scoping and that only the
  `${project.build.directory}` form of `-Ddetekt.report` lands per module. The Checkstyle parser above was run
  against those real reports (scoped and unscoped).
- detekt 1.23.x embeds Kotlin compiler 2.0.21 and still parsed Kotlin 2.4 sources (with JDK `sun.misc.Unsafe`
  deprecation warnings on JDK 24+ — harmless); very new syntax can still trip it — report a detekt parse error as
  a tool limitation, not a code issue.
- **Gradle path verified** in Docker (`gradle:8-jdk21`, Gradle 8.14.6, Kotlin JVM plugin 2.4.21) under
  `$TMPDIR/iru-verify/kotlin/iru-kotlin-code-quality-gradle{,2}/`: `io.gitlab.arturbosch.detekt` 1.23.8 `detekt`
  → `build/reports/detekt/detekt.{xml,sarif,html,md,txt}` (absolute paths, `warning`), `detektMain` →
  `main.{xml,…}`, task fails with `Analysis failed with N weighted issues.` but still writes the reports;
  `dev.detekt` 2.0.0-alpha.6 registers `detekt`, `detektMain`/`detektTest` (type resolution) and
  `detektMainSourceSet`/`detektTestSourceSet`, writes `detekt.xml` with relative paths and `error` severity;
  `org.jlleitschuh.gradle.ktlint` 14.2.0 `ktlintCheck` wrote only ANSI-colored `.txt` by default and `.xml` with a
  `CHECKSTYLE` reporter (absolute paths, `source="standard:<rule>"`); Spotless Gradle 8.10.4
  `spotlessKotlinCheck` produced both console shapes described in Step 3. `--continue` let every task run despite
  failures. The Step 3 parser ran correctly on the Gradle detekt 1.x/2.x and ktlint XML reports.
- The Maven plugins are third-party community plugins (detekt and ktlint ship no official Maven integration) —
  look up current versions at run time on Maven Central if a report looks wrong for the version in use; October
  2026 fallbacks: detekt-maven-plugin **1.23.8**, ktlint-maven-plugin **3.7.1**, spotless-maven-plugin **3.10.4**;
  Gradle: detekt **1.23.8** (2.x still alpha), `org.jlleitschuh.gradle.ktlint` **14.2.0**, Spotless **8.10.4**.
