---
name: nycraves
description: "Complete development guide for the NYCRAVES codebase. Use this skill when creating any new code - components, pages, features, data functions, or utilities. Ensures visual consistency (brutalist dark theme), code consistency (established patterns), and proper Next.js 16 architecture (caching, Server Components, loading states). Triggers on (1) Creating new components, (2) Building new pages, (3) Adding features, (4) Writing data functions, (5) Questions about patterns or conventions."
---

# NYCRAVES Development Guide

Complete patterns and conventions for the NYCRAVES NYC rave events app.

## What This Skill Covers

1. **UI Design System** - Brutalist dark-mode aesthetic
2. **Component Patterns** - Structure, naming, exports
3. **Architecture** - Data fetching, caching, utilities
4. **Next.js 16** - Cache Components, Server/Client patterns

## Core Principles

1. **Consistency over creativity** - Match existing patterns exactly
2. **Server Components by default** - Only use `'use client'` when necessary
3. **Centralized utilities** - Never duplicate functions across files
4. **Centralized constants** - Import from `lib/constants/`, don't hardcode
5. **Barrel exports always** - Every folder needs `index.ts` with named exports
6. **Cache everything** - Data functions use `'use cache'` + `cacheTag` + `cacheLife`

## Quick Reference

### Creating a New Component

1. Place in `/components/[domain]/`
2. Add `'use client'` only if using hooks/browser APIs
3. Define TypeScript interface for props
4. Follow design tokens from [design-tokens.md](references/design-tokens.md)
5. Match structure from [component-patterns.md](references/component-patterns.md)
6. Add named export to domain's `index.ts`

### Creating a Data Function

1. Place in `/lib/data/[domain].ts`
2. Add `'use cache'` directive
3. Add `cacheTag('[domain]')` for invalidation
4. Add `cacheLife('hours')` or `'days'`
5. Export from `lib/data/index.ts`

See [architecture-patterns.md](references/architecture-patterns.md) for full examples.

### Creating a New Utility

1. Check if similar function exists in `lib/utils.ts`
2. If reusable (2+ files), add to `lib/utils.ts`
3. Add JSDoc comment explaining purpose
4. Import from `@/lib/utils` everywhere

## Reference Files

Load these as needed for detailed patterns and examples:

- **[design-tokens.md](references/design-tokens.md)** - Typography, colors, spacing, borders, interactive states
- **[component-patterns.md](references/component-patterns.md)** - File organization, component structure, common UI patterns, page layouts
- **[architecture-patterns.md](references/architecture-patterns.md)** - Data fetching, caching, utilities, constants, import order, anti-patterns
