---
name: iru-rust-rustdoc
description: >-
  Audit given Rust items or files (a crate or Cargo workspace — e.g. a command-line tool's `src/lib.rs` modules, a library) for complete rustdoc on every public item — crate/module `//!` docs, a one-sentence summary line, and the conventional `# Errors` (functions returning `Result`), `# Panics` (functions that can panic), `# Safety` (`unsafe fn`/traits) and `# Examples` (runnable doctests where they add value) sections, with intra-doc links (``[`Type::method`]``) instead of bare names — generate any missing or incomplete docs grounded in the actual code and current changes, then verify the result: the doc lints scoped to the files (`missing_docs`, `clippy::missing_errors_doc`, `clippy::missing_panics_doc`, `clippy::missing_safety_doc`, `clippy::doc_markdown`, run through `cargo clippy --message-format=json` even when the project's `[lints]` table doesn't enable them), `cargo doc --workspace --no-deps` with `RUSTDOCFLAGS="-D warnings"` (broken intra-doc links, `rustdoc::missing_crate_level_docs`, bare URLs, invalid code-block attributes), and `cargo test --doc` so every new example compiles and passes. Knows that doctests only run for library targets — doc examples in a bin-only crate's `main.rs` are never compiled — and that this catalog's CLI scaffold keeps the logic in `lib.rs` for that reason. Invoke as `/iru-rust-rustdoc <items-or-files>` (comma-separated item paths such as `crate::output::Envelope`, `commands::greet::run`, `<member_crate>::config`, or files/globs such as `src/output.rs,src/commands/*.rs`), or `/iru-rust-rustdoc` with no argument to scope to the `.rs` files touched by uncommitted changes plus commits on the current branch not yet on the base branch. Use whenever the user (or `iru-rust-code-one-task-group` via `iru-gate-runner`) wants rustdoc completeness checked and filled in for specific Rust code, instead of waiting for a `missing_docs` warning or a broken link to fail CI.
model: sonnet
allowed-tools: Read Edit Write Glob Grep Bash(git *) Bash(cargo *) Bash(RUSTDOCFLAGS=* *) Bash(python3 *) Bash(rustup *) Bash(command -v *) Bash(find *) Bash(grep *) Bash(ls *) Bash(cat *) Bash(head *) Bash(test *) Bash(mkdir -p target*) Bash(rm -f target/iru-rust-rustdoc-*)
---

# Rust Rustdoc

Make sure a set of Rust items carry complete, well-formed rustdoc, filling in whatever is missing, then prove the
result through the doc lints, a warnings-as-errors `cargo doc` build, and the doctests. This skill only adds/completes
doc comments (`///`, `//!`) — it does not change behavior, signatures, attributes, `use` lines, or any non-doc
code. Test code (`tests/`, `#[cfg(test)] mod tests`, `benches/`) and generated code are out of scope; docs
they already have are left as-is. It makes no assumptions about this being any particular repository — discover the
workspace, its conventions and tooling fresh each run.

## Step 0 — Survey the workspace

```bash
cargo metadata --format-version 1 --no-deps | python3 -c 'import json,sys; m=json.load(sys.stdin); ids=set(m["workspace_members"]); print(m["workspace_root"]); [print(p["name"], [(t["kind"][0], t["src_path"], t["doctest"]) for t in p["targets"]]) for p in m["packages"] if p["id"] in ids]'
```

- Run everything from the workspace root. Note each member's **library root** (`kind` `lib`, `src_path`
  `…/src/lib.rs`) and binaries. A target with `doctest: false` (every bin, or a lib with `doctest = false` in
  `[lib]`) never runs its examples.
- **Bin-only crates**: doc comments in `src/main.rs`/`src/bin/*.rs` are rendered by `cargo doc` only when no library
  shares the name, and their code blocks are **never** compiled or run (`cargo test --doc` on such a package fails with
  `no library targets found`, verified). Document a binary's items for readers, but don't write `# Examples` there —
  put examples on the library items the binary calls. This catalog's CLI scaffold keeps `main.rs` thin for this reason.
- Tooling: `cargo clippy --version` and `cargo doc` (rustdoc ships with every toolchain). Clippy missing → the section
  lints in Step 3 can't run; say so and rely on reading the code plus Step 5's build.

## Step 1 — Determine scope

- **Argument provided**: comma-separated item paths or files/globs.
  - Files/globs → expand with `find`/`ls`; keep `.rs` files.
  - Item paths → resolve to the defining file: `crate::output::Envelope` / `output::Envelope` → the module file
    (`src/output.rs` or `src/output/mod.rs`) of the crate whose library root you're in (with several members, ask or
    prefer the CLI package), then `grep -n "pub \(struct\|enum\|trait\|fn\|type\|const\|static\|mod\) Envelope"` to
    find the item; `<member_crate>::config` → that member's `src/config.rs`. A module path covers the whole module
    file; an item path covers that item and its public members (fields, variants, methods, associated items).
