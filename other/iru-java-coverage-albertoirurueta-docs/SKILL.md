---
name: iru-java-coverage
description: Generate a code coverage report for a JVM (Java or Kotlin) project, scoped to the test selector given (same selector syntax as the `iru-java-test` skill), and report the exact line-coverage percentage for the specific class(es) touched. Maven — `mvn clean jacoco:prepare-agent test jacoco:report`, read from `target/site/jacoco/jacoco.csv`. Gradle (wrapper preferred, Kotlin DSL or Groovy) — JaCoCo via `./gradlew clean test --tests '<pattern>' jacocoTestReport` (CSV/XML under `build/reports/jacoco/test/`, both forced on through a throwaway init script when the build doesn't enable them), or Kover via `koverXmlReport` (`build/reports/kover/report.xml`) when the `org.jetbrains.kotlinx.kover` plugin is applied. Quarkus — also reads the `quarkus-jacoco` extension's report (`target/jacoco-report/` or `build/jacoco-report/`) for `@QuarkusTest` coverage. Falls back to the per-class HTML source report to show which lines/branches are still uncovered, and accounts for Kotlin's compiler-generated classes (`FooKt`, `Foo.Companion`, lambdas). Measures unit tests only — never runs Failsafe/`integrationTest`/`quarkusIntTest`. Invoke as `/iru-java-coverage <selector> [TargetClass1,TargetClass2,...]`, or `/iru-java-coverage` with no argument to run the full unit suite and report whole-project coverage. Use whenever the user wants to check, or verify a coverage bar (e.g. "at least 80% line coverage") for a class or set of classes, instead of eyeballing test output.
model: haiku
allowed-tools: Read Write Bash(mvn *) Bash(./mvnw *) Bash(./gradlew *) Bash(gradle *) Bash(cat *) Bash(awk *) Bash(grep *) Bash(find *) Bash(ls *) Bash(mkdir *) Bash(python3 *) Bash(rm -f */jacoco.exec) Bash(rm -f jacoco.exec) Bash(QUARKUS_DEVSERVICES_ENABLED=false *) Bash(QUARKUS_JACOCO_REPORT=false *) Bash(java -jar *jacoco*cli*)
---

# Java Coverage

Run JaCoCo (or Kover) against a scoped (or full) unit-test run and report the exact, measured coverage percentage
for the class(es) the user cares about. Works for Java and Kotlin sources, Maven and Gradle builds. This skill only
measures and reports coverage — it does not add tests or modify source/test/build code unless asked to as a
follow-up.

## Step 0 — Detect the build tool and coverage engine

Detect the build tool exactly as `iru-java-test`'s Step 0 does (`pom.xml` → Maven; `settings.gradle(.kts)`/
`build.gradle(.kts)` → Gradle, `./gradlew` preferred over `gradle`; Android Gradle plugin → use
`iru-android-coverage` instead; Kotlin Multiplatform plugin → use `iru-kmp-coverage` instead). Then pick the coverage engine:

- **Maven** → JaCoCo through `jacoco-maven-plugin` (Step 3a).
- **Gradle with Kover** — `org.jetbrains.kotlinx.kover` (or `id("org.jetbrains.kotlinx.kover")`/a `kover` alias in
  `gradle/libs.versions.toml`) applied in a build script → Kover (Step 3c). Prefer it over JaCoCo when both are
  applied, since it is the engine the project chose for its Kotlin code.
- **Any other Gradle build** → JaCoCo through Gradle's `jacoco` plugin (Step 3b) — applied by the build already,
  or added for this run only by Step 3b's init script.
