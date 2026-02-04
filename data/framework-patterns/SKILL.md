---
name: framework-patterns
description: Modern patterns for Next.js 16 and TanStack Start v1
---

# Framework Patterns

**Purpose**: Detect framework → Load resources

- Keywords: next.js, nextjs, tanstack start, tanstack router, app router, server component, client component, route handler, route loader, api, endpoint, middleware, integration, router, routing, navigation, link

## Detection

| File | Framework | Load |
|------|-----------|------|
| `next.config.js\|mjs\|ts` | Next.js 16 | `resources/nextjs-patterns.md` |
| `routeTree.gen.ts` | TanStack Start v1 | `resources/tanstack-start-patterns.md` |
| `convex/` dir exists | + Convex backend | `resources/convex-integration.md` |
| Migrating frameworks | Migration | `resources/migration.md` |
| `reactCompiler: true` in config | + React Compiler | `resources/react-compiler.md` |

## Load Strategy

1. Detect: `next.config.*` → Next.js, `routeTree.gen.ts` → TanStack
2. Load primary: nextjs-patterns.md OR tanstack-start-patterns.md
3. If `convex/` → + convex-integration.md
4. If React Compiler → + react-compiler.md
5. If migrating → migration.md (instead of primary)

**Contexts**:
- Next.js: 43 + 500 = 550 lines
- Next.js + Convex: 43 + 500 + 600 = 1,150 lines
- TanStack + Convex: 43 + 550 + 600 = 1,200 lines
- No Convex: Skip convex-integration.md (saves 600 lines)

**Rule**: Never load all. Load framework + backend only.
