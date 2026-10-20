---
name: iru-setup-rust-gitignore
description: >-
  Create or update the root `.gitignore` for a Rust repository — the command-line tool layout `iru-setup-rust-cli`
  produces (`Cargo.toml` workspace with the tool package + `xtask/`, `src/`, `tests/golden/`) or any other Cargo
  crate or workspace — covering Cargo's build directory `/target/` (which also holds the xtask outputs
  `target/dist/{man,completions}`, rustdoc `target/doc/`, cargo-llvm-cov's `target/llvm-cov*` and
  `target/lcov.info`, nextest JUnit reports), coverage files written outside it (`lcov.info`, `*.profraw`,
  `*.profdata`), rustfmt backups (`**/*.rs.bk`), pending snapshot files (`*.pending-snap`, `*.snap.new`), cargo-fuzz
  output (only when `fuzz/Cargo.toml` exists), env files (keeping `.env.example`), editor/OS files, the Antora docs
  build output (`docs/build/`, `docs/node_modules/`), the repository-wide `.integration-test.lock/`, and — for a
  Ratatui terminal UI — the UI tests' capture directory `.ui-screenshots/` (never `.ui-quality.yml`). Never ignores
  `Cargo.lock` for a package with a binary target (the tool's reproducible build); for a library-only crate it asks
  (`cargo-lock: commit|ignore`, Cargo's own default being commit). Never ignores `rust-toolchain.toml`,
  `.cargo/config.toml`, `deny.toml`, golden files or the generated-but-committed
  `docs/modules/ROOT/pages/cli-reference.adoc`. Invoke as `/iru-setup-rust-gitignore`, optionally with `args`
  (`key: value` lines): `cargo-lock: commit|ignore` (pre-resolved answer for library-only crates), `mode:
  new|existing` (default: detected from whether a root `.gitignore` already exists) and `on-existing:
  ask|keep|update|replace` (default `ask`). Announces whether it is creating from scratch or updating; an existing
  `.gitignore` is never overwritten silently — it warns, shows a diff, and asks Update (merge in what's missing, keep
  hand-added lines) / Keep as is / Replace, unless `on-existing` decides. Use whenever a Rust repository (a CLI tool,
  library, or service) needs a `.gitignore` bootstrapped, or an existing one checked/gap-filled against this house
  template.
model: haiku
---

# Setup Rust Gitignore

Create or refresh the root `.gitignore` of a Rust repository. The template is short on purpose: Cargo writes almost
everything under one directory, `target/`, so the work is in not ignoring what must stay tracked (`Cargo.lock` for
binaries, toolchain and cargo-deny config, golden test files, the generated CLI reference page). Never overwrite an
existing `.gitignore` without showing the user exactly what would change and getting explicit approval first — it
can carry hand-added, project-specific entries that must not be dropped silently.

## Step 0 — Resolve inputs

Parse `args` as `key: value` lines, skipping any question already answered:

- `cargo-lock: commit|ignore` — only consulted for a library-only crate (Step 3). A package with a binary target
  always commits `Cargo.lock`; an `ignore` passed for one is reported and overridden.
- `mode: new|existing` — if omitted, detect it: a root `.gitignore` already present means `existing`; its absence
  means `new`. `mode: existing` never means "update silently" — the existing file still goes through Step 5's Update /
  Keep as is / Replace question (unless `on-existing` decides it).
- `on-existing: ask|keep|update|replace` — how Step 5 treats an existing `.gitignore`. Default `ask`.
  `keep`/`update`/`replace` applies that choice without asking (the warning and diff are still printed). Only meant
  for scripted runs; an orchestrator passes it only if its own `args` received it.

Any other key (e.g. the full shared-args set `iru-setup-cli-repository` forwards: `language`, `ui`, `bin-name`, …)
is ignored and named in the report.

## Step 1 — Survey the repository

Detect the following before composing content — each gates a Step 3 decision:

- The root `Cargo.toml` — confirms a Rust repository; if none exists (this skill running before the scaffold),
  assume `iru-setup-rust-cli`'s layout (a binary package) and say so. Otherwise run
  `cargo metadata --no-deps --format-version 1` (or read the manifests) and note whether any workspace member has a
  `bin` target (`[[bin]]`, `src/main.rs`, `src/bin/`) — the `Cargo.lock` decision.
- `fuzz/Cargo.toml` → cargo-fuzz in use.
- `docs/antora.yml` or `docs/antora-playbook.yml` → Antora (its lines are added either way when `docs/` will hold the
  site; `iru-setup-cli-repository` runs `iru-setup-antora` before this skill).
- `.env.example` → keep it tracked while ignoring `.env`.
- A tracked file under a path the template would ignore (`git ls-files -- target '*/target/*' '*.profraw'
  'lcov.info' '*.rs.bk'`) — flag each in the report: writing `.gitignore` never untracks anything.
- A tracked `Cargo.lock` that this run would ignore (library-only + `ignore`) — flag it with the `git rm --cached
  Cargo.lock` it needs.
- The root `.gitignore`, if present — read it. Flag a `Cargo.lock` line when a binary target exists (it must go), and
  a bare `*.json`, `*.adoc` or `docs/` line (it would hide golden files or the CLI reference).

Tell the user which of the two this run is doing:

- **Creating from scratch** — no root `.gitignore`: write Step 4's content without asking.
- **Updating existing** — a root `.gitignore` exists: warn up front that Step 5 will ask whether to Update, Keep as
  is, or Replace it (or apply `on-existing`) rather than overwrite anything silently.

## Step 2 — The root `.gitignore` base template

Unconditional — include it verbatim (every line flush-left; git doesn't trim leading whitespace):

```gitignore
# Cargo build output: binaries, rustdoc (target/doc), cargo-llvm-cov (target/llvm-cov*, target/lcov.info),
# nextest reports (target/nextest), and `cargo xtask docs` output (target/dist: man pages, completions)
/target/

# Coverage files written outside target/ (an lcov export, raw LLVM profiles from a misdirected LLVM_PROFILE_FILE)
lcov.info
*.profraw
*.profdata

# rustfmt backups and pending snapshot reviews (snapbox/insta); accepted golden files stay tracked
**/*.rs.bk
*.pending-snap
*.snap.new

# Environment files (never commit secrets; the example documents the shape)
.env
.env.*
!.env.example

# Antora documentation build output (see iru-setup-antora)
docs/build/
docs/node_modules/

# Editors
.idea/
*.iml
.vscode/*
!.vscode/settings.json
!.vscode/tasks.json
!.vscode/launch.json
!.vscode/extensions.json
*.swp
*~

# OS files
.DS_Store
Thumbs.db
Desktop.ini

# Repository-wide lock serializing container-backed test runs (iru-rust-test ignored: include|only)
.integration-test.lock/
```

Notes on specific lines:

- `/target/` is **anchored**: Cargo puts a workspace's single build directory at the root, `xtask` included, so an
  unanchored `target/` would only add risk (a `src/target/` module directory). A crate outside the workspace keeps
  its own `target/` — Step 3 adds `fuzz/target/` for cargo-fuzz; add others the same way when such crates exist.
- Everything `iru-setup-rust-cli`'s gates and xtask produce lands in `target/` (`target/dist/man/`,
  `target/dist/completions/`, `target/dist/cli-reference.adoc` without Antora, `target/lcov.info`, `target/doc/`),
  so no separate lines are needed; `lcov.info` and `*.profraw` catch tool runs pointed elsewhere (a root
  `lcov.info` export for Sonar, `default.profraw` from a binary run outside cargo-llvm-cov).
- `docs/modules/ROOT/pages/cli-reference.adoc` is generated by `cargo xtask docs` but **committed** — CI diffs it
  with `cargo xtask docs --check`. Nothing here may match it.
- `.integration-test.lock/` is the atomic-`mkdir` lock directory (with its owner file) the coding/test skills create
  around container-backed tests — always transient.

## Step 3 — Project-specific additions

Only add a section when Step 1 found what it targets:

- **`Cargo.lock`** — decide, never guess:
  - Any binary target (a CLI, a service — `iru-setup-rust-cli`'s layout always): **commit it** and add no line.
    The release binary must be reproducible, `cargo install --locked` and every `--locked` gate depend on it.
  - Library-only workspace: resolve `cargo-lock` from `args`, else ask with `AskUserQuestion`:
    - **Commit it (Recommended)** — "Cargo's default since 1.74 (`cargo new` no longer ignores it): CI tests the
      exact dependency set, and `--locked` gates work. Consumers ignore it either way; pair it with a CI job against
      the latest dependencies (`cargo update` then test) if you want early breakage signals." No line added.
    - **Ignore it** — "The older library convention: every CI run resolves the newest compatible versions, so CI
      sees what a new consumer gets — but builds aren't reproducible and `--locked` gates can't be used." Add:
      ```gitignore
      # Library: consumers resolve their own dependency graph
      /Cargo.lock
      ```
- **cargo-fuzz** (`fuzz/Cargo.toml` found):
  ```gitignore
  # cargo-fuzz build output, generated corpus and crash artifacts
  fuzz/target/
  fuzz/corpus/
  fuzz/artifacts/
  fuzz/coverage/
  ```
  Keep a hand-curated seed corpus tracked by moving it out of `fuzz/corpus/` (e.g. `fuzz/seeds/`) — say so if
  `git ls-files fuzz/corpus` lists files.
- **Terminal UI** (`ratatui` in any member's `Cargo.toml`, or a root `.ui-quality.yml`/`.ui-screenshots/`):
  ```gitignore
  # UI test captures (UI contract: .ui-screenshots/<kind>/<Id>/<state>--<direction>--<theme>.txt), regenerated every run
  .ui-screenshots/
  ```
  `.ui-quality.yml` (the accessibility level and capture matrix) stays **tracked**; the documentation skills copy the
  captures they use into the Antora `images/ui/` tree, which is committed.
- Don't invent entries beyond what was detected.

## Step 4 — Compose the proposed content

Step 2's base template plus the Step 3 sections that matched. If a root `.gitignore` exists, merge: keep every
existing line not already covered (hand-added ignores survive) and don't repeat a line already present verbatim —
except a `Cargo.lock`/`/Cargo.lock` line when a binary target exists, which the merge drops (named in the diff and
the report).

Before proposing, write the draft to a temp path outside the repository, then check it doesn't hide what the
scaffold commits: for each of these that exists, `git check-ignore --no-index -v -- <path>` must print nothing when
run with the draft as the active `.gitignore` (simplest: copy the draft over `.gitignore` in a scratch clone, or
`git -c core.excludesFile=<draft> check-ignore --no-index`): `Cargo.toml`, `Cargo.lock` (binary case),
`rust-toolchain.toml`, `rustfmt.toml`, `deny.toml`, `clippy.toml`, `.cargo/config.toml`, `src/main.rs`,
`src/lib.rs`, `tests/cli.rs`, `tests/golden/*.json`, `xtask/Cargo.toml`, `xtask/src/main.rs`,
`docs/modules/ROOT/pages/cli-reference.adoc`, `docs/antora.yml`, `.env.example`, `.secrets.baseline`,
`.ui-quality.yml`, `src/tui/ui_screenshots.rs`, `docs/modules/ROOT/images/ui/**`. Refuse any line that matches one of
them.

## Step 5 — If a `.gitignore` already existed, warn and ask Update / Keep as is / Replace

Skip when Step 1 found no root `.gitignore` — write it straight away.

Otherwise, if the proposed content differs from disk:

- Show the proposed **Update** content as a diff (`git diff --no-index <current> <draft>`). Say which hand-added
  lines a **Replace** would drop, and name any conflicting existing line (e.g. `Cargo.lock` for a binary, a bare
  `*.json` hiding `tests/golden/`, `docs/` hiding the Antora sources and the CLI reference, an unanchored `target`
  matching a source directory).
- Unless `on-existing` is `keep`/`update`/`replace` (apply it, still printing the warning and diff), ask via
  `AskUserQuestion`, with the consequence in each option:
  - **Update (Recommended)** — "Merge: add the template lines this file is missing; keep every hand-added line
    (except a `Cargo.lock` ignore for a binary, which is removed). Your customizations survive."
  - **Keep as is** — "Leave the file untouched. Nothing you customized changes, but the missing lines in the diff
    (e.g. `/target/`, `*.profraw`, `.integration-test.lock/`) stay unignored — the report lists them."
  - **Replace** — "Overwrite with this skill's template only. Matches the house pattern exactly, but every
    hand-added line is lost (recoverable only from git history)."
  If the user wants only some lines, let them say so in free text and revise the draft.

## Step 6 — Write and report

Write the composed content to `.gitignore` (on Update or Replace, or when none existed). Then summarize:

- Whether this run created from scratch or updated an existing file, the action taken — **created / updated /
  replaced / kept as is** — and whether it came from the user or `on-existing`; when kept as is, the template lines
  it still lacks; when replaced, the hand-added lines dropped.
- The `Cargo.lock` decision: binary target found (committed, not asked) or library-only (from `args`, asked, or
  defaulted to commit), with the reasoning restated.
- Which Step 3 sections were included vs. skipped and why (e.g. "no cargo-fuzz section — no `fuzz/Cargo.toml`",
  "terminal-UI section — `ratatui` is a dependency").
- The result of Step 4's safety check (every listed file still tracked).
- Any already-tracked file under a newly ignored path (Step 1), with the `git rm -r --cached <path>` it needs.

**Warn explicitly**:

- Review the generated/updated `.gitignore` before committing — detection is heuristic.
- Writing `.gitignore` never untracks a file already committed (a `target/` directory, a `.env`): run
  `git rm -r --cached <path>` for each, and rotate any secret that was ever committed.
- Keep `Cargo.lock` committed for any crate that ships a binary; regenerate the CLI reference with
  `cargo xtask docs` rather than ignoring it.

## Verification notes

Verified on 2026-10-16 in `$TMPDIR/iru-verify/cli/iru-setup-rust-gitignore/` (outside this repository): a copy of an
`iru-setup-rust-cli` scaffold (`ui: tui`, after a real `cargo build`, `cargo nextest`, `cargo llvm-cov` with
`--lcov --output-path target/lcov.info`, `cargo doc`, `cargo xtask docs` into `docs/modules/ROOT/pages/` and a
release build) was `git init`-ed with the base template + the cargo-fuzz section, seeded with one extra file per
remaining pattern, and checked with `git check-ignore -v` and `git status --porcelain --ignored`:

| Path | Expected | Result |
|---|---|---|
| `target/release/<bin>`, `target/dist/man/<bin>.1`, `target/dist/completions/_<bin>`, `target/doc/index.html`, `target/lcov.info`, `target/llvm-cov-target/…`, `target/nextest/…` | ignored | ignored — `/target/` |
| `lcov.info`, `default.profraw`, `merged.profdata`, `src/lib.rs.bk`, `tests/golden/x.pending-snap`, `x.snap.new` | ignored | ignored |
| `.env`, `.env.local` | ignored | ignored |
| `.env.example`, `.vscode/settings.json` | **tracked** | **not ignored** (negations) |
| `docs/build/site/index.html`, `docs/node_modules/x`, `.integration-test.lock/owner`, `.DS_Store`, `.idea/x` | ignored | ignored |
| `fuzz/target/x`, `fuzz/corpus/x`, `fuzz/artifacts/x` | ignored | ignored |
| `Cargo.toml`, `Cargo.lock`, `rust-toolchain.toml`, `rustfmt.toml`, `deny.toml`, `.cargo/config.toml`, `src/**`, `tests/cli.rs`, `tests/golden/greet-ada.json`, `tests/golden/schema.json`, `xtask/**`, `docs/modules/ROOT/pages/cli-reference.adoc`, `src/target/mod.rs`, `fuzz/Cargo.toml` | **tracked** | **not ignored** — `git add -A` staged only these, nothing under `target/` |
| Terminal-UI section (added for the UI contract; checked with git 2.x in a scratch repository): `.ui-screenshots/screen/App/default--ltr--no-color.txt` | ignored | ignored; `.ui-quality.yml`, `src/tui/ui_screenshots.rs`, `docs/modules/ROOT/images/ui/screen/App/default--ltr--no-color.txt` not ignored |
| Library variant with `/Cargo.lock` | `Cargo.lock` ignored, `xtask/Cargo.lock`-style nested files untouched | as expected (anchored) |

## Sources

- The Cargo Book: "Cargo.toml vs Cargo.lock" and the 2023 change of guidance (commit `Cargo.lock` by default, also
  for libraries — https://blog.rust-lang.org/2023/08/29/committing-lockfiles.html); `cargo new` output
- GitHub's `Rust.gitignore` (https://github.com/github/gitignore/blob/main/Rust.gitignore) — `target/`, `**/*.rs.bk`,
  `*.pdb`-style debug files are covered by `/target/` here
- cargo-llvm-cov, cargo-nextest and cargo-fuzz output locations; snapbox/insta pending-snapshot files
- irurueta docs: `programming-languages/rust/cargo-and-workspaces.adoc`, `ai/cli-for-agents/documenting-clis.adoc`
  (generated docs committed)
- This catalog: `iru-setup-rust-cli` (layout), `iru-setup-windows-gitignore` / `iru-setup-swift-gitignore`
  (structure, the `Package.resolved` decision this `Cargo.lock` decision mirrors)
