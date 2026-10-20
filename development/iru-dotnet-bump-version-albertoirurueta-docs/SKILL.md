---
name: iru-dotnet-bump-version
description: >-
  Set a .NET project's version to an exact value in every place it must agree — a .NET library, service, or Windows
  desktop app (WPF, WinUI 3, Windows Forms) alike. Rewrites `<Version>` (or `<VersionPrefix>` + `<VersionSuffix>`) in
  the root `Directory.Build.props` when it declares one, otherwise in every non-test `*.csproj` that declares one, and
  the MSIX package identity — `<Identity Version="x.y.z.0">` in every tracked `Package.appxmanifest` (WinUI
  single-project MSIX) and `packaging/AppxManifest.xml` (WPF/WinForms MSIX) — always as the four-part numeric value
  derived from the new version (pre-release suffix stripped, revision `0`, as the Microsoft Store requires). Follows
  this catalog's `x.y.z-dev` development-version convention (Step 5). Uses an embedded, tested Python helper with
  `--list` and `--dry-run` modes, preserves BOMs and CRLF line endings, never touches test projects or explicit
  `<AssemblyVersion>`/`<FileVersion>` values (it reports them), and refuses to write when the `<Version>` locations
  disagree until the user confirms. Invoke as `/iru-dotnet-bump-version <new-version>` where `<new-version>` is the
  literal target (e.g. `1.4.0` or `1.5.0-dev`) — this skill never computes a bump itself (`iru-release` computes the
  release/next-dev values per Step 5 and passes each one through). Also accepts `args` (`key: value` lines):
  `sync-files: yes|no` (default: ask) to also update README/Antora version mentions, `next-version:
  <upcoming-version>` so that sync maps "Latest release" markers to `<new-version>` and "Current development
  version" markers to the upcoming value, and `dry-run: yes|no` (default `no`) to print the diff without writing
  anything. Reports every location found with its old value, the new values, and every file touched. Use whenever
  the user, or `iru-release` (key `dotnet`), needs a .NET project's version set to a specific value instead of
  hand-editing MSBuild properties and MSIX manifests.
model: haiku
allowed-tools: Read Bash(python3 *) Bash(dotnet msbuild *) Bash(git ls-files *) Bash(git describe *) Bash(git tag *) Bash(git diff *) Bash(grep *) Bash(find *) Bash(ls *) Bash(cat *) Bash(mkdir *)
---

# .NET Bump Version

Set a .NET project's version to an exact value across every file that must agree with it — the MSBuild version
property and, for a packaged Windows desktop app, the MSIX identity version — and, optionally, README/Antora version
mentions. This skill never computes a version itself: it applies exactly the string it's given, validated for shape.
The "which version comes next" logic belongs to the caller (typically `iru-release`) and is defined in Step 5, the
same contract `iru-java-bump-version`, `iru-typescript-bump-version`, `iru-php-bump-version` and the other
`iru-<key>-bump-version` skills define for their ecosystems. It never commits, tags, builds, or packages anything.

## Step 0 — Resolve inputs

- The positional argument is `<new-version>` (e.g. `1.4.0`, `1.5.0-dev`). Missing → ask for it before doing anything
  else; never guess or compute one here.
- `args` (`key: value` lines), if present:
  - `sync-files: yes|no` — also update README/Antora mentions (Step 7). Omitted → ask once with `AskUserQuestion`
    after Step 3 shows such mentions exist; don't ask when none do.
  - `next-version: <upcoming-version>` — the upcoming development version (e.g. `1.5.0-dev`) that "Current
    development version" markers should show after a release, while "Latest release" markers show `<new-version>`.
    Only meaningful with `sync-files: yes`; validated like `<new-version>`.
  - `dry-run: yes|no` — default `no`. `yes` runs everything through showing the diff, then stops: nothing is written;
    say so plainly in the report.

Reject before touching anything a value that is obviously not a version (empty, or containing whitespace).

## Step 1 — Validate the version string

MSBuild's `<Version>` is free-form, but NuGet (SemVer 2.0) and the MSIX identity are not, so use this catalog's
convention — `X.Y.Z` or `X.Y.Z-dev`:

```bash
python3 -c 'import re,sys; sys.exit(0 if re.fullmatch(r"\d+\.\d+\.\d+(-dev)?", sys.argv[1]) else 1)' "<new-version>"
```

