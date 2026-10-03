---
name: rust-tooling
description: How to create Rust tools for the orchestrator, add crates to the workspace, and write shell wrappers. Use when building new tools or extending existing ones.
user-invocable: false
---

# Creating Rust Tools

The orchestrator can build its own compiled tools to automate repeated patterns. Tools live in a Cargo workspace at `tools/rust/`.

## Workspace structure

```
tools/
  check-field-inventory-rs   # shell wrapper (extensionless or -rs suffix, executable)
  check-field-inventory.jq   # legacy jq version (kept for reference)
  rust/
    Cargo.toml               # workspace root: members = ["crates/*"]
    Cargo.lock               # committed for reproducible builds
    crates/
      check-field-inventory/ # existing tool
        Cargo.toml
        src/
          main.rs
      your-new-tool/         # new crate goes here
        Cargo.toml
        src/
          main.rs
```

## Adding a new tool

### 1. Create the crate

```bash
mkdir -p tools/rust/crates/my-tool/src
```

### 2. Write `Cargo.toml`

Use the Write tool to create `tools/rust/crates/my-tool/Cargo.toml`:

```toml
[package]
name = "my-tool"
version = "0.1.0"
edition = "2021"
description = "What this tool does"

[dependencies]
clap = { version = "4", features = ["derive"] }
```

The workspace `members = ["crates/*"]` glob automatically picks up new crates.

### 3. Write the source

Use the Write tool to create `tools/rust/crates/my-tool/src/main.rs` with a `clap` CLI.

Convention: accept `--repo-root <path>` as the first argument for locating repo files.

### 4. Build

```bash
cargo build --release --manifest-path tools/rust/Cargo.toml
```

### 5. Create the shell wrapper

Use the Write tool to create `tools/my-tool` (extensionless, matching the audit repo convention):

```bash
#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
BINARY="$SCRIPT_DIR/rust/target/release/my-tool"

if [ ! -x "$BINARY" ]; then
    echo "Pre-built binary not found, building..." >&2
    cargo build --release --manifest-path "$SCRIPT_DIR/rust/Cargo.toml" >&2
fi

exec "$BINARY" --repo-root "$REPO_ROOT" "$@"
```

### 6. Test

```bash
bash tools/my-tool --help
```

## Conventions

- **Use `clap` derive** for CLI argument parsing
- **Accept `--repo-root`** to locate repo files relative to the workspace root
- **Shell wrappers** — invoked as `bash tools/my-tool`
- **Commit `Cargo.lock`** for reproducible CI builds
- **Pre-build in CI** — the orchestrator workflow builds all tools before the session starts
- **Keep dependencies minimal** — each tool should be focused and fast to compile
- **`serde_json`** is the standard crate for JSON parsing (already in workspace)

## Shared `state-schema` crate

The workspace includes a shared library crate at `tools/rust/crates/state-schema/` that provides strongly-typed serde structs for `docs/state.json`. All tools that read or write the state file should depend on this crate instead of parsing JSON manually.

### Adding it as a dependency

In your tool's `Cargo.toml`:

```toml
[dependencies]
state-schema = { path = "../state-schema" }
```

### Usage

```rust
use state_schema::StateJson;

let content = std::fs::read_to_string("docs/state.json")?;
let state: StateJson = serde_json::from_str(&content)?;
// Access typed fields: state.copilot_metrics, state.test_count, state.field_inventory, etc.
```

Key features:
- `#[serde(default)]` on all structs — tolerates missing fields
- `#[serde(flatten)] extra: BTreeMap<String, Value>` — preserves unknown fields on round-trip
- `SCHEMA_VERSION` constant for validation
- All tools that need state.json (metric-snapshot, cycle-status, housekeeping-scan, pipeline-check, check-field-inventory) use this crate

### When to update state-schema

When you add a new top-level or nested field to `docs/state.json` that a Rust tool needs to read, add the corresponding struct field to `state-schema/src/lib.rs`. If no Rust tool needs it yet, the `#[serde(flatten)] extra` field will capture it automatically.

## When to create a tool

**Tools are the default.** Create a tool when you notice:
- Any manual process you've performed more than once
- Complex JSON processing that's error-prone with manual jq queries
- Verification or validation checks that should be automated
- Data extraction patterns from state files or API responses
- Any task blocked by sandbox restrictions on existing tools (like `jq -f`)
- **Groundwork for reasoning tasks** — even tasks requiring judgment benefit from tools that gather and structure the inputs (e.g., a tool that presents a summary of what changed since last cycle, so the orchestrator can focus on deciding what to do rather than collecting data)

If in doubt, build the tool. A small Rust tool takes minutes to create and saves time on every future cycle. Dispatch non-trivial tools to the Copilot coding agent — describe the tool's purpose, inputs, outputs, and constraints in an issue spec.

## Permissions

The orchestrator has `Bash(cargo *)` and `Bash(bash *)` permissions, so it can:
- Build tools: `cargo build --release --manifest-path tools/rust/Cargo.toml`
- Run tools via wrapper: `bash tools/my-tool --help`
- Run tools directly: `tools/rust/target/release/my-tool --repo-root .`

These permissions are configured in both `.claude/settings.local.json` (local) and `.github/workflows/orchestrator.yml` (CI).
