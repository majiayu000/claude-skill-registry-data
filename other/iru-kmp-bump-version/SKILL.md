---
name: iru-kmp-bump-version
description: >-
  Set a Kotlin Multiplatform (Android + iOS) app's version to an exact value across both platforms — the root
  `gradle.properties` `VERSION_NAME` (and, only for a release value, `VERSION_CODE` incremented by one), plus, only
  for a release value, the iOS host app's `iosApp/Configuration/Config.xcconfig` `MARKETING_VERSION` (set to the
  release) and `CURRENT_PROJECT_VERSION` (set to the new `VERSION_CODE`) — never writing a `-SNAPSHOT` value into
  any iOS file, since App Store Connect rejects it. Detects the layout at runtime and falls back, when the
  `iru-setup-kmp-app` layout isn't present, to `versionName`/`versionCode` literals in the Android app module's
  `build.gradle(.kts)` (`androidApp/`, `composeApp/`, `app/`), the `gradle/libs.versions.toml` `[versions]` entries
  the build reads them from, XcodeGen `project.yml` settings, a literal `Info.plist`
  `CFBundleShortVersionString`/`CFBundleVersion`, or a committed `project.pbxproj` `MARKETING_VERSION`. Invoke as
  `/iru-kmp-bump-version <new-version>` where `<new-version>` is the literal target version (`1.2.0` or
  `1.3.0-SNAPSHOT`) — this skill never computes a bump itself; `iru-release` computes the release/next-dev values per
  the pre-release convention in Step 5 and passes each one through. Also accepts `args`: `sync-files: yes|no`
  (default: ask) to also update README/Antora version mentions, `next-version: <upcoming-version>` so that sync maps
  "Latest release" markers to `<new-version>` and "Current development version"/"Latest snapshot" markers to the
  upcoming value, and `dry-run: yes|no` (default `no`) to print the diff without writing anything. Reports the old
  and new values of every field and every file touched. Equivalent to `iru-android-bump-version`/
  `iru-swift-bump-version` for a KMP app. Use whenever the user, or `iru-release`, needs a KMP app's version set to a
  specific value instead of hand-editing Gradle properties and Xcode build settings.
model: haiku
allowed-tools: Read Bash(python3 *) Bash(./gradlew *) Bash(grep *) Bash(find *) Bash(ls *) Bash(cat *) Bash(git ls-files *) Bash(git diff *) Bash(xcodebuild *) Bash(xcodegen *) Bash(/usr/libexec/java_home *)
---

# KMP Bump Version

Set a Kotlin Multiplatform app's version to an exact value in every file that must agree with it — the shared
Gradle side (read by the Android app) and the iOS host app's Xcode build settings. This skill never computes a
version itself: it applies exactly the version string it's given, validated for shape. The "which version comes
next" logic belongs to the caller and is defined in Step 5, mirroring `iru-android-bump-version`'s Step 5 (the
Android `-SNAPSHOT` + `versionCode` rule) and `iru-swift-bump-version`'s Step 4 (`MARKETING_VERSION` +
`CURRENT_PROJECT_VERSION`). It never commits, tags, or regenerates anything beyond the sanity check in Step 6.

## Step 0 — Resolve inputs

- The positional argument is `<new-version>` — the exact target string (e.g. `1.2.0`, `1.3.0-SNAPSHOT`). If it's
  missing, ask the user for it before doing anything else; never guess or compute one here.
- `args` (`key: value` lines), if present:
  - `sync-files: yes|no` — whether to also update README/Antora version mentions (Step 8). If omitted, ask once
    with `AskUserQuestion` after Step 2 confirms such mentions exist; skip asking when none do.
  - `next-version: <upcoming-version>` — the upcoming pre-release value (e.g. `1.3.0-SNAPSHOT`) that "Current
    development version"/"Latest snapshot"-style markers should show after a release, while "Latest release"
    markers show `<new-version>`. Only meaningful with `sync-files: yes`; `iru-release` passes it so a release never
    regresses a development marker to the release value.
  - `dry-run: yes|no` — default `no`. When `yes`, compose every change, print the diffs (Step 7), and stop without
    writing anything or running Step 6 — say plainly in the report that nothing was modified.

