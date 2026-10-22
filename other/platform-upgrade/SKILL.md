---
name: platform-upgrade
description: >
  Takes a Maven or Gradle project that builds on a Spring Boot line below this architecture's
  floor up to it — the version bump, the renamed starters and test slices, the renamed
  configuration properties — and leaves the build green and the diff uncommitted. Use when
  `/arch-adopt` or `export` refused a project for its Spring Boot line, or when a project
  should move up before adopting. Explicit invocation only.
argument-hint: "[--ref <tag|sha|main>] [--source <local path>]"
disable-model-invocation: true
allowed-tools: Read, Write, Edit, Bash, Glob, Grep, AskUserQuestion
model: opus
---

# Platform Upgrade

Moves the project the session is rooted at from the Spring Boot line its build declares to the
one the Initializr serves today, because `ArchHook.java export` refuses a project below
`doctor.platform.min_line` and nothing else leads it there. The norms, exemplars and
architecture-test allowlist this `.claude/` ships are written for that floor and later.

**Two engines, in this order.** What is mechanical goes through a recipe that
`ArchHook.jar upgrade-recipe` writes from data — `doctor.platform.upgrade` of
`.claude/schemas/extensions.json` — and Spring's own metadata, and that the OpenRewrite core runs
through the project's own wrapper. What no rename covers is the guided residue (step 8), written
by you, one compile error at a time, against the norms. Never a recipe module under another
license: every artifact this procedure runs is Apache 2.0, and the data was written from what
this repository compiles, not from someone else's recipes.

**Never writes a version from memory.** The Spring Boot target is read from a project the
Initializr generates (step 3), the BOMs and library versions from the metadata it serves for that
target (step 3), the engine's version from the repository that serves it (step 4), a Gradle version
from the list Gradle publishes (step 5b), a dependency's version from where it is published
(step 8). No network → stop and ask.

**Compares, never judges, what was red.** The tests run once before anything changes (step 4b) and
once at the end (step 9); `ArchHook.jar test-diff` says which cases got worse. A red build that was red
before is reported as that — never as the upgrade's, and never fixed by editing a test.

**Writes the build and `src/**`, and never commits.** The diff is the person's to review, and
`git checkout -- .` is how they undo it.

## Procedure

### 1 · Refuse to write over uncommitted work

```bash
git rev-parse --is-inside-work-tree && git status --porcelain
```

Not a git repository, or the output is not empty → **stop**. The upgrade rewrites the build and the
sources; `git diff` is how the person reviews it and `git checkout` how they undo it. Say what to
run (`git init` and a first commit, or commit or stash what is pending). Don't offer to commit.

Then the tools, once: `java -version` must report a JDK that the project's build accepts, and the
build tool is the one whose file sits at the project root — `pom.xml` (Maven) or `build.gradle` /
`build.gradle.kts` (Gradle). Both present → ask which one builds the project. Its wrapper
(`./mvnw`, `./gradlew`) is what runs everything below; none → stop and say so. This skill never
adds a wrapper and never assumes a Maven or Gradle on `PATH`.

The test run of step 4b and the context run of step 8b start containers when the project's tests use
Testcontainers. Look for it (`grep -rl testcontainers` over the build file and `src/test`) and, when it
is there, `docker info`: a daemon that is down turns every one of those tests red for a reason that has
nothing to do with the upgrade. Say it before step 4b, and let the person start Docker or go on knowing
the baseline will record those cases as failing.

### 2 · Fetch the source

A project below the floor has no `ArchHook.jar` of this shape, so the mode that writes the recipe
comes from the source, fetched as `arch-adopt` § 2-3 does it: `$SRC` named once there, the
`source` block of the `extensions.json` it finds, `--ref` and `--source <path>` with the same
meaning, nothing about the URL written from memory. An adopted project that already has
`.claude/` fetches too: a later floor needs the later data.

The plugin that delivers this skill ships only this file, as it does for `arch-adopt`, and it can be
older than the tag just fetched: the jar, the data and the two Gradle init scripts all come from
`$SRC`. So the text follows them — run § 3b of `arch-adopt` now, with `platform-upgrade` as the running
skill. If it hands over, read `$SRC/.claude/skills/platform-upgrade/SKILL.md` and continue in that
file, from this step, without fetching again. The report's `Procedure` line says which text ran.
Everything this procedure downloads or writes outside the project goes in one directory:

