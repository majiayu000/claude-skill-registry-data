---
name: eslint-neostandard
description: Configures ESLint v9 flat config and neostandard for JavaScript and TypeScript projects, including migrating from legacy `.eslintrc*` files or the `standard` package. Used to
  set up or fix linting with `eslint.config.js` or `eslint.config.mjs`, troubleshoot lint errors, configure neostandard rules, migrate from `.eslintrc` to flat config, or integrate linting into CI
  pipelines and pre-commit hooks.
packages:
  - eslint
  - neostandard
tags:
  - eslint
  - lint
allowed-tools: Read, Write, Edit, Glob, Grep
metadata:
  tags: linting, neostandard, eslint, eslint9, flat-config, javascript, typescript
---

## Use this skill when

- Setting up linting in a JavaScript or TypeScript project
- Using `neostandard` as a Standard-like ESLint v9 flat-config baseline
- Configuring `eslint@9` with the flat config system (`eslint.config.js` / `eslint.config.mjs`)
- Migrating from `standard` to `neostandard` or ESLint v9
- Migrating from legacy `.eslintrc*` configuration to ESLint v9
- Running linting consistently in CI and local development

## Do not use this skill when

- The project uses ESLint v8 with legacy `.eslintrc` and migration is explicitly out of scope
- You need a formatter rather than a linter (use Prettier skill)

## Instructions

1. Install `eslint@9` and `neostandard` as dev dependencies.
2. Create `eslint.config.js` (or `.mjs`) exporting `neostandard()` as the base config array.
3. Add project-specific rule overrides on top of the base array.
4. Run `npx eslint .` to confirm no config errors.
5. Add a `"lint": "eslint ."` script to `package.json`.
6. Integrate into CI with a non-fix run; use `--fix` only in local workflows.

## Capabilities

### ESLint v9 Flat Config System

ESLint v9 replaced `.eslintrc*` files with a flat config system. Config lives in `eslint.config.js` (or `.mjs`) at the project root and exports an array of config objects. Each object can specify `files`, `ignores`, `plugins`, `rules`, `languageOptions`, and `settings`. Multiple objects in the array are merged in order.

The flat config system is strictly additive: later objects override earlier ones for matching files. There are no more `extends` strings — plugins and parsers are imported directly as JavaScript modules.

### neostandard

neostandard is the community-maintained successor to the `standard` linting package, rebuilt for ESLint v9 flat config. It provides a Standard-like ruleset (no semicolons, 2-space indent, single quotes) without the legacy monolithic package approach.

The `neostandard()` function returns a config array that can be spread into your own config or used directly as the export. Options include enabling TypeScript rules, semi mode, and ignoring certain globals.

### TypeScript Support

neostandard includes TypeScript-aware rules when the `ts: true` option is passed. The `@typescript-eslint` parser is used automatically for `.ts` and `.tsx` files. Type-checked rules require `parserOptions.project` pointing to your `tsconfig.json`.

### Migration from Legacy Config

Legacy `.eslintrc*` files and `standard` package are incompatible with ESLint v9 flat config. Migration involves:
- Replacing `extends: ["standard"]` with `neostandard()` in the new flat config
- Converting plugin references from string names to direct imports
- Moving `env` declarations to `languageOptions.globals`
- Updating parser options format

The `@eslint/migrate-config` tool can assist with mechanical conversion of legacy configs.

### CI and Editor Integration

In CI pipelines, always run `eslint .` without `--fix` so lint failures block the build. Use `--max-warnings 0` to treat warnings as errors in strict pipelines.

For pre-commit hooks, use `lint-staged` to run ESLint only on staged files with `--fix`. This keeps commits clean without running the full project lint.

Editor integration (VS Code): install the ESLint extension and set `eslint.useFlatConfig: true` in settings for flat config projects.

## Behavioral Traits

- Prefers reproducible linting with pinned major versions (`eslint@9`, `neostandard@x`)
- Keeps config minimal and explicit — avoids large rule overrides unless justified
- Uses flat config for all ESLint v9 projects
- Treats lint failures as quality gates in CI
- Enables auto-fix for local workflows only; CI runs without `--fix`
- Reads existing `eslint.config.js` before suggesting changes to understand current setup

## Knowledge Base

- ESLint v9 flat config array format and merge semantics
- neostandard rule defaults (no semi, 2-space indent, single quotes, space-before-function-paren)
- `neostandard()` options: `ts`, `semi`, `noJsx`, `globals`, `ignores`
- TypeScript parser configuration and type-checked rule requirements
- Migration path: `standard` → `neostandard`, `.eslintrc` → `eslint.config.js`
- `eslint --fix` vs `eslint` and when to use each
- `lint-staged` integration for pre-commit hooks
- Common flat config gotchas: `ignores` as a standalone object applies globally; inside a config object it is file-scoped

## Reference Files

- [rules/neostandard.md](rules/neostandard.md) — Install, configure, and extend neostandard with ESLint
- [rules/eslint-v9-flat-config.md](rules/eslint-v9-flat-config.md) — Build ESLint v9 flat config for JS/TS projects
- [rules/migration-from-standard.md](rules/migration-from-standard.md) — Migrate from `standard` to `neostandard` or ESLint v9
- [rules/migration-from-legacy-eslint.md](rules/migration-from-legacy-eslint.md) — Migrate from `.eslintrc*` to flat config safely
- [rules/ci-and-editor-integration.md](rules/ci-and-editor-integration.md) — CI scripts, pre-commit, and editor setup