- **Quarkus** (`io.quarkus` plugin / `quarkus-bom` / `io.quarkus:quarkus-*` dependencies) — additionally check for
  the `io.quarkus:quarkus-jacoco` test dependency. JaCoCo's ordinary agent cannot attribute coverage for classes
  Quarkus transforms at build time, so `@QuarkusTest` coverage only shows up in `quarkus-jacoco`'s own report
  (Step 4's Quarkus note). Plain unit tests (no `@QuarkusTest`) are measured by the ordinary engine as usual.

## Step 1 — Determine the test scope

If the user gave a selector, it uses the exact same syntax as the `iru-java-test` skill's Step 1 tables (class,
class+method, comma list, wildcard, package pattern, tag expression — translated to Gradle `--tests` patterns the
same way). If no selector was given, run the whole unit suite.

Important: JaCoCo only records coverage for code actually exercised by the tests that ran in this invocation. If
a class under test is covered by tests spread across multiple test classes, the selector must include all of
them (comma-separated / one `--tests` each) — scoping to just one of them will undercount that class's real
coverage. When in doubt about whether a selector covers everything relevant to the target class, prefer a broader
selector (e.g. the whole package, or the full suite) over a narrow one.

**Unit tests only.** This skill measures the unit-test run alone — Maven Surefire (`test` phase; callers may pass
`-DskipITs`, which is harmless here since `verify` is never reached), Gradle's `test` task. Never run `mvn verify`,
Failsafe, or a Gradle `integrationTest`/`quarkusIntTest`/`check`/`build` task from this skill: callers such as the
Spring Boot/Kotlin Spring Boot/Quarkus group skills gate on coverage earned **without** containers, and folding
integration tests in would hide a class that is only covered through them.

## Step 2 — Determine the target class(es) to report on

- If the user (or the calling skill) explicitly named target class(es), use those.
- Otherwise, infer them from the test selector by convention: a test class `FooTest` targets `Foo`,
  `FooTest#methodName` still targets `Foo`. For a comma list of test classes, infer one target class per test
  class.
- If the selector is a wildcard, package pattern, or tag expression, target classes can't be inferred by name —
  report on every class touched by that run (Step 4 already surfaces all of them), or ask the user which class(es)
  they care about if the run touches many unrelated ones.
- **Kotlin**: one source file can compile to several JVM classes, each a separate report row — for a target `Foo`
  (in `Foo.kt`) also consider `FooKt` (top-level functions/properties in that file), `Foo.Companion` /
  `Foo$Companion` (companion object), and `Foo$…` lambda/coroutine-continuation classes. Include them when the
  code under discussion lives there.

## Step 3 — Run the coverage build

### 3a — Maven

```bash
mvn clean jacoco:prepare-agent test jacoco:report -Dtest=<selector>
```

Omit `-Dtest=<selector>` entirely to run the full suite; add `-pl <module list> -am` when the caller scoped the run
to modules (each module then gets its own `<module>/target/site/jacoco/`). Do not add profile flags —
they only affect the `package`-phase source/javadoc jar attachment, which this command never reaches, so they
have no effect on the test run or the coverage report and just add noise.

The `jacoco:` prefix resolves when the project's `pom.xml` declares `jacoco-maven-plugin`; if Maven fails with
"No plugin found for prefix 'jacoco'", use the fully qualified goals instead
(`org.jacoco:jacoco-maven-plugin:<version>:prepare-agent` … `:report`, current release version).

This regenerates `target/site/jacoco/` from scratch each time (the `clean` goal wipes the previous `jacoco.exec`
and report), so there's no risk of reading a stale report from an earlier run. Kotlin sources compiled by
`kotlin-maven-plugin` land in the same `target/classes`, so the command is unchanged for Kotlin or mixed modules.

### 3b — Gradle with JaCoCo

Gradle's `jacocoTestReport` only writes HTML by default (`xml.required`/`csv.required` are off), and a build may not
apply the `jacoco` plugin at all. Rather than editing the build, pass a throwaway init script that applies the
plugin to every Java/Kotlin JVM module and forces the CSV and XML reports on, for this run only:

