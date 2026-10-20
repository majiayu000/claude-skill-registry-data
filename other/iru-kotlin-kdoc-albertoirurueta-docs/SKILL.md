---
name: iru-kotlin-kdoc
description: >-
  Audit given Kotlin class(es)/file(s)/package scope in a JVM Kotlin project (plain library, Kotlin Spring Boot, or Kotlin Quarkus — not Android, which `iru-android-dokka` covers) for complete KDoc coverage — type-level docs, primary-constructor parameters (`@property` for declared properties, `@param` for plain parameters, `@constructor` where construction has its own behavior), every function and property within the discovered visibility bar (including Spring beans' and Quarkus CDI beans' public methods, `@ConfigurationProperties`/`@ConfigMapping` properties, and data classes' properties), enum entries, companion-object members, top-level and nested declarations — required tags `@param`/`@return`/`@throws`/`@see`/`@sample`, `@suppress` honored, and Dokka module/package includes (`module.md` with `# Module`/`# Package` sections) wired for every module/package touched (creating them if missing) — generate any missing or incomplete KDoc grounded in the actual code and current changes, then run the project's Dokka build to confirm the KDoc is well-formed: Gradle `org.jetbrains.dokka` (Dokka 2 `dokkaGenerate`/`dokkaGeneratePublicationHtml`, or Dokka 1 `dokkaHtml`, wrapper preferred, Kotlin DSL or Groovy) or Maven `org.jetbrains.dokka:dokka-maven-plugin` (`dokka:dokka`). Invoke as `/iru-kotlin-kdoc <scope>` where `<scope>` is a comma-separated list of class names, file paths, or a package glob, or `/iru-kotlin-kdoc` with no argument to scope to Kotlin files touched by uncommitted changes plus commits on the current branch not yet on the base branch. Discovers the project's own documentation bar (detekt `comments` rules, Dokka `documentedVisibilities`/`reportUndocumented`, contributor guides, observed practice) rather than assuming a fixed style. Use whenever the user wants KDoc completeness checked and filled in for specific Kotlin classes/modules, instead of relying on a Dokka run to surface gaps (Dokka does not fail on undocumented members by default).
model: sonnet
allowed-tools: Read Edit Write Bash(mvn *) Bash(./mvnw *) Bash(gradle *) Bash(./gradlew *) Bash(git status *) Bash(git diff *) Bash(git log *) Bash(git symbolic-ref *) Bash(git branch *) Bash(find *) Bash(grep *) Bash(ls *)
---

# Kotlin KDoc

Make sure a set of Kotlin declarations — and the module(s)/package(s) they live in — carry complete, well-formed
KDoc, filling in whatever is missing, then prove the result builds via the project's own Dokka tooling. This skill
only adds/completes documentation comments (including creating missing module/package include files and wiring
them into the Dokka configuration) — it does not change behavior, signatures, or non-KDoc code. Test sources
(`src/test/kotlin`, `src/test/java`, `src/integrationTest/**`, `src/testFixtures/**`) carry no KDoc requirement —
don't add KDoc there even if named explicitly — but never strip or "clean up" KDoc a test class already has. Java
files in a mixed module are out of scope here (use `iru-java-javadoc`); Android modules (an Android Gradle plugin
applied) belong to `iru-android-dokka`, and Kotlin Multiplatform modules (the `kotlin("multiplatform")` plugin
applied) to `iru-kmp-dokka`. Make no assumptions about the repository — discover its conventions and
Dokka setup fresh each run.

## Step 1 — Determine scope and build tool

- **Build tool**: Gradle when `settings.gradle(.kts)`/`build.gradle(.kts)` exists (`./gradlew`, or `gradlew.bat`
  on Windows, when the wrapper exists, else `gradle`); Maven when `pom.xml` exists (`./mvnw`/`mvnw.cmd` when
  present, else `mvn`). If both exist, use whichever the CI workflow or contributor guide invokes; ask only if
  neither says.
- **Argument provided** (comma-separated class names, file paths, or a package glob): resolve each to its file. For
  a simple class/object name, locate it with `find`/`grep` across every module's main source roots
  (`src/main/kotlin` and `src/main/java` — Kotlin files may live in either) rather than guessing the module or
  package. A file under a test source root is dropped from Steps 3-6 and named in the Step 7 report; a `.java` file
  is dropped with a pointer to `iru-java-javadoc`.
- **No argument**: every main-source `.kt` file touched by uncommitted changes plus commits on the current branch
  not yet on the base branch, the same approach as `iru-update-docs`:
  ```bash
  git status
  git diff <base-branch>...HEAD --name-only
  git diff --name-only
  ```
  (determine the base branch via `git symbolic-ref refs/remotes/origin/HEAD` or `git branch -a`; ask the user only
  if genuinely ambiguous). Keep only `.kt` files under a main source root — skip tests, `build/`/`target/` output
  (including generated sources such as OpenAPI/jOOQ/KSP/kapt output), `.kts` build scripts, and non-Kotlin files.
- Empty scope (no argument and no relevant changes) → tell the user there is nothing to document and stop.
- From the in-scope files derive the distinct modules (the Gradle project or Maven module directory owning each
  file) and packages (each file's `package` declaration) — they feed Step 4 and Step 6.

## Step 2 — Discover this project's actual KDoc bar before auditing

Projects vary on whether `internal`/`protected`/`private` members need KDoc — discover it, don't assume it:

- Contributor guides (`CLAUDE.md`, `AGENTS.md`, `README`, `CONTRIBUTING`) for any stated KDoc convention.
- A detekt config (`detekt.yml`/`detekt.yaml`, `config/detekt/detekt.yml`, or whatever the Gradle
  `detekt { config.setFrom(...) }` / Maven `<config>` points to): the `comments` rule set's
  `UndocumentedPublicClass`, `UndocumentedPublicFunction`, `UndocumentedPublicProperty` (`active`, plus
  `searchInNestedClass`/`searchInInnerClass`/`searchInInnerObject`/`searchInProtectedClass` overrides) and
  `OutdatedDocumentation` (requires `@param`/`@property` tags to match the actual parameters — when active, a stale
  or missing tag is a gap even on an otherwise documented declaration). No config, or none of these active, gives
  no enforced bar from this source.
- The Dokka configuration: Gradle `dokka { dokkaSourceSets.configureEach { documentedVisibilities(...) } }`
  (Dokka 2) or `dokkaSourceSets { configureEach { documentedVisibilities.set(...) } }` (Dokka 1); Maven
  `<documentedVisibilities>`/`<includeNonPublic>`. Default is `PUBLIC` only; anything wider (`INTERNAL`,
  `PROTECTED`) is published and therefore in scope. Also note `reportUndocumented` (Gradle source-set option /
  Maven `<reportUndocumented>`): when the project sets it, Dokka itself lists undocumented declarations in Step 6
  — use those warnings as a cross-check of Step 3, but never turn it on yourself.
- If none of these answer it, skim 2-3 existing classes near the ones in scope to see whether the project
  documents `internal`/`private` members or only public ones, and treat observed practice as the bar.
- On conflict between a stated/configured convention and observed practice, follow the **stricter** one.

Skim a couple of well-documented, structurally similar declarations in the project to internalize its phrasing
before writing: person and tense, whether summaries end in a period, `@param`/`@return`/`@throws` ordering, use of
`[Declaration]` links vs. backticked names. With nothing to learn from, fall back to standard KDoc convention:

- **Summary first**: one concise sentence, third person present tense, then a blank KDoc line and any longer
  explanation.
- **`@param name description`** — KDoc's form (no hyphen, no `{type}`), one per function/plain constructor
  parameter, in declaration order; `@param T description` for each generic type parameter.
- **`@property name description`** — for every `val`/`var` declared in a primary constructor, including every
  property of a `data class`, instead of `@param` (Dokka renders them as documented properties).
- **`@constructor description`** — on a class whose primary constructor does something worth stating beyond
  assigning properties (an `init` block that validates arguments, registers listeners, or opens resources);
  omitted for plain holders.
- **`@return description`** — omitted for `Unit`.
- **`@throws ExceptionType description`** (`@exception` is an alias — keep whichever the project uses) — one per
  exception the implementation actually throws (including `require`/`check`/`error` →
  `IllegalArgumentException`/`IllegalStateException`) or declares via `@Throws(...)`.
- **`@see Declaration`** for a worthwhile cross-reference; **`[Declaration]`** links in prose.
- **`@sample fqn.of.sampleFunction`** only where the project already keeps runnable samples (and wires them via
  Dokka `samples`); never invent a sample function to satisfy the tag.
- **`@suppress`** carried over verbatim on members intentionally hidden; never add it new — if an existing
  `@suppress` looks like a mislabeled omission, flag it in the report.

## Step 3 — Audit each in-scope declaration

Read the full file, then check every item below is present, non-empty, and actually describes purpose and
behavior (not a restatement of the name), scoped per Step 2's bar:

- **Type-level**: class/interface/object/enum/annotation/sealed type/`typealias`, with `@param T` per type
  parameter.
- **Primary constructor**: `@property`/`@param` per parameter, `@constructor` where Step 2's rule applies,
  `@throws` for validation the constructor/`init` performs.
- **Secondary constructors**: documented like functions, one block per overload.
- **Properties**: every `val`/`var` in scope, including `lateinit var`, `const val`, and properties with custom
  accessors whose behavior isn't obvious from the type.
- **Functions**: top-level, member, extension, operator, infix, and `suspend` functions — `@param` per parameter
  (including the extension receiver's role, described in the summary), `@return` unless `Unit`, `@throws` per
  thrown exception. For `suspend` functions or ones returning `Flow`/`Mono`/`Uni`, state blocking/dispatcher or
  emission semantics only when the implementation makes them non-obvious.
- **Enum entries**, **companion-object members**, **nested/inner types** (recurse with the same checks).
- **Overrides**: require their own KDoc only if Step 2 found the project documents overrides; otherwise Dokka
  inherits the supertype's KDoc — follow the project.
- **`@suppress`-tagged members**: excluded from gaps, recorded as "suppressed".

Framework-specific checks (apply only when the framework is actually present in the file):

- **Spring beans** (`@Service`, `@Component`, `@Repository`, `@RestController`/`@Controller`, `@Configuration`):
  every public method is public API — document it. For web handlers, describe the request it handles, what each
  `@PathVariable`/`@RequestParam`/`@RequestBody` parameter means, the response, and `@throws` for exceptions that
  surface as error responses (via `@ResponseStatus` or an `@ExceptionHandler`/`@ControllerAdvice` mapping). For
  `@Bean` factory methods, describe the bean produced and why it's configured that way. For `@Transactional`/
  `@Cacheable`/`@Async` methods, mention the transactional/caching/async contract when callers depend on it.
- **Configuration holders**: `@ConfigurationProperties` classes (often `data class`es) need `@property` per
  property including its unit and default; Quarkus `@ConfigMapping` interfaces need KDoc on each accessor
  (it is the property's documentation) and on `@WithDefault` values' meaning.
- **Quarkus CDI beans** (`@ApplicationScoped`, `@Singleton`, `@RequestScoped`) and **JAX-RS resources**
  (`@Path`): same treatment as Spring beans and handlers.
- **JPA/Panache entities**: document the entity and each persistent property (including `lateinit var` and
  relationship properties — state the owning side/fetch semantics if non-obvious); a Panache
  `companion object : PanacheCompanion<…>`'s finder methods are public API.

For each gap record: the declaration, what's missing (whole comment vs. a specific tag), and its visibility.

## Step 4 — Ensure each touched module and package has narrative docs

Dokka takes module/package documentation from Markdown files listed as `includes`, not from per-package source
files (there is no `package-info.kt`). For each module from Step 1:

- Find the existing wiring:
  - **Gradle, Dokka 2**: `dokka { dokkaSourceSets.configureEach { includes.from("module.md") } }` (or
    `named("main") { … }`) in the module's build script or a convention plugin.
  - **Gradle, Dokka 1**: `tasks.dokkaHtml { dokkaSourceSets { configureEach { includes.from("module.md") } } }`
    (or `tasks.withType<DokkaTask>().configureEach { … }`); Groovy uses the same blocks with `includes.from('…')`.
  - **Maven**: `<includes><include>module.md</include></includes>` in the `dokka-maven-plugin` `<configuration>`.
- Read every listed file and confirm it has a `# Module <module-name>` heading with a real description (the name
  must match Dokka's module name — Gradle project name / Maven `<moduleName>`, default `${project.artifactId}`)
  and a `# Package <fully.qualified.name>` section with a non-empty description for each touched package —
  combined in one file or split across several, whichever the project already does.
- Missing wiring, file, or heading → create/complete it: a `module.md` at the module root summarizing what the
  module provides (from the in-scope classes' actual responsibilities), plus a `# Package <fqn>` section per
  touched package that lacks one. If the includes wiring is absent, add it with the Edit tool to the module's
  existing Dokka configuration block in the shape for that Dokka version/build tool above — the only build-file
  edit this skill makes, since an unwired file is silently ignored. If Dokka isn't applied to the module at all,
  don't add the plugin: write the file, report that Dokka is not configured, and skip Step 6 for that module.
- For an existing package gaining new classes, extend its description only if they introduce a concept not yet
  mentioned; leave an accurate description untouched.

## Step 5 — Generate the missing KDoc

For every gap from Steps 3-4, write KDoc grounded in:

- The actual implementation — read the body (parameter usage, return expression, thrown exceptions, guard
  conditions, the expression a custom getter evaluates, the annotations that change runtime behavior); never
  infer from the signature or name alone.
- Current uncommitted/branch changes to that declaration (`git diff`, `git log -p` for the file) — describe current
  behavior, not what the code used to do.
- The phrasing conventions from Step 2, so new comments are indistinguishable from the project's own.

Apply edits with the Edit tool. Do not modify code logic, signatures, annotations, imports, formatting outside the
added comments, or member order.

## Step 6 — Verify the KDoc actually builds

Run the narrowest Dokka task that generates the site for the in-scope module(s), once per module (or with several
task paths in one Gradle invocation):

**Gradle** — first identify the Dokka generation: `org.jetbrains.dokka` 2.x in Dokka Gradle Plugin V2 mode (the
default from 2.1; opted into on 2.0 via `org.jetbrains.dokka.experimental.gradle.pluginMode=V2Enabled` in
`gradle.properties`) registers `dokkaGenerate`/`dokkaGeneratePublicationHtml`; Dokka 1.x, or 2.x with
`pluginMode=V1Enabled`, runs `dokkaHtml` (and `dokkaHtmlMultiModule` at an aggregating root). Confirm with
`./gradlew :<module>:tasks --all | grep -i dokka` — in V2 mode the V1 tasks are still listed but described as
`[⚠ V1 tasks disabled]`, so a listed `dokkaHtml` alone doesn't mean V1 mode; pick `dokkaGeneratePublicationHtml`
whenever it is registered.

```bash
./gradlew :<module>:dokkaGeneratePublicationHtml   # Dokka 2 (V2 mode): HTML only
./gradlew :<module>:dokkaGenerate                  # Dokka 2 fallback: every configured publication
./gradlew :<module>:dokkaHtml                      # Dokka 1 / V1 mode
```

Retry once with `--no-configuration-cache` if a run fails on a configuration-cache error (a known rough edge of
some Dokka versions) and note that the project needs it.

**Maven** — the plugin needs the module's compile classpath, so build upstream reactor modules in the same run:

```bash
./mvnw -B -pl <modules> -am compile org.jetbrains.dokka:dokka-maven-plugin:dokka
```

(single-module project: `./mvnw -B compile org.jetbrains.dokka:dokka-maven-plugin:dokka`). Output lands in
`<module>/target/dokka` unless `<outputDir>` overrides it.

**Reading the result**: Dokka fails only on structural problems (unparseable KDoc, a broken source-set
configuration, an include file it can't read) — and on warnings only when `failOnWarning` is set (Gradle
source-set option / Maven `<failOnWarning>`). Otherwise a successful exit can still hide problems: read the
console for `Couldn't resolve link: [X] in <File>.kt/<fqn.member>` warnings (Gradle V2 prefixes them
`w: [:<task>] `; Gradle V1 prints them bare; Maven as `[WARNING]`), Maven's closing
`Generation completed with N warnings and M errors` line (Gradle prints no such summary — count the lines), plus `Undocumented: <pkg>/<Class>/<member>/` lines when
the project enables `reportUndocumented`. Fix every warning tied to an in-scope file and re-run until none remain;
warnings in out-of-scope files are pre-existing — report them, don't fix them unless asked.

**A clean Dokka run does not prove completeness** — unless `reportUndocumented` is on, an undocumented declaration
renders with just its signature, silently. Step 3's audit is the completeness gate; Step 6 proves the KDoc that
exists is well-formed and its links resolve.

## Step 7 — Report

Per file/class in scope: how many declarations were already fully documented, how many gaps were found and
filled (name each), and how many were `@suppress`-tagged and excluded. Per module/package: whether its
`module.md`/`# Package` coverage already existed and was complete, was extended, or was newly created, and whether
includes wiring had to be added. Then the Dokka result per module (pass with zero in-scope warnings, or the exact
warning/error text and declarations), the Dokka version/mode and task used, and the output location. Name any
argument dropped as a test file, Java file, or Android module, and list out-of-scope pre-existing Dokka warnings
separately as a follow-up.

Do not fix detekt/ktlint findings unrelated to KDoc, add or modify tests, or apply/configure the Dokka plugin where
it isn't already applied — those belong to `iru-kotlin-code-quality`, the coding/test skills, and the user.

## Known quirks / verification notes

- **Maven path verified locally** (Maven 3.9, JDK 25, Kotlin 2.4.21, `dokka-maven-plugin` **2.2.0**) in
  `$TMPDIR/iru-verify/kotlin/iru-kotlin-kdoc/`: `compile org.jetbrains.dokka:dokka-maven-plugin:dokka` generated
  `target/dokka/index.html`; `<includes><include>module.md</include></includes>` rendered the `# Module` text on
  the index; `@property`/`@constructor`/`@throws` rendered on the class pages; an unresolved `[NoSuchThing]` link
  produced `[WARNING] Couldn't resolve link: …` with `Generation completed with 2 warnings and 0 errors` and
  **BUILD SUCCESS** (warnings never fail without `failOnWarning`); `<reportUndocumented>true</reportUndocumented>`
  added `[WARNING] Undocumented: com.example.demo/Plain/undocumented/#kotlin.Int/` lines. `reportUndocumented` and
  `failOnWarning` have no Maven user property — they can only come from the pom. A two-module reactor confirmed
  `-pl <module> -am compile …:dokka` builds the parent plus the named module and writes only
  `<module>/target/dokka`.
- **Gradle path verified** in Docker (`gradle:8-jdk21`, Gradle 8.14.6, Kotlin JVM plugin 2.4.21) under
  `$TMPDIR/iru-verify/kotlin/iru-kotlin-kdoc-gradle/`: with `org.jetbrains.dokka` 2.2.0 (and 2.1.0) and no
  `gradle.properties` switch, V2 mode is the default — `dokkaGenerate`, `dokkaGenerateHtml`,
  `dokkaGenerateModuleHtml`, `dokkaGeneratePublicationHtml` registered, V1 tasks listed as disabled;
  `dokkaGeneratePublicationHtml` with `dokka { dokkaSourceSets.configureEach { includes.from("module.md");
  reportUndocumented.set(true) } }` wrote `build/dokka/html/index.html` (module text rendered) and printed
  `w: [:dokkaGeneratePublicationHtml] Couldn't resolve link: …` / `… Undocumented: com.example.demo/Plain/ (jvm)`
  with **BUILD SUCCESSFUL**. With `org.jetbrains.dokka.experimental.gradle.pluginMode=V1Enabled`, `dokkaHtml` and
  the `tasks.dokkaHtml { dokkaSourceSets { configureEach { includes.from(...) } } }` DSL worked, output also in
  `build/dokka/html`. Not verified: Groovy DSL, multi-module aggregation (`dokkaHtmlMultiModule`/V2 aggregate),
  Dokka 2.0 opt-in. A `dokkaPublications.html { outputDirectory.set(...) }` override moves the output — confirm the
  path from the build files.
- Look up the current Dokka version at run time (Maven Central `org/jetbrains/dokka/dokka-maven-plugin`, Gradle
  plugin portal `org.jetbrains.dokka`); October 2026 fallback: **2.2.0** (2.3.0 was still in Beta).
- `suppressInheritedMembers` (Gradle source-set option / Maven `<suppressInheritedMembers>`) hides inherited
  members from the site — when set, don't flag inherited-but-undocumented overrides as gaps.
- Kotlin compiler plugins common in Spring/Quarkus (`kotlin-spring`/all-open, `kotlin-jpa`/no-arg) don't affect
  Dokka output — a class opened by all-open is still documented as declared in source.
