---
name: iru-rust-code-one-task
description: >-
  Implement a single task from a Rust `implementation_plan.md`-style task list — just the implementation and its
  tests — in any Cargo package or workspace: an agent-friendly command-line tool scaffolded by `iru-setup-rust-cli`
  (logic in `src/lib.rs`, thin `src/main.rs`, clap 4, optional Ratatui UI, `tests/cli.rs`, `xtask/`) or any other
  Rust library, service or CLI. Detects at runtime, from `cargo metadata` and the manifests, the workspace vs.
  single-crate layout, lib/bin targets, edition and `rust-version` (MSRV), `rust-toolchain.toml`, clap derive vs.
  builder, ratatui/crossterm, tokio, the test crates (assert_cmd, predicates, snapbox/trycmd, insta, tempfile,
  testcontainers), the `[lints]`/`clippy.toml`/`rustfmt.toml`/`deny.toml` configuration, an `xtask` member, and
  whether the project follows the catalog's CLI contract (an exit-code enum mapped to `ExitCode`, `--format`/`--json`,
  a JSON error envelope) — then loads only the matching guidance from this skill's own `reference/` directory
  (always: Rust code style — edition 2024 rules, logic in the lib, naming, ownership, the lint set, no new
  dependencies — and testing — unit tests with injected writers, `assert_cmd` end-to-end tests with a cleared
  environment that still forwards `LLVM_PROFILE_FILE`, golden JSON, exit-code tables, no-TTY and `NO_COLOR` tests;
  as needed: error handling with `thiserror` and one failure→exit-code mapping, rustdoc, the shared CLI contract,
  clap, output/colour/prompts/signals/broken pipe, Ratatui with `TestBackend`, the catalog's UI contract on Ratatui
  when a task touches the terminal UI — `Widget` components, `Action` events, lists rendering only the visible window,
  state × direction × theme UI tests captured as `.txt` into `.ui-screenshots/`, asserted accessibility checks at the
  `.ui-quality.yml` level —, security — argv-only processes, path
  canonicalization, redacted secrets, `unsafe_code = "forbid"` — and async/tokio only when the project already uses
  it). Re-checks the current code state, implements exactly what the task specifies, writes/updates its tests,
  formats only its own files with rustfmt, compile-checks with `cargo check --all-targets --locked` (plus
  `--all-features` when the package has features), then — if the task didn't stop on a blocker — immediately checks
  off this task's own checkbox (and its sub-tasks') in `implementation_plan.md` with a "group validation pending"
  note, before handing back a short summary. Does not run tests, clippy, coverage, `cargo deny`, `cargo doc`, or
  license-header checks — those happen once per task group in `iru-rust-code-one-task-group`, which invokes this skill
  once per task (in parallel when the group allows it, through `iru-isolated-skill-executor`). Invoke as
  `/iru-rust-code-one-task <task description>`, passing the task's own text — including its exact
  `implementation_plan.md` checkbox line(s) — as the argument. The coding skill for plan tasks tagged `rust`.
model: sonnet
allowed-tools: Read Edit Write Bash(cargo check *) Bash(cargo metadata *) Bash(cargo tree *) Bash(cargo fmt *) Bash(rustfmt *) Bash(cargo --version) Bash(rustc --version) Bash(rustup show *) Bash(rustup target list *) Bash(uname *) Bash(git status *) Bash(git diff *) Bash(git log *) Bash(find *) Bash(grep *) Bash(ls *) Bash(cat *)
---

# Implement one plan task (Rust)

Carry out a single task's implementation, tests, and checkbox update in a Rust crate or workspace — nothing else.
This is the narrowest execution unit for a `rust` task in the `iru-code` pipeline: `iru-rust-code-one-task-group`
calls it once per task in a bucket (potentially many at once, in parallel agents), then handles license headers,
rustdoc auditing, tests, coverage, clippy/rustfmt/cargo-deny, and any container-backed tests itself, once for the
whole bucket. It uses a medium model on purpose — the plan carries the hard reasoning; this skill executes one task
against code agreements that live in `reference/`.

Two things shape every Rust task:

