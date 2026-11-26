---
name: rust-supply-chain
description: Audit a Rust dependency tree — advisories, licences, banned and duplicate crates, and unmaintained dependencies — and turn each finding into a decision. Use when checking whether dependencies are safe to ship, when cargo audit or cargo deny reports something, when adding a dependency to a project with a licence policy, when a build pulls in two versions of the same crate, or when the user asks about supply chain risk in Rust.
---

# Rust Supply Chain

An audit that ends in a list of advisory IDs has done the easy half. The hard
half is saying, per advisory, whether this repo actually reaches the vulnerable
code path and what to do about it.

## What this covers, and the one rule

Four questions: is anything we depend on known-vulnerable, is anything
unmaintained, does every licence in the tree comply with the policy, and is
the tree carrying weight it does not need. Each added crate lengthens
compiles, grows the binary, and widens the set of authors you trust, and that
includes its `build.rs` and any proc macros, which run arbitrary code on the
build machine. Read `Cargo.lock` as the authority
on what is actually built — not `Cargo.toml`, which states ranges — and read
the MSRV from `docs/agents/rust.md`, because a fix that bumps a dependency
past the MSRV is not a fix. The rule: **every finding ends in a decision** —
upgrade, replace, vendor, or accept with a written reason and an expiry. An
unactioned advisory list is noise, and noise trains people to ignore the tool.

## Two tools, overlapping on purpose

`cargo audit` reads the RustSec advisory database and answers exactly one
question: is anything in the tree known-vulnerable. `cargo deny` answers four
— `advisories`, `bans`, `licenses`, `sources` — including that same one,
against a policy file; with no deny.toml it runs on built-in defaults that
encode no policy. A repo running `cargo deny check` does not
need `cargo audit` separately; a repo that wants only advisory checking and no
policy file is better off with `cargo audit` alone. Say which the repo should
run and why, rather than adding both. The policy file in full, annotated, is
in `DENY.md`; it lands in the target repo only on explicit request.

## Reading an advisory properly

An ID and a severity are the start. The question is whether *this* repo
reaches the affected code — a parsing vulnerability in a crate used only in a
build script for developer tooling is a different decision from the same
advisory in a network-facing path. The mechanics: `cargo tree --invert
<crate>` shows who pulled it in, which tells you whether the dependency is
direct (you upgrade) or transitive (you upgrade the intermediary, or wait for
it). State plainly that "no upstream fix yet" is a real outcome with real
options — pin, patch via `[patch.crates-io]`, vendor, or replace — and that
recording the choice matters more than which one is picked.

## Unmaintained is a finding, not a warning to mute

RustSec issues `RUSTSEC-*` unmaintained notices with no vulnerability
attached. Treat them as a maintenance-planning signal with a horizon, not an
emergency: note the crate, check whether a maintained fork has consensus, and
decide whether to move now or watch it.

## Duplicates are a licence and a binary-size problem before they are a taste problem

```bash
cargo tree -d
```

Cargo lets semver-incompatible versions of a crate coexist (a 0.x and a 1.x,
or two majors) and never two compatible ones, so a duplicate always means a
range somewhere is stuck on an older line. Every duplicate means two
versions compiled in, two licence obligations, and — when the crate has global
state or a public type crossing an API boundary — genuinely confusing type
errors: two `Url` types that look identical and do not unify. That is also the
price of splitting everything into tiny single-purpose crates; the
composability is real, and so is the version skew. The fix is usually raising a lower bound so
the two ranges unify, not banning the crate. `cargo deny check bans` is what
keeps a resolved duplicate resolved.

## Version requirements say how much drift is allowed

A bare `"1.4"` means `^1.4`: any compatible newer release. `"~1.4.2"` allows
patch releases only, `"=1.4.2"` pins one exact version, and `"*"` accepts
anything. Prefer the bare form (`"1"` or `"1.4.23"` as the lower bound the
code truly needs). An exact pin in a library blocks every other crate in the
graph from unifying on a neighbouring version and manufactures the duplicates
above; a wildcard hands control of the build to whoever publishes next.
Exact pins belong in an application's lockfile, not in manifests other crates
depend on.

Commit `Cargo.lock` for a binary or application — the lockfile is what makes
the build reproducible and the audit meaningful. For a library it is optional,
because consumers resolve their own.

To see why a feature is on, or which dependency turns it on:

```bash
cargo tree --edges features --invert <crate>
```

## Licence policy is a decision the repo owns, not one this skill imports

The axis runs from permissive-only to copyleft-tolerated. `deny.toml` needs an
explicit allow-list either way, and crates with no licence metadata at all
need a per-crate exception with a reason attached. Do not ship an opinion
about which licences a user may accept — name the axis, let the repo decide,
and record the decision in the policy file.

Some facts the user can act on, stated as information rather than a rule.
Depending only on permissively licensed crates keeps a permissive crate freely
redistributable; one copyleft dependency changes what downstream users may do
with the whole binary. And the licence, like the default feature set, is part
of the public contract of a crate: changing either is a breaking change for
someone.

## Licensing the crate itself

When the repo is a crate it publishes, the ecosystem default is the dual
licence `MIT OR Apache-2.0`: `license = "MIT OR Apache-2.0"` in the manifest
and both licence texts shipped as files in the repo root, matching the Rust
project. Offer it as the default when the user has no preference; if they have
chosen another licence, keep theirs and make sure the manifest field and the
licence files agree with each other.

## What to run on a schedule instead of on every commit

The advisory database changes without the code changing, so an audit belongs
on a weekly schedule and on dependency-change pull requests — not in a
pre-commit hook, where it costs network time on every commit. If the repo
wants that wired into CI, run the `/setup-rust-ci` skill — it writes the
workflow.

## Verification

```bash
cargo deny check            # advisories, bans, licenses, sources
cargo audit                 # if the repo uses it standalone
cargo tree -d
cargo tree --edges features   # which dependency enables which feature
cargo update --dry-run      # what a routine refresh would move
```

Report exit codes, not just output: `cargo deny check` exits non-zero on any
denied finding, and that exit code is what a CI job keys on. If a tool is not
installed, say so and give the install line — never report a clean audit that
did not run.
