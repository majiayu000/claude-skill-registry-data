---
name: nx-workspace-architecture
description: Guide structuring new features in Nx workspaces. Use when user asks about creating libraries, organizing code, or where to place new features.
allowed-tools: Bash, Glob, Grep, Read
---

# Nx Workspace Architecture

## Core Principles

1. **Domain over Technical** - organize by business domains (products, orders, checkout), not technical types (components, services)
2. **Thin App Shell** - apps are deployment containers; business logic lives in libs
3. **Explicit Boundaries** - use Nx projects to enforce separation, not just folders

## Library Types

| Prefix        | Purpose                                 | Can Import                  |
| ------------- | --------------------------------------- | --------------------------- |
| `feat-*`      | Smart components, pages, business logic | feat, ui, data-access, util |
| `ui-*`        | Presentational/dumb components          | ui, util                    |
| `data-access` | API calls, state management             | data-access, util           |
| `util`        | Pure functions, helpers, types          | util only                   |

## Folder Structure

```
packages/
├── {domain}/           # e.g. products, orders, checkout
│   ├── data-access/
│   ├── feat-{name}/
│   ├── ui-{name}/
│   └── util/
└── shared/             # cross-domain utilities
```

## Tagging Strategy

Add to project.json:

- `scope:{domain}` - vertical boundary (products, orders, shared)
- `type:{library-type}` - horizontal layer (feature, ui, data-access, util)

## Decision Flow

When user wants to add new functionality:

1. **Identify domain** - which business area does it belong to?
2. **Determine library type**:
   - Has routing/pages? → `feat-*`
   - Purely visual component? → `ui-*`
   - API/state logic? → `data-access`
   - Pure utilities? → `util`
3. **Check existing libs** - can it extend an existing library?
4. **Create new lib only if** needed for clear separation

## When to Split Libraries

Split when you observe:

- Frequent cross-library changes for single features
- Circular dependencies emerging
- Unclear ownership between teams
- Single lib growing too large (>20 files is a smell)

## Generator Commands

Use the nx-generators skill.
