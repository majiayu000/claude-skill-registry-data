---
name: ts-project-initialize
description: 'TypeScript project initialization best practices'
---

<scope>

Initialize TypeScript projects with proper tooling, type checking, and framework setup.

Reference documentation: `package.md`, `workspace.md`, `typescript.md`, `oxc.md`, `hono.md`, `tanstack-spa.md`, `shadcn-ui.md`, `dev-tools.md`, `ci.md`
</scope>

<configuration_decisions>

## Key Configuration Decisions

**Project visibility**:

- Public → Include LICENSE file
- Private → Omit license

**Package structure**:

- Single package → Root-level configuration
- Workspace (monorepo) → Root shared config + per-package configs

**Application type**:

- Frontend only → TanStack Router + shadcn/ui
- Backend only → Hono
- Full-stack → Hono + TanStack Router + shadcn/ui
- npm library → No framework, focus on build/publish config
</configuration_decisions>

<setup_principles>

## Setup Dependencies and Order

**Required setup sequence** (due to configuration dependencies):

1. **Base package** (`package.md`): Foundation for all subsequent configs
2. **Workspace structure** (`workspace.md`): Only if monorepo - must precede package setup
3. **Linting/formatting** (`oxc.md`): Requires package structure to be established
4. **Application setup**: Location depends on package structure
   - Single package: Root directory
   - Workspace: Separate `packages/*/` directories
   - TypeScript (`typescript.md`): Required for all projects
   - Backend: `hono.md`
   - Frontend SPA: `tanstack-spa.md`
   - UI components: `shadcn-ui.md`
5. **Development tools** (`dev-tools.md`): Requires application structure
6. **CI/CD** (`ci.md`): Final step after all configs established

**Location constraints**:

- Single package: All configs at root
- Workspace: Shared configs at root, app-specific in `packages/*/`
</setup_principles>

<reference_index>

## Setup Reference Documents

**Core setup** (all projects):

- `package.md`: Package configuration (package.json, pnpm)
- `typescript.md`: TypeScript strict configuration
- `oxc.md`: Linting and formatting with oxc
- `dev-tools.md`: Development utilities
- `ci.md`: CI/CD pipelines

**Structure-specific**:

- `workspace.md`: Monorepo/pnpm workspace setup

**Framework-specific**:

- `hono.md`: Backend API with Hono
- `tanstack-spa.md`: Frontend SPA with TanStack Router
- `shadcn-ui.md`: UI component library setup

</reference_index>

<best_practices>

## Configuration Best Practices

**TypeScript**:

- Always use strict type checking
- Configure path aliases for clean imports

**Package management**:

- Use pnpm for all TypeScript projects
- Configure workspace protocol for monorepo dependencies

**Tooling consistency**:

- oxc for linting and formatting (faster than ESLint/Prettier)
- Consistent script names across workspace packages

</best_practices>
