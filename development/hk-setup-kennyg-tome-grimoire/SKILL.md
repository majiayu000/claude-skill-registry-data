---
name: hk-setup
description: Set up hk (git hook manager) with pre-commit hooks for any project. Detects project type (Python, JS/TS, Go, Rust, etc.) and configures appropriate linters/formatters. Use when user wants to add pre-commit hooks, set up hk, or configure linting for a project.
license: MIT
compatibility: Requires hk to be installed (brew install hk or mise use hk). Works with Claude Code and similar agents.
metadata:
  author: kenny
  version: "1.1"
---

# hk Setup

Configure [hk](https://hk.jdx.dev) git hooks with appropriate linters for any project.

## When to Use This Skill

- User asks to set up pre-commit hooks
- User wants to add linting/formatting to a project
- User mentions hk, git hooks, or pre-commit
- User wants to enforce code quality on commits

## Prerequisites

```bash
# Install hk (one of these)
brew install hk
mise use -g hk
```

## Workflow

### 1. Detect Project Type

Look for these files to identify the project:

| File | Project Type | Recommended Linters |
|------|--------------|---------------------|
| `pyproject.toml`, `*.py` | Python | ruff, ruff_format |
| `package.json`, `*.ts` | JavaScript/TypeScript | biome (or eslint + prettier) |
| `go.mod`, `*.go` | Go | go_fmt, golangci_lint |
| `Cargo.toml`, `*.rs` | Rust | rustfmt, cargo_clippy |
| `Package.swift`, `*.swift` | Swift | swiftlint, swiftformat |
| `*.sh`, `*.bash` | Shell | shellcheck, shfmt |
| `Dockerfile` | Docker | hadolint |
| `*.pkl` | Pkl configs | pkl |

### 2. Check Available Tools

```bash
hk builtins  # List all built-in linters
```

See [references/builtins.md](references/builtins.md) for full catalog. Key builtins:

| Language | Recommended Builtins |
|----------|---------------------|
| Python | `ruff`, `ruff_format` |
| JS/TS | `biome` or `eslint` + `prettier` |
| Go | `go_fmt`, `go_imports`, `golangci_lint` |
| Rust | `rustfmt`, `cargo_clippy` |
| Shell | `shellcheck`, `shfmt` |

### 3. Generate hk.pkl

Create `hk.pkl` in project root. Always use version-pinned imports:

```pkl
amends "package://github.com/jdx/hk/releases/download/v1.28.0/hk@1.28.0#/Config.pkl"
import "package://github.com/jdx/hk/releases/download/v1.28.0/hk@1.28.0#/Builtins.pkl"

local linters = new Mapping<String, Step> {
    // Add linters here based on project type
}

hooks {
    ["pre-commit"] {
        fix = true
        stash = "git"
        steps = linters
    }
    ["pre-push"] {
        steps = linters
    }
    ["fix"] {
        fix = true
        steps = linters
    }
    ["check"] {
        steps = linters
    }
}
```

### 4. Install & Test

```bash
hk validate       # Check config syntax
hk install        # Install git hooks
hk check --all    # Run all checks
hk fix --all      # Auto-fix issues
```

## Project Templates

### Python (ruff + ty)

```pkl
local linters = new Mapping<String, Step> {
    ["ruff"] = Builtins.ruff
    ["ruff-format"] = Builtins.ruff_format
    ["ty"] {
        glob = "**/*.py"
        check = "ty check"
    }
    ["pkl"] = Builtins.pkl
}
```

### JavaScript/TypeScript (eslint + prettier)

```pkl
local linters = new Mapping<String, Step> {
    ["eslint"] = Builtins.eslint
    ["prettier"] = Builtins.prettier
    ["pkl"] = Builtins.pkl
}
```

### JavaScript/TypeScript (biome)

Biome is a fast all-in-one linter+formatter. Use instead of eslint+prettier for new projects:

```pkl
local linters = new Mapping<String, Step> {
    ["biome"] = Builtins.biome
    ["pkl"] = Builtins.pkl
}
```

### JavaScript/TypeScript (oxc)

Oxlint + oxfmt from the [oxc project](https://oxc.rs). Oxfmt is alpha but very fast:

```pkl
local linters = new Mapping<String, Step> {
    ["oxlint"] = Builtins.ox_lint
    ["oxfmt"] {
        glob = "**/*.{ts,tsx,js,jsx,json,md}"
        check = "oxfmt --check {{files}}"
        fix = "oxfmt {{files}}"
    }
    ["pkl"] = Builtins.pkl
}
```

Install: `npm install -g oxfmt`

### Go

```pkl
local linters = new Mapping<String, Step> {
    ["gofmt"] = Builtins.gofmt
    ["goimports"] = Builtins.goimports
    ["golangci-lint"] = Builtins.golangci_lint
    ["pkl"] = Builtins.pkl
}
```

### Rust

```pkl
local linters = new Mapping<String, Step> {
    ["rustfmt"] = Builtins.rustfmt
    ["clippy"] = Builtins.clippy
    ["pkl"] = Builtins.pkl
}
```

### Swift (swiftlint + swiftformat)

```pkl
local linters = new Mapping<String, Step> {
    ["swiftlint"] = Builtins.swiftlint
    ["swiftformat"] {
        glob = "**/*.swift"
        check = "swiftformat --lint {{files}}"
        fix = "swiftformat {{files}}"
    }
    ["pkl"] = Builtins.pkl
}
```

### Shell

```pkl
local linters = new Mapping<String, Step> {
    ["shellcheck"] = Builtins.shellcheck
    ["shfmt"] = Builtins.shfmt
    ["pkl"] = Builtins.pkl
}
```

### Docker

```pkl
local linters = new Mapping<String, Step> {
    ["hadolint"] = Builtins.hadolint
    ["pkl"] = Builtins.pkl
}
```

## Universal Linters

These work for any project. Add them directly to your linters mapping:

```pkl
local linters = new Mapping<String, Step> {
    // Language-specific linters...
    ["ruff"] = Builtins.ruff

    // Universal linters (add to any project)
    ["typos"] = Builtins.typos                             // Spell checker
    ["trailing-whitespace"] = Builtins.trailing_whitespace // Remove trailing spaces
    ["newlines"] = Builtins.newlines                       // Ensure final newline
}
```

Note: Pkl Mappings don't support `+` concatenation. Define all linters in a single mapping.

Other useful universal builtins:
- `check_merge_conflict` - Prevent committing merge conflict markers
- `detect_private_key` - Prevent committing private keys
- `check_added_large_files` - Warn about large files

## Custom Steps

For tools without builtins, define custom steps:

```pkl
["my-linter"] {
    glob = "**/*.ext"           // Files to match
    check = "my-tool check {{files}}"  // Check command
    fix = "my-tool fix {{files}}"      // Optional fix command
}
```

### Step Options

| Option | Description |
|--------|-------------|
| `glob` | File patterns to match |
| `check` | Command to run for checking |
| `fix` | Command to run for fixing (optional) |
| `exclusive` | Run in isolation (no parallel) |
| `batch` | Process files in batches |
| `stomp` | Allow file modifications during check |

## Environment Variables

If tools are in a venv or non-standard location:

```pkl
env {
    ["PATH"] = ".venv/bin:\(read("env:PATH"))"
}
```

Or better: install tools globally via brew/mise.

## Troubleshooting

### Tool not found

```bash
# Check if tool is in PATH
which ruff

# Install globally
brew install ruff
# or
mise use -g ruff
```

### Config validation failed

```bash
hk validate
# Check Pkl syntax errors in output
```

### Hooks not running

```bash
# Reinstall hooks
hk install

# Check hook files exist
ls -la .git/hooks/pre-commit
```

## Examples

### User asks to add pre-commit hooks

1. Check project type (look for pyproject.toml, package.json, etc.)
2. Check what tools are available (`hk builtins`, `which ruff`)
3. Create appropriate hk.pkl
4. Run `hk validate && hk install`
5. Test with `hk check --all`
6. Fix issues with `hk fix --all`

### User has existing linter config

1. Read existing config (ruff.toml, .eslintrc, etc.)
2. Use matching hk builtins
3. Add any custom tools as custom steps
