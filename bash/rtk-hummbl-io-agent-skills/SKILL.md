---
name: rtk
description: >
  CLI proxy that compresses bash command outputs before agent reads them. Single
  Rust binary, zero dependencies, <10ms overhead, 60-90% fewer tokens on common
  dev commands. 100+ supported commands (git, grep, ls, cat, test runners, build
  tools, linters, package managers). Hook-based: auto-rewrites `git status` ->
  `rtk git status` before execution. Agent receives compact output without
  calling rtk explicitly. Use when user says "rtk", "rust token killer", "compress
  command output", "compact bash output", or wants CLI-level token compression
  (vs caveman-mode for prose, vs ponytail for code, vs headroom for full proxy).
  Source: rtk-ai/rtk (74K stars, Apache 2.0) — github.com/rtk-ai/rtk
license: Apache-2.0
version: 0.1.1
execution-mode: advisory
category: hummbl-research
status: candidate
---

# RTK — Rust Token Killer

CLI proxy. Compresses bash command output before agent reads it. Single Rust binary. <10ms overhead. 60-90% fewer tokens.

## What it does

Intercepts shell commands, compresses output, agent sees compact version. Hook-based — auto-rewrites commands, no explicit `rtk` call needed.

```
Without rtk:  agent --git status--> shell --> git --> full raw output --> agent
With rtk:     agent --git status--> RTK   --> git --> compact output  --> agent
```

## Prerequisites

Choose the install path for the current platform: use the Bash commands below
on Linux/macOS, or the release archive instructions on Windows. The preferred
Cargo path requires an installed Rust toolchain; the pinned installer path
requires Python 3 for its fail-closed script-hash check.

## Install

Choose one method.

### Cargo (preferred reproducible source build)

```bash
# v0.45.0 at an exact commit
cargo install --git https://github.com/rtk-ai/rtk \
  --rev b34be37caf3796b69a50952a28e60e32b5daad43 --locked
```

### Homebrew (convenient, current formula version)

```bash
brew install rtk
```

### Pinned release installer (Linux/macOS)

```bash
# Pinned release installer (Linux/macOS) — download, verify, then execute locally.
# Update the version, commit, and SHA-256 together when upgrading.
install_rtk_pinned() (
  set -eu
  rtk_version="v0.45.0"
  rtk_commit="b34be37caf3796b69a50952a28e60e32b5daad43"
  rtk_installer_sha256="d6eb73a772903e13ff34ee1be8a8b24e896ba9a978f20d2279a08b4083ea6f77"
  rtk_installer="$(mktemp)"
  trap 'rm -f -- "$rtk_installer"' EXIT
  curl -fsSLo "$rtk_installer" \
    "https://raw.githubusercontent.com/rtk-ai/rtk/${rtk_commit}/install.sh"
  python3 -c 'import hashlib, pathlib, sys; p = pathlib.Path(sys.argv[1]); actual = hashlib.sha256(p.read_bytes()).hexdigest(); expected = sys.argv[2]; sys.exit(0 if actual == expected else f"installer SHA-256 mismatch: {actual}")' \
    "$rtk_installer" "$rtk_installer_sha256"
  RTK_VERSION="$rtk_version" sh "$rtk_installer"
)
install_rtk_pinned
```

### Windows

```text
# Windows: download rtk-x86_64-pc-windows-msvc.zip from releases
# Extract to PATH (e.g. C:\Users\<you>\.local\bin)
# Run from Command Prompt / PowerShell / Windows Terminal — do not double-click .exe
```

Verify:
```bash
rtk --version   # Pinned Cargo/installer paths should show "rtk 0.45.0"; Homebrew may be newer
rtk gain        # Savings dashboard
```

Name collision warning: another "rtk" (Rust Type Kit) exists on crates.io. If `rtk gain` fails, use the pinned Cargo command above.

## Init for agent

```bash
rtk init -g                     # Claude Code / Copilot (default)
rtk init -g --gemini            # Gemini CLI
rtk init -g --codex             # Codex (OpenAI)
rtk init -g --agent cursor      # Cursor
rtk init -g --agent windsurf    # Windsurf
rtk init --agent cline          # Cline / Roo Code
rtk init --agent kilocode       # Kilo Code
rtk init --agent antigravity    # Google Antigravity
rtk init --agent kimi           # Kimi AI
rtk init -g --agent pi          # Pi
rtk init --agent hermes         # Hermes
rtk init -g --agent droid       # Factory Droid
```

Restart agent after init. Test: `git status` — auto-rewritten to `rtk git status`.