1. **Logic lives in the library.** In a CLI, `src/main.rs` only gathers process facts and calls one `lib` entry point
   with injected writers; commands, policies, the TUI state and rendering are library code with unit tests. That is
   what makes the 80% per-file coverage bar reachable — where a piece of code goes is the first decision.
2. **A contract CLI's observable behaviour is the interface.** When the project follows the catalog's CLI contract,
   stdout/stderr separation, the exit-code enum, the JSON envelope, `--format`, no prompts without a TTY, and
   `NO_COLOR` are non-negotiable: a change that breaks one is a bug, whatever the task says about style.

## Step 0 — Detect the project shape once

Settle these from the files, never from assumptions (this skill is copied into other repositories):

- **Rust at all**: a `Cargo.toml` at the repository root or in the directory the task names. None → this isn't a Rust
  project: report it as a blocker (the task was mis-tagged) and stop.
- **Layout**: `cargo metadata --no-deps --format-version 1 --locked` (no `jq` assumed — read the JSON): workspace
  members (`workspace_members`, a virtual manifest with only `[workspace]`, `[workspace.package]`/
  `[workspace.dependencies]`/`[workspace.lints]` inheritance), each package's targets (`kind`: `lib`, `bin`, `test`,
  `example`, `bench`, `custom-build` for `build.rs`), `edition`, `rust_version`, and `features`. Note an `xtask`
  member and the `.cargo/config.toml` alias that runs it. A bin-only package (no `lib` target) can't be imported by
  `tests/` — note it; don't create `lib.rs` unless the task says so.
- **Toolchain**: `rust-toolchain.toml` (channel, components, targets), `cargo --version`/`rustc --version`;
  `clippy.toml` (`msrv`, `allow-unwrap-in-tests`, …), `rustfmt.toml` (`style_edition`, `max_width`), `deny.toml`. An
  older toolchain than `rust-version` → "compile-check unavailable", not a reason to edit the toolchain file.
- **Lints**: `[lints]` / `[workspace.lints]` (and whether members say `lints.workspace = true`) — what new code must
  satisfy (`missing_docs`, `unsafe_code = "forbid"`, the clippy pedantic subset, `print_stdout`, `unwrap_used`).
- **Frameworks** (from `[dependencies]`): `clap` with the `derive` feature and `#[derive(Parser)]` → derive API, else
  builder; `clap_complete`/`clap_mangen`; `ratatui` (and whether code imports `ratatui::crossterm` or a separate
  `crossterm`); `tokio` (and its features); `serde`/`serde_json` (check `cargo tree -e features -i serde_json` for
  `preserve_order` only when a task touches JSON ordering); `thiserror`/`anyhow`; `anstream`/`anstyle`/`owo-colors`;
  `dialoguer`; `signal-hook`/`ctrlc`; `indicatif`; `tracing`/`log`.
- **Tests** (`[dev-dependencies]` + `tests/`): `assert_cmd`, `predicates`, `tempfile`/`assert_fs`, `snapbox`/`trycmd`
  (`tests/cmd/*.trycmd`), `insta` (`snapshots/`), `proptest`, `rstest`, `serial_test`, `testcontainers` (container
  tests marked `#[ignore = "…"]`); golden files (`tests/golden/`); a `#[cfg(test)] mod test_support` helper; two or
  three existing tests for naming and helper style.
- **CLI contract**: the project follows it when it has an exit-code enum (or const block) converted into
  `std::process::ExitCode` with the contract's numbers (2 usage, 3 validation, 4 not found, 5 confirmation…), a
  `--format`/`--json` global flag, or an error envelope with `schemaVersion`. Then `reference/cli-contract.md` rules
  are binding for every command/output change. A CLI without those signals → follow its own conventions and don't
  retrofit the contract unless the task asks (report the divergence). A non-CLI crate → the CLI references are never
  routed.
- **Host**: `uname -s` (absent/`MINGW*`/`MSYS*` → Windows). `#[cfg(windows)]` code can be compile-checked with
  `--target x86_64-pc-windows-msvc` only when `rustup target list --installed` already lists it — never install a
  target here.

## Step 1 — Decide where the code goes, then read only the reference material this task needs

