---
name: rust-cli
description: "Build production Rust CLIs with clap derive, anyhow/thiserror boundaries, script-friendly stdout/stderr, ExitCode mapping, assert_cmd tests, and release Cargo workspaces."
category: development
risk: safe
source: self
source_type: self
date_added: "2026-08-26"
tags: ["rust", "cli", "clap", "cargo", "anyhow", "thiserror", "assert-cmd", "exit-codes"]
tools: ["claude", "cursor", "gemini", "codex"]
---

# Rust CLI Tooling AI Skill Guide (Claude)

## Overview & Engine Architecture

Rust CLIs are **Cargo binary crates** (often workspace members) that parse argv with **clap**, report failures with **`anyhow` at the binary edge** and structured **`thiserror` in libraries** when callers must match variants, and exit with **meaningful codes**. Agents keep I/O fallible, avoid `unwrap`/`expect` on user-facing paths, put **data on stdout / diagnostics on stderr**, and prove behavior with **`assert_cmd`** integration tests.

```
┌─────────────────────────────────────────────────────────────┐
│                 Rust CLI execution path                       │
│                                                             │
│  cargo run / installed binary                               │
│  ├── clap::Parser / Subcommand (+ env defaults)             │
│  ├── library crate (thiserror / Result)                     │
│  └── bin edge: anyhow context → ExitCode + stderr           │
│                                                             │
│  I/O contract                                               │
│  ├── stdout: machine-consumable result (text/json)          │
│  └── stderr: progress, warnings, errors                     │
│                                                             │
│  Quality                                                    │
│  └── unit + assert_cmd / trycmd + clippy -D warnings        │
└─────────────────────────────────────────────────────────────┘
```

---

## When to use / when not to

**Use when**

- Building command-line tools, devops helpers, or scriptable utilities in Rust.
- Adding subcommands, flags, env-backed defaults, and `--format json` for automation.
- Structuring workspace `lib` + `bin` crates and release/`--target` distribution.

**Do not use when**

- The deliverable is a long-running HTTP service → `@go-services` or `@nodejs` / `@express`.
- Packaging is primarily Python entry points → `@python-packaging`.
- Someone asks to embed production secrets in the binary or disable TLS verification for “convenience” → refuse.

---

## Operational Capabilities & Agent Directives

1. Derive **`clap::Parser` / `Subcommand`**; every flag gets a help string; document env vars in help/README.
2. **`anyhow::Result` in `main`** with `.with_context(|| …)` on I/O; use **`thiserror`** in libraries when callers match error kinds.
3. **Stdout = data, stderr = diagnostics**; never log progress on stdout if the tool is meant for pipes.
4. Map failure classes to **exit codes** (0 success, 2 usage/clap, 1 general)—scripts depend on `$?`.
5. Prefer `?` over `unwrap` on user input paths; reserve `expect` for invariants that are programmer bugs.
6. Gate quality with `cargo fmt`, `cargo clippy -- -D warnings`, `cargo test`, and **`assert_cmd`** smoke tests.
7. Pin **MSRV** in `Cargo.toml` when supporting older toolchains; use workspaces when lib reuse or compile times matter.

---

## Production Example: clap + anyhow + assert_cmd

`Cargo.toml` (excerpt):

```toml
[package]
name = "inventory"
version = "0.1.0"
edition = "2021"
rust-version = "1.74"

[dependencies]
anyhow = "1"
clap = { version = "4", features = ["derive", "env"] }

[dev-dependencies]
assert_cmd = "2"
predicates = "3"
```

```rust
use anyhow::{Context, Result};
use clap::{Parser, Subcommand};
use std::path::PathBuf;
use std::process::ExitCode;

#[derive(Parser)]
#[command(name = "inventory", version, about = "Inventory helper CLI")]
struct Cli {
    /// Emit machine-readable JSON on stdout
    #[arg(long, global = true, env = "INVENTORY_FORMAT")]
    format: Option<String>,

    #[command(subcommand)]
    cmd: Commands,
}

#[derive(Subcommand)]
enum Commands {
    /// Count lines in a file (stdout = count only)
    Count {
        path: PathBuf,
    },
}

fn run() -> Result<()> {
    let cli = Cli::parse();
    match cli.cmd {
        Commands::Count { path } => {
            let data = std::fs::read_to_string(&path)
                .with_context(|| format!("read {}", path.display()))?;
            let n = data.lines().count();
            if cli.format.as_deref() == Some("json") {
                println!("{{\"lines\":{n}}}");
            } else {
                println!("{n}");
            }
        }
    }
    Ok(())
}

fn main() -> ExitCode {
    match run() {
        Ok(()) => ExitCode::SUCCESS,
        Err(err) => {
            eprintln!("error: {err:#}");
            ExitCode::from(1)
        }
    }
}
```

