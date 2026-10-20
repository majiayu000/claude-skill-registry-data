---
name: iru-java-code-quality
description: >-
  Run this project's Java static-analysis tools — Checkstyle, PMD, and SpotBugs — and summarize every issue found (file, line, rule/check, message), grouped by tool. Maven: `mvn clean compile checkstyle:checkstyle pmd:pmd spotbugs:spotbugs`, reading `target/checkstyle-result.xml`, `target/pmd.xml`, and `target/spotbugsXml.xml`. Gradle (wrapper preferred, Kotlin DSL or Groovy): whichever of `checkstyleMain`, `pmdMain`, and `spotbugsMain` (the `com.github.spotbugs` plugin) the build actually defines, run with `--continue`, reading their XML reports under `build/reports/checkstyle/`, `build/reports/pmd/`, and `build/reports/spotbugs/`. Kotlin sources are not analyzed by Checkstyle or PMD (and SpotBugs only sees their bytecode) — for Kotlin code use `iru-kotlin-code-quality` (detekt + ktlint); a mixed Java/Kotlin project runs both. Invoke as `/iru-java-code-quality` to check the whole project, or `/iru-java-code-quality <path-or-class-name>` to scope the summary to a specific file/class — the underlying build always analyzes the whole project (none of these tools support a per-class selector), only the reported summary is filtered. Use whenever the user wants a lint/static-analysis pass called out separately from `iru-java-test`/`iru-java-coverage`, instead of running the full `mvn site`/`./gradlew check` build.
model: haiku
allowed-tools: Read Bash(mvn *) Bash(./mvnw *) Bash(./gradlew *) Bash(gradle *) Bash(awk *) Bash(grep *) Bash(find *) Bash(ls *)
---

# Java Code Quality

Run Checkstyle, PMD, and SpotBugs directly (not via `mvn site`/`./gradlew check`) and report every issue they find.
This skill only runs static analysis and reports results — it does not fix issues unless asked to as a follow-up.

## Step 0 — Detect the build tool and the languages in play

- Detect the build tool exactly as `iru-java-test`'s Step 0 does (`pom.xml` → Maven; `settings.gradle(.kts)`/
  `build.gradle(.kts)` → Gradle, `./gradlew` preferred over `gradle`; Android Gradle plugin → use
  `iru-android-code-quality` instead; Kotlin Multiplatform plugin → use `iru-kmp-code-quality` instead).
- **Kotlin sources are not analyzed by these tools.** Checkstyle and PMD parse Java source only, so anything under
  `src/main/kotlin` (or `.kt` files anywhere) is invisible to them. SpotBugs works on bytecode, so it does see
  compiled Kotlin classes, but its findings there are dominated by Kotlin compiler-generated patterns (null-check
  intrinsics, synthetic accessors, data class methods) and are no substitute for a Kotlin linter. Kotlin code is
  covered by `iru-kotlin-code-quality` (detekt + ktlint):
  - **Pure Kotlin project** (no `src/main/java`, no `.java` files outside build output): say so, point the caller
    to `iru-kotlin-code-quality`, and stop — unless SpotBugs is explicitly configured in the build and the user
    wants its output anyway.
  - **Mixed Java/Kotlin**: run this skill for the Java sources and state in the report that the Kotlin sources were
    not covered here and need `iru-kotlin-code-quality` as well.

## Step 1 — Run the static analysis tools

### Maven

```bash
mvn clean compile checkstyle:checkstyle pmd:pmd spotbugs:spotbugs
```

- `clean compile` first is required: SpotBugs analyzes compiled bytecode under `target/classes`, and fails
  silently ("No files found to run spotbugs, check compile phase has been run" — build still succeeds, but no
  `spotbugsXml.xml` is produced) if that directory is missing or stale relative to the current source.
- Checkstyle and PMD only need source. Each picks up whatever ruleset the project's `pom.xml` configures for it
  (a custom `configLocation`/`rulesets` file, or the plugin's own defaults if the pom doesn't override them).
- Running the three goals directly, instead of `mvn site`, skips the slower javadoc/JXR/Surefire-report
  generation the full site build also does — this is meant to be a quick, focused quality pass.
- Do not add profile flags, they only affect package-phase source/javadoc jar attachment and has
  no effect on these goals.

### Gradle

