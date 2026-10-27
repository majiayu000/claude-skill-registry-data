---
name: iru-android-bump-version
description: "/iru-android-bump-version <new-version> sets an Android library/app project's version to the literal value given: libraryVersion in lib/build.gradle.kts, versionName/versionCode in app/build.gradle.kts, optionally README/Antora mentions. Args: sync-files: yes|no, dry-run: yes|no. Reports old/new version and files touched."
model: haiku
---

# Android Bump Version

Set an Android (Gradle/Kotlin) project's version to an exact value across every file that needs to agree with it:
`lib/build.gradle.kts`'s `libraryVersion`, `app/build.gradle.kts`'s `versionName` (and, per the rule in Step 4,
`versionCode`), and — optionally — `README.md`/Antora version mentions. This skill never computes a version itself
— it applies exactly the version string it's given, validated for shape. The "which version to compute next"
logic (release vs. pre-release bump) belongs to the caller and is defined in Step 5 below, mirroring
`iru-typescript-bump-version`'s Step 5 for the npm ecosystem and this catalog's existing Maven `-SNAPSHOT`
convention (`iru-release`) for the Java ecosystem.

## Step 0 — Resolve inputs

**Kotlin Multiplatform projects are out of scope.** If the Kotlin Multiplatform plugin (`kotlin("multiplatform")`/`org.jetbrains.kotlin.multiplatform`, directly or via a `libs.versions.toml` alias) is applied anywhere in the build — a KMP app's Android host module included — stop and hand the request to `iru-kmp-bump-version` instead (or tell the caller to, when it isn't installed); this skill assumes a plain Android `lib`/`app` layout.

Parse the invocation:

- The positional argument is `<new-version>` — the exact target version string (e.g. `1.2.0`, `1.2.0-SNAPSHOT`).
  If it's missing, ask the user for it before doing anything else; don't guess or compute one here.
- `args` (`key: value` lines), if present:
  - `sync-files: yes|no` — whether to also update README/Antora version mentions (Step 8). If omitted, ask once
    with `AskUserQuestion` after Step 2 confirms whether such mentions actually exist; skip asking if none do.
  - `next-version: <upcoming-version>` — the upcoming pre-release version (e.g. `1.5.0-SNAPSHOT`) that README/
    Antora "Latest snapshot"/"Current development version"-style markers should show after a release, while
    "Latest release" markers show `<new-version>`. Only meaningful with `sync-files: yes`; `iru-release` passes it
    so a release never regresses a development marker to the release value (see Step 8).
  - `dry-run: yes|no` — default `no`. When `yes`, run every step through composing the new file contents and
    showing the diff (Step 7), then stop — do not write anything, and say so plainly in the report.

Reject, before touching anything, a `<new-version>` that is obviously not attempting a version at all (empty
string, or contains whitespace) with a short message asking for a valid value — Step 1 validates the actual shape.

## Step 1 — Validate the version string

Android's `libraryVersion`/`versionName` are free-form strings (Gradle doesn't parse or validate them the way npm
parses semver), so there is no build-tool command to lean on for validation the way
`npm version <v> --no-git-tag-version` does for `iru-typescript-bump-version`. Validate with a regex instead —
this catalog's convention (Step 5) is Maven-style `X.Y.Z` or `X.Y.Z-SNAPSHOT`:

```bash
python3 -c 'import re,sys; v=sys.argv[1]; sys.exit(0 if re.fullmatch(r"\d+\.\d+\.\d+(-SNAPSHOT)?", v) else 1)' "<new-version>"
```

If it doesn't match, warn the user the value doesn't follow this catalog's `X.Y.Z`/`X.Y.Z-SNAPSHOT` convention and
ask whether to proceed anyway (some projects intentionally use a different scheme, e.g. a `-rc.N`/`-alpha.N`
suffix, or a purely numeric `versionCode`-style scheme for an app-only project) — don't hard-stop on a
non-matching but plausible string, only flag it.

## Step 2 — Survey which modules exist

- `lib/build.gradle.kts` exists → this is (or includes) a library module; Step 3 applies to it.
- `app/build.gradle.kts` exists → this is (or includes) an app module; Step 4 applies to it.
- Neither existing is a hard stop: tell the user neither module's build script was found at the expected path and
  ask for the correct path(s), or whether the project uses a different module layout than this catalog's
  `iru-setup-android-library`/`iru-setup-android-app` scaffold produces — don't silently do nothing.
- Also note, for Step 3's `mavenPublishing { coordinates(…) }` block and Step 6, whether `publish: yes` was used
  at scaffold time (the `mavenPublishing` block only exists in `lib/build.gradle.kts` when it was) — this doesn't
  change what gets rewritten (the version is only read from `libraryVersion`, `coordinates(…)` references that same
  `val`, not a separate literal), but is useful context for the report.

