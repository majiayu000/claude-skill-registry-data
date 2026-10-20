---
name: iru-rust-coverage
description: >-
  Measure a Rust project's test coverage — a single crate or a Cargo workspace, e.g. a command-line tool whose logic lives in `src/lib.rs` behind a thin `src/main.rs` — with cargo-llvm-cov (source-based LLVM coverage; `cargo llvm-cov nextest` when cargo-nextest is installed, plain `cargo llvm-cov` otherwise), always `--locked`, running the tests once with `--no-report` and then writing an lcov file (`target/coverage/lcov.info`, per-line hits) and a JSON summary (`target/coverage/summary.json`, per-file line/region/function figures), read with a small stdlib Python parser. Reports the exact line % (the gate figure) and region % for the total and per target file, with uncovered line ranges for every file under the bar; branch coverage is reported as unavailable on a stable toolchain (`--branch` needs nightly). Binaries spawned by end-to-end tests (assert_cmd's `Command::cargo_bin`) are instrumented too, so `src/main.rs` is measured fairly. Excludes `xtask/` (and any other tooling member) from the report with `--ignore-filename-regex`; `tests/` files are never reported; doctests don't count on stable (`--doctests` is nightly-only). Only container-free tests count — `#[ignore]` tests are never run here — and the report is still produced from a run with failing tests (labeled as such). Never uses `--fail-under-*`: it judges the bar itself. Invoke as `/iru-rust-coverage [targets]` — `[targets]` is a comma-separated list of source files (`src/commands/greet.rs`), directories (`src/commands/`), or module paths (`crate::output`, `commands::greet`, `<member_crate>::config`) — or `/iru-rust-coverage` with no argument for the whole workspace; optional `key: value` lines: `bar: <N>` (default 80), `package: <name>`, `features: all|<comma list>`, `filter: <test filter>` (a test-name substring, or `expr:<nextest filterset>`). Reports "coverage not wired" (cargo-llvm-cov or `llvm-tools-preview` missing) instead of a false 0%. Use whenever the user (or `iru-rust-code-one-task-group` via `iru-gate-runner`) wants to check, or verify a bar for, a Rust file, module, or the whole workspace, instead of eyeballing `cargo llvm-cov` tables.