Integration test (`tests/cli.rs`):

```rust
use assert_cmd::Command;
use predicates::prelude::*;

#[test]
fn count_missing_file_fails() {
    Command::cargo_bin("inventory")
        .unwrap()
        .args(["count", "does-not-exist.txt"])
        .assert()
        .failure()
        .code(1)
        .stdout(predicate::str::is_empty())
        .stderr(predicate::str::contains("read"));
}
```

Commands:

```bash
cargo new inventory --bin
cargo add clap --features derive,env
cargo add anyhow
cargo add --dev assert_cmd predicates
cargo run -- count ./README.md
cargo clippy -- -D warnings
cargo test
cargo build --release
```

Distribute via release binary or `@docker` when the org ships tools as images.

---

## Technical Troubleshooting Matrix

| Signature | Likely cause | Fix path |
| :--- | :--- | :--- |
| Pipe consumer parses log noise | Progress/logs on stdout | Move to stderr; keep stdout pure |
| CI passes on failure | Exit 0 despite validation error | Return non-zero `ExitCode`; assert in `assert_cmd` |
| Clap usage printed oddly | Error before format flag parsed | Recover format from raw argv for usage errors if needed |
| `unwrap` panic (exit 101) | Panic on bad user input | `?` + context; never panic for expected I/O errors |
| Slow `cargo build` | Monolith crate / many proc-macros | Workspace libs; feature-gate heavy deps |
| Cross-compile linker errors | Missing target / linker | `rustup target add`; zig/cross or CI matrix |
| Color codes break logs | Always-on ANSI | `clap`/`anstream` auto vs `--color never` |

---

## Best Practices

1. Support `--format json` (or `--output`) when output grows beyond one scalar.
2. Document required env vars in `--help` and README; prefer `env = "…"` on clap args.
3. Unit-test library logic; integration-test the **binary** with `assert_cmd` (and trycmd for help snapshots when stable).
4. Use `tracing` to stderr with levels; default quiet for scripts.
5. `cargo build --release` for distribution; strip/LTO only when measured and MSRV-safe.

---

## Limitations

- Cross-compilation needs target toolchains and sometimes custom linkers.
- Async (tokio) CLIs add complexity—use only when concurrent I/O dominates.
- Signal handling, TTY detection, and Windows argv/path rules are OS-sensitive.
- Ecosystem crates with heavy proc-macros increase compile time for dependents.

---

## Related Skills

- `@go-services` — Go alternative for simple static service binaries
- `@docker` — ship CLIs in images when host installs are hard
- `@python-packaging` — Python CLI packaging alternative
- `@nodejs` — Node-based CLIs when the org standard is JS/TS
- `@typescript` — typed config/schemas consumed by the CLI

---

## Agent Operational Directive

> **MANDATORY**: Clap-derived help for every flag. Data on stdout, errors on stderr. Non-zero exit codes for failures. Prefer `anyhow` at the edge and structured errors in libraries when matching matters. Prove with `cargo test` + `assert_cmd`. Never embed secrets in binaries.

---

## Source anchors (research)

- [Command Line Applications in Rust — exit codes](https://rust-cli.github.io/book/in-depth/exit-code.html)
- [clap / CLI Spec error + exit mapping](https://clispec.dev/guide/rust/)
- [assert_cmd CLI testing patterns](https://alexwlchan.net/2025/testing-rust-cli-apps-with-assert-cmd/)
- [Reddit: anyhow vs thiserror guidance](https://www.reddit.com/r/rust/comments/1cnhy7d/whats_the_wisdom_behind_use_thiserror_for/)
