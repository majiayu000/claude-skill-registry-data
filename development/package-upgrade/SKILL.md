---
name: Package Upgrade
description: Systematic approach for upgrading packages in the Baseplate monorepo, ensuring consistency between monorepo dependencies and generated project code.
---

# Package Upgrade Skill

Use this skill when the user asks to upgrade packages, update dependencies, or mentions upgrading specific npm packages in the Baseplate monorepo.

## Overview

Baseplate has a dual-location package management system:

1. **Monorepo catalog** (`pnpm-workspace.yaml`) - Defines versions for the Baseplate development environment
2. **Generator constants** - Defines versions that get injected into generated projects

Both locations must be kept in sync to ensure generated projects use the intended package versions.

## Step-by-Step Process

### 1. Identify Package Locations

Before upgrading, identify where the package is defined:

**Common generator constants locations:**
- `packages/react-generators/src/constants/react-packages.ts` - React, Vite, Tailwind, UI libraries
- `packages/fastify-generators/src/constants/fastify-packages.ts` - Fastify, server-side packages
- `packages/core-generators/src/constants/core-packages.ts` - Core Node.js utilities

Search commands:
```bash
# Search for package in catalog
grep "package-name" pnpm-workspace.yaml

# Search for package in generator constants
grep -r "package-name" packages/*/src/constants/
```

### 2. Check Current and Latest Versions

```bash
# Get latest version from npm
npm view package-name version

# Get all available versions (helpful for major version planning)
npm view package-name versions --json
```

### 3. Research Breaking Changes

Before upgrading, especially for major versions:
- Check the package's CHANGELOG.md or release notes
- Look for migration guides
- Check compatibility with other packages (peer dependencies)

### 4. Update Package Versions

#### 4.1 Update Monorepo Catalog

Edit `pnpm-workspace.yaml`:
```yaml
catalog:
  package-name: NEW_VERSION
```

#### 4.2 Update Generator Constants

Find and update the appropriate constants file:
```typescript
export const PACKAGES = {
  'package-name': 'NEW_VERSION',
} as const;
```

### 5. Install and Resolve Dependencies

```bash
# Install new versions
pnpm install

# Resolve duplicate dependencies and conflicts
pnpm dedupe
```

**Note:** `pnpm dedupe` is crucial as it resolves version conflicts that can occur when upgrading packages with complex dependency trees.

### 6. Sync Generated Projects

Update all example projects to use the new package versions:

```bash
# Sync all example projects
pnpm start sync-examples
```

This command:
- Regenerates all projects in `examples/` directory
- Updates `package.json` files with new versions
- Ensures generated code reflects any API changes

### 7. Verification and Testing

```bash
# Run type checking across all packages
pnpm typecheck

# Run linting (with auto-fix)
pnpm lint:only:affected -- --fix

# Run tests if available
pnpm test:affected

# Build all packages to ensure compatibility
pnpm build
```

### 8. Create Changeset

After successfully upgrading packages, create a changeset:

```bash
echo "---
'@baseplate-dev/react-generators': patch
---

Upgrade package-name to X.Y.Z

- package-name: OLD_VERSION → NEW_VERSION" > .changeset/upgrade-package-name.md
```

**Changeset guidelines:**
- Use patch level for most package upgrades unless they introduce breaking changes
- Include affected package names in the frontmatter
- List all upgraded packages with version changes

## Package Categories

### Frontend Packages (React Generators)
**Location:** `packages/react-generators/src/constants/react-packages.ts`

Common packages: `react`, `react-dom`, `vite`, `@vitejs/plugin-react`, `tailwindcss`, `@tailwindcss/vite`, `@tanstack/react-router`, `@apollo/client`, `graphql`

### Backend Packages (Fastify Generators)
**Location:** `packages/fastify-generators/src/constants/fastify-packages.ts`

Common packages: `fastify`, `@pothos/core`, `prisma`, `zod`

### Core Packages (Core Generators)
**Location:** `packages/core-generators/src/constants/core-packages.ts`

Common packages: `typescript`, `eslint`, `prettier`, `vitest`

## Troubleshooting

### Peer Dependency Warnings
1. Check if newer versions of the package are available
2. Look for compatibility matrices in package documentation
3. Use `pnpm dedupe` to resolve conflicts

### Type Errors After Upgrade
1. Check the package's TypeScript definitions
2. Update imports and usage to match new API
3. Install updated `@types/*` packages if needed

### Build Failures
1. Check package changelog for breaking configuration changes
2. Update relevant config files (vite.config.ts, etc.)
3. Look for migration guides in package documentation

## Best Practices

1. **Batch Related Updates** - Group related packages together (e.g., React ecosystem, Vite ecosystem)
2. **Test Major Upgrades Separately** - Create a separate branch for major version upgrades
3. **Check Example Projects** - Manually test generated example projects after upgrading
4. **Version Pinning Strategy:**
   - Patch versions: Generally safe to auto-update
   - Minor versions: Review changelog, usually safe
   - Major versions: Always test thoroughly, may require code changes