- **No argument**: every non-test `.rs` file touched by uncommitted changes plus commits on the current branch not yet
  on the base branch:
  ```bash
  git status --porcelain
  git diff --name-only <base-branch>...HEAD -- '*.rs'
  git diff --name-only -- '*.rs'
  ```
  (base branch via `git symbolic-ref refs/remotes/origin/HEAD`, else `git branch -a`; ask only if genuinely
  ambiguous).
- Always drop `target/`, `tests/`, `benches/`, `examples/` (examples are documentation already), `build.rs`,
  generated files (`// @generated`, `include!`d `OUT_DIR` code) and anything git-ignored — name dropped arguments in the
  report. Empty scope → say there is nothing to document and stop.
- **What gets documented** (the audit set): what `missing_docs` checks — every item reachable from the crate's public
  API: the crate root (`//!` in `lib.rs`), public modules (`//!` at the top of the module file, or `///` on the
  `pub mod` line), and public structs, enums, **each variant**, **each `pub` field**, traits and their methods, `pub`
  functions and methods, `pub` consts/statics/type aliases and macros exported with `#[macro_export]`. Private items
  and `pub(crate)` items are out of scope unless the project documents them habitually (look at
  `--document-private-items` in CI) — never add docs to trait-impl methods (`impl Display for X { fn fmt … }`): they
  inherit the trait's docs.

## Step 2 — Discover this project's actual documentation bar

- **Lints**: `[lints.rust]` `missing_docs`, `[lints.rustdoc]` (`broken_intra_doc_links`, `missing_crate_level_docs`,
  `private_intra_doc_links`, `bare_urls`), `[lints.clippy]` (`pedantic` enables `missing_errors_doc`,
  `missing_panics_doc`, `doc_markdown`, `must_use_candidate`; `missing_safety_doc` is on by default) — in the root
  `Cargo.toml` or `[workspace.lints]` inherited with `lints.workspace = true`; also crate-level `#![warn(missing_docs)]`
  attributes. The project's `allow`s are part of the bar (e.g. `missing_panics_doc = "allow"`).