A path in the task wins. Otherwise: domain logic, command behaviour, output/terminal policies, config merging, TUI
state/rendering → the library (`src/lib.rs` modules, `src/commands/<name>.rs` in the scaffold); clap types →
`src/cli.rs`; process-fact gathering → `src/main.rs` (only that); generators (man pages, completions files, CLI
reference) → `xtask/`; shared code in a workspace → the member that owns the concept. Genuinely ambiguous → the
library, and say so in Step 8. Record the packages the task touches — Step 5 derives the compile-check from them.

This skill ships a `reference/` directory next to this file. Read `reference/README.md` first — it is short and
routes you to the rest — then read only what it points at. The routing, restated:

| Read | When |
|---|---|
| `reference/code-style.md` | **Always.** |
| `reference/testing.md` | The task writes or updates tests — nearly every task. |
| `reference/error-handling.md` | An error type, a fallible function, a panic/`expect`, or the failure→exit-code mapping. |
| `reference/rustdoc.md` | The task adds or changes a `pub` item (including clap fields/variants — their docs are `--help`). |
| `reference/cli-contract.md` | Contract CLI (Step 0) and the task touches a command, flag, output, exit code, prompt, signal, config, `schema` or `completion`. |
| `reference/clap.md` | A subcommand, argument, flag, value enum, env-backed flag, help text, completions/man pages, or config precedence. |
| `reference/output-and-terminal.md` | Writing to stdout/stderr, JSON/JSONL/the envelope, colour, prompts, progress, SIGINT/SIGTERM, broken pipe. |
| `reference/ratatui.md` | `ratatui` is a dependency and the task touches the terminal UI. |
| `reference/ui-contract.md` + `reference/ui-implementation.md` | `ratatui` is a dependency and the task adds or changes a screen, component, list or other UI. |
| `reference/security.md` | Spawning a process, paths from arguments/config, untrusted input, tokens/secrets, writing files, or anything tempting `unsafe`/`env::set_var`. |
| `reference/async.md` | `tokio` is already a dependency and the task touches async code, cancellation, timeouts, or async tests. |

If `reference/` is missing (the skill directory was copied without it), proceed using the repository's own
`CLAUDE.md` conventions and the surrounding code's style, and say so in Step 8 — don't guess at what the reference
would have said.

## Step 2 — Re-check the current code state

Read the actual current content of every file the task touches before editing — other tasks in the same bucket may
be landing concurrently. Also read what binds to what you change: for a new/renamed subcommand or flag, `src/cli.rs`,
the dispatch in `lib::run`, the `schema` command, and the end-to-end tests and golden files that pin its output; for
a changed error, every `From` impl and the exit-code mapping; for a changed `pub` signature, its callers (`grep -rn`
across the workspace, `xtask/` and `tests/` included). Note what the surrounding code does about the things
`reference/` has opinions on; a crate that consistently does something else wins, and the divergence goes in Step 8.

## Step 3 — Implement exactly what the task specifies

Apply `reference/code-style.md` and whichever optional files Step 1 selected, plus the repository's own `CLAUDE.md`
where more specific. Work in dependency order: domain types and errors → logic → command wiring (clap types,
dispatch, `schema`) → `main.rs` only if process facts change.

Non-negotiable, because a gate, the contract, or another platform enforces them:

- **`main.rs` stays thin** — no logic, no branching beyond collecting facts and calling the library.
- **No `println!`/`print!`/`eprintln!`/`process::exit`** in library or command code: write through the injected
  writers and return an `Exit`; never panic on input (`unwrap`/`expect`/indexing on untrusted data).
- **Contract CLIs**: results only on stdout, everything else on stderr; failures map to the existing exit-code enum
  in one place (never a new number, never renumbering); JSON output keeps sorted keys, `schemaVersion`, and the error
  envelope; prompts only behind the TTY/`--no-input`/`CI` policy; destructive commands keep `--dry-run`/`--yes`; a TUI
  starts only on a TTY and its actions keep a `--json` command.
- **Docs on every new `pub` item** (`missing_docs` + `-D warnings` in CI), `# Errors`/`# Panics` sections where they
  apply.
