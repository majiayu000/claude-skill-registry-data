---
name: setup-rust-skills
description: Configure a Rust repo for this skill set — lint and format configuration, and a recorded project posture (edition, MSRV, async runtime, no_std, unsafe policy) at docs/agents/rust.md.
disable-model-invocation: true
---

# Setup Rust Skills

Configuration is a promise the tooling keeps. Every other skill in this set
reads the lint level and the recorded posture before running a verification
step, and this skill is the one that writes both. It runs only when the user
invokes it — it drops files into the repo, and the model never decides that on
its own. The whole run is governed by one rule: **read before writing, and
never overwrite a deliberate setting.**

## What this writes, and the one rule

Three artifacts (plus, for a new crate or on request, the project-shape
decisions in `WORKSPACE.md`): the lint configuration — the levels in `Cargo.toml` and the
knobs in `clippy.toml` — a `rustfmt.toml`, and `docs/agents/rust.md`. If an
artifact already exists, the change is presented as a diff for approval;
existing keys are left alone unless the user says otherwise, and only missing
keys are added.

## Detect first, ask second

Read `Cargo.toml`, the crate root, and `rust-toolchain.toml`. Ask only about
what could not be detected, and ask in one batch rather than one question at
a time. The five facts to end up with:

| Fact | Usually detected from |
|---|---|
| Edition | `[package].edition` or `[workspace.package].edition` |
| MSRV | `rust-version`, `clippy.toml` `msrv`, or the CI job that builds on the oldest compiler |
| Async runtime | `tokio`, `async-std`, or `smol` in the dependencies — or none |
| `no_std` posture | `#![no_std]` at the crate root |
| Unsafe policy | `#![forbid(unsafe_code)]`, an existing `unsafe_code` level, or the absence of one |

The unsafe policy lands as one of three: forbidden, allowed with review, or
unrestricted. When nothing in the repo settles it, that is the one question
worth asking.

## Where lint levels actually go

`clippy.toml` cannot set lint levels — it holds the configurable-lint knobs:
`msrv`, thresholds such as `max-fn-params-bools`, and the test carve-outs for
`unwrap_used`, `expect_used`, and printing. Levels belong in `[lints.rust]` and `[lints.clippy]` in
`Cargo.toml`, or — for a workspace — in `[workspace.lints]` at the root plus
`lints.workspace = true` in each member. Write each file for its own purpose:
a level in `clippy.toml` compiles fine and does nothing, which is worse than
an error. Confirm against the installed toolchain rather than assuming —
`cargo clippy -- --help` settles which lints exist, and the `[lints]` block
in the repo `Cargo.toml` settles where the levels already live. The full
worked configuration is in `TEMPLATES.md`.

## The tools worth having configured

| Tool | Answers |
|---|---|
| `cargo audit` | does any dependency have a published advisory |
| `cargo hack --feature-powerset check` | does every feature combination compile, or only the one CI happens to build |
| `cargo udeps` | which declared dependencies are not used |
| `cargo miri test` | does the unsafe code hit undefined behaviour under an interpreter |

Propose, do not install: `cargo hack` and `cargo udeps` go in a scheduled job,
`miri` only where a crate has `unsafe`; the posture file records the answer
either way.

`cargo hack` earns its slot because each independent feature doubles the
number of configurations, so the one CI happens to build is a small fraction
of what users can select. The check only passes when features are additive:
any combination compiles, and turning a feature on only adds to the public
API, never taking away or altering something already exported. A crate that needs a `std` switch names the feature `std`, never
`no-std`.

Beyond those four, know the everyday cargo subcommands and name them in the
posture file when a repo leans on them: `check` for a fast type-only pass,
`doc`, `bench`, `update`, `tree` for why a dependency is present, and
`metadata` for scripts that need the workspace shape. `cargo expand`,
`cargo deny`, and `cargo semver-checks` are further opt-ins. Suggest
`rust-analyzer` for the editor: it surfaces type and lint feedback while code
is written. A division of labour holds the whole toolset together — wire a
tool into CI when its signal is worth a red build, and put it in the editor
(or a commit hook) when it is fast and has no false positives.

## A defensible default set, proposed not imposed

Present the set with a one-line reason per entry and let the user cut it — a
set the user did not agree to is a set they will disable in a week:

