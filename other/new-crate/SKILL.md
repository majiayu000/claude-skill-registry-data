---
name: new-crate
description: Add a new crate to the OpenDataSuite Cargo workspace with correct layering, metadata, lints, and test scaffolding. Use when creating ods-* module crates, provider crates, or stores, or when scaffolding the workspace for the first time.
---

# Add a crate

## Decide where it goes
| Kind | Path | May depend on |
|---|---|---|
| Core/domain (`ods-core`, `ods-events`, `ods-config`, `ods-policy`) | `crates/` | std, serde, small utility crates; `ods-core` depends on nothing internal |
| Contracts (`ods-sdk`) | `crates/` | `ods-core`, foundation crates |
| Module (`ods-state`, `ods-erd`, …) | `crates/` | core, sdk, other modules only if ADR-approved |
| Provider/store (`ods-provider-*`, `ods-store-*`) | `providers/` | core, foundation, sdk, vendor client libs — never modules |
| Binary (`ods-cli`) | `crates/` | anything |

A module crate must **never** depend on a provider crate. If you need one, you need a new
contract in `ods-sdk` instead.

## First-time workspace scaffold
If no root `Cargo.toml` exists, create it with:
- `[workspace] resolver = "3"`, `members = ["crates/*"]` — add `"providers/*"` with the first provider crate (Cargo rejects a glob that matches nothing)
- `[workspace.package]` edition = "2024", license = (per #10/#101, default `Apache-2.0`), repository, rust-version
- `[workspace.dependencies]` pinning shared deps (serde, thiserror, tokio, clap, tracing)
- `[workspace.lints.rust] unsafe_code = "forbid"`; `[workspace.lints.clippy] all = "warn", pedantic = "warn"` (allow noisy ones explicitly)
- `rust-toolchain.toml` (stable), `deny.toml`, `.github/workflows/ci.yml` running the `verify` stages.

## Per-crate steps
1. `cargo new --lib crates/<name>` (or `providers/<name>`); binaries use `--bin`.
2. In its `Cargo.toml`: `version.workspace = true`, `edition.workspace = true`,
   `license.workspace = true`, `[lints] workspace = true`; use `dep.workspace = true` for shared deps.
3. `src/lib.rs` starts with a crate-level doc comment stating purpose and allowed dependencies.
4. Add at least one unit test and, for providers, wire the SDK conformance tests.
5. Register the crate's layer in `scripts/check-layering.py` (unknown crates fail CI).
6. Update the layout in `docs/ROADMAP.md` §7 / AGENTS.md if the crate is new to the plan.
7. Run the `verify` skill.
