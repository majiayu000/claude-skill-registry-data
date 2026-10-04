---
name: cgagentharness-verify-deps
description: |
  Verify Cargo dependencies, security advisories, licenses, and locked versions for CG-Agent-Harness. Run this whenever Cargo.toml changes, after adding/updating dependencies, or before pushing security-sensitive PRs. Checks: Cargo.lock is committed and locked, cargo deny passes (advisories/licenses/bans), no unsafe code regressions, no outdated critical deps, toolchain version matches rust-toolchain.toml, and no feature flags that contradict security posture. Essential for maintaining supply-chain hygiene and reproducible builds.
compatibility: |
  Requires: cargo, cargo-deny, rustup, Cargo.toml and Cargo.lock in both crates
  Context: Independent backend and desktop Rust crates with separate toolchains and policies
---

# Dependency verification

Read `docs/DEPENDENCIES.md`, both Cargo manifests/locks and both deny policies.
Backend Rust 1.88 and desktop Rust 1.90 are independent; desktop is not a root
workspace member. Use the pinned rustup tools and preserve working installations.

1. Verify both lockfiles are tracked, and run locked metadata/tree/build commands
   in both crates. Do not infer a stale lock merely because newer releases exist.
2. Preview updates using `cargo update --dry-run --locked --verbose --config
   'resolver.incompatible-rust-versions="fallback"'`. A plain semver update can
   exceed MSRV. Backend ordered-float 5.4 and the immutable desktop Tauri patch
   are deliberate constraints described in the dependency guide.
3. Run `cargo deny check` in both crates. Advisory, license, banned dependency or
   unknown-source errors block acceptance. Multiple-version warnings are allowed
   by current policy; record them. A missing cargo-deny is a missing required
   check, not a pass. Do not add advisory exceptions to silence a finding.
4. Inspect added Cargo features and every new unsafe block with its enclosing
   safety argument. Existing macOS platform trust/sandbox FFI uses narrow unsafe
   calls; a text-count heuristic does not prove safety. Cargo-deny does not
   enforce arbitrary feature semantics or runtime network behavior.
5. For authorized compatible updates, remove only `--dry-run --locked` from the
   preview, inspect the resulting diff and rerun the pinned-toolchain quality
   bar, release builds, packaged backend and native checks where affected.
   Major API/toolchain migrations need their own scope and evidence.
6. Record exact source/lockfiles, commands, exit codes, advisory data freshness,
   updated/retained dependencies and platform limitations. Tests are isolated
   from provider credentials and use owned temporary homes.

Never pipe a pass/fail command into grep or suppress its error output. Never
change global rustup overrides, global Git identity or user model state to make
verification pass. Dependency preparation may access approved registries;
application verification remains subject to the existing sandbox/write policy.