Important: hook only runs on Bash tool calls. Built-in tools (Read, Grep, Glob) do not pass through. For those workflows, use shell commands (`cat`/`head`/`tail`, `rg`/`grep`, `find`) or call `rtk read`, `rtk grep`, `rtk find` directly.

## Supported commands (100+)

### Files
```bash
rtk ls .                        # Compact directory tree
rtk read file.rs                # Smart file reading (signatures + structure)
rtk read file.rs -l aggressive  # Signatures only (strips bodies)
rtk smart file.rs               # 2-line heuristic code summary
rtk find "*.rs" .               # Compact find results
rtk grep "pattern" .            # Grouped search results
rtk diff file1 file2            # Condensed diff
```

### Git
```bash
rtk git status                  # Compact status
rtk git log -n 10               # One-line commits
rtk git diff                    # Condensed diff
rtk git add                     # -> "ok"
rtk git commit -m "msg"         # -> "ok abc1234"
rtk git push                    # -> "ok main"
rtk git pull                    # -> "ok 3 files +10 -2"
```

### GitHub CLI
```bash
rtk gh pr list                  # Compact PR listing
rtk gh pr view 42               # PR details + checks
rtk gh issue list               # Compact issue listing
rtk gh run list                 # Workflow run status
```

### Test runners
```bash
rtk pytest                      # Python tests (-90%, failures only)
rtk cargo test                  # Cargo tests (-90%)
rtk go test                     # Go tests (NDJSON, -90%)
rtk jest                        # Jest compact (failures only)
rtk vitest                      # Vitest compact (failures only)
rtk playwright test             # E2E results (failures only)
rtk rspec                       # RSpec (JSON, -60%+)
rtk rake test                   # Ruby minitest (-90%)
rtk sbt test                    # ScalaTest (-90%)
rtk test <cmd>                  # Generic test wrapper (-90%)
rtk err <cmd>                   # Filter errors only from any command
```

### Build & lint
```bash
rtk lint                        # ESLint grouped by rule/file
rtk tsc                         # TypeScript errors grouped by file
rtk cargo build                 # Cargo build (-80%)
rtk cargo clippy                # Cargo clippy (-80%)
rtk ruff check                  # Python linting (JSON, -80%)
rtk golangci-lint run           # Go linting (JSON, -85%)
rtk rubocop                     # Ruby linting (JSON, -60%+)
rtk next build                  # Next.js build compact
rtk prettier --check .          # Files needing formatting
rtk sbt compile                 # Compilation errors only (-75%)
```

### Package managers
```bash
rtk pnpm list                   # Compact dependency tree
rtk pip list                    # Python packages (auto-detect uv)
rtk pip outdated                # Outdated packages
rtk bundle install              # Ruby gems (strip noise)
rtk uv run pytest               # Preserve uv env, keep program output
```

## Four compression strategies

1. **Smart Filtering** — removes noise (comments, whitespace, boilerplate)
2. **Grouping** — aggregates similar items (files by dir, errors by type)
3. **Truncation** — keeps relevant context, cuts redundancy
4. **Deduplication** — collapses repeated log lines with counts

## Savings explained

RTK cuts up to 90% of bash output agent reads. Not same as cutting bill 90%. Bash output = one contributor to input tokens. Input tokens = part of bill (also output tokens). Reduction dilutes at every step.

Token counts estimated as `bytes / 4` — RTK ships no tokenizer. Percentages reliable, absolute numbers approximate.

## When to use

- Bash command output bloating agent context
- Git operations, test runs, build output, lint results
- Want zero-code-change compression (hook-based)
- Rust-grade performance (<10ms, <5MB)

## When NOT to use

- Already using headroom for full proxy compression (overlaps — pick one)
- Output prose compression only (use caveman-mode)
- Code minimization only (use ponytail)
- Non-CLI token sources (RAG, conversation history — use headroom)

## Changelog

- **0.1.1 (2026-08-31):** Removed download-to-shell pipelines; pinned Cargo and installer paths to the v0.45.0 commit and added fail-closed installer SHA-256 verification.
- **0.1.0:** Initial fleet skill.

## Pair with

- **caveman-mode** — rtk cuts input (command output), caveman cuts output (prose). Both = max.
- **ponytail** — rtk compresses what agent reads, ponytail minimizes what agent writes (code).
- **headroom** — rtk = CLI commands only, headroom = full proxy (RAG, logs, files, history). Use both if CLI is dominant token source.
- **caveman-ponytail** — all four together = brain big, mouth small, code small, context small, commands small.

## Boundaries

RTK = CLI command output compression only. Does not compress prompts, conversation history, RAG chunks, or model output prose. Hook-based — only intercepts Bash tool calls, not built-in Read/Grep/Glob. For those, call `rtk read`/`rtk grep`/`rtk find` explicitly.
