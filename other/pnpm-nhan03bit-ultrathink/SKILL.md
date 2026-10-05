---
name: pnpm
description: pnpm package manager, workspaces, strict dependency resolution, monorepo support, and performance optimization
layer: domain
category: build-tools
triggers:
  - "pnpm"
  - "pnpm workspace"
  - "pnpm-workspace.yaml"
  - "pnpm install"
  - "pnpm add"
  - "pnpm-lock.yaml"
  - "pnpm catalogs"
inputs:
  - "Package management requirements"
  - "Workspace/monorepo structure"
  - "Dependency resolution issues"
outputs:
  - "pnpm configuration"
  - "Workspace setup"
  - "Dependency management commands"
  - "CI optimization strategies"
linksTo:
  - monorepo
  - nodejs
  - dev-workflow
  - turborepo
linkedFrom: []
preferredNextSkills: [turborepo, monorepo]
fallbackSkills: [bun, nodejs]
riskLevel: low
memoryReadPolicy: selective
memoryWritePolicy: none
sideEffects: [package installation, lockfile changes]
---

# pnpm

## Purpose

Manage JavaScript/TypeScript dependencies efficiently using pnpm. Covers the content-addressable store, workspace monorepo management, strict dependency resolution, catalogs for shared versions, patching packages, CI optimization, and common workflows for day-to-day development.

## Core Patterns

### Essential Commands

```bash
# Install all dependencies
pnpm install                    # Install from lockfile
pnpm install --frozen-lockfile  # CI mode — fail if lockfile needs update

# Add/remove packages
pnpm add zod drizzle-orm        # Add production dependencies
pnpm add -D vitest @types/node  # Add dev dependencies
pnpm add -g tsx                 # Add global package
pnpm remove lodash              # Remove a package

# Run scripts
pnpm dev                        # Run "dev" script from package.json
pnpm run build                  # Run "build" script
pnpm exec vitest                # Run a binary from node_modules/.bin
pnpm dlx create-next-app@latest # Run a package without installing (like npx)

# Update dependencies
pnpm update                     # Update all within semver ranges
pnpm update --latest            # Update to latest versions (ignoring ranges)
pnpm update zod                 # Update specific package
pnpm outdated                   # Check for outdated packages

# Inspect
pnpm list                       # List installed packages
pnpm list --depth 0             # Top-level only
pnpm why react                  # Show why a package is installed
pnpm audit                      # Check for vulnerabilities
```

### Workspace Setup (Monorepo)

```yaml
# pnpm-workspace.yaml
packages:
  - "apps/*"
  - "packages/*"
  - "tooling/*"
```

```
my-monorepo/
  pnpm-workspace.yaml
  package.json             # Root package.json
  .npmrc                   # pnpm settings
  apps/
    web/
      package.json         # "name": "@myorg/web"
    api/
      package.json         # "name": "@myorg/api"
  packages/
    ui/
      package.json         # "name": "@myorg/ui"
    shared/
      package.json         # "name": "@myorg/shared"
  tooling/
    eslint-config/
      package.json         # "name": "@myorg/eslint-config"
    tsconfig/
      package.json         # "name": "@myorg/tsconfig"
```

### Workspace Dependencies

```jsonc
// apps/web/package.json
{
  "name": "@myorg/web",
  "dependencies": {
    "@myorg/ui": "workspace:*",      // Always latest from workspace
    "@myorg/shared": "workspace:^",  // Semver-compatible from workspace
    "next": "^15.0.0"
  }
}
```

```bash
# Workspace-aware commands
pnpm add zod --filter @myorg/web          # Add to specific package
pnpm add zod --filter @myorg/web...       # Add to package and its dependencies
pnpm --filter @myorg/web dev              # Run dev in specific package
pnpm --filter "./apps/*" build            # Run build in all apps
pnpm -r build                             # Run build in all packages (recursive)
pnpm -r --parallel build                  # Run build in parallel across packages
pnpm --filter @myorg/web... build         # Build package and all its workspace deps
pnpm --filter "...@myorg/web" test        # Test package and everything that depends on it
```

### Catalogs (Shared Version Management)

```yaml
# pnpm-workspace.yaml — centralize dependency versions
packages:
  - "apps/*"
  - "packages/*"

catalog:
  react: ^19.0.0
  react-dom: ^19.0.0
  typescript: ^5.7.0
  zod: ^3.24.0

catalogs:
  react18:
    react: ^18.3.0
    react-dom: ^18.3.0
```

```jsonc
// apps/web/package.json — reference catalog versions
{
  "dependencies": {
    "react": "catalog:",         // Uses ^19.0.0 from default catalog
    "react-dom": "catalog:",
    "zod": "catalog:"
  }
}

// packages/legacy-widget/package.json
{
  "dependencies": {
    "react": "catalog:react18",  // Uses ^18.3.0 from named catalog
    "react-dom": "catalog:react18"
  }
}
```

### .npmrc Configuration

