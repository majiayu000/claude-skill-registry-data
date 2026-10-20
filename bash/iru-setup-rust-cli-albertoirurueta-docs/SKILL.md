---
name: iru-setup-rust-cli
description: >-
  Scaffold an agent-friendly Rust command-line tool at the repository root — a Cargo workspace (`Cargo.toml` with the
  tool package, version `0.1.0-dev`, edition 2024, `rust-version` = the MSRV computed from the dependency graph, an
  explicit `[[bin]]`, `[workspace.lints]` with `missing_docs`, `unsafe_code = "forbid"`, Clippy `pedantic` plus
  `print_stdout`/`print_stderr`/`dbg_macro`, and a release profile with fat LTO, `codegen-units = 1`, stripped symbols
  and `panic = "unwind"` kept on purpose; `Cargo.lock` committed), `rust-toolchain.toml` (stable + rustfmt, clippy,
  llvm-tools), `rustfmt.toml`, `deny.toml` (cargo-deny advisories/licenses/bans/sources), `.cargo/config.toml` (the
  `cargo xtask` alias), a thin `src/main.rs` and a library holding all logic — clap 4 derive tree with the global
  flags `--format text|json|jsonl`/`--json`/`--no-color`/`--no-input`/`-q`/`-v`/`--log-format`/`--config`
  (`<BIN>_FORMAT`/`<BIN>_NO_INPUT`/`<BIN>_CONFIG` through clap's `env`), the exit-code enum 0–7/130/143 in one file,
  a `thiserror` error with the JSON error envelope on stderr, sorted-key compact JSON and a `jsonl` summary line,
  colour per stream (TTY, `NO_COLOR`, `TERM=dumb`, `FORCE_COLOR`, `--no-color`, machine mode), prompts only on a
  terminal and never under `--no-input`/`<BIN>_NO_INPUT`/`CI`, flags → env → TOML config file → defaults,
  SIGINT/SIGTERM → 130/143 (immediate when nothing needs cleanup, deferred with a guard otherwise), broken pipe as a
  quiet exit 0, a panic as exit 1 — and the commands `greet [NAME] [--ask]`, `completion <shell>`, `schema [COMMAND]`
  (clap's `Command` walked into JSON with per-command exit codes and safety metadata), `version` and `--version`;
  with `ui: tui` a Ratatui `browse` picker (TTY-gated → exit 2 with a pointer to `greet --json`, terminal restored on
  panic and on SIGTERM, state and drawing unit-tested with `TestBackend`, the list rendering only the rows that fit,
  and — per the catalog's UI contract — a `.ui-quality.yml` at the repository root, a test-only
  `src/tui/ui_screenshots.rs` helper and UI tests capturing every picker state in each direction as
  `.ui-screenshots/screen/App/<state>--<direction>--no-color.txt` with the asserted accessibility checks). Tests: in-process tests of `run` with
  injected terminal facts and environment, assert_cmd + predicates + snapbox golden-file end-to-end tests of the
  real binary, ~98% line coverage measured with cargo-llvm-cov (80% bar). An `xtask` member generates man pages
  (clap_mangen), completions (clap_complete) and `docs/modules/ROOT/pages/cli-reference.adoc` (only when the Antora
  module exists; `--check` for CI). Invoke as `/iru-setup-rust-cli`. Accepts pre-resolved inputs via `args`
  (`key: value` lines) — `bin-name`, `crate-name`, `description`, `ui` (`none`/`tui`), `msrv`, `branching`
  (`gitflow`/`main-only`), `license`, `developer-name`, `developer-email`, `organization-url`, `owner`,
  `repository-url`, `accessibility` (`enforce`/`report`/`off`, `ui: tui` only), `open-source`, `visibility`, `ci`, `sonar` (+ `sonar-organization`/`sonar-project-key`/
  `sonar-host-url`), `distribution` (`none`/`internal`/`store`), `mode` (`new`/`existing`) and `on-existing`
  (`ask`/`keep`/`update`/`replace`) — so `iru-setup-cli-repository` can drive it without re-prompting. Announces
  whether it is scaffolding from scratch or updating; for every file group it owns that already exists it warns and
  asks Update / Keep as is / Replace / Stop (unless `on-existing` decides), never overwrites hand-written source, and
  treats a foreign Cargo layout as foreign. Every crate version is looked up live on crates.io with a verified
  2026-10-16 fallback table. Ends by running the contract's gates (fmt, clippy `-D warnings`, nextest, doctests,
  rustdoc `-D warnings`, cargo-deny, cargo-llvm-cov, `cargo xtask docs`, an MSRV check) and smoke checks of the
  release binary on pipes and on a pseudo-terminal.
model: sonnet
allowed-tools: Read Write Edit AskUserQuestion Bash(cargo *) Bash(rustup *) Bash(rustc *) Bash(curl *) Bash(git *) Bash(gh repo view *) Bash(python3 *) Bash(jq *) Bash(bash *) Bash(mkdir *) Bash(mktemp *) Bash(ls *) Bash(find *) Bash(grep *) Bash(cat *) Bash(test *) Bash(command -v *) Bash(date *) Agent
---

# Setup Rust CLI

Generate a complete, buildable, agent-friendly Rust command-line tool: a Cargo workspace whose library holds every
behaviour of the catalog's CLI contract behind a thin `main.rs`, a small set of sample commands that are each
tested, an optional Ratatui terminal UI, quality configuration with warnings-as-errors in CI, and an `xtask` that
generates the man pages, shell completions and the Antora CLI reference from the same command tree. Every template
in `reference/` was rendered into throwaway projects and proven against the real toolchain on 2026-10-16 (Rust
1.99.1, cargo-nextest 0.9.148, cargo-llvm-cov 0.9.1, cargo-deny 0.20.2; MSRV toolchains 1.85.0 and 1.88.0) for
`ui: none` and `ui: tui` — see **Verification notes**.

The layout is the **scaffold contract** the Rust coding and gate skills (`iru-rust-code-one-task(-group)`,
`iru-rust-test`, `iru-rust-coverage`, `iru-rust-code-quality`, `iru-rust-rustdoc`, `iru-rust-bump-version`) and
`iru-setup-cli-github-workflows` detect and call — Step 8's contract table lists the confirmed commands and paths.
This skill writes no CI workflow, `.gitignore`, README, changelog, `LICENSE` or Antora file other than the
generated `cli-reference.adoc` (`iru-setup-cli-repository` chains `iru-setup-antora`, `iru-setup-rust-gitignore`,
`iru-setup-cli-github-workflows`, `iru-setup-changelog` and `iru-setup-readme`), and no Sonar file (the workflows
skill passes the Sonar keys on the scanner's command line).

The behaviour it implements is `cli-contract.md` (streams, exit codes, TTY/colour/prompts, machine-readable output,
safety, configuration, self-description, startup) — the same contract the Go, Swift and .NET CLI scaffolds embed.

## Reference files — read only what this run needs

| Read | When |
|---|---|
| `reference/cargo-templates.md` | **Always.** `Cargo.toml`, `rust-toolchain.toml`, `rustfmt.toml`, `deny.toml`, `.cargo/config.toml`, `xtask/Cargo.toml`. |
| `reference/source-templates.md` | **Always.** `src/main.rs`, `src/lib.rs`, `src/cli.rs`, `src/exit.rs`, `src/error.rs`, `src/output.rs`, `src/term.rs`, `src/config.rs`, `src/signals.rs`, `src/commands/{mod,greet,completion,schema,version}.rs`. |
| `reference/test-templates.md` | **Always.** `src/tests.rs` (in-process), `tests/cli.rs` (end-to-end), `tests/golden/greet-ada.json`. |
| `reference/xtask-templates.md` | **Always.** `xtask/src/main.rs`. |
| `reference/tui-templates.md` | `ui: tui` only. `src/commands/browse.rs`, `src/tui/{mod,app,ui,ui_screenshots}.rs`, `.ui-quality.yml`. |
| `reference/smoke-checks.md` | Step 7 — the pipe/exit-code script and the pseudo-terminal script (extracted outside the repository). |

**Conditional-marker convention used in every reference file**: a line `// >>> <condition>` (Rust) or
`# >>> <condition>` (TOML) opens a block that is written only when the condition holds, and the matching `<<<` line
closes it; the marker lines themselves are never written. Conditions: `ui: tui`, `license` (a license was chosen),
`no-license` (proprietary: `publish = false` instead), `repository` (a repository URL is known). A file heading
suffixed `(ui: tui)` exists only for `ui: tui`. **Placeholders** are written `__Token__` and come from Step 5's
table; they never collide with Rust syntax. Templates hold a `4`-backtick fence when the file itself contains
triple backticks (doc-test examples) — copy the content between the fences exactly.

## Step 0 — Resolve inputs

Invoked stand-alone (`/iru-setup-rust-cli`) or by `iru-setup-cli-repository` / the `iru-setup-repository` front
door, which pass resolved answers as `key: value` lines, e.g.:

```
bin-name: shelfctl
crate-name: shelfctl
description: Manage a book shelf from the command line.
ui: tui
branching: gitflow
license: MIT OR Apache-2.0
developer-name: Jane Doe
developer-email: jane@example.com
organization-url: https://github.com/example-org
owner: example-org
open-source: yes
visibility: public
ci: yes
sonar: none
distribution: store
mode: new
on-existing: ask
```

Recognized keys:

- **Identity**: `bin-name` (the executable name, `^[a-z][a-z0-9-]*$`, ≤ 40 characters — also the clap command
  name, the man page and completion file names, and, upper-cased with `-` → `_`, the environment prefix `<BIN>_`);
  `crate-name` (the Cargo package name — and crates.io name — default `bin-name`; must match
  `^[a-z][a-z0-9_-]*$` and must not be a name already taken on crates.io when `distribution: store` publishes there:
  check `curl -s -o /dev/null -w '%{http_code}' https://crates.io/api/v1/crates/<crate-name>` (`404` = free) and say
  so if taken); `description` (one sentence ending in a period, no `"`, no backslash — it becomes
  `[package].description`, the crate doc's first line and the `--help` about text); `license` (an SPDX expression —
  `MIT OR Apache-2.0` is the Rust ecosystem default, `MIT`, `Apache-2.0`, …; "No license (proprietary)" → the
  `no-license` condition: no `license` key, `publish = false`); `developer-name`, `developer-email` (→ `authors`);
  `organization-url`, `owner`, `repository-url` (→ `repository`; default `https://github.com/<owner>/<repo>` from
  Step 3).
- **Shape (this skill)**: `ui` (`none`/`tui`, default `none`); `accessibility` (`enforce`/`report`/`off`, default
  `enforce`; only used with `ui: tui` — the level written to `.ui-quality.yml`, which the TUI's UI tests read); `msrv` (the minimum supported Rust version written
  to `rust-version`; default computed in Step 4 — never lower than what Step 4 computes); `branching`
  (`gitflow` → version `0.1.0-dev`, `main-only` → `0.1.0`; default `gitflow`).
- **Shared pipeline vocabulary**: `open-source` (`yes`/`no`), `visibility` (`public`/`private`/`internal`), `ci`
  (`yes`/`no`), `sonar` (`cloud`/`self-hosted`/`none`) + `sonar-organization`/`sonar-project-key`/`sonar-host-url`
  (recorded for the report only — no file carries them), `distribution` (`none`/`internal`/`store` — recorded; only
  `store` with the `crates-io` channel makes a free crate name matter), `mode` (`new`/`existing`), `on-existing`
  (`ask`/`keep`/`update`/`replace`, default `ask`).

Every key found is resolved — skip its question in Step 2. Unknown keys from a full shared-args set (`language`,
`ci-tests`, `pages`, `cross-os-ci`, `channels`, `integration-branch`, `stable-branch`, `publish`, …) are ignored
and named in the report. `mode: existing` never means "update silently": Step 1 still warns about, and asks about,
every pre-existing file group. Only `on-existing` skips that question (`keep` = create only missing files;
`update`/`replace` applied to every existing group; the warning is still printed). Orchestrators forward
`on-existing` only when their own `args` received it.

## Step 1 — Survey the repository

Check for every file Step 6 would write: `Cargo.toml`, `Cargo.lock`, `rust-toolchain.toml`/`rust-toolchain`,
`rustfmt.toml`/`.rustfmt.toml`, `clippy.toml`/`.clippy.toml`, `deny.toml`, `.cargo/config.toml`, `src/**`,
`tests/**`, `xtask/**`, and (`ui: tui`) `.ui-quality.yml`. If `mode` wasn't supplied, derive it: a root `Cargo.toml` ⇒ `existing`, else `new`. Then
tell the user which of the three this run is doing:

- **Scaffolding from scratch** — none exist: "Scaffolding the Rust CLI **from scratch**." Go to Step 2. Other
  repository files (`docs/`, `.github/`, `README.md`, `LICENSE`, `CLAUDE.md`) are fine.
- **Updating an existing Rust CLI in this layout** — a root `Cargo.toml` whose package has `src/lib.rs` +
  `src/main.rs`, a `clap` dependency, and (ideally) `src/exit.rs`/`xtask/`: warn, listing every file found by path,
  that each existing file group below will be decided individually (missing files are still created). Read the
  current package name, `[[bin]]` name, description, version, `rust-version`, license, authors, repository and
  whether `ratatui` is a dependency (→ `ui`), and offer them as Step 2's defaults. Groups (only those with a file
  present): **Cargo manifest** (`Cargo.toml`, `Cargo.lock`), **toolchain and quality config**
  (`rust-toolchain.toml`, `rustfmt.toml`, `deny.toml`, any `clippy.toml`), **`.cargo/config.toml`**, **the source
  skeleton** (`src/**`), **tests** (`src/tests.rs`, `tests/**`), **`xtask/`**, and — `ui: tui` only — **UI quality
  config** (`.ui-quality.yml`; Update keeps its `directions`/`themes` and any `accessibility` value unless `args` set
  one, adding missing keys; Keep as is reports a level that differs from this run's; Replace rewrites it from the
  template). Unless `on-existing` decides, ask
  with `AskUserQuestion`, one question per group (batch up to 4 per call), naming each concrete conflict with this
  run's choices (e.g. "`Cargo.toml` has no `[workspace]` — `cargo xtask` needs the `xtask` member", "`[lints]` sets
  no `missing_docs`", "`rust-version` is 1.80 but ratatui 0.30 needs 1.88", "`edition = "2021"` — the templates use
  2024 syntax (let-chains, `unsafe_code` defaults)", "`ratatui` is a dependency but you chose `ui: none`"):
  - **Update (Recommended for the manifest, toolchain/quality config and `.cargo/config.toml`)** — "Merge: add what's
    missing (dependencies at Step 4's versions, `[workspace] members = ["xtask"]`, `[workspace.lints]`, the release
    profile, the alias, the cargo-deny sections) and correct the values this skill owns (`rust-version` raised to the
    computed MSRV, lint levels), keeping every dependency, feature, profile and setting this skill doesn't own. You
    review a diff; customizations survive, but a customized part this skill owns may be rewritten." Never touch an
    existing `version` (`iru-rust-bump-version` owns it). For the source skeleton, tests and `xtask/`, Update only
    creates their missing files.
  - **Keep as is (Recommended for the source skeleton, tests and `xtask/`)** — "Leave the file(s) untouched. Nothing
    you customized changes, but they may stay out of date or disagree with this run's choices — the report lists
    each mismatch."
  - **Replace** — "Regenerate from this skill's template. Matches the house pattern exactly, but every customization
    is lost (recoverable only from git history)." Never the default. Even on Replace, never overwrite a `*.rs` file
    unless its content exactly matches this skill's rendered template (i.e. it is still the untouched sample).
  - **Stop** (first question only) — "End this skill now without changing any file." Report and end.

  Ask about groups whose expected content depends on Step 2 answers (`ui`, license) after Step 2 when `args` didn't
  already resolve them. Never add the `greet` sample to an existing tool that already has its own commands unless the
  user asks — on the update path ask once "Add the sample `greet` command as a reference?" (default **No**); the
  contract modules (`exit.rs`, `error.rs`, `output.rs`, `term.rs`, `signals.rs`, `config.rs`) are still offered
  as missing files.
- **A foreign layout** — a `Cargo.toml` with only `src/main.rs` holding the logic, a workspace whose members are
  other crates (a library, a service), a non-clap parser (`argh`, `pico-args`, `bpaf`, `lexopt`), or a
  `Cargo.toml` that is a virtual manifest: this is not this skill's scaffold. Warn explicitly and ask
  (`AskUserQuestion`) whether to add this skill's missing pieces alongside without touching existing code (only the
  toolchain/quality config, `deny.toml`, `.cargo/config.toml` and the lint/profile sections of the manifest — each
  still per-group Update/Keep/Replace; moving logic into a library or migrating the parser is a coding task, never
  done here), or stop. Never move, rename or convert existing crates.

