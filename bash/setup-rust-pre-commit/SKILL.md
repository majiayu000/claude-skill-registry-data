---
name: setup-rust-pre-commit
description: Set up fast pre-commit hooks for a Rust repo — format and lint the staged changes only, with CI left as the real gate.
disable-model-invocation: true
---

# Setup Rust Pre-commit

A pre-commit hook is a convenience, never a gate. CI is the gate: it runs on every
push whether or not a local hook ever fired. A hook that tries to be the gate gets
slow, and a slow hook gets bypassed with `--no-verify` within a week — at which
point the repo has neither a hook nor the honesty of admitting it. Like
`/setup-rust-ci`, this skill runs only when the user invokes it — a hook executes
on someone's behalf at every commit, and the model never decides that on its own.

## The one rule, stated first

A hook that takes longer than about two seconds will be bypassed. Everything else
in this skill follows from that: format and lint, never test; staged files, never
the workspace; report and stop, never fix silently.

## Ask which mechanism before writing anything

Three, and the choice is the user's:

| Mechanism | Fits when | Costs |
|---|---|---|
| `core.hooksPath` script | Rust-only repo, no other hook needs | Each contributor runs one `git config` line; nothing enforces that they did |
| `lefthook` | Mixed repo, wants parallel hooks, no Python | One binary dependency |
| `pre-commit` | The repo already uses it for other languages | Python toolchain, and the Rust hooks shell out to cargo anyway |

Detect what is already there — an existing `.pre-commit-config.yaml`,
`lefthook.yml`, or `core.hooksPath` setting — and match it rather than introducing
a second mechanism. The complete files for all three, ready to paste, are in
`HOOKS.md`.

## What goes in the hook, and what never does

In: `cargo fmt` on the staged Rust files, and `cargo clippy` at the configured
level. Out: `cargo test` (too slow, and a broken test is what CI exists to
report), `cargo build --release`, and anything network-bound such as
`cargo audit` — those belong on a schedule, and `/rust-supply-chain` covers them.

The level is not a flag the hook adds. Read the recorded posture from
`docs/agents/rust.md`, exactly as `/setup-rust-ci` does — including the clippy
command it records, at the level configured in `Cargo.toml` — and if the file
is absent, say so and offer to run `/setup-rust-skills` first; do not guess a
level and bake the guess into a hook. The hook then runs clippy with no level
flag added, because clippy applies the repo `[lints]` configuration on its own.
A hook stricter than CI fails commits CI would pass, which is the single most
effective way to get a hook uninstalled. The `-D warnings` flag belongs only in
the fallback form — a repo with no lint configuration at all — and nowhere else.

## Staged-only is the difference between two seconds and thirty

The file list comes from what the user actually staged:

    git diff --cached --name-only --diff-filter=ACM -- '*.rs'

The warning worth stating plainly: `cargo clippy` cannot be scoped to files. It
works per crate, so a workspace hook should lint only the crates containing staged
files — and a repo where even that is still slow should drop clippy from the hook
and keep `fmt`. The hook that survives is the one the repo keeps trusting.

## Formatting: report or rewrite, and say which

Two defensible designs. `cargo fmt --check` fails and makes the user format;
`cargo fmt` rewrites the files and re-stages them. Rewriting silently changes what
the user is about to commit, so if the repo picks it, the hook must print every
file it touched. Never rewrite without printing. Say in the contributing notes
which design the repo uses, so a newcomer is not ambushed by a hook that edits a
staged file. The rewrite variant, written out, is in `HOOKS.md`.

## Document the bypass in the same breath as the hook

`git commit --no-verify` exists, and contributors will need it — a
work-in-progress commit on a branch, an emergency fix. A hook presented as
unbypassable is a hook people route around resentfully. Write the bypass into the
repo contributing notes next to the setup line: what the hook runs, how to install
it, and that `--no-verify` is available and legitimate. The block to paste is in
`HOOKS.md`.

## Verification

Prove the hook both fires and passes — a hook nobody has seen reject anything is
not known to work:

```bash
# 1. install it, then deliberately break formatting
printf 'fn  main( ) {}\n' > /tmp/hook-probe.rs && cp /tmp/hook-probe.rs src/hook_probe.rs
git add src/hook_probe.rs
git commit -m "probe: hook must reject this"   # expected: rejected, naming the file
git restore --staged src/hook_probe.rs && rm src/hook_probe.rs
# the reset in step 2 is only valid because step 1 was rejected — if that commit landed, fix the install before step 2
# 2. confirm a clean commit still passes, and time it
time git commit --allow-empty -m "probe: hook must allow this"
git reset HEAD~1
```

Report the measured time. Over two seconds, cut the hook down rather than shipping
it.
