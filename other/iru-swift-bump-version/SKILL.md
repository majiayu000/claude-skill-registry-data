---
name: iru-swift-bump-version
description: "/iru-swift-bump-version <new-version> - sets a Swift package, command-line tool or Apple app version to the exact value given: the CLI version literal, a SwiftPM library's tag-mirroring files, or an app's MARKETING_VERSION and build number. Optional args: sync-files, dry-run, kind: library|app|cli. Reports old/new values and files touched."
model: haiku
---

# Swift Bump Version

Set a Swift (SwiftPM library) or Apple app (Xcode-generated) project's version to an exact value across every file
that needs to agree with it. Unlike the Java/npm/Android ecosystems, a SwiftPM **library** carries no in-tree
version field the package manager itself reads — a consumer's `.package(url:, from:/exact:)` resolves against the
package's **git tag**, full stop, so this skill only rewrites the files that exist purely by this catalog's own
convention to mirror that tag (`version.txt`, `CHANGELOG.md`, README snippets), never a value SwiftPM itself
consults. An Apple **app**, by contrast, does carry an in-tree version: `MARKETING_VERSION`/`CURRENT_PROJECT_VERSION`
in whichever project format (XcodeGen, Tuist, raw `.xcconfig`, or `.xcodeproj`) is in play. A Swift **command-line
tool** carries one too: the string literal its `--version` prints (`Version.swift`'s `toolVersion`, or a
`CommandConfiguration(version:)` literal), which follows the `x.y.z-dev` convention on the integration branch. This
skill never computes
a version itself — it applies exactly the version string it's given, validated for shape. The "which version to
compute next" logic belongs to the caller and is defined in Step 5, mirroring `iru-typescript-bump-version`'s Step 5
and `iru-android-bump-version`'s Step 5.

## Step 0 — Resolve inputs

Parse the invocation:

- The positional argument is `<new-version>` — the exact target version string (e.g. `1.4.0`, `1.4.0-rc.1`). If
  it's missing, ask the user for it before doing anything else; don't guess or compute one here.
- `args` (`key: value` lines), if present:
  - `sync-files: yes|no` — whether to also update `docs/antora.yml`/Antora page version mentions and, for an app,
    a README version mention (Step 8). If omitted, ask once with `AskUserQuestion` after Step 2 confirms whether
    such mentions actually exist; skip asking if none do.
  - `next-version: <upcoming-version>` — the upcoming pre-release version (e.g. `1.5.0-rc.1`, or the next
    planned tag) that README/Antora "Latest snapshot"/"Current development version"-style markers should show
    after a release, while "Latest release" markers and the dependency snippet show `<new-version>`. Only
    meaningful with `sync-files: yes`; `iru-release` passes it so a release never regresses a development marker
    to the release value (see Step 8).
  - `dry-run: yes|no` — default `no`. When `yes`, run every step through composing the new file contents and
    showing the diff (Step 7), then stop — do not write anything, and say so plainly in the report.
  - `kind: library|app|cli` — overrides Step 2's auto-detected project kind. Use this when a repository legitimately
    carries both a root `Package.swift` (e.g. a local `Packages/Core` package used by an app target) and a
    generator manifest/`.xcodeproj` — auto-detection alone can't disambiguate which one the user means to bump.

Reject, before touching anything, a `<new-version>` that is obviously not attempting a version at all (empty
string, or contains whitespace) with a short message asking for a valid value — Step 1 validates the actual shape.

## Step 1 — Validate the version string

Neither SwiftPM nor Xcode's build settings parse or validate `MARKETING_VERSION`/a git tag as strict semver (both
are free-form strings), so — the same situation `iru-android-bump-version` is in — there's no build-tool command to
lean on the way `npm version <v> --no-git-tag-version` validates for the npm ecosystem. Validate with a regex
instead, using this catalog's convention: plain semver, `X.Y.Z` optionally followed by a hyphen pre-release
identifier and/or a `+` build-metadata identifier (`X.Y.Z-rc.1`, `X.Y.Z+build.5`) — the general form, since a Swift
package release tag and an app's `MARKETING_VERSION`/TestFlight build both commonly use pre-release suffixes
(`-rc.1`, `-beta.2`) that the stricter Java `-SNAPSHOT`-only shape doesn't need to allow for:

```bash
python3 -c 'import re,sys; v=sys.argv[1]; sys.exit(0 if re.fullmatch(r"\d+\.\d+\.\d+(-[0-9A-Za-z][0-9A-Za-z.]*)?(\+[0-9A-Za-z][0-9A-Za-z.]*)?", v) else 1)' "<new-version>"
```

Verified locally: `1.2.0` and `1.2.0-rc.1` match; `1.2` (missing patch), `1.2.0 ` (trailing whitespace), an empty
string, and `abc` all correctly fail to match.

If it doesn't match, warn the user the value doesn't follow this catalog's `X.Y.Z`/`X.Y.Z-<pre-release>` convention
and ask whether to proceed anyway (some projects intentionally use a different scheme) — don't hard-stop on a
non-matching but plausible string, only flag it, mirroring `iru-android-bump-version`'s Step 1.