- **CI**: `RUSTDOCFLAGS: -D warnings` on `cargo doc` (this catalog's workflows set it), `--document-private-items`,
  `--all-features` (feature-gated items are documented only when their feature is on), `[package.metadata.docs.rs]`
  (`all-features`, `rustdoc-args = ["--cfg", "docsrs"]` with `#[cfg_attr(docsrs, doc(cfg(...)))]`).
- **House style** from 2–3 well-documented files near the scope and any contributor guide (`CLAUDE.md`, `AGENTS.md`,
  `CONTRIBUTING.md`): third-person summary ("Returns …", "Parses …" — the std/API-Guidelines style), whether
  `# Examples` is habitual, `?` in examples with a hidden `# Ok::<(), Error>(())` line, how errors are named in
  `# Errors`. Follow the **stricter** of stated vs observed.

**The convention** (rustdoc book + Rust API Guidelines, as used by this catalog's scaffolds):

- First paragraph = **one-sentence summary** ending in a period; it is what module listings and search show. Then a
  blank `///` line and optional detail. Markdown throughout; identifiers in backticks (`clippy::doc_markdown` flags
  bare `CamelCase`/`snake_case` words).
- **Intra-doc links** for every type, method or module named: ``[`Envelope`]``, ``[`Envelope::to_json`]``,
  ``[`crate::exit::ExitCode`]``, ``[`std::io::Error`]``; disambiguate with `struct@`/`fn@`/`macro@` when names collide.
  A link to a private item from public docs triggers `rustdoc::private_intra_doc_links` — link to something public or
  use plain backticks.
- **`# Errors`** — every `pub fn` returning `Result`: which error variants/kinds and when (``Returns
  [`CliError::Validation`] if `name` is empty or longer than 64 characters.``). Read the body for every `?`, `Err(..)`
  and `.map_err(..)`.
- **`# Panics`** — every `pub fn` that can panic (`unwrap`, `expect`, indexing, `assert!`, `unreachable!`, integer
  overflow in debug): the condition. If the panic is impossible by construction, prefer stating why in an internal
  comment and let the user decide — never invent a condition.
- **`# Safety`** — every `unsafe fn` / `unsafe trait`: the invariants the caller must uphold. (This catalog's CLI
  scaffold forbids `unsafe_code`, so this is rare.)
- **`# Examples`** — a runnable doctest on the main entry points of the library API (constructors, parsers, the
  command functions a CLI's `main` calls), using the crate's public path (`use democli::output::Envelope;`), with
  `?` + a hidden `# Ok::<(), democli::Error>(())` line instead of `unwrap()` where the API returns `Result`. Use
  ` ```no_run ` for examples that would touch the network/filesystem/terminal, ` ```ignore ` never (it hides rot), and
  ` ```text ` for shell sessions or output samples. Don't add examples to trivial getters.
- Crate root: `//!` in `lib.rs` with what the crate provides (for a CLI's library: "Library behind the `<bin>` command:
  …"); each public module: a `//!` line saying what it holds. Enum variants and struct fields get one-line `///`s.

## Step 3 — Audit each in-scope file

Run the doc lints for the whole workspace, forced on, and keep only in-scope findings (`-A` the rest so the output
stays about docs):

```bash
mkdir -p target
cargo clippy --workspace --all-targets --all-features --locked --message-format=json -- \
  -A clippy::all -A clippy::pedantic -W missing_docs -W clippy::missing_errors_doc -W clippy::missing_panics_doc \
  -W clippy::missing_safety_doc -W clippy::doc_markdown > target/iru-rust-rustdoc-lints.json 2>/dev/null
python3 - target/iru-rust-rustdoc-lints.json 'src/output.rs,src/commands/' <<'PY'
import json
import sys

scope = [s.rstrip("/") for s in sys.argv[2].split(",") if s]
seen = set()
for line in open(sys.argv[1]):
    if not line.startswith("{"):
        continue
    d = json.loads(line)
    if d.get("reason") != "compiler-message":
        continue
    m = d["message"]
    sp = [s for s in m["spans"] if s["is_primary"]]
    if not sp:
        continue
    key = ((m.get("code") or {}).get("code"), sp[0]["file_name"], sp[0]["line_start"])
    if key in seen or not any(key[1] == s or key[1].startswith(s + "/") for s in scope):
        continue
    seen.add(key)
    print(f"{key[1]}:{key[2]} {key[0]} — {m['message']}")
PY
```

(Drop `--locked` when the project has no `Cargo.lock`.) The `-W` flags apply to every workspace crate — including
members that don't inherit the lint table, such as `xtask` — which is why the scope filter matters. Findings name the
item's line: `missing_docs` ("missing documentation for a function/struct/the crate/a variant/a struct field"),
`clippy::missing_errors_doc`, `clippy::missing_panics_doc`, `clippy::missing_safety_doc`, `clippy::doc_markdown`.

Then **read each in-scope file** — lints only prove a doc exists, not that it's right — and for every item in Step 1's
audit set check that the summary actually describes it (not "Greet." for `greet`), that `# Errors` lists the errors
the body really returns (compare with every `?`/`Err`), that `# Panics` matches the panicking calls, that links
resolve to what's meant, and that the docs describe **current** behavior (`git diff`/`git log -p` for the file).
Record each gap: item, kind, what's missing (whole doc vs a section/link/example), file.

## Step 4 — Write the missing docs

Before editing, capture the Step 5 build's warnings once (baseline) so new warnings can be told from pre-existing ones.

For every gap, write the doc grounded in the implementation (what is returned and when, which errors/panics, side
effects such as writing to stdout/stderr, files, exit codes for a CLI's command functions) and in the convention from
Step 2, so new docs are indistinguishable from hand-written ones. Apply with the Edit tool: `///` immediately above the
item and above any `#[derive]`/attributes it has (attributes may sit between the doc and the item, but keep the
existing order); `//!` as the first lines of `lib.rs`/the module file, after a license header comment if there is
one. Do not modify code, signatures, attributes, `use` lines, or formatting outside the added docs, and don't reorder
items. Keep lines within the project's `max_width` (rustfmt doesn't wrap comments by default) — run nothing that
rewrites code; `cargo fmt` is not this skill's job.

## Step 5 — Verify

Write every output as `target/iru-rust-rustdoc-*` (`target/` is gitignored) and delete them at the end
(`rm -f target/iru-rust-rustdoc-*`).

1. **Doc lints** — re-run Step 3. Every finding in an in-scope file must be gone (one on an item this run didn't touch
   but that sits in an in-scope file is still a gap — fix it).
2. **rustdoc build, warnings as errors**:
   ```bash
   RUSTDOCFLAGS="-D warnings" cargo doc --workspace --no-deps --locked [--all-features] --message-format=json \
     > target/iru-rust-rustdoc-doc.json 2>/dev/null; echo "exit=$?"
   ```
   Exit `101` lists each warning-turned-error as a `compiler-message` (same parser as Step 3, without the clippy
   flags): `rustdoc::broken_intra_doc_links` ("unresolved link to `Nope`"), `rustdoc::private_intra_doc_links`,
   `rustdoc::bare_urls`, `rustdoc::invalid_codeblock_attributes`, `rustdoc::unescaped_backticks`, and the project's
   own `[lints]` (`missing_docs` is enforced by rustdoc too — verified). Mirror CI's flags (`--all-features`,
   `--document-private-items`, `--cfg docsrs` when `[package.metadata.docs.rs]` uses it). Add `-W
   rustdoc::missing_crate_level_docs` to `RUSTDOCFLAGS` when the scope includes a crate root.
3. **Doctests**:
   ```bash
   cargo test --workspace --locked --doc [--all-features] > target/iru-rust-rustdoc-doctest.log 2>&1
   ```
   Every example you wrote must compile and pass (`test src/output.rs - output::Envelope (line 12) ... ok`). A failing
   one is fixed in the doc, never by changing code. Packages without a library are skipped by cargo — say "no
   doctests for bin-only crate `<name>`". `compile_fail`/`should_panic` examples you add must state why in the prose.

Compare with the Step 4 baseline: any **new** warning or failure naming an in-scope file was caused by this run — fix
and re-run until none remain. Pre-existing problems outside the scope are follow-ups, not this skill's to fix.

## Step 6 — Report

Per file in scope: how many public items were already fully documented, the gaps found and filled (name each with its
kind and what was added — "`Envelope` struct: summary + 3 field docs", "`greet::run`: `# Errors` (2 variants) +
`# Examples`", "crate root: `//!` docs"), then the verification result — doc lints: clean or what remains; `cargo
doc` with `-D warnings`: pass, or the open warnings; doctests: N passed / which failed / "none (bin-only)". Name the
convention source, arguments dropped (tests, examples, generated), and pre-existing out-of-scope failures as
follow-ups. Never paste raw tool output or JSON.

Do not fix non-doc lints, change code to make a doc "true", edit `Cargo.toml` lint tables or CI, edit license
headers, or add/modify tests — those belong to `iru-rust-code-quality`, the coding skills, and the user.

## Verification notes

Verified on 2026-10-16 with Rust 1.99.1 stable (clippy 0.1.99), in `$TMPDIR/iru-verify/cli/rust-gates/` (outside this
repository) on a workspace with a `democli` lib + bin (`[lints.rust] missing_docs = "warn"`, `[lints.clippy] pedantic`)
and an `xtask` member:

- The Step 3 command reported `missing_docs` for an undocumented `pub fn` (`src/lib.rs:23`) and for the bin crate root
  (`src/main.rs:1` — `[lints]` applies to bins too), `clippy::missing_errors_doc` for a `Result`-returning fn and
  `clippy::missing_panics_doc` for a fn calling `unwrap()`; the `-W missing_docs` flag also hit `xtask/src/main.rs`,
  removed by the scope filter.
- `RUSTDOCFLAGS="-D warnings" cargo doc --workspace --no-deps --message-format=json` exited `101` with
  `rustdoc::broken_intra_doc_links` ("unresolved link to `Nope`") and `missing_docs` as `error`-level messages; without
  `-D warnings` the same two were warnings.
- After adding a summary + `# Examples` doctest, an `# Errors` section with an intra-doc link to
  ``[`std::num::ParseIntError`]``, a `# Panics` section and the bin's `//!` line, the lints came back empty, `cargo doc`
  exited `0`, and `cargo test --doc` ran 2 doctests, both passing.
- On a bin-only crate `cargo test --doc` exited `101` (`no library targets found in package`) and a deliberately
  failing example in `main.rs` was never compiled by `cargo test`.
- Not verified: `--document-private-items` workspaces, `doc(cfg)` with `--cfg docsrs` (nightly feature), scraped
  examples (nightly), and macro-generated items.

## Sources

- irurueta docs: programming-languages/rust/documentation-with-rustdoc.adoc (`///` vs `//!`, one-sentence summary,
  `# Examples`/`# Errors`/`# Panics`/`# Safety`, intra-doc links, doctest attributes, rustdoc lints, `RUSTDOCFLAGS="-D
  warnings" cargo doc --no-deps`)
- irurueta docs: programming-languages/rust/testing-and-benchmarking.adoc (doctests run by `cargo test`, combined
  doctests in edition 2024, bin-only crates can't be imported — logic in `lib.rs`)
- irurueta docs: programming-languages/rust/tooling-clippy-rustfmt-and-rust-analyzer.adoc (`[lints]` table, pedantic
  doc lints)
- The rustdoc book; Rust API Guidelines: Documentation (C-CRATE-DOC, C-EXAMPLE, C-FAILURE, C-LINK)
