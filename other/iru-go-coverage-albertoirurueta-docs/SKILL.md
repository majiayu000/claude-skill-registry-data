---
name: iru-go-coverage
description: >-
  Run a Go module's (or Go workspace's) container-free tests with statement coverage — `go test -covermode=atomic -coverpkg=./... -coverprofile=build/coverage/cover.out` — and read the profile with a small stdlib Python parser that merges the per-test-binary duplicate blocks `-coverpkg` writes, maps import paths back to repository-relative files, excludes generated files (`// Code generated … DO NOT EDIT.`), and reports the exact statement % for the total and per file (with uncovered line ranges for files under the bar). `-coverpkg=./...` makes code exercised from another package's tests count — including in-process testscript end-to-end tests that run the Cobra command tree, whose re-executed subprocess coverage testscript merges into the profile — so a thin `cmd/<bin>/main.go` and `internal/cli` are measured fairly. Optionally merges a second profile from instrumented binaries (`go build -cover` + `GOCOVERDIR` + `go tool covdata textfmt`). Branch coverage is reported as "not available in Go" (the toolchain measures statements only). Only container-free tests count toward the gate — the `integration` build tag is not set unless asked, and then the result is labeled as not the gate value. Invoke as `/iru-go-coverage [targets]` — `[targets]` is a comma-separated list of Go files (`internal/greet/greet.go`), package directories (`internal/cli`), or import paths — or `/iru-go-coverage` with no argument for whole-module coverage; optional `key: value` lines: `bar: <N>` (default 80), `coverpkg: <pattern>` (default `./...`), `tags: <comma list>`, `run: <regex>` (narrow the tests), `profile: <extra coverprofile>` (merge, e.g. a `covdata textfmt` output), `lock: held`. Reports "coverage not measurable" instead of a false 0% when a target has no statements or lies outside `-coverpkg`. Report-only: never adds tests or modifies source. Use whenever the user (or `iru-go-code-one-task-group` via `iru-gate-runner`) wants to check, or verify a bar for, a Go file, package, or the whole module, instead of reading `go tool cover -func` output by hand.
