---
name: nx
description: Nx monorepo build system, generators, executors, affected commands, caching, and project graph
layer: domain
category: build-tools
triggers:
  - "nx"
  - "nx workspace"
  - "nx generate"
  - "nx affected"
  - "nx graph"
  - "nx.json"
  - "nx cloud"
  - "nx plugin"
inputs:
  - "Monorepo architecture requirements"
  - "Build and test optimization needs"
  - "Project graph structure"
outputs:
  - "Nx workspace configuration"
  - "Generator and executor setup"
  - "CI pipeline configuration"
  - "Caching and affected command strategies"
linksTo:
  - monorepo
  - cicd
  - turborepo
  - dev-workflow
linkedFrom: []
preferredNextSkills: [cicd, monorepo]
fallbackSkills: [turborepo, pnpm]
riskLevel: low
memoryReadPolicy: selective
memoryWritePolicy: none
sideEffects: [code generation, build artifacts]
---

# Nx

## Purpose

Manage monorepos and large-scale projects with Nx. Covers workspace setup, the project graph, task orchestration with caching, generators for code scaffolding, executors for custom build steps, affected commands for CI optimization, Nx Cloud for distributed caching, and plugin development.

## Core Patterns

### Workspace Structure

```
my-workspace/
  nx.json                  # Nx configuration
  package.json             # Root package.json
  tsconfig.base.json       # Shared TS config
  apps/
    web/
      project.json         # App-specific Nx config
      src/
    api/
      project.json
      src/
  libs/
    shared/
      ui/
        project.json
        src/
      utils/
        project.json
        src/
      data-access/
        project.json
        src/
  tools/
    generators/            # Custom workspace generators
```

### nx.json Configuration

```jsonc
{
  "$schema": "./node_modules/nx/schemas/nx-schema.json",
  "defaultBase": "main",
  "namedInputs": {
    "default": ["{projectRoot}/**/*", "sharedGlobals"],
    "sharedGlobals": ["{workspaceRoot}/tsconfig.base.json", "{workspaceRoot}/.eslintrc.json"],
    "production": [
      "default",
      "!{projectRoot}/**/*.spec.ts",
      "!{projectRoot}/**/*.test.ts",
      "!{projectRoot}/tsconfig.spec.json",
      "!{projectRoot}/jest.config.ts"
    ]
  },
  "targetDefaults": {
    "build": {
      "dependsOn": ["^build"],     // Run build on deps first
      "inputs": ["production", "^production"],
      "outputs": ["{projectRoot}/dist"],
      "cache": true
    },
    "test": {
      "inputs": ["default", "^production", "{workspaceRoot}/jest.preset.js"],
      "cache": true
    },
    "lint": {
      "inputs": ["default", "{workspaceRoot}/.eslintrc.json", "{workspaceRoot}/.eslintignore"],
      "cache": true
    },
    "e2e": {
      "cache": false  // E2E tests are non-deterministic
    }
  },
  "plugins": [
    {
      "plugin": "@nx/next/plugin",
      "options": { "buildTargetName": "build", "devTargetName": "dev", "startTargetName": "start" }
    },
    {
      "plugin": "@nx/eslint/plugin",
      "options": { "targetName": "lint" }
    }
  ],
  "nxCloudId": "your-nx-cloud-id"
}
```

### project.json (Per-Project Config)

```jsonc
// apps/web/project.json
{
  "name": "web",
  "sourceRoot": "apps/web/src",
  "projectType": "application",
  "tags": ["scope:web", "type:app"],
  "targets": {
    "build": {
      "executor": "@nx/next:build",
      "outputs": ["{options.outputPath}"],
      "options": {
        "outputPath": "dist/apps/web"
      },
      "configurations": {
        "production": {
          "optimization": true,
          "sourceMap": false
        }
      }
    },
    "serve": {
      "executor": "@nx/next:server",
      "options": { "buildTarget": "web:build", "port": 3000 }
    },
    "test": {
      "executor": "@nx/jest:jest",
      "options": {
        "jestConfig": "apps/web/jest.config.ts",
        "passWithNoTests": true
      }
    }
  }
}
```

