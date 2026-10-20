---
name: iru-java-javadoc
description: Audit given Java class(es) for complete Javadoc coverage — class/interface/enum-level doc, every field/constant, every constructor/method (including private ones and any inner/nested class or enum constant), and a `package-info.java` with a brief description for every package touched (creating one if it's missing) — generate any missing or incomplete Javadoc grounded in the actual code and current changes, then run the project's Javadoc build goal to confirm the generated Javadoc is well-formed and builds without warnings/errors. Invoke as `/iru-java-javadoc <ClassName1,ClassName2,...>` (or file paths), or `/iru-java-javadoc` with no argument to scope to classes touched by uncommitted changes plus commits on the current branch not yet on the base branch. Works against any Java/Maven project — it discovers the project's own Javadoc conventions and enforcement level rather than assuming a fixed style. Use whenever the user wants Javadoc completeness checked and filled in for specific classes, instead of relying on a full site/lint build to surface gaps.
model: sonnet
---

# Java Javadoc

Make sure a set of Java classes — and the package(s) they live in — carry complete, well-formed Javadoc, filling
in whatever is missing, then prove the result actually builds via the project's Javadoc tooling. This skill only
adds/completes documentation comments (including creating a missing `package-info.java`) — it does not change
behavior, signatures, or non-Javadoc code. Test classes are out of scope for documentation requirements — they
don't need class/member-level Javadoc added, even if named explicitly — but any Javadoc a test class already has
must be left as-is; never strip or "clean up" existing comments in test code. It makes no assumptions about this
being any particular repository — discover the project's actual conventions and build setup fresh each run.

## Step 1 — Determine scope

- **Argument provided** (comma-separated class names or file paths): resolve each to its file. If given a simple
  class name, locate it via `find`/`grep` across the whole project (main and test source roots) rather than
  guessing the package. If a resolved file turns out to live under the project's test source root (`src/test/java`
  by convention), drop it from the scope audited/generated in Steps 2-5 — say so in the Step 7 report rather than
  silently ignoring it — since test classes carry no Javadoc requirement here.
- **No argument**: default to every main-source `.java` file touched by uncommitted changes plus commits on the
  current branch not yet on the base branch, same approach as the `iru-update-docs` skill:
  ```bash
  git status
  git diff <base-branch>...HEAD --name-only
  git diff --name-only
  ```
  (determine the base branch via `git symbolic-ref refs/remotes/origin/HEAD` or `git branch -a` if unclear; ask
  the user only if genuinely ambiguous). Filter the changed-file list to the project's main Java source root —
  skip test code, build-generated files, and non-Java files.
- If the resulting scope is empty (no argument and no relevant changes), tell the user there is nothing to
  document and stop.
- From the in-scope class files, derive the distinct set of packages involved (each file's `package` declaration)
  — these feed Step 4, which checks each one has its own `package-info.java`.

## Step 2 — Discover this project's actual Javadoc bar before auditing

Don't assume a fixed documentation scope — discover it from the project itself, since projects vary on whether
private members need Javadoc:

- Check for a contributor guide (`CLAUDE.md`, `AGENTS.md`, a top-level `README`, or a `CONTRIBUTING` file) for any
  stated Javadoc convention.
- Check for a Checkstyle config (commonly referenced from `pom.xml`'s `maven-checkstyle-plugin` configuration,
  e.g. `checkLocation`/`configLocation`) for `JavadocType`, `JavadocMethod`, and `JavadocVariable` modules — read
  their `scope` property if set (`public`, `protected`, `package`, or `private`); if the property is absent, the
  check's own default scope applies (consult the Checkstyle version in use if it matters).
- Check the `maven-javadoc-plugin` configuration in `pom.xml` for a `<show>` setting (`public`/`protected`/
  `package`/`private`), which controls what the generated site actually exposes.
- If none of the above give a clear answer, skim 2-3 existing classes near the ones in scope to see empirically
  whether private fields/methods already carry Javadoc there — treat that observed practice as the bar, since a
  stated convention that's looser than what the codebase actually does would leave real gaps unaddressed.
- Reconcile any conflict between a stated convention and the actually-enforced/observed one by following the
  stricter of the two, so this skill's output would pass the project's own lint/build checks.

Skim a couple of existing, well-documented classes/interfaces/enums in the project (prefer ones structurally
similar to what's in scope) to internalize the exact phrasing conventions before writing new Javadoc: person and
tense used, whether sentences end in a period, how `@param <T>` is used for generic type parameters, the ordering
of `@param`/`@return`/`@throws`, and whether blank lines appear inside a Javadoc comment block. If the project has
no existing Javadoc to learn from, fall back to standard Javadoc conventions (third person, present tense,
`@param`, `@return`, `@throws` in that order, one sentence summary first).

## Step 3 — Audit each in-scope class

Read the full file, then check every one of the following is present, non-empty, and actually describes the
member's purpose (not just restates its name), scoped per the bar established in Step 2:

- **Type-level**: a doc comment on the class/interface/enum/annotation itself, including `@param <T>` for each
  generic type parameter declared on the type.
- **Fields and constants**: every field and `static final` constant within the discovered scope.
- **Constructors**: every constructor within scope, with `@param` for each parameter and `@throws` for any
  exception the constructor can throw, per this project's own argument-validation convention (if one is stated or
  observed in Step 2).
- **Methods**: every method within scope, with `@param` per parameter, `@return` unless `void`, and `@throws` for
  every checked exception and any documented unchecked exception.
- **Enum constants**: a doc comment on each constant.
- **Nested/inner classes, interfaces, enums**: recurse into these with the same checks as top-level types.
- **`@Override` methods**: only require their own Javadoc if Step 2 found this project actually documents
  overrides (rather than relying on `{@inheritDoc}` or inherited docs) — follow whichever this project does.

For each item found incomplete or missing entirely, record: the member, what's missing (whole comment vs. a
missing `@param`/`@return`/`@throws` tag), and its current visibility.

