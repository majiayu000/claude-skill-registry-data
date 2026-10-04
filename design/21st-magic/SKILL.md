---
name: 21st-magic
description: Generate and integrate premium UI components from 21st.dev Magic library into ChefFlow. Use when building new UI components, improving existing pages, redesigning surfaces, or when user mentions "make it look better", "upgrade UI", "component", or "21st".
---

# 21st Magic - UI Component Generation

## When to trigger

- Building new pages or components
- User asks to improve visual quality of existing UI
- Redesigning a surface (cards, tables, forms, navs)
- Any UI work where a polished component would elevate quality

## Workflow

1. **Identify the surface** - what page/component needs improvement
2. **Check existing pattern** - read current implementation to understand data shape
3. **Generate via 21st Magic MCP** - use `mcp__21st-magic` tools to generate component
4. **Adapt to ChefFlow** - ensure it uses:
   - Existing Tailwind config (`tailwind.config.ts`)
   - ChefFlow color tokens and design system
   - Proper TypeScript types from `types/`
   - Server/client boundary (use 'use client' only when needed)
5. **Integrate** - wire into existing data flow, server actions, props

## Integration rules

- Components go in `components/{domain}/` per module-guard
- Never replace working logic; only upgrade the visual layer
- Preserve all existing functionality when swapping components
- Keep accessibility (aria labels, keyboard nav, focus management)
- Match existing patterns in `components/ui/` for primitives

## What 21st Magic provides

- Pre-built animated components (cards, modals, tables, charts)
- Modern interaction patterns (hover states, transitions, micro-animations)
- Responsive layouts with proper breakpoints
- Component variants (sizes, states, themes)

## Do NOT use for

- Business logic or server actions
- Database queries or API routes
- Auth or security-sensitive surfaces
- Components that already look good and work well