```bash
WORK=${WORK:-/tmp/platform-upgrade}; mkdir -p "$WORK"
```

A ref older than this skill has no `upgrade-recipe` or `test-diff` mode, and an unknown mode exits 0
with one line on stderr — it would read as a success. So, before anything else:

```bash
grep -q 'upgrade-recipe' "$SRC/.claude/hooks/ArchHook.java" && grep -q 'test-diff' "$SRC/.claude/hooks/ArchHook.java"
```

Nothing found → stop and say that the fetched ref predates this skill; `--ref` names a newer one.

Read `doctor.platform.upgrade` of `$SRC/.claude/schemas/extensions.json` now. The keys named
below — `engine`, `recipes`, `test_starters` — are read from that file, never typed from this one.

### 3 · Resolve the target version

The Initializr is the version oracle. Generate a throwaway project into `$WORK` and read its
parent version:

```bash
mkdir -p "$WORK/initializr"
curl -sS --fail -L "<engine.initializr_starter>" -d type=maven-project -d language=java \
  | tar -xzf - -C "$WORK/initializr"
grep -m1 -A2 '<artifactId>spring-boot-starter-parent</artifactId>' "$WORK/initializr/pom.xml"
```

The version in the `<version>` line is `<target>`. No network, or the throwaway holds no version to read →
**stop and ask** the person for the version. `upgrade-recipe` checks its shape and that it is not
below the floor; it never chooses one.

The same service lists the BOMs and the libraries that carry their own version for that line — a
Spring Cloud train, Modulith, springdoc — which the Boot bump does not move:

```bash
curl -sS --fail -L -H "Accept: <engine.initializr_accept>" "<engine.initializr_dependencies>" -o "$WORK/initializr.json"
```

The file is for the Boot version the Initializr serves now; step 5 refuses it for any other. The
download failed → go on without it, and the report says the BOMs were not moved.

### 4 · Resolve the engine's version

Read both from the repository that serves them. Print the versions chosen, so the report can name
them.

**Maven.** `<release>` of `engine.maven_plugin_metadata`, read with `curl -sS --fail -L`. Central serves it
and everything it depends on.

**Gradle.** The Plugin Portal lists plugin versions that import a `rewrite-bom` Maven Central does
not serve, so the newest one does not resolve. Take the newest of the last
`engine.gradle_candidates` entries of `engine.gradle_plugin_metadata` whose POM
(`engine.gradle_plugin_pom`) names a `rewrite-bom` version that `engine.central_bom` answers 200
for. Every fetch follows redirects — the Plugin Portal answers some with one — so the metadata and the
POM are `curl -sS --fail -L`, and the BOM check is `curl -sSfIL`. None → stop: the engine's public
line moved, and `engine` is the block to edit.

### 4b · The baseline — what was red before the upgrade

Run the project's tests on the tree as the person left it, and record every case. Step 9 compares
against this; without it, a red build says nothing about who broke it. It is a full build — minutes —
and it writes only build output (`target/`, `build/`):

```bash
# Maven
./mvnw -B -fae clean verify -Dmaven.test.failure.ignore=true
# Gradle
./gradlew clean build --continue

CLAUDE_PROJECT_DIR="$SRC" java -jar "$SRC/.claude/hooks/ArchHook.jar" test-diff snapshot . --out "$WORK/baseline.json"
```

The build may fail — the exit code of the build is not the answer, the snapshot is. Exit 2 and "no
JUnit XML report" → the tree does not get as far as running its tests: there is no baseline. Say so, and
go on; step 9 then reports any red as it is.

### 5 · Pass 1 — the bump, the coordinates, the types

The project's line is read from its own build by the mode:

```bash
CLAUDE_PROJECT_DIR="$SRC" java -jar "$SRC/.claude/hooks/ArchHook.jar" upgrade-recipe . \
  --pass bump --target <target> --initializr "$WORK/initializr.json" --out "$WORK/bump.yml"
```

Leave `--initializr` out when step 3 did not download the file. Exit 2 and a message that the project is
already at or above the floor → say so and stop: there is nothing to upgrade. Any other exit 2 is shown
as it is — the file being for another Boot version included. The recipe's name is
`doctor.platform.upgrade.recipes.bump_name`. Run it through the project's wrapper:

