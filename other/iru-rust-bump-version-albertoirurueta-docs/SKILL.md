---
name: iru-rust-bump-version
description: >-
  Set a Rust project's version to an exact value in every place it must agree — a single crate or a Cargo workspace (e.g. a command-line tool scaffolded by `iru-setup-rust-cli`, a library, a multi-crate workspace). Rewrites the root `Cargo.toml` `[package] version` and/or `[workspace.package] version` (which every member declaring `version.workspace = true` inherits), the `[package] version` of any other publishable member that moves in lockstep with it, and the `version = "…"` requirement of every path dependency on those packages (`[workspace.dependencies]`, `[dependencies]`/`[dev-dependencies]`/`[build-dependencies]`/`[target.….dependencies]`, inline or `[dependencies.<name>]` tables, keeping an `=`/`^`/`~` operator) — so `cargo` can still resolve the workspace after a `-dev` → release → next `-dev` cycle; tooling members with `publish = false` (e.g. `xtask`) or their own version are reported and left alone. Refreshes `Cargo.lock` with `cargo update --workspace --offline`, which rewrites only the workspace's own entries. Validates the value as SemVer 2.0 (what Cargo requires) and follows this catalog's `x.y.z-dev` development-version convention (Step 5). Uses an embedded, tested Python helper (driven by `cargo metadata`, regex-based TOML edits that keep comments, formatting and CRLF line endings) with `--list` and `--dry-run` modes, and refuses to write when the version locations disagree until the user confirms. Invoke as `/iru-rust-bump-version <new-version>` where `<new-version>` is the literal target (e.g. `1.4.0` or `1.5.0-dev`) — this skill never computes a bump itself (`iru-release` computes the release/next-dev values per Step 5 and passes each one through). Also accepts `args` (`key: value` lines): `sync-files: yes|no` (default: ask) to also update README/Antora version mentions (`cargo install <crate> --version`, `<crate> = "x.y.z"` dependency snippets, `cargo add <crate>@x.y.z`, "Latest release" markers, `docs/antora.yml`), `next-version: <upcoming-version>` so that sync maps "Latest release" markers to `<new-version>` and "Current development version" markers to the upcoming value, and `dry-run: yes|no` (default `no`) to print the diff without writing anything. Reports every location found with its old value, the new value, and every file touched. Use whenever the user, or `iru-release` (key `rust`), needs a Rust project's version set to a specific value instead of hand-editing `Cargo.toml` files.
model: haiku
allowed-tools: Read Edit Bash(python3 *) Bash(cargo metadata *) Bash(cargo update *) Bash(cargo pkgid *) Bash(cargo check *) Bash(git ls-files *) Bash(git describe *) Bash(git tag *) Bash(git diff *) Bash(grep *) Bash(find *) Bash(ls *) Bash(cat *) Bash(mkdir *)
---

# Rust Bump Version

Set a Rust project's version to an exact value across every file that must agree with it — the root `Cargo.toml`'s
`[package]`/`[workspace.package]` version, lockstep members, path-dependency requirements on them, and `Cargo.lock` —
and, optionally, README/Antora version mentions. This skill never computes a version itself: it applies exactly the
string it's given, validated as SemVer. The "which version comes next" logic belongs to the caller (typically
`iru-release`) and is defined in Step 5, the same contract `iru-java-bump-version`, `iru-dotnet-bump-version`,
`iru-python-bump-version` and the other `iru-<key>-bump-version` skills define for their ecosystems. It never commits,
tags, builds, publishes, or runs `cargo release`/`cargo set-version`.

## Step 0 — Resolve inputs

- The positional argument is `<new-version>` (e.g. `1.4.0`, `1.5.0-dev`). Missing → ask for it before doing anything
  else; never guess or compute one here.
- `args` (`key: value` lines), if present:
  - `sync-files: yes|no` — also update README/Antora mentions (Step 7). Omitted → ask once with `AskUserQuestion`
    after Step 3 shows such mentions exist; don't ask when none do.
  - `next-version: <upcoming-version>` — the upcoming development version (e.g. `1.5.0-dev`) that "Current
    development version" markers should show after a release, while "Latest release" markers show `<new-version>`.
    Only meaningful with `sync-files: yes`; validated like `<new-version>`.
  - `dry-run: yes|no` — default `no`. `yes` runs everything through showing the diff, then stops: nothing is written
    and `Cargo.lock` isn't refreshed; say so plainly in the report.