```bash
mkdir -p "$TMPDIR/iru-java-coverage"
cat > "$TMPDIR/iru-java-coverage/jacoco-reports.init.gradle" <<'EOF'
allprojects {
    pluginManager.withPlugin('java') {
        pluginManager.apply('jacoco')
        tasks.withType(JacocoReport).configureEach {
            reports {
                xml.required = true
                csv.required = true
            }
        }
    }
}
EOF
./gradlew clean test --tests '<pattern>' jacocoTestReport \
  --init-script "$TMPDIR/iru-java-coverage/jacoco-reports.init.gradle"
```

- `--tests` must follow the `test` task it filters (it attaches to the task named right before it); omit it to run
  the full suite. For a multi-module build scoped to modules, name each module's tasks:
  `./gradlew clean :service:test --tests '<pattern>' :service:jacocoTestReport --init-script …`.
- Running `test` and `jacocoTestReport` in the same invocation (in that order) guarantees the report is built from
  this run's execution data even when the build doesn't wire `finalizedBy`/`dependsOn` between them; `clean` wipes
  the previous `build/jacoco/test.exec` so nothing stale is merged in.
- The init script is Groovy, which every Gradle version accepts whether the build itself uses the Kotlin DSL or
  Groovy. It only adds configuration; it never changes the project's files. A build script that explicitly sets
  `xml.required = false`/`csv.required = false` on `jacocoTestReport` runs after the init script and wins — then
  use whichever format the build left enabled (HTML at worst) and say so.

Reports land per module at `build/reports/jacoco/test/jacocoTestReport.csv` and `…/jacocoTestReport.xml` (or the
`outputLocation`s the build configured — check `jacocoTestReport { reports { … } }` if those files are missing).

### 3c — Gradle with Kover

```bash
./gradlew clean test --tests '<pattern>' koverXmlReport
```

Kover's report tasks depend on the `test` tasks themselves, and the `--tests` filter on the explicitly named `test`
task still applies. The XML report is at `build/reports/kover/report.xml` (Kover 0.7+; for an aggregated
multi-module setup, the root project's `build/reports/kover/report.xml` covers every module listed in its
`dependencies { kover(project(":x")) }`). It uses the JaCoCo XML format, so Step 4's XML path reads it unchanged.
Kover variants other than the default (`koverXmlReport<Variant>`) are only relevant when the user asks for one.

### Build failures