### Essential Commands

```bash
# Run targets
nx serve web                       # Dev server for app
nx build web                       # Build specific project
nx test shared-utils               # Test specific library
nx lint web                        # Lint specific project
nx run web:build:production        # Run target with configuration

# Run across projects
nx run-many -t build test lint     # Run multiple targets across all projects
nx run-many -t build --projects=apps/*  # Build all apps
nx run-many -t test --parallel=5   # Run tests in parallel

# Affected commands (only what changed since base)
nx affected -t build               # Build only affected projects
nx affected -t test                # Test only affected projects
nx affected -t lint --base=main    # Lint affected since main branch
nx show projects --affected        # List affected project names

# Project graph
nx graph                           # Open interactive dependency graph
nx graph --affected                # Show only affected in graph

# Generators
nx generate @nx/next:app my-app    # Scaffold a Next.js app
nx generate @nx/react:lib my-lib   # Scaffold a React library
nx generate @nx/js:lib utils --directory=libs/shared  # JS library

# Cache management
nx reset                           # Clear local cache
nx report                          # Show installed plugin versions

# Migrations
nx migrate latest                  # Update Nx and plugins
nx migrate --run-migrations        # Apply pending migrations
```

### Inferred Targets (Plugin-Based)

```jsonc
// nx.json — plugins auto-detect and register targets
{
  "plugins": [
    {
      "plugin": "@nx/vite/plugin",
      "options": {
        "buildTargetName": "build",
        "testTargetName": "test",
        "serveTargetName": "serve"
      }
    }
  ]
}
// No project.json needed — Nx infers targets from vite.config.ts presence
```

### Module Boundary Rules

```jsonc
// .eslintrc.json (root)
{
  "overrides": [
    {
      "files": ["*.ts", "*.tsx"],
      "rules": {
        "@nx/enforce-module-boundaries": [
          "error",
          {
            "enforceBuildableLibDependency": true,
            "allow": [],
            "depConstraints": [
              { "sourceTag": "type:app", "onlyDependOnLibsWithTags": ["type:lib", "type:util"] },
              { "sourceTag": "type:lib", "onlyDependOnLibsWithTags": ["type:lib", "type:util"] },
              { "sourceTag": "type:util", "onlyDependOnLibsWithTags": ["type:util"] },
              { "sourceTag": "scope:web", "onlyDependOnLibsWithTags": ["scope:web", "scope:shared"] },
              { "sourceTag": "scope:api", "onlyDependOnLibsWithTags": ["scope:api", "scope:shared"] }
            ]
          }
        ]
      }
    }
  ]
}
```

### Custom Generator

```typescript
// tools/generators/feature-lib/index.ts
import {
  Tree,
  formatFiles,
  generateFiles,
  joinPathFragments,
  names,
  addProjectConfiguration,
} from "@nx/devkit";

interface Schema {
  name: string;
  scope: "web" | "api" | "shared";
}

export default async function featureLibGenerator(tree: Tree, schema: Schema) {
  const { className, propertyName, fileName } = names(schema.name);
  const projectRoot = joinPathFragments("libs", schema.scope, fileName);

  addProjectConfiguration(tree, `${schema.scope}-${fileName}`, {
    root: projectRoot,
    sourceRoot: `${projectRoot}/src`,
    projectType: "library",
    tags: [`scope:${schema.scope}`, "type:lib"],
    targets: {},
  });

  generateFiles(tree, joinPathFragments(__dirname, "files"), projectRoot, {
    className,
    propertyName,
    fileName,
    scope: schema.scope,
    tmpl: "", // Strips __tmpl__ from filenames
  });

  await formatFiles(tree);
}
```

