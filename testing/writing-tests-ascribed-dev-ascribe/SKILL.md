---
name: writing-tests
description: "How Ascribe's tests are laid out, where a new test of each kind goes, which fixture helpers to build it from, and what keeps it fast. Use it whenever you add, change, move, or debug a test in this repository, decide which layer should prove a behavior, hit a stale snapshot or generated file, notice a slow test, or are asked to review test coverage, even if the request only says 'add a test for this'."
---

# Writing tests in Ascribe

Ascribe has about 1,900 Rust tests and 1,000 JS tests, and nearly every one holds a spec rule, an output contract, a fixed bug, an agreement between two implementations, or a repository invariant. The file-level doc comment says which, and the test's name is a sentence stating the fact held. Keep both: they're how the suite stays reviewable by listing it, and how a reader knows what a failure means.

This skill is about where a test goes and how to make it good and fast. The rules every change follows are in [AGENTS.md](../../../AGENTS.md); the map of the crates and the test tables are in [ARCHITECTURE.md](../../../ARCHITECTURE.md#tests). Read those sections first if you haven't.

## The layers, and what each proves

Each layer tests something the one below can't. Put a test where its fact lives, and don't repeat it in the layers above unless they add something (the binary agreeing with the library does; the same assertion twice doesn't).

| Layer | Where | What it proves | Add one when |
|---|---|---|---|
| Conformance cases | `tests/conformance/cases/<area>/<case>/` with `expect.yaml` | The spec, written by hand from SPEC.md, against the real parser, checker, resolver, and formatter through adapters | A behavior change, always (AGENTS.md). A new diagnostic's row in `diagnostics.toml` must have a case: `tests/conformance/tests/suite.rs` checks |
| Crate integration tests | `crates/<crate>/tests/all/<file>.rs`, one program per crate (`tests/all.rs`) | A library entry point's behavior on projects built in memory: edges, invariants, the shape of what it returns | The rule's edges, beyond the spec's example; anything about the returned data a case can't express |
| Unit tests | `#[cfg(test)]` in `src/` | A private function's contract (a parser step, an encoder, a comparison) | The function is small, pure, and its edges are many |
| CLI tests | `crates/ascribe-cli/tests/all/` | What a user sees from the binary: exit codes, standard streams, JSON shapes, output replacement, temp repositories | Only what the binary shows. A library behavior belongs in the library's tests |
| Language server tests | `crates/ascribe-lsp/tests/all/` | Requests and notifications over an in-memory connection, scripted | A request, a capability, incremental behavior under edits |
| Agreement tests | `agreement.rs`, `incremental_differential.rs`, `differential.rs`, `reach.rs`, `parity.rs`, `lsp_parity.rs`, `build_view_parity.rs`, `tests/render/`, the extension's `test:parity` | Two implementations, or a short path and the full one, give the same answer | You add a case the two must agree on. Extend the vocabulary; don't write a parallel test |
| Repository invariants | `names.rs`, `registry.rs`, `file_reads.rs`, `network.rs`, `fork_md.rs`, `scripts/repo-docs`, `scripts/docs-site/facts.test.ts`, `scripts/design/tokens.test.ts` | The rules in AGENTS.md hold: one home per fact, reads through `FileSystem`, no network, generated files current, docs' paths exist | A new rule of that kind. These grep source and are cheap |
| JS package tests | `packages/<pkg>/test/`, vitest | Each package against its contract (`packages/elements/CONTRACT.md`, the render fixtures, the JSON shapes) | A package behavior. Browser tests only for what needs a browser |
| CI-only suites | `packages/vscode/test/integration/` (real VS Code), `examples/astro-site/test/e2e/` (Playwright), `site/test/` | The whole thing, end to end | Rarely; they're slow and run only in CI |

The conformance suite's format and adapters are in [tests/conformance/README.md](../../../tests/conformance/README.md). A case that uses a tag no adapter handles fails, so skips are always deliberate.

## Where a kind of change is tested

- **A new or changed diagnostic:** its entry in `crates/ascribe-core/data/diagnostics.toml`, which generates its slug constant; a conformance case that expects the slug; a `[[diagnostic]].example` with a wrong page and a right page, which `crates/ascribe-query/tests/explain_examples.rs` runs; the file-level or page-level check's own test in `crates/ascribe-check/tests/all/`; and the generated reference, rewritten with `ASCRIBE_BLESS=1`.
- **The site output's markup:** a fixture in `tests/render/` (both renderers run them: `crates/ascribe-emit/tests/all/render_fixtures.rs` and `packages/astro/test/render-fixtures.test.ts`), the element contract if a name or attribute is new, `ascribe_core::names` for the name, and the Quill snapshots in `crates/ascribe-emit/tests/all/snapshots/`.
- **The plain or JSON output:** `crates/ascribe-emit/tests/all/plain.rs` or the JSON assertions in `quill.rs`, construct by construct, and the snapshots.
- **A command's output or JSON:** the command's file in `crates/ascribe-cli/tests/all/`, the JSON Schema (`crates/ascribe-cli/src/shapes.rs`, blessed), and `tests/output.rs`'s fixtures if the docs show the output.
- **A server request:** a scenario over `support::Client` in `crates/ascribe-lsp/tests/all/`, and `lsp_parity.rs` if the request reports diagnostics the CLI also reports.
- **Incremental updates:** add to the vocabulary in `crates/ascribe-resolve/tests/incremental_support/` so the differential tests exercise it. Don't write a second incremental test by hand; the property test is the proof.
- **The content model:** a failing fixture per loading rule in `crates/ascribe-model/tests/rules.rs` (every `model-` diagnostic must have one), and `load.rs` for the example models.
- **A formatter rule:** a conformance case under `format/`, and the rule's group in `crates/ascribe-fmt/tests/all/rules.rs`; idempotence over every input is already proved by `inputs.rs` and `fuzz.rs`, and the nightly `format` fuzz target (`fuzz/`, CONTRIBUTING.md) feeds it arbitrary text. A crash a fuzz target finds is fixed with a test of its input in the crate's own tests.

## Fixtures: build on what's there

Each crate's `tests/support/` builds projects in memory; reach for it before a temp directory, and a temp directory before a process. The helpers, by crate:

- **ascribe-resolve:** `support::project(&[(path, text)])` on a shared `MODEL`; `build_support::project`, `project_with(model, files)`, `resolve(project, page, build)`, `published`, `summary` for resolved pages; `incremental_support` for worlds that change step by step.
- **ascribe-check:** each file has its own `project(&[(path, text)])` over `MemoryFs`; `prompt.rs` and `page.rs` show the two shapes. `tests/all/commands.rs` uses a temp directory because it tests locating `ascribe.toml`.
- **ascribe-emit:** `support::memory_project(model, files)`, `plain(project, build, page)`, `site(...)`, `html_tree` and `first_difference` to compare rendered HTML as a tree, not as text; `support::quill()` and `load(root)` for the example on disk.
- **ascribe-diff:** `compare.rs` and `html.rs` build both versions in memory (`version(model, files)`); only `git.rs`, `drift.rs`, and `command.rs` make repositories, because they test reading one.
- **ascribe-lsp:** `support::Fixture::new(model, files)` writes a project to a temp directory; `Client::start(root)` is a scripted client over an in-memory connection (`open`, `change`, `request`, `settle`, `diagnostics`, `shutdown`). One client per thread is fine.
- **ascribe-syntax and ascribe-fmt:** `support::check_tree` proves every span covers its text; `fmt`'s `outline` compares documents ignoring formatting.
- **Links on every platform:** `tests/support/links.rs`, included with `#[path]`; `file` returns `false` where a link can't be made, and the test leaves that part out.
- **CLI:** each file has `project(files) -> TempDir`, `ascribe(dir, args) -> Output` (the binary from `CARGO_BIN_EXE_ascribe`), and where it needs history, `git(dir, args)` with a fixed author and date so commits are the same on every run.
- **JS:** `packages/review/test/helpers/repo.ts` (`tempRepo`, one per file in `beforeAll` unless a test checks out), `helpers/github.ts` (`FakeGitHub`, `thread`, `comment`, `review`), `helpers/fake-gh.ts` (a fake `gh` on PATH); `packages/elements/test/harness.ts` (`ENGINES`, `launch`, `open`); `packages/astro/test/html.ts` (`firstDifference`).

Nothing in a test reaches the network: code repositories are reached by `file://` URLs, and `crates/ascribe-cli/tests/all/network.rs` fails on a crate that could.

## Reproduce before you test

A reported behavior is a claim; check it before deciding what to prove, since the test you'd write for a bug that isn't there is a test of nothing. The quickest routes, in order:

- **The library, from a test's support module:** `support::fmt(source)` and `support::outline(source, options)` in `ascribe-fmt`, `ascribe_syntax::parse` with `support::check_tree` in `ascribe-syntax`, `build_support::resolve` and `summary` in `ascribe-resolve`, `support::plain` and `site` in `ascribe-emit`. A temporary `#[test]` with `eprintln!`, run with `-- --nocapture`, and deleted once you've seen the answer.
- **The binary on a scratch copy:** `cargo build -p ascribe-cli`, then `target/debug/ascribe check`, `fmt --check`, `resolve`, or `outline` on a copy of an example under `examples/`; `ascribe resolve --build <name> <page>` shows a page as a build publishes it.
- **The conformance cases:** `tests/conformance/cases/<area>/` often already holds the exact input; `cargo test -p ascribe-conformance --test conformance -- <case id>` runs one.

Then say in your report what the behavior is, where it's already held, and what was missing, before what you added.

## Writing one well

- **Name the fact.** `a_link_to_a_page_the_build_drops_is_recorded_and_left_unresolved`, not `test_links`. If you can't write the name as a sentence, you don't yet know what the test holds.
- **Say what the file covers** in its `//!` comment, including which spec section, and what the layers above or below already cover so a reader doesn't look for it here.
- **One fact per test, several assertions if they're the same fact.** A failure message should say what's wrong and show the input (`"{what} adds {key:?}:\n{after}"`).
- **Assert on structure, not on text that isn't a contract.** Prompt wording, help text, and log lines change freely (decision 54); the cut at a block, the cap, and the exit code don't. A snapshot of non-contract text costs a review every time the wording moves and proves nothing a structural assertion wouldn't.
- **Snapshots are for contracts.** The Quill pages under each build, the command output the docs show, the generated schemas. Review every change with `cargo insta review`; never accept blindly. insta keeps a snapshot beside the asserting file, named by module path: `tests/all/snapshots/all__<file>__<test>.snap`.
- **No timing assertions.** A debug build on a loaded runner fails them for reasons that aren't the code. Print timings with `eprintln!` if they're informative; the benchmarks in `tests/corpora/` hold performance, with a margin.
- **Paths differ by platform.** Compare paths through `ascribe_core::path`, make links through `tests/support/links.rs`, and don't assume case-sensitivity either way. A test that must skip on Windows says why with `skipIf` or a comment.
- **A test that found a bug keeps the bug's shape.** Minimal input, the exact wrong output it used to give, named for the fact rather than the issue number.

## Keeping it fast

The suite's time is concentrated, and each of these was once the slowest thing in it:

- **Don't check the whole project per iteration.** A full `check_project` of a small example is 30 ms in debug; thousands of them are a minute. Check what a change can reach: the edited file's file-level diagnostics and the page-level diagnostics of the pages it's part of, which is what the incremental index recomputes (`Affected::recheck`). `crates/ascribe-lsp/tests/all/edit_examples.rs` shows the shape, and how to run a loop across pages in parallel with one client per thread.
- **One program per crate.** A new test file goes under `tests/all/` with a `#[path = "all/<file>.rs"] mod <file>;` line in `tests/all.rs`, not beside it in `tests/`: every file in `tests/` is a separate binary, a separate link, and a separate process. `determinism.rs` is the one exception, because CI runs it alone. Run one file's tests with `cargo test -p <crate> --test all <file>::` (the `::` keeps a substring filter to that file).
- **Property tests take the shared budget.** Use `ProptestConfig::default()` (plus `max_shrink_iters` or `failure_persistence` if you need them) and let `PROPTEST_CASES` in `.cargo/config.toml` set the count; raise it in the environment for a soak. A "never panics" test finds what it will find in a few hundred cases; a differential test is worth more, and the soak is how it gets them.
- **Share fixtures per file.** A git repository per test is a few hundred milliseconds each; one in `beforeAll` or a `static` is one. Keep a per-test repository only when the test commits or checks out.
- **Build once.** A global setup that runs `tsc` or `esbuild` skips the build when `dist/` is newer than its sources (`packages/elements/test/global-setup.ts`). Don't add a build step to a test that can read the committed output.
- **Browsers are for what needs them.** The element library runs Chromium alone locally and all three engines under `CI` (`ASCRIBE_ENGINES` chooses). A DOM question that doesn't need layout belongs in a vitest test, not a browser.
- **The corpus and the 3,000-page project are release-only.** Mark a test on them `#[ignore = "slow in debug builds; run with --release -- --ignored"]`; the weekly workflow runs them.

Measure before and after:

```sh
# Per-test times in one program (libtest's unstable flag, fine for measuring)
RUSTC_BOOTSTRAP=1 cargo test -p ascribe-lsp --test all -- -Zunstable-options --report-time
# Per-file times for a JS package
corepack pnpm --filter @ascribed/review exec vitest run --reporter=verbose
```

A test that takes more than a few seconds in debug needs a reason in its doc comment, or a change.

## Generated files and blessing

Some tests write the file they check when run with `ASCRIBE_BLESS=1`: the diagnostics reference, each command's options and JSON Schemas, the command output the docs show, what `agents sync` writes, the names each package imports, the render fixtures' inputs, the Zod fixtures, the extension's settings and commands, the design specimen and tokens. The table of which test rewrites what is in [ARCHITECTURE.md](../../../ARCHITECTURE.md#ascribe_bless1); run the one named, or `pnpm bless` to run all of them in order, then read the diff before committing it. A generated file is never edited by hand.

## Before you finish

- `cargo fmt --all --check`, `cargo clippy --workspace --all-targets --locked -- -D warnings`, `cargo test --workspace --locked`, and the JS set from CONTRIBUTING.md. Test files allow `unwrap`, `expect`, and `panic!` with `#![allow(...)]` at the top; keep that line when you add a file.
- Moved or renamed a test file? `scripts/repo-docs/paths.test.ts` fails on any doc that still names the old path: `corepack pnpm vitest run scripts/repo-docs`.
- Changed what a test proves? Its doc comment and the crate's README's test list say what it covers; update them.
- A behavior change has its conformance case, and its page under `docs/content/` and changelog entry in `changes/`, per AGENTS.md. A test-only change has neither, and changes no output: `node scripts/compare/outputs.ts --base main` shows it.
