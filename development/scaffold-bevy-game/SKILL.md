---
name: scaffold-bevy-game
description: Use when starting a new Bevy game or fixing a Bevy project that compiles slowly, has fat code in main.rs, or has no CI — creates a lib+bin cargo project with fast dev builds, plugin composition, assets folder, clippy/rustfmt/nextest CI and optional wasm.
---

# Scaffold Bevy Game

Target: Bevy 0.20, Rust edition 2024. Versions and the "newest Bevy unless a crate is behind" rule: [stack-versions](../_shared/stack-versions.md). Rationale per rule: [scaffold-patterns.md](scaffold-patterns.md).

## 1. Audit current state (change nothing)

```bash
cat .claude/stack-profile.md 2>/dev/null          # languages, task_runner, ci, lint_format.rust, tests.layout
ls Cargo.toml src/lib.rs src/main.rs rust-toolchain.toml .cargo/config.toml assets .github/workflows 2>/dev/null
grep -nE '^bevy|^edition|rust-version|dynamic_linking|\[profile' Cargo.toml 2>/dev/null
grep -c "add_systems\|spawn(" src/main.rs 2>/dev/null   # logic in main.rs = to extract
cargo --version; cargo nextest --version; ls justfile mise.toml Makefile 2>/dev/null
```

Read the profile first. Without it, detect: `Cargo.toml` → `cargo`; `justfile` → `just`; `.github/` → `github-actions`. Ask only about the **target platform** (desktop only, or desktop + web) and only if the repo does not say — it changes the CI and profile output.
Third-party Bevy crates (physics, input): check each crate's `bevy` requirement now (see stack-versions). It decides the Bevy line.

## 2. Decide what to do
- No `Cargo.toml` → full scaffold (steps 4–7).
- Project exists → apply only the delta: missing `[profile]` tuning, `dev` feature, lib/bin split, CI, `rust-toolchain.toml`, lints.
- All present and `cargo clippy --all-targets -- -D warnings` is clean → say "already in place" and stop.

## 3. Detect track
- **Desktop only** → skip the wasm profile and CI job.
- **Desktop + web** → add `wasm-release` profile, the `wasm32-unknown-unknown` target, and the web CI job.
- **Workspace** only when a second crate exists (dedicated server, tools, shared protocol). One game = one package with `lib.rs` + `main.rs`.

## 4. Install only what's missing

```bash
rustup toolchain install stable --component clippy rustfmt   # skip if present
cargo install cargo-nextest --locked                          # skip if `cargo nextest --version` works
rustup target add wasm32-unknown-unknown                      # web track only
cargo install wasm-bindgen-cli --locked                       # web track only; version must equal the wasm-bindgen crate in Cargo.lock
```

Linux build dependencies (Debian/Ubuntu): `g++ pkg-config libx11-dev libasound2-dev libudev-dev libxkbcommon-x11-0`.
macOS needs nothing extra. Bevy CLI is optional alpha (git install only) — never required here.

## 5. Generate the seams

`cargo new --lib <name>` then add `src/main.rs`. Canonical files (full text in [scaffold-patterns.md](scaffold-patterns.md)):

```
Cargo.toml              # lib+bin, dev feature, profiles, lints
rust-toolchain.toml     # stable + clippy + rustfmt
rustfmt.toml            # only if you deviate from defaults (usually: none)
justfile                # run / check / test / web
.cargo/config.toml      # Linux aarch64 / Windows linker only; macOS and x86_64 Linux need none
.github/workflows/ci.yml
assets/                 # sprites/ audio/ fonts/ — see manage-bevy-assets
src/lib.rs              # GamePlugin: composes feature plugins
src/main.rs             # 6 lines: App + DefaultPlugins + GamePlugin
src/<feature>.rs        # one plugin per feature — see structure-bevy-app
tests/                  # headless integration tests — see test-bevy-systems
```

`main.rs` stays thin so the whole game is a library that tests can build without a window:

```rust
use bevy::prelude::*;
use my_game::GamePlugin;

fn main() -> AppExit {
    App::new().add_plugins((DefaultPlugins, GamePlugin)).run()
}
```

```rust
// src/lib.rs
use bevy::prelude::*;

pub mod core;

pub struct GamePlugin;

impl Plugin for GamePlugin {
    fn build(&self, app: &mut App) {
        app.add_plugins(core::CorePlugin);
    }
}
```

## 6. Wire it
- `Cargo.toml`: `bevy = { version = "0.20", default-features = false, features = ["2d", "ui", "audio"] }` (add `"3d"` for 3D). Feature `dev = ["bevy/dev", "bevy/dynamic_linking"]`. `[profile.dev] opt-level = 1`, `[profile.dev.package."*"] opt-level = 3`.
- Daily loop: `cargo run --features dev` (hot reload + dynamic linking). Release and CI builds never pass `dev`.
- `[lints.clippy] too_many_arguments = "allow"` and `type_complexity = "allow"`: Bevy systems take injected parameters.
- CI: fmt → clippy `-D warnings` → `cargo nextest run` (+ `cargo test --doc`). Web track adds a `cargo check --target wasm32-unknown-unknown` job.
- Commit `Cargo.lock`. Ignore `target/` and `dist/`.

## 7. Verify

```bash
cargo fmt --check && cargo clippy --all-targets -- -D warnings && cargo nextest run
cargo run --features dev        # a window opens; edit a file in assets/ and see it reload
cargo build --release           # builds without the dev feature (no dylib in target/release/)
```

Expected: all three commands exit 0; `ls target/release | grep -i bevy_dylib` prints nothing.
Web track: `cargo check --target wasm32-unknown-unknown --lib` exits 0.

Also follow: [engineering principles](../../core/_shared/engineering-principles.md), [security baseline](../../core/_shared/security-baseline.md) (CI permissions, no secrets in assets), then [structure-bevy-app](../structure-bevy-app/SKILL.md).