## Step 3 — Read and rewrite `lib/build.gradle.kts` (`val libraryVersion = "…"`)

Read the current value first so the diff is visible even if a later step fails partway through:

```bash
grep -n 'val libraryVersion = ' lib/build.gradle.kts
```

Rewrite it with a `python3` one-liner (safe identically on macOS and Linux — no BSD-vs-GNU `sed -i` flag
differences to worry about):

```bash
python3 - "lib/build.gradle.kts" "<new-version>" <<'PY'
import re, sys
path, new_version = sys.argv[1], sys.argv[2]
text = open(path).read()
new_text, n = re.subn(
    r'(val libraryVersion = )"[^"]*"',
    lambda m: f'{m.group(1)}"{new_version}"',
    text, count=1,
)
if n == 0:
    sys.exit(f"libraryVersion pattern not found in {path}")
open(path, "w").write(new_text)
PY
```

If the sed/Perl equivalent is preferred and available, the macOS-and-Linux-safe form (BSD `sed` requires an
argument after `-i`, GNU `sed` treats a bare `-i` differently — `-i.bak` plus deleting the backup works
identically on both) is:

```bash
sed -i.bak -E 's/(val libraryVersion = )"[^"]*"/\1"<new-version>"/' lib/build.gradle.kts && rm lib/build.gradle.kts.bak
```

`coordinates("<group>", "<artifact>", libraryVersion)` inside the `mavenPublishing` block (when `publish: yes` at
scaffold time) already references the `val`, not a literal — nothing else to change there.

## Step 4 — Read and rewrite `app/build.gradle.kts` (`versionName` and `versionCode`)

Read both current values first:

```bash
grep -n 'versionCode = \|versionName = ' app/build.gradle.kts
```

**`versionName`** always gets set to `<new-version>` verbatim, the same substitution shape as Step 3:

```bash
python3 - "app/build.gradle.kts" "<new-version>" <<'PY'
import re, sys
path, new_version = sys.argv[1], sys.argv[2]
text = open(path).read()
new_text, n = re.subn(
    r'(versionName = )"[^"]*"',
    lambda m: f'{m.group(1)}"{new_version}"',
    text, count=1,
)
if n == 0:
    sys.exit(f"versionName pattern not found in {path}")
open(path, "w").write(new_text)
PY
```

**`versionCode`** — an Android app's `versionCode` is a monotonically-increasing integer the platform (or an
internal/store distribution channel) uses to tell which build is newer; it must never go backwards and, per Google
Play policy, can never be reused once a build carrying it has been uploaded. The chosen rule (documented here since
there is no reference-repository precedent to mirror — irurueta-android-glutils's `app/` sample never bumped its
own `versionCode` in its commit history beyond the single value already in the scaffold template):

> **Increment `versionCode` by exactly 1 only when `<new-version>` is a release (does not end in `-SNAPSHOT`).**
> Leave it unchanged when `<new-version>` itself ends in `-SNAPSHOT`.

Rationale: a `-SNAPSHOT` version is a development build that this catalog's own convention (Step 5) never uploads
to a store/distribution channel on its own — only the `main.yml`/release-triggered workflow does that, for a
non-`SNAPSHOT` version. Burning a `versionCode` value on every `develop`-branch snapshot bump would waste
irrecoverable numbers for builds that were never actually shipped. This mirrors the `X.Y.Z-SNAPSHOT` → `X.Y.Z` →
`X.Y.(Z+1)-SNAPSHOT` cadence in Step 5: the middle step (cutting the release) is the only one that increments
`versionCode`, because it's the only one of the three that corresponds to a build a distribution channel will
actually receive.

```bash
python3 - "app/build.gradle.kts" <<'PY'
import re, sys
path = sys.argv[1]
text = open(path).read()
def bump(m):
    return f"versionCode = {int(m.group(1)) + 1}"
new_text, n = re.subn(r"versionCode = (\d+)", bump, text, count=1)
if n == 0:
    sys.exit(f"versionCode pattern not found in {path}")
open(path, "w").write(new_text)
PY
```

Run the `versionCode` step **only when `<new-version>` does not end in `-SNAPSHOT`** (check with the same shell
test used during this skill's own verification: `[[ "<new-version>" != *-SNAPSHOT ]]`). When skipped, say so
explicitly in the report (Step 8) rather than silently leaving `versionCode` unmentioned — the user should be able
to tell at a glance whether a `versionCode` bump was considered and declined, versus never considered.

If the project's convention differs (e.g. it wants `versionCode` bumped on every call regardless of `-SNAPSHOT`,
or computed from a build number instead), that's a call for the user to make explicitly via `args` or free text
before this step runs — don't silently apply a different rule than the one documented here without saying so in
the report.

## Step 5 — The Android-catalog pre-release convention (for a future `iru-release`-style caller)