- **No new dependency, feature, crate, workspace member, edition/MSRV/toolchain change, `unsafe`, or lint
  relaxation** (`#[allow]`, `[lints]` edits) unless the task explicitly calls for it — a blocker to report (Step 6)
  otherwise. When the task does add a dependency, follow `reference/code-style.md` (workspace dependencies, minimal
  features); `cargo check` updates `Cargo.lock` — never hand-edit it.
- **Never hand-edit generated output** — completions, man pages, a generated `cli-reference.adoc`/partial, `insta`
  snapshots you haven't reviewed, anything under `target/`.

- **Terminal UI work decomposes first** (`reference/ui-contract.md` §2): write the `Screen › Region › Component` tree
  (inputs, `Action` events, visual states, what is reused) before coding, build leaves first, keep raw `KeyEvent`s
  inside key handling, render collections through the visible-window pattern (`reference/ui-implementation.md`), and
  include the tree in the Step 8 report.

Don't add anything the task didn't ask for — no speculative abstractions, no unrelated cleanup, no restyling.

## Step 4 — Write or update the tests

Follow `reference/testing.md` and the existing test style: unit tests in a `#[cfg(test)] mod tests` at the bottom of
each changed file, commands tested through the crate's in-memory test helper (stdout/stderr buffers, fake confirm,
injected TTY facts); for every new or changed command, error path or flag in a contract CLI, end-to-end tests in
`tests/cli.rs` (or the crate's equivalent) through the clean-environment helper — exit code from a table, exact
stdout (golden file for `--json`), `stderr("")` on success, one envelope on stderr and empty stdout for a JSON
failure, a closed-stdin "never prompts" case, `NO_COLOR`/no-TTY output without escape bytes; `TestBackend` tests for
TUI rendering and plain `KeyEvent` tests for its state — and, for a screen/component the task added or changed, the
UI tests of `reference/ui-implementation.md` §4–§6: every visual state with minimal/typical/many-items/long-content
and right-to-left fixtures, each captured through `src/tui/ui_screenshots.rs` as
`.ui-screenshots/<kind>/<Id>/<state>--<direction>--<theme>.txt` for every `.ui-quality.yml` direction × theme the
TUI has (plus `no-color`), and the asserted accessibility checks at the file's level. Tests never depend on the real terminal, the network, the
user's config, or process-global state (no `env::set_var`; temp dirs for `HOME`/`XDG_CONFIG_HOME`). A test that
needs Docker or the network is marked `#[ignore = "requires docker (testcontainers)"]`. Cover the edge cases implied
by the doc comments' `# Errors`/`# Panics`. Update golden files deliberately and name each one in Step 8. Do not run
the tests — `iru-rust-code-one-task-group` runs them once per bucket.

## Step 5 — Format and compile-check

A broken compile in one task blocks every other task in a parallel bucket from validating.

1. **Format only the files this task wrote or edited**: `rustfmt --edition <edition> <file> …` (rustfmt picks up the
   repository's `rustfmt.toml`). rustfmt also formats the out-of-line child modules of a file it's given (verified) —
   when a touched file is a `lib.rs`/`main.rs`/`mod.rs`, check `git diff --name-only` afterwards and list any other
   file it reformatted in Step 8. Never run `cargo fmt` over the whole workspace here (sibling tasks are editing it).
2. **Compile-check** the touched packages, tests included:
   `cargo check --all-targets --locked -p <package>` (one `-p` per touched package; `--workspace` only when the task
   changed something every member depends on), adding `--all-features` when the package declares features (the CI
   convention) — and also the default features if the task touched `#[cfg(feature = …)]` code. `--locked` fails if
   `Cargo.lock` would change: for a task that legitimately adds a dependency, run once without `--locked` to update
   the lock file, then re-run with it. Keep the crate's lint configuration as is: a rustc warning (`missing_docs`,
   `unused_imports`, `dead_code`) in code this task wrote is the task's own error to fix now. Clippy is **not** run
   here — the group runs it once — but write code that satisfies the crate's `[lints]` (`reference/code-style.md`).
3. `#[cfg(windows)]`/`#[cfg(unix)]` code: when the other target is already installed, also
   `cargo check --all-targets --locked --target <triple> -p <package>`; otherwise say "other-OS cfg unchecked".

Outcomes:

- **Failure in code this task wrote or edited**: fix it — it's the task's own code, not a finding to defer.
- **Failure outside the task's scope** (a sibling task's in-flight edit, a pre-existing error): don't fix unrelated
  code; re-run once if it looks like a transient race with a concurrently-writing sibling, then note it in Step 8.
  (Concurrent `cargo` runs wait on the build-directory lock — "Blocking waiting for file lock" is normal, not a
  failure.)
