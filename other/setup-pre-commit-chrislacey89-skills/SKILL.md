---
name: setup-pre-commit
description: "Infrastructure skill for setting up commit-time quality gates. Use when a repo needs Lefthook-based pre-commit hooks for formatting, linting, type checking, and tests. Supports downstream /execute and /pre-merge, but is not part of the normal feature-delivery pipeline."
---

# Setup Pre-Commit Hooks

## Invocation Position

This is an infrastructure skill, not a normal feature-delivery stage.

Use `/setup-pre-commit` when a project needs commit-time formatting, linting, type checking, and test hooks.

Do not use it as part of the default feature pipeline. It prepares the repo so later `/execute` and `/pre-merge` steps have stronger feedback loops.

## What This Sets Up

- **Lefthook** for git hook management (fast, zero-dependency, config-as-code)
- **Formatting + linting** on staged files (Biome preferred; Prettier, ESLint, or others supported)
- **Typecheck** and **test** scripts in the pre-commit hook

## Steps

### 1. Detect Package Manager

Check for `pnpm-lock.yaml` (pnpm), `package-lock.json` (npm), `yarn.lock` (yarn), `bun.lockb` (bun). Use whichever is present. Default to npm if unclear.

Store the detected package manager — it's used for all install and run commands below.

### 2. Detect Existing Formatter/Linter

Before installing anything, check what's already in the project:

```bash
# Check package.json for existing tools
cat package.json | grep -E "biome|prettier|eslint|oxlint|dprint" 2>/dev/null
# Check for config files
ls biome.json biome.jsonc .prettierrc .prettierrc.* prettier.config.* .eslintrc* eslint.config.* 2>/dev/null
```

**If an existing formatter/linter is detected:** use it. Don't install a competing tool.

**If nothing is detected:** recommend Biome (single tool for formatting + linting, fast, zero-config defaults) and confirm with the user before installing.

Ask: "No formatter/linter detected. I'd recommend Biome — it handles both formatting and linting in one tool, is very fast, and works out of the box. Want to go with Biome, or would you prefer Prettier, ESLint, or something else?"

### 3. Install Dependencies

Install as devDependencies using the detected package manager:

**Lefthook (always):**
```bash
# pnpm
pnpm add -D lefthook

# npm
npm install -D lefthook

# yarn
yarn add -D lefthook

# bun
bun add -D lefthook
```

**Formatter/linter (based on detection or user choice):**

| Tool | Install | Config file |
|------|---------|-------------|
| Biome (preferred) | `@biomejs/biome` | `biome.json` |
| Prettier | `prettier` | `.prettierrc` |
| ESLint | `eslint` | `eslint.config.*` |
| Prettier + ESLint | `prettier eslint` | both |
| oxlint | `oxlint` | `oxlint.json` |
| dprint | `dprint` | `dprint.json` |

### 4. Initialize Lefthook

```bash
npx lefthook install
```

This creates the git hook symlinks. No `.husky/` directory, no `prepare` script needed — Lefthook manages hooks directly via `lefthook.yml`.

Add a `prepare` script to package.json so hooks are installed automatically for anyone who clones the repo:

```json
{
  "scripts": {
    "prepare": "lefthook install"
  }
}
```

### 5. Create `lefthook.yml`

Create `lefthook.yml` at the repo root. The configuration depends on which formatter/linter was detected or chosen.

**With Biome (preferred):**

```yaml
pre-commit:
  parallel: true
  commands:
    format-and-lint:
      glob: "*.{js,ts,jsx,tsx,json,css}"
      run: npx @biomejs/biome check --write --staged {staged_files}
      stage_fixed: true
    typecheck:
      run: {package_manager} run typecheck
    test:
      run: {package_manager} run test
```

**With Prettier:**

```yaml
pre-commit:
  parallel: true
  commands:
    format:
      glob: "*.{js,ts,jsx,tsx,json,css,md,yml,yaml}"
      run: npx prettier --write {staged_files}
      stage_fixed: true
    typecheck:
      run: {package_manager} run typecheck
    test:
      run: {package_manager} run test
```

**With ESLint:**