```ini
# .npmrc — project-level pnpm settings
# Strictness
strict-peer-dependencies=false
auto-install-peers=true

# Hoisting (needed for some tools like Next.js)
public-hoist-pattern[]=*eslint*
public-hoist-pattern[]=*prettier*
shamefully-hoist=false    # Keep strict by default

# Performance
store-dir=~/.pnpm-store  # Default content-addressable store location
prefer-frozen-lockfile=true

# Registry
registry=https://registry.npmjs.org/

# Scoped registries
@myorg:registry=https://npm.pkg.github.com
//npm.pkg.github.com/:_authToken=${GITHUB_TOKEN}
```

### Patching Packages

```bash
# Create a patch for a broken dependency
pnpm patch express@4.21.0        # Opens package in temp dir for editing
# ... make your edits ...
pnpm patch-commit /tmp/abc123    # Commits the patch

# Patches stored in package.json:
# "pnpm": { "patchedDependencies": { "express@4.21.0": "patches/express@4.21.0.patch" } }
```

### Overrides (Dependency Resolution)

```jsonc
// package.json — force specific versions across the tree
{
  "pnpm": {
    "overrides": {
      "lodash": "^4.17.21",           // Force version everywhere
      "foo>bar": "^2.0.0",            // Override only within foo's deps
      "react": "$react"               // Use the version from root package.json
    },
    "peerDependencyRules": {
      "ignoreMissing": ["@babel/*"],   // Suppress peer dep warnings
      "allowedVersions": {
        "react": "19"                  // Allow React 19 even if peer asks for 18
      }
    }
  }
}
```

### CI Optimization

```yaml
# GitHub Actions — optimized pnpm setup
- uses: pnpm/action-setup@v4
  with:
    version: 9

- uses: actions/setup-node@v4
  with:
    node-version: 22
    cache: pnpm  # Caches the pnpm store automatically

- run: pnpm install --frozen-lockfile

# For monorepos — only install affected packages
- run: pnpm install --frozen-lockfile --filter "...[origin/main]"
```

```dockerfile
# Dockerfile — multi-stage with pnpm
FROM node:22-slim AS base
ENV PNPM_HOME="/pnpm"
ENV PATH="$PNPM_HOME:$PATH"
RUN corepack enable

FROM base AS deps
WORKDIR /app
COPY package.json pnpm-lock.yaml .npmrc ./
RUN --mount=type=cache,id=pnpm,target=/pnpm/store \
    pnpm install --frozen-lockfile --prod

FROM base AS build
WORKDIR /app
COPY package.json pnpm-lock.yaml .npmrc ./
RUN --mount=type=cache,id=pnpm,target=/pnpm/store \
    pnpm install --frozen-lockfile
COPY . .
RUN pnpm build

FROM base AS runtime
WORKDIR /app
COPY --from=deps /app/node_modules ./node_modules
COPY --from=build /app/dist ./dist
CMD ["node", "dist/index.js"]
```

## Best Practices

- **Always commit `pnpm-lock.yaml`** — ensures reproducible installs across environments
- **Use `--frozen-lockfile` in CI** — prevents accidental lockfile drift in pipelines
- **Use `workspace:*`** for internal deps — keeps workspace packages linked automatically
- **Use catalogs** for shared versions — eliminates version drift across workspace packages
- **Avoid `shamefully-hoist`** — it defeats pnpm's strict isolation; fix the root cause instead
- **Use `pnpm dlx`** instead of `npx` — respects pnpm's store and is more predictable
- **Enable `corepack`** for CI — `corepack enable` pins the pnpm version from `packageManager` field
- **Use filter patterns** for monorepo commands — `--filter` is more precise than `-r`
- **Set `packageManager`** in root `package.json` — `"packageManager": "pnpm@9.15.0"` for corepack

## Anti-Patterns

| Anti-Pattern | Why It's Bad | Do Instead |
|---|---|---|
| `shamefully-hoist=true` globally | Breaks pnpm's isolation model | Hoist specific packages with `public-hoist-pattern` |
| Not committing lockfile | Non-reproducible installs | Always commit `pnpm-lock.yaml` |
| `pnpm install` in CI without `--frozen-lockfile` | Can silently update lockfile | Always use `--frozen-lockfile` |
| Using `npm:` or `yarn:` in scripts | Mixes package managers | Stick to pnpm exclusively |
| Manual version sync in monorepo | Versions drift between packages | Use `catalog:` in `pnpm-workspace.yaml` |
| Installing everything globally | Pollutes system, version conflicts | Use `pnpm dlx` for one-off tools |
| Ignoring peer dependency warnings | Hidden runtime compatibility bugs | Fix peers or explicitly allow versions |
| Running `pnpm -r build` without filter | Builds everything, slow CI | Use `--filter` to target affected packages |

## Decision Guide

| Scenario | Recommendation |
|---|---|
| New project, single package | `pnpm init` + standard workflow |
| Monorepo with shared packages | `pnpm-workspace.yaml` + `workspace:*` |
| Monorepo with version alignment | Use catalogs in `pnpm-workspace.yaml` |
| CI pipeline caching | `pnpm/action-setup` + `actions/setup-node` with `cache: pnpm` |
| Docker builds | Multi-stage with `--mount=type=cache` for the store |
| Need to patch a broken dep | `pnpm patch` + `pnpm patch-commit` |
| Force a transitive dep version | Use `pnpm.overrides` in root `package.json` |
| Deploying monorepo app | `pnpm deploy --filter @myorg/web` for isolated output |