Reject before touching anything a value that is obviously not a version (empty, or containing whitespace).

## Step 1 — Validate the version string

Cargo requires SemVer 2.0 (`MAJOR.MINOR.PATCH[-PRE][+BUILD]`); this catalog's convention is `X.Y.Z` or `X.Y.Z-dev`:

```bash
python3 -c 'import re,sys; sys.exit(0 if re.fullmatch(r"(0|[1-9]\d*)\.(0|[1-9]\d*)\.(0|[1-9]\d*)(-dev)?", sys.argv[1]) else 1)' "<new-version>"
```

No match → if it is still SemVer (`1.5.0-rc.1`, `1.5.0-alpha.2`; the helper in Step 2 checks the full grammar), warn
that it doesn't follow the `-dev` convention and ask whether to proceed (Cargo orders any SemVer pre-release before its
release). Anything else — `1.0`, `v1.2.3`, `1.2.3.4`, `01.2.3` — is refused (the helper exits `invalid: … is not a
SemVer 2.0 version`). Build metadata (`+build.5`) is accepted by Cargo but ignored for ordering and rejected by
crates.io as a distinguishing factor — warn if given. Anything with a `-` suffix counts as a **pre-release**.

## Step 2 — Write the helper and survey the version locations

| Location | Rewritten to | When |
|---|---|---|
| root `Cargo.toml` `[package] version` | `<new-version>` | the root manifest is a package (this catalog's CLI scaffold: `[package]` + `[workspace] members = ["xtask"]`) |
| root `Cargo.toml` `[workspace.package] version` | `<new-version>` | a workspace sharing one version; members with `version.workspace = true` (or `version = { workspace = true }`) follow it without being edited |
| a member's own `[package] version` | `<new-version>` | it currently equals the project version **and** the member is publishable (lockstep) |
| `version = "…"` of a path dependency on a lockstep package | operator kept + `<new-version>` (`=0.1.0-dev` → `=0.2.0-dev`) | in `[workspace.dependencies]` or any member's dependency tables, inline (`core = { path = "core", version = "0.1.0-dev" }`) or as a `[dependencies.core]` table |
| `Cargo.lock` workspace entries | refreshed by Cargo (Step 4) | `Cargo.lock` exists |

Members with `publish = false` (an `xtask`, a test-support crate) or a different version are printed as `note: …
left untouched` — ask whether one of them should move too only when it looks like a product crate. Never edit a
version string with `sed` across the workspace: dependency entries on **registry** crates with the same number must
stay untouched.

```bash
mkdir -p "$TMPDIR/iru-rust-bump-version"
cat > "$TMPDIR/iru-rust-bump-version/rust_version.py" <<'PY'
import difflib, json, pathlib, re, subprocess, sys

args = sys.argv[1:]
dry, force = "--dry-run" in args, "--force" in args
args = [a for a in args if not a.startswith("--")]
new = args[0] if args else None          # None => --list
SEMVER = re.compile(r"(0|[1-9]\d*)\.(0|[1-9]\d*)\.(0|[1-9]\d*)"
                    r"(?:-((?:0|[1-9]\d*|\d*[A-Za-z-][0-9A-Za-z-]*)(?:\.(?:0|[1-9]\d*|\d*[A-Za-z-][0-9A-Za-z-]*))*))?"
                    r"(?:\+([0-9A-Za-z-]+(?:\.[0-9A-Za-z-]+)*))?")
if new is not None and not SEMVER.fullmatch(new):
    sys.exit(f"invalid: {new!r} is not a SemVer 2.0 version (Cargo requires MAJOR.MINOR.PATCH[-PRE][+BUILD])")

try:
    meta = json.loads(subprocess.run(["cargo", "metadata", "--format-version", "1", "--no-deps", "--offline"],
                                     capture_output=True, text=True, check=True).stdout)
except (OSError, subprocess.CalledProcessError) as e:
    sys.exit(f"cargo metadata failed: {getattr(e, 'stderr', e)}")
root_dir = pathlib.Path(meta["workspace_root"])
member_ids = set(meta["workspace_members"])
members = [p for p in meta["packages"] if p["id"] in member_ids]
root_manifest = root_dir / "Cargo.toml"


def read(p):
    return p.read_text(encoding="utf-8")


def rel(p):
    return pathlib.Path(p).resolve().relative_to(root_dir.resolve()).as_posix()


def tables(text):
    """TOML table name -> (body start, body end); regex-based so it runs on python3 < 3.11 (no tomllib)."""
    heads = [(re.sub(r"\s+", "", m.group(1)), m.start(), m.end())
             for m in re.finditer(r"(?m)^[ \t]*\[\[?([^\[\]\n]+)\]\]?[ \t]*(?:#.*)?$", text)]
    out = {}
    for i, (name, _, end) in enumerate(heads):
        out.setdefault(name, (end, heads[i + 1][1] if i + 1 < len(heads) else len(text)))
    return out


def key_str(text, span, key):
    """First `key = "value"` in the table body -> match (group 3 = value)."""
    rx = re.compile(r'(?m)^([ \t]*' + re.escape(key) + r'[ \t]*=[ \t]*)(")([^"\n]*)(")')
    return rx.search(text, *span) if span else None


def inherits_version(text):
    span = tables(text).get("package")
    return bool(span) and re.search(r"(?m)^[ \t]*version(\.workspace[ \t]*=[ \t]*true|[ \t]*=[ \t]*\{[^}]*workspace[ \t]*=[ \t]*true)",
                                    text[span[0]:span[1]]) is not None


targets = []                              # (path, match-finder, label)
root_text = read(root_manifest)
rt = tables(root_text)
pkg_v = key_str(root_text, rt.get("package"), "version")
ws_v = key_str(root_text, rt.get("workspace.package"), "version")
if pkg_v:
    targets.append((root_manifest, ("package", "version"), "[package] version"))
if ws_v:
    targets.append((root_manifest, ("workspace.package", "version"), "[workspace.package] version"))
project = pkg_v.group(3) if pkg_v else (ws_v.group(3) if ws_v else None)
if project is None:
    lits = sorted({p["version"] for p in members if not inherits_version(read(pathlib.Path(p["manifest_path"])))})
    if len(lits) == 1:
        project = lits[0]
    else:
        sys.exit(f"No root [package]/[workspace.package] version, and members disagree: {lits} — ask which package(s) to bump")

lockstep, independent = [], []
for p in members:
    mp = pathlib.Path(p["manifest_path"])
    t = read(mp)
    if inherits_version(t):
        lockstep.append(p["name"])
        print(f"{rel(mp)}: version.workspace = true    [{p['name']} — follows [workspace.package]]")
    elif mp.resolve() == root_manifest.resolve() or (p["version"] == project and p.get("publish") != []):
        lockstep.append(p["name"])
        if mp.resolve() != root_manifest.resolve():
            targets.append((mp, ("package", "version"), f"[package] version ({p['name']})"))
    else:
        independent.append(p)
        why = "publish = false" if p.get("publish") == [] else "its own version"
        print(f"note: {rel(mp)} ({p['name']} {p['version']}) has {why} — left untouched")

# Requirements on lockstep members from path dependencies: inline tables and [<deps>.<name>] tables.
DEP_TABLE = re.compile(r"^(?:workspace\.)?(?:target\..+\.)?(?:dev-|build-)?dependencies$")
manifests = sorted({root_manifest.resolve()} | {pathlib.Path(p["manifest_path"]).resolve() for p in members})
for mp in manifests:
    text = read(mp)
    for tname, span in tables(text).items():
        if DEP_TABLE.match(tname):
            for m in re.finditer(r'(?m)^[ \t]*([A-Za-z0-9_-]+)[ \t]*=[ \t]*\{([^}\n]*)\}', text[span[0]:span[1]]):
                body = m.group(2)
                pkg = re.search(r'package[ \t]*=[ \t]*"([^"]+)"', body)
                name = pkg.group(1) if pkg else m.group(1)
                if name in lockstep and "path" in body and re.search(r'version[ \t]*=[ \t]*"', body):
                    targets.append((pathlib.Path(mp), ("inline", tname, m.group(1)), f"[{tname}] {m.group(1)} requirement"))
        else:
            base, _, dep = tname.rpartition(".")
            if DEP_TABLE.match(base) and dep:
                body = text[span[0]:span[1]]
                pkg = re.search(r'(?m)^[ \t]*package[ \t]*=[ \t]*"([^"]+)"', body)
                if (pkg.group(1) if pkg else dep) in lockstep and re.search(r"(?m)^[ \t]*path[ \t]*=", body):
                    targets.append((pathlib.Path(mp), (tname, "version"), f"[{tname}] requirement"))


def locate(text, how):
    if how[0] == "inline":
        span = tables(text)[how[1]]
        m = re.compile(r'(?m)^([ \t]*' + re.escape(how[2]) + r'[ \t]*=[ \t]*\{[^}\n]*?\bversion[ \t]*=[ \t]*")([^"\n]*)(")').search(text, *span)
        return m and (m.start(2), m.end(2), m.group(2))
    m = key_str(text, tables(text).get(how[0]), how[1])
    return m and (m.start(3), m.end(3), m.group(3))


found, edits = [], {}
for path, how, label in targets:
    text = edits.get(path, read(path))
    loc = locate(text, how)
    if not loc:
        continue
    s, e, value = loc
    found.append((rel(path), text.count("\n", 0, s) + 1, value, label, how))
    if new is not None:
        op = re.match(r"[=^~<>]*\s*", value).group(0) if "requirement" in label else ""
        edits[path] = text[:s] + op + new + text[e:]

for f, line, value, label, _ in found:
    print(f"{f}:{line}: {value}    [{label}]")
pv = {v for _, _, v, label, _ in found if "requirement" not in label}
if len(pv) > 1:
    print(f"WARNING: version locations disagree: {sorted(pv)}", file=sys.stderr)
    if new is not None and not force:
        sys.exit("Refusing to write: confirm with the user, then re-run with --force to align every location")
print(f"current: {project}")
print(f"lockstep packages: {', '.join(sorted(lockstep))}")
if new is None:
    sys.exit(0)
for path, text in edits.items():
    old = read(path)
    if text == old:
        continue
    if dry:
        sys.stdout.writelines(difflib.unified_diff(old.splitlines(True), text.splitlines(True), rel(path), rel(path)))
        continue
    raw = path.read_bytes()
    out = text.replace("\r\n", "\n")
    if b"\r\n" in raw:
        out = out.replace("\n", "\r\n")
    path.write_bytes(out.encode("utf-8"))
    print(f"updated {rel(path)}")
PY
python3 "$TMPDIR/iru-rust-bump-version/rust_version.py" --list
```

Run it from the workspace root (or any directory inside the workspace — `cargo metadata` finds the root; it needs no
network with `--no-deps --offline`). It parses TOML with anchored regexes, so it runs on any `python3` ≥ 3.8 (no
`tomllib`) and leaves comments and formatting intact. Output: `note:` lines, one `<file>:<line>: <value>    [<location>]`
line per location (plus `version.workspace = true` lines for inheriting members), `current: <version>` and the
lockstep package list. Then:

- **No version anywhere** (non-zero exit: `No root [package]/[workspace.package] version, and members disagree`) — a
  virtual workspace whose members version independently. Ask which package(s) the release is for; don't invent a
  `[workspace.package]` section.
- **Locations disagree** (`WARNING: version locations disagree`) — e.g. the root `[package]` says `0.0.9` while
  `[workspace.package]` says `0.1.0-dev`. Show the list and ask whether to align them all to `<new-version>` (Step 4
  then passes `--force`) or stop.
- **A path-dependency requirement that doesn't match** the current version is still rewritten (with its operator) —
  mention it; it was probably already broken or deliberately loose (`"0.1"`).
- The current version for the report, and for `iru-release` (which reads it this way), is the `current:` line —
  `cargo pkgid -p <package>` (`…#<name>@0.1.0-dev`) confirms what Cargo evaluates.

## Step 3 — Look for mirrored mentions

```bash
grep -n -i -E "latest release|current development version|cargo install|cargo add|^[a-z0-9_-]+ = \"[0-9]+\.[0-9]+|brew install|--version [0-9]" README.md 2>/dev/null
grep -rln -i -E "latest release|cargo install|cargo add" docs/modules/ROOT/pages 2>/dev/null; grep -n '^version:' docs/antora.yml 2>/dev/null
grep -rn --include='*.rs' -E '"<current-version>"' src */src 2>/dev/null   # hard-coded version literals
```

Only when something turns up is `sync-files` worth asking about (Step 0). A Rust CLI should read its version from
`env!("CARGO_PKG_VERSION")` (clap's `#[command(version)]` does) — a hard-coded literal equal to the current version in
`*.rs` is reported, not rewritten (it's code; suggest `env!("CARGO_PKG_VERSION")`). Golden test files that embed
`--version` output (`tests/snapshots/*`, `tests/cmd/*.toml` for trycmd) are reported too — the tests will tell.

## Step 4 — Preview (`dry-run: yes`) or apply

```bash
python3 "$TMPDIR/iru-rust-bump-version/rust_version.py" "<new-version>" --dry-run   # unified diff only
python3 "$TMPDIR/iru-rust-bump-version/rust_version.py" "<new-version>"             # write
cargo update --workspace --offline                                                  # refresh Cargo.lock (skip on dry-run)
```

- Add `--force` only after the user confirmed aligning disagreeing locations (Step 2). The script rewrites exactly
  the locations `--list` printed and nothing else. A non-zero exit at any point → stop, show the error, and treat
  nothing as updated; never fall back to hand edits.
- **`Cargo.lock`**: `cargo update --workspace` (`-w`) only re-locks the workspace's own packages — registry
  dependencies keep their locked versions (verified: the only lockfile change was `version = "0.1.0-dev"` →
  `"0.1.0"` on the workspace entries, even with registry deps present). `--offline` avoids touching the network; if it
  fails because something isn't in the local registry cache, run `cargo update --workspace` without `--offline` and
  say so. Skip when there is no `Cargo.lock`; when it exists but isn't tracked (`git ls-files Cargo.lock` prints
  nothing — a library that doesn't commit it), refresh it anyway and say it's untracked.
- Never run plain `cargo update` (it would upgrade every dependency) or `cargo generate-lockfile` (it re-resolves
  everything).

## Step 5 — The Rust-catalog pre-release convention (for `iru-release` and other callers)

The Rust equivalent of `iru-java-bump-version`'s `-SNAPSHOT` and `iru-dotnet-bump-version`'s `-dev` — the contract
`iru-release` calls this skill against (two calls per release, each passing a computed `<new-version>`), and the one
the `iru-setup-rust-cli` scaffold (`version = "0.1.0-dev"`) and the `sync.yml` written by
`iru-setup-cli-github-workflows` use:

- **Current development version**: `x.y.z-dev` (e.g. `1.4.0-dev`) in the root `[package]`/`[workspace.package]`
  version on the gitflow integration branch. SemVer/Cargo order `1.4.0-dev` after `1.3.0` and before `1.4.0`, and
  `<bin> --version` prints it as is. A main-only repository has no development marker: the version is always the last
  or next release `x.y.z`.
- **Cutting a release**: strip the suffix — `x.y.z-dev` → `x.y.z`. Call this skill with `<new-version>: x.y.z`; the
  release workflow then checks that the git tag (`vX.Y.Z`) equals this version and, for `distribution: store`,
  publishes the crate. Never publish a `-dev` version to crates.io.
- **Opening the next development cycle**: bump the minor (this catalog's default, matching `iru-release`'s
  recommended "minor bump" and the `sync.yml` workflow) and re-append `-dev` — `x.y.z` → `x.(y+1).0-dev`; a patch or
  major bump is the caller's choice. Call this skill again (or let `sync.yml` do it after the release is published)
  with that exact value — this skill never decides which component to bump. For `0.y.z` crates Cargo treats a minor
  bump as breaking (`^0.1` doesn't match `0.2`), which is exactly why the path-dependency requirements are rewritten.
- **Requirements must move with the version**: a stale requirement makes the workspace unresolvable — with
  `[workspace.package] version = "0.2.0-dev"` and `democore = { path = "core", version = "0.1.0-dev" }`, `cargo check`
  fails with `failed to select a version for the requirement democore = "^0.1.0-dev"`, and an exact `=0.1.0-dev`
  requirement fails even for the `0.1.0` release (verified). Step 2's helper rewrites them in the same pass.

## Step 6 — Sanity check

Skip with `dry-run: yes`. Otherwise:

```bash
python3 "$TMPDIR/iru-rust-bump-version/rust_version.py" --list   # every location shows the new value, no warning
cargo pkgid -p <each lockstep package>                           # …#<name>@<new-version>
cargo check --workspace --offline --locked -q                    # the workspace still resolves with the committed lock
```

`cargo check --locked` must succeed (it fails with `cannot update the lock file … because --locked was passed` if Step
4's refresh was skipped, or with `failed to select a version for the requirement` if a requirement was missed). It
needs the dependencies in the local cache — if `--offline` can't find them, say the build check wasn't run rather
than assume it passed.

## Step 7 — Optionally sync other files that mirror the version

Ask (or honor `sync-files`) whether to update the mentions Step 3 found, mapping each by what it names — the same rule
as `iru-java-bump-version`'s Step 7 — with targeted Edit-tool substitutions only (never a repository-wide replace of
the old string):

- "Latest release" markers (and a `Latest release` row in the README's status table), `cargo install <crate>
  --version x.y.z`, `cargo add <crate>@x.y.z`, a `<crate> = "x.y.z"` line in a `[dependencies]` snippet for this
  project's own crate, versioned download URLs/archive names (`<bin>-x.y.z-<target>.tar.gz`) → `<new-version>` only
  when it is a release.
- "Current development version" markers → `next-version` when given; otherwise `<new-version>` only if it is a `-dev`
  value, and untouched (warn in Step 8 that the caller should pass `next-version`) when it's a release — never regress
  a development marker to a release value.
- `docs/antora.yml` `version:` → `<new-version>` only for a release (Antora's component version names released
  versions; skip `-dev`), if the site tracks the release version at all.
- Antora pages under `docs/modules/ROOT/pages/` with the same markers/snippets → as for the README. A generated CLI
  reference (`cli-reference.adoc` written by `cargo xtask docs`) is regenerated by its generator, not edited here.

A README badge that pulls the version live (crates.io, GitHub release, Homebrew shields) must not be rewritten.

## Step 8 — Report

- Every location from `--list` with its old value and the new one, the lockstep packages, inheriting members, and every
  member left untouched (with why: `publish = false` / own version).
- Every file changed (by the script, by `cargo update --workspace`, and by Step 7), or that nothing changed.
- Any disagreement aligned with `--force` after the user confirmed, and any requirement that didn't match before.
- Whether this was a `dry-run`, and the Step 6 result (`--list` agreement, `cargo pkgid` values, `cargo check` result or
  "not run").
- **Warn explicitly**: review the diff before committing (this skill commits nothing); hard-coded version literals or
  golden `--version` outputs found in Step 3 were not changed.

## Verification notes

Verified on 2026-10-16 in `$TMPDIR/iru-verify/cli/rust-gates/bump/` (outside this repository; Rust 1.99.1, host
`python3` 3.9) by running the exact helper above:

- A virtual workspace (`[workspace.package] version = "0.1.0-dev"` with a trailing comment, members `core` and `cli`
  inheriting via `version.workspace = true` and `version = { workspace = true }`, `[workspace.dependencies] democore =
  { path = "core", version = "0.1.0-dev" }`, a `[dev-dependencies.democore]` table with `version = "=0.1.0-dev"`, and
  an `xtask` member at `0.1.0` with `publish = false`): `--list` reported the three locations, both inheriting members
  and the `xtask` note; `--dry-run` printed the diff and left `git status` clean; `0.1.0` rewrote
  `[workspace.package]` (comment kept), both requirements (`=` kept), and `cargo update --workspace --offline` changed
  only the two workspace entries in `Cargo.lock`; `cargo pkgid` printed `democli@0.1.0`/`democore@0.1.0`; then
  `0.2.0-dev` left `xtask` at `0.1.0` (an earlier helper draft wrongly moved it because its version happened to equal
  the release — fixed by the `publish = false` rule) and `cargo check --offline` passed.
- The CLI-scaffold shape (root `[package] version = "0.1.0-dev"` + `[workspace] members = ["xtask"]`, assert_cmd and
  predicates as registry dev-dependencies): `0.1.0` changed exactly one line in `Cargo.toml` and one in `Cargo.lock`.
- A root `[package] version = "0.0.9"` next to `[workspace.package] version = "0.1.0-dev"` → `WARNING: version
  locations disagree` and a refusal without `--force`. `1.0` and `v1.0.0` → `invalid: … is not a SemVer 2.0 version`.
  A CRLF member manifest stayed CRLF.
- Leaving a requirement stale reproduced the two `failed to select a version for the requirement` errors quoted in
  Step 5.
- Not verified: `[patch]`/`[replace]` sections pointing at workspace members, members outside the root directory
  (`members = ["../x"]`), multi-line inline tables (TOML 1.1, newer Cargo), and Windows path handling in the helper.

## Sources

- irurueta docs: programming-languages/rust/cargo-and-workspaces.adoc (`[package] version`, `[workspace.package]`
  inheritance with `version.workspace = true`, `[workspace.dependencies]`, path + version dependencies, SemVer caret
  requirements, `Cargo.lock` and `cargo update`)
- irurueta docs: ai/cli-for-agents/packaging-and-distribution.adoc (release tags matching the manifest version, `--version` output)
- The Cargo Book: the manifest format, specifying dependencies (`path` + `version`, SemVer compatibility for `0.y.z`),
  `cargo update --workspace`; SemVer 2.0.0 specification
