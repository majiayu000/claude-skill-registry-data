---
name: rust
description: Use when writing Rust command-line tools and libraries with cargo and clap — tariff or pricing calculators, data processing, error handling with Result, property and table tests, and release builds. Also use when fighting the borrow checker on a simple data flow, when choosing between anyhow and thiserror, or when floating-point results need exact decimal behaviour.
---

# Rust

Default: stable toolchain via `rustup`, edition from `cargo new`, `clap` (derive) for CLIs, `anyhow` in binaries and `thiserror` in libraries, `cargo test`, `clippy` and `rustfmt` in CI.

## Setup

1. `cargo new tool` (binary) or `cargo new --lib core`; for anything non-trivial, a workspace with `core` (logic) and `cli` (I/O).
2. Pin the toolchain with `rust-toolchain.toml` so every machine uses the same compiler and components (`clippy`, `rustfmt`).
3. Commit `Cargo.lock` for binaries.

## CLI with clap

```rust
#[derive(clap::Parser)]
#[command(version, about)]
struct Args {
    /// Monthly usage in kWh
    #[arg(long)]
    usage: u32,
    #[arg(long, default_value = "plans.toml")]
    plans: std::path::PathBuf,
}
```

- Doc comments become help text; keep them accurate.
- Parse, then call a pure function from `core`; print results in `main` only.

## Modelling money and tiers

For tiered tariffs (first N units at one price, next M at another, plus a fixed charge and an adjustment per unit):

- Represent prices as integers of the smallest unit (or a decimal crate such as `rust_decimal`) — not `f64`.
- Model tiers as a sorted `Vec<(Option<u32>, i64)>` (upper bound, price per unit; `None` = no limit) and compute with one loop; test boundaries at exactly the tier limits.
- Compare plans by evaluating each across a range of usages and reporting the crossover points, which is what a person actually wants to know.

## Errors

- Libraries: an error enum with `thiserror`, one variant per failure the caller may handle.
- Binaries: `anyhow::Result` with `.context("reading plans file")` so messages explain what was being done.
- Avoid `unwrap()` outside tests and truly impossible cases; prefer `expect("reason")` when you must.

## Testing

- Unit tests next to the code (`#[cfg(test)] mod tests`), integration tests in `tests/` that run the binary with `assert_cmd`.
- Table tests over boundary values; `proptest` for invariants (e.g. total cost is monotonic in usage).

## Verification loop

1. `cargo fmt --check`, `cargo clippy -- -D warnings`.
2. `cargo test`.
3. `cargo build --release` and run the binary with `--help` and a real input.

## Pitfalls

- **Borrow fights over a simple flow** usually mean shared mutable state; restructure into owned data passed through functions, or clone small values. Reach for `Rc<RefCell<_>>` last.
- **Integer overflow** panics in debug and wraps in release; use `checked_*`/`saturating_*` where inputs are external.
- **`String` vs `&str`:** take `&str` (or `impl AsRef<str>`) in parameters, return `String`.
- **Slow first build** is normal; use `cargo check` while iterating.
- **Cross-compiling** needs the target's linker; build in a container of the target platform when in doubt.
