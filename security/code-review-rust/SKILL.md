---
name: code-review-rust
description: >
  Security review of Rust code — where a memory-safe language still has real bugs: `unsafe`, FFI,
  panics, and the usual injection/logic sinks. Load when reviewing Rust source/PR, on .rs / Cargo.toml
  in scope, or "review this Rust". Signals: Cargo.toml, unsafe blocks, extern "C", unwrap/expect,
  actix/axum/rocket handlers.
domain: code-review
type: reference
stability: learning
modes: [defense, pentest, bugbounty]
severity: info
cwe: [CWE-119, CWE-248, CWE-89, CWE-78, CWE-22]
tools: [cargo-audit, clippy, semgrep, miri]
schema_version: 1
---

# Rust source review

## When it applies
Reviewing Rust (a service, a CLI, a library). Safe Rust removes most memory bugs, so the review
focuses on the places safety is opted out of, the ways Rust code still panics or mis-handles input,
and ordinary injection/logic in web handlers.

## Why it works
Rust's guarantees hold only outside `unsafe` and only for memory safety — they don't stop SQL built
by string, a command run via a shell, a `.unwrap()` that panics on attacker input (DoS), or a logic
error. Concentrating on those boundaries finds the real bugs efficiently.

## Sinks & patterns (grep, then reason about the boundary)
- **`unsafe` blocks**: every one is a manual proof obligation — raw pointer deref, `get_unchecked`,
  `slice::from_raw_parts`, `mem::transmute`, uninitialised memory. Check the invariant it assumes.
- **FFI**: `extern "C"`/`bindgen` boundaries — lengths, lifetimes, and NUL handling across the C edge
  (the C side has none of Rust's guarantees; pair with `code-review-cpp`).
- **Panics as DoS**: `unwrap`/`expect`/`panic!`/indexing `v[i]`/`unreachable!` on
  attacker-controlled input; integer `as` casts that truncate; arithmetic overflow (panics in debug,
  wraps in release — both can be bugs). Prefer `?`/checked ops.
- **Injection**: SQL via `format!` into a query instead of parameter binding (sqlx/diesel);
  `std::process::Command` with `sh -c` and concatenated input; `Command` arg vs shell form.
- **Path / SSRF**: user paths joined without canonicalisation + prefix check; HTTP clients (reqwest)
  fetching user URLs.
- **Deserialization / web**: `serde` into types from untrusted data (resource exhaustion, unexpected
  variants); actix/axum/rocket extractors bound to over-broad structs (mass assignment); missing
  auth middleware on state-changing routes.

## Method
1. Run `cargo audit` (known-vuln deps), `cargo clippy`, and `semgrep`; `miri` for `unsafe` UB where feasible.
2. `rg 'unsafe|unwrap\(\)|expect\(|transmute|Command::new|format!\(.*(SELECT|INSERT|UPDATE)'` → review each.
3. Justify every `unsafe` block's invariant; if you can't, that's a finding.
4. Confirm exploitable injection/logic with the matching runtime skill.

## Gotchas
- Idiomatic Rust is genuinely safe — don't invent memory bugs in safe code; spend effort on `unsafe`,
  FFI, panics, deps, and logic.
- Release-mode integer overflow wraps silently — a `checked_*`/`saturating_*` audit matters for
  size/index math.
- `cargo audit` flags vulnerable crates you'd never see by reading — always run it.

## References
Rustonomicon (unsafe); RustSec advisory DB / cargo-audit; Clippy lint set; Secure Rust Guidelines (ANSSI).