This is the Android-ecosystem equivalent of the Java catalog's Maven `-SNAPSHOT` convention (`iru-release`) and
the npm catalog's `-dev.N` convention (`iru-typescript-bump-version`'s Step 5) — the contract a later
release-automation skill is expected to call this skill against (typically two calls per release, each passing a
computed `new-version` through the positional argument):

- **Current development version**: `x.y.z-SNAPSHOT` (e.g. `1.2.0-SNAPSHOT`) — matches this catalog's existing
  Maven convention exactly, unlike npm's own `-dev.N` identifier, since Android/Gradle has no equivalent
  pre-release-numbering convention of its own to prefer instead.
- **Cutting a release**: strip the `-SNAPSHOT` suffix entirely — `x.y.z-SNAPSHOT` → `x.y.z`. Call this skill with
  `<new-version>: x.y.z`. Per Step 4, this is the one call of the three that also increments `app/build.gradle.kts`'s
  `versionCode`.
- **Opening the next development cycle**: bump the patch component and reappend `-SNAPSHOT` — `x.y.z` →
  `x.y.(z+1)-SNAPSHOT`. Call this skill again, immediately or in a follow-up sync step, with
  `<new-version>: x.y.(z+1)-SNAPSHOT`. (A caller wanting a minor/major bump instead is a deliberate decision made
  when the next feature set is known, exactly as `iru-release`'s own Step 4 frames it for Maven — this skill only
  applies whatever exact string it's given, it never guesses which component to bump.)

## Step 6 — `./gradlew -q help` sanity check

After Step 3/4's rewrites, confirm the build script is still syntactically valid Kotlin DSL by running a cheap,
side-effect-free Gradle task rather than a full build:

```bash
export JAVA_HOME="$(/usr/libexec/java_home -v 21)"   # or -v 17 — the default JDK on this machine may be newer
                                                        # than Gradle/AGP support; switch and note it if `-v 21`
                                                        # itself isn't installed
./gradlew -q help
```

A non-zero exit or a Kotlin-compilation error in the output means the rewrite broke the file (e.g. the regex
matched something unintended, or ran twice and produced a syntax error) — stop, show the actual error, and do not
report success. This skill's own authoring did **not** run this command (Gradle runs were left to the heavier
scaffold verification of `iru-setup-android-library`/`iru-setup-android-app`) — treat it as unverified-by-this-skill's-authoring but
still the correct check to run against a real project, and say so in the report.

## Step 7 — Preview (`dry-run: yes`) or write

- Compose the new file contents for every file touched (Step 3/4, and Step 8 if accepted) without writing them to
  disk first — `python3`'s `re.subn` above naturally supports this by reading into a string and only calling
  `open(path, "w")` at the end; for a dry run, print the substituted text (or a unified diff:
  `diff -u <(cat original) <(printf '%s' "$new_text")`) instead of writing it.
- If `dry-run: yes`: show the diff for every file that would change, do not write anything, do not run Step 6, and
  say plainly in the report that this was a preview only — no file was modified.
- Otherwise: write each file, then run Step 6.

## Step 8 — Optionally sync other files that mirror the version

Ask (or honor `args: sync-files`) whether to also update other places that name the current version, the same way
`iru-typescript-bump-version`'s Step 6 and `iru-release`'s Steps 7–9 do for their ecosystems:

**Marker mapping when `next-version` was given** (the `iru-release` case — same rule as
`iru-java-bump-version`'s Step 7): rewrite each mention by what it names rather than to one value —
"Latest release"-style markers and a Project Status `Latest release` row → `<new-version>` when it is a release
(no `-SNAPSHOT` pre-release suffix), left untouched when `<new-version>` is itself a pre-release; "Latest snapshot"/
"Current development version"-style markers → `next-version` when given, otherwise `<new-version>` only if it is
a pre-release value, and untouched (with a warning in the Report step that the caller should pass `next-version`)
when `<new-version>` is a release — never regress a development marker to a release value. A snippet with no
such marker → `<new-version>`.

- **`README.md`** — an installation/dependency snippet naming the current version, if any:
  ```bash
  grep -n "implementation ['\"]" README.md
  ```
  Rewrite the trailing version segment of a matched `implementation 'com.irurueta:irurueta-android-glutils:1.1.11'`
  (or Kotlin-DSL `implementation("…:…:…")`) -style line the same way as Step 3/4:
  ```bash
  python3 - "README.md" "<new-version>" <<'PY'
  import re, sys
  path, new_version = sys.argv[1], sys.argv[2]
  text = open(path).read()
  new_text, n = re.subn(
      r"(implementation\s*\(?['\"][^:'\"]+:[^:'\"]+:)[^'\"]+(['\"])",
      lambda m: f"{m.group(1)}{new_version}{m.group(2)}",
      text,
  )
  open(path, "w").write(new_text)
  print(f"README replacements: {n}")
  PY
  ```

  (The `\s*` between `implementation` and the optional `\(` matters — the Groovy-style form in the reference
  README has a literal space, `implementation 'com…'`, with no parentheses at all; the Kotlin-DSL form some
  projects use instead, `implementation("com…")`, has the parenthesis but no space. Verified locally against
  both forms — see Verification notes.)
- **`docs/antora.yml`** — its `version:` field, if this repository has an Antora site and that field is meant to
  track the library's released version (skip for a `-SNAPSHOT` value — this catalog's convention, matching
  `iru-release`'s Java path and `iru-typescript-bump-version`'s Step 6, is to only write a released version there,
  never a pre-release/snapshot one).
