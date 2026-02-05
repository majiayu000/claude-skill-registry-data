---
name: toolchain-preferences
description: "Apply preferred toolchain and technology stack defaults: pnpm, Next.js, TypeScript, Convex, Vercel, Tailwind, shadcn/ui, Zustand, TanStack, Vitest. Use when setting up new projects, choosing dependencies, discussing stack decisions, or evaluating alternatives."
---

# Toolchain Preferences

Default technology stack and tooling choices for new projects.

## Package Management

### pnpm (Default)

**Why pnpm:**
- Faster than npm/yarn
- Disk-efficient through content-addressable storage
- Strict by default (no phantom dependencies)
- Better monorepo support

**Usage:**
```bash
pnpm install
pnpm add <package>
pnpm dev
```

### Version Management: asdf

**Node.js version per project:**
```
# .tool-versions
nodejs 22.15.0
```

Ensures consistent environments across projects and machines.

## Core Stack

### Framework: Next.js App Router + TypeScript

**Why Next.js:**
- Full-stack React framework
- Server components, streaming, React Server Components (RSC)
- Excellent developer experience, fast iteration
- Zero-config routing, API routes, server actions

**Always TypeScript:**
- Type safety from database to UI
- Better IDE support, refactoring confidence
- Catches errors at compile time

### Backend: Convex

**Why Convex:**
- Real-time database as a service
- Type-safe from database to UI (auto-generated types)
- Reactive queries with automatic caching
- No API layer needed — direct function calls
- Built-in auth, file storage, scheduling

**When to use:**
- Real-time features (chat, collaboration, live updates)
- Rapid prototyping (skip API boilerplate)
- Type-safe full-stack (database → UI)

**Alternative:** tRPC + Prisma for non-real-time apps

### Deployment: Vercel

**Why Vercel:**
- Zero-config Next.js deployment
- Edge functions, analytics, preview deployments
- Tight integration with Next.js features (middleware, ISR, etc.)
- Great DX (git push → deployed)

## UI Stack

### Styling: Tailwind CSS + shadcn/ui

**Tailwind CSS:**
- Utility-first CSS for fast iteration
- Consistent design system via `tailwind.config.ts`
- No CSS file overhead, tree-shakeable
- Responsive, dark mode, arbitrary values

**shadcn/ui:**
- Copy-paste components (NOT a dependency)
- Full control over component code
- Built on Radix primitives
- Accessible by default

**Alternative:** Use Radix UI directly for full customization

### State Management: Zustand

**Why Zustand:**
- Minimal boilerplate vs Redux
- Simple API, works with React patterns
- Good for client-side state (Convex handles server state)

**When to use:**
- Client-side UI state (modals, forms, preferences)
- Cross-component state without prop drilling

**Alternative:** React Context + hooks for simple cases

### Data Handling: TanStack Query + TanStack Table

**TanStack Query:**
- Server state management (when NOT using Convex)
- Caching, refetching, optimistic updates
- Replaces Redux for server data

**TanStack Table:**
- Headless table logic (sorting, filtering, pagination)
- Works with any UI framework
- Fully customizable, accessible

## Build Tools

### Default Build Tool by Project Type

**Next.js projects:**
- Use Next.js built-in build (Turbopack or webpack)
- Zero config, optimized for framework

**Standalone apps (React/Vue/Svelte):**
- Vite: Fast, modern, great DX
- HMR, instant server start, optimized builds

**Libraries:**
- tsup: Simple TypeScript bundler
- unbuild: Clean, minimal builds

## Testing

### Vitest (Default)

**Why Vitest:**
- Fast, modern test runner
- Compatible with Jest API (easy migration)
- Great TypeScript support
- Watch mode, coverage, snapshots

**When to use:**
- Unit tests, integration tests
- Component testing (with @testing-library/react)

**E2E Testing:**
- Playwright for end-to-end tests

## Quick Reference

### New Project Setup

```bash
# Create Next.js app with TypeScript
npx create-next-app@latest --typescript --tailwind --app

# Use pnpm
pnpm install

# Add Convex
pnpm add convex
npx convex dev

# Add shadcn/ui
npx shadcn@latest init
npx shadcn@latest add button card

# Add Zustand (if needed)
pnpm add zustand

# Add testing
pnpm add -D vitest @testing-library/react @testing-library/jest-dom
```

### Dependency Decision Tree

**Need real-time data?**
- YES → Convex
- NO → TanStack Query + API layer (or tRPC)

**Need complex client state?**
- YES → Zustand
- NO → React Context + useState/useReducer

**Need data tables?**
- YES → TanStack Table
- NO → Plain HTML table or simple list

**Need UI components?**
- Start with shadcn/ui (copy-paste)
- Customize as needed (you own the code)

## When to Deviate

### Valid Deviations

**Static sites:**
- Consider Astro instead of Next.js
- Better for content-heavy, low-interactivity sites

**Non-real-time apps:**
- tRPC + Prisma instead of Convex
- More control over database schema, migrations

**Simple projects:**
- React Context instead of Zustand
- Reduce dependencies for small apps

**Component libraries:**
- Radix UI directly instead of shadcn
- When you need 100% control from start

### Anti-Patterns to Avoid

❌ **npm/yarn** — Use pnpm for consistency

❌ **Redux** — Too much boilerplate; use Zustand or TanStack Query

❌ **Class components** — Use function components + hooks

❌ **CSS-in-JS (styled-components, Emotion)** — Runtime overhead; use Tailwind

❌ **Create React App** — Deprecated; use Vite or Next.js

❌ **Component libraries as dependencies** — Prefer shadcn copy-paste approach

## Philosophy

**Opinionated defaults, pragmatic deviations.**

These tools work well together, have been battle-tested, and provide excellent developer experience. But they're defaults, not dogma.

Choose tools that:
1. Solve real problems (not resume-driven development)
2. Have good documentation and community
3. Integrate well with the rest of the stack
4. Match project requirements (not all projects need real-time)

**Prefer boring technology that works over shiny technology that might.**
