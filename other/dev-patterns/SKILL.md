---
name: dev-patterns
description: System architecture patterns and coding conventions. Auto-apply when creating components, organizing files, structuring layers, refactoring code, or discussing architecture patterns like Atomic Design, Repository Pattern, DRY.
allowed-tools: Read, Grep, Glob, Bash, Edit, Write
---

# System Architecture Patterns & Conventions

Patterns và conventions áp dụng **cross-cutting** cho toàn bộ codebase.

## Pattern References

| Pattern | Reference | Khi nào apply |
|---------|-----------|---------------|
| **Atomic Design** | [atomic-design.md](atomic-design.md) | Tạo/tổ chức components |
| **Architecture Layers** | [architecture.md](architecture.md) | Tổ chức code theo layers (Repository → Service → Route) |
| **Conventions** | [conventions.md](conventions.md) | Naming, file structure, DRY, error handling |

## Project Directory Structure

```
app/
├── components/              # Atomic Design hierarchy
│   ├── atoms/               # Smallest UI elements (Button, Badge, Icon)
│   ├── molecules/           # Combinations of atoms (FormField, StatCard)
│   ├── organisms/           # Complex UI sections (DataTable, NavigationBar)
│   └── templates/           # Page layouts (AdminLayout, OnboardingLayout)
├── routes/                  # Remix routes = Pages in Atomic Design
│   └── app.*.tsx
├── models/                  # Data access layer (Prisma helpers)
├── services/                # Business logic layer
├── jobs/                    # Background jobs (BullMQ)
├── graphql/                 # Shopify GraphQL queries
├── hooks/                   # Custom React hooks
├── utils/                   # Pure utility functions
├── types/                   # Shared TypeScript types
└── config/                  # App configuration

extensions/
├── theme-app-extension/     # Shopify Theme App Extension
└── src/                     # Preact storefront source
    └── components/          # Flat structure (no atomic — too lightweight)
```

## Layer Rules (Dependency Direction)

```
Routes (app/routes/)
  ↓ imports
Services (app/services/)
  ↓ imports
Models (app/models/)
  ↓ imports
Database (Prisma client)

Rules:
  ✅ Routes → Services → Models → DB
  ✅ Routes → Models (skip service if no business logic)
  ❌ Models → Services (no upward dependency)
  ❌ Services → Routes (no upward dependency)
  ❌ Models → Routes (no upward dependency)
```

## Quick Decision Table

| Situation | Action |
|-----------|--------|
| New UI element, reusable | → `components/atoms/` |
| Combining 2-3 atoms | → `components/molecules/` |
| Complex section with logic | → `components/organisms/` |
| Page layout wrapper | → `components/templates/` |
| Full page with data | → `routes/app.*.tsx` |
| Database query/mutation | → `models/*.server.ts` |
| Business logic (multi-step) | → `services/*.server.ts` |
| Shared type definition | → `types/*.ts` |
| Pure helper function | → `utils/*.ts` (or `.server.ts`) |
| React state logic | → `hooks/use*.ts` |
| Background processing | → `jobs/*.ts` |

$ARGUMENTS