```yaml
pre-commit:
  parallel: true
  commands:
    lint:
      glob: "*.{js,ts,jsx,tsx}"
      run: npx eslint --fix {staged_files}
      stage_fixed: true
    typecheck:
      run: {package_manager} run typecheck
    test:
      run: {package_manager} run test
```

**With Prettier + ESLint:**

```yaml
pre-commit:
  parallel: true
  commands:
    format:
      glob: "*.{js,ts,jsx,tsx,json,css,md,yml,yaml}"
      run: npx prettier --write {staged_files}
      stage_fixed: true
    lint:
      glob: "*.{js,ts,jsx,tsx}"
      run: npx eslint --fix {staged_files}
      stage_fixed: true
    typecheck:
      run: {package_manager} run typecheck
    test:
      run: {package_manager} run test
```

**Adapt the config:**
- Replace `{package_manager}` with the detected package manager (pnpm, npm, yarn, bun)
- If the repo has no `typecheck` script in package.json, omit that command and tell the user
- If the repo has no `test` script in package.json, omit that command and tell the user
- Adjust `glob` patterns to match the project's file types

### 6. Create Formatter Config (if missing)

Only create if no config exists and the user chose to install a new tool.

**Biome (`biome.json`):**

```json
{
  "$schema": "https://biomejs.dev/schemas/1.9.4/schema.json",
  "organizeImports": {
    "enabled": true
  },
  "formatter": {
    "indentStyle": "space",
    "indentWidth": 2,
    "lineWidth": 80
  },
  "linter": {
    "enabled": true,
    "rules": {
      "recommended": true
    }
  }
}
```

**Prettier (`.prettierrc`):**

```json
{
  "useTabs": false,
  "tabWidth": 2,
  "printWidth": 80,
  "singleQuote": false,
  "trailingComma": "es5",
  "semi": true,
  "arrowParens": "always"
}
```

### 7. Verify

- [ ] `lefthook.yml` exists at repo root
- [ ] `prepare` script in package.json is `"lefthook install"`
- [ ] Formatter/linter config exists
- [ ] Run `npx lefthook run pre-commit` to verify hooks work
- [ ] No `.husky/` directory exists (if migrating from Husky, remove it)

### 8. Clean Up Husky (if migrating)

If the project previously used Husky:

```bash
# Remove Husky artifacts
rm -rf .husky
# Remove Husky from dependencies
{package_manager} remove husky lint-staged
# Remove .lintstagedrc if it exists and is no longer needed
rm -f .lintstagedrc .lintstagedrc.* lint-staged.config.*
```

Update the `prepare` script in package.json from `"husky"` to `"lefthook install"`.

### 9. Commit

Stage all changed/created files and commit with message:

`chore: add pre-commit hooks (lefthook + biome)` (or substitute the actual formatter name)

This will run through the new pre-commit hooks — a good smoke test that everything works.

## Why Lefthook over Husky

- **No node_modules dependency at hook runtime** — Lefthook hooks run directly, no `npx lint-staged` wrapper
- **Config as code** — `lefthook.yml` is declarative and version-controlled; Husky uses shell scripts in `.husky/`
- **Parallel execution** — runs formatting, typecheck, and tests in parallel by default
- **`{staged_files}` built-in** — no need for lint-staged as a separate dependency; Lefthook handles staged file filtering natively
- **`stage_fixed: true`** — automatically re-stages files after formatting fixes, no extra tooling
- **Glob filtering** — only runs tools on matching file types, no wasted cycles

## Why Biome as Default

- **Single tool** — replaces both Prettier (formatting) and ESLint (linting)
- **Fast** — written in Rust, 10-100x faster than Prettier + ESLint
- **Zero config** — works out of the box with sensible defaults
- **Compatible** — 97% Prettier-compatible formatting, growing ESLint rule coverage
- **One config file** — `biome.json` instead of `.prettierrc` + `.eslintrc` + conflicting rules

## Handoff

- **Expected input:** a repo that needs commit-time quality gates
- **Produces:** working git hooks and tool configuration for commit-time checks
- **Supports downstream:** `/execute` and `/pre-merge` by making basic verification more automatic
- **What comes next:** return to normal feature work with stronger local feedback loops
