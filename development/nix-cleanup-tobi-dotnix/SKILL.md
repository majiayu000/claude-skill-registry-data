---
name: nix-cleanup
description: CI workflow checks and code cleanup tools
---

# NixOS CI and Code Cleanup

This skill provides context about the CI workflow and code cleanup tools used in this repository.

## CI Workflow

The CI is defined in @.github/workflows/ci.yml and runs three main checks:

1. **Flake Check** (`nix flake check --no-build`)
   - Validates flake syntax and structure
   - Checks all NixOS configurations
   - Ensures all outputs are buildable
   - Does NOT build derivations (fast check)

2. **Statix** (`nix run nixpkgs#statix -- check .`)
   - Lints Nix code for common issues and anti-patterns
   - Suggests best practices and improvements
   - Can auto-fix issues with `statix fix`

3. **Deadnix** (`nix run nixpkgs#deadnix -- .`)
   - Detects unused code and bindings
   - Finds dead `let` bindings, function arguments, etc.
   - Can auto-fix with `deadnix -e`

## Running Checks Locally

Always run these before committing:

```bash
# Quick check (no builds)
nix flake check --no-build

# Lint for anti-patterns
nix run nixpkgs#statix -- check .

# Find dead code
nix run nixpkgs#deadnix -- .
```

## Auto-fixing Issues

```bash
# Fix statix issues
nix run nixpkgs#statix -- fix .

# Remove dead code
nix run nixpkgs#deadnix -- -e .
```

## Common Issues

### Unused Let Bindings
```nix
# Bad - 'foo' is never used
let
  foo = "unused";
  bar = "used";
in bar

# Good - removed unused binding
let
  bar = "used";
in bar
```

### Unused Function Parameters
```nix
# Bad - 'pkgs' is never used
{ pkgs, lib, ... }: {
  imports = [ ];
}

# Good - removed from signature
{ lib, ... }: {
  imports = [ ];
}
```

## Best Practices

1. Always run `/nix-check` slash command after making changes
2. Use `statix` and `deadnix` to keep code clean
3. CI runs on every push and PR
4. All checks must pass before merging