model: haiku
allowed-tools: Read Write Bash(go *) Bash(GOFLAGS=* go *) Bash(GOCOVERDIR=* *) Bash(python3 *) Bash(docker info *) Bash(command -v *) Bash(git rev-parse *) Bash(find *) Bash(grep *) Bash(ls *) Bash(cat *) Bash(test *) Bash(date *) Bash(mkdir -p build*) Bash(mkdir .integration-test.lock*) Bash(rmdir .integration-test.lock*) Bash(rm -f .integration-test.lock/owner) Bash(rm -f build/coverage/*) Bash(rm -rf build/coverage/covdata*)
---

# Go Coverage

Run the module's fast (container-free) tests with Go's statement coverage and report the exact, measured coverage for
the files the user cares about, read from the coverprofile. This skill only measures and reports coverage — it does
not add tests, modify source/test code, or change any configuration unless asked to as a follow-up.

## Step 1 — Determine scope and test selection

- **Targets** (optional, comma-separated): Go files (`internal/greet/greet.go`), package directories (`internal/cli`
  — the files directly in it), directory trees (`internal/cli/...` — the directory and everything below), or import
  paths (`github.com/acme/tool/internal/cli` → its directory via `go list -f '{{.Dir}}' <path>`, made relative). No
  targets → every file in the profile.
- **`bar: <N>`** — the threshold to judge each target against; default **80** (this catalog's group gate).
- **`coverpkg: <pattern>`** — what is instrumented; default `./...` (Step 2 explains why). In a `go.work` workspace
  whose root isn't a module, the default is one `./<dir>/...` per workspace module, comma-joined (`go list -m -f
  '{{.Dir}}'`, verified: `./...` alone fails there), and the test patterns are those same `./<dir>/...` entries.
- **`tags:`**, **`run:`** — as in `iru-go-test` Step 0. A `run:` filter undercounts code other tests also exercise —
  say which tests ran; prefer the whole fast suite when in doubt.
- **`profile: <path>`** — an extra coverprofile to merge (e.g. Step 4's binary coverage).
- **`lock: held`** — only meaningful with `tags: integration` (Step 3).

Detect the toolchain, module/workspace layout, vendoring, and race-detector availability exactly as `iru-go-test`
Steps 1–2 do; a wiring failure there (no Go, inconsistent vendoring, `go.mod requires go >= …`) stops this skill too.

## Step 2 — Run the coverage build

```bash
rm -f build/coverage/cover.out && mkdir -p build/coverage build/test-results
go test -count=1 -covermode=atomic -coverpkg=<coverpkg> -coverprofile=build/coverage/cover.out \
  [-tags <tags>] [-run '<regex>'] -json <test patterns, default ./...> > build/test-results/go-test.json
```

- **`-coverpkg=./...`** instruments every package of the module in every test binary, so a package with no tests of
  its own (`cmd/<bin>`, `internal/version`) and code reached only through another package's tests (the CLI tests in
  `internal/cli` driving `internal/greet`) are counted. Without it, each package is measured only by its own tests
  and `cmd/<bin>/main.go` never appears. The profile then repeats every block once per test binary — the parser
  merges them (a block counts as covered if any binary hit it).
- **In-process testscript e2e tests count**: `testscript.Main` re-executes the test binary for each `exec <bin>` line,
  and go-internal merges those subprocesses' coverage into the profile (verified: `cli.Main`, reached only from
  `.txtar` scripts, measured 83.3% → 100% as scripts were added).
- **`-covermode=atomic`** is the mode `-race` requires and is safe with parallel tests; this run doesn't add `-race`
  (`iru-go-test` covers that), which keeps it faster.
- **Test failures**: the profile is still written when tests fail (verified) — report the coverage but say it comes
  from a failing run, and list the failures by parsing `build/test-results/go-test.json` with `iru-go-test`'s Step 6
  parser. A **build failure** leaves that package's blocks out of the profile (or no profile at all) — report it and
  never read a stale file (hence the `rm -f` first).
- **Integration coverage** only when `tags` contains `integration`: run it through `iru-go-test` Step 5 (Docker
  check + `.integration-test.lock`, `lock: held` honored) with `-coverprofile=build/coverage/cover-integration.out`,
  and report it separately, labeled "includes container-backed tests — not the gate value".

## Step 3 — Optional: coverage of the real binary (Go ≥ 1.20)

When the project's end-to-end tests run a **built binary as a subprocess** (a shell/bats/Python harness, or Go tests
that `exec.Command` a binary built in `TestMain` instead of testscript's in-process re-exec), that code is invisible to
`-coverprofile`. Instrument the binary instead:

```bash
rm -rf build/coverage/covdata && mkdir -p build/coverage/covdata
go build -cover -covermode=atomic -coverpkg=./... -o build/coverage/<bin>-cover ./cmd/<bin>
GOCOVERDIR=build/coverage/covdata <run the e2e harness against build/coverage/<bin>-cover>
go tool covdata percent -i=build/coverage/covdata                       # per-package summary
go tool covdata textfmt -i=build/coverage/covdata -o build/coverage/e2e.out
```

`textfmt` writes the same legacy profile format as `-coverprofile` (verified), so pass `profile:
build/coverage/e2e.out` and the parser merges it with the unit profile. Only do this when the user asks or the
project already wires it (a `GOCOVERDIR` in its Makefile/CI) — the harness is the project's, not this skill's.

## Step 4 — Read the exact coverage from the profile

Profile lines are `<import path>/<file>.go:<startLine>.<startCol>,<endLine>.<endCol> <statements> <count>`. Statement
% = covered statements / statements. `go tool cover -func` only gives per-*function* figures (and a total), so per
*file* figures come from this parser (verified: its total matched `go tool cover -func`'s `total: (statements)
76.9%`, and per-file sums matched the per-function rows). Pass the profile(s) comma-joined, then the targets, then
the bar:

```bash
python3 - build/coverage/cover.out[,build/coverage/e2e.out] 'internal/greet/greet.go,internal/cli' 80 <<'PY'
import os
import re
import subprocess
import sys

profile = sys.argv[1]
want = [w.strip().rstrip("/") for w in (sys.argv[2] if len(sys.argv) > 2 else "").split(",") if w.strip()]
bar = float(sys.argv[3]) if len(sys.argv) > 3 else 80.0

# Map import-path file names (github.com/o/r/internal/x/y.go) back to repo-relative paths via go list.
mods = subprocess.run(["go", "list", "-m", "-f", "{{.Path}} {{.Dir}}"], capture_output=True, text=True).stdout.split("\n")
roots = [l.split(" ", 1) for l in mods if " " in l]       # one line per module (several in a go.work)
cwd = os.path.realpath(os.getcwd())


def rel(name):
    for path, d in sorted(roots, key=lambda r: -len(r[0])):
        if name == path or name.startswith(path + "/"):
            return os.path.relpath(os.path.join(os.path.realpath(d), name[len(path) + 1:]), cwd)
    return name


blocks = {}                                     # (file, block) -> [stmts, hit]
lines = [ln for prof in profile.split(",") if prof for ln in open(prof)]   # several profiles merge
for line in lines:
    if line.startswith("mode:"):
        continue
    m = re.match(r"^(.+\.go):(\d+\.\d+,\d+\.\d+) (\d+) (\d+)$", line.strip())
    if not m:
        continue
    key = (m[1], m[2])                          # -coverpkg repeats every block once per test binary: merge
    b = blocks.setdefault(key, [int(m[3]), False])
    b[1] = b[1] or int(m[4]) > 0

GEN = re.compile(r"^// Code generated .* DO NOT EDIT\.$", re.M)
files = {}
for (f, blk), (n, hit) in blocks.items():
    s = files.setdefault(f, {"stmts": 0, "hit": 0, "miss": set()})
    s["stmts"] += n
    if hit:
        s["hit"] += n
    elif n:
        start, end = blk.split(",")
        s["miss"].update(range(int(start.split(".")[0]), int(end.split(".")[0]) + 1))


def ranges(nums):
    out = []
    for n in sorted(nums):
        if out and n == out[-1][1] + 1:
            out[-1][1] = n
        else:
            out.append([n, n])
    return ", ".join(str(a) if a == b else f"{a}-{b}" for a, b in out)


def pct(h, n):
    return f"{100 * h / n:.2f}%" if n else "n/a"


def match(path, w):
    if w.endswith("/..."):
        return path.startswith(w[:-4] + "/")
    return path == w or os.path.dirname(path) == w


th = tn = 0
rows, generated = [], []
for f in sorted(files):
    path, s = rel(f), files[f]
    try:
        head = open(path, encoding="utf-8", errors="replace").read(4096)
    except OSError:
        head = ""
    if GEN.search(head):                       # generated code never counts toward the bar
        generated.append(path)
        continue
    th, tn = th + s["hit"], tn + s["stmts"]
    if want and not any(match(path, w) for w in want):
        continue
    rows.append((path, s))
print(f"TOTAL statements {th}/{tn} ({pct(th, tn)}) branches: not available in Go")
for path, s in rows:
    p = 100 * s["hit"] / s["stmts"] if s["stmts"] else 100.0
    flag = "" if p >= bar else f" BELOW {bar:g}% uncovered: {ranges(s['miss'])}"
    print(f"{path} statements {s['hit']}/{s['stmts']} ({pct(s['hit'], s['stmts'])}){flag}")
if generated:
    print(f"excluded (generated): {', '.join(generated)}")
for w in want:
    if not any(match(r[0], w) for r in rows):
        print(f"NOT IN PROFILE {w} — no statements, outside -coverpkg, generated, or its package failed to build")
PY
```

Interpreting it:

- **Generated files** (the standard `// Code generated … DO NOT EDIT.` line, e.g. `stringer`/`mockgen`/protobuf
  output) are excluded from both the total and the per-file list and named on one line (verified).
- **`NOT IN PROFILE`** — a file with no executable statements (only `var`/`const`/type declarations, such as
  `internal/version/version.go` or a `doc.go`), a package outside `-coverpkg`, a generated file, or a package that
  failed to build. Say which (check `go-test.json` for build failures); never report it as 0%. A file present with
  `0/N` genuinely is 0%.
- **Thin entry points**: `cmd/<bin>/main.go` holding only `os.Exit(cli.Main(ctx, os.Args[1:], …))` is one or two
  statements reached only when the real binary runs — testscript's in-process `exec` calls the registered
  function, not `main()`, so it stays uncovered under `go test` (verified: `0/1`) unless Step 3's binary coverage is
  merged (verified: `1/1`). Report it as "thin entry point, exercised by the binary — excluded from the bar" when it
  contains no logic (no branches, only the `Main` call); if it holds real logic, it counts like any file and the
  finding is "move the logic into `internal/cli`".
- **Branches**: Go's coverage is statement-based (blocks between branch points); there is no branch metric — say
  "branch coverage: not available in Go" rather than inventing one. An uncovered `if` arm shows up as uncovered lines.

Leave `build/coverage/cover.out` in place when `build/` is gitignored (CI and `sonar.go.coverage.reportPaths` read
it); otherwise delete it after parsing (`rm -f build/coverage/*`).

## Step 5 — Report results

State the toolchain, how coverage was collected (`-coverpkg=<pattern>`, `-covermode=atomic`, whether a binary
profile was merged), the test selection (and that `integration`-tagged tests were not compiled), and whether the
tests passed. Then, computed from the actual profile — never estimated:

- **Total**: statement % and whether it meets the bar; "branch coverage: not available in Go".
- **Per target** (or per file, for an unscoped run with few files): statement %, and for every target under the bar
  the uncovered line ranges (`internal/greet/greet.go: 71.43% (5/7) — uncovered: 18-19, 27`) so the user, or a
  follow-up coding step, knows where to add tests. Name excluded generated files and thin entry points, and every
  `NOT IN PROFILE` target with its reason.

Never paste the profile or `go tool cover` output. If the run never started (wiring problem) or a target's package
failed to build, report that instead of a percentage, with the exact command and the fix. Do not add tests, modify
source/test code, or re-run to raise the number — that's a follow-up the user (or a coding skill) drives explicitly.

## Verification notes

Verified with Go 1.27.2 (darwin/arm64), cobra 1.10.2 and go-internal 1.16.0 (testscript) in
`$TMPDIR/iru-verify/cli/go-gates/demo` (a throwaway Cobra CLI module outside this repository):

- `go test -count=1 -covermode=atomic -coverpkg=./... -coverprofile=… ./...` exited `1` (one deliberately failing test)
  but still wrote the profile; it listed each block once per test binary. The parser reported `TOTAL statements
  20/26 (76.92%)` — `go tool cover -func` said `total: (statements) 76.9%` — with `internal/cli/cli.go 15/18
  (83.33%)` (= `Main 83.3%`), `internal/greet/greet.go 5/7 (71.43%) BELOW 80% uncovered: 18-19, 27`, and
  `cmd/democtl/main.go 0/1`. `cli.Main` was reached only from in-process testscript scripts.
- A `// Code generated by stringer; DO NOT EDIT.` file was excluded and named; `internal/version/version.go` (only
  `var` declarations) and an unknown target came back `NOT IN PROFILE`; target filters by file and by directory worked.
- `go build -cover -covermode=atomic -coverpkg=./...` + `GOCOVERDIR=… ./democtl-cover greet Zed` (and a failing
  `greet ""`, exit 3) wrote `covmeta`/`covcounters` files; `go tool covdata percent` printed per-package figures and
  `go tool covdata textfmt` a legacy profile; merged with the unit profile, `cmd/democtl/main.go` became `1/1` and
  the total `24/30 (80.00%)`.
- A two-module `go.work` workspace: `-coverpkg=./a/...,./b/...` with `./a/... ./b/...` produced a merged profile
  that the parser mapped back to `a/a.go`/`b/b.go` via `go list -m`.
- Still unverified: Windows paths, profiles from `-tags integration` runs with real containers merged into the gate
  number (deliberately not done), and very large modules (the parser holds every block in memory).

## Sources

- go.dev: `go help testflag` (`-cover`, `-covermode`, `-coverpkg`, `-coverprofile`), go.dev/blog/cover (statement
  coverage, block profile format), go.dev/doc/build-cover (Go 1.20 `go build -cover`, `GOCOVERDIR`, `go tool covdata
  percent|textfmt|merge`), go.dev/ref/mod (workspaces), `go generate` docs (the `Code generated … DO NOT EDIT.`
  convention)
- pkg.go.dev: github.com/rogpeppe/go-internal/testscript (`Main` re-exec of the test binary)
- irurueta docs: ai/cli-for-agents/testing-clis.adoc (thin entry point, logic in a testable core, in-process
  testscript end-to-end tests)
