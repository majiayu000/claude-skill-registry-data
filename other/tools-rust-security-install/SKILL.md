---
name: tools-rust-security-install
description: Install the Rust security tooling (cargo-audit, cargo-deny, cargo-geiger, Miri) used for dependency-advisory and unsafe-code review
---

This skill should not need sudo privileges. Read `docs/agents/rust.md` first —
it records which of these tools the repo runs and where Miri applies.

## Prerequisites (must already be installed)
- Rust toolchain (rustup/cargo)
- A C toolchain and `pkg-config` + OpenSSL headers (cargo-geiger builds against them)

If any prerequisite is missing, inform the user and stop.

## Installation Steps

Skip any tool whose `--version` already succeeds.

1. cargo-audit (RustSec advisories against `Cargo.lock`):
   ```
   cargo audit --version || cargo install --locked cargo-audit
   ```

2. cargo-deny (advisories, bans, sources, licenses):
   ```
   cargo deny --version || cargo install --locked cargo-deny
   ```

3. cargo-geiger (unsafe usage per crate):
   ```
   cargo geiger --version || cargo install --locked cargo-geiger
   ```
   cargo-geiger 0.14+ needs rustc 1.97. If the install fails with a rustc-version
   error, pin the last release that supports the active toolchain (the error names
   it), e.g. `cargo install --locked cargo-geiger --version 0.13.0` (rustc >= 1.85).
   If it fails on OpenSSL, report the error and continue with the other tools.

4. Miri (undefined-behaviour checker; nightly only):
   ```
   rustup +nightly component add miri rust-src
   cargo +nightly miri --version
   ```

## Verification

```
cargo audit --version
cargo deny --version
cargo geiger --version
cargo +nightly miri --version
```

Report which tools are installed and their versions, and any that failed.

## Usage notes

- `cargo audit` — run from the repo root; scans the workspace `Cargo.lock`.
- `cargo deny check advisories` works without config; `bans`/`licenses`/`sources`
  need a `deny.toml` (`cargo deny init`), which the repo does not have yet.
- Miri cannot run the FFI crates (SPDK/CUDA/RDMA). Candidates are the pure-Rust
  `unsafe` in `lib/shm-queue` and the `component-core` channels, e.g.
  `cargo +nightly miri test -p shm-queue`.
