---
name: nix-dev-shell
description: Automatically detects Nix flakes and runs commands in a dev shell environment. Use when running build, test, or development commands in projects with flake.nix. Ensures commands run with proper Nix dependencies loaded.
allowed-tools: Read, Grep, Glob, Bash
---

# Nix Dev Shell Auto-Activation

## Overview

This skill automatically detects when a Nix flake is present and ensures development commands run inside the appropriate Nix dev shell environment, providing access to all declared dependencies.

## Core Workflow

### 1. Flake Detection

Before running any development command, check for a flake:

```bash
# Check if flake.nix exists in current directory or parent directories
if [ -f flake.nix ]; then
    echo "Flake detected - will use nix dev shell"
fi
```

Use the Glob tool to detect flakes:
```
pattern: **/flake.nix
```

### 2. Dev Shell Activation

When a flake is detected, wrap commands using one of these methods:

**Method 1: nix develop -c (recommended for flakes)**
```bash
nix develop -c <command> <args>
```

**Method 2: nix shell (alternative syntax)**
```bash
nix shell --command <command> <args>
```

**Method 3: Multiple commands**
```bash
nix develop --command bash -c "command1 && command2"
```

**Method 4: Legacy nix-shell (for shell.nix)**
```bash
nix-shell --run "<command> <args>"
```

### 3. Commands That Should Use Dev Shell

Always run these in dev shell when flake.nix exists:
- Build commands: `cargo build`, `npm run build`, `make`, `go build`
- Test commands: `cargo test`, `npm test`, `pytest`, `go test`
- Development servers: `npm run dev`, `cargo run`
- Package managers: `npm install`, `cargo add`, `pip install`
- Formatters/linters: `rustfmt`, `eslint`, `black`, `gofmt`
- Custom project scripts defined in flake.nix

### 4. Commands That Should NOT Use Dev Shell

These Nix commands should run directly (not in dev shell):
- `nix build`
- `nix flake check`
- `nix fmt`
- `nix develop` (obviously)
- `nh os switch`
- `nh os build`

## Usage Patterns

### Pattern 1: Build/Test Commands

```bash
# User asks: "run the tests"
nix develop -c cargo test

# User asks: "build the project"
nix develop -c npm run build
```

### Pattern 2: Multiple Commands

```bash
# User asks: "install dependencies and run tests"
nix develop --command bash -c "npm install && npm test"
```

### Pattern 3: Simple Approach

```bash
# Alternative using nix shell
nix shell --command make test

# Or for legacy shell.nix
nix-shell --run "cargo build"
```

## Decision Tree

```
Is flake.nix present?
├─ YES
│  ├─ Is it a Nix command (build, flake check, fmt)?
│  │  ├─ YES → Run directly (nix build, nix fmt, etc.)
│  │  └─ NO → Is it a dev/build/test command?
│  │     ├─ YES → Run in dev shell (nix develop -c <cmd>)
│  │     └─ NO → Ask user if command needs dev shell
└─ NO → Run command directly
```

## Examples

### Example 1: Rust Project

```bash
# User: "run cargo test"
# Skill behavior:

# Check for flake
[ -f flake.nix ] && {
    # Run in dev shell
    nix develop -c cargo test
}
```

### Example 2: Node.js Project

```bash
# User: "install packages and start dev server"
# Skill behavior:

nix develop --command bash -c "npm install && npm run dev"
```

### Example 3: NixOS Configuration

```bash
# User: "check the flake configuration"
# Skill behavior:

# This is a Nix command - run directly
nix flake check
```

### Example 4: Format Code

```bash
# User: "format the nix files"
# Skill behavior:

# nix fmt runs directly (not in dev shell)
nix fmt
```

## Important Notes

1. **Always detect flake first**: Use Glob or check for file existence before deciding
2. **Preserve user intent**: If user explicitly says "in dev shell" or "without dev shell", respect it
3. **Background processes**: For long-running commands (dev servers), consider using `run_in_background: true`
4. **Error handling**: If `nix develop` fails, suggest checking flake.nix or running `nix flake check`
5. **Project context**: Check CLAUDE.md for project-specific Nix commands and patterns

## When to Activate This Skill

- User mentions "build", "test", "run", "start", or similar development commands
- User asks to execute package manager commands (npm, cargo, pip, etc.)
- Working in a project directory with flake.nix
- User explicitly mentions "dev shell" or "nix develop"

## Integration with Project

This NixOS dotfiles repo has specific Nix commands documented in CLAUDE.md:
- `nh os switch --hostname=<name>` - Deploy NixOS config (run directly)
- `nix flake check` - Validate flake (run directly)
- `nix fmt` - Format Nix files (run directly)
- `nix build .#<output>` - Build specific output (run directly)

These are management commands and should NOT use dev shell.

## Troubleshooting

**Dev shell fails to start:**
```bash
# Check flake validity first
nix flake check

# Try with verbose output
nix develop --verbose
```

**Command not found in dev shell:**
- Check if the command is defined in flake.nix devShells
- Verify flake.lock is up to date: `nix flake update`

**Slow dev shell activation:**
- Consider using `nix develop --offline` if dependencies are already cached
- Use direnv integration for automatic shell activation (if available)