```bash
# Maven
./mvnw -B <engine.maven_plugin>:<maven version>:run \
  -Drewrite.configLocation="$WORK/bump.yml" -Drewrite.activeRecipes=<bump_name>

# Gradle — copy $SRC/.claude/skills/platform-upgrade/templates/rewrite-init.gradle.example to $WORK/rewrite-init.gradle first
./gradlew --init-script "$WORK/rewrite-init.gradle" -Dnerviz.plugin.version=<gradle version> \
  -Dnerviz.recipe="$WORK/bump.yml" -Dnerviz.recipe.name=<bump_name> rewriteRun
```

The recipe runs against the classpath the project **still has**: that is why the type renames sit
here and not after the bump. Besides the bump it renames the coordinates, adds without a version the
starter a used type now needs (`requires_starter`), removes the version a renamed or added coordinate
carried, and moves each BOM and each library the Initializr file lists. `git diff --stat` must show the
build file changed. It did not → the
build declares its Spring Boot version where no step of the recipe reads it (a property in a
parent POM that is not this project's, a version catalog); name the file, ask the person to
change that one line, and run the step again. Never edit around it.

Then read the diff for what a recipe cannot see. A renamed or added coordinate carries **no version**
(`renames.dependencies`'s `to`, `requires_starter`'s values): the BOM manages them, and one left behind
overrides it — remove it by hand and say so. Each BOM of `$WORK/initializr.json` that the build declares
reads the version the file lists; one that does not (a version in a catalog, or computed in a script)
is set to it by hand.

Two more the recipe leaves as they are, and the diff shows:

- **A pin over a managed version.** A property or a plugin version the build sets by hand
  (`set('testcontainers.version', …)`, `ext['x.version']`, a plugin at an old `version`) is not touched:
  it overrides what the new BOM manages, and it can be the reason a later step fails. List each one in
  the report (`Pins`) with the value the Initializr's starter or the BOM carries, and ask before
  removing or raising any.
- **Gradle `AddDependency` in a build that declares its dependencies in `ext {}`.** The added starter
  can land in a second `dependencies {}` block after `ext {}` instead of the existing one. It works;
  merge it into the existing block if the build had one outside `ext {}`.

### 5b · The Gradle wrapper — before the new plugin configures anything

Gradle only. The bump put a Spring Boot plugin in the build that may refuse the wrapper's Gradle; every
`./gradlew` from here on configures it, and `./gradlew wrapper` would be refused the same way. Ask once:

```bash
./gradlew -q help
```

Green → nothing to change. Red, with a message that lists the Gradle lines the plugin accepts and names
the one running (`requires Gradle 8.x (8.14 or later) or 9.x. The current version is Gradle 8.10.2`) →
take the **lowest** accepted major, the smallest jump, and its newest release from
`engine.gradle_versions_all` (an entry with `final` true and `broken` false). Put it in the wrapper's own
properties, which no build configures, then let Gradle refresh the rest:

```bash
# gradle/wrapper/gradle-wrapper.properties — distributionUrl=<engine.gradle_distribution, {version} replaced>
./gradlew wrapper --gradle-version <that version>   # refreshes the scripts and the jar
./gradlew -q help                                    # must pass
```

`gradlew`, `gradlew.bat` and `gradle/wrapper/gradle-wrapper.jar` then show in `git diff`: they are
Gradle's output, not edits to review line by line. The report names them as that.

The message names no line → the `version` that `engine.gradle_current` returns. Never a version from
memory, and never a major jump the message did not ask for.

### 6 · The new classpath

Dependency resolution now sees the new BOM. List the jars it resolves — one file, every module:

```bash
# Maven — one file per module, joined with a newline between them
./mvnw -B -q dependency:build-classpath -Dmdep.outputFile=target/nerviz-classpath.txt
for f in $(find . -path '*/target/nerviz-classpath.txt'); do cat "$f"; echo; done > "$WORK/classpath.txt"

# Gradle — copy $SRC/.claude/skills/platform-upgrade/templates/classpath-init.gradle.example to $WORK/classpath-init.gradle first
rm -f "$WORK/classpath.txt"
./gradlew -q --init-script "$WORK/classpath-init.gradle" \
  -Dnerviz.classpath.out="$WORK/classpath.txt" nervizClasspath
```

A resolution failure here is the first signal that a dependency has no counterpart on the new line;
read the message, it names the artifact. That is step 8's, not a reason to stop.

### 7 · Pass 2 — the property renames

```bash
CLAUDE_PROJECT_DIR="$SRC" java -jar "$SRC/.claude/hooks/ArchHook.jar" upgrade-recipe . \
  --pass properties --classpath "$WORK/classpath.txt" --out "$WORK/properties.yml"
```

It reads the metadata each jar publishes and renames only what a jar itself declares an error with
a replacement. The count it prints is the number of **rules** it wrote, not of properties the project
had: how many the run changed is `git diff` over the configuration files, and that is what the report
counts. It writes nothing, and says so, when no jar declares one: skip the run. Otherwise run
it the way step 5 did, with `properties_name` for the recipe, and **without compiling**: the
sources do not compile until step 8, and the engine does not need them to rename a property.

```bash
# Maven — add:  -Dmaven.main.skip=true -Dmaven.test.skip=true
# Gradle — add: -x compileJava -x compileTestJava
```

### 8 · The guided residue

Compile, read the first errors, fix the cause, compile again:

```bash
./mvnw -B -q test-compile          # Maven
./gradlew -q compileTestJava       # Gradle
```

What recurs, and its owner:

| The error names | The cause | The fix |
|---|---|---|
| a package of a key of `test_starters` | the test slice moved to a module of its own | the test-scope dependency that key maps to, `group:artifact` and no version, in the module whose compile failed |
| `tools.jackson`, `JacksonException`, `com.fasterxml.jackson.databind`, a checked `JsonProcessingException` | Jackson 3 moved the core and made its exceptions unchecked; annotations stayed | `engine.migration_guide`, its Jackson section, then the code. The architecture test's allowlist says which roots the domain may import, not how to migrate |
| a third-party artifact the BOM no longer resolves, or a library built for the old line | the library moved on its own schedule | pass 1 already moved every one `$WORK/initializr.json` lists; any other, to the version Maven Central lists as `<release>` of that artifact, after reading its own notes |
| anything else | an API that changed shape | the project's own code is changed, minimally; `engine.migration_guide` says what changed and why |

**A green compile is not a migrated Jackson.** Jackson 2 stays on the classpath whenever a library
still brings it, so `com.fasterxml.jackson.databind` compiles and the row above never fires. After the
compile, `grep -rl 'com.fasterxml.jackson.databind' src` and, for the build tool in use,
`./mvnw -B dependency:tree -Dincludes=com.fasterxml.jackson.core` or
`./gradlew dependencyInsight --dependency jackson-databind`: a hit in `src` with Jackson 3 also resolved
is code still on Jackson 2. List the files in the report (`Not verified`); migrating them is a decision
per site, as the row says.

Two rules, no exceptions: **a test that fails is reported, never deleted, skipped or loosened**, and
**the same error three times in a row stops the loop** — say what was tried and ask.

### 8b · The context loads

Compiling proves the sources agree with the new jars, not that the application starts: a starter whose
auto-configuration moved out, a property no jar reads any more, a bean that now needs a module — all
compile, and all fail only when the context is built. Run first, and on their own, the test classes
annotated `@SpringBootTest` (`grep -rl '@SpringBootTest' src`) **and every concrete class that extends
one of them** — the annotation is inherited, so a subclass of an abstract base builds the context and the
base alone is never a test to run:

```bash
grep -rlE 'extends +<Base>\b' src/test                # per class found, until no new one appears
./mvnw -B -q test -Dtest='<Class>,<Class>' -Dsurefire.failIfNoSpecifiedTests=false   # Maven
./gradlew -q test --tests '<Class>' --tests '<Class>'                                # Gradle
```

Select **concrete** classes only, and read the surefire or Gradle report directory afterwards: Maven with
`failIfNoSpecifiedTests=false` exits 0 and writes nothing when the selection matched no test, which reads
as a green context and is the opposite. No report for a class you selected → the selection was wrong,
not the context.

Red → the first `Caused by` names the bean or the property; fix its cause and run again, under the same
three-strikes rule. A class that is `fail` in `$WORK/baseline.json` already failed before the upgrade
(often a database or broker that is not up): skip it here, step 9 reports it as pre-existing. No
`@SpringBootTest` class at all → the report says `Not verified: context load`; do not write one.

### 9 · Verify

```bash
./mvnw -B -fae clean verify -Dmaven.test.failure.ignore=true   # Maven
./gradlew clean build --continue                               # Gradle

CLAUDE_PROJECT_DIR="$SRC" java -jar "$SRC/.claude/hooks/ArchHook.jar" test-diff compare . --baseline "$WORK/baseline.json"
```

`clean` first, always: a report left by step 4b would otherwise read as this run's. Build and compare
green → continue. Compare exit 2 → the regressions, the missing tests and the new failures it lists are
the report, with the first error of each; nothing is committed, and a missing test is never answered by
restoring it from the baseline's side. Only pre-existing failures → report them as that: the project was
red before the upgrade and is no redder. No baseline (step 4b) → the failing tests and the first error
are the report. A compile error and no report → that error is.
When the project already has `.claude/hooks/ArchHook.jar`, run `java -jar .claude/hooks/ArchHook.jar
doctor` too and put its `Platform` line in the report.

### 10 · Hand the diff over

`git status --short` and `git diff --stat`. Do **not** commit. Print the next command for the person
to type: `/arch-adopt` — now the project is at or above the floor, and a project that never had this
`.claude/` is adopted by it.

## Report

```
✅ upgraded — <from line> → <target>, <Maven | Gradle>

Source ....... <base_url host>, ref <ref>
Procedure .... <the running text | the fetched text — arch-adopt § 3b>
Engine ....... <engine artifact> <version>
Baseline ..... <n> test cases, <n> failing before | none — the tree ran no tests
Pass 1 ....... <n> files changed (<n> sources, <n> build)
BOMs ......... <n> moved by the recipe, <n> by hand | not moved — no Initializr metadata
Wrapper ...... <unchanged | Gradle <from> → <to>, gradlew · gradlew.bat · wrapper jar are Gradle's output> (Gradle only)
Pins ......... <each override of a managed version and the value the BOM carries | none>
Pass 2 ....... <n> properties renamed in the configuration files (git diff) | none declared by the jars
Residue ...... <n> edits by hand — <one line each>
Context ...... <n> @SpringBootTest classes green | Not verified: context load
Verify ....... <green | no worse than the baseline: <n> pre-existing | the regressions, verbatim first line>
Not verified . <what no step above ran — one line each | none>

Review: git diff · Undo: git checkout -- .
Next: /arch-adopt
```

## Why this is a manually-invoked skill

Form 2 (`disable-model-invocation: true`): it rewrites a person's build and sources, so it may only
run when they ask for it by name — axis 2 of the interview. The closest rejected form was a step
inside `arch-adopt`: that skill runs remote content and travels into every project with a territory
of `.claude/`, and widening it to `src/**` would give the one skill that fetches the whole tree the
right to rewrite the whole project. The mechanical part is deliberately **not** here — it is
`ArchHook.jar upgrade-recipe`, Form 7c, because the same input has to produce the same recipe and
a test has to be able to hold it; for the same reason the comparison of the tests is `ArchHook.jar test-diff`
and not the model reading report directories. (`@.claude/decisions/0175-platform-upgrade-below-the-floor.md`,
`@.claude/decisions/0176-platform-upgrade-baseline-context-and-runtime-starters.md`)

Pinned to `opus`: it edits code it did not write and decides what a compile error means (`@.claude/decisions/0081-skill-model-required-per-class.md`).

## Contract

**Class:** build — the territory is `skill_classes.build`'s override for this skill in
`@.claude/schemas/extensions.json`: the root build file, the wrapper files and `src/**`, at the
project root and under any module. `ArchHook.java guard` enforces it.

**Unfiltered Bash:** the upgrade fetches (`curl`, `tar`, `git ls-remote`), runs the project's own
wrapper — whose goals and tasks are the project's, not a fixed list — and the mode. Writes stay
under `guard` and `guard bash`, and a force push is blocked by `guard bash` (`guard.force_push`).

**Reads** `doctor.platform` of `.claude/schemas/extensions.json` in the fetched source — the
floor, the line patterns and the whole `upgrade` block — the project's build files, `src/**` and the
JUnit reports its own build writes, and what the Initializr, Gradle and the engine's repositories serve.

**Writes** the build file, wrapper files and `src/**` of the project, and `$WORK/**` outside it.
Never `.claude/**`: that is `/arch-adopt`'s.

**Refuses** a dirty worktree, a directory that is not a git repository, a project already at or
above the floor, and a build with no wrapper. Never commits, and never deletes, skips or loosens a
test.

**Travels into the project** (`export.skills.include`): a later floor raise sends an adopted project
here, and the plugin that delivered it may be gone by then.

**Hands off to** `/arch-adopt`, typed by the person once the diff is reviewed.