- **`cargo` can't run at all** (toolchain older than `rust-version`, no network for a first dependency fetch, a
  `rust-toolchain.toml` channel that isn't installed): report "compile-check unavailable" with the reason — the
  group's validation still catches real errors.

## Step 6 — When to interrupt the user

Keep interruptions rare. Stop and use `AskUserQuestion` (or plain text if no real choice is offered) only when:

- The task is ambiguous in a way that changes correctness or scope and can't be safely inferred.
- The task's approach is infeasible against the real code (it names an item that doesn't exist, needs a binary-only
  crate's internals from `tests/`, or demands a behaviour the CLI contract forbids — a prompt without a TTY, data on
  stderr, a renumbered exit code).
- The task needs a new dependency/feature/crate/member, a toolchain/edition/MSRV change, `unsafe`, or a lint
  relaxation it doesn't explicitly call for.
- The task would put a secret in arguments, output, logs, or source (`reference/security.md`) — a design problem to
  report.
- A breaking change to published JSON output (renamed/removed/retyped field) that the task doesn't acknowledge — it
  needs a `schemaVersion` decision.

Don't stop merely because the task is nontrivial. Don't report the task done to work around a blocker; report it as
blocked (Step 8). A conflict between `reference/` and the surrounding code is not a reason to stop: follow the
surrounding code and report the divergence.

## Step 7 — Check off this task's checkbox now

If this task did not stop on a blocker, update `implementation_plan.md` at the repository root before reporting back.
Re-read it fresh (sibling tasks may be editing it), locate this task's own checkbox line by the exact text passed in,
flip `[ ]` to `[x]` for it and every sub-task the work covered, and add a short note naming the packages and files
touched, e.g.:

```
- [x] Task 3. **Add `list` command with `--limit`/`--cursor`** — src/cli.rs, src/commands/list.rs, schema entry,
  tests/cli.rs + tests/golden/list-default.json; group validation pending.
```

Keep the "group validation pending" wording — `iru-rust-code-one-task-group` replaces it with the final outcome.
Edit only this task's own line(s). If this task stopped on a blocker, leave its checkbox untouched.

## Step 8 — Report the outcome

Hand back a short summary:

- **The shape detected** (workspace/single crate, packages and targets, edition/MSRV, clap API, ratatui/tokio,
  contract CLI or not, test crates) and **the packages touched**, with the reference files actually read.
- **The files touched** and **the tests added/updated** (unit, end-to-end, TUI, doctests — not run), and every
  golden/snapshot file created or changed (and whether a JSON change is additive or needs a `schemaVersion` bump).
- **The compile-check result per package** (and `--all-features`/other-target checks): passed, failed on this task's
  code and fixed, failed outside this task's scope, or unavailable (and why); any file rustfmt reformatted beyond the
  task's own.
- **For terminal UI work**: the `Screen › Region › Component` decomposition, and the UI tests and captures added
  (component/screen/flow, states × directions × themes, accessibility rule ids checked; not run).
- **Generated artifacts that need regenerating** (completions, man pages, CLI reference via `cargo xtask …`) because
  the command tree changed.
- **Whether this task stopped on a blocker**, with enough detail for the caller to surface it.
- **Any deliberate deviation from `reference/`**, and pre-existing violations noticed and left alone (`println!` in
  commands, logic in `main.rs`, `unwrap` on input, a missing contract rule, secrets in output).

This skill never runs tests, clippy, coverage, `cargo deny`, `cargo doc`, the full workspace `cargo fmt`, or
license-header checks, and never captures a quality baseline.

## Verification notes