If the build fails (compilation error or test failure), report that failure — don't attempt to read a coverage
report that wasn't (re)generated. A `@QuarkusTest`/Testcontainers start-up failure because Docker isn't available
is an **environment failure** (see `iru-java-test`'s Quarkus notes), not a coverage result — report it as such and
name the test classes that couldn't run.

## Step 4 — Read the exact coverage

Use the CSV when one exists (Maven's `target/site/jacoco/jacoco.csv`, Gradle JaCoCo's
`build/reports/jacoco/test/jacocoTestReport.csv`, `quarkus-jacoco`'s `jacoco.csv` if it wrote one); otherwise the
JaCoCo-format XML (Gradle JaCoCo's `jacocoTestReport.xml`, Kover's `report.xml`, `quarkus-jacoco`'s `jacoco.xml`).

### From a CSV

Its header is:

```
GROUP,PACKAGE,CLASS,INSTRUCTION_MISSED,INSTRUCTION_COVERED,BRANCH_MISSED,BRANCH_COVERED,LINE_MISSED,LINE_COVERED,COMPLEXITY_MISSED,COMPLEXITY_COVERED,METHOD_MISSED,METHOD_COVERED
```

For a small, known number of target classes from Step 2 (the common case), extract just their row(s) instead of
reading the whole file — a multi-module project's CSV can have many rows:

```bash
awk -F, 'NR==1 || $3=="<ClassName1>" || $3=="<ClassName2>"' target/site/jacoco/jacoco.csv
```

(Gradle: the same command against `build/reports/jacoco/test/jacocoTestReport.csv`, once per module.)

Matching the `CLASS` column exactly (not a substring grep) avoids a false match against an unrelated class whose
name merely contains the target's (e.g. `FooBar` when the target is `Foo`) — nested/inner classes appear as
separate rows, e.g. `Outer.Inner` (`Outer$Inner` in older JaCoCo versions), and need their own explicit condition
if relevant. If Step 2 couldn't narrow down to specific class names (a wildcard/package-pattern/full-suite run
touching many classes), read the whole file instead — composing a long `awk` condition for many classes isn't
worth it once there are more than a handful.

For each target class, once you have its row, compute:

```
line coverage %      = LINE_COVERED / (LINE_COVERED + LINE_MISSED) * 100
branch coverage %     = BRANCH_COVERED / (BRANCH_COVERED + BRANCH_MISSED) * 100   (n/a if both are 0, e.g. enums/records with no branches)
instruction coverage % = INSTRUCTION_COVERED / (INSTRUCTION_COVERED + INSTRUCTION_MISSED) * 100
```

### From a JaCoCo-format XML

Each `<class name="com/example/Foo">` element's direct `<counter type="LINE|BRANCH|INSTRUCTION" missed=".."
covered=".."/>` children are that class's totals. Extract the target classes (a target `Foo` also matches its
nested `Foo$…` classes; pass `FooKt` explicitly for Kotlin top-level functions) without reading the whole file:

```bash
python3 - <report.xml> <ClassName1> <ClassName2> <<'PY'
import sys, xml.etree.ElementTree as ET
path, targets = sys.argv[1], sys.argv[2:]
root = ET.parse(path).getroot()
for pkg in root.iter("package"):
    for cls in pkg.findall("class"):
        name = cls.get("name").split("/")[-1]            # e.g. Foo, Foo$Companion, FooKt
        if targets and not any(name == t or name.startswith(t + "$") for t in targets):
            continue
        c = {x.get("type"): (int(x.get("missed")), int(x.get("covered"))) for x in cls.findall("counter")}
        def pct(k):
            m, v = c.get(k, (0, 0))
            return "n/a" if m + v == 0 else f"{v / (m + v) * 100:.1f}% ({v}/{m + v})"
        print(f"{pkg.get('name').replace('/', '.')}.{name}: line {pct('LINE')}, branch {pct('BRANCH')}, instruction {pct('INSTRUCTION')}")
PY
```

With no class names it prints every class — fine for a small module, otherwise narrow it.

### Source of truth and edge cases

Use the CSV/XML counters, not the HTML `index.html` tables, as the source of truth for the percentage — the HTML
package-level table's "Cov." columns are instruction and branch coverage only; it never prints a line-coverage
percentage directly, only raw missed/total line counts, so computing from the CSV/XML is more direct and less
error-prone than parsing HTML.

If a target class doesn't appear in the report at all, it means no code in that class executed during this run
(either it's dead/unreachable from the tests that ran, or the selector didn't include tests that exercise it) —
report 0%, not an error. (A class with no executable code may also be omitted — e.g. an interface without
default methods. Kover, unlike JaCoCo, also lists classes the run never loaded, at 0%.)

**Kotlin noise.** Recent JaCoCo versions (0.8.x) filter most Kotlin compiler-generated bytecode — data class
`equals`/`hashCode`/`toString`/`copy`/`componentN`, `lateinit` and non-null checks, `when`-on-string hashing,
inline-function bodies inlined into callers — so a data class typically shows only its constructor and property
getters. What remains can still look like gaps: an `inline`/`reified` function's own body (only ever executed
inlined into callers), a companion object or `FooKt` row that's never touched directly, coroutine state-machine
branches in `suspend` functions. Call these out as generated-code noise rather than as missing tests when the
uncovered lines in the source HTML map to them. Kover's default engine applies its own, similar filtering, but its
counters are not identical to JaCoCo's for the same run (e.g. it counted a companion object's static initializer as
covered where JaCoCo reported the `Companion` row at 0%) — compare a class only against numbers from the same engine.

**Quarkus (`quarkus-jacoco`).** When the extension is present and `@QuarkusTest` classes ran, its report is written
to `target/jacoco-report/` (Maven) or `build/jacoco-report/` (Gradle) — `jacoco.xml` (and `index.html`), unless
`quarkus.jacoco.report-location` moves it. It covers what the `@QuarkusTest` classes exercised; the ordinary
report from Step 3 covers the plain unit tests. Unless the project merges the two (e.g. a shared
`quarkus.jacoco.data-file` with `jacoco-maven-plugin`), read both for each target class and report both numbers,
labelled by source — never add them up (overlapping lines would be double-counted), and say that the true combined
figure is at least the higher of the two. A `@QuarkusTest` that needs Dev Services containers is not a no-container
unit test: when the caller's gate is "unit tests only", report its contribution separately, for information.

**Quarkus `@QuarkusComponentTest` coverage** (verified on Quarkus 3.40). The ordinary JaCoCo agent reports **0%** for
a class exercised only by `@QuarkusComponentTest`, whether or not `quarkus-jacoco` is present, because Quarkus loads
those classes through its own class loader. From Quarkus 3.31, `quarkus-jacoco` instruments component tests (and
`@QuarkusTest` subjects) itself; without a `@QuarkusTest` in the run its runtime writes to the `jacoco-agent.destfile`
system property, default `<module>/jacoco.exec`. Keep that data in its **own** file and merge it with the agent's —
never point `jacoco-agent.destfile` at the agent's exec file: two writers on one file in one JVM lose data (a
component-tested class falls back to its plain-test figure, and `@QuarkusTest` subjects to 0%, as soon as a
`@QuarkusTest` shares the run).

- **The build already wires it** (a Surefire `systemPropertyVariables`/Gradle test-task `jacoco-agent.destfile` of
  `<build dir>/jacoco-quarkus.exec`, the agent's `exclClassLoaders`/`excludeClassLoaders` = `*QuarkusClassLoader`, and
  a `merge` execution or a `jacocoTestReport` reading both files): use it — Maven
  `test jacoco:merge@<merge id> jacoco:report@<report id>` (ids from the pom), Gradle `test jacocoTestReport`.
- **Maven, ad hoc**: add `-Djacoco.exclClassLoaders='*QuarkusClassLoader' -Djacoco-agent.destfile=target/jacoco-quarkus.exec
  -Dquarkus.jacoco.report=false` to the Step 3 run (drop `jacoco:report` from it), then merge with the JaCoCo CLI —
  `mvn dependency:copy -Dartifact=org.jacoco:org.jacoco.cli:<jacoco version>:jar:nodeps -DoutputDirectory=target/jacoco-cli`,
  `java -jar target/jacoco-cli/org.jacoco.cli-<version>-nodeps.jar merge target/jacoco.exec target/jacoco-quarkus.exec
  --destfile target/jacoco-merged.exec` — and report with `jacoco:report -Djacoco.dataFile=target/jacoco-merged.exec`.
- **Gradle, ad hoc**: add to the throwaway init script, for each project, `tasks.withType<Test>().configureEach { val q =
  project.layout.buildDirectory.file("jacoco-quarkus.exec").get().asFile; jvmArgumentProviders.add(
  CommandLineArgumentProvider { listOf("-Djacoco-agent.destfile=" + q.absolutePath) }); doFirst { q.delete() };
  extensions.findByType(JacocoTaskExtension::class.java)?.excludeClassLoaders = listOf("*QuarkusClassLoader") }` and
  `tasks.withType<JacocoReport>().configureEach { executionData(project.fileTree(project.layout.buildDirectory) {
  include("jacoco/test.exec", "jacoco-quarkus.exec") }) }`. It must be a JVM argument: a `systemProperty()` set from
  an init script is reset by the Quarkus Gradle plugin and silently ignored. Run with `QUARKUS_JACOCO_REPORT=false` in
  the environment so `quarkus-jacoco` doesn't write (and wait for) its own second report.

Without `quarkus-jacoco` (or on Quarkus < 3.31), report such classes as **unmeasured — exercised only by component
tests**, never as 0% covered, and suggest adding the extension rather than adding it. Delete a stray
`<module>/jacoco.exec` left by an earlier run unless the project already ignores it. Container-free runs on Gradle
disable Dev Services through the environment (`QUARKUS_DEVSERVICES_ENABLED=false ./gradlew …`) because `-D` doesn't
reach the test JVM; on Maven `-Dquarkus.devservices.enabled=false` works.

## Step 5 — Report results

State, per target class, the line coverage percentage (and branch coverage if relevant to the discussion),
computed from actual CSV/XML numbers — never estimate or guess — and which report it came from (JaCoCo Maven,
JaCoCo Gradle, Kover, `quarkus-jacoco`). If the user's bar is "at least N%": say clearly whether each class meets it.

For classes under the bar, point to the per-class HTML report for line-level detail on exactly what's uncovered:
Maven `target/site/jacoco/<package-with-dots>/<ClassName>.html` (e.g.
`target/site/jacoco/com.example.myapp/Foo.html`), Gradle JaCoCo `build/reports/jacoco/test/html/<package>/…`,
Kover `build/reports/kover/html/` (generate with `koverHtmlReport` only if the user wants it). Read the JaCoCo
companion source file (same name plus the source extension, e.g. `Foo.java.html` or `Foo.kt.html`) for the actual
highlighted source: each line is a `<span class="nc" id="L<n>">` (not covered), `<span class="pc" id="L<n>">`
(partially covered branch), or `<span class="fc" id="L<n>">` (fully covered) —
`grep -o 'class="nc" id="L[0-9]*"' <file>` gives the exact uncovered line numbers when the user wants to know
precisely which lines/branches to target with new tests, rather than just the aggregate percentage. In the XML,
the `<sourcefile name="Foo.kt">` element's `<line nr=".." mi=".." mb=".."/>` entries give the same per-line detail
(`mi > 0` → missed instructions on that line; `mb > 0` → missed branches).

Do not add tests, modify source/test/build code, or re-run anything to try to raise coverage — that's a follow-up
the user (or another skill, e.g. `iru-code`) drives explicitly.

## Verification notes

- Maven + Kotlin (`$TMPDIR/iru-verify/java/iru-java-coverage/kt/`, `kotlin-maven-plugin` 2.2.0, JaCoCo 0.8.13 via
  the fully qualified goals): `jacoco.csv` rows `Foo`, `Foo.Companion`, `FooKt`, `Point` (data class generated
  members filtered), `Foo.kt.html` source report; the Step 4 XML reader matched the CSV numbers.
- Gradle 8 (`gradle:8-jdk21` Docker image), Kotlin DSL multi-module build with a mixed Kotlin/Java `svc` module and
  **no** `jacoco` plugin applied (`$TMPDIR/iru-verify/java/iru-java-coverage-gradle/`): the Step 3b init script
  (extracted from this file) applied JaCoCo and produced `svc/build/reports/jacoco/test/jacocoTestReport.csv` and
  `.xml` plus `html/com.ex/Foo.kt.html`; the Step 4 `awk` and XML reader both worked on them.
- Gradle 8 + Kover 0.9.1 (`$TMPDIR/iru-verify/java/iru-java-coverage-kover/`): `clean test --tests 'FooTest.should
  parse input' koverXmlReport` ran exactly that one test and wrote `svc/build/reports/kover/report.xml`, which the
  Step 4 XML reader parsed unchanged.
- Not verified: `quarkus-jacoco` report paths/contents (taken from the Quarkus docs), Kover multi-module
  aggregation.
