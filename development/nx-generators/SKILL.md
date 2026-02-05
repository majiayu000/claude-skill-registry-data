---
name: nx-generators
description: Run Nx generators to create new projects, libraries, components. Use when user needs to generate code, scaffold projects, or understand generator options.
allowed-tools: Bash, Glob, Grep, Read
---

# Nx Generators

## Finding and Installing new plugins

- List plugins: `pnpm nx list`
- Install plugins `pnpm nx add <plugin>`. Example: `pnpm nx add @nx/react`.

## Commands

- List generators for plugin: `pnpm nx list @nx/react`
- Generator help: `pnpm nx g @nx/react:application --help`
- Dry run: `pnpm nx g @nx/react:application myapp --dry-run`
- Execute: `pnpm nx g @nx/react:application myapp`

## Workflow

1. Identify which plugin has needed generator
2. Check generator options with `--help`
3. Use `--dry-run` to preview changes
4. Execute generator
5. Run `pnpm nx format:write` after generation