Exercised in `$TMPDIR/iru-verify/cli/rust-coding/` on macOS (arm64) with Rust 1.99.1 (clippy 0.1.99, rustfmt
`style_edition = "2024"`), cargo-nextest 0.9.148 and cargo-llvm-cov 0.9.1, crate versions resolved live from
crates.io on 2026-10-16 (clap 4.6.7, clap_complete 4.6.11, clap_mangen 0.3.3, ratatui 0.30.2, anstream 1.0.0,
anstyle 1.0.14, dialoguer 0.12.0, signal-hook 0.4.5, thiserror 2.0.21, serde_json 1.0.154, toml 1.1.8, tokio 1.53.3,
assert_cmd 2.2.2, predicates 3.1.4, tempfile 3.27.0):

- A `democli` crate built to the guidance (edition 2024, `rust-version = "1.88"`, the recommended `[lints]` set;
  `Exit` enum 0–7/130/143, `CliError` + `RunError`, sorted-key `write_json`, the envelope, colour/prompt policies,
  `signal-hook` interrupts, `greet`/`reset`/`completion`/`schema`/`browse` with a Ratatui list) passed `cargo check
  --all-targets --locked`, `cargo test` (45 unit + 9 end-to-end + 1 doctest), `cargo nextest run` (54 passed),
  `cargo clippy --all-targets --all-features -- -D warnings` and `cargo fmt --check`, and `RUSTDOCFLAGS="-D warnings"
  cargo doc --no-deps`; `cargo check`/`clippy --target x86_64-pc-windows-msvc` also passed (incl. signal-hook's
  `register_conditional_shutdown`), and so did `cargo check --target x86_64-unknown-linux-gnu`. `cargo llvm-cov`:
  96.6% lines overall, every file ≥ 86% (`main.rs` 100% via the end-to-end tests); the lowest, `browse.rs` 86.8% and
  `tui/mod.rs` 91.5%, miss exactly the terminal-bound `ratatui::run`/event-loop lines.
- A second crate compiled and tested every other snippet (path canonicalization incl. a symlink escape, argv-only
  `Command`, a redacting `Token` + `0600` file, control-character stripping, config precedence with
  `deny_unknown_fields`, `clap_mangen::generate_to`, tokio `select!` with timeout/ctrl_c/SIGTERM).
- Real-process checks: SIGTERM → 143, SIGINT → 130 after cleanup, a second SIGINT during cleanup exits after 50 ms
  instead of 300 ms; tokio variant: timeout → 6, SIGTERM → 143, SIGINT → 130; `democli browse` under a pseudo-terminal
  (80×24) rendered, quit on `q` with exit 0, entered and left the alternate screen.
- Findings folded into `reference/`: a bool flag with `env = "…"` rejects `1` unless it uses `BoolishValueParser`;
  `assert_buffer_lines` also compares styles (use `Buffer::with_lines` + `set_style` + `assert_buffer`); `env_clear()`
  in end-to-end tests drops `LLVM_PROFILE_FILE` and `main.rs` then measures 0% (forward it); clippy pedantic's
  `struct_excessive_bools` fires on clap flag structs, `doc_markdown` on bare `serde_json`, `assert_is_empty` on
  `assert!(!s.is_empty())`; `allow-unwrap-in-tests` doesn't cover helper fns in `tests/*.rs`; clap's `StyledStr`
  `Display` is plain text; `#[tokio::test(start_paused = true)]` needs `test-util`; rustfmt formats child modules of a
  file it's given.
- `reference/ui-contract.md` (verbatim catalog copy) and `reference/ui-implementation.md` were added later for the UI
  contract without a Rust toolchain on the authoring machine: the Ratatui APIs they use (`Buffer::content`/`area`,
  `Cell::symbol`, `Span::width`, `ListState::offset_mut`, `TestBackend::buffer`) were checked against docs.rs, the
  code sketches were not compiled.
- **Unverified locally**: running the binaries on Windows/Linux (only cross-`check`ed), the TUI on a Windows console,
  real `dialoguer` prompts (they need a TTY; the policy and fake-confirm paths are tested), and container-backed
  (`testcontainers`) tests.
