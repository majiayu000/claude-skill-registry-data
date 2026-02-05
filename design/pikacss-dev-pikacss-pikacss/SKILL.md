---
name: pikacss-dev
description: Develop, test, and document the PikaCSS monorepo (core engine, unplugin adapters, Vite/Nuxt plugins, docs site) using pnpm-based workflows.
license: MIT
compatibility: Requires pnpm 10.24.0 and a recent Node.js LTS in a workspace checkout.
metadata:
  repo: pikacss
  version: 0.0.34
allowed-tools: bash:pnpm bash:node read
---

## Purpose
Use this skill to work on PikaCSS internals (not for end-users). It covers builds, tests, docs, plugin adapters, and release hygiene across the monorepo.

## Setup
- Install dependencies: pnpm install
- Hooks: simple-git-hooks + lint-staged run automatically on prepare
- Preferred environment: Node LTS (18+), pnpm 10.24.0

## Core workflows
- Builds, tests, typecheck, lint, docs, and release guidance are in [reference-commands.md](reference-commands.md).
- Package map, plugin targets, docs, and examples are in [reference-packages.md](reference-packages.md).
- Scaffolding: Use `pnpm newpkg` for general packages or `pnpm newplugin` for PikaCSS plugins.

## Notes and cautions
- Release pipeline (`pnpm release`) chains build, docs, typecheck, publint, dist cleanup, and version bump; use only when intending to publish.
- Publint validates published exports; run before publish changes to packages.
- Use filters when touching a single package to keep tasks fast.
- Keep docs and examples consistent with core changes; see references for locations.

## CI/CD Pipeline

### GitHub Actions Workflows
- **ci.yml**: Runs tests, typecheck, lint on PRs and pushes
- Tests run across multiple Node versions
- Automatic checks must pass before merge

### Release Automation
1. Run `pnpm release` (uses bumpp for versioning)
2. Publint validates package.json exports
3. Docs are built and verified
4. All tests and checks must pass
5. Publish to npm with `pnpm publish:packages`

## Debugging Build Issues

### Common Issues
- **tsdown fails**: Check tsconfig.json, clear dist folders
- **Dependency issues**: `rm -rf node_modules pnpm-lock.yaml && pnpm install`
- **Circular deps**: Review package.json dependencies graph
- **Type errors**: Run `pnpm typecheck --filter <package>`

### Package Architecture

**Dependency Graph**:
```
core (no deps)
  ↑
  ├── integration (depends on core)
  │     ↑
  │     ├── unplugin (depends on integration)
  │     │     ↑
  │     │     ├── vite (depends on unplugin)
  │     │     └── nuxt (depends on unplugin)
  │     └── plugin-* (depends on core)
```

**When to create new packages**:
- New build tool integration → Add to unplugin exports
- New framework adapter → Create new package in packages/
- New plugin → Use `pnpm newplugin <name>`
- Core features → Add to @pikacss/core

## Advanced Development

### Monorepo Workflow Patterns
- Use `--filter` to target specific packages
- Use workspace protocol (`workspace:*`) for internal deps
- Build order: core → integration → unplugin → framework adapters
- Test in isolation before testing integration

### Inter-Package Communication
- Core exports engine API
- Integration uses core for style processing
- Unplugin wraps integration for bundlers
- Framework adapters wrap unplugin with framework-specific config

```
