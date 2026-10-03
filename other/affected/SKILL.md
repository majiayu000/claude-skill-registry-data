---
name: affected
description: Analyze which monorepo packages and apps are affected by current changes
type: analysis
version: v0.1
argument-hint: "[optional: specific commit range or branch to analyze]"
---

# Affected

Determine which packages and apps in the monorepo are affected by current changes. Useful before committing, testing, or deploying to know the blast radius.

## Process

1. **Determine the change set:**
   - If `$ARGUMENTS` specifies a commit range or branch, use `git diff` for that range.
   - Otherwise, use `git diff HEAD` (staged + unstaged changes).
   - If no changes exist, check for unpushed commits with `git log @{u}..HEAD`.

2. **Read the monorepo structure:**
   - Check for `turbo.json`, `pnpm-workspace.yaml`, `lerna.json`, or `package.json` workspaces to understand the package graph.
   - List all packages/apps and their locations.

3. **Map changes to packages:**
   - For each changed file, determine which package it belongs to.
   - List directly changed packages.

4. **Compute transitive dependents:**
   - Read `package.json` of each directly changed package to find its `name`.
   - Search other packages' `package.json` files for dependencies on the changed packages.
   - Build the full dependency chain (direct → transitive).

5. **Check for cross-cutting changes:**
   - Root config changes (`tsconfig.json`, `turbo.json`, `.env*`, `tailwind.config.*`) affect all packages.
   - Shared package changes (e.g., `packages/ui`, `packages/config`) cascade to consumers.

6. **Identify what to test:**
   - If Turborepo: suggest `turbo run test --filter=...[HEAD~1]` or equivalent.
   - Otherwise: list the test commands for each affected package.

## Output

### Directly Changed
- `packages/foo` — 3 files changed (briefly what)
- `apps/bar` — 1 file changed (briefly what)

### Transitively Affected
- `apps/web` — depends on `packages/foo`
- `apps/admin` — depends on `packages/foo` via `packages/shared`

### Cross-Cutting
- `tsconfig.base.json` changed — affects all TypeScript packages

### Recommended Test Commands
```bash
# commands to test affected packages
```

## Constraints
- Do not run tests — only analyze and recommend.
- If the monorepo tool is Turborepo, prefer Turbo-native filtering where possible.
- Keep the output concise — list packages, not individual files (unless scoped to a single package).


## Default Shipping Contract

Follow the shared shipping contract convention in CLAUDE.md.
