---
name: rust-code-review
description: Review Rust changes on two axes at once — standards (idioms, ownership, errors, API surface, unsafe) and spec (does the change do what was asked) — with a Rust smell baseline layered on the repo lint configuration. Use when reviewing a Rust diff, pull request, or branch, when asked whether a change is ready to merge, or when a review needs to cover more than what clippy already reports. Also use for an audit or critique of a Rust file or crate, or when asked what is wrong with some Rust.
---

# Rust Code Review

A review is a statement about what a change owes — to the request that asked
for it, and to the standards the repo already lives by. This skill runs both
statements as separate passes and merges them into one report led by a
verdict. It never restates a rule a smell maps to: the craft skills and
`/rust-testing` own the standards, and the review routes to them.

## Two axes, run separately

A single reviewer reading for both correctness-against-the-request and craft
does neither well: spec drift hides behind clean-looking code, and style nits
crowd out the missing edge case. Run a **standards pass** and a **spec pass**
as separate passes — as parallel sub-agents when the harness supports it,
sequentially when it does not — then merge. The prompts for both, the merge
rules, and the report shape are in `REVIEW-PASSES.md`.

## Fix the scope before reading

Settle three things and print them at the head of the report, so the author
can correct a wrong assumption before reaching a finding:

- **Subject.** For a diff: the lines that changed, plus any code those changes
  break, but not the untouched remainder of the file. For a file, module, or
  crate: that unit and nothing wider.
- **Library or application.** A `lib.rs`, `pub` items other crates use, or a
  published manifest means library. A library is held to the API bar strictly;
  an application gets the simplicity bar instead — concrete types, a catch-all
  error type, no speculative generality. Say which one was assumed.
- **Edition and MSRV**, taken from `Cargo.toml`, so that no recommendation
  depends on a toolchain newer than the one the project builds with.

## The machine goes first

Before either pass reads a line, run the verification step below and read the
output. Anything clippy already reports is not a review finding; it is a build
failure someone forgot to run. Put the tool output in the report grouped by
cause — eight hits of one lint make one line, not eight — and say what ran
and what could not. Reviewer attention is for what the tools cannot see: the
judgment call, the missing edge case, the scope that crept in.

## Read the repo lint configuration before judging style

`[lints.clippy]` in `Cargo.toml`, a `clippy.toml`, a `rustfmt.toml`,
`#![deny(...)]` in the crate root. A finding that contradicts a level the repo
deliberately set is not a finding — it is a proposal, and it says so
explicitly. Never override the configured level, and never re-run at a
stricter one and report the extra hits as defects. Pedantic output is
proposals only, and only the ones that matter for this code, unless the repo
itself opted into pedantic. The smell baseline layers on top of this
configuration, never in place of it — a finding that the repo lint config
already permits is a finding about the config, raised separately.

## Priority order of what to read for

Spend attention in this order, and never let a lower tier crowd out a higher
one:

1. **Correctness and soundness** — undefined behaviour, reachable panics
   (indexing, narrowing casts, overflow), trait-contract hazards that corrupt
   collections, lock hazards, destructors that can fail.
2. **Error handling** — what callers can match on, what context survives.
3. **API design** — strict for a library, relaxed for an application.
4. **Idiom and clarity.**
5. **Docs and tests.**

The concrete smells for each tier, with the owning skill, are in `SMELLS.md`.

## The smell baseline

What this skill adds beyond clippy: the judgment calls no lint can make. The
full table — the smell, how it shows up in a diff, why it is a defect, and the
owning skill — is `SMELLS.md`. The top ones:

- an unexplained `clone` at the call site — `/ownership-not-clone`
- `unwrap` or `expect` on a path a caller controls — `/rust-errors`
- `pub` on an item with no external caller — `/rust-api-design`
- a boolean or stringly-typed parameter that should be an enum —
  `/type-driven-design`
- blocking work inside an async function — `/async-rust`
- an `unsafe` block with no `// SAFETY:` comment — `/unsafe-rust`
- a behaviour change with no test that would have caught it — `/rust-testing`

An `#[allow(lint)]` that outlived its reason is invisible and permanent.
`#[expect(lint, reason = "...")]` fails once the situation it was written for
goes away, which turns a silenced lint into one that reports itself when it
becomes stale. In review, an `#[allow]` with no reason is a finding; with a
reason it is a conversation. `#[expect]` and the `reason` key need Rust 1.81
or later; in a crate with an earlier MSRV, use `#[allow]` with a `//` comment
explaining why.

## Severity, and saying nothing

Three levels only: **blocking** (wrong behaviour, unsound, a reachable panic on
outside input, breaks the public API without a version bump, or an API choice
that turns into a semver break after release), **should-fix** (a real defect the
author would want to know about), **note** (a genuine improvement the author may decline).
Anything below that threshold is dropped rather than written down — a review
of forty nits and one soundness bug buries the soundness bug. No
praise-padding, and no restating the diff back to the author. The one
exception is the short keep list in the long report form, described in
`REPORT-FORMAT.md`.

## Finding format

Two shapes. The default, for a diff or a short review, is one line each, most
severe first: `path:line — severity: what is wrong. What
to do instead.`

```
src/cache.rs:41 — blocking: guard held across .await; drop it before the fetch.
src/parse.rs:8 — should-fix: unwrap on caller input; return the ParseError instead.
src/lib.rs:102 — note: this fn takes String where &str would do.
```

A finding with no concrete fix is a question, and is phrased as one.

For a file, crate, or audit-style review, or when the user asks for a report,
use the long block instead: location, standard, consequence, and the
minimal edit that fixes it. Both shapes, the report skeleton, and the
closing are in `REPORT-FORMAT.md`.

Rules that hold in both shapes:

- Cite a location — `path:line`, or "whole file" when there is no single line.
- Name a rule a reader can look up: a clippy lint name, or the owning skill of
  this repo.
- Group repeats into one finding listing the lines.
- Respect visible intent: a documented quirk or a commented choice becomes a
  note stating the trade-off, never a blocker.
- Stay proportionate: five to ten findings for a short file, and a real bug is
  never buried among nits.

## What this skill does not do

It does not rewrite the code — findings, not patches, unless the author asks —
and it never runs `cargo fmt` on reviewed code; `--check` only.
It does not review a diff it cannot build: a check that cannot run is named in
the report, not papered over. It does not decide the parity contract of a
port; that is `/port-to-rust`.

## Verification

Run before reporting, and quote the results in the report:

```bash
cargo fmt --check
cargo clippy --all-targets --all-features   # at the repo configured level; add -- -D warnings only if there is no lint config
cargo test --all-features
```

If any of the three cannot run — no network for dependencies, no nightly for a
required component, a file with no manifest around it — the report says which
check did not run rather than implying a clean bill. For a loose file, copying
it into a scratch crate to run the tools is fine; the original stays untouched.

## Closing

If the repo has no lint configuration at all, end the report by suggesting
`/setup-rust-skills`, and cite two or three items in this report that the
lints it installs would have flagged.
