---
name: pnpm
description: This skill should be used every time you work on pnpm workspace structure, dependency management, or runtime command execution in this repository.
compatibility: opencode
---

# pnpm Workspace Rules (Hardlink + Bun Runtime)

This file defines the required pnpm workspace conventions for this repo.

## Core Principles

1. Use `pnpm` as the only dependency manager and lockfile authority.
2. Use Bun for all runtime script execution (`bun --cwd <package-dir> run <script>`).
3. Keep workspace code inside `src/` for every app and package.
4. Treat `apps/` as runnable runtime projects.
5. Treat `packages/` as reusable libraries with non-runnable code.
6. All installed dependencies in `node_modules` must come from pnpm links/hardlinks, never copied vendor trees.

## Workspace Layout

```
src/
  apps/
    <app-name>/
      src/
      package.json
  packages/
    <pkg-name>/
      src/
      package.json
pnpm-workspace.yaml
.npmrc
pnpm-lock.yaml
```

## Folder Semantics

- `src/apps/*`: runtime entrypoints and deployable applications.
- `src/packages/*`: shared libraries, utilities, SDKs, design systems, and other non-runnable modules.
- `src/`: required location for implementation code in both apps and packages.

## Runtime Policy (Bun Mandatory)

1. Execute scripts with Bun from the target workspace package.
2. Standard form: `bun --cwd <package-dir> run <script>`.
3. Do not use `node`, `npm`, or `pnpm run` as the runtime execution interface.
4. Keep `pnpm` focused on install/add/remove/update and workspace dependency graph operations.

## Dependency Storage Policy (Hardlink Mandatory)

1. `package-import-method=hardlink` is required.
2. `node-linker=isolated` is required.
3. `symlink=true` is required.
4. Do not use hoisted layouts or copied `node_modules` trees.
5. Do not introduce tooling that vendors full dependency sources into workspace packages.

Required `.npmrc` baseline:

```ini
package-import-method=hardlink
node-linker=isolated
symlink=true
```

## Apps vs Packages Rules

1. `src/apps/*` may define runnable scripts such as `dev`, `start`, or platform runtime commands.
2. `src/packages/*` must not be treated as deployable runtime apps.
3. Library packages should expose buildable/importable artifacts and typed APIs.
4. If a package needs executable tooling, keep it explicit and separate from app runtime concerns.

## Frontend Package Visualization (Storybook)

1. Any frontend/UI library under `src/packages/*` must provide Storybook coverage for visual components.
2. Stories should live with source (for example `src/**/*.stories.tsx`) or another clearly documented package-local convention.
3. Storybook development and build commands must be executed with Bun runtime commands.

## Validation Checklist

1. `pnpm-workspace.yaml` includes intended `src/apps/*` and `src/packages/*` workspaces.
2. Each workspace package has a `src/` folder.
3. `.npmrc` enforces hardlink + isolated linker + symlink settings.
4. Runtime commands are invoked via Bun command form.
5. UI libraries in `src/packages/*` include Storybook stories for visual review.
