---
name: kit-monorepo-review
description: Review a monorepo or workspace for package boundary problems, including imports that reach into another package's internals, imports of packages not declared as dependencies, circular dependencies between packages or modules, version drift of the same external dependency across packages, misplaced shared code, and dependencies declared at the wrong level, and report findings with severity and file locations. Use when asked to review a monorepo's structure, package boundaries, dependency graph, or workspace hygiene, or to find cycles or undeclared dependencies across packages. Do not use for general code review of a diff (use kit-code-review), for making the fixes (use kit-monorepo-change), or for single-package repositories; this skill reports and does not edit code.
---

# Monorepo review

Report findings without modifying code unless the user asks for fixes.

## 1. Build the package graph

- Identify the workspace tool and list the packages, modules, or crates with their manifests (`package.json`, `go.mod`, `pyproject.toml`, `Cargo.toml`).
- For each package, record its declared internal and external dependencies, and its actual imports of other workspace packages (search for package names, module paths, and relative paths that leave the package directory).
- Use tool graphs when available (`pnpm ls -r --depth 0`, `nx graph --file=graph.json`, `go list -deps`, `uv tree`, `cargo tree`), and confirm by reading code.

## 2. Check

- **Boundary violations:** relative imports that leave the package (`../../other/src/...`), deep imports into another package's `src`, `internal`, or private modules instead of its public entry point, and Go imports of another module's `internal` packages.
- **Undeclared dependencies:** a package imports another workspace package or an external library that its own manifest does not declare (it works only because of hoisting or the workspace root).
- **Cycles:** packages or modules that depend on each other directly or through a chain. Show the cycle path.
- **Version drift:** the same external dependency at different major or minor versions across packages, or internal dependencies pinned to stale versions instead of the workspace protocol.
- **Misplaced code and dependencies:** shared code duplicated across packages, application code in a shared library, runtime dependencies declared only at the root, and dev tooling duplicated in every package.
- Respect the repo's documented rules (lint rules for boundaries, Nx tags, CODEOWNERS) and do not report what they explicitly allow.

## 3. Verify and report

Confirm each finding by reading the import and the manifests; run the repo's dependency or boundary checks when available (`nx lint` with module boundaries, `pnpm -r why`, `go build ./...` in each module (cross-module `internal` imports fail to compile), `cargo tree -d`). Report findings ordered by severity (critical, high, medium, low) with `file:line`, the problem, why it matters (build order, hoisting breakage, release coupling), and a fix. If there are no findings, say so and list what was checked.

## Examples

- Use: "Review our monorepo's package boundaries." "Are there circular dependencies between packages?" "Why does billing work locally but fail when installed alone?"
- Skip: "Review my PR for bugs." (kit-code-review) "Move the shared code into a package." (kit-monorepo-package)
