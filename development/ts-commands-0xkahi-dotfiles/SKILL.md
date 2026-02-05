---
name: ts-commands
description: >- 
  Determine package manager, workspace configuration, and available commands in TypeScript/JavaScript projects.
  Use when agent needs to understand how to run commands in a TS/JS project, including 
  (1) Detecting the correct package manager (npm/yarn/pnpm/bun),
  (2) Understanding workspace/monorepo setups,
  (3) Finding available scripts across packages,
  (4) Determining the correct command syntax for running development scripts
---

# Ts Commands 

Analyze TypeScript/JavaScript projects to determine the correct commands for running scripts, managing dependencies, and working with workspaces.

## Workflow

Analyzing a project involves these steps:

1. Detect package manager
2. Analyze workspace configuration (if applicable)
3. Discover available scripts
4. Determine the correct commands to run

### Step 1: Detect Package Manager

Check in this order:

**1. packageManager field in root package.json:**
```json
{
  "packageManager": "pnpm@8.0.0"
}
```

**2. Lock files in root directory:**
- `pnpm-lock.yaml` → pnpm
- `yarn.lock` → yarn
- `bun.lockb` → bun
- `package-lock.json` → npm

**3. Workspace configuration files:**
- `pnpm-workspace.yaml` → pnpm
- Check `package.json` for workspace field (could be npm/yarn/pnpm)

**If multiple lock files exist:**
1. Prioritize packageManager field
2. Use most recently modified lock file
3. Note the inconsistency

### Step 2: Analyze Workspace Configuration

**Check for workspace setup in root package.json:**
```json
{
  "workspaces": ["packages/*", "apps/*"]
}
```

**Or pnpm-workspace.yaml:**
```yaml
packages:
  - 'packages/*'
  - 'apps/*'
```

**Detect monorepo tools:**
- `turbo.json` → Turborepo
- `nx.json` → Nx
- `lerna.json` → Lerna

**Find workspace packages:**
1. Use Glob tool with workspace patterns (e.g., `packages/*/package.json`)
2. Read each package.json to get package names
3. Map workspace structure

For detailed workspace configuration patterns, see [references/workspace-configs.md](references/workspace-configs.md)

### Step 3: Discover Available Scripts

**1. Find all package.json files:**
- Root: `package.json`
- Workspaces: Based on patterns from Step 2

**2. Extract scripts from each package.json:**
```json
{
  "scripts": {
    "dev": "vite",
    "build": "tsc && vite build",
    "test": "vitest",
    "lint": "eslint .",
    "typecheck": "tsc --noEmit"
  }
}
```

**3. Identify common script types:**
- Development: `dev`, `start`, `serve`
- Building: `build`, `compile`, `bundle`
- Testing: `test`, `test:watch`, `test:coverage`
- Linting: `lint`, `lint:fix`
- Formatting: `format`, `format:check`
- Type checking: `typecheck`, `type-check`
- Cleaning: `clean`, `clean:dist`

### Step 4: Determine Commands to Run

**Command syntax by package manager:**

**npm:**
```bash
npm run <script>                    # Run script
npm run <script> -w <workspace>     # Run in specific workspace
npm run <script> --workspaces       # Run in all workspaces
```

**yarn (v1 classic):**
```bash
yarn <script>                       # Run script
yarn workspace <name> <script>      # Run in workspace
yarn workspaces run <script>        # Run in all workspaces
```

**yarn (v2+ berry):**
```bash
yarn <script>                       # Run script
yarn workspace <name> <script>      # Run in workspace
yarn workspaces foreach <script>    # Run in all workspaces
```

**pnpm:**
```bash
pnpm <script>                       # Run script (or pnpm run <script>)
pnpm --filter <name> <script>       # Run in workspace
pnpm -r <script>                    # Run in all workspaces (recursive)
pnpm --parallel -r <script>         # Run in all workspaces in parallel
```

**bun:**
```bash
bun run <script>                    # Run script (or bun <script>)
bun --filter <name> run <script>    # Run in workspace
bun run --filter "*" <script>       # Run in all workspaces
```

For version-specific differences and advanced features, see [references/package-managers.md](references/package-managers.md)

## Command Determination Output Format

Provide commands in this format:

```
Package Manager: <detected-pm> <version-if-available>
Workspace Setup: <yes/no>
Monorepo Tool: <tool-name-if-detected>

Available Commands:

Root-level:
  <pm-command> dev          # Start development server
  <pm-command> build        # Build for production
  <pm-command> test         # Run tests
  <pm-command> lint         # Lint code
  <pm-command> typecheck    # Check TypeScript types

Workspace-specific:
  <workspace-name> (<path>):
    <pm-command> --filter <workspace-name> dev
    <pm-command> --filter <workspace-name> build
    <pm-command> --filter <workspace-name> test

  <workspace-name-2> (<path>):
    <pm-command> --filter <workspace-name-2> dev
    ...

Run across all workspaces:
  <pm-command> -r <script>  # For pnpm
  <pm-command> workspaces run <script>  # For yarn/npm
```

## Common Patterns

### Workspace Protocols in Dependencies

When reading package.json dependencies, recognize these workspace references:

**pnpm:**
- `"workspace:*"` → Latest version in workspace
- `"workspace:^"` → Semver caret range
- `"workspace:~"` → Semver tilde range

**yarn:**
- `"workspace:*"` → Workspace protocol (v2+)
- `"link:../package-name"` → Local link

**npm/general:**
- `"file:../package-name"` → Local file dependency

### Build Tool Detection

Identify build tools by configuration files:
- `tsconfig.json` → TypeScript
- `vite.config.ts/js` → Vite
- `webpack.config.js` → Webpack
- `rollup.config.js` → Rollup
- `esbuild.config.js` → esbuild
- `turbo.json` → Turborepo
- `nx.json` → Nx

### Monorepo-Specific Commands

**Turborepo:**
```bash
turbo run <script>                  # Run with caching
turbo run <script> --filter=<name>  # Run in specific package
```

**Nx:**
```bash
nx run <project>:<target>           # Run target in project
nx run-many --target=<target>       # Run in multiple projects
```

**Lerna:**
```bash
lerna run <script>                  # Run in all packages
lerna run <script> --scope=<name>   # Run in specific package
```

These tools typically wrap the underlying package manager commands.

## Edge Cases

### No Scripts Found
- Check if package.json exists
- Verify it's not a workspace-only root (scripts might be in workspace packages)
- Look for alternative task runners (Makefile, Taskfile, justfile)

### Script Dependencies
Some scripts call other scripts:
```json
{
  "scripts": {
    "build": "npm run clean && npm run compile",
    "clean": "rm -rf dist",
    "compile": "tsc"
  }
}
```

Note these dependencies when showing available commands.

### Version-Specific Syntax
- Yarn v1 vs v2+ have different commands
- pnpm versions <7 may have different flags
- Check packageManager field for version hints

Refer to [references/package-managers.md](references/package-managers.md) for version-specific details.

### Environment-Specific Scripts
Recognize scripts that may have environment variants:
```json
{
  "scripts": {
    "dev": "vite",
    "dev:prod": "vite --mode production",
    "test": "vitest",
    "test:ci": "vitest run --coverage"
  }
}
```

Include these variants when listing available commands.
