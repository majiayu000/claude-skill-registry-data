---
name: iru-go-bump-version
description: >-
  Set a Go module's in-tree version to an exact value — a Cobra command-line tool scaffolded by `iru-setup-go-cli` (`internal/version/version.go`: `var Version = "0.1.0-dev"`, overridden at release time with `-ldflags -X <module>/internal/version.Version=…`) or any Go project that keeps a `var`/`const Version = "…"` string literal in a non-test, non-generated `.go` file (including a `var (…)` block or `package main`). Follows this catalog's `x.y.z-dev` development-version convention (Step 5). Uses an embedded, tested Python helper with `--list` and `--dry-run` modes that finds every literal, refuses to write when they disagree until the user confirms, flags a `const Version` (which `-ldflags -X` silently can't override), checks every `-X …Version=` reference in `.goreleaser.yaml`, `Makefile`, `Taskfile.yml`, `justfile` and GitHub workflows against the real import path (a wrong path is silently ignored by the linker), and warns when a major version ≥ 2 doesn't match a `/vN` module-path suffix (Go's semantic import versioning — never rewritten here, it's a breaking import-path change). Reminds that for module consumers (`go get`, `go install …@vX.Y.Z`) the git tag `vX.Y.Z` is the version, so a library with no literal is reported as "version comes from git tags" and nothing is changed. Invoke as `/iru-go-bump-version <new-version>` where `<new-version>` is the literal target without a `v` (e.g. `1.4.0` or `1.5.0-dev`) — this skill never computes a bump itself (`iru-release` computes the release/next-dev values per Step 5 and passes each one through). Also accepts `args` (`key: value` lines): `sync-files: yes|no` (default: ask) to also update README/Antora version mentions, `next-version: <upcoming-version>` so that sync maps "Latest release" markers to `<new-version>` and "Current development version" markers to the upcoming value, `files: <comma list>` to restrict the search to specific `.go` files, and `dry-run: yes|no` (default `no`) to print the diff without writing anything. Reports every location found with its old value, the new value, every `-ldflags -X` reference and whether it matches, and every file touched. Use whenever the user, or `iru-release` (key `go`), needs a Go project's version set to a specific value instead of hand-editing version.go.
model: haiku
allowed-tools: Read Bash(python3 *) Bash(go build *) Bash(go list *) Bash(go version *) Bash(go vet *) Bash(git ls-files *) Bash(git describe *) Bash(git tag *) Bash(git diff *) Bash(grep *) Bash(find *) Bash(ls *) Bash(cat *) Bash(mkdir *) Bash(rm -f build/iru-go-bump-version*)
---

# Go Bump Version

Set a Go project's in-tree version literal to an exact value across every file that must agree with it, check that
the release build's `-ldflags -X` override still points at it, and, optionally, update README/Antora version
mentions. This skill never computes a version itself: it applies exactly the string it's given, validated for shape.
The "which version comes next" logic belongs to the caller (typically `iru-release`) and is defined in Step 5, the same
contract `iru-dotnet-bump-version`, `iru-python-bump-version` and the other `iru-<key>-bump-version` skills define for
their ecosystems. It never commits, tags, builds a release, or edits `go.mod`.

## Step 0 — Resolve inputs

- The positional argument is `<new-version>` (e.g. `1.4.0`, `1.5.0-dev`). Missing → ask for it before doing anything
  else; never guess or compute one here.
- `args` (`key: value` lines), if present:
  - `sync-files: yes|no` — also update README/Antora mentions (Step 7). Omitted → ask once with `AskUserQuestion`
    after Step 3 shows such mentions exist; don't ask when none do.
  - `next-version: <upcoming-version>` — the upcoming development version (e.g. `1.5.0-dev`) that "Current
    development version" markers should show after a release, while "Latest release" markers show `<new-version>`.
    Only meaningful with `sync-files: yes`; validated like `<new-version>`.
  - `files: <comma list>` — only look at these `.go` files (passed to the helper as `--files=`); default: every
    git-tracked non-test `.go` file outside `vendor/`, `testdata/`, `dist/`.
  - `dry-run: yes|no` — default `no`. `yes` runs everything through showing the diff, then stops: nothing is written;
    say so plainly in the report.

Reject before touching anything a value that is obviously not a version (empty, or containing whitespace).

## Step 1 — Validate the version string

Go module versions are semantic versions with a `v` prefix on the **tag** (`v1.4.0`); the in-tree literal, the
`-ldflags -X` value GoReleaser injects (`{{.Version}}` strips the `v`), and this catalog's convention carry no
prefix — `X.Y.Z` or `X.Y.Z-dev`:

```bash
python3 -c 'import re,sys; sys.exit(0 if re.fullmatch(r"\d+\.\d+\.\d+(-dev)?", sys.argv[1]) else 1)' "<new-version>"
```

- No match but `v`-prefixed (`v1.4.0`) → strip the `v`, say so, and continue (the tag keeps it; the literal doesn't).
- No match but still SemVer (`X.Y.Z-<pre-release>`, e.g. `-rc.1`, `-beta.2`) → warn that it doesn't follow the `-dev`
  convention and ask whether to proceed (`go` orders any SemVer pre-release correctly, and GoReleaser marks such a
  release as a pre-release).
- Anything else (`1.0`, `1.2.3.4`, build metadata `+x` — which Go module versions forbid on tags) → refuse.

Anything with a `-` suffix counts as a **pre-release**.

## Step 2 — Write the helper and survey the version locations

| Location | Rewritten to | When |
|---|---|---|
| `var Version = "…"` (or `var Version string = "…"`, or a `Version = "…"` line in a `var (…)` block) in a non-test `.go` file — `internal/version/version.go` in this catalog's scaffold | `<new-version>` | always |
| `const Version = "…"` (alone or in a `const (…)` block) | `<new-version>` | always — but reported: `-ldflags -X` can't override a constant (verified: the build succeeds and the binary keeps the literal), so a release pipeline injecting the tag has no effect |
| `-X <import path>.Version=…` in `.goreleaser.y*ml`, `Makefile`, `Taskfile.y*ml`, `justfile`, `.github/workflows/*.y*ml` | never rewritten — **checked**: the path must be `<module>/<dir>.Version` of a `var` (or `main.Version` for `package main`) | reported `ok` or `MISMATCH` |

Generated files (`// Code generated … DO NOT EDIT.`), `_test.go` files, `vendor/`, `testdata/` and `dist/` are never
touched. Other `…Version` identifiers (`MinVersion`, `APIVersion`, `SchemaVersion`) don't match the pattern and stay
untouched; a `Commit`/`Date` stamped next to `Version` is release-time metadata, not a version — left alone.

```bash
mkdir -p "$TMPDIR/iru-go-bump-version"
cat > "$TMPDIR/iru-go-bump-version/go_version.py" <<'PY'
import difflib, pathlib, re, subprocess, sys


def read(p):
    return p.read_bytes().decode("utf-8")  # no newline translation: CRLF files stay CRLF


args = sys.argv[1:]
dry, force = "--dry-run" in args, "--force" in args
files_arg = next((a.split("=", 1)[1] for a in args if a.startswith("--files=")), "")
args = [a for a in args if not a.startswith("--")]
new = args[0] if args else None          # None => --list
root = pathlib.Path(".")
SKIP = {"vendor", "testdata", "node_modules", ".git", "dist"}
# var Version = "x" | const Version = "x" | var Version string = "x" | a `Version = "x"` line inside a var (...) block
DECL = re.compile(r'^(?P<pre>\s*(?:(?:var|const)\s+)?Version(?:\s+string)?\s*=\s*")(?P<val>[^"\n]*)(?P<post>")', re.M)


def go_files():
    if files_arg:
        return [pathlib.Path(f) for f in files_arg.split(",") if f]
    try:
        out = subprocess.run(["git", "ls-files", "*.go"], capture_output=True, text=True, check=True).stdout.split()
        cand = [pathlib.Path(p) for p in out]
    except (FileNotFoundError, subprocess.CalledProcessError):
        cand = sorted(root.rglob("*.go"))
    return [p for p in cand if p.exists() and not p.name.endswith("_test.go")
            and not any(part in SKIP for part in p.parts)]


found = []                                # (path, line, value, kind, match)
for p in go_files():
    text = read(p)
    if re.search(r"^// Code generated .* DO NOT EDIT\.$", text, re.M):
        continue
    for m in DECL.finditer(text):
        line_start = text.rfind("\n", 0, m.start()) + 1
        block = text[:m.start()]
        kind = "const" if re.search(r"(?:^|\n)\s*const\b[^\n]*$", text[line_start:m.end()]) or \
            (block.rfind("const (") > block.rfind(")") and not m.group("pre").lstrip().startswith("var")) else "var"
        found.append((p, text.count("\n", 0, m.start()) + 1, m.group("val"), kind, m))

for p, line, val, kind, _ in found:
    print(f"{p.as_posix()}:{line}: {val}    [{kind} Version]")
    if kind == "const":
        print(f"note: {p.as_posix()} declares Version as a const — -ldflags -X can only override a package-level string var")
if not found:
    sys.exit('No `var Version = "…"` / `const Version = "…"` literal found in any non-test .go file')

mod = pathlib.Path("go.mod")
modpath = re.search(r"^module\s+(\S+)", read(mod), re.M).group(1) if mod.exists() else ""
print(f"module: {modpath}")
# -ldflags -X references must name <import path>.Version of a var, or the linker silently ignores them
targets = set()
for p, _, _, kind, _ in found:
    if kind != "var":
        continue
    pkg = re.search(r"^package\s+(\w+)", read(p), re.M).group(1)
    d = p.parent.as_posix()
    targets.add("main.Version" if pkg == "main" else f"{modpath}.Version" if d == "." else f"{modpath}/{d}.Version")
for cfg in [*root.glob(".goreleaser.y*ml"), *root.glob("Makefile"), *root.glob("Taskfile.y*ml"), *root.glob("justfile"),
            *root.glob(".github/workflows/*.y*ml")]:
    for n, line in enumerate(cfg.read_text(encoding="utf-8", errors="replace").splitlines(), 1):
        for ref in re.findall(r"-X[ =]['\"]?([\w./-]+\.Version)=", line):
            ok = "ok" if ref in targets else f"MISMATCH — no var at that path (expected one of {sorted(targets)}); the linker ignores it silently"
            print(f"ldflags: {cfg.as_posix()}:{n}: -X {ref}  [{ok}]")
values = sorted({f[2] for f in found})
if len(values) > 1:
    print(f"WARNING: Version literals disagree: {values}", file=sys.stderr)
    if new is not None and not force:
        sys.exit("Refusing to write: confirm with the user, then re-run with --force to align every literal")
if len(values) == 1:
    print(f"current: {values[0]}")
if new is None:
    sys.exit(0)

major = int(re.match(r"v?(\d+)", new).group(1))
suffix = re.search(r"/v(\d+)$", modpath)
if major >= 2 and (not suffix or int(suffix.group(1)) != major):
    print(f"WARNING: major version {major} needs the module path to end in /v{major} (go.mod says {modpath!r}); "
          f"consumers can't `go get` v{major}.x tags otherwise — changing it is a breaking import-path change, not done here",
          file=sys.stderr)
if major < 2 and suffix:
    print(f"WARNING: module path {modpath!r} has a /v{suffix.group(1)} suffix but the new version is {new}", file=sys.stderr)

edits = {}
for p, _, _, _, _ in found:
    text = edits.get(p, read(p))
    edits[p] = DECL.sub(lambda m: m.group("pre") + new + m.group("post"), text)
for p, text in edits.items():
    old = read(p)
    if text == old:
        continue
    if dry:
        sys.stdout.writelines(difflib.unified_diff(old.splitlines(True), text.splitlines(True), str(p), str(p)))
        continue
    p.write_bytes(text.encode("utf-8"))
    print(f"updated {p.as_posix()}")
PY
python3 "$TMPDIR/iru-go-bump-version/go_version.py" --list
```

Run it from the module root (the directory holding `go.mod`; in a `go.work` workspace, the root of the module that
builds the binary). Output: one `<file>:<line>: <value>    [var|const Version]` line per literal, `note:` lines,
`module: <path>`, one `ldflags: <file>:<line>: -X <ref>  [ok|MISMATCH …]` line per reference, and a `current:` line.
Then:

- **No literal anywhere** (non-zero exit: `No var Version … found`) — common for a Go **library**, whose version
  *is* its git tag: `go get example.com/lib@v1.4.0` resolves the tag, and nothing in the tree needs to change. Report
  "version comes from git tags (latest: `git describe --tags --abbrev=0`)", change nothing, and let `iru-release`
  treat the tag as the version (as for a Swift library). For a CLI that relies only on `debug.ReadBuildInfo()` —
  Go ≥ 1.24 stamps the main module's version from the VCS tag (verified: `go version -m` showed `v0.1.0+dirty` for a
  build at tag `v0.1.0` with a modified tree) and `go install …@vX.Y.Z` stamps `vX.Y.Z` — the same applies. Otherwise
  ask whether to add `internal/version/version.go` with `var Version = "<new-version>"` (the scaffold's layout) and
  re-run `--list` — never invent it silently.
- **Literals disagree** (`WARNING: Version literals disagree`) — show the list and ask whether to align them all to
  `<new-version>` (Step 4 then passes `--force`) or which to leave (edit the others by hand and say so in the report).
- **`const Version`** note — tell the user an `-ldflags -X` override can't work with it; suggest changing `const` to
  `var` (a one-word code change the user approves — not made here).
- **`ldflags … MISMATCH`** — the release build injects a version into a path with no such `var` (a moved package, a
  renamed module, a typo); the linker ignores it **silently** (verified), so released binaries would print the
  committed literal. Report it prominently; fixing the pipeline file is a follow-up for the user or
  `iru-setup-cli-github-workflows`.
- The current version for the report, and for `iru-release` (which reads it this way), is the `current:` line.

## Step 3 — Look for mirrored mentions

```bash
grep -n -i "latest release\|current development version\|go install \|go get \|@v[0-9]" README.md 2>/dev/null
grep -rln -i "latest release\|go install \|go get " docs/modules/ROOT/pages 2>/dev/null; grep -n '^version:' docs/antora.yml 2>/dev/null
```

Only when something turns up is `sync-files` worth asking about (Step 0). `go install …@latest` snippets need no
change; `@vX.Y.Z` pins do (Step 7). Golden files of a `--version` test (`testdata/script/*.txtar` matching
`version 0.1.0-dev`, `testdata/*.golden`) also mirror the literal — list them in the report as tests the caller must
update (this skill doesn't edit tests); a scaffold that reads `version.Version` in its assertions needs nothing.

## Step 4 — Preview (`dry-run: yes`) or apply

```bash
python3 "$TMPDIR/iru-go-bump-version/go_version.py" "<new-version>" --dry-run   # unified diff only
python3 "$TMPDIR/iru-go-bump-version/go_version.py" "<new-version>"             # write
```

Add `--force` only after the user confirmed aligning disagreeing literals (Step 2), and `--files=<a.go>,<b.go>` when
`files:` was given. The helper rewrites only the string inside each matched `Version` literal, keeping CRLF line
endings and everything else byte-for-byte. A `WARNING: major version N needs the module path to end in /vN` on stderr
→ include it in the report verbatim (Step 5). A non-zero exit at any point → stop, show the error, and treat nothing as
updated; never fall back to hand edits.

## Step 5 — The Go-catalog pre-release convention (for `iru-release` and other callers)

The Go equivalent of `iru-java-bump-version`'s `-SNAPSHOT` and `iru-dotnet-bump-version`'s `-dev` — the contract
`iru-release` calls this skill against (two calls per release, each passing a computed `<new-version>`), and the one
the `sync.yml` written by `iru-setup-cli-github-workflows` and the `iru-setup-go-cli` scaffold use:

- **Current development version**: `x.y.z-dev` (e.g. `1.4.0-dev`) in the `Version` literal on the gitflow integration
  branch. SemVer orders `1.4.0-dev` before `1.4.0` and after `1.3.0`. A local `go build` prints it; a main-only
  repository has no development marker — the literal is always the last or next release `x.y.z`.
- **The git tag is the source of truth for module consumers**: releases are tagged `vX.Y.Z` (with the `v` — the go
  command ignores tags without it). `go install <module>/cmd/<bin>@vX.Y.Z` builds from the tag **without** any
  `-ldflags`, so the committed literal is what those users see — which is why the release commit carries `X.Y.Z`, not
  `X.Y.Z-dev`. The release workflow (GoReleaser) injects the tag again via `-X …Version={{.Version}}` and checks that
  the tag minus `v` equals the literal. Never tag `-dev` versions.
- **Major version 2 and above**: Go's semantic import versioning requires the module path to end in `/vN`
  (`module github.com/acme/tool/v2`) and every internal import to use it. The helper warns when `<new-version>`'s
  major is ≥ 2 and the suffix is missing or different; the path change is a breaking, repository-wide import rewrite
  the user does deliberately (and announces) — never part of a version bump. A `cmd/` binary that nobody imports is
  still affected: `go install …@v2.0.0` fails without the `/v2` path.
- **Cutting a release**: strip the suffix — `x.y.z-dev` → `x.y.z`. Call this skill with `<new-version>: x.y.z`, commit,
  tag `vx.y.z`.
- **Opening the next development cycle**: bump the minor (this catalog's default, matching `iru-release`'s
  recommended "minor bump" and the `sync.yml` workflow) and re-append `-dev` — `x.y.z` → `x.(y+1).0-dev`; a patch or
  major bump is the caller's choice. Call this skill again (or let `sync.yml` do it after the release is published)
  with that exact value — this skill never decides which component to bump.
- **Tag-only projects** (no literal — Step 2): the release is the git tag. `iru-release` skips its "must currently be
  a pre-release" check and its next-version question for them, exactly as for a Swift library. In a multi-module
  repository, a nested module's tags carry its directory prefix (`tools/v1.2.0`) — say so when `go.mod` isn't at the
  repository root.

## Step 6 — Sanity check

Skip with `dry-run: yes`. Otherwise:

```bash
python3 "$TMPDIR/iru-go-bump-version/go_version.py" --list     # every literal shows the new value, no warning
go build -o build/iru-go-bump-version-bin ./cmd/<bin> && ./build/iru-go-bump-version-bin --version
rm -f build/iru-go-bump-version-bin
```

The binary must print `<new-version>` (a CLI with a different version command, e.g. `<bin> version`, is run that way;
a library with no binary just needs `go build ./...` and `go vet ./<version package>` to pass). Without a Go
toolchain, say the build check wasn't run rather than assume it passed.

## Step 7 — Optionally sync other files that mirror the version

Ask (or honor `sync-files`) whether to update the mentions Step 3 found, mapping each by what it names — the same rule
as `iru-java-bump-version`'s Step 7:

- "Latest release" markers (and a `Latest release` row in the README's status table) and pinned install snippets
  (`go install <module>/cmd/<bin>@vX.Y.Z`, `go get <module>@vX.Y.Z` — note the `v`), Homebrew/Scoop/WinGet commands
  pinned to a version → `<new-version>` (with `v` where the snippet uses a tag) only when it is a release.
- "Current development version" markers → `next-version` when given; otherwise `<new-version>` only if it is a `-dev`
  value, and untouched (warn in Step 8 that the caller should pass `next-version`) when it's a release — never regress
  a development marker to a release value.
- `docs/antora.yml` `version:` → `<new-version>` only for a release (Antora's component version names released
  versions; skip `-dev`), if the site tracks the release version at all.
- Antora pages under `docs/modules/ROOT/pages/` with the same markers/snippets → as for the README. A generated CLI
  reference page (written by the scaffold's `gendocs` tool) is regenerated, not hand-edited — mention it.

Targeted, scoped substitutions only — never a repository-wide replace of the old string. A README badge pulling the
version live (GitHub release, pkg.go.dev, Homebrew shields) must not be rewritten.

## Step 8 — Report

- Every literal from `--list` with its old and new value, `const` notes, and every `-ldflags -X` reference with
  `ok`/`MISMATCH`.
- Every file changed (by the script and by Step 7), or that nothing changed because the version comes from git tags.
- Any disagreement aligned with `--force` after the user confirmed, golden/test files that mirror the old value, and
  whether this was a `dry-run`; the Step 6 result (`--list` agreement, `--version` output or "not run").
- **Warn explicitly**: review the diff before committing (this skill commits and tags nothing); tag releases as
  `v<new-version>`; a major ≥ 2 needs the `/vN` module path (with the helper's warning verbatim) before it can be
  consumed with `go get`/`go install`.

## Verification notes

Verified in `$TMPDIR/iru-verify/cli/go-gates/demo` (Go 1.27.2, host `python3` 3.9, a throwaway Cobra CLI module
committed to a throwaway git repository) by running the exact helper above:

- `--list` on the scaffold layout (`internal/version/version.go`: `var Version = "0.1.0-dev"`) printed the literal,
  `module: github.com/example/democtl`, `current: 0.1.0-dev`, and for a `.goreleaser.yaml` with
  `-X github.com/example/democtl/internal/version.Version={{.Version}}` → `[ok]`, while a second `-X
  …/internal/versionX.Version=…` line → `MISMATCH`.
- `0.1.0 --dry-run` printed the unified diff and left the file unchanged; `0.1.0` rewrote it; `2.0.0-dev --dry-run`
  warned `major version 2 needs the module path to end in /v2`. A `var (…)` block, `const Version = "…"` and
  `Version string = "…"` inside `const (…)` were found, the two constants with the `-ldflags -X` note; a second
  literal in `package main` produced `Version literals disagree`, a refusal without `--force`, and both rewritten
  with it (expected `-X` target `main.Version` listed).
- `go build -ldflags "-X …/internal/version.Version=9.9.9"` → `democtl version 9.9.9`; the same flag against a
  `const Version`, and against a misspelled package path, built without error and printed `0.1.0-dev` — the silent
  no-op the helper's checks exist for.
- `go version -m` on a binary built at tag `v0.1.0` (dirty tree) showed `mod github.com/example/democtl
  v0.1.0+dirty` (Go ≥ 1.24 VCS version stamping).
- Not verified: `go install …@vX.Y.Z` from a published module (needs a public repository), nested-module tag prefixes,
  and CRLF files on Windows (the helper reads/writes bytes without newline translation).

## Sources

- go.dev/ref/mod (module paths, `/vN` major version suffixes, version queries, tags `vX.Y.Z`, nested-module tag
  prefixes); go.dev/doc/modules/version-numbers and go.dev/doc/modules/major-version
- go.dev: `go doc cmd/link` (`-X importpath.name=value` — string variables only), Go 1.24 release notes (main-module
  version from VCS in build info), pkg.go.dev/runtime/debug#ReadBuildInfo
- GoReleaser docs (goreleaser.com): builds `ldflags`, `{{.Version}}` (tag without `v`)
- irurueta docs: ai/cli-for-agents/self-describing-help.adoc (`--version` on stdout, `version --json` build metadata),
  ai/cli-for-agents/packaging-and-distribution.adoc (versioned release archives, tags)