## Step 2 — Survey which project kind/files exist

Determine the project kind (honor `args: kind` if given, otherwise auto-detect):

- **Command-line tool** (checked first): a root `Package.swift` declaring an `.executableTarget` that depends on
  `ArgumentParser` (`grep -n 'executableTarget\|ArgumentParser' Package.swift`), no generator manifest/`.xcodeproj`
  at the root, **and** Step 3b's helper finds a version literal under `Sources/` → `kind: cli`, Step 3b applies. An
  ArgumentParser package with no literal (its `--version` isn't wired, or it reads the version from elsewhere) falls
  through to **Library** — the git tag is then its only version; say so.
- **Library**: a root `Package.swift` exists and no generator manifest/`.xcodeproj` is present at the root →
  `kind: library`, Step 3 applies.
- **App**: any of `project.yml` (XcodeGen), `Project.swift` (Tuist), or a `*.xcodeproj` directory exists at the
  root → `kind: app`, Step 4 applies. When more than one of these exists (e.g. both a generator manifest and a
  checked-in `.xcodeproj` the generator produced), prefer the generator manifest — it's the source of truth the
  `.xcodeproj` is regenerated from, so editing the `.xcodeproj` directly would be overwritten on the next
  `xcodegen generate`/`tuist generate`.
- **Both present** (e.g. an app repository with a local `Packages/Core` SwiftPM package alongside its own root
  `Package.swift`): this is exactly the case `args: kind` exists to disambiguate — if it isn't given, ask via
  `AskUserQuestion` which one the user means, rather than guessing; note that a nested package under `Packages/`
  is not scanned as a second target on its own, only the repository root.
- **Neither found**: hard stop — tell the user no `Package.swift`, `project.yml`, `Project.swift`, or `.xcodeproj`
  was found at the repository root, and ask for the correct path or whether the project uses a different layout
  than this catalog's `iru-setup-swift-library`/`iru-setup-apple-app` scaffold produces — don't silently do
  nothing.

Also note, for Step 3/8, whether `version.txt` and `CHANGELOG.md` already exist at the root (both are optional —
`version.txt` is only meaningful when this repository's `iru-setup-swift-github-workflows`-generated `sync.yml`
bumps `MARKETING_VERSION`/`version.txt` on the gitflow sync — and `CHANGELOG.md` is
created by `iru-setup-changelog`), and for Step 4, which of `project.yml`/`Project.swift`/`*.xcconfig`/`.xcodeproj`
actually carry `MARKETING_VERSION`/`CURRENT_PROJECT_VERSION` (a project can spread these across more than one —
e.g. a `Version.xcconfig` included from `project.yml`'s `configFiles:` — survey with `grep -rn
"MARKETING_VERSION\|CURRENT_PROJECT_VERSION"` across `project.yml`, `Project.swift`, and every `*.xcconfig` before
picking which file(s) actually own the value, so Step 4 doesn't silently miss one or double-bump another).

## Step 3 — Read and rewrite library files (`version.txt`, `CHANGELOG.md`, README snippets)

These three files are this skill's **primary** output for a library — unlike the optional Step 8 sync, they are
rewritten unconditionally (when the file exists, or, for `version.txt`, created per the note below), because the
task description for this skill states them as the library path's core deliverable, not an opt-in extra.

**`version.txt`** — a plain one-line file holding the current released version, read by this catalog's
`sync.yml` template (`iru-setup-swift-github-workflows`) to know what the "current" version is between
tags. Read the old value first, then overwrite:

```bash
cat version.txt 2>/dev/null || echo "(no version.txt yet)"
printf '%s\n' "<new-version>" > version.txt
```

If `version.txt` doesn't exist yet, create it — but only after confirming with the user (or via `args`) that this
repository's `sync.yml`/README actually reference it (`grep -rn "version.txt" .github/workflows/ README.md 2>/dev/null`);
if nothing references it, note in the report that a `version.txt` file was **not** created because nothing in this
repository reads one, and the only real "version" for this package remains its git tag.

**`CHANGELOG.md`** — rename the top `## [Unreleased]` heading to `## [<new-version>] - <today's date>` and reopen a
fresh, empty `## [Unreleased]` above it, the same Keep a Changelog convention `iru-release`'s Step 7 uses for the
Java/Maven path:

```bash
python3 - "CHANGELOG.md" "<new-version>" "$(date +%F)" <<'PY'
import re, sys
path, new_version, today = sys.argv[1], sys.argv[2], sys.argv[3]
text = open(path).read()
new_text, n = re.subn(
    r'^## \[Unreleased\]\s*\n(?:[ \t]*\n)*',
    f'## [Unreleased]\n\n## [{new_version}] - {today}\n\n',
    text,
    count=1,
    flags=re.MULTILINE,
)
if n == 0:
    sys.exit("## [Unreleased] heading not found in CHANGELOG.md")
open(path, "w").write(new_text)
PY
```

Skip this file entirely (note it in the report) if `CHANGELOG.md` doesn't exist — don't create one here, that's
`iru-setup-changelog`'s job.

**README `.package(url:, from:/exact:)` snippets** — rewrite the version literal following either keyword,
covering both the version-range form (`from: "1.0.0"`, which SwiftPM resolves as `.upToNextMajor(from:)`) and the
pinned form (`exact: "1.0.0"`):

```bash
python3 - "README.md" "<new-version>" <<'PY'
import re, sys
path, new_version = sys.argv[1], sys.argv[2]
text = open(path).read()
new_text, n = re.subn(
    r'((?:from|exact)\s*:\s*)"[^"]*"',
    lambda m: f'{m.group(1)}"{new_version}"',
    text,
)
open(path, "w").write(new_text)
print(f"README replacements: {n}")
PY
```

If `n` is `0`, README has no `.package(...)` snippet to update — note that, don't fail. If `n` is greater than the
number of snippets you expected (e.g. the README also shows an unrelated `from:`/`exact:` argument in a different
context), show the diff and confirm before trusting it silently — this regex is intentionally broad because it
must match both the `from:`/`exact:` keyword forms and doesn't anchor on `.package(url:` (a snippet can wrap across
lines), so a false-positive match elsewhere in the README is possible in principle, though not observed in this
skill's own verification.

## Step 3b — Read and rewrite a command-line tool's version literal (`kind: cli`)

A Swift command-line tool keeps its version in source, because `--version` must print it: in the
`iru-setup-swift-cli` layout that is `Sources/<Bin>Kit/Version.swift` (`public let toolVersion = "0.1.0-dev"`,
which the root command's `CommandConfiguration(version: toolVersion)` reads), and in other ArgumentParser tools often a
literal `version: "1.2.3"` inside `CommandConfiguration(...)`. The helper below finds both — a `*version*`-named
`let`/`var` string literal in any `Version.swift`, a `toolVersion`/`version` literal elsewhere under `Sources/`, and a
semver-looking `version: "…"` in a file that builds a `CommandConfiguration` — and rewrites every one of them, never
`.build/`, `Tests/` or a differently-named literal such as `apiVersion = "2.0.0"`. Write it to a scratch file outside
the repository and run it from the repository root:

```python
import difflib, os, re, sys

# Usage: python3 -I cli_version.py <package-root> [--list | --dry-run <new> | <new>]
LITERAL = re.compile(
    r'^(?P<head>[ \t]*(?:(?:public|package|internal|fileprivate|private|static|nonisolated)[ \t]+)*(?:let|var)[ \t]+'
    r'(?P<name>\w*[Vv]ersion\w*)(?:[ \t]*:[ \t]*String)?[ \t]*=[ \t]*")(?P<value>\d+\.\d+\.\d+[^"\\\n]*)(?P<tail>")',
    re.MULTILINE,
)
CONFIG = re.compile(r'(?P<head>\bversion:[ \t]*")(?P<value>\d+\.\d+\.\d+[^"\\\n]*)(?P<tail>")')


def sources(root):
    base = os.path.join(root, "Sources")
    for directory, dirs, files in os.walk(base):
        dirs[:] = sorted(d for d in dirs if not d.startswith(".") and not d.endswith(".docc"))
        for name in sorted(files):
            if name.endswith(".swift"):
                yield os.path.join(directory, name)


def find(root):
    hits = []
    for path in sources(root):
        text = open(path, encoding="utf-8").read()
        in_version_file = os.path.basename(path) == "Version.swift"
        for match in LITERAL.finditer(text):
            # Outside Version.swift only `toolVersion`/`version` count, so an `apiVersion = "2.0.0"` is left alone.
            if in_version_file or match.group("name") in ("toolVersion", "version"):
                hits.append((path, "literal", match))
        if "CommandConfiguration" in text:
            for match in CONFIG.finditer(text):
                hits.append((path, "CommandConfiguration", match))
    return hits


def main():
    root, args = sys.argv[1], sys.argv[2:]
    hits = find(root)
    if not hits:
        sys.exit("no version literal found under Sources/ (Version.swift or CommandConfiguration(version:))")
    values = sorted({match.group("value") for _, _, match in hits})
    for path, kind, match in hits:
        print(f"{os.path.relpath(path, root)}: {kind} {match.group('value')!r}")
    if len(values) > 1:
        print(f"WARNING: the literals disagree: {values}")
    if not args or args[0] == "--list":
        return
    dry = args[0] == "--dry-run"
    new = args[1] if dry else args[0]
    for path in sorted({path for path, _, _ in hits}):
        old = open(path, encoding="utf-8").read()
        spans = {match.span() for hit_path, kind, match in hits if hit_path == path and kind == "literal"}
        text = LITERAL.sub(lambda m: m.group("head") + new + m.group("tail") if m.span() in spans else m.group(0), old)
        if "CommandConfiguration" in text:
            text = CONFIG.sub(lambda m: m.group("head") + new + m.group("tail"), text)
        if text == old:
            continue
        if dry:
            rel = os.path.relpath(path, root)
            sys.stdout.writelines(difflib.unified_diff(old.splitlines(True), text.splitlines(True), rel, rel))
        else:
            open(path, "w", encoding="utf-8").write(text)
            print(f"updated {os.path.relpath(path, root)}")


main()
```

1. `python3 -I <scratch>/cli_version.py . --list` — prints every literal (`path: literal|CommandConfiguration 'value'`);
   the old version is that value. If the literals disagree (`WARNING: the literals disagree`), show them and ask
   which is authoritative before writing. No literal → exit 1 ("no version literal found"): report that `--version`
   isn't wired and stop (or fall back to the library path if the user confirms).
2. `python3 -I <scratch>/cli_version.py . --dry-run <new-version>` prints a unified diff (Step 7's preview);
   `python3 -I <scratch>/cli_version.py . <new-version>` writes and prints `updated <path>` per file.

A tool's README `.package(from:)` snippets don't apply (a CLI isn't consumed as a dependency) and `CHANGELOG.md` is
left to the caller (`iru-release`'s own Step 7 writes the release section) — only Step 8's optional sync (README /
`docs/antora.yml` / Antora version mentions, e.g. a Homebrew or download snippet) touches other files.

## Step 4 — Read and rewrite app files (`MARKETING_VERSION`/`CURRENT_PROJECT_VERSION`)

Apply to whichever file(s) Step 2 identified as owning the value. `MARKETING_VERSION` always gets set to
`<new-version>` verbatim; `CURRENT_PROJECT_VERSION` is a monotonically increasing build-number integer — the same
role Android's `versionCode` plays for Google Play, and Apple's own guidance requires it strictly increase for
every build uploaded to App Store Connect/TestFlight, so **always increment it by exactly 1** on every call of this
skill (unlike `iru-android-bump-version`'s conditional `-SNAPSHOT`-gated rule, there is no in-tree pre-release
marker for an app's `MARKETING_VERSION` to gate on here — see Step 5).

**XcodeGen `project.yml`** (`settings: base:`):

```bash
grep -n "MARKETING_VERSION\|CURRENT_PROJECT_VERSION" project.yml
python3 - "project.yml" "<new-version>" <<'PY'
import re, sys
path, new_version = sys.argv[1], sys.argv[2]
text = open(path).read()
# Quote-tolerant: matches both `MARKETING_VERSION: 1.0.0` and `MARKETING_VERSION: "1.0.0"`, and keeps
# whichever form the file already uses.
text, n_mv = re.subn(
    r'(MARKETING_VERSION:\s*)("?)[^"\s]+\2',
    lambda m: f'{m.group(1)}{m.group(2)}{new_version}{m.group(2)}',
    text, count=1,
)
if n_mv == 0:
    sys.exit("MARKETING_VERSION not found in project.yml")
def bump(m):
    return f"{m.group(1)}{m.group(2)}{int(m.group(3)) + 1}{m.group(2)}"
text, n_cpv = re.subn(
    r'(CURRENT_PROJECT_VERSION:\s*)("?)(\d+)\2',
    bump,
    text, count=1,
)
if n_cpv == 0:
    sys.exit("CURRENT_PROJECT_VERSION not found in project.yml")
open(path, "w").write(text)
print(f"MARKETING_VERSION replacements: {n_mv}, CURRENT_PROJECT_VERSION replacements: {n_cpv}")
PY
```

Both regexes only touch the **first** occurrence in the file, and both tolerate an optional pair of double
quotes around the value (`1.0.0` and `"1.0.0"`; `1` and `"1"`), preserving whichever form the file uses —
`iru-setup-apple-app` writes them unquoted, but a hand-edited or older manifest may quote them. This catalog's
`iru-setup-apple-app` scaffold writes these keys once, under the top-level `settings: base:` block; a project that also overrides either key
per-target (a nested `targets: <Target>: settings: base:` block) needs those reviewed by hand afterward (Step 9
warns about this explicitly) — this skill does not attempt to find and rewrite every per-target override, only the
project-wide default.

**Tuist `Project.swift`** (`settings: .settings(base: [...])`) — same idea, Swift dictionary-literal syntax
instead of YAML:

```bash
grep -n "MARKETING_VERSION\|CURRENT_PROJECT_VERSION" Project.swift
python3 - "Project.swift" "<new-version>" <<'PY'
import re, sys
path, new_version = sys.argv[1], sys.argv[2]
text = open(path).read()
text, n_mv = re.subn(
    r'("MARKETING_VERSION":\s*)"[^"]*"',
    lambda m: f'{m.group(1)}"{new_version}"',
    text, count=1,
)
if n_mv == 0:
    sys.exit('MARKETING_VERSION not found in Project.swift')
def bump(m):
    return f'{m.group(1)}"{int(m.group(2)) + 1}"'
text, n_cpv = re.subn(
    r'("CURRENT_PROJECT_VERSION":\s*)"(\d+)"',
    bump,
    text, count=1,
)
if n_cpv == 0:
    sys.exit('CURRENT_PROJECT_VERSION not found in Project.swift')
open(path, "w").write(text)
print(f"MARKETING_VERSION replacements: {n_mv}, CURRENT_PROJECT_VERSION replacements: {n_cpv}")
PY
```

**`*.xcconfig`** (e.g. a shared `Version.xcconfig` included via `project.yml`'s `configFiles:`, or hand-maintained
in a `.xcodeproj`-only project) — same substitution shape, `KEY = value` syntax:

```bash
grep -n "MARKETING_VERSION\|CURRENT_PROJECT_VERSION" <path>.xcconfig
python3 - "<path>.xcconfig" "<new-version>" <<'PY'
import re, sys
path, new_version = sys.argv[1], sys.argv[2]
text = open(path).read()
text, n_mv = re.subn(
    r'(MARKETING_VERSION\s*=\s*)\S+',
    lambda m: f'{m.group(1)}{new_version}',
    text, count=1,
)
if n_mv == 0:
    sys.exit("MARKETING_VERSION not found in xcconfig")
def bump(m):
    return f"{m.group(1)}{int(m.group(2)) + 1}"
text, n_cpv = re.subn(
    r'(CURRENT_PROJECT_VERSION\s*=\s*)(\d+)',
    bump,
    text, count=1,
)
if n_cpv == 0:
    sys.exit("CURRENT_PROJECT_VERSION not found in xcconfig")
open(path, "w").write(text)
print(f"MARKETING_VERSION replacements: {n_mv}, CURRENT_PROJECT_VERSION replacements: {n_cpv}")
PY
```

**Hand-maintained `.xcodeproj` with no generator manifest at all** (no `project.yml`/`Project.swift` found in
Step 2, only a checked-in `.xcodeproj`) — do not hand-edit `project.pbxproj`'s version fields with a regex as the
first choice; Apple ships a purpose-built tool for exactly this:

```bash
xcrun agvtool new-marketing-version "<new-version>"
xcrun agvtool new-version -all "<current-build-number> + 1"   # compute the new integer yourself, agvtool takes the literal target value, not a delta
```

`agvtool new-marketing-version <v>` sets `MARKETING_VERSION` (all matching build configurations); `agvtool
new-version -all <n>` sets `CURRENT_PROJECT_VERSION` to the literal integer `<n>` (not a delta — read the current
value first with `agvtool what-version` and pass `current + 1`). Both commands must be run from the directory
containing the `.xcodeproj` (or its parent). `agvtool` requires the project's "Current Project Version" build
setting to already be using `agvtool`-managed versioning (`VERSIONING_SYSTEM = "apple-generic"`) — if it isn't
(`agvtool what-version` errors with a message to that effect), fall back to the documented `sed` on
`project.pbxproj` instead, which needs a `-g` since `MARKETING_VERSION`/`CURRENT_PROJECT_VERSION` appear once per
build configuration (Debug/Release, and once more per target):

```bash
sed -i.bak -E \
  -e 's/(MARKETING_VERSION = )[^;]+;/\1<new-version>;/g' \
  -e 's/(CURRENT_PROJECT_VERSION = )[0-9]+;/echo "\1$((\2 + 1));"/ge' \
  <name>.xcodeproj/project.pbxproj && rm <name>.xcodeproj/project.pbxproj.bak
```

(The `CURRENT_PROJECT_VERSION` line above uses GNU `sed`'s `e` flag to evaluate a shell expression per match so
each occurrence increments independently rather than being set to one literal value — this needs GNU `sed`; on
macOS's BSD `sed` this `e`-flag trick does not work identically, so on macOS prefer the `agvtool` path, or fall
back to the `python3` regex form shown above adapted to `project.pbxproj`'s `KEY = value;` syntax with a trailing
semicolon, matching every occurrence with `re.subn(..., text)` with no `count=1` limit.) Confirmed locally:
`xcrun agvtool help` exists and lists `new-marketing-version`/`new-version [-all]` as documented above; the actual
rewrite (either path) was **not** exercised against a real hand-maintained `.xcodeproj` in this skill's own
verification — see "Known quirks / verification notes".

## Step 5 — The Swift-catalog pre-release convention (for `iru-release` and other callers)

This is the Swift-ecosystem equivalent of the Java catalog's Maven `-SNAPSHOT` convention (`iru-release`), the npm
catalog's `-dev.N` convention (`iru-typescript-bump-version`'s Step 5), and the Android catalog's `-SNAPSHOT`
convention (`iru-android-bump-version`'s Step 5) — except that, unlike those three ecosystems, **there is no
in-tree pre-release marker for a library at all**:

- **Library**: no development-version file or field exists in-tree between releases — SwiftPM has nothing to read
  until a tag exists, so there is nothing to set to a "next dev" value the way `1.4.0-dev.0`/`1.4.0-SNAPSHOT` are.
  The release **is** the git tag: `iru-release` determines the release version as
  the next semver component bump from the last tag —
  ```bash
  git describe --tags --abbrev=0
  ```
  (verified locally: tagging a throwaway repo's initial commit `1.1.0`, then committing again, correctly returns
  `1.1.0` — the last reachable tag, not a guess) — asks the user which component to bump (patch/minor/major) from
  that value the same way the Java/npm/Android paths do, then calls this skill once with the resulting
  `new-version` to update `version.txt`/`CHANGELOG.md`/README (Step 3), and separately creates the actual git tag
  itself (this skill never tags — tagging is a release-orchestration action, not a file-rewrite one, and belongs to
  the caller, exactly as this skill never commits).
- **Command-line tool** (`kind: cli`): the in-tree literal carries a `-dev` pre-release suffix on the integration
  branch (`0.1.0-dev`), exactly like this catalog's PHP/.NET/Rust/Go command-line conventions. `iru-release` strips
  it for the release (`0.1.0-dev` → `0.1.0`, calling this skill with `0.1.0`), and the next development value is the
  minor bump plus `-dev` (`0.2.0-dev`) — written by the repository's `sync.yml` after the release, or by a second call
  of this skill against `develop`. The release tag is the version without a `v` prefix and must equal the literal
  (the release workflow checks it).
- **App**: `MARKETING_VERSION` **is** the release version in-tree (there's no separate pre-release file to bump
  either, but for a different reason than the library case — an app's "current development version" is simply
  whatever `MARKETING_VERSION` already says, since TestFlight/App Store builds are distinguished from each other by
  `CURRENT_PROJECT_VERSION`, not by a `-SNAPSHOT`/`-dev.N`-style suffix on `MARKETING_VERSION`). The convention:
  `CURRENT_PROJECT_VERSION` increases by exactly 1 on every call (Step 4) — monotonically, forever, never reset —
  while `MARKETING_VERSION` is set to whatever release/beta version string the caller decides on (a plain
  `x.y.z` for a store release, or `x.y.z-beta.N` for an internal/TestFlight-only build, at the caller's
  discretion — this skill validates the shape in Step 1 but does not itself decide which one a given call should
  use).

## Step 6 — Sanity check

- **Library**: confirm `Package.swift` is still syntactically valid after Step 3 touched files near it (Step 3
  never edits `Package.swift` itself, but this is still the cheapest signal that nothing in the package broke):
  ```bash
  swift package dump-package
  ```
  A non-zero exit means something is wrong with the package manifest (unrelated to this skill's own edits, since
  it never touches `Package.swift`, but worth surfacing) — show the actual error and don't report success blindly.
  Verified locally: run against a throwaway `DemoLib` package (Swift 6.4 toolchain, `swift-tools-version:5.10`),
  exits `0` and prints the expected JSON manifest (name, platforms, products, targets).
- **Command-line tool**: build and ask the binary — `swift build --product <bin>` then
  `"$(swift build --show-bin-path)/<bin>" --version` must print exactly `<new-version>` (the `<bin>` is the
  `.executable` product name in `Package.swift`). A compile error here means the helper matched something it
  shouldn't have — show it and restore the file from the diff.
- **App**: regenerate the Xcode project from its manifest and confirm the new value round-trips through
  `xcodebuild -showBuildSettings`:
  ```bash
  xcodegen generate   # or: tuist generate
  xcodebuild -showBuildSettings -project <Name>.xcodeproj -scheme <Scheme> | grep MARKETING_VERSION
  ```
  **Unverified locally** — this environment has no `brew`, so `xcodegen`/`tuist` are not installable here (per this
  group's environment notes) and this check was not exercised against a real generated project. The `project.yml`/
  `Project.swift`/`*.xcconfig` regex rewrites themselves (Step 4) **were** verified directly against sample files
  (see "Known quirks / verification notes") — only this specific generate-and-inspect round-trip is unverified.
  For a hand-maintained `.xcodeproj` (`agvtool` path), the equivalent check is `agvtool what-marketing-version` /
  `agvtool what-version` immediately after Step 4's `agvtool` calls, which read back exactly what was just written
  — cheaper than a full `xcodebuild -showBuildSettings` and doesn't need a scheme name.

## Step 7 — Preview (`dry-run: yes`) or write

- Compose the new file contents for every file touched (Step 3/4, and Step 8 if accepted) without writing them to
  disk first — every `python3` snippet above naturally supports this since it builds the substituted string in
  memory before the final `open(path, "w").write(...)` call; for a dry run, print that string (or a diff) instead
  of writing it.
- **Quirk discovered during this skill's own verification**: computing the diff via a shell `diff -u
  <(cat original) <(printf '%s' "$new_text")` one-liner (the form `iru-android-bump-version`'s Step 7 uses) loses
  the file's trailing newline once `new_text` has passed through a bash `$(...)` command substitution — bash
  strips trailing newlines from command substitution, so the diff shows a spurious "\ No newline at end of file"
  even though the real write (via `python3`'s own `open().write()`, not through a shell variable) would have
  preserved it correctly. Prefer computing and printing the dry-run diff **inside** the same `python3` process that
  built `new_text` (e.g. `difflib.unified_diff(open(path).read().splitlines(keepends=True),
  new_text.splitlines(keepends=True))`) rather than round-tripping the string through a shell variable first.
- If `dry-run: yes`: show the diff for every file that would change, do not write anything, do not run Step 6, and
  say plainly in the report that this was a preview only — no file was modified.
- Otherwise: write each file, then run Step 6.

## Step 8 — Optionally sync other files that mirror the version

Ask (or honor `args: sync-files`) whether to also update other places that name the current version, the same way
`iru-typescript-bump-version`'s Step 6 and `iru-android-bump-version`'s Step 8 do for their ecosystems. Unlike
those two skills, a library's README dependency snippet is already handled unconditionally in Step 3 — Step 8 here
only covers the files that may legitimately be intentionally out of step with the in-tree/tag version:

**Marker mapping when `next-version` was given** (the `iru-release` case — same rule as
`iru-java-bump-version`'s Step 7): rewrite each mention by what it names rather than to one value —
"Latest release"-style markers and a Project Status `Latest release` row → `<new-version>` when it is a release
(no pre-release pre-release suffix), left untouched when `<new-version>` is itself a pre-release; "Latest snapshot"/
"Current development version"-style markers → `next-version` when given, otherwise `<new-version>` only if it is
a pre-release value, and untouched (with a warning in the Report step that the caller should pass `next-version`)
when `<new-version>` is a release — never regress a development marker to a release value. A snippet with no
such marker → `<new-version>`.

- **`docs/antora.yml`** — its `version:` field, if this repository has an Antora site and that field is meant to
  track the released version (skip for a pre-release value, e.g. `x.y.z-rc.N` — this catalog's convention, matching
  `iru-release`'s Java path and the npm/Android bump-version skills, is to only write a released version there).
- Any Antora page under `docs/modules/ROOT/pages/` showing an install/dependency snippet with a literal version
  string:
  ```bash
  grep -rl '"[^"]*":\s*"\?[0-9]\+\.[0-9]\+\.[0-9]\+' docs/modules/ROOT/pages/*.adoc 2>/dev/null
  ```
  Update each match with the same `from:`/`exact:` substitution shown in Step 3 (or a `MARKETING_VERSION`-style
  substitution for an app-flavored doc page, if any).
- **App only — a README "Current version"/App Store badge mention**, if any (`grep -n "MARKETING_VERSION\|Current
  version" README.md`): apps more commonly show a static App Store/TestFlight badge that pulls live rather than
  hardcoding a version string, so ask before touching README at all here, unlike the library path where the
  `.package(...)` snippet in Step 3 is always meant to track the exact current version.

This is offered, not automatic — these files may be intentionally out of step with the tag/`MARKETING_VERSION`
(e.g. a badge pulling live from the Swift Package Index or the App Store rather than a hardcoded string), so don't
rewrite anything the user didn't confirm.

## Step 9 — Report

Summarize:

- The project kind detected (`library`/`app`, and how — auto-detected or `args: kind` override), the old version
  and the new version.
- **Library**: every file actually changed (`version.txt` — or "not created, nothing references it"; `CHANGELOG.md`
  — or "skipped, file doesn't exist"; README `.package(...)` snippet replacement count), and the explicit reminder
  that **the git tag itself is the actual release artifact** — this skill does not create it, the caller must run
  `git tag <new-version>` (typically un-prefixed, matching this catalog's `git tag --sort=-v:refname` convention
  used elsewhere) and push it once the changes here are committed.
- **Command-line tool**: every literal rewritten (path + kind), the `--version` read-back, and that `CHANGELOG.md`
  was left to the caller.
- **App**: which file(s) `MARKETING_VERSION`/`CURRENT_PROJECT_VERSION` were rewritten in (`project.yml`,
  `Project.swift`, one or more `*.xcconfig` files, or via `agvtool`/`project.pbxproj` sed), the old/new
  `CURRENT_PROJECT_VERSION` build number, and any per-target override left untouched that needs manual review
  (Step 4's note).
- Whether this was a `dry-run` (no file written) or an actual write.
- The Step 6 sanity-check result — `swift package dump-package` passed/failed for a library (this was actually run
  during this skill's own verification), or "not run — `xcodegen`/`tuist` unavailable, unverified locally" for an
  app (or the `agvtool what-version`/`what-marketing-version` read-back result for the `.xcodeproj`-only path).
- **Warn explicitly**: review the diff before committing (this skill doesn't commit or tag anything); for a
  library, the version-bearing artifact is the **git tag**, not any file this skill touched — nothing here
  substitutes for actually creating and pushing that tag; for an app, `CURRENT_PROJECT_VERSION` must never be
  reused once a build carrying it has been uploaded to App Store Connect, so re-running this skill against a value
  already shipped is not recoverable by re-running it again with a lower number; a `project.yml`/`Project.swift`
  value that's also overridden per-target was not touched and needs manual review; a README/Antora mention that
  pulls the version live from the Swift Package Index/App Store rather than hardcoding it should not have Step 8
  applied to it.

## Known quirks / verification notes

Verified in `$TMPDIR/iru-verify/swift/bump-version/`, using the local toolchain (Xcode 27.0, Swift 6.4, no `brew`
— `xcodegen`/`tuist` not installable in this environment, per this group's environment notes):

- **Step 1 regex**: `1.2.0` and `1.2.0-rc.1` match; `1.2`, `1.2.0 ` (trailing space), an empty string, and `abc`
  all correctly fail — exercised with `python3 -c` directly, all six cases behaved as documented above.
- **Step 3, `version.txt`**: a throwaway `1.0.0` file correctly became `1.2.0` after `printf '%s\n'
  "1.2.0" > version.txt`.
- **Step 3, README `.package(...)` snippets**: a sample README with both a `from: "1.0.0"` range-form and an
  `exact: "1.0.0"` pinned-form snippet — both replaced correctly to `"1.2.0"` in one run (`README replacements: 2`
  reported), confirming the single regex handles both keyword forms.
- **Step 3, `CHANGELOG.md` heading**: the first draft of the regex (`^## \[Unreleased\]\s*$`, matching only the
  heading's own line) left a **missing blank line** between the newly inserted `## [<version>] - <date>` heading
  and the following `### Added` subsection, because the blank line that originally followed `## [Unreleased]`
  stayed exactly where it was in the source text rather than moving with the heading. Fixed by widening the match
  to also consume any blank lines immediately following the heading
  (`^## \[Unreleased\]\s*\n(?:[ \t]*\n)*`) and re-inserting exactly the right blank lines in the replacement
  template — reverified against the same sample file, output now has the expected blank line before `### Added`,
  matching this catalog's `CHANGELOG.md`'s own Keep a Changelog formatting exactly (checked by diffing against the
  format used in this repository's real root `CHANGELOG.md`).
- **Step 4, `project.yml`**: a sample XcodeGen manifest with `settings: base: MARKETING_VERSION: 1.0.0` /
  `CURRENT_PROJECT_VERSION: 1` correctly became `1.2.0` / `2` after one run; a target-level
  `settings: base:` block with an unrelated key (`PRODUCT_BUNDLE_IDENTIFIER`) was correctly left untouched (the
  regex only matched the top-level occurrence, as intended — see Step 4's caveat about per-target overrides).
- **Step 4, `Project.swift`**: a sample Tuist manifest with `"MARKETING_VERSION": "1.0.0"` /
  `"CURRENT_PROJECT_VERSION": "1"` inside `settings: .settings(base: [...])` correctly became `"1.2.0"` / `"2"`.
- **Step 4, `*.xcconfig`**: a sample `Version.xcconfig` with `MARKETING_VERSION = 1.0.0` /
  `CURRENT_PROJECT_VERSION = 1` correctly became `MARKETING_VERSION = 1.2.0` / `CURRENT_PROJECT_VERSION = 2`.
- **Step 4, `agvtool`**: `xcrun agvtool help` confirmed present and documents exactly the subcommands this skill
  relies on (`new-marketing-version`, `new-version [-all]`, `what-version`, `what-marketing-version`). The actual
  `new-marketing-version`/`new-version -all` invocations and the `project.pbxproj` `sed` fallback were **not**
  exercised against a real `.xcodeproj` in this verification (building one from scratch outside Xcode's own
  project-creation flow was out of scope here) — the commands are documented from `agvtool help`'s own usage text
  and Apple's documented behavior, not independently confirmed end-to-end.
- **Step 5, pre-release convention**: `git describe --tags --abbrev=0` confirmed against a throwaway git repo —
  tag `1.1.0` on the first commit, a second commit on top, `git describe --tags --abbrev=0` correctly returns
  `1.1.0` (the last reachable tag, ignoring the untagged commit on top of it).
- **Step 6, library**: `swift package dump-package` against the throwaway `DemoLib` package (a minimal library
  product/target with a Swift Testing test) exits `0` and prints the expected JSON (name, platforms, products,
  targets) — confirmed working end-to-end.
- **Step 6, app**: **unverified locally** — no `xcodegen`/`tuist` binary available in this environment (no
  `brew`); the `project.yml`/`Project.swift`/`*.xcconfig` rewrites themselves were verified directly (see above),
  but the generate-and-inspect round-trip (`xcodegen generate` → `xcodebuild -showBuildSettings | grep
  MARKETING_VERSION`) was not exercised.
- **Step 7, dry-run diff mechanism**: discovered and documented inline in Step 7 above — a shell `diff -u <(cat
  original) <(printf '%s' "$var")` one-liner silently drops the file's trailing newline once the new content has
  passed through a bash command substitution, producing a spurious "no newline at end of file" diff line; computing
  the diff inside the same `python3` process that built the replacement text avoids this.
- **Step 3b, command-line tool** (verified 2026-10-16 in `$TMPDIR/iru-verify/cli/swift/iru-swift-bump-version/`, Swift
  6.4): on a copy of an `iru-setup-swift-cli` scaffold, `--list` found only `Sources/MyToolKit/Version.swift`
  (`'0.1.0-dev'`); `--dry-run 0.1.0` printed a one-line diff and wrote nothing; `0.1.0` rewrote it, `swift build`
  succeeded and `my-tool --version` printed `0.1.0`; `0.2.0-dev` then rewrote it again. On a second package with no
  `Version.swift` and `CommandConfiguration(abstract: "Does things (fast).", version: "1.2.3-dev", …)` plus a
  `static let apiVersion = "2.0.0"`, only the `CommandConfiguration` literal changed (parentheses in the abstract
  didn't confuse it; `apiVersion` untouched). A package with no literal exits 1 with "no version literal found".