model: haiku
allowed-tools: Read Bash(cargo *) Bash(python3 *) Bash(rustup *) Bash(command -v *) Bash(find *) Bash(grep *) Bash(ls *) Bash(cat *) Bash(test *) Bash(mkdir -p target*) Bash(rm -f target/coverage/*)
---

# Rust Coverage

Run the project's container-free tests under cargo-llvm-cov and report the exact, measured line (and region) coverage
for the files the user cares about, read from an lcov file and llvm-cov's JSON summary. This skill only measures and
reports coverage — it does not add tests, modify source/test code, change coverage configuration, or install tools
unless asked to as a follow-up.

## Step 0 — Parse the arguments

- **Targets** (optional, comma-separated): source files (`src/commands/greet.rs`), directories (`src/commands/`), or
  module paths. Resolve a module path against the owning package's library root from `cargo metadata --no-deps`
  (the `lib` target's `src_path`, usually `<member>/src/lib.rs`): `crate::commands::greet` / `commands::greet` →
  `src/commands/greet.rs`, else `src/commands/greet/mod.rs`, else the directory `src/commands/greet/`;
  `<member_crate>::config` → that member's `src/config.rs`. `crate::output::Envelope` (an item, not a module) →
  the file that defines it (`grep -rn "struct Envelope\|enum Envelope" <member>/src`). No targets → every reported
  file.
- **`bar: <N>`** — the threshold to judge each target's line % against; default **80** (this catalog's group gate).
- **`package: <name>`** — one workspace member (`-p <name>`); default `--workspace`.
- **`features: all|<comma list>`** — `--all-features` / `--features a,b`; default features otherwise.
- **`filter: <x>`** — narrows the test run: a test-name substring, or `expr:<filterset>` (nextest only). Coverage is
  only recorded for code the selected tests execute — a narrow filter undercounts a module that other tests also
  exercise; prefer the whole suite when judging a bar and say which tests ran.

## Step 1 — Check that coverage is wired (never trust a 0% without this)

```bash
cargo llvm-cov --version                                   # cargo-llvm-cov installed?
rustup component list --installed | grep -E '^llvm-tools'  # llvm-tools-preview for the active toolchain?
cargo nextest --version                                    # optional: run through nextest
```

- **No cargo-llvm-cov** → stop: "coverage not wired — install cargo-llvm-cov (`cargo install cargo-llvm-cov --locked`,
  or `taiki-e/install-action` in CI)". Don't install it yourself.
- **No `llvm-tools`** → cargo-llvm-cov offers to install it interactively; don't answer for the user: report
  "`llvm-tools-preview` missing — `rustup component add llvm-tools-preview` (this catalog's `rust-toolchain.toml`
  lists it under `components`)".
- Run from the workspace root. Use `--locked` when `Cargo.lock` exists (a stale lock fails exactly as in
  `iru-rust-test` Step 1 — report it, don't update it).

## Step 2 — Run the tests once, instrumented

```bash
mkdir -p target/coverage && rm -f target/coverage/lcov.info target/coverage/summary.json
cargo llvm-cov clean --workspace          # drop stale .profraw data from earlier runs

# nextest installed (preferred — same runner as iru-rust-test):
cargo llvm-cov nextest --locked --no-fail-fast --no-report <--workspace | -p NAME> [--all-features|--features a,b] \
  [-E '<filterset>' | -- <substring>] > target/coverage/run.log 2>&1
# otherwise:
cargo llvm-cov --locked --no-fail-fast --no-report <--workspace | -p NAME> [--all-features|--features a,b] \
  [-- <substring>] > target/coverage/run.log 2>&1
```

- **Spawned binaries count**: cargo-llvm-cov builds into `target/llvm-cov-target/` with instrumentation and sets
  `LLVM_PROFILE_FILE`, so the binary `assert_cmd::Command::cargo_bin("<bin>")` launches from an integration test
  writes its own profile — `src/main.rs` showed up 7/7 lines covered purely from `tests/cli.rs` (verified). A test
  that runs a binary from somewhere else (`target/debug/<bin>` by hard-coded path, a `cargo run` subprocess) isn't
  instrumented: say so if the e2e tests do that.
- **Failing tests**: the run exits non-zero (`100` nextest, `101` cargo test) but the profile data is kept, and the
  report in Step 3 still works (verified) — report the coverage, label it "from a run with failing tests", and list
  the failures by running `iru-rust-test`'s Step 5 parser on `target/coverage/run.log` (libtest form) or naming them
  from nextest's `FAIL` lines. A **build failure** (`could not compile`) produces no data — report that cause and
  never read a stale file. (`--ignore-run-fail` also tolerates failures but can't be combined with `--no-fail-fast`
  and is marked unstable — don't use it.)
- **Ignored tests** (`#[ignore = "…"]`, this catalog's container-backed tests) are not run: the gate number must be
  reproducible without Docker. If the user explicitly asks for integration coverage, run the same command with
  `--run-ignored all` (nextest) / `-- --include-ignored` through `iru-rust-test`'s Step 3 (Docker check +
  `.integration-test.lock`, `lock: held` honored), write it to `target/coverage/lcov-integration.info`, and label it
  "includes container-backed tests — not the gate value".
- **Doctests** don't contribute: `--doctests` needs nightly (on stable it fails with `the option Z is only accepted on
  the nightly compiler`, verified). Say so when a target is mostly exercised by its doc examples.
- Never pass `--fail-under-lines`/`--fail-under-regions`/`--fail-under-file-lines`: the caller gates, and those flags
  would turn a measurement into a failed command.

## Step 3 — Write the reports

```bash
R='(^|/)xtask/'      # add other tooling-only members/dirs here, e.g. '(^|/)(xtask|fuzz|benches)/'
cargo llvm-cov report --ignore-filename-regex "$R" --lcov --output-path target/coverage/lcov.info
cargo llvm-cov report --ignore-filename-regex "$R" --json --summary-only --output-path target/coverage/summary.json
```

- `--ignore-filename-regex` is matched against **absolute** paths — keep the `(^|/)…/` anchoring so it can't match a
  parent directory name by accident. Exclude only tooling (`xtask`, fuzz targets, bench harnesses), never product code
  to lift a number; say what was excluded. Integration-test files under `tests/` and dependency sources are already
  left out by cargo-llvm-cov (verified: `tests/cli.rs` never appeared).
- `--branch` (and branch data) needs a nightly toolchain: on stable it warns `--branch flag requires nightly
  toolchain` and the build fails on `-Z` (verified). Report branch coverage as **unavailable on stable**; only when the
  project's own toolchain is nightly may you add `--branch` to both the run and the report, then read `BRF`/`BRH`.
- Unit tests in `#[cfg(test)] mod tests` blocks live in the same file as the code, so their lines count toward that
  file's total (verified: `lib.rs`'s test functions appear in its `DA:` lines, and an ignored test's body shows as
  uncovered). `#[coverage(off)]` is unstable (`E0658` on stable, verified) — just mention the effect when a file's
  only misses are test code.

## Step 4 — Read the exact coverage

lcov gives per-line hits (`SF:`/`DA:<line>,<hits>`/`LF`/`LH`); the JSON summary (`llvm.coverage.json.export` 3.x:
`data[0].files[].summary.{lines,regions,functions,branches}` and `data[0].totals`) gives regions. Parse both:

```bash
python3 - target/coverage/lcov.info target/coverage/summary.json 'src/commands/greet.rs,src/output/' 80 <<'PY'
import json
import os
import sys

lcov_path, summary_path = sys.argv[1], sys.argv[2]
want = [w.strip().rstrip("/") for w in (sys.argv[3] if len(sys.argv) > 3 else "").split(",") if w.strip()]
bar = float(sys.argv[4]) if len(sys.argv) > 4 else 80.0
root = os.path.realpath(os.getcwd())


def rel(p):
    p = os.path.realpath(p)
    return os.path.relpath(p, root) if p.startswith(root + os.sep) else p


def pct(c, v):
    return f"{100 * c / v:.2f}%" if v else "n/a"


def ranges(nums):
    out = []
    for n in sorted(nums):
        if out and n == out[-1][1] + 1:
            out[-1][1] = n
        else:
            out.append([n, n])
    return ", ".join(str(a) if a == b else f"{a}-{b}" for a, b in out)


files, cur = {}, None
for ln in open(lcov_path):
    ln = ln.rstrip("\n")
    if ln.startswith("SF:"):
        cur = files.setdefault(rel(ln[3:]), {"da": {}, "brf": 0, "brh": 0})
    elif ln.startswith("DA:") and cur is not None:
        n, hits = ln[3:].split(",")[:2]
        cur["da"][int(n)] = max(cur["da"].get(int(n), 0), int(hits))
    elif ln.startswith("BRF:") and cur is not None:
        cur["brf"] += int(ln[4:])
    elif ln.startswith("BRH:") and cur is not None:
        cur["brh"] += int(ln[4:])
regions = {}
data = json.load(open(summary_path))["data"][0]
for f in data["files"]:
    regions[rel(f["filename"])] = f["summary"]["regions"]
t = data["totals"]
print(f"TOTAL lines {t['lines']['covered']}/{t['lines']['count']} ({pct(t['lines']['covered'], t['lines']['count'])})"
      f" regions {t['regions']['covered']}/{t['regions']['count']} ({pct(t['regions']['covered'], t['regions']['count'])})"
      f" branches {pct(t['branches']['covered'], t['branches']['count']) if t['branches']['count'] else 'n/a (no branch data)'}")
seen = set()
for path in sorted(files):
    if want and not any(path == w or path.startswith(w + "/") for w in want):
        continue
    seen.update(w for w in want if path == w or path.startswith(w + "/"))
    f = files[path]
    lv, lc = len(f["da"]), sum(1 for h in f["da"].values() if h > 0)
    r = regions.get(path, {"count": 0, "covered": 0})
    miss = [n for n, h in f["da"].items() if h == 0]
    under = lv and 100 * lc / lv < bar
    print(f"{path} lines {lc}/{lv} ({pct(lc, lv)}) regions {r['covered']}/{r['count']} ({pct(r['covered'], r['count'])})"
          + (f" branches {f['brh']}/{f['brf']} ({pct(f['brh'], f['brf'])})" if f["brf"] else "")
          + (f" UNDER {bar:g}% uncovered: {ranges(miss)}" if under else ""))
for w in want:
    if w not in seen:
        print(f"NOT IN REPORT {w}")
PY
```

Targets are matched by workspace-relative path (exact file, or directory prefix) — never substring, so `greet.rs`
doesn't match `regreet.rs`. Per-file line figures from lcov equal the `Lines`/`Cover` columns of `cargo llvm-cov
report` (verified: `lib.rs` 13/26 = 50.00%, `main.rs` 7/7). Line % is the gate figure (the metric every other stack's
gate uses); region % is reported alongside because it catches untested arms of a one-line `if`/`match`.

- **`NOT IN REPORT <target>`** — the file wasn't compiled into any test run (a module not declared with `mod`, a file
  behind a disabled feature, an `xtask` path the regex excluded, a bin-only crate whose `main.rs` no test executes):
  report that cause instead of 0%.
- A file listed with `lines 0/N` genuinely is 0%. A file with no instrumented lines (only declarations/re-exports)
  doesn't appear in lcov at all — `n/a`, not 0%.

Leave `target/coverage/` in place (`target/` is gitignored; CI and Sonar read `lcov.info` from there).

## Step 5 — Report results

State the runner (`cargo llvm-cov nextest` or `cargo llvm-cov`), toolchain (stable → no branch data), selection
(`--workspace`/`-p`, features, filter, ignored tests not run), what the regex excluded, and whether the tests passed.
Then, computed from the actual report numbers — never estimated:

- **Total**: line % and region % (branch "unavailable on stable"), and whether the line % meets the bar.
- **Per target** (or per file for an unscoped run with few files): line % and region %, and for every target under the
  bar its uncovered line ranges (`src/commands/greet.rs: lines 71.43%, regions 66.67% — uncovered: 41-43, 57`) so the
  user, or a follow-up coding step, knows where to add tests.

Never paste the lcov/JSON or the console table. If coverage wasn't wired, the build failed, or a target isn't in the
report, say that instead of a percentage, with the exact command and the fix. Do not add tests, modify code, edit
`Cargo.toml`/`rust-toolchain.toml`, or re-run to raise the number — that's a follow-up the user (or a coding skill)
drives explicitly.

## Verification notes

Verified on 2026-10-16 with Rust 1.99.1 (stable), cargo-llvm-cov 0.9.1 (`llvm-tools` component installed),
cargo-nextest 0.9.148, in `$TMPDIR/iru-verify/cli/rust-gates/` (outside this repository) on a workspace with a
`democli` lib + bin (`tests/cli.rs` spawning the binary through assert_cmd 2.2, one failing unit test, one ignored test,
a doctest) and an `xtask` member:

- `cargo llvm-cov nextest --workspace --locked --no-fail-fast --no-report` exited `100` (one failing test) and the
  following `report --lcov`/`--json --summary-only` calls still succeeded; the parser printed `TOTAL lines 20/33
  (60.61%) regions 33/50 (66.00%) branches n/a`, `src/lib.rs lines 13/26 (50.00%) regions 16/33 (48.48%) UNDER 80%
  uncovered: 15, 19, 23-26, 29-31, 45, 49-51` and `src/main.rs lines 7/7 (100.00%)` — matching cargo-llvm-cov's own
  text table — and `NOT IN REPORT src/nope.rs` for a missing target. `cargo llvm-cov` (cargo test runner) gave the
  same figures.
- `src/main.rs` reached 100% only through the assert_cmd-spawned binary. `--ignore-filename-regex '(^|/)xtask/'`
  removed `xtask/src/main.rs` (0/3 lines) from the totals; `tests/cli.rs` never appeared.
- A nextest substring filter after `--` (`cargo llvm-cov nextest -p democli --no-report -- greet`) ran 2 tests and
  lowered `lib.rs` to 6/26 — a narrow filter undercounts.
- `--branch` and `--doctests` on stable: warnings `requires nightly toolchain`, then `the option Z is only accepted on
  the nightly compiler`, exit `101`/`1`. `--ignore-run-fail` with `--no-fail-fast` → `may not be used together`.
- Not verified: nightly branch/MC/DC data, Windows (`.exe` binaries under `llvm-cov-target`), `cargo llvm-cov
  --profraw-only`/merging across CI jobs, and e2e tests that launch the binary from a hard-coded `target/debug` path.

## Sources

- irurueta docs: programming-languages/rust/testing-and-benchmarking.adoc (unit tests beside the code, integration tests
  in `tests/`, logic in `lib.rs` so it is testable)
- irurueta docs: programming-languages/rust/cargo-and-workspaces.adoc (workspace members, `xtask` pattern,
  `--workspace`/`-p`)
- irurueta docs: ai/cli-for-agents/testing-clis.adoc (end-to-end tests that run the real binary)
- cargo-llvm-cov README (github.com/taiki-e/cargo-llvm-cov: `nextest` subcommand, `--no-report` + `report`,
  `--lcov`/`--json`/`--summary-only`, `--ignore-filename-regex`, nightly-only `--branch`/`--doctests`)
