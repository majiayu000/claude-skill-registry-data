---
name: monorepo-management-skill
description: >-
  Manage JS/TS monorepos — Turborepo, Nx, pnpm workspaces; package boundaries,
  build caching, changesets.
license: Apache-2.0
compatibility: opencode
category: DevOps
---

## What I do

Structure JS/TS monorepos: tool selection (Turborepo vs Nx vs pnpm-only), workspace layout, shared config packages, enforced package boundaries, build caching, changesets.

## When to use me

- Setting up or restructuring a monorepo (apps/ + packages/ split, shared configs)
- Cross-package breakage risk, cache misses, or boundary drift (apps importing package internals)

**Related:** `performance-optimization-skill` (profiling/bundles) · `civiltekk-documentation-sync-skill` (doc sync across packages).

## House conventions

**Layout**: `apps/*` (deployables) + `packages/*` (shared: `ui`, `utils`, `typescript-config`, `eslint-config`). Internal deps use `"@repo/x": "workspace:*"`.

**Shared TS config**: `packages/typescript-config/{base,nextjs,react-library}.json`; app tsconfigs extend `@repo/typescript-config/nextjs.json` via `"extends"`. Same pattern for ESLint (`@repo/eslint-config`).

**Enforced boundaries** (`eslint-plugin-boundaries`, `boundaries/element-types`): apps must import package ENTRY POINTS, never `packages/*/src/**` internals; `packages/ui` must not depend on `apps/*`. Message strings say why — the rule is teaching, not just blocking.

**OpenCode LSP (root config)**: a root `opencode.json` with `"lsp": {"typescript": {}, "eslint": {}}` gives ambient cross-package diagnostics (a `packages/ui` change breaking `apps/web` surfaces live). Servers trigger per-file by extension; one root config covers the whole workspace — no per-package config. Token cost is real in large repos: monitor, scope servers, or set `"lsp": false` to disable. Refs: opencode.ai/docs/lsp, /docs/config.

**Caching**: Turborepo local cache by default; remote cache (Vercel) for CI speedup; pipeline defined in `turbo.json` (`build` depends on `^build`). pnpm-workspace.yaml defines package globs; root package.json drives scripts.

> Removed 2026-09: step-by-step tool-selection essays, full turbo.json/pnpm-workspace/package.json listings, ESLint flat-config walkthroughs, task-pipeline deep-dives, changesets tutorial, common-issue troubleshooting — vendor docs the model knows; what remains is the house layout, boundary rules, and the root-LSP integration pattern.