```json
// tools/generators/feature-lib/schema.json
{
  "$schema": "https://json-schema.org/schema",
  "id": "feature-lib",
  "title": "Feature Library Generator",
  "type": "object",
  "properties": {
    "name": { "type": "string", "description": "Library name", "$default": { "$source": "argv", "index": 0 } },
    "scope": { "type": "string", "enum": ["web", "api", "shared"], "description": "Scope tag" }
  },
  "required": ["name", "scope"]
}
```

```bash
# Use the custom generator
nx generate @myorg/tools:feature-lib auth --scope=shared
```

### CI Configuration (GitHub Actions)

```yaml
# .github/workflows/ci.yml
name: CI

on:
  push:
    branches: [main]
  pull_request:

jobs:
  main:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
        with:
          fetch-depth: 0  # Needed for affected commands

      - uses: pnpm/action-setup@v4
        with:
          version: 9

      - uses: actions/setup-node@v4
        with:
          node-version: 22
          cache: pnpm

      - run: pnpm install --frozen-lockfile

      # Set SHAs for affected commands
      - uses: nrwl/nx-set-shas@v4

      # Run only what's affected
      - run: pnpm nx affected -t lint test build --parallel=3

      # Or with Nx Cloud for distributed task execution
      # - run: pnpm nx-cloud start-ci-run --distribute-on="3 linux-medium-js"
      # - run: pnpm nx affected -t lint test build
```

### Nx Cloud (Remote Caching)

```bash
# Connect workspace to Nx Cloud
npx nx connect

# CI sees cache hits from other developers and CI runs
# Local dev benefits from CI cache — never rebuild what CI already built
```

## Best Practices

- **Use tags and module boundaries** — enforce architectural rules with `@nx/enforce-module-boundaries`
- **Prefer inferred targets** — let plugins auto-detect config files instead of manual `project.json` targets
- **Use `affected`** in CI — only run tasks for projects impacted by the current changeset
- **Define `namedInputs`** — separate production inputs from test inputs for precise cache invalidation
- **Enable Nx Cloud** — remote cache shared across CI and local dev eliminates redundant work
- **Use generators** for scaffolding — ensures consistency and includes all boilerplate (tests, configs)
- **Set `dependsOn: ["^build"]`** for build targets — ensures dependencies are built first
- **Keep libraries small and focused** — better cache granularity and clearer dependency graph
- **Use `--parallel`** with a reasonable limit (3-5) — over-parallelization causes memory issues
- **Run `nx migrate` regularly** — keeps plugins compatible and applies codemods automatically

## Anti-Patterns

| Anti-Pattern | Why It's Bad | Do Instead |
|---|---|---|
| Huge monolithic libraries | Poor cache granularity, slow rebuilds | Split into focused feature libraries |
| No module boundary rules | Circular deps, spaghetti architecture | Configure tag-based constraints |
| `cache: false` on everything | Defeats Nx's primary value proposition | Only disable cache for non-deterministic tasks |
| Skipping `fetch-depth: 0` in CI | Affected commands can't diff properly | Always fetch full history |
| Manual `project.json` for everything | Verbose, hard to maintain | Use plugin-inferred targets |
| Running all targets, not affected | Wastes CI time on unchanged code | Use `nx affected -t ...` |
| Ignoring `nx migrate` | Version drift between plugins | Run migrations on a regular cadence |
| Putting all code in `apps/` | No code sharing, duplicated logic | Extract shared code into `libs/` |

## Decision Guide

| Scenario | Recommendation |
|---|---|
| New monorepo, JS/TS stack | Nx with integrated repo setup |
| Existing monorepo, add build orchestration | Nx with package-based setup (less invasive) |
| Need distributed CI caching | Enable Nx Cloud (free for open source) |
| Enforce architecture rules | Module boundaries with scope/type tags |
| Scaffold new projects consistently | Custom generators in `tools/generators/` |
| Need to support multiple frameworks | Nx plugins: `@nx/next`, `@nx/react`, `@nx/node`, `@nx/nest` |
| Compare with Turborepo | Nx has richer graph analysis, generators, and plugin ecosystem |
| Small project (1-3 packages) | Turborepo or plain pnpm workspaces may be simpler |