Reject, before touching anything, a `<new-version>` that is obviously not a version (empty, or contains
whitespace). Throughout this skill, **release** means `<new-version>` is exactly `X.Y.Z` (three dot-separated
integers, `re.fullmatch(r"\d+\.\d+\.\d+", v)`); **snapshot** means anything else — `-SNAPSHOT`, but also any other
pre-release suffix (`-rc.1`, `-beta`) the user chose to proceed with in Step 1. A snapshot never bumps a version code
and never reaches an iOS file, which is how the hard rule in Step 1 is enforced rather than merely stated.

## Step 1 — Validate the version string

`VERSION_NAME`/`versionName` are free-form strings to Gradle and `MARKETING_VERSION` is free-form to Xcode, so there
is no build-tool validator to lean on. Validate with this catalog's convention, Maven-style `X.Y.Z` or
`X.Y.Z-SNAPSHOT` (the same regex as `iru-android-bump-version`):

```bash
python3 -c 'import re,sys; v=sys.argv[1]; sys.exit(0 if re.fullmatch(r"\d+\.\d+\.\d+(-SNAPSHOT)?", v) else 1)' "<new-version>"
```

If it doesn't match, warn that the value doesn't follow the `X.Y.Z`/`X.Y.Z-SNAPSHOT` convention and ask whether to
proceed anyway — don't hard-stop on a plausible but different scheme. One hard rule regardless: a value carrying
**any** pre-release suffix (`-SNAPSHOT`, `-rc.1`, `-beta`, …) is never written to an iOS file (Step 4) — App Store
Connect requires `CFBundleShortVersionString` to be one to three period-separated integers.

## Step 2 — Survey where the version lives

Find every version source before writing anything, so Steps 3–4 neither miss one nor double-bump another:

```bash
grep -nE '^[[:space:]]*VERSION_(NAME|CODE)[[:space:]]*[=:]' gradle.properties 2>/dev/null
find . -path ./build -prune -o -name '*.xcconfig' -not -path '*/build/*' -not -path '*/Pods/*' -print \
  | xargs grep -nE '^[[:space:]]*(MARKETING_VERSION|CURRENT_PROJECT_VERSION)[[:space:]]*=' 2>/dev/null
grep -rnE 'versionName|versionCode' --include=build.gradle.kts --include=build.gradle . 2>/dev/null | grep -v '/build/'
grep -nE '^[[:space:]]*[A-Za-z0-9_.-]*[vV]ersion-?([nN]ame|[cC]ode)[[:space:]]*=' gradle/libs.versions.toml 2>/dev/null
grep -nE 'MARKETING_VERSION|CURRENT_PROJECT_VERSION' iosApp/project.yml project.yml 2>/dev/null
find . -name Info.plist -not -path '*/build/*' -not -path '*/Pods/*' | xargs grep -nA1 -E 'CFBundleShortVersionString|CFBundleVersion' 2>/dev/null
find . -name project.pbxproj -not -path '*/build/*' | xargs grep -c 'MARKETING_VERSION' 2>/dev/null
```

Classify what you found:

- **Gradle side** — the first match in this order is the source of truth:
  1. **`gradle.properties` `VERSION_NAME`** (+ `VERSION_CODE`) — the `iru-setup-kmp-app` layout; the Android app
     module reads them (`versionName = providers.gradleProperty("VERSION_NAME")…`/`project.property(…)`). Step 3a.
  2. **`gradle/libs.versions.toml` entries** — the app module's `versionName`/`versionCode` read
     `libs.versions.<accessor>.get()`. Map the accessor back to its TOML key (`libs.versions.app.versionName` ↔
     `app-versionName`/`app_versionName`/`app.versionName` — Gradle normalizes `-`, `_`, `.` to the same accessor) and
     rewrite that key. Step 3b.
  3. **String/integer literals** in the Android application module's build script — `androidApp/` (this catalog's
     layout), `composeApp/` (the JetBrains wizard's single-module layout), or `app/`, whichever applies
     `com.android.application`. Step 3c.
  Never rewrite a `versionName = …` line that reads a property/catalog value — rewrite the source it reads.
- **iOS side** — first match in this order:
  1. **`iosApp/Configuration/Config.xcconfig`** (or any `*.xcconfig` holding literal `MARKETING_VERSION`/
     `CURRENT_PROJECT_VERSION`) — the `iru-setup-kmp-app` layout and the JetBrains wizard's. Step 4a. An xcconfig whose
     values are `$(VERSION_NAME)`-style references is not a source — follow the reference.
  2. **XcodeGen `project.yml`** `settings: base:` keys (when the project doesn't route them through an xcconfig).
     Step 4b.
  3. **A literal `Info.plist`** `CFBundleShortVersionString`/`CFBundleVersion` (not `$(MARKETING_VERSION)`). Step 4c.
  4. **A committed `project.pbxproj`** (`git ls-files '*.pbxproj'` lists it) with literal `MARKETING_VERSION` — only
     when nothing above owns the value. A `.xcodeproj` regenerated from `project.yml` is never edited (the next
     `xcodegen generate` would overwrite it). Step 4d.
- **Nothing on the Gradle side** → hard stop: say no `VERSION_NAME`, catalog entry, or `versionName` literal was found
  and ask for the correct location — don't silently do nothing. **Nothing on the iOS side** → not a stop (a KMP
  library module, or an Android-only checkout) — note "no iOS version source found" in the report.
- Also check for Step 8 candidates (`grep -nE '[0-9]+\.[0-9]+\.[0-9]+' README.md docs/antora.yml 2>/dev/null`).

## Step 3 — Rewrite the Gradle side

Every snippet below takes a trailing `yes|no` dry-run flag, composes the new text in memory, and either prints a
unified diff computed inside the same `python3` process (avoiding the trailing-newline loss
`iru-swift-bump-version`'s Step 7 documents for shell `diff <(…)` round-trips) or writes the file. Run them from the
repository root.

**3a — `gradle.properties`** (primary). `VERSION_NAME` always becomes `<new-version>`; `VERSION_CODE` is incremented
by exactly 1 **only for a release** and left unchanged for a snapshot (Step 5 explains why):

```bash
python3 - gradle.properties "<new-version>" "<dry-run>" <<'PY'
import re, sys, difflib
path, new_version, dry = sys.argv[1], sys.argv[2], sys.argv[3] == "yes"
release = re.fullmatch(r"\d+\.\d+\.\d+", new_version) is not None
orig = text = open(path).read()
name = re.search(r'(?m)^[ \t]*VERSION_NAME[ \t]*[=:][ \t]*([^\r\n]*)$', text)
if not name:
    sys.exit(f"VERSION_NAME not found in {path}")
old_name = name.group(1).strip()
text = text[:name.start(1)] + new_version + text[name.end(1):]
code = re.search(r'(?m)^[ \t]*VERSION_CODE[ \t]*[=:][ \t]*(\d+)[ \t]*$', text)
old_code = new_code = int(code.group(1)) if code else None
if code and release:
    new_code = old_code + 1
    text = text[:code.start(1)] + str(new_code) + text[code.end(1):]
if dry:
    sys.stdout.writelines(difflib.unified_diff(orig.splitlines(True), text.splitlines(True), path, path))
elif text != orig:
    open(path, "w").write(text)
print(f"VERSION_NAME {old_name} -> {new_version}; VERSION_CODE {old_code} -> {new_code}"
      + ("" if code else " (no VERSION_CODE key)") + (" [dry-run]" if dry else ""))
PY
```

Note the printed new `VERSION_CODE` — Step 4 writes it into `CURRENT_PROJECT_VERSION`.

**3b — `gradle/libs.versions.toml`** (fallback). Run once for the name key with the literal value and, for a release
only, once for the code key with `+1`:

```bash
python3 - gradle/libs.versions.toml "<versionName key>" "<new-version>" "<dry-run>" <<'PY'
import re, sys, difflib
path, key, value, dry = sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4] == "yes"
orig = text = open(path).read()
m = re.search(r'(?m)^[ \t]*' + re.escape(key) + r'[ \t]*=[ \t]*"([^"]*)"', text)
if not m:
    sys.exit(f'{key} = "..." not found in {path}')
old = m.group(1)
new = str(int(old) + 1) if value == "+1" else value
text = text[:m.start(1)] + new + text[m.end(1):]
if dry:
    sys.stdout.writelines(difflib.unified_diff(orig.splitlines(True), text.splitlines(True), path, path))
elif text != orig:
    open(path, "w").write(text)
print(f"{key} {old} -> {new}" + (" [dry-run]" if dry else ""))
PY
# release only:
python3 - gradle/libs.versions.toml "<versionCode key>" "+1" "<dry-run>" <<'PY'
…same script…
PY
```

**3c — literals in the Android app module's build script** (fallback; Kotlin DSL `versionName = "…"`/
`versionCode = 12` or Groovy `versionName "…"`/`versionCode 12`). `versionCode` increments only for a release:

```bash
python3 - <module>/build.gradle.kts "<new-version>" "<dry-run>" <<'PY'
import re, sys, difflib
path, new_version, dry = sys.argv[1], sys.argv[2], sys.argv[3] == "yes"
release = re.fullmatch(r"\d+\.\d+\.\d+", new_version) is not None
orig = text = open(path).read()
name = re.search(r'''(versionName\s*=?\s*)(["'])([^"']*)\2''', text)
if not name:
    sys.exit(f"no versionName string literal in {path} (it may read a property - bump that source instead)")
old_name = name.group(3)
code = re.search(r'(versionCode\s*=?\s*)(\d+)\b', text)
old_code = new_code = int(code.group(2)) if code else None
edits = [(name.start(3), name.end(3), new_version)]
if code and release:
    new_code = old_code + 1
    edits.append((code.start(2), code.end(2), str(new_code)))
for start, end, value in sorted(edits, reverse=True):
    text = text[:start] + value + text[end:]
if dry:
    sys.stdout.writelines(difflib.unified_diff(orig.splitlines(True), text.splitlines(True), path, path))
elif text != orig:
    open(path, "w").write(text)
print(f"versionName {old_name} -> {new_version}; versionCode {old_code} -> {new_code}"
      + ("" if code else " (no versionCode literal)") + (" [dry-run]" if dry else ""))
PY
```

If a project's convention differs (e.g. `versionCode` bumped on every call, or derived from a CI build number),
that's the user's explicit call before this step runs — never silently apply a different rule than the one
documented here, and say which rule was applied in the report.

## Step 4 — Rewrite the iOS side (release values only)

**Skip this whole step for a snapshot** (any value that isn't plain `X.Y.Z` — see Step 0) and say so in the report ("iOS version left at `<current>` — `-SNAPSHOT`
values are never written to Xcode build settings"). For a release, `MARKETING_VERSION` becomes `<new-version>` and
`CURRENT_PROJECT_VERSION` becomes **the new `VERSION_CODE` from Step 3** (so Android `versionCode` and the iOS build
number stay identical); when the Gradle side has no version code at all, pass an empty string and the snippets fall
back to the current build number + 1. Pass `+1` for that fallback in 4c.

**4a — `*.xcconfig`** (primary: `iosApp/Configuration/Config.xcconfig`). Accepts `KEY=value` and `KEY = value`, keeps
trailing `//` comments, and refuses (exit 1) when the value is a `$(…)` reference:

```bash
python3 - iosApp/Configuration/Config.xcconfig "<new-version>" "<new VERSION_CODE or empty>" "<dry-run>" <<'PY'
import re, sys, difflib
path, new_version, new_code, dry = sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4] == "yes"
orig = text = open(path).read()
mv = re.search(r'(?m)^[ \t]*MARKETING_VERSION[ \t]*=[ \t]*([^\s/]*)', text)
cpv = re.search(r'(?m)^[ \t]*CURRENT_PROJECT_VERSION[ \t]*=[ \t]*([^\s/]*)', text)
if not mv or not cpv:
    sys.exit(f"MARKETING_VERSION/CURRENT_PROJECT_VERSION not both found in {path}")
if mv.group(1).startswith("$(") or not cpv.group(1).isdigit():
    sys.exit(f"{path} derives the version from another setting ({mv.group(1)} / {cpv.group(1)}) - edit that source instead")
old_mv, old_cpv = mv.group(1), int(cpv.group(1))
target_cpv = int(new_code) if new_code else old_cpv + 1
# replace from the end so earlier offsets stay valid
for m, value in sorted([(mv, new_version), (cpv, str(target_cpv))], key=lambda p: p[0].start(1), reverse=True):
    text = text[:m.start(1)] + value + text[m.end(1):]
if dry:
    sys.stdout.writelines(difflib.unified_diff(orig.splitlines(True), text.splitlines(True), path, path))
elif text != orig:
    open(path, "w").write(text)
print(f"MARKETING_VERSION {old_mv} -> {new_version}; CURRENT_PROJECT_VERSION {old_cpv} -> {target_cpv}" + (" [dry-run]" if dry else ""))
PY
```

**4b — XcodeGen `project.yml`** (fallback) — reuse `iru-swift-bump-version`'s Step 4 `project.yml` snippet, but set
`CURRENT_PROJECT_VERSION` to the new `VERSION_CODE` instead of `+1` when one exists. Then the `.xcodeproj` must be
regenerated (`xcodegen generate --spec iosApp/project.yml`) before the change shows up in Xcode — Step 6 does that
when `xcodegen` is installed.

**4c — literal `Info.plist`** (fallback). `$(…)` references are reported and left untouched (the real value lives in
a build setting — find it):

```bash
python3 - iosApp/iosApp/Info.plist "<new-version>" "<new VERSION_CODE or +1>" "<dry-run>" <<'PY'
import re, sys, difflib
path, new_version, new_code, dry = sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4] == "yes"
orig = text = open(path).read()
out = []
for key, value in (("CFBundleShortVersionString", new_version), ("CFBundleVersion", new_code)):
    m = re.search(r'<key>' + key + r'</key>\s*<string>([^<]*)</string>', text)
    if not m:
        out.append(f"{key}: absent")
        continue
    if m.group(1).startswith("$("):
        out.append(f"{key}: {m.group(1)} (build-setting reference, left untouched)")
        continue
    if value == "+1":
        value = str(int(m.group(1)) + 1)
    text = text[:m.start(1)] + value + text[m.end(1):]
    out.append(f"{key}: {m.group(1)} -> {value}")
if dry:
    sys.stdout.writelines(difflib.unified_diff(orig.splitlines(True), text.splitlines(True), path, path))
elif text != orig:
    open(path, "w").write(text)
print("; ".join(out) + (" [dry-run]" if dry else ""))
PY
```

**4d — committed `project.pbxproj`** (last resort). Rewrites **every** occurrence (one per build configuration and
target), quoted or not, and sets every `CURRENT_PROJECT_VERSION` to the same value:

```bash
python3 - iosApp/iosApp.xcodeproj/project.pbxproj "<new-version>" "<new VERSION_CODE or empty>" "<dry-run>" <<'PY'
import re, sys, difflib
path, new_version, new_code, dry = sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4] == "yes"
orig = text = open(path).read()
codes = [int(c) for c in re.findall(r'CURRENT_PROJECT_VERSION = "?(\d+)"?;', text)]
target = new_code if new_code else str(max(codes) + 1 if codes else 1)
text, n_mv = re.subn(r'(MARKETING_VERSION = )("?)[^;"]+\2;', lambda m: f'{m.group(1)}{m.group(2)}{new_version}{m.group(2)};', text)
text, n_cpv = re.subn(r'(CURRENT_PROJECT_VERSION = )("?)\d+\2;', lambda m: f'{m.group(1)}{m.group(2)}{target}{m.group(2)};', text)
if n_mv == 0:
    sys.exit(f"MARKETING_VERSION not found in {path}")
if dry:
    sys.stdout.writelines(difflib.unified_diff(orig.splitlines(True), text.splitlines(True), path, path))
elif text != orig:
    open(path, "w").write(text)
print(f"MARKETING_VERSION x{n_mv} -> {new_version}; CURRENT_PROJECT_VERSION x{n_cpv} {sorted(set(codes))} -> {target}" + (" [dry-run]" if dry else ""))
PY
```

`xcrun agvtool new-marketing-version`/`new-version -all` (see `iru-swift-bump-version`'s Step 4) are an alternative
for a hand-maintained `.xcodeproj` using `VERSIONING_SYSTEM = apple-generic`.

## Step 5 — The KMP-catalog pre-release convention (for `iru-release` and other callers)

The KMP equivalent of the Android catalog's `-SNAPSHOT` convention (`iru-android-bump-version`'s Step 5), applied to
two platforms at once. `iru-release` reads the current version from `gradle.properties` `VERSION_NAME` (Step 2's
Gradle-side source of truth — the iOS `MARKETING_VERSION` always shows the **last release**, never the development
version) and calls this skill with each computed value:

- **Current development version**: `x.y.z-SNAPSHOT` in `VERSION_NAME` (e.g. `1.2.0-SNAPSHOT`) on `develop`; iOS
  `MARKETING_VERSION` meanwhile still holds the previous release (e.g. `1.1.0`).
- **Cutting a release**: strip `-SNAPSHOT` — call with `<new-version>: x.y.z`. This is the only call that changes
  build numbers: `VERSION_CODE` += 1, `MARKETING_VERSION` = `x.y.z`, `CURRENT_PROJECT_VERSION` = the new
  `VERSION_CODE`. A store build (Play Store `versionCode`, App Store Connect `CFBundleVersion`) can never reuse a
  build number, and snapshot builds are never uploaded — so burning numbers on snapshot bumps would waste
  irrecoverable values.
- **Opening the next development cycle**: call with `<new-version>: x.y.(z+1)-SNAPSHOT` (or the minor/major bump the
  caller chose) — only `VERSION_NAME` changes; `VERSION_CODE` and every iOS value stay as the release left them.
  The `sync.yml` workflow that `iru-setup-kmp-github-workflows` generates performs this second call after a
  release when present (see `iru-release`'s Step 4).

## Step 6 — Sanity check

After writing (never for `dry-run: yes`):

```bash
export JAVA_HOME="$(/usr/libexec/java_home -v 21)"   # or -v 17; the default JDK may be newer than AGP supports
./gradlew -q help                                    # build scripts still configure
./gradlew -q :<android-app-module>:properties | grep -E '^(VERSION_NAME|VERSION_CODE):'   # gradle.properties layout
```

A non-zero exit or a Kotlin-script compile error means a rewrite broke something — stop, show the error, and don't
report success. For the iOS side, `grep -n 'MARKETING_VERSION\|CURRENT_PROJECT_VERSION' <file>` reads back what was
written; when `iosApp/project.yml` exists and `xcodegen` is on `PATH`, also run `xcodegen generate --spec
iosApp/project.yml` and `xcodebuild -showBuildSettings -project iosApp/iosApp.xcodeproj -scheme iosApp | grep -E
'MARKETING_VERSION|CURRENT_PROJECT_VERSION'` to confirm the xcconfig value round-trips — otherwise report that
round-trip as "not run (xcodegen not installed)".

## Step 7 — Preview (`dry-run: yes`) or write

Pass `yes` as each snippet's dry-run argument to print the diffs without writing; pass `no` to write. With
`dry-run: yes`, run every applicable snippet (Steps 3, 4 and, if accepted, 8), skip Step 6, and state plainly that
this was a preview only. Note that a dry-run of Step 4 must use the `VERSION_CODE` value Step 3's dry-run printed,
since nothing was written for it to re-read.

## Step 8 — Optionally sync other files that mirror the version

Ask (or honor `args: sync-files`) whether to also update README/Antora mentions, the same way
`iru-android-bump-version`'s Step 8 does. **Marker mapping** (same rule as `iru-java-bump-version`'s Step 7): "Latest
release"/"Current release" markers → `<new-version>` when it is a release, untouched for a snapshot; "Current
development version"/"Latest snapshot" markers → `next-version` when given, otherwise `<new-version>` only if it is
a snapshot, and untouched (with a warning that the caller should pass `next-version`) when it is a release — never
regress a development marker to a release value; an `implementation("group:artifact:version")` snippet (a KMP
library module published alongside the app) → `<new-version>`.

- **`README.md`** — line-based, markers matched case-insensitively (snippet below the list).
- **`docs/antora.yml`** — its `version:` field only for a release (never a snapshot — this catalog's convention,
  matching `iru-release` and every other bump-version skill), and only if that field is meant to track releases
  (an Antora component versioned `~` or by branch is left alone).
- **Antora pages** under `docs/modules/ROOT/pages/` naming a literal version (`grep -rlE
  '[0-9]+\.[0-9]+\.[0-9]+' docs/modules/ROOT/pages/*.adoc`) — run the README snippet against each, after showing the
  matches.

```bash
python3 - README.md "<new-version>" "<next-version or empty>" "<dry-run>" <<'PY'
import re, sys, difflib
path, new_version, next_version, dry = sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4] == "yes"
release = re.fullmatch(r"\d+\.\d+\.\d+", new_version) is not None
VER = r'\d+\.\d+\.\d+(?:-SNAPSHOT)?'
orig = open(path).read()
out, notes = [], []
for line in orig.splitlines(True):
    low = line.lower()
    if re.search(r'snapshot|development version|dev version', low) and not re.search(r'implementation', low):
        target = next_version or (new_version if not release else None)
        if target is None:
            notes.append(f"left development marker untouched (pass next-version): {line.strip()}")
    elif re.search(r'latest release|current release|latest version', low):
        target = new_version if release else None
    elif re.search(r'''implementation\s*\(?["']''', line):
        target = new_version
        line = re.sub(r'''(implementation\s*\(?["'][^:"']+:[^:"']+:)[^"']+(["'])''',
                      lambda m: f"{m.group(1)}{target}{m.group(2)}", line)
        out.append(line)
        continue
    else:
        target = None
    if target:
        line = re.sub(VER, target, line)
    out.append(line)
text = "".join(out)
if dry:
    sys.stdout.writelines(difflib.unified_diff(orig.splitlines(True), text.splitlines(True), path, path))
elif text != orig:
    open(path, "w").write(text)
changed = sum(1 for a, b in zip(orig.splitlines(), text.splitlines()) if a != b)
print(f"{path}: {changed} line(s) changed" + (" [dry-run]" if dry else ""))
for n in notes:
    print("NOTE", n)
PY
```

Offered, not automatic — a store badge that pulls the version live must not be rewritten; don't touch anything the
user didn't confirm.

## Step 9 — Report

- Old → new for every field touched: `VERSION_NAME`, `VERSION_CODE` (incremented, or "unchanged — snapshot"),
  `MARKETING_VERSION`/`CURRENT_PROJECT_VERSION` (and the file), or "iOS untouched — snapshot" / "no iOS version
  source found"; which fallback (3b/3c/4b/4c/4d) was used instead of the primary layout and why.
- Step 8 files accepted, with the marker lines changed and any development marker left untouched.
- Dry-run (nothing written) or actual write, and the Step 6 result.
- **Warn explicitly**: review the diff before committing (this skill never commits or tags); build numbers can never
  be reused once a build carrying them reached Google Play or App Store Connect, so re-running a release bump is not
  undone by bumping down; per-target overrides of `MARKETING_VERSION`/`CURRENT_PROJECT_VERSION` in `project.yml` or
  `project.pbxproj` beyond the first occurrence (4b) need manual review; a `.xcodeproj` generated from `project.yml`
  must be regenerated before Xcode sees the change.

## Verification notes

Verified in `$TMPDIR/iru-verify/kmp/iru-kmp-bump-version/` (October 2026, Python 3, macOS) — every snippet above was
run with `python3 -I` against sample files covering the primary layout and each fallback:

- **3a + 4a, release `1.2.0-SNAPSHOT` → `1.2.0`**: `VERSION_NAME=1.2.0`, `VERSION_CODE` `7 → 8`;
  `Config.xcconfig` `MARKETING_VERSION=1.1.0 → 1.2.0`, `CURRENT_PROJECT_VERSION=7 → 8`, the `//` comment and other
  keys untouched. **Snapshot `1.2.0` → `1.3.0-SNAPSHOT`**: only `VERSION_NAME` changed, `VERSION_CODE` stayed `8`.
  The dry-run flag printed the diff and left the file byte-identical (`git diff --no-index` empty).
- **4a edge cases**: `MARKETING_VERSION = 1.0.0 // trailing` (spaces + comment) rewritten in place keeping the
  comment; `$(VERSION_NAME)`/`$(VERSION_CODE)` references refused with exit 1.
- **3b**: `app-versionName = "3.1.0-SNAPSHOT"` → `"3.1.0"`, `app-versionCode = "40"` → `"41"` with `+1`.
- **3c**: Kotlin DSL `versionName = "2.0.0-SNAPSHOT"`/`versionCode = 12` — snapshot left the code at 12, release set
  `2.0.0`/`13`; Groovy `versionCode 4`/`versionName "1.0"` → `5`/`"1.1.0"`; a `versionName =
  project.property("VERSION_NAME") as String` script (the verification project's real `androidApp`) is refused with
  "no versionName string literal" rather than mangled.
- **4c**: literal `<string>1.0</string>`/`<string>3</string>` → `1.2.0`/`4`; `$(MARKETING_VERSION)`/
  `$(CURRENT_PROJECT_VERSION)` reported and left untouched. **4d**: two build configurations' `MARKETING_VERSION = 1.0;`/
  `CURRENT_PROJECT_VERSION = 5;` all rewritten to `1.2.0`/`6`.
- **Step 8**: a README with `| Latest release | 1.1.0 |`, `| Current development version | 1.2.0-SNAPSHOT |` and an
  `implementation("com.example:shared:1.1.0")` snippet — release `1.2.0` + `next-version 1.3.0-SNAPSHOT` → `1.2.0` /
  `1.3.0-SNAPSHOT` / `1.2.0`; release without `next-version` left the development row untouched and printed the
  NOTE; snapshot `1.3.0-SNAPSHOT` left "Latest release" untouched.
- **Step 6**: after the 3a rewrite of the verification KMP project's real `gradle.properties` (`$TMPDIR/iru-verify/kmp/iru-kmp-dokka/`, Gradle 9.8.1, AGP 9.4.1, Kotlin 2.4.21, JDK 21), `./gradlew -q help` exited 0 and `./gradlew -q :androidApp:properties` printed `VERSION_CODE: 8` / `VERSION_NAME: 1.2.0` — the app module reads the new values.
- **Not verified locally**: the XcodeGen round-trip (`xcodegen` isn't installed here), `agvtool` against a real
  `.xcodeproj`, and the 4b `project.yml` rewrite inside a KMP repository (the snippet itself is
  `iru-swift-bump-version`'s, verified there).