No match → if it is still SemVer (`X.Y.Z-<pre-release>`, e.g. `-rc.1`, `-preview.2`), warn that it doesn't follow
the `-dev` convention and ask whether to proceed (NuGet orders any SemVer pre-release correctly). Anything that isn't
`X.Y.Z[-suffix]` — `1.0`, `1.2.3.4`, `v1.2.3` — is refused: the MSIX identity needs exactly three numeric parts plus
the revision this skill appends, each part `0`–`65535`. Anything with a `-` suffix counts as a **pre-release**.

## Step 2 — Write the helper and survey the version locations

| Location | Rewritten to | When |
|---|---|---|
| root `Directory.Build.props` `<Version>` | `<new-version>` | it declares `<Version>` or `<VersionPrefix>` (this catalog's scaffolds: `iru-setup-windows-app`) |
| root `Directory.Build.props` `<VersionPrefix>` / `<VersionSuffix>` | `X.Y.Z` / the suffix (`dev`), or an empty `<VersionSuffix></VersionSuffix>` for a release | the project splits the version that way |
| every non-test `*.csproj` declaring `<Version>`/`<VersionPrefix>` | as above | only when `Directory.Build.props` declares none |
| every git-tracked `Package.appxmanifest` and `AppxManifest.xml` (e.g. `packaging/AppxManifest.xml`) `<Identity … Version="…">` | `X.Y.Z.0` — always numeric, suffix stripped, revision `0` | the file exists outside `bin/`/`obj/`/`AppPackages/` |

Test projects (`IsTestProject`, or referencing MSTest/xUnit/NUnit/`Microsoft.NET.Test.Sdk`, or named `*.Tests`/
`*.UITests`) are never touched. Explicit `<AssemblyVersion>`/`<FileVersion>`/`<InformationalVersion>` are reported
and left alone — the SDK derives all three from `<Version>` unless a project overrides them, and an override is a
deliberate choice this skill doesn't second-guess.

```bash
mkdir -p "$TMPDIR/iru-dotnet-bump-version"
cat > "$TMPDIR/iru-dotnet-bump-version/dotnet_version.py" <<'PY'
import difflib, pathlib, re, subprocess, sys

args = sys.argv[1:]
dry, force = "--dry-run" in args, "--force" in args
args = [a for a in args if not a.startswith("--")]
new = args[0] if args else None          # None => --list
root = pathlib.Path(".")
SKIP = {"bin", "obj", "node_modules", ".git", ".vs", "artifacts", "AppPackages", "BundleArtifacts", "publish"}


def files(pattern):
    return [p for p in sorted(root.rglob(pattern)) if not any(part in SKIP for part in p.parts)]


def read(p):
    return p.read_text(encoding="utf-8-sig")


def tracked(p):
    try:
        r = subprocess.run(["git", "ls-files", "--error-unmatch", str(p)], capture_output=True)
        return r.returncode == 0 if r.returncode in (0, 1) else True
    except FileNotFoundError:
        return True                       # no git: treat an existing file as tracked


def is_test(p):
    t = read(p)
    return (re.search(r"<IsTestProject>\s*true\s*</IsTestProject>", t, re.I) is not None
            or re.search(r'Include="(MSTest[^"]*|Microsoft\.NET\.Test\.Sdk|xunit[^"]*|NUnit)"', t) is not None
            or re.search(r"\.(Tests?|UITests|IntegrationTests)\.csproj$", p.name) is not None)


def split(v):
    m = re.fullmatch(r"(\d+\.\d+\.\d+)(?:-(.+))?", v)
    return (m.group(1), m.group(2) or "") if m else (v, "")


def msix(v):
    parts = split(v)[0].split(".")
    if len(parts) != 3 or not all(x.isdigit() and int(x) <= 65535 for x in parts):
        sys.exit(f"Cannot derive a four-part MSIX version from {v!r} (X.Y.Z, each part 0-65535)")
    return ".".join(parts) + ".0"


def value_for(kind, v):
    if kind == "version":
        return v
    if kind == "prefix":
        return split(v)[0]
    if kind == "suffix":
        return split(v)[1]
    return msix(v)


TAG = lambda name: re.compile(rf"(<{name}>\s*)([^<]*?)(\s*</{name}>)")
IDENTITY = re.compile(r'(<Identity\b[^>]*?\bVersion\s*=\s*")([^"]*)(")', re.S)

targets = []                              # (path, kind, regex, label)
props = root / "Directory.Build.props"
prop_files = [props] if props.exists() and re.search(r"<Version(Prefix)?>", read(props)) else []
if not prop_files:
    prop_files = [p for p in files("*.csproj") if not is_test(p) and re.search(r"<Version(Prefix)?>", read(p))]
for p in prop_files:
    t = read(p)
    if "<VersionPrefix>" in t:
        targets.append((p, "prefix", TAG("VersionPrefix"), "VersionPrefix"))
        if "<VersionSuffix>" in t:
            targets.append((p, "suffix", TAG("VersionSuffix"), "VersionSuffix"))
    if "<Version>" in t:
        targets.append((p, "version", TAG("Version"), "Version"))
for p in files("Package.appxmanifest") + files("AppxManifest.xml"):
    if tracked(p) and IDENTITY.search(read(p)):
        targets.append((p, "msix", IDENTITY, "MSIX Identity Version"))

for p in files("*.csproj") + ([props] if props.exists() else []):
    for tag in ("AssemblyVersion", "FileVersion", "InformationalVersion"):
        m = TAG(tag).search(read(p))
        if m:
            print(f"note: {p.as_posix()} sets <{tag}>{m.group(2)}</{tag}> explicitly — left untouched")

if not any(k in ("version", "prefix") for _, k, _, _ in targets):
    sys.exit("No <Version>/<VersionPrefix> found in Directory.Build.props or any non-test *.csproj")

found, edits = [], {}
for path, kind, rx, label in targets:
    text = edits.get(path, read(path))
    m = rx.search(text)
    if not m:
        continue
    found.append((path.as_posix(), text.count("\n", 0, m.start()) + 1, m.group(2), label, kind))
    if new is not None:
        edits[path] = text[:m.start()] + m.group(1) + value_for(kind, new) + m.group(3) + text[m.end():]

for path, line, value, label, _ in found:
    print(f"{path}:{line}: {value}    [{label}]")

suf = {f[0]: f[2] for f in found if f[4] == "suffix"}
current = {f[2] if f[4] == "version" else f[2] + ("-" + suf[f[0]] if suf.get(f[0]) else "")
           for f in found if f[4] in ("version", "prefix")}
if len(current) > 1:
    print(f"WARNING: <Version> locations disagree: {sorted(current)}", file=sys.stderr)
    if new is not None and not force:
        sys.exit("Refusing to write: confirm with the user, then re-run with --force to align every location")
if len(current) == 1:
    cur = next(iter(current))
    print(f"current: {cur}")
    ms = sorted({f[2] for f in found if f[4] == "msix"})
    if ms and re.fullmatch(r"\d+\.\d+\.\d+(-.+)?", cur) and ms != [msix(cur)]:
        print(f"note: MSIX Identity Version {ms} does not match {msix(cur)} derived from <Version> — realigned on write")
if new is None:
    sys.exit(0)
for path, text in edits.items():
    old = read(path)
    if text == old:
        continue
    if dry:
        sys.stdout.writelines(difflib.unified_diff(old.splitlines(True), text.splitlines(True), str(path), str(path)))
        continue
    raw = path.read_bytes()
    out = text.replace("\r\n", "\n")
    if b"\r\n" in raw:
        out = out.replace("\n", "\r\n")   # keep CRLF files CRLF (Visual Studio writes manifests that way)
    path.write_bytes((b"\xef\xbb\xbf" if raw.startswith(b"\xef\xbb\xbf") else b"") + out.encode("utf-8"))
    print(f"updated {path.as_posix()}")
PY
python3 "$TMPDIR/iru-dotnet-bump-version/dotnet_version.py" --list
```

Run it from the repository root (the directory holding the solution and `Directory.Build.props`). Output: `note:`
lines, one `<file>:<line>: <value>    [<location>]` line per location, and a `current:` line. Then:

- **No `<Version>`/`<VersionPrefix>` anywhere** (non-zero exit) — the project relies on the SDK default `1.0.0` or on a
  tool such as MinVer/Nerdbank.GitVersioning/GitVersion (look for `MinVer`, `Nerdbank.GitVersioning`/`version.json`,
  `GitVersion.yml`). With such a tool the git tag (or `version.json`) is the version: report that, change nothing,
  and let `iru-release` treat the tag as the version (as for a Swift library). Otherwise ask whether to add
  `<Version><new-version></Version>` to `Directory.Build.props` (creating it with a `<Project><PropertyGroup>` shell
  if absent) and re-run `--list` — never invent it silently.
- **Locations disagree** (`WARNING: <Version> locations disagree`) — e.g. two app projects carrying their own
  `<Version>`. Show the list and ask whether to align them all to `<new-version>` (Step 4 then passes `--force`) or
  which to leave (edit the others by hand and say so in the report).
- **MSIX identity out of step** (`note: MSIX Identity Version … does not match`) — informational: the identity is
  derived, so the write realigns it. Mention it in the report (someone hand-edited a manifest).
- The current version for the report, and for `iru-release` (which reads it this way), is the `current:` line.

## Step 3 — Look for mirrored mentions

```bash
grep -n -i "latest release\|current development version\|dotnet add package\|PackageReference Include\|winget install\|Version=" README.md 2>/dev/null
grep -rln -i "latest release\|dotnet add package\|winget install" docs/modules/ROOT/pages 2>/dev/null; grep -n '^version:' docs/antora.yml 2>/dev/null
```

Only when something turns up is `sync-files` worth asking about (Step 0). An `.appinstaller` file (App Installer
feed) carries the MSIX version too, but in this catalog's workflows it is **generated at release time** by
`release.yml`, not committed — if a committed one turns up, report it and leave it for the release workflow rather
than rewriting it here.

## Step 4 — Preview (`dry-run: yes`) or apply

```bash
python3 "$TMPDIR/iru-dotnet-bump-version/dotnet_version.py" "<new-version>" --dry-run   # unified diff only
python3 "$TMPDIR/iru-dotnet-bump-version/dotnet_version.py" "<new-version>"             # write
```

Add `--force` only after the user confirmed aligning disagreeing locations (Step 2). The script rewrites exactly the
first match of each location `--list` printed — other `<Version>` elements (e.g. inside an unrelated `ItemGroup`
metadata), test projects, `PackageVersion`s in `Directory.Packages.props` and every other file stay untouched. A
non-zero exit at any point → stop, show the error, and treat nothing as updated; never fall back to hand edits.

## Step 5 — The .NET-catalog pre-release convention (for `iru-release` and other callers)

The .NET equivalent of `iru-java-bump-version`'s `-SNAPSHOT` and `iru-php-bump-version`'s `-dev` — the contract
`iru-release` calls this skill against (two calls per release, each passing a computed `<new-version>`), and the one
the `sync.yml` written by `iru-setup-windows-github-workflows` and the `iru-setup-windows-app` scaffold use:

- **Current development version**: `x.y.z-dev` (e.g. `1.4.0-dev`) in `<Version>` on the gitflow integration branch.
  NuGet/SemVer order `1.4.0-dev` before `1.4.0` and after `1.3.0`; `AssemblyInformationalVersion` carries it as is.
  A main-only repository has no development marker: `<Version>` is always the last or next release `x.y.z`.
- **MSIX identity**: always `x.y.z.0`, derived — so a `1.4.0-dev` build is packaged as `1.4.0.0`, the same identity
  version the `1.4.0` release will get. Windows refuses to install a package over an installed one with the same
  identity version but different content, so a sideloaded dev build must be uninstalled before the release MSIX is
  installed (or CI may stamp a build-specific revision at packaging time — never in the committed manifest; the
  Microsoft Store requires revision `0` for submitted packages).
- **Cutting a release**: strip the suffix — `x.y.z-dev` → `x.y.z`. Call this skill with `<new-version>: x.y.z`.
- **Opening the next development cycle**: bump the minor (this catalog's default, matching `iru-release`'s
  recommended "minor bump" and the `sync.yml` workflow) and re-append `-dev` — `x.y.z` → `x.(y+1).0-dev`; a patch or
  major bump is the caller's choice. Call this skill again (or let `sync.yml` do it after the release is published)
  with that exact value — this skill never decides which component to bump.
- **Version-from-git projects** (MinVer, Nerdbank.GitVersioning, GitVersion — Step 2): no in-tree marker; the release
  is the git tag. `iru-release` skips its "must currently be a pre-release" check and its next-version question for
  them, exactly as for a Swift library.

## Step 6 — Sanity check

Skip with `dry-run: yes`. Otherwise:

```bash
python3 "$TMPDIR/iru-dotnet-bump-version/dotnet_version.py" --list   # every location shows the new value, no warning
dotnet msbuild <one non-test project> -getProperty:Version             # what MSBuild actually evaluates
```

`-getProperty:Version` must print `<new-version>` (it needs the .NET SDK; on a non-Windows host a WPF/WinForms project
evaluates fine because `-getProperty` doesn't resolve the Windows Desktop targeting pack — pick the Core/library
project anyway). Without an SDK, say the MSBuild check wasn't run rather than assume it passed.

## Step 7 — Optionally sync other files that mirror the version

Ask (or honor `sync-files`) whether to update the mentions Step 3 found, mapping each by what it names — the same rule
as `iru-java-bump-version`'s Step 7:

- "Latest release" markers (and a `Latest release` row in the README's status table), `dotnet add package <Id>
  --version x.y.z` / `<PackageReference Include="<Id>" Version="x.y.z" />` snippets for this project's own package,
  and `winget install <Id> --version x.y.z` lines → `<new-version>` only when it is a release.
- "Current development version" markers → `next-version` when given; otherwise `<new-version>` only if it is a `-dev`
  value, and untouched (warn in Step 8 that the caller should pass `next-version`) when it's a release — never
  regress a development marker to a release value.
- `docs/antora.yml` `version:` → `<new-version>` only for a release (Antora's component version names released
  versions; skip `-dev`), if the site tracks the release version at all.
- Antora pages under `docs/modules/ROOT/pages/` with the same markers/snippets → as for the README.

Targeted, scoped substitutions only — never a repository-wide replace of the old string. A README badge pulling the
version live (NuGet, GitHub release, WinGet shields) must not be rewritten.

## Step 8 — Report

- Every location from `--list` with its old value, the new `<Version>` (or prefix/suffix) and the derived MSIX
  `x.y.z.0`, and any explicit `AssemblyVersion`/`FileVersion`/`InformationalVersion` left untouched.
- Every file changed (by the script and by Step 7), or that nothing changed because the version comes from git tags.
- Any disagreement aligned with `--force` after the user confirmed, and any MSIX identity that was out of step.
- Whether this was a `dry-run`, and the Step 6 result (`--list` agreement, `-getProperty:Version` value or "not run").
- **Warn explicitly**: review the diff before committing (this skill commits nothing); a `-dev` build and the
  following release share the MSIX identity version (Step 5); a committed `.appinstaller` is not managed here.

## Verification notes

Verified in `$TMPDIR/iru-verify/windows/iru-dotnet-bump-version/` (macOS, .NET SDK 10.0.402, host `python3` 3.9) by
running the exact helper above against a copy of a scaffold-shaped solution (`Directory.Build.props` `<Version>`,
WPF app, `src/<App>/Package.appxmanifest` with CRLF line endings and a multi-line `<Identity>`, and
`packaging/AppxManifest.xml`) committed to a throwaway git repository:

- `--list` reported `<Version>1.2.0-dev`, both identity versions and the `current:` line, plus the out-of-step note
  for a manifest left at `1.1.0.0`.
- `1.2.0` rewrote `<Version>` and realigned the stale manifest to `1.2.0.0`; `--dry-run` printed the diff and left
  `git status` clean; `1.3.0-dev` wrote `<Version>1.3.0-dev</Version>` and `Version="1.3.0.0"` in both manifests;
  CRLF endings were preserved (`file` still reports CRLF).
- A library with `<VersionPrefix>2.0.0</VersionPrefix><VersionSuffix>dev</VersionSuffix>`, an explicit
  `<FileVersion>` and a test project carrying its own `<Version>9.9.9`: the test project was ignored, `FileVersion`
  reported and untouched, `2.0.0` emptied the suffix and `dotnet msbuild -getProperty:Version` then printed `2.0.0`;
  `2.1.0-dev` printed `2.1.0-dev`. `1.0` was refused (no MSIX derivation possible).
- `dotnet msbuild -getProperty:Version` on the Core project printed the new value; `AssemblyVersion`/`FileVersion`
  come back empty from `-getProperty` (they are computed in targets, not at evaluation) — don't use them as a check.

Not verified: MinVer/Nerdbank.GitVersioning repositories (the "version from git" branch follows their docs), and real
MSIX packaging/installation of the rewritten manifests — unverified locally (needs Windows).