| Level | Lint | Why |
|---|---|---|
| deny | `unsafe_op_in_unsafe_fn` | an implicit `unsafe` inside an `unsafe fn` hides the invariant the caller must uphold |
| deny | `clippy::undocumented_unsafe_blocks` | every `unsafe` block needs a written `// SAFETY:` invariant |
| deny | `clippy::missing_safety_doc` | every `pub unsafe fn` needs a `# Safety` doc section |
| deny | `clippy::unwrap_used` | a panic in production code is a design decision — the test carve-out keeps it as the assertion in tests |
| deny | `clippy::expect_used` | the same rule, for the variant with a message |
| deny | `clippy::allow_attributes_without_reason` | an `allow` with no reason is a silenced lint nobody can re-evaluate |
| deny | `clippy::map_err_ignore` | a `map_err` closure that ignores its argument throws away the source error, which whoever debugs the failure needed |
| deny | `clippy::multiple_unsafe_ops_per_block` | a single unsafe operation per block lets each `// SAFETY:` comment justify exactly one thing |
| warn | `clippy::allow_attributes` | pushes every suppression toward `#[expect]`; needs MSRV 1.81 or later, so propose it only when the detected MSRV allows |
| warn | `clippy::pedantic`, as a group | worth a look, not a blocker; the group level leaves room to re-allow the noisy members |
| warn | `clippy::fn_params_excessive_bools`, `clippy::struct_excessive_bools` | a `true` or `false` argument says nothing where it is passed, and it leaves no room for a third option; use an enum or two methods |
| warn | `clippy::clone_on_ref_ptr` | `Rc::clone(&x)` makes a cheap clone visibly cheap |
| warn | `clippy::redundant_clone` | cloning a value that is never touched afterwards pays for a copy nobody needs |
| warn | `clippy::rc_buffer` | `Rc<String>` and `Rc<Vec<T>>` should be `Rc<str>` and `Rc<[T]>` |
| warn | `clippy::as_conversions` | a bare `as` hides intent; prefer `From` or `TryFrom` |
| warn | `clippy::cast_possible_truncation`, `clippy::cast_sign_loss` | numeric casts that can drop high bits or discard a sign without a trace |
| warn | `clippy::missing_assert_message` | an `assert!` should carry a message that explains the failure; the lint stays silent inside tests |
| warn | `clippy::string_add` | `+` on a `String` hides an allocation; use `format!` or `push_str` |
| warn | `clippy::wildcard_imports` | glob imports hide where a name came from; `use super::*` in a test module is allowed |
| warn | `clippy::dbg_macro`, `clippy::todo` | leftovers that should not reach a commit |
| warn | `clippy::panic_in_result_fn` | a function that returns `Result` should return the failure, not panic |
| warn | `missing_docs` [lib] | the public surface should document itself |
| warn | `clippy::exhaustive_enums` [lib] | exported enums should be `#[non_exhaustive]` so adding a variant is not a breaking change |
| warn | `clippy::print_stdout`, `clippy::print_stderr` [lib] | a library logs or returns; it does not print |
| warn | `clippy::missing_panics_doc`, `clippy::missing_errors_doc` [lib] | reachable panics and failures belong under `# Panics` and `# Errors` |
| warn | `missing_debug_implementations` | a public type with no `Debug` is a type nobody can print in a bug report |
| warn | `unreachable_pub` | a `pub` item not reachable from the crate root is either a mistake or should be `pub(crate)` |
| warn | `rust_2018_idioms`, as a group | catches `dyn`-less trait objects and anonymous lifetimes left behind by older code; `priority = -1` |

Rows tagged [lib] only fit a library. Choose the variant from what detection
finds: a `src/lib.rs`, a `[lib]` target, or a package intended for publishing
means the library variant; a binary-only crate gets the application variant,
which drops every [lib] row. A workspace gets the [lib] rows in the library
members only, as `missing_docs` already is. The `clippy::pedantic` group
entry is enabled only when the user keeps it, and then these members are
re-allowed as noise, each with its reason: `module_name_repetitions` (the module
path is already visible where the type is used), `must_use_candidate` (it
suggests `#[must_use]` far more often than a reviewer would), `module_inception`
(a module such as `parser::parser` holding the main item is acceptable), and
`enum_glob_use` (a glob import of variants inside the one function that
matches on them stays readable).

