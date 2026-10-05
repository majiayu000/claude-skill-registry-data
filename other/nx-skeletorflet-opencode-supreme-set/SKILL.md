---
name: nx
description: Nx — smart monorepo with generators, executors, computation caching, dependency graph, Nx Cloud.
---

## nx

### Generators & Executors
- `nx generate @nx/react:app web` — scaffold projects from plugins.
- Custom generators: `tools/generators/my-gen/index.ts` with schema.json.
- Executors abstract build/test commands: `"executor": "@nx/vite:build"`.
- `nx list` — show available plugins; `nx generate list` — show generators.

### Computation Caching
- Cache key = task name + inputs (files, env, flags, dependencies' outputs).
- `cacheableOperations: ["build", "test", "lint"]` in `nx.json`.
- `--skip-nx-cache` to bypass; `--reset` to clear local cache.
- Inputs: `namedInputs: { production: ["!**/*.test.ts"] }` — selective cache invalidation.

### Affected Commands
- `nx affected:test --base=main` — only test projects changed since main.
- `nx affected:build --files=apps/web/src/button.tsx` — specific files.
- `nx graph --affected` — visual diff of affected projects.

### Dependency Graph
- `nx graph` — interactive visualization of project dependencies.
- `nx graph --focus=myapp` — zoom into a specific project.
- Implicit dependencies: `"implicitDependencies": ["shared-ui"]` in project.json.

### Cloud & Tools
- Nx Cloud: `nx connect-to-nx-cloud` — remote caching + distributed execution.
- Nx Console — VS Code extension for generator UI and graph.
- Migrate: `nx migrate latest` — update versions and configs automatically.
- `nx add @nx/next` — add plugin to existing workspace.
