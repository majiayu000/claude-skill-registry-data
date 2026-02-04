---
name: nix-check
description: Check and validate NixOS configuration. Use when asked to check,
  validate, lint, or verify the nix config, flake, or configuration files.
---

# Nix Configuration Checker

## When to Use
Use this skill when the user asks to check, validate, lint, or verify the nix configuration.

## Instructions

Run the validation scripts in sequence:

1. **Format Check** - Verify code formatting:
   ```bash
   ./scripts/fmt.sh --check
   ```

2. **Lint Check** - Check for linting issues and dead code:
   ```bash
   ./scripts/lint.sh
   ```

3. **Flake Check** - Validate flake and do a dry-run build:
   ```bash
   ./scripts/check.sh
   ```

## Reporting Results

- If all checks pass, report success
- If any check fails, report which check failed and show the relevant error output
- Suggest fixes for common issues (formatting can be auto-fixed with `./scripts/fmt.sh`)