## Step 2 — Collect the required inputs

For anything Step 0 didn't resolve, ask directly (plain conversation, pre-filled from Step 1 when updating):
**bin-name** (default: the repository directory's basename, lowercased, non-`[a-z0-9-]` dropped), **crate-name**
(default `bin-name`; confirm in one line), **description**, developer name/email/organization URL.

Then, with `AskUserQuestion` (skip any resolved):

- **ui** — **No terminal UI (Recommended)** (`none`: every command is a plain command; styled, TTY-aware output is
  still there) / **Ratatui terminal UI** (`tui`: adds `browse`, a full-screen picker for people; agents and scripts
  keep using `greet --json`; adds ratatui + crossterm and raises the MSRV to 1.88).
- **accessibility** — only with `ui: tui` and stand-alone (an orchestrator resolves it): "Automated accessibility
  checks in UI tests?" — **Enforce (Recommended)** (violations fail the UI tests) / **Report only** (listed, never
  failing) / **Off** (not run). For a terminal UI these are the asserted checks (selection visible without colour,
  key help on screen), not an automated audit.
- **license** — **MIT OR Apache-2.0 (Recommended)** "the Rust ecosystem's dual license" / **MIT** / **Apache-2.0** /
  **No license (proprietary)** (`publish = false`) / **Other** (ask the SPDX expression). If one is chosen, remind in
  Step 8 to add the `LICENSE` file(s) (`iru-check-license` can backfill headers).