- Any Antora page under `docs/modules/ROOT/pages/` showing a dependency snippet with a literal version string:
  ```bash
  grep -rl "implementation.*[0-9]\+\.[0-9]\+\.[0-9]\+" docs/modules/ROOT/pages/*.adoc 2>/dev/null
  ```
  Update each match the same way as the README snippet above.

This is offered, not automatic — these files may be intentionally out of step with the Gradle build scripts (e.g.
a README badge pulling live from Maven Central rather than a hardcoded string), so don't rewrite anything the user
didn't confirm.

## Step 9 — Report

Summarize:

- The old version and the new version, and every file actually changed: `lib/build.gradle.kts` (or "skipped — no
  `lib` module"), `app/build.gradle.kts`'s `versionName` (or "skipped — no `app` module"), whether `versionCode`
  was incremented (and its old/new value) or left unchanged (and why — `-SNAPSHOT` target), and any Step 8 files
  accepted.
- Whether this was a `dry-run` (no file written) or an actual write.
- The `./gradlew -q help` result (Step 6) — passed, failed with the actual error, or not run because `dry-run:
  yes` (this skill's own authoring did not exercise this command locally; see Verification notes).
- **Warn explicitly**: review the diff before committing (this skill doesn't commit anything); the `versionCode`
  rule (increment only for a non-`-SNAPSHOT` release) is this catalog's own convention, not something enforced by
  Gradle/AGP itself — confirm it matches the project's actual store/distribution policy before relying on it,
  especially for a project with more than one app flavor sharing a `versionCode` scheme; a README/Antora badge
  that pulls the version live from Maven Central/the Play Store rather than hardcoding it should not have Step 8
  applied to it.

## Verification notes

Verified in `$TMPDIR/iru-verify/android/bump-version/`: copied the reference repository's actual
`lib/build.gradle.kts` and `app/build.gradle.kts` (and `README.md`) there and ran the exact Step 3/4/8 `python3`
commands above.

- `1.1.11` → `1.2.0-SNAPSHOT`: `lib/build.gradle.kts`'s `val libraryVersion = "1.1.11"` became
  `val libraryVersion = "1.2.0-SNAPSHOT"` (one-line diff, nothing else touched);
  `app/build.gradle.kts`'s `versionName = "1.1.11"` became `versionName = "1.2.0-SNAPSHOT"`, `versionCode = 10`
  correctly left unchanged (target ends in `-SNAPSHOT`); `README.md`'s
  `implementation 'com.irurueta:irurueta-android-glutils:1.1.11'` became `…:1.2.0-SNAPSHOT'` (1 replacement
  reported). The Step 8 README regex was caught and fixed during this verification: an earlier draft required an
  optional `(` immediately after `implementation` with no `\s*` in between, which matched **zero** times against
  the reference README's Groovy-style `implementation 'com…'` (space, no parens) — confirmed the `\s*\(?` form now
  in Step 8 matches both that form and the Kotlin-DSL `implementation("com…")` form (1 replacement each, verified
  against both).
- `1.2.0-SNAPSHOT` → `1.2.0` (release cut): `versionName` updated to `"1.2.0"` and `versionCode` correctly
  incremented `10` → `11` (target does not end in `-SNAPSHOT`).
- `./gradlew -q help` (Step 6) was **not** run against these throwaway copies — Gradle execution was left to the
  full scaffold verification of `iru-setup-android-library`/`iru-setup-android-app`, and a bare copy of two `build.gradle.kts` files
  outside a real Gradle project (no wrapper, no `settings.gradle.kts`, no `gradle.properties`) wouldn't exercise
  it meaningfully anyway. Marked **unverified locally**; the `JAVA_HOME=$(/usr/libexec/java_home -v 21)` note in
  Step 6 is carried over from the briefing's environment notes, not independently re-confirmed here.
- The `sed -i.bak` alternative in Step 3 was not separately executed (the `python3` path was used throughout this
  verification) — it's included because it's the macOS/Linux-portable `sed -i` idiom used elsewhere in similar
  skills in this catalog, but the `python3` form is the one this skill's own verification actually exercised and
  is the recommended primary path.