Gate on detection, and never override. Every row is proposed only when the
repo has not already set that lint; an existing level is left exactly as it
is, in either direction. The MSRV gate covers `clippy::allow_attributes` and
`clippy::allow_attributes_without_reason`: both need 1.81, so with an older
or unknown MSRV they are omitted and the run says so. Verify each name against
the installed toolchain before writing it, since a renamed lint is a warning
nobody reads.

One house stance is a choice, not a fact. The default denies
`clippy::expect_used`, so a panic needs a deliberate suppression with a
reason. A repo can prefer the opposite: unwrap is banned, and `expect` with a
message is the sanctioned panic. That repo sets `expect_used = "allow"`
(with `unwrap_used` still denied), and when detection finds that level the
skill honours it, as it does any other deliberate setting, and does not
propose the deny back.

Two boundaries on the set: never enable the whole `restriction` group — these
individual lints are the selection — and the `pedantic` entry carries
`priority = -1`, which is what lets individual members be re-allowed
afterwards. `missing_docs` stays out of the set for a binary crate.

Prefer `#[expect(lint, reason = "...")]` over `#[allow(lint)]` where the
toolchain supports it, because `expect` fails when the situation it was
written for goes away, and an `allow` that outlived its reason is invisible.
`#[allow]` is for two places only: generated code and macro output, where the
expansion cannot know whether the lint will fire.

The goal is a build with zero warnings, and the order of response to a lint
is fixed: fix the code first; only where the lint is genuinely wrong for this
site, suppress it narrowly — one item, with a reason — never module-wide or
crate-wide. Never write `#![deny(warnings)]` in source. A new toolchain adds
lints, so the build breaks after an upgrade nobody asked for, and the blanket
deny also blocks extra lint tools from running at their own levels. Deny the
specific lints that matter, by name, in the lint block; where a whole-build
failure on any warning is wanted, that belongs in CI, and only as the
fallback described in `setup-rust-ci`.

Two further levers. Clippy groups other than `pedantic` — `cargo`,
`suspicious`, `complexity`, `perf`, `style`, `correctness` — are enabled the
same way, as a group at `priority = -1` so individual members can be
re-allowed; the defaults already cover most of them, so list a group only
when raising it above its default. And read the full clippy lint list once,
default-off lints included, because the list teaches idiom: a default-off
lint that fits the repo gets offered with a reason, as part of the set the
user can cut.

## Project shape the setup also settles

A new crate gets a few creation-time decisions that are cheap now and costly
later; for an existing repo these are detected and recorded, never changed
without an approved diff. Workspace layout, dependency sharing, edition, MSRV,
toolchain pinning, and the out-of-box build rule are in `WORKSPACE.md`. The
short form: latest stable edition and an MSRV at creation, one flat
workspace, no unstable features, and a build that needs only `cargo` and
`rustc`.

## Formatting is rustfmt's job

Formatting is not a review topic: run the formatter and accept its output,
and do not hand-format in a way it will undo. The `rustfmt.toml` stays small,
and each key must carry a reason. `#[rustfmt::skip]` is allowed in exactly two
cases — a table or matrix whose manual alignment carries meaning, and
generated code — and never for personal style; put it on the smallest item
and say why in a comment beside it. The keys, stable and nightly, are in
`TEMPLATES.md`.

## `docs/agents/rust.md` is the point

The lint files configure the compiler; this file configures every agent that
opens the repo afterwards. It records the five detected facts plus the things
that would otherwise be rediscovered wrongly — the test command, whether
`--all-features` is meaningful for the feature set, which of the four tools
the repo runs, and which crates form the public surface. It is what this set
means by "the repo recorded posture": the file wins over any skill default.
Keep it short enough to be read in full every session — a page nobody reads
changes nothing. The full template is in `TEMPLATES.md`.

## Idempotence, stated as behaviour

Re-running reports one of three outcomes per artifact: created, updated with
an approved diff, or already correct and left alone. Never "regenerated" —
regeneration implies a rewrite, and a rewrite of a file the user already
approved is a change nobody asked for.

## Verification

After writing:

```bash
cargo fmt --check          # expected to fail loudly if rustfmt.toml changed the house style; report, do not auto-format the repo
cargo clippy --all-targets # now at the level just configured
cargo test
```

If the new set turns a clean build red, report it with the count and top
offenders — do not quietly lower the level just written.