- **branching** — stand-alone only: **gitflow (Recommended)** (`0.1.0-dev` on `develop`) / **main-only** (`0.1.0`).
- **open-source**, **sonar** and **distribution** — stand-alone only (an orchestrator resolves them): ask
  `open-source` first; resolve `visibility` (`gh repo view --json visibility -q .visibility`, lowercased; else ask —
  `internal` counts as private; flag open source + private as contradictory); recommend `sonar: cloud` only when
  open source and public (SonarCloud is free only for public/open-source projects), otherwise `none`; with
  `ci: no`, recommend `none`. Say this skill writes no Sonar file. `distribution` default: `store` when open source,
  otherwise `internal`; it is recorded for the report (and triggers Step 0's crate-name availability check).

## Step 3 — Infer repository information

Parse `git remote get-url origin` (`git@host:owner/repo.git` or `https://host/owner/repo.git`) for `<owner>` and
`<repo>` (the `repository-url` default `https://github.com/<owner>/<repo>` on GitHub). No `origin` and no
`repository-url` → drop the `repository` condition and say so; never invent a URL.

## Step 4 — Toolchain and versions

1. **Toolchain**: `command -v cargo rustup` and `rustc --version`. Missing → tell the user to install Rust with
   rustup (<https://rustup.rs>) and stop; never install a toolchain system-wide yourself. `rust-toolchain.toml` pins
   the `stable` channel, so the first cargo command downloads it if needed (say so — a few hundred MB).
2. **Gate tools** (needed only for Step 7): `cargo nextest --version`, `cargo llvm-cov --version`,
   `cargo deny --version`. Each missing one → offer `cargo install --locked <cargo-nextest|cargo-llvm-cov|cargo-deny>`
   (asking first — it builds from source and takes minutes), or run Step 7 without it and report that gate
   "unverified (tool not installed)". `cargo llvm-cov` also needs `rustup component add llvm-tools-preview`
   (the toolchain file lists it).
3. **Crate versions** — look each up live: `curl -fsSL -A 'iru-setup-rust-cli' https://crates.io/api/v1/crates/<crate>`
   → `.crate.max_stable_version` (crates.io requires a User-Agent). Adopt a newer version only within the same
   SemVer-compatible line as the fallback (same major, or same minor for `0.x`: clap 4.x, ratatui 0.30.x,
   clap_mangen 0.3.x, signal-hook 0.4.x, toml 1.x, snapbox 1.x); a new incompatible line (ratatui 0.31, clap 5,
   toml 2) is reported as drift and left for a deliberate follow-up, because the templates were verified against the
   fallback line. When a lookup fails, use the fallback and say so in Step 8. After adopting newer versions, Step 7
   must pass before trusting them.

   | Crate | Role | 2026-10-16 fallback |
   |---|---|---|
   | `clap` (features `derive`, `env`, `wrap_help`) | parser, help, `env` layer | `4.6.7` |
   | `clap_complete` | `completion` command, xtask completions | `4.6.11` |
   | `clap_mangen` (xtask only) | man pages | `0.3.3` |
   | `anstyle` | ANSI styles (clap's own styling crate) | `1.0.14` |
   | `serde` (feature `derive`) / `serde_json` | JSON output, config | `1.0.229` / `1.0.154` |
   | `thiserror` | error type | `2.0.21` |
   | `toml` | config file | `1.1.8` |
   | `signal-hook` | SIGINT/SIGTERM | `0.4.5` |
   | `ratatui` (`default-features = false`, feature `crossterm`; `ui: tui`) | terminal UI (crossterm re-exported as `ratatui::crossterm`) | `0.30.2` |
   | `assert_cmd` / `predicates` / `snapbox` / `tempfile` (dev) | end-to-end tests, golden files | `2.2.2` / `3.1.4` / `1.2.2` / `3.27.0` |

4. **MSRV** (`rust-version`) — unless `msrv` was given (and is not lower): the maximum of the edition-2024 floor
   `1.85`, `1.88` for `ui: tui` (the TUI template uses let-chains, and ratatui 0.30 declares 1.88), and every chosen
   direct dependency's declared `rust_version` (`https://crates.io/api/v1/crates/<crate>/<version>` →
   `.version.rust_version`). After Step 6 resolves `Cargo.lock`, recompute it over the whole graph and raise
   `rust-version` if a transitive crate needs more:
   ```bash
   cargo metadata --format-version 1 --locked | python3 -c 'import json,sys; print(max((tuple(map(int,p["rust_version"].split("."))) for p in json.load(sys.stdin)["packages"] if p.get("rust_version") and p["source"]), default=(1,85)))'
   ```
   Verified on 2026-10-16: `1.85` for `ui: none`, `1.88` for `ui: tui`.

## Step 5 — Reference templates

Read the reference files this run needs (table above). Placeholders:

| Placeholder | Source |
|---|---|
| `__package__` | `crate-name` (Cargo package name, also the xtask's path dependency) |
| `__bin__` | `bin-name` |
| `__crate__` | `crate-name` with `-` → `_` (the library's Rust path, e.g. `shelfctl::main()`) |
| `__BIN_ENV__` | `bin-name` upper-cased, `-` → `_` (`SHELFCTL` → `SHELFCTL_FORMAT`, `SHELFCTL_NO_INPUT`, `SHELFCTL_CONFIG`) |
| `__Description__` | `description` |
| `__Version__` | `0.1.0-dev` (gitflow) / `0.1.0` (main-only) |
| `__Msrv__` | Step 4 (e.g. `1.88`) — in `Cargo.toml` and `xtask/Cargo.toml` |
| `__License__` | the SPDX expression (`license` condition) |
| `__Accessibility__` | `accessibility` (`enforce` by default; `ui: tui` only) |
| `__Authors__` | `Name <email>` (or `Name` without an email) |
| `__RepositoryUrl__` | Step 3 (`repository` condition) |
| `__ClapVersion__`, `__ClapCompleteVersion__`, `__ClapMangenVersion__`, `__AnstyleVersion__`, `__SerdeVersion__`, `__SerdeJsonVersion__`, `__ThiserrorVersion__`, `__TomlVersion__`, `__SignalHookVersion__`, `__RatatuiVersion__`, `__AssertCmdVersion__`, `__PredicatesVersion__`, `__SnapboxVersion__`, `__TempfileVersion__` | Step 4 |

Directory layout produced (`[tui]` = `ui: tui` only; `[gen]` = generated in Step 6, not a template):

```
Cargo.toml  Cargo.lock[gen]  rust-toolchain.toml  rustfmt.toml  deny.toml  .cargo/config.toml
src/main.rs  src/lib.rs  src/cli.rs  src/exit.rs  src/error.rs  src/output.rs  src/term.rs  src/config.rs
src/signals.rs  src/tests.rs
src/commands/{mod,greet,completion,schema,version}.rs  src/commands/browse.rs[tui]
src/tui/{mod,app,ui,ui_screenshots}.rs[tui]  .ui-quality.yml[tui]
tests/cli.rs  tests/golden/greet-ada.json  tests/golden/schema.json[gen]
xtask/Cargo.toml  xtask/src/main.rs
docs/modules/ROOT/pages/cli-reference.adoc[gen, only when docs/modules/ROOT exists]
```

## Step 6 — Scaffold the project

Apply Step 1's per-group decision to every file that already exists (Keep as is → skip; Update → merge after
showing `git diff --no-index <current> <draft>`; Replace → overwrite within Step 1's source-file limit). Files that
didn't exist are always written.

1. Write every template from the reference files this run reads, applying the markers and placeholders (UTF-8, LF
   line endings, a final newline). `tests/golden/` holds only `greet-ada.json` at this point.
2. `cargo generate-lockfile` (resolves `Cargo.lock`; the 2024 edition's resolver 3 prefers versions compatible with
   `rust-version`), then recompute the MSRV (Step 4.4) and, if it rose, update `rust-version` in both manifests.
3. `cargo fmt --all` — placeholder lengths change line wrapping; formatting is part of the template contract (the
   check in Step 7 must pass without further edits). On an existing project, run `cargo fmt --all --check` first
   and ask before reformatting files this skill didn't write.
4. Generate the schema golden file: `SNAPSHOTS=overwrite cargo test --locked --test cli` — writes
   `tests/golden/schema.json` (pretty-printed, keys sorted, `version` redacted as `[VERSION]` so releases don't
   touch it). Read it once to confirm the command list and the description.
5. `cargo xtask docs` — writes `target/dist/man/*.1`, `target/dist/completions/*`, and the CLI reference: into
   `docs/modules/ROOT/pages/cli-reference.adoc` when `docs/modules/ROOT/` exists (run again after
   `iru-setup-antora` when an orchestrator chains it later), else `target/dist/cli-reference.adoc`.

## Step 7 — Verify

Run through the `iru-gate-runner` agent where the logs are long (build, clippy, tests, coverage), reporting only
pass/fail and the key figures; quote error output verbatim for a failure only. Fix anything this skill wrote until
green — never "fix" pre-existing code to make a gate pass; report it instead. From the repository root:

```bash
cargo fmt --all --check
cargo clippy --workspace --all-targets --all-features --locked -- -D warnings      # --workspace: xtask too
cargo nextest run --workspace --locked                                              # or cargo test --workspace --locked
cargo test --doc --locked                                                           # nextest can't run doctests
RUSTDOCFLAGS="-D warnings" cargo doc --workspace --no-deps --locked
cargo deny check                                                                    # advisories need network
cargo llvm-cov nextest --workspace --locked --ignore-filename-regex '(^|/)xtask/' \
  --lcov --output-path target/lcov.info --fail-under-lines 80
cargo xtask docs && cargo xtask docs --check
cargo +<msrv> check --workspace --all-targets --locked     # only if `rustup toolchain install <msrv> --profile minimal` is acceptable
cargo build --release --locked
```

Then the smoke checks from `reference/smoke-checks.md`, extracted to a scratch directory **outside** the repository:
`bash <scratch>/smoke.sh ./target/release/<bin>` (pipes, exit codes 0/2/3/4, stdout purity, the envelope, no ESC
bytes when piped or with `NO_COLOR`, closed-pipe exit 0, the golden file) and, on macOS/Linux,
`python3 -I <scratch>/pty_smoke.py ./target/release/<bin> [tui]` (prompt, SIGINT/SIGTERM → 130/143,
`<BIN>_NO_INPUT`, and the TUI). On Windows run only `smoke.sh` under Git Bash, or report the PTY part "unverified
(needs a Unix pseudo-terminal)".

Expected on a fresh scaffold (verified): fmt clean, 0 Clippy warnings, 50 (`tui`) / 42 (`none`) in-process tests +
13 / 12 end-to-end tests + 1 doctest passed, rustdoc 0 warnings, `advisories ok, bans ok, licenses ok, sources ok`
(two `duplicate` warnings with `ui: tui`), line coverage 97.6% (`tui`) / 98.8% (`none`), every smoke check passing.
The `ui: tui` counts predate the UI-contract additions (the window test, the matrix test and five helper tests add
seven in-process tests) — a run also leaves 8 captures under `.ui-screenshots/screen/App/` (4 states × `ltr`/`rtl` ×
`no-color`); add `.ui-screenshots/` to `.gitignore` (`iru-setup-rust-gitignore` does).

## Step 8 — Report

Summarize: the mode (**scaffolded from scratch** / **updated an existing tool** / **stopped**), resolved
`bin-name`, `crate-name`, `description`, `ui`, version, MSRV (computed vs given), license (or none), and, per Step 1
group, the action taken — **created / updated / replaced / kept as is** — and whether it came from the user or
`on-existing`, listing each mismatch of a kept group and, for a replaced one, what customizations could have been
lost (check `git diff`) — including `.ui-quality.yml` (`ui: tui`: created / updated / replaced / kept as is, with
the `accessibility` level written). Then the crate versions used (live vs fallback, and any drift past the verified line),
each Step 7 command with its result (tests, coverage %, Clippy count, deny result, smoke checks), anything
**unverified** and why, and the ignored `args` keys. Say what `sonar` and `distribution` mean here (recorded only)
and list the Antora pages worth adding by hand: usage (getting started), exit codes and the error envelope, the
JSON output schema (`greet`, `schema`, `version`), using the tool from an agent (`--json --no-input`, `schema`,
exit-code reactions), plus the nav entry `* xref:cli-reference.adoc[CLI reference]` for the generated page.

### Scaffold contract (confirmed by running it — downstream skills depend on these)

| What | Exact name / path |
|---|---|
| Workspace | root `Cargo.toml` = the tool package `<crate-name>` + `[workspace] members = ["xtask"]`, `resolver = "3"`; lint policy in `[workspace.lints]` (`[lints] workspace = true` in both members) |
| Targets | library `src/lib.rs` (crate `<crate_name>`, all logic, `pub fn main() -> ExitCode` and `pub fn run(args, &mut Context) -> Exit`), binary `[[bin]] name = "<bin>"` → `src/main.rs` (one call) |
| Detection | `Cargo.toml` with `[[bin]]` + `clap` (+ `ratatui` for `ui: tui`); `src/exit.rs` (contract), `xtask/` |
| Version | `[package] version` in the root `Cargo.toml` (`0.1.0-dev` on gitflow `develop`); `xtask` is `0.0.0`, `publish = false`; tests read `env!("CARGO_PKG_VERSION")`, so a bump touches only `Cargo.toml` + `Cargo.lock` |
| Exit codes | `src/exit.rs` `enum Exit` (0–7, 130, 143, `name()` = envelope `code`) |
| Env vars | `<BIN>_FORMAT`, `<BIN>_NO_INPUT` (Boolish: `1/true/yes/on`), `<BIN>_CONFIG`; plus `NO_COLOR`, `FORCE_COLOR`/`CLICOLOR_FORCE`, `TERM`, `CI`, `XDG_CONFIG_HOME`/`HOME`/`APPDATA` |
| Format / lint | `cargo fmt --all --check`; `cargo clippy --workspace --all-targets --all-features --locked -- -D warnings` |
| Tests | `cargo nextest run --workspace --locked` (or `cargo test --workspace --locked`) + `cargo test --doc --locked`; unit/in-process tests in `src/**` and `src/tests.rs`, end-to-end in `tests/cli.rs` (assert_cmd; never `env_clear()` — it drops `LLVM_PROFILE_FILE`) |
| Golden files | `tests/golden/*.json`, refreshed with `SNAPSHOTS=overwrite cargo test --test cli` (snapbox); `schema.json` redacts `version` |
| Coverage | `cargo llvm-cov nextest --workspace --locked --ignore-filename-regex '(^|/)xtask/' --lcov --output-path target/lcov.info` (end-to-end runs of the binary are instrumented; 80% line bar) |
| Docs | `RUSTDOCFLAGS="-D warnings" cargo doc --workspace --no-deps --locked` → `target/doc/<crate_name>/`; doctests via `cargo test --doc` |
| Supply chain | `cargo deny check` (`deny.toml`) |
| CLI docs | `cargo xtask docs` → `target/dist/man/<bin>.1` + `<bin>-<command>.1`, `target/dist/completions/{<bin>.bash,_<bin>,<bin>.fish,_<bin>.ps1,<bin>.elv}`, `docs/modules/ROOT/pages/cli-reference.adoc` (or `target/dist/cli-reference.adoc` without Antora); `cargo xtask docs --check` exits 1 when the committed page is stale |
| Release binary | `cargo build --release --locked [--target <triple>]` → `target/[<triple>/]release/<bin>[.exe]` (fat LTO, `codegen-units = 1`, stripped, `panic = "unwind"`); `cargo check` passes for `x86_64-unknown-linux-musl` and `x86_64-pc-windows-msvc` |
| UI contract (`ui: tui`) | `.ui-quality.yml` at the root; captures via `src/tui/ui_screenshots.rs` (`capture`, `check_accessibility`, `tui_violations`, `ui_quality`) into `$UI_SCREENSHOTS_DIR` or `.ui-screenshots/screen/App/<state>--<ltr\|rtl>--no-color.txt` |
| Smoke contract | `<bin> --version`/`--help` exit 0 on stdout; unknown command 2; `greet --json` → `{"greeting":"Hello, NAME!","name":"NAME","schemaVersion":1}`; `greet ''` 3 + envelope; `schema nope` 4; `browse` without a TTY 2 |

### Warn explicitly

- Review every generated file before committing — especially `description`, `authors`, `license` and the sample
  `greet` command, which is a placeholder for real commands (keep its tests' *shape* when replacing it).
- **Commit `Cargo.lock`** (it is a binary) and the golden files; refresh goldens only deliberately and bump
  `schemaVersion` for a breaking JSON change.
- New commands must be added to `commands::info` (exit codes + safety) — a unit test fails otherwise — and to the
  golden `schema.json`; regenerate the CLI reference with `cargo xtask docs` in the same commit.
- Run `iru-setup-rust-gitignore` — `/target/` (build, coverage, `target/dist`) must never be committed.
- With `sonar` ≠ `none`, a `SONAR_TOKEN` secret and the Sonar project must exist before CI analysis works; with
  `distribution: store` and the crates-io channel, the crate name must be free and a crates.io token/trusted
  publisher configured (the workflows skill lists the secrets).
- No `LICENSE` file was written: add it (both files for `MIT OR Apache-2.0`) or run `iru-check-license`.

## Verification notes

Rendered from these exact reference files on 2026-10-16 into `$TMPDIR/iru-verify/cli/iru-setup-rust-cli/`
(outside the repository; macOS 27 arm64, Rust 1.99.1 in a throwaway `RUSTUP_HOME`): `render-tui` (`shelfctl`,
`ui: tui`, `MIT OR Apache-2.0`, repository set), `render-none` (`bin-name: hello`, `crate-name: hello-tool` —
bin ≠ package —, `ui: none`, no license), and `final-tui` re-rendered from the files in this skill. Each passed:
`cargo generate-lockfile`; `cargo fmt --all --check` after one `cargo fmt`; Clippy `-D warnings` on the workspace
(0 warnings) and on `--target x86_64-pc-windows-msvc`; `cargo check --target x86_64-unknown-linux-musl`;
nextest (63 / 54 tests), doctests, rustdoc `-D warnings`; cargo-deny 0.20.2 (`advisories ok, bans ok, licenses ok,
sources ok`; `ui: tui` warns `duplicate` for `signal-hook` 0.3/0.4 — crossterm 0.29 still uses 0.3 — and `syn`
2/3); cargo-llvm-cov 0.9.1 line coverage 97.59% (`tui`) / 98.77% (`none`) with `src/main.rs` at 100% from the
end-to-end runs; `cargo xtask docs` (6 / 5 man pages, 5 completion scripts, the reference into
`docs/modules/ROOT/pages/`) and `--check` (0, then 1 after a hand edit); the generated AsciiDoc converted by
Asciidoctor.js 3.0.4 with 0 warnings; MSRV checks with `cargo +1.88` (`tui`) and `cargo +1.85 check`/`test`
(`none`); `cargo publish --dry-run` (packaged, verified, upload aborted); `--version` ≈ 6.5 ms. Smoke checks on the
release binary: every `smoke.sh` expectation, and on a pseudo-terminal: prompt, SIGINT/SIGTERM at the prompt →
130/143, `<BIN>_NO_INPUT=1` → 2 and `=0` prompts, `browse` Down+Enter → greeting after `ESC[?1049l`, `q` → 0,
Ctrl-C → 130, SIGTERM in the TUI → terminal restored, `shelfctl: terminated`, 143.

Gotchas found and fixed in the templates: an env-backed bool flag needs `BoolishValueParser` (clap's default
rejected `<BIN>_NO_INPUT=1` with exit 2); `clippy --all-targets` without `--workspace` silently skipped `xtask`;
clippy 1.99's `assert_is_empty` and `doc_markdown` lints; the first frame of a Ratatui app on a 0×0 pty is empty;
signal handlers are process-wide, so only one test installs them; hard-coded versions in tests would break every
bump (`env!("CARGO_PKG_VERSION")` instead); clap_complete panics on a failed write (scripts are generated into
memory first); `ratatui`'s default features add widgets and backends the picker doesn't use (only `crossterm` is enabled; 104 instead of 113 crates).

**UI-contract additions unverified**: `.ui-quality.yml`, `src/tui/ui_screenshots.rs`, `App::visible_window`/
`selected_index` (replacing `list_state`) and the matrix test in `tui/ui.rs` were added later without a Rust toolchain
on the authoring machine — written against the ratatui 0.30 API (`Buffer::content`/`area`, `ListState::offset_mut`,
`Span::width`) but never compiled here; the first `ui: tui` run's Step 7 is their verification.

Not verified locally: running on Windows (signals there: Ctrl-C only; SIGTERM is never delivered) and Linux
(compile-checked for musl, not run); the TUI on Windows terminals; publishing to crates.io for real; the GitHub
Actions side (owned by `iru-setup-cli-github-workflows`).

## Sources

- irurueta docs: `ai/cli-for-agents/streams-and-exit-codes.adoc`, `tty-colour-and-interactivity.adoc`,
  `machine-readable-output.adoc`, `safety-and-idempotency.adoc`, `configuration-and-auth.adoc`,
  `self-describing-help.adoc` (the `schema` shape), `frameworks-go-and-rust.adoc` (clap, clap_complete, clap_mangen,
  Ratatui), `tuis-vs-clis.adoc`, `testing-clis.adoc`, `documenting-clis.adoc`, `agent-readiness-checklist.adoc` —
  https://www.irurueta.com/ai/cli-for-agents/index.html
- irurueta docs: `programming-languages/rust/cargo-and-workspaces.adoc` (workspace, `[lints]`, release profile,
  resolver 3), `tooling-clippy-rustfmt-and-rust-analyzer.adoc` (lint groups, `-D warnings` only in CI,
  `rustfmt.toml`, cargo-deny), `toolchain-rustup-and-editions.adoc` (`rust-toolchain.toml`, MSRV),
  `error-handling.adoc` (`thiserror`), `testing-and-benchmarking.adoc`, `documentation-with-rustdoc.adoc`,
  `io-files-processes-and-environment.adoc`, `serialization-with-serde.adoc`
- clap (https://docs.rs/clap/4), clap_complete, clap_mangen, Ratatui (https://ratatui.rs, `ratatui::run`,
  `TestBackend`), signal-hook (`flag::register_conditional_shutdown`), assert_cmd, snapbox, cargo-llvm-cov,
  cargo-nextest, cargo-deny (https://embarkstudios.github.io/cargo-deny/), the Cargo Book (`rust-version`,
  `[lints]`, `[profile]`), NO_COLOR (https://no-color.org)
- This catalog: the shared CLI contract (`cli-contract.md`), `iru-setup-windows-app` / `iru-setup-macos-app` /
  `iru-setup-python-fastapi` (structure)
