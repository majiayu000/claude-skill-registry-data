---
name: project-gate-setup
description: "Use when a project needs its landing-gate configuration established or updated - the canonical config at .thrum/gate-config.json naming the per-landing test, race and lint commands, the focused-versus-full rule, how to build the merged tree, the structural checks, the verdict log and the evidence retention the gate role follows. Detects Go, Node/TypeScript, Python and Rust from the repo, asks when unsure, and writes the file the gate role reads at gate time. Triggers - set up the gate, configure the gate role, gate config, what does the gate run, gate-config.json is missing, GATE CONFIG ABSENT."
---

# Project Gate Setup

## Canonical path

`.thrum/gate-config.json` — the single authoritative location. The gate role reads it at gate time. Its preamble names
no project command; every command comes from this file. A field left out means the gate falls back to asking, never to
guessing.

## Run modes and dispatch order

On every invocation, dispatch in this order. Earlier branches short-circuit later ones.

1. **First-run** (config absent) — generate `.thrum/gate-config.json` from repo inspection and the answers below.
2. **Re-run-unchanged** (config present and matches the repo) — report "gate-config.json is current; no changes needed"
   and exit without writing.
3. **Re-run-evolved** (config present, repo has drifted) — compute a sectional diff, present it, write only on approval.

Load the /thrum:generator-idempotency-protocol skill and follow it.

> **Human in the loop.** The candidates below are proposals. The user confirms every command before it is written.

## First-run mode

### Step 1: Census the languages

Detect every language present; a repo can carry several. Record them as `languages_detected`.

- Manifest files at the repo root or in each workspace: `go.mod`, `package.json`,
  `pyproject.toml` / `requirements*.txt` / `setup.py` / `tox.ini`, `Cargo.toml`.
- `git ls-files` extension histogram as a cross-check, and as the only signal where a subtree has no manifest.
- A language counts when it has a manifest or clears 5% of tracked files. A polyglot repo gets a command set per language.

### Step 2: Read the project's own commands first

The project's own definition of "passing" outranks any default below. Read, in this order, and treat what you find as
ground truth:

1. CI workflow `run:` steps (`.github/workflows/*`, `.gitlab-ci.yml`, `Jenkinsfile`, `.circleci/config.yml`).
2. `Makefile` / `justfile` targets named `test`, `check`, `ci`, `lint`, `verify`.
3. `package.json` `scripts` (`test`, `lint`, `typecheck`, `build`); the lockfile picks the package manager
   (`pnpm-lock.yaml`, `yarn.lock`, `package-lock.json`, `bun.lockb`). For workspaces, enumerate the packages.
4. `README` / `CONTRIBUTING` test instructions.

### Step 3: Propose commands per language

Defaults apply only where Step 2 found nothing. Each is a candidate the user confirms.

| Signal | Build / test candidates | Zero-match control |
|---|---|---|
| `go.mod` | `go build ./...`, `go vet ./...`, `go test ./...`; a race lane `go test -race ./...` when CI runs one; `golangci-lint run` only if a `.golangci.*` file exists | `go test -list '<selector>' ./pkg` plus a selector that must list nothing |
| `package.json` | the repo's own `test`, `lint`, `typecheck`, `build` scripts via the detected package manager | the runner's list mode (`--listTests`, `--list`) plus a selector that matches nothing |
| `pyproject.toml` etc. | `pytest` when configured; `ruff` / `mypy` only when configured | `pytest --collect-only -q <selector>` plus an impossible selector |
| `Cargo.toml` | `cargo build`, `cargo test`, `cargo clippy -- -D warnings`, `cargo fmt --check` | `cargo test <filter> -- --list` plus an impossible filter |

### Step 4: Ask what detection could not settle

Ask only what is still open. Never pick silently between several plausible commands.

- Which command is the required per-landing test, and is there a separate race or sanitizer lane with its own time bound?
- Is any package or suite too large to run as one monolith (record it under `never_monolithic` with the route to use)?
- Which files are generated, and what regenerates each? Which baseline or ratchet files may the gate refresh for an
  already-reviewed pattern?
- Which targets write to source (formatters, `--fix` linters, code generators)? Scan Makefile targets and package scripts
  for `fmt`, `format`, `--fix`, `lint-fix` and propose them for `write_capable_targets`.
- Which structural checks must pass for a change to be mergeable (generated-file drift, dependency or license checks,
  schema checks)?
- Where does the one-line verdict record go? Offer `docs/gate-log.md` as the default.
- Which directories hold gate output that is deleted once the verdict is decided? Default: nothing is kept.
- Do any tests share fixed-name resources (ports, sockets, fixtures) that forbid parallel runs?

### Step 5: Write `.thrum/gate-config.json`

Fields (all optional; omit rather than leave empty):

| Field | Meaning |
|---|---|
| `languages_detected` | the Step 1 record |
| `build_merged_tree` | how to build the merged tree the gate judges: fetch, merge into a scratch worktree, build |
| `per_landing` | ordered `{name, cmd, kind}` list every landing runs (`kind`: build, test, race, lint) |
| `full_fallback` | what to run when test selection errors or cannot run |
| `focused_vs_full` | the rule: a selector run only localizes a failure; the verdict rests on the whole-lane run |
| `zero_match_check` | how to prove a selector ran something, with the control that must find nothing |
| `structural_checks` | `{name, cmd, why}` checks beyond tests |
| `generated_files` | `{pattern, regen_cmd}` the gate may regenerate as a bookkeeping commit |
| `baselines` | ratchet or baseline files the gate may refresh for an already-reviewed pattern |
| `write_capable_targets` | commands never to run on a tree anyone cares about |
| `never_monolithic` | packages or suites that must go through a sharded route |
| `shared_resources` | fixed-name resources that forbid parallel execution |
| `verdict_log` | the one committed record per gate |
| `retention_paths` | gate output deleted after the verdict |

Examples per language are in `references/gate-config.go.json`, `gate-config.node.json`, `gate-config.python.json` and
`gate-config.rust.json`. Start from the one that matches, then replace every value with what Steps 2 to 4 settled.

Ensure the file is not gitignored: add `!/.thrum/gate-config.json` beside the existing `.thrum/` exceptions in
`.gitignore` when the repo ignores `.thrum/*`.

Announce the path, summarize what was detected per language and which answers came from the user, then tell the user the
gate preamble picks the file up with no further step (its text only points at the file).

If Step 2 and Step 3 found no test command for a detected language, write no command for it, say so, and leave the
field out. The gate then reports that lane as `NOT RUN`.

## Re-run-unchanged mode

Triggered when `.thrum/gate-config.json` exists. Read it in full, re-run Steps 1 to 3 comparing instead of writing, and
check each command still exists (script name, make target, CI step). If nothing differs, print
`.thrum/gate-config.json is current; no changes needed` and stop. If anything differs, continue in evolved mode.

## Re-run-evolved mode

> **Never silently overwrite.** The file may hold answers only the user knew. A write without confirmation is a bug.

Drift categories: a language appearing or disappearing; a command whose script, target or CI step changed or vanished;
a new write-capable target; a new generated file or baseline; a changed verdict-log location.

Present each drift as a plain-language change, the proposed edit, and a one-line reason. On approval apply the edits in
place, preserving the rest. On decline write nothing and record the skipped proposal for the next run.

## Reference

- `.thrum/gate-config.json` — the file this skill generates
- `references/` — one example per language
- `project-hotpath-gate` and `project-philosophy` — sibling generators for the hot-path lenses and the philosophy doc
- the gate role preamble — reads this file at gate time and falls back to `GATE CONFIG ABSENT` when it is missing