## Step 4 — Ensure each touched package has a `package-info.java`

Most Javadoc/Checkstyle setups expect a `package-info.java` per package. For each package derived in Step 1:

- If `package-info.java` already exists in that package's directory, read it and check it has a non-empty
  `/** ... */` package doc comment above the `package` declaration (not just a license/file header) — treat a
  missing or placeholder-only comment the same as a missing file.
- If it's missing or the doc comment is absent/placeholder-only, create/complete it. Look for another
  `package-info.java` anywhere else in the project to copy its format (file header if the project prepends one to
  every source file, comment style, level of detail); if none exists anywhere in the project, use whatever file
  header convention regular source files in this project use (if any), followed by a plain package Javadoc
  comment and the `package <name>;` declaration — no class body, this file only ever contains an optional header,
  the doc comment, and the package declaration.
- Base the description on what the package's classes actually do: for a brand-new package, summarize the
  in-scope classes' responsibilities; for an existing package gaining new in-scope classes, extend the current
  description if the new classes introduce a concept not yet mentioned, otherwise leave an already-accurate
  description untouched. Match the level of detail of other `package-info.java` files already in the project, if
  any exist (e.g. a short overview paragraph, plus a list of concrete classes/entry points when the package has
  more than one).

## Step 5 — Generate the missing Javadoc

For every gap found in Step 3, write the Javadoc directly grounded in:

- The member's actual implementation (parameter usage, return expression, thrown exceptions) — read the method
  body, don't infer purely from the signature/name.
- Any current uncommitted/branch changes to that member (`git diff` / `git log -p` for that file/hunk if the
  member was just added or modified) — if the change altered behavior, the new Javadoc must describe the current
  behavior, not stale prior behavior a name alone might suggest.
- The phrasing conventions gathered in Step 2 — match voice, tense, and tag ordering/style exactly so the new
  comments are indistinguishable from hand-written ones in this codebase.

Apply the edits with the Edit tool. Do not modify code logic, signatures, formatting outside the added comments,
or reorder members — this skill only adds/completes Javadoc comments.

## Step 6 — Verify the Javadoc actually builds

Determine how this project builds Javadoc: check `pom.xml` for a `maven-javadoc-plugin` declaration (in
`<build><plugins>` and/or `<reporting><plugins>`) and any contributor-guide command that already names a Javadoc
goal (e.g. a full local-verification command). Prefer running the narrowest goal that actually generates and
validates Javadoc output without a full site build:

```bash
mvn javadoc:jar
```

Fall back to `mvn org.apache.maven.plugins:maven-javadoc-plugin:jar` if the plugin isn't bound to a lifecycle
phase under a short goal prefix, or to `mvn javadoc:javadoc` if only the report goal is configured. This mirrors
how a dedicated code-quality skill would invoke a static-analysis plugin directly rather than through a full site
build, since only Javadoc generation is being checked here. It fails the build on malformed Javadoc (unclosed
tags, bad HTML, broken `{@link}` references) — read any reported warnings/errors, they name the exact file and
line.

If it fails or warns, fix the offending comment(s) and re-run until it succeeds with no warnings tied to files in
scope. Warnings in files outside the current scope are pre-existing — note them in the report but don't fix them
unless the user asks.

## Step 7 — Report

Per class in scope, state: how many members were already fully documented, how many gaps were found and filled
(name each), and the final Javadoc build result. Separately, state per package whether its `package-info.java`
already existed and was complete, was extended, or was newly created. If any argument resolved to a test class
(Step 1), name it and note it was excluded since test classes carry no Javadoc requirement here. If any
out-of-scope pre-existing Javadoc warning surfaced in Step 6, mention it separately as a follow-up rather than
silently leaving it out of the report.

Do not run a full site/lint build, fix static-analysis issues unrelated to Javadoc, or add/modify tests — those
are a separate quality/implementation skill's job, if this project has one.
