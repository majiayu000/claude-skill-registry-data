---
name: kit-monorepo-package
description: Add a new package, module, or crate to a monorepo workspace, or extract existing code into one, matching the layout and wiring of the existing packages (workspace membership, manifest, build and test configuration, TypeScript project references, exports, go.work use, uv workspace members, Cargo members) and updating imports so everything still builds and passes tests. Use when the user asks to create, scaffold, add, split out, or extract a package, library, module, service, or crate in a workspace. Do not use for changing code inside existing packages (use kit-monorepo-change), for release versioning (use kit-monorepo-release), or for single-package repositories.
---

# Monorepo package

## 1. Learn the conventions

- Read two or three existing packages similar to the new one: directory location, naming and scope (`@org/name`, module paths, crate names), manifest fields, scripts, build output, test setup, lint and TypeScript configuration, README, and license fields.
- Read the workspace configuration that must include the package: `pnpm-workspace.yaml` or `workspaces` globs, `turbo.json` or `project.json`, `tsconfig` references, `go.work`, `[tool.uv.workspace] members`, `Cargo.toml` `members`, and any CODEOWNERS or release configuration.

## 2. Create or extract

- Create the package by copying the structure of the closest existing package, not a generic template. Keep it private or unpublished unless the user says otherwise, and start its version where the repo's other new packages start.
- Register it: make sure the workspace globs cover it, add `go.work use ./path`, add it to uv or Cargo members, add TypeScript project references, and add it to task pipelines only where the repo lists packages explicitly.
- When extracting, move the code with its tests, expose a deliberate public API (`exports`, `__init__.py`, exported identifiers, `pub` items), replace old imports in every consumer with the new package name, and declare the new dependency in each consumer's manifest. Leave no copies behind and do not create import cycles.
- Move files with `git mv` (or copy, verify, then delete) after reading them; never overwrite a file you have not read.
- Refresh the lockfile with the workspace tool (`pnpm install`, `uv lock`, `cargo check`; for Go, `go work use ./path` and `go mod tidy` in the new module). Never hand-edit a lockfile; if the command cannot run, say so and leave the refresh to the user.

## 3. Verify

Build and test the new package and every consumer through the workspace tool, then run the full workspace checks, because workspace configuration changed. Confirm there are no leftover references to the old paths (`git grep`).

## 4. Report

Summarize where the package lives, how it is wired into the workspace, its public API, consumers updated, commands run with results, and choices for the user to confirm (name, visibility, initial version).

## Examples

- Use: "Create a packages/notifications library like packages/email." "Extract the money helpers from apps/web into a shared package." "Add a new Go module for the worker to go.work."
- Skip: "Fix a bug in packages/utils." (kit-monorepo-change) "Version and release the packages." (kit-monorepo-release)