Gradle's `checkstyle` and `pmd` plugins and the `com.github.spotbugs` plugin each add one task per source set; the
`*Main` tasks analyze production code. Only some of them may be applied, and asking Gradle to run a task that
doesn't exist anywhere fails the whole invocation ("Task 'pmdMain' not found"), so first list which exist:

```bash
./gradlew -q tasks --all | grep -oE '(^|:)(checkstyleMain|pmdMain|spotbugsMain)\b' | sort -u
```

Then run exactly those (a bare task name runs it in every module that defines it):

```bash
./gradlew clean checkstyleMain pmdMain spotbugsMain --continue
```

- `clean` matters for the same reason as Maven's: `spotbugsMain` depends on compiling `main`, and up-to-date tasks
  would otherwise be skipped without regenerating their reports. Compilation (`compileJava`, and `compileKotlin` in
  a mixed module) runs automatically as a dependency.
- `--continue` is required, not cosmetic: by default Checkstyle (any error-severity violation), PMD (any violation)
  and SpotBugs (any bug) **fail their task** when they find issues, and without `--continue` Gradle stops at the
  first failed task so the remaining tools never run. A task that fails *because it found violations* still wrote
  its report — that is a result to read, not a build failure. Only a compilation failure (or a tool/configuration
  error such as a missing ruleset file) means the reports weren't produced.
- Do not add `-x`, `--offline`, or `ignoreFailures` overrides, and don't run `check`/`build` (they also run tests).
- If none of the three tasks exists, say so — none of these tools is configured in this Gradle build — and stop;
  don't apply plugins or edit the build to add them.

Reports, per module:

| Tool | XML report (default location) |
|---|---|
| Checkstyle | `build/reports/checkstyle/main.xml` |
| PMD | `build/reports/pmd/main.xml` |
| SpotBugs | `build/reports/spotbugs/main.xml` — only when the build enables an XML report (`tasks.spotbugsMain { reports.create("xml") { required = true } }` in Kotlin DSL, `spotbugsMain { reports { xml { required = true } } }` in Groovy) |

If the build configured a different `destination`/`outputLocation`, or enabled only an HTML/SARIF SpotBugs report,
use what the build configures — `find . -path '*/build/reports/*' -newer build.gradle* -name '*.xml'` (or `.sarif`)
locates the freshly written files. Don't edit the build to switch a report format on; if SpotBugs only produced HTML,
read the HTML and say so in the report. With **no** SpotBugs report configured at all, the plugin writes no file —
it prints one line per bug to the console instead (`H C NP: Null pointer dereference of s in com.ex.Bar.twice(int)
Dereferenced at Bar.java:[line 4]` — priority H/M/L, category letter, bug-pattern abbreviation, message, location), so
run with `--console=plain` and parse those lines from the output.

Gradle's `pmd` plugin defaults to the `category/java/errorprone.xml` ruleset only (unless `pmd { ruleSetFiles/
ruleSets }` says otherwise), so an empty PMD report on a Gradle build is common and doesn't mean the stricter
Maven-style rulesets were applied.

### Build failures

If the build fails outright (e.g. a compile error), report that and stop — the reports below won't have been
freshly (re)generated, so don't read stale copies from an earlier run.

## Step 2 — Read each generated report, scoped to the request if given

Three XML reports are produced, one per tool (under `target/` for Maven, under each module's `build/reports/` for
Gradle — see the table above). The file formats are identical between Maven and Gradle; only the paths differ, so
substitute the Gradle path in every command below. Console output only shows progress, not the full issue
list, so these need to be read directly — but the run in Step 1 always analyzed the whole project
regardless of scope (none of these plugins expose a per-file CLI selector like Surefire's `-Dtest`), so a scoped
invocation should extract just the matching entries rather than reading each full report and filtering
afterward — these reports can get large on a project with many files/issues.

**With no argument** (project-wide): read each of the three files in full.

**With a specific file/class name**: extract only the matching block(s) instead of reading the whole file:

- **Checkstyle** (`target/checkstyle-result.xml`) and **PMD** (`target/pmd.xml`) both wrap each file's issues in
  a `<file name="...">...</file>` block — extract just the matching block(s):
  `awk '/<file name="[^"]*\/<Name>\.java"/,/<\/file>/' target/checkstyle-result.xml` (same for `pmd.xml`).
  A `.kt` name never appears in these two reports (see Step 0).
- **SpotBugs** (`target/spotbugsXml.xml`) doesn't group issues by file the same way — grep for the class name
  with enough surrounding context to capture the whole `<BugInstance>` block it belongs to:
  `grep -B 8 -A 4 'classname="[^"]*\.<Name>"' target/spotbugsXml.xml` (widen the context window if a match looks
  cut off; a `<BugInstance>` rarely runs past a dozen lines). Infer the base package from any matching entry
  rather than assuming one, and also match a nested class (e.g. `Foo$Inner` when `<Name>` is `Foo`).

An empty extraction for a tool means that tool found nothing for this file/class, not that the report is
missing — only fall back to reading the whole file if the extraction itself looks wrong (e.g. no `<file>`/
`classname` entry anywhere matches the expected pattern at all, suggesting a naming mismatch rather than a clean
result).

**Checkstyle** entries look like:
```xml
<file name="/abs/path/Foo.java">
  <error line="28" column="12" severity="error" message="..." source="com.puppycrawl.tools.checkstyle.checks.sizes.LineLengthCheck"/>
