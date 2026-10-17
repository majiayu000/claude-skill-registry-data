---
name: convert-esm
description: Migrate CommonJS to ESM step by step, fixing require/module.exports, imports, and config.
argument-hint: "[package-or-path]"
related:
  - use-astgrep
  - run-typecheck
  - deep-review-codebase
  - update-references
  - run-build
  - run-test
  - refactor
---

## Goal

Migrate a JavaScript/TypeScript project from CommonJS (`require`/`module.exports`) to ESM (`import`/`export`) systematically without breaking the runtime.

## Scope

- Covers: `require` → `import`, `module.exports` → `export`, `"type": "module"` config, file extensions (`.js` vs `.cjs` vs `.mjs`), dynamic requires, `__dirname`/`__filename` equivalents, JSON imports
- Migrate one package/module at a time — in a monorepo, one workspace at a time
- Action-oriented: change real code — verify with typecheck/build/test at every step

## Execute

### 1. Assess Current State

> Goal: Size the work and find blockers

1. Count `require`/`module.exports` sites with `use-astgrep` or `search-files-patterns`
2. Check the `package.json` `"type"` field and runtime/tooling support (Node version, bundler, test runner)
3. Find blockers: `require()` calls that can't be made static, conditional requires, CJS-only deps
4. Check the dependencies that import this project — run `/deep-review-codebase`

### 2. Plan Migration Order

> Goal: Order the work to minimize breakage

1. Do leaf modules first (no internal dependents) → core modules last
2. Identify files that need renaming (`.js` → `.mjs` in mixed mode) or config changes
3. Plan `package.json`: `"type": "module"`, `exports` map, `engines`

### 3. Convert

> Goal: Convert in batches with verification

1. Convert `require` → `import` and `module.exports` → `export` one module at a time
2. Replace `__dirname`/`__filename` with `import.meta.url` + `fileURLToPath`
3. Convert dynamic `require()` → `await import()`, or a static import where possible
4. JSON requires → `import ... with { type: 'json' }` or `fs.readFile`
5. Add `.js` extensions to relative imports per the ESM spec
6. Run `/update-references` whenever export/import paths change

### 4. Update Config

> Goal: Adapt tooling to support ESM

1. Set `"type": "module"` in `package.json` + an `exports` map
2. tsconfig: `module: "NodeNext"`/`"ESNext"` and the matching `moduleResolution`
3. Test runner, bundler, scripts — check every tool that reads the code
4. Use `.cjs` for files that must stay CommonJS (config files a tool requires)

### 5. Verify

> Goal: Confirm everything runs on ESM

1. `/run-typecheck` + `/run-lint` pass
2. `/run-build` passes — bundle/output correct
3. `/run-test` passes — watch for test mocks that rely on CJS semantics (`jest.mock` vs `vi.mock`)
4. Smoke-test the real runtime entry points

## Rules

### 1. Incremental

- Convert one module/package at a time — never big-bang the whole repo at once
- Verify after each batch — if something breaks, know exactly where

### 2. Compatibility Aware

- If the package is a published library → decide with the user upfront whether to dual-publish (ESM+CJS) or go ESM-only
- Watch for tools that are still CJS-only — use `.cjs` files or interop instead of forcing a migration

### 3. No Semantic Changes

- Convert syntax/module system only — never refactor logic along the way
- Circular imports that CJS tolerates may break in ESM — flag them to `/follow-tool-madge`

## Expected Outcome

- Codebase fully ESM — no leftover `require`/`module.exports` (except necessary `.cjs`)
- typecheck/build/test all pass
- `package.json` exports map correct for consumers
