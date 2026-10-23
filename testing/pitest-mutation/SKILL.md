---
name: pitest-mutation
description: "Configures PIT (PITest) for mutation testing of JVM projects (Java, Kotlin via the Kotlin plugin) - wires the `pitest-maven` or `pitest-gradle-plugin` with `mutationThreshold`, `coverageThreshold`, target classes/tests filtering, runs `mvn pitest:mutationCoverage`, parses the HTML + XML reports. Use when the JVM suite needs mutation-quality verification - the canonical Java mutation testing tool, fast (PIT analyzes \"in minutes rather than days\")."
---

# pitest-mutation

## Overview

Per [pit-home][pit]:

[pit]: https://pitest.org/

> "PIT is a mutation testing system for Java and JVM applications.
> It automatically introduces faults into code, then runs tests to
> see if they catch these modifications."
>
> "Faults (or mutations) are automatically seeded into your code,
> then your tests are run. If your tests fail then the mutation is
> killed, if your tests pass then the mutation lived."
> ([pit-home][pit])

Per [pit-home][pit], PIT differentiates on **speed**: "analyzes in
minutes rather than days" vs older mutation tools.

## When to use

- A JVM project (Java, Kotlin via plugin) needs mutation-quality
  verification.
- A team wants to identify "partial testing that traditional metrics
  miss" ([pit-home][pit]).
- Maven / Gradle integration is required (PIT is first-class for
  both).

## How to use

1. Add the `pitest-maven` (or `info.solidsoft.pitest` Gradle) plugin, including `pitest-junit5-plugin` for JUnit 5 suites.
2. Point `targetClasses` at production packages and `targetTests` at the matching test packages - never mutate test code.
3. Set `mutationThreshold` and `coverageThreshold` to the current baseline and request HTML + XML `outputFormats`.
4. Run `mvn pitest:mutationCoverage` (or `./gradlew pitest`) and open `target/pit-reports/<timestamp>/index.html`.
5. For each surviving mutant, add or strengthen a test until it is killed.
6. Use `-DwithHistory` for PR runs so only changed code is re-mutated.
7. In CI, run full weekly and incremental per-PR, uploading `target/pit-reports/` as an artifact.

## Step 1 - Install (Maven)

```xml
<plugin>
  <groupId>org.pitest</groupId>
  <artifactId>pitest-maven</artifactId>
  <version>1.17.0</version>
  <configuration>
    <targetClasses>
      <param>com.example.checkout.*</param>
    </targetClasses>
    <targetTests>
      <param>com.example.checkout.*Test</param>
    </targetTests>
    <mutationThreshold>75</mutationThreshold>
    <coverageThreshold>80</coverageThreshold>
    <outputFormats>
      <format>HTML</format>
      <format>XML</format>
    </outputFormats>
  </configuration>
  <dependencies>
    <dependency>
      <groupId>org.pitest</groupId>
      <artifactId>pitest-junit5-plugin</artifactId>
      <version>1.2.1</version>
    </dependency>
  </dependencies>
</plugin>
```

For JUnit 5, the `pitest-junit5-plugin` is required; for JUnit 4
the default plugin works.

## Step 2 - Run

```bash
mvn pitest:mutationCoverage
```

Reports land at `target/pit-reports/<timestamp>/`. The
`index.html` shows per-class mutation coverage.

## Step 3 - Configure (Gradle)

```gradle
plugins {
    id 'java'
    id 'info.solidsoft.pitest' version '1.15.0'
}

pitest {
    targetClasses = ['com.example.checkout.*']
    targetTests = ['com.example.checkout.*Test']
    mutationThreshold = 75
    coverageThreshold = 80
    outputFormats = ['HTML', 'XML']
    junit5PluginVersion = '1.2.1'
}

// Run via:
// ./gradlew pitest
```

## Step 4 - Mutators

PIT's default mutator set covers conditional, arithmetic, return
value, void method calls, and constructor calls. Activate
additional mutator sets via `<mutators>`:

```xml
<mutators>
  <mutator>STRONGER</mutator>     <!-- All default + extra -->
  <mutator>DEFAULTS</mutator>     <!-- Default set -->
  <mutator>ALL</mutator>          <!-- Everything -->
</mutators>
```

Per [pit-home][pit], reports "combine line coverage with mutation
coverage data."

## Step 5 - `pitmp-maven-plugin` for incremental runs

For PRs, only mutate changed code:

```bash
mvn pitest:mutationCoverage -DwithHistory
```

`withHistory` reads / writes a history file in `target/`; subsequent
runs only mutate code different from the cached history. For PR
runs, combine with git diff to scope further:

```bash
mvn pitest:mutationCoverage \
  -Dfeatures='+gitci(level[1])' \
  -Dpitmp.git.diff.target=origin/main
```

(The `pitmp-maven-plugin` extension adds git-diff-based scoping;
not in core PIT.)

## Step 6 - CI integration

```yaml
- uses: actions/setup-java@v4
  with: { distribution: temurin, java-version: '21' }

- name: Mutation testing (full)
  if: github.event_name == 'schedule'  # weekly cron
  run: mvn pitest:mutationCoverage

- name: Mutation testing (incremental, PR)
  if: github.event_name == 'pull_request'
  run: mvn pitest:mutationCoverage -DwithHistory

- uses: actions/upload-artifact@v4
  if: always()
  with:
    name: pit-reports
    path: target/pit-reports/
```

The XML output (`mutations.xml`) is machine-parseable for
dashboards.

## Step 7 - Kotlin support

PIT works with Kotlin via standard Maven/Gradle Kotlin plugins;
mutators apply to compiled bytecode. Per [pit-home][pit], "ArcMutate,
from the same team, extends PIT with Kotlin support, Spring
integration, and Git analysis" - for richer Kotlin / Spring
support, evaluate ArcMutate (commercial).

## Worked example

`CheckoutService` in `com.example.checkout` has a free-shipping rule and green JUnit 5 tests.

1. Wire the plugin (Step 1) with `targetClasses` = `com.example.checkout.*`, `targetTests` = `com.example.checkout.*Test`, `mutationThreshold` = 75.
2. `mvn pitest:mutationCoverage` writes `target/pit-reports/<timestamp>/index.html` and fails the build below the 75 threshold.
3. `index.html` flags a survivor: the free-shipping boundary `total >= 50` mutated to `total > 50`, uncaught because no test uses `total == 50`.
4. Add a JUnit 5 test at the `total == 50` boundary; `mvn pitest:mutationCoverage` now kills the mutant and clears the threshold.
5. Switch the PR job to `-DwithHistory` so later runs only re-mutate changed classes.

## Pitfalls and limitations

Anti-patterns (mutating everything per PR, `mutationThreshold: 100`, mixed Maven/Gradle config, missing JUnit 5 plugin, targeting test classes, the `ALL` mutator set) and PIT's limitations (bytecode-level equivalent mutants, build-tool coupling, commercial Kotlin / Spring extras, per-class scope) are catalogued in [references/pitest-pitfalls.md](references/pitest-pitfalls.md).

## References

- [pit][pit] - PIT overview: mutation testing definition, JVM-only,
  speed claim ("minutes rather than days"), Maven/Gradle/Ant
  integration, ArcMutate Pro extension.
- `stryker-mutation`,
  `stryker-net-mutation`,
  `mutmut-mutation`,
  `mull-mutation` - per-language
  siblings.