</file>
```
A `<file>` with no `<error>` children is clean. The rule name is the last segment of `source` (e.g.
`LineLengthCheck`).

**PMD** entries look like:
```xml
<file name="/abs/path/Foo.java">
  <violation beginline="130" endline="130" rule="UnnecessaryModifier" ruleset="Code Style"
             package="com.example.pkg" class="Foo" method="bar" priority="3">
    message text
  </violation>
</file>
```
`priority` is PMD's own 1 (highest) to 5 (lowest) scale; unless the build sets a minimum priority
(`<minimumPriority>` in the pom, `rulesMinimumPriority` in Gradle's `pmd {}` block), all five levels are reported.

**SpotBugs** entries look like:
```xml
<BugInstance category="BAD_PRACTICE" priority="2" type="CT_CONSTRUCTOR_THROW">
  <ShortMessage>...</ShortMessage>
  <LongMessage>...</LongMessage>
  <Class classname="com.example.pkg.Foo" primary="true">
    <SourceLine classname="com.example.pkg.Foo" start="36" end="50" sourcefile="Foo.java"/>
  </Class>
</BugInstance>
```
`priority` here is SpotBugs' own scale (1 = High, 2 = Medium, 3 = Low) — distinct from PMD's. A `BugInstance` may
list secondary classes/methods/fields in addition to the primary one; report against the primary `<Class>`'s
`<SourceLine>` for file/line.

## Step 3 — Report

Group findings by tool, then by file. For each issue, give file:line, the rule/check name, and the message.
State a total count per tool at the top and an overall total; if a tool found zero issues (in the requested
scope), say so briefly rather than omitting it silently. For Gradle, say which of the three tasks exist in the
build (a tool that isn't configured is "not configured", not "zero issues"). If the project has Kotlin sources,
end with a one-line note that they were not covered by Checkstyle/PMD and need `iru-kotlin-code-quality`.

Do not attempt to fix any of the issues found, or modify source/checkstyle/pmd/spotbugs configuration — that's a
follow-up the user drives explicitly.

## Verification notes

Gradle path verified with Gradle 8 (`gradle:8-jdk21` Docker image) in
`$TMPDIR/iru-verify/java/iru-java-code-quality-gradle/`, a Kotlin DSL multi-module build whose `svc` module mixes
Kotlin (`src/main/kotlin`) and Java (`src/main/java`) and applies `checkstyle`, `pmd`, and `com.github.spotbugs`
6.1.13: the `tasks --all | grep` detection found all three tasks (as `:checkstyleMain` etc.); `clean checkstyleMain
pmdMain spotbugsMain --continue` ran all three even though Checkstyle and SpotBugs failed their tasks on findings,
and wrote `build/reports/checkstyle/main.xml`, `build/reports/pmd/main.xml`, and (with the XML report enabled)
`build/reports/spotbugs/main.xml` in the same formats as Maven's; the Step 2 `awk`/`grep` extractions worked on them
unchanged; no `.kt` file appeared in the Checkstyle or PMD report. Without an XML report, SpotBugs wrote no file and
printed its findings to the console as shown above. The Maven path is unchanged.
