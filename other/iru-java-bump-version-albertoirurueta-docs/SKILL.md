---
name: iru-java-bump-version
description: >-
  Set a JVM (Java or Kotlin) project's version to an exact value, for Maven or Gradle builds. Maven — for a
  single-module `pom.xml`, rewrites the root artifact's own `<version>` element in place (the first `<version>` that
  is a direct child of `<project>`, never the `<parent>`'s version or a dependency/plugin's version); for a Maven
  reactor (the root `pom.xml` declares `<modules>`), instead runs `mvn versions:set -DnewVersion=<new-version>
  -DgenerateBackupPoms=false` so every module and parent reference updates consistently in one step. Gradle (Kotlin
  DSL or Groovy, wrapper preferred — e.g. a Kotlin Spring Boot or Quarkus service, or a plain JVM library) — finds
  every place the project version is declared as a literal (`version=` in `gradle.properties`, `version = "…"` /
  `version '…'` in any module's `build.gradle(.kts)`, a `gradle.properties` key or `gradle/libs.versions.toml`
  `[versions]` entry the build script reads it from), refuses to write when modules disagree until the user
  confirms, and rewrites them all to the new value. Android Gradle projects are out of scope — see
  `iru-android-bump-version`. Invoke as
  `/iru-java-bump-version <new-version>` where `<new-version>` is the literal target version (e.g. `1.4.0` or
  `1.4.1-SNAPSHOT`) — this skill does not compute bumps itself, it only applies the value it's given (`iru-release`
  computes the release/next-dev values per the pre-release convention documented in this file and passes each one
  through in turn). Also accepts `args`: `sync-files: yes|no` (default: ask) to also update README/Antora version
  mentions, `next-version: <upcoming-version>` so that sync maps "Latest release" markers to `<new-version>` and
  "Latest snapshot"/"Current development version" markers to the upcoming pre-release value instead of rewriting
  every marker to the single value, and `dry-run: yes|no` (default `no`) to print the diff/command without writing
  or running anything.
  Reports the old and new version, the build tool and whether the project was treated as a reactor/multi-module
  build or a single module, and every file touched. Use whenever the user, or another skill such as `iru-release`,
  needs a Maven or Gradle JVM project's version set to a specific value instead of hand-editing `pom.xml` or Gradle
  build files.
model: haiku
allowed-tools: Read Bash(mvn *) Bash(./mvnw *) Bash(./gradlew *) Bash(gradle *) Bash(python3 *) Bash(grep *) Bash(find *) Bash(ls *) Bash(cat *) Bash(mkdir *)
---

# Java Bump Version

Set a JVM (Java or Kotlin) project's version to an exact value across every file that needs to agree with it:
`pom.xml` for Maven (the root artifact's own version, or every module's version in a reactor), the Gradle files
that declare the project version for Gradle (`gradle.properties`, `build.gradle(.kts)`, `gradle/libs.versions.toml`),
and — optionally — README/Antora version mentions. This skill never computes a version itself — it applies exactly the version string it's given, validated
for shape. The "which version to compute next" logic (release vs. pre-release bump) belongs to the caller
(typically `iru-release`) and is defined in Step 5 below so that caller has one place to read it from — the same
contract `iru-typescript-bump-version`, `iru-android-bump-version`, and `iru-swift-bump-version` each define for
their own ecosystems.

## Step 0 — Resolve inputs

Parse the invocation:

- The positional argument is `<new-version>` — the exact target version string (e.g. `1.4.0`, `2.0.0-SNAPSHOT`). If
  it's missing, ask the user for it before doing anything else; don't guess or compute one here.
- `args` (`key: value` lines), if present:
  - `sync-files: yes|no` — whether to also update README/Antora version mentions (Step 7). If omitted, ask once
    with `AskUserQuestion` after Step 2 confirms whether such mentions actually exist; skip asking if none do.
  - `next-version: <upcoming-version>` — the upcoming pre-release version (e.g. `1.5.0-SNAPSHOT`) that README/
    Antora "Latest snapshot"/"Current development version" markers should show after a release, while "Latest
    release" markers show `<new-version>`. Only meaningful with `sync-files: yes`; `iru-release` passes it
    alongside the release version. Validate it the same way Step 1 validates `<new-version>`.
  - `dry-run: yes|no` — default `no`. When `yes`, run every step through composing the new file contents (or the
    `mvn versions:set` command that would run, or the Gradle-file diff) and showing the diff, then stop — do not write anything or run any
    mutating command, and say so plainly in the report.

