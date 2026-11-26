---
name: setup-rust-ci
description: Write a GitHub Actions workflow for a Rust repo — format, clippy at the configured level, tests, and an MSRV job, derived from the posture the repo already recorded.
disable-model-invocation: true
---

# Setup Rust CI

CI is a promise the tooling keeps in public. The workflow this skill writes runs
on every push and pull request, and the first thing a contributor learns about
the repo is the tick or the cross. It runs only when the user invokes it — a
workflow executes on someone's behalf, and the model never decides that on its
own. The whole run is governed by one rule: **read the recorded posture first,
and make CI say exactly what the local tooling says.**

## What this writes, and the one rule

One workflow file, `.github/workflows/rust.yml`, plus a line in the contributing
notes the repo keeps, if it has them. The rule: **the CI job runs the same
commands the skills run locally, at the same level, or CI is lying.** A workflow
whose clippy invocation is stricter than the repo `[lints]` block produces
failures nobody can reproduce; one that is laxer produces a green tick that
means nothing. The full file, and the variants, are in `WORKFLOWS.md`.

## Read the posture first

`docs/agents/rust.md` — written by `/setup-rust-skills` — carries edition,
MSRV, async runtime, `no_std` posture, and unsafe policy. Every one of those
changes the workflow: MSRV decides whether there is a second toolchain job,
`no_std` decides whether `--target` matters, and the unsafe policy decides
whether a Miri job earns its slot. If the file is absent, say so and offer to
run `/setup-rust-skills` first — do not guess a posture and bake the guess
into CI.

## The three jobs that always earn their place

`fmt` (`cargo fmt --check`), `clippy` at the configured level, and `test`.
Each with its own job so a red tick names the failure without opening logs.
`build` is not a fourth default job — it earns its place in exactly two
spots: the `no_std` variant, where `cargo test` cannot run on a bare-metal
target so the job builds only, and the MSRV job, whose command is
`cargo build`. State plainly what does not belong in the default set: a
coverage gate, a benchmark run, and a cross-compilation matrix are all
things a repo adds when it needs them, not things a setup skill imposes.

## The clippy invocation, and warnings as errors

The clippy job runs at the levels the repo configures in its lint block, and
adds no blanket flag. When the repo has no lint configuration at all, the
fallback is to make every warning fatal, either with `-- -D warnings` on the
clippy command or `RUSTFLAGS="-D warnings"` for the job. Choose one, and say in
a comment that it is the fallback and goes away once a lint block exists. The
reason for not making it the default is the same one that keeps
`#![deny(warnings)]` out of source: a new toolchain adds lints, and a blanket
deny turns an unrelated upgrade into a red build and blocks extra lint tools.
A deliberate fatal lint is denied by name in the lint block, so local runs and
CI agree.

## Feature combinations

Each independent feature doubles the configurations, and a CI run with
default features or with `--all-features` covers two of them. Where features
are independent, add a job that checks the combinations that matter, with
`cargo hack`, per feature or over the powerset; a large powerset belongs on a
schedule rather than on every push. Code that differs per platform needs the
same treatment: a job on each platform that has distinct code, not only the
one the maintainers use.

## Toolchain consistency

When the repo pins its toolchain in `rust-toolchain.toml`, the jobs use that
version, not a floating `stable`, so a compiler release cannot change CI
results on an unchanged commit. The MSRV job and an optional "latest stable"
job are the deliberate exceptions, and both are named for what they are.

## Checks beyond the default jobs

Add these only when the repo earns them, and propose rather than impose.

- Advisories and policy: a `cargo audit` or `cargo deny` job, run on
  dependency-changing pull requests and on a weekly schedule, since new
  advisories appear without any commit. `/rust-supply-chain` decides what the
  policy says; this skill wires the job.
- Generated-code drift: if the repo commits generated output (bindings,
  protocol code, lookup tables), a job regenerates it and fails if the
  working tree then differs from what is committed. The template is in
  `WORKFLOWS.md`.
- Process problems: when the team hits a recurring problem that a script
  can detect — a forgotten changelog entry, a lockfile out of date, a forbidden
  import — add the check to CI before fixing the instances. A failing check
  proves the problem is real and keeps the fix from regressing.
- Flaky tests are removed or quarantined, not retried until green; a CI that
  cries wolf teaches people to ignore it.

## What belongs in CI and what in the editor

CI is for checks whose failure should block a merge and that are worth the
minutes: the jobs above. Fast checks with no false positives — rustfmt on
save, clippy in `rust-analyzer` — belong in the editor, and cheap commit-time
ones in `/setup-rust-pre-commit`. A check lives in CI as well as locally only
if it can run locally, so every job's command must be one a contributor can
type.

## MSRV is a job, not a hope

If `rust-version` is set in `Cargo.toml`, CI must build on exactly that
toolchain, because nothing else will catch the day a contributor uses a newer
standard-library method. The version, not the ref, is what is pinned: the
`toolchain` input takes the MSRV read from `Cargo.toml`, never `stable`, as the
read step in `WORKFLOWS.md` does. The job builds and does not test —
`WORKFLOWS.md` says why.

## What makes a workflow safe to hand someone

- `permissions: contents: read` at the top level, widened only per job that
  needs it — a workflow that cannot write needs no audit for writes.
- Every action carries an explicit version ref — a floating ref lets the
  workflow change underneath the repo without the repo changing.
- A `concurrency` group keyed on the ref — a force-push cancels the
  superseded run instead of paying for two builds of the same code.
- `timeout-minutes` on each job — a hung job is an open-ended bill, and the
  timeout is what closes it.
- Caching that keys on the lockfile — the cache is valid exactly while the
  dependency set is unchanged, no wider.

Each has to survive a reviewer asking why it is there, because a workflow the
user cannot justify to their own reviewer will be deleted.

## Never overwrite an existing workflow

If `.github/workflows/` already holds a Rust workflow, read it and report the
difference as a diff for approval. A repo with CI has CI for reasons that
predate this skill.

## Verification

Before committing the workflow, prove every command in it actually passes
locally — with the `WORKFLOWS.md` caveat that `--all-features` is sometimes
wrong (mutually exclusive features), a repo in that case proves at the feature
set its CI actually runs:

```bash
cargo fmt --check
cargo clippy --all-targets --all-features   # at the level the repo configured
cargo test --all-features
actionlint .github/workflows/rust.yml   # if available; report if not installed
```

Then, after pushing, confirm the first run:
`gh run list --workflow rust.yml --limit 1`. A workflow that has never run once
is not evidence of anything.
