---
name: monorepo-change
description: Make a change in a monorepo or multi-module workspace (pnpm, npm, or yarn workspaces, Turborepo, Nx, Go workspaces with go.work, uv workspaces, or Cargo workspaces) by finding the package that owns the code and the packages that depend on it, keeping package boundaries, updating internal dependency versions and the lockfile with the workspace tool, and building and testing only what is affected, then the whole workspace when shared code changed. Use when a change touches code shared by several packages, modules, or services in a workspace, or when the user asks to change, fix, or add behavior in such a repository. Do not use for adding or extracting a whole package (use agent-kit:monorepo-package), for release versioning (use agent-kit:monorepo-release), for reviewing boundaries without changes (use agent-kit:monorepo-review), or for single-package repositories.
---

# Monorepo change

## 1. Map the workspace

- Identify the tool and its configuration: `pnpm-workspace.yaml`, `workspaces` in `package.json`, `turbo.json`, `nx.json`, `go.work`, `[tool.uv.workspace]` in `pyproject.toml`, or `[workspace]` in `Cargo.toml`. Read root and package scripts and project instructions for the documented commands.
- Find the package that owns the code to change and the packages that depend on it: `pnpm why`/`pnpm ls --filter ...<pkg>`, `nx graph` or `nx show projects --affected`, `turbo run <task> --filter=...<pkg> --dry`, a search for imports of the module path in the other `go.work` modules, `uv tree --invert --package <pkg>`, `cargo tree -i <crate>`, or a search for imports of the package name.

## 2. Change within boundaries

- Change the owning package and import other packages only through their public entry points (`exports`, the module path, the published crate API), never by reaching into another package's `src` or internal directories.
- Declare every new cross-package dependency in the consuming package's manifest using the workspace protocol the repo uses (`workspace:*`, a path or workspace dependency in `pyproject.toml` or `Cargo.toml`; in a Go workspace the `go.work` `use` entry is enough, and a `require` with a real version or `replace` is only needed for builds outside the workspace), then refresh the lockfile with the tool (`pnpm install`, `npm install`, `uv lock`, `cargo check`); never hand-edit lockfiles.
- When a change alters a package's public API, update all dependents in the same change or keep the old API working, and say which packages were affected.
- Put a dependency in the package that uses it, not the workspace root, unless the repo keeps shared dev tooling at the root.

## 3. Verify what is affected

- Run the build, type check, and tests for the owning package and its dependents with the workspace tool: `pnpm --filter ...<pkg> run test` (the package and its dependents), `turbo run test --filter=...[origin/main]`, `nx affected -t test`, `go test ./...` in each affected module or `go test example.com/mod/...`, `uv run --package <member> pytest`, `cargo test -p <crate>`.
- Use the repository's own scripts when they exist; package-level commands sometimes only work from the root script. If shared configuration, the lockfile, or a widely used package changed, run the full workspace checks.

## 4. Report

Summarize the packages changed and why, dependents updated, dependency and lockfile changes, the commands run with results, and anything that needs a release (see agent-kit:monorepo-release).

## Examples

- Use: "Add a currency field to the shared money package and use it in billing." "Fix the date bug in packages/utils." "Rename this function used across services."
- Skip: "Create a new packages/notifications package." (agent-kit:monorepo-package) "Bump versions for the release." (agent-kit:monorepo-release)