Reject, before touching anything, a `<new-version>` that is obviously not attempting a version at all (empty
string, or contains whitespace) with a short message asking for a valid value — Step 1 validates the actual shape.

## Step 1 — Validate the version string

Maven's own CLI doesn't strictly parse `-DnewVersion=` as semver (it accepts any string), and Gradle's
`project.version` is a free-form value too, so — the same situation
`iru-android-bump-version` is in — there's no build-tool command to lean on for validation the way `npm version
<v> --no-git-tag-version` does for the npm ecosystem. Validate with a regex instead, using this catalog's
Maven-style convention: `X.Y.Z` optionally followed by `-SNAPSHOT`:

```bash
python3 -c 'import re,sys; v=sys.argv[1]; sys.exit(0 if re.fullmatch(r"\d+\.\d+\.\d+(-SNAPSHOT)?", v) else 1)' "<new-version>"
```

If it doesn't match, warn the user the value doesn't follow this catalog's `X.Y.Z`/`X.Y.Z-SNAPSHOT` convention and
ask whether to proceed anyway (some projects intentionally use a different pre-release scheme, e.g. `-rc.1`) —
don't hard-stop on a non-matching but plausible string, only flag it, mirroring `iru-android-bump-version`'s Step 1.

## Step 2 — Survey the project layout

- **Detect the build tool** at the repository root:
  - `pom.xml` → **Maven**: continue with the reactor check below, then Steps 3–4's Maven paths.
  - No `pom.xml`, but `settings.gradle(.kts)`/`build.gradle(.kts)` → **Gradle**: skip the reactor check and use
    Steps 3–4's Gradle path. Prefer the wrapper (`./gradlew`) over a system `gradle` for Step 6.
  - Both present → use the one the CI workflow (`.github/workflows/*.yml`) builds with; ask the user if that
    doesn't settle it.
  - The Kotlin Multiplatform plugin (`kotlin("multiplatform")`/`org.jetbrains.kotlin.multiplatform`) applied
    anywhere → stop and point the user at `iru-kmp-bump-version`, which owns the KMP app's
    `VERSION_NAME`/`VERSION_CODE` and the iOS `MARKETING_VERSION`.
  - An Android Gradle plugin applied anywhere (`grep -rlE "com\.android\.(application|library)|android-(application|library)" --include='*.gradle*' --include='libs.versions.toml' .`)
    → stop and point the user at `iru-android-bump-version`, which owns the Android
    `libraryVersion`/`versionName`/`versionCode` layout.
  - Neither build file → ask the user for the correct path or build tool.
- **Maven only** — determine whether this is a **reactor** (multi-module) build: does the root `pom.xml` declare a `<modules>`
  element as a direct child of `<project>` (not nested inside `<profiles>`)?
  ```bash
  python3 -c '
  import re, sys
  text = open("pom.xml").read()
  parent = re.search(r"<parent>.*?</parent>", text, flags=re.DOTALL)
  search = text
  if parent:
      s, e = parent.span()
      search = text[:s] + " " * (e - s) + text[e:]
  profiles = re.search(r"<profiles>", search)
  scope = search[:profiles.start()] if profiles else search
  sys.exit(0 if re.search(r"<modules>", scope) else 1)
  '
  ```
  Exit `0` → reactor, Step 4 uses `mvn versions:set`. Exit `1` → single module, Step 4 edits `pom.xml` directly.
- **Gradle only** — note whether it is multi-module (`include(...)`/`include '...'` in `settings.gradle(.kts)`);
  Step 3's Gradle scan covers every module either way.
- Note these findings for Step 8's report — the report must say plainly which path was taken and why.

## Step 3 — Locate and read the current version

Before changing anything, locate and read the current value so the diff is visible even if a later step fails
partway through, and so a caller like `iru-release` can obtain it without guessing.

**Locating the project's own `<version>`** — the rule to follow, without ever hardcoding any artifactId: it is the
first `<version>` element that is a **direct child of `<project>`**, i.e. it is never the `<parent>`'s `<version>`
(a child of `<parent>`, one level deeper) and never a dependency's or plugin's `<version>` (nested inside
`<dependencies>`/`<dependencyManagement>`/`<build>`/`<profiles>`). By Maven convention this element sits right
after `<artifactId>`, near the top of the file, before any of those later sections begin. Locate it by first
blanking out the `<parent>...</parent>` block (if any) so its own `<version>` can never match, then taking the
first `<version>...</version>` that appears before the first `<dependencies>`, `<dependencyManagement>`,
`<build>`, `<profiles>`, `<modules>`, or `<properties>` section:

```bash
python3 - "pom.xml" <<'PY'
import re, sys
path = sys.argv[1] if len(sys.argv) > 1 else "pom.xml"
text = open(path).read()

parent = re.search(r"<parent>.*?</parent>", text, flags=re.DOTALL)
search = text
if parent:
    s, e = parent.span()
    search = text[:s] + " " * (e - s) + text[e:]

boundary = re.search(
    r"<(dependencies|dependencyManagement|build|profiles|modules|properties)>", search
)
scope = search[: boundary.start()] if boundary else search

m = re.search(r"<version>([^<]*)</version>", scope)
if not m:
    sys.exit("Could not locate the project's own <version> element in pom.xml")
print(m.group(1))
PY
```

For a reactor, the root `pom.xml`'s own version located this way is normally what every module inherits from (via
`<parent><version>${revision}</version></parent>` or an explicit matching version) — this is the value to report
and pass through as "current version"; Step 4's `mvn versions:set` updates every module regardless of whether they
currently agree with it exactly.

**Gradle** — the project version can live in several places, and a multi-module build may declare it once (root
`gradle.properties`, or `allprojects { version = … }` in the root build script) or once per module. Rather than
guessing one file, scan every place it can be declared as a literal:

- `version=<value>` in any `gradle.properties` (Gradle maps this key onto `project.version` automatically);
- `version = "<value>"` / `version = '<value>'` / Groovy `version '<value>'` / `project.version = …` as a statement
  in any module's `build.gradle(.kts)` (plugin coordinates such as `id("…") version "…"` never match — they don't
  start the line with `version`);
- indirections a build script's `version = …` line points at: a `gradle.properties` key read via
  `property("key")`/`findProperty("key")`/`providers.gradleProperty("key")` (or a bare Groovy `version = key`), and
  a `gradle/libs.versions.toml` `[versions]` entry read via `libs.versions.<alias>.get()` (alias `app.version`
  matches the TOML key `app-version`/`app_version`/`app.version`).

`buildSrc/`, `build-logic/`, and `build/` output are skipped. Write the helper once, then list what it finds:

```bash
mkdir -p "$TMPDIR/iru-java-bump-version"
cat > "$TMPDIR/iru-java-bump-version/gradle_version.py" <<'PY'
import re, sys, pathlib, difflib
args = sys.argv[1:]
dry = "--dry-run" in args
args = [a for a in args if a not in ("--dry-run", "--force")]
new_version = None if not args or args[0] == "--list" else args[0]

SKIP = {"build", ".gradle", ".git", "node_modules", "out", ".idea", "buildSrc", "build-logic"}
files = sorted(
    p for p in pathlib.Path(".").rglob("*")
    if p.is_file() and not any(part in SKIP for part in p.parts[:-1])
    and (p.name in ("gradle.properties", "build.gradle", "build.gradle.kts")
         or p.as_posix() == "gradle/libs.versions.toml")
)
builds = [p for p in files if p.name.startswith("build.gradle")]
END = r"[ \t]*(?://.*)?$"
LIT = re.compile(r"^([ \t]*(?:project\.)?version[ \t]*=?[ \t]*)([\"'])([^\"'$]+)\2(?=" + END + ")", re.M)
LINE = re.compile(r"^[ \t]*(?:project\.)?version[ \t]*=[ \t]*(.+?)" + END, re.M)
prop_keys, toml_keys = {"version"}, set()
for p in builds:
    for expr in LINE.findall(p.read_text()):
        m = re.search(r"(?:property|findProperty|gradleProperty|getProperty)\([ \t]*[\"']([\w.-]+)[\"']", expr)
        if m: prop_keys.add(m.group(1))
        m = re.search(r"libs\.versions\.([\w.]+?)\.get\(\)", expr)
        if m: toml_keys.add(m.group(1))
        if re.fullmatch(r"[A-Za-z_]\w*", expr.strip()): prop_keys.add(expr.strip())

found, new_texts = [], {}
def scan(p, rx, group, repl_fn):
    text = p.read_text()
    for m in rx.finditer(text):
        found.append((p.as_posix(), text.count("\n", 0, m.start()) + 1, m.group(group)))
    if new_version is not None:
        new_texts[p] = rx.sub(repl_fn, text)

for p in files:
    if p.name == "gradle.properties":
        keys = "|".join(re.escape(k) for k in sorted(prop_keys))
        rx = re.compile(r"^([ \t]*(?:" + keys + r")[ \t]*[=:][ \t]*)(\S[^\r\n]*?)[ \t]*$", re.M)
        scan(p, rx, 2, lambda m: m.group(1) + new_version)
    elif p.name.endswith(".toml") and toml_keys:
        text = p.read_text()
        sec = re.search(r"^\[versions\][ \t]*$(.*?)(?=^\[|\Z)", text, re.M | re.S)
        if not sec: continue
        alts = "|".join(re.sub(r"\\\.", "[-_.]", re.escape(k)) for k in sorted(toml_keys))
        rx = re.compile(r"^([ \t]*(?:" + alts + r")[ \t]*=[ \t]*)\"([^\"]*)\"", re.M)
        body = sec.group(1)
        for m in rx.finditer(body):
            found.append((p.as_posix(), text.count("\n", 0, sec.start(1) + m.start()) + 1, m.group(2)))
        if new_version is not None:
            new_texts[p] = text[:sec.start(1)] + rx.sub(lambda m: m.group(1) + '"' + new_version + '"', body) + text[sec.end(1):]
    elif p.name.startswith("build.gradle"):
        scan(p, LIT, 3, lambda m: m.group(1) + m.group(2) + new_version + m.group(2))

for path, line, value in found:
    print(f"{path}:{line}: {value}")
if not found:
    sys.exit("No literal project version found (gradle.properties `version=`, build script `version = \"...\"`, "
             "or a gradle.properties/libs.versions.toml entry the build script reads it from)")
values = {v for _, _, v in found}
if len(values) > 1:
    print(f"WARNING: modules disagree on the current version: {sorted(values)}", file=sys.stderr)
    if new_version is not None and "--force" not in sys.argv:
        sys.exit("Refusing to write: confirm with the user, then re-run with --force to align every location")
if new_version is None:
    sys.exit(0)
for p, new_text in new_texts.items():
    old = p.read_text()
    if new_text == old:
        continue
    if dry:
        sys.stdout.writelines(difflib.unified_diff(old.splitlines(True), new_text.splitlines(True), str(p), str(p)))
    else:
        p.write_text(new_text)
        print(f"updated {p}")
PY
python3 "$TMPDIR/iru-java-bump-version/gradle_version.py" --list
```

Each output line is `<file>:<line>: <current value>` — the current version is that value, and the listed files are
exactly what Step 4 will rewrite. Then:

- **Nothing found** (non-zero exit with "No literal project version found") — the version is computed (e.g. from a
  git tag via a plugin such as `axion-release`/`nebula.release`, or from an environment variable) or set in
  `buildSrc`/a convention plugin. Show the user the `version` lines `grep -rn "version" --include='build.gradle*' .`
  turns up and ask where the version lives; don't edit a computed version.
- **Locations disagree** (a `WARNING: modules disagree…` line) — show the list and ask the user whether to align
  all of them to `<new-version>` (Step 4 then passes `--force`) or which ones to leave alone (edit only those by
  hand, then say so in the report). Some multi-module builds version modules independently on purpose.
- Before trusting the list, glance at each hit in context: a `version = "…"` inside a `publishing { … }` /
  `MavenPublication` block is a publication override that normally should follow the project version, but a
  `version = …` inside an unrelated custom block is not the project version — exclude it by hand if so.

## Step 4 — Preview (`dry-run: yes`) or apply the new version

**Reactor** (Step 2 found `<modules>`):

```bash
mvn versions:set -DnewVersion=<new-version> -DgenerateBackupPoms=false
```

`-DgenerateBackupPoms=false` writes the change directly instead of leaving `pom.xml.versionsBackup` files behind,
which also means `mvn versions:commit` (whose only job is to delete those backups) is unnecessary here — don't run
it. If `dry-run: yes`, run `mvn versions:set -DnewVersion=<new-version> -DgenerateBackupPoms=false -DdryRun` and
report what it shows to be planning to change (the `versions-maven-plugin` supports its own `-DdryRun` flag), or
if that flag isn't available in the resolved plugin version, at minimum show every `pom.xml` under the reactor
whose `<version>` currently matches the value read in Step 3, since those are exactly the files `versions:set`
would touch, then stop without running the mutating command.

**Single module** (no `<modules>`):

```bash
python3 - "pom.xml" "<new-version>" <<'PY'
import re, sys
path, new_version = sys.argv[1], sys.argv[2]
text = open(path).read()

parent = re.search(r"<parent>.*?</parent>", text, flags=re.DOTALL)
search = text
if parent:
    s, e = parent.span()
    search = text[:s] + " " * (e - s) + text[e:]

boundary = re.search(
    r"<(dependencies|dependencyManagement|build|profiles|modules|properties)>", search
)
scope_end = boundary.start() if boundary else len(search)

m = re.search(r"<version>[^<]*</version>", search[:scope_end])
if not m:
    sys.exit("Could not locate the project's own <version> element in pom.xml")
start, end = m.span()
old = m.group(0)
new_text = text[:start] + f"<version>{new_version}</version>" + text[end:]

if len(sys.argv) > 3 and sys.argv[3] == "--dry-run":
    import difflib
    diff = difflib.unified_diff(
        text.splitlines(keepends=True), new_text.splitlines(keepends=True),
        fromfile=path, tofile=path,
    )
    sys.stdout.writelines(diff)
else:
    open(path, "w").write(new_text)
    print(f"pom.xml: {old} -> <version>{new_version}</version>")
PY
```

Pass a fourth argument `--dry-run` (computing and printing the diff inside the same `python3` process, not via a
shell variable, so a trailing newline isn't lost) when `dry-run: yes`; otherwise omit it so the file is written.

**Gradle** (Step 2 found a Gradle build):

```bash
python3 "$TMPDIR/iru-java-bump-version/gradle_version.py" "<new-version>"            # write
python3 "$TMPDIR/iru-java-bump-version/gradle_version.py" "<new-version>" --dry-run  # preview: unified diff only
```

Add `--force` only after the user confirmed aligning locations that currently disagree (Step 3). The script
rewrites every location Step 3 listed — and nothing else: dependency/plugin versions, other `gradle.properties`
keys, and other `[versions]` entries are untouched (verified, see Verification notes).

If any path fails (non-zero exit, or the locate step can't find a version to rewrite), stop, show the
actual error, and do not treat any file as updated — don't partially apply the version by hand as a fallback.

## Step 5 — The Java-catalog pre-release convention (for `iru-release` and other callers)

This is the JVM-ecosystem (Maven and non-Android Gradle alike) equivalent of `iru-typescript-bump-version`'s `-dev.N` convention,
`iru-android-bump-version`'s `-SNAPSHOT` convention, and `iru-swift-bump-version`'s tag-based convention — the
contract a caller (typically `iru-release`) is expected to call this skill against (two calls per release, each
passing a computed `new-version` through the positional argument):

- **Current development version**: `x.y.z-SNAPSHOT` (e.g. `1.4.0-SNAPSHOT`) — Maven's own conventional
  pre-release marker, and this catalog's pre-existing convention before this skill was extracted from
  `iru-release`.
- **Cutting a release**: strip the `-SNAPSHOT` suffix entirely — `x.y.z-SNAPSHOT` → `x.y.z`. Call this skill with
  `<new-version>: x.y.z`.
- **Opening the next development cycle**: bump the patch or minor component (caller's choice — this catalog's
  established default is a minor bump, matching the repeatable `1.3.0` → `1.4.0-SNAPSHOT` cadence `iru-release`
  has always used) and reappend `-SNAPSHOT` — `x.y.z` → `x.y.(z+1)-SNAPSHOT` or `x.(y+1).0-SNAPSHOT`. Call this
  skill again, immediately or in a follow-up sync step, with the resulting `<new-version>`. This skill only
  applies whatever exact string it's given — it never guesses which component to bump.

## Step 6 — Sanity check

After Step 4's rewrite (skip entirely when `dry-run: yes`), confirm `pom.xml` is still well-formed and the new
version actually took effect, with a cheap, side-effect-free Maven command rather than a full build:

```bash
mvn -q help:evaluate -Dexpression=project.version -DforceStdout
```

This should print exactly `<new-version>`. A non-zero exit, an XML-parsing error, or a mismatched printed value
means the rewrite broke the file or targeted the wrong element — stop, show the actual error/output, and do not
report success. For a reactor, also spot-check one non-root module's POM
(`mvn -q -pl <module> help:evaluate -Dexpression=project.version -DforceStdout`) to confirm `versions:set`
actually propagated there too.

For **Gradle**, the equivalent cheap check is the built-in `properties` task, which configures the build (so a
broken build script fails here) without compiling anything:

```bash
./gradlew -q properties | grep '^version:'             # root project
./gradlew -q :<module>:properties | grep '^version:'   # spot-check one module in a multi-module build
```

Each should print `version: <new-version>`. A configuration error or a mismatched value means the rewrite missed a
location or broke a file — stop, show the actual output, and do not report success.

## Step 7 — Optionally sync other files that mirror the version

Ask (or honor `args: sync-files`) whether to also update other places that name the current version, the same way
`iru-typescript-bump-version`'s Step 6, `iru-android-bump-version`'s Step 8, and `iru-swift-bump-version`'s Step 8
do for their ecosystems:

- **`README.md`** — a Maven/Gradle dependency snippet naming the current version, if any:
  ```bash
  grep -n "<version>\|Latest release\|Latest snapshot\|Current development version" README.md
  ```
  Update each matched `<version>...</version>` inside an install/dependency code block the same way Step 4
  rewrote `pom.xml` — a targeted, scoped substitution, not a blind repository-wide replace — mapping each marker
  by what it names rather than rewriting them all to one value:
  - "Latest release" markers (and a Project Status row such as `Latest release`) → `<new-version>` when
    `<new-version>` is a release (no `-SNAPSHOT`); when `<new-version>` is itself a `-SNAPSHOT` (a next-dev bump
    on `develop`), leave them untouched — they still name the last real release.
  - "Latest snapshot"/"Current development version" markers → `next-version` when it was given; otherwise
    `<new-version>` only if it is a `-SNAPSHOT` value, and untouched (with a warning in Step 8 that the caller
    should pass `next-version`) when `<new-version>` is a release — never regress a development marker to a
    release value.
  - A snippet naming a single version with no such marker → `<new-version>`.

  A Gradle dependency snippet (`implementation("group:artifact:1.2.3")`, Groovy `implementation 'group:artifact:1.2.3'`)
  for this project's own coordinates follows the same marker mapping; find them with
  `grep -nE "implementation[[:space:]]*\(?['\"]" README.md` and rewrite only the trailing version segment of lines naming this
  project's own `group:artifact` (the regex in `iru-android-bump-version`'s Step 8 does exactly this — restrict it
  to this project's coordinates so third-party dependency snippets in the README are left alone). A Spring Boot or
  Quarkus service usually has no dependency snippet at all — then only the "Latest release"-style markers apply.
- **`docs/antora.yml`** — its `version:` field, if this repository has an Antora site and that field is meant to
  track the released version (skip for a `-SNAPSHOT` value — this catalog's convention is to only write a
  released version there, matching `iru-typescript-bump-version`/`iru-android-bump-version`/
  `iru-swift-bump-version`'s own Step 6/8).
- Any Antora page under `docs/modules/ROOT/pages/` showing a dependency snippet with a literal version string:
  ```bash
  grep -rlE "<version>|implementation.*[0-9]+\.[0-9]+\.[0-9]+" docs/modules/ROOT/pages/*.adoc 2>/dev/null
  ```
  Update each match the same way as the README snippet above.

This is offered, not automatic — these files may be intentionally out of step with the build files (e.g. a README badge
pulling live from Maven Central rather than a hardcoded string), so don't rewrite anything the user didn't
confirm.

## Step 8 — Report

Summarize:

- The build tool (Maven or Gradle). For Maven, whether the project was treated as a **reactor**
  (`mvn versions:set` path) or a **single module** (direct `pom.xml` edit), and why (presence/absence of
  `<modules>`); for Gradle, whether it is multi-module and every version location Step 3 found (and whether they
  disagreed and were aligned with `--force` after the user confirmed).
- The old version (Step 3) and the new version, and every file actually changed: `pom.xml` (or every module's
  `pom.xml` for a reactor) / each Gradle file rewritten, plus any Step 7 files accepted.
- Whether this was a `dry-run` (nothing written/run) or an actual write.
- The Step 6 sanity-check result — `mvn help:evaluate` output for the root (and, for a reactor, the spot-checked
  module), or `./gradlew -q properties` for Gradle — passed, failed with the actual error, or not run because
  `dry-run: yes`.
- **Warn explicitly**: review the diff before committing (this skill doesn't commit anything); for a reactor,
  `versions:set -DgenerateBackupPoms=false` writes directly with no backup files to fall back on if the wrong
  version was passed — double-check `<new-version>` before confirming a non-dry-run call; a README/Antora badge
  that pulls the version live from Maven Central rather than hardcoding it should not have Step 7 applied to it.

## Verification notes

Verified in `$TMPDIR/iru-verify/java/iru-java-bump-version/` by running the exact Step 3/4 Gradle helper (extracted
from this file) against hand-written Gradle layouts:

- Root `gradle.properties` `version=1.4.0-SNAPSHOT` plus a Groovy module `version '1.4.0-SNAPSHOT'`, with
  `kotlin("jvm") version "…"`/`id("org.springframework.boot") version "…"` plugin lines and an unrelated
  `kotlinVersion=` key: both project-version locations listed and rewritten to `1.4.0`; plugin lines and other keys
  untouched; `--dry-run` printed the unified diff and wrote nothing.
- `version = libs.versions.app.version.get()` → only `[versions] app-version` rewritten; a `[libraries]` entry with
  the same value and `[plugins]`/multi-line `version = "…"` entries outside `[versions]` untouched.
- `version = property("projVer") as String` and Groovy `version = projectVersion` → the referenced
  `gradle.properties` key rewritten, other keys untouched.
- Two modules declaring `2.0.0` and `2.1.0` → write refused with the disagreement warning; `--force` aligned both.
- A build with no literal version → non-zero exit with the "No literal project version found" message.

- Real Gradle 8 (`gradle:8-jdk21` Docker image, `$TMPDIR/iru-verify/java/iru-java-bump-version-gradle/`): a
  two-module Kotlin DSL build with root `gradle.properties` `version=1.4.0-SNAPSHOT`, a Kotlin `svc` module
  inheriting it, and a Groovy `lib` module using `version = libs.versions.lib.version.get()` — the helper rewrote
  both locations to `1.4.0`, and Step 6's `gradle -q properties | grep '^version:'` printed `version: 1.4.0` for the
  root, `:svc`, and `:lib`.

Not verified locally: real-project behavior of version
plugins (e.g. `axion-release`) or `buildSrc`/convention-plugin-defined versions, which the helper deliberately
doesn't touch. The Maven paths are unchanged from before the Gradle branch was added.
