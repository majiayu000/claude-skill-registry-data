---
name: nuxt
description: This skill should be used when working on Nuxt projects (v3+). Use it for building Vue applications with Nuxt's file-based routing, server-side rendering, and auto-import features. Trigger when working with .vue or .ts files in Nuxt directories (pages/, server/, composables/, middleware/), nuxt.config.ts, or when the project contains a nuxt dependency in package.json. Also trigger for questions about Nuxt concepts like composables, auto-imports, server routes, SSR/SSG patterns, or file-based routing.
---

# Nuxt Development

## Overview

This skill provides specialized guidance for developing Nuxt applications (v3+), including Vue best practices, Nuxt-specific conventions, ecosystem library knowledge, and access to up-to-date documentation.

## When to Use This Skill

Trigger this skill when:

- Working in a project with `nuxt` as a dependency in package.json
- Creating or editing `.vue` single-file components
- Working with `.ts` or `.tsx` files in Nuxt directories: `pages/`, `server/`, `composables/`, `middleware/`, `layouts/`, or `utils/`
- Working with Nuxt-specific files: `nuxt.config.ts`, `app.vue`, or any file in Nuxt convention directories
- Questions about Nuxt architecture, routing, or SSR/SSG patterns
- User mentions Nuxt-specific concepts: composables, auto-imports, server routes, server API, middleware, file-based routing
- Debugging Nuxt-specific issues or errors

## Documentation Access

### Official Nuxt Documentation

Fetch up-to-date Nuxt documentation when needed:

```
https://nuxt.com/llms.txt
```

Fetch when:

- Uncertain about current Nuxt API syntax or conventions
- User asks about specific Nuxt features or modules
- Working with recently released Nuxt features
- Encountering Nuxt-specific errors or configuration issues
- Need to verify patterns work with the specific Nuxt version in use

## Quick Reference

### Auto-Imported APIs (No Import Needed)

Nuxt automatically imports these without explicit import statements:

**Vue APIs:** `ref`, `reactive`, `computed`, `watch`, `onMounted`, `defineProps`, `defineEmits`, `defineModel`

**Nuxt Composables:** `useState`, `useFetch`, `useAsyncData`, `useRoute`, `useRouter`, `navigateTo`, `useCookie`, `useHead`, `useSeoMeta`, `useRuntimeConfig`, `showError`, `clearError`

**Auto-imports:**

- Components from `components/` directory
- Composables from `composables/` directory
- Server utilities from `server/utils/` directory

### File-Based Conventions

**Routing:**

- `pages/index.vue` → `/`
- `pages/about.vue` → `/about`
- `pages/users/[id].vue` → `/users/:id` (dynamic route)

**Server API:**

- `server/api/users.get.ts` → `/api/users` (GET endpoint)
- `server/api/users.post.ts` → `/api/users` (POST endpoint)
- `server/routes/healthz.ts` → `/healthz` (custom route)

**Layouts & Middleware:**

- `layouts/default.vue` - Default layout
- `middleware/auth.ts` - Named middleware (use via `definePageMeta({ middleware: 'auth' })`)
- `middleware/analytics.global.ts` - Global middleware (runs on every route)

### Nuxt CLI Commands

**Development:**

- `nuxt dev` - Start development server
- `nuxt dev --host` - Expose to network

**Building:**

- `nuxt build` - Production build
- `nuxt generate` - Static site generation
- `nuxt preview` - Preview production build

**Analysis:**

- `nuxt analyze` - Bundle size analysis
- `nuxt typecheck` - Type checking
- `nuxt info` - Environment info for bug reports

## Project Dependency Detection

**Important:** Before providing library-specific guidance, check if the library is installed by examining `package.json`. Only include library-specific advice for dependencies that exist in the project.

### Core Libraries (Included by Default)

- **Vue** - Component framework (auto-imported)
- **Vue Router** - Routing (file-based, managed by Nuxt)
- **Nitro** - Server engine (built into Nuxt)

### Optional Libraries to Check

Check `package.json` for these before suggesting their features:

**State & Utilities:**

- `pinia` or `@pinia/nuxt` - State management → See `references/pinia.md`
- `@vueuse/core` or `@vueuse/nuxt` - Composition utilities → See `references/vueuse.md`
- `drizzle-orm` - Database ORM → See `references/drizzle-db0.md`
- `@nuxthub/core` - Full-stack platform (DB, blob, KV, cache) → See `references/nuxthub.md`

**Testing:**

- `@nuxt/test-utils` + `vitest` - Unit and component testing → See `references/nuxt-testing.md`

**Core Nuxt Modules (Dedicated References):**

- `@nuxt/ui` - UI component library → See `references/nuxt-ui.md`
- `@nuxt/image` - Image optimization → See `references/nuxt-image.md`
- `@nuxt/content` - File-based CMS → See `references/nuxt-content.md`
- `@nuxtjs/i18n` - Internationalization → See `references/nuxt-i18n.md`
- `@nuxtjs/tailwindcss` - Tailwind CSS → See `references/tailwind.md`

**Other Nuxt Modules:**

- `@nuxt/icon`, `@nuxtjs/seo`, `@nuxtjs/color-mode` → See `references/nuxt-modules.md`
- `@nuxt/eslint`, `@nuxt/fonts`, `@nuxt/scripts`, `nuxt-security` → See `references/nuxt-modules.md`

## References

This skill includes detailed reference documentation for specific topics. Load these files as needed when working with specific features:

### Core Best Practices

**`references/vue-best-practices.md`** - Vue component patterns and conventions

- Use when writing or reviewing Vue components
- Covers: Script setup syntax, props/emits/v-model, component structure, template directives, reactivity patterns

**`references/nuxt-patterns.md`** - Common Nuxt patterns and recipes

- Use when implementing features or solving common tasks
- Covers: Data fetching, SEO/meta tags, error handling, environment config, server API routes, middleware, state management, composables, layouts, plugins

### Core Nuxt Modules (Comprehensive Documentation)

**`references/nuxt-ui.md`** - Nuxt UI component library (Last updated: 2025-01)

- Only use if `@nuxt/ui` is installed
- Covers: v3/v4 setup and migration, components (forms, buttons, modals, tables), Tailwind v4 integration, theming, validation, troubleshooting
- **Important:** Includes version-specific breaking changes and setup requirements

**`references/tailwind.md`** - Tailwind CSS in Nuxt (Last updated: 2025-01)

- Only use if `@nuxtjs/tailwindcss` is installed
- Covers: v3/v4 setup, configuration, responsive design, dark mode, custom utilities, plugins, JIT mode, performance optimization

**`references/nuxt-image.md`** - Image optimization (Last updated: 2025-01)

- Only use if `@nuxt/image` is installed
- Covers: NuxtImg/NuxtPicture components, image providers, lazy loading, responsive images, performance optimization

**`references/nuxt-content.md`** - File-based CMS (Last updated: 2025-01)

- Only use if `@nuxt/content` is installed
- Covers: Markdown/YAML content, queryContent API, components (ContentDoc, ContentList), navigation, search, pagination, syntax highlighting

**`references/nuxt-i18n.md`** - Internationalization (Last updated: 2025-01)

- Only use if `@nuxtjs/i18n` is installed
- Covers: Multi-language routing, translations, locale switching, SEO, number/date formatting, pluralization, composables

### State Management & Utilities

**`references/pinia.md`** - Pinia state management

- Only use if `pinia` or `@pinia/nuxt` is installed
- Covers: Store definition, component usage, SSR, persistence, testing

**`references/vueuse.md`** - VueUse composables

- Only use if `@vueuse/core` or `@vueuse/nuxt` is installed
- Covers: State management composables, browser APIs, element interaction, utilities, common patterns

**`references/drizzle-db0.md`** - Database with Drizzle ORM

- Only use if `drizzle-orm` is installed (without NuxtHub)
- Covers: Setup, schema definition, CRUD operations, queries, joins, filtering, transactions, migrations, type safety

**`references/nuxthub.md`** - NuxtHub Full-Stack Platform (Last updated: 2025-12)

- Only use if `@nuxthub/core` is installed
- Covers: Multi-vendor deployment, Drizzle ORM integration, blob storage, KV storage, caching, migrations CLI, DevTools integration
- **Note:** NuxtHub v0.10 uses Drizzle ORM with `hub:db` imports - different from standalone Drizzle setup

### Testing

**`references/nuxt-testing.md`** - Nuxt Test Utils with Vitest (Last updated: 2025-12)

- Only use if `@nuxt/test-utils` and `vitest` are installed
- Covers: Vitest configuration, test environments, mountSuspended, renderSuspended, mockNuxtImport, mockComponent, registerEndpoint, component/composable/API testing patterns

### Other Modules

**`references/nuxt-modules.md`** - Other official Nuxt modules

- Brief overview of: @nuxt/icon, @nuxtjs/seo, @nuxtjs/color-mode, @nuxt/eslint, @nuxt/fonts, @nuxt/scripts, nuxt-security
- For detailed guidance on @nuxt/ui, @nuxt/image, @nuxt/content, @nuxtjs/i18n, or @nuxtjs/tailwindcss, use their dedicated reference files instead

## How to Use This Skill

1. **Check dependencies** - Examine `package.json` first to know what libraries are available
2. **Follow Vue best practices** - Apply patterns from `vue-best-practices.md` to all component code
3. **Leverage auto-imports** - Don't manually import Nuxt/Vue composables that are auto-imported
4. **Use file-based conventions** - Follow Nuxt's directory structure for routing, APIs, and middleware
5. **Reference library docs** - When a library is installed, consult its reference file for specific patterns
6. **Verify version-specific features** - Reference files include "Last updated" dates; verify with official docs for version-specific details
7. **Fetch official docs** - For recent features or uncertainty, fetch from https://nuxt.com/llms.txt or module-specific documentation URLs

### Version-Specific Information

- **Reference files with dates** (marked "Last updated: YYYY-MM") contain version-specific info
- **Verify with official docs** when:
  - Working with modules not documented in references
  - Module version differs significantly from documentation date
  - Encountering breaking changes or migration scenarios
  - Uncertain about syntax or API for current version
- **Fallback principle:** If reference documentation doesn't match project needs, fetch official docs rather than guessing

## Important Conventions

### Component Files Must:

- Use `<script setup lang="ts">` syntax
- Place `<template>` section first, before `<script>` and `<style>`
- Use type-based `defineProps()`, `defineEmits()`, and `defineModel()`
- Use multi-word component names (except pages/layouts)
- Use `v-for="item of items"` with `:key`
- Prefer `ref()` over `reactive()`

### TypeScript Organization:

- Place all types/interfaces in `/types` directory (or `/app/types` in Nuxt 4)
- Organize by domain: `types/user.ts`, `types/post.ts`, `types/auth.ts`
- **NO barrel exports** - import directly from specific files: `import type { User } from '~/types/user'`
- Use PascalCase naming conventions:
  - Props interfaces: `ButtonProps`, `CardProps`
  - State interfaces: `AuthState`, `UserState`
  - API types: `CreateUserRequest`, `CreateUserResponse`
- **Don't use `as any`** - prefer type guards, type narrowing, or `as unknown as Type` when absolutely necessary

### File Structure (Nuxt 4):

- Nuxt 4 supports optional `/app` directory for app-specific code
- Components can live in `/components` or `/app/components`
- Composables can live in `/composables` or `/app/composables`
- Types can live in `/types` or `/app/types`
- Both root-level and `/app` directory structures are supported

### Data Fetching State Handling:

- Use `status` property (not deprecated `pending`)
- Status values: `'idle' | 'pending' | 'success' | 'error'`
- Destructure: `const { data, status, error } = await useFetch(...)`
- Handle all states in templates:
  ```vue
  <div v-if="status === 'pending'">Loading...</div>
  <div v-else-if="status === 'error'">Error: {{ error }}</div>
  <div v-else>{{ data }}</div>
  ```

### Styling Strategy:

- Check `package.json` for `@nuxtjs/tailwindcss` dependency
- **If Tailwind is installed:** Prefer Tailwind utility classes in templates
  - Use arbitrary variants for scrollbars: `[&::-webkit-scrollbar]:w-1.5`
  - Use `@theme` directive for custom animations and CSS variables
  - Use arbitrary variants for pseudo-elements: `before:content-['★']`
- **If Tailwind is NOT installed:** Use `<style scoped>` for component styles
- **Use `<style>` only for:** Very complex keyframes, cross-browser scrollbars, or unreadable utility expressions

### Accessibility:

- Add appropriate ARIA attributes to interactive elements
- Ensure keyboard navigation support (tab order, enter/space handlers)
- Use semantic HTML elements (`<button>`, `<nav>`, `<main>`, etc.)

### Nuxt Projects Should:

- Don't manually import auto-imported composables
- Use `useFetch` for API calls instead of manual fetch
- Define server routes in `server/api/` with `.get.ts`, `.post.ts` naming
- Use `useState` for shared state across components
- Use `definePageMeta` for page-specific config (middleware, layout, etc.)

### When Libraries Are Installed:

- **Pinia** - Use for complex state management across many components
- **VueUse** - Prefer VueUse composables over custom implementations for common patterns
- **Drizzle** - Use for type-safe database operations with full TypeScript inference

### VueUse Integration Guidelines:

When encountering custom utility implementations for common patterns, check if VueUse provides an equivalent solution:

- **State patterns:** `useAsyncData`, `useToggle`, `useCounter`, `useLocalStorage`, `useSessionStorage`
- **DOM interactions:** `useMouse`, `useScroll`, `useElementVisibility`, `useIntersectionObserver`, `useResizeObserver`
- **Browser APIs:** `useClipboard`, `useMediaQuery`, `useDark`, `usePreferredDark`, `useGeolocation`
- **Utilities:** `refDebounced`, `useDebounceFn`, `refThrottled`, `useThrottleFn`, `useInterval`, `useTimeout`

**When to suggest VueUse:**

- Detecting bespoke implementations of the above patterns
- User asks about utilities for common tasks (debouncing, throttling, etc.)
- Building features that require browser API abstractions

**Only suggest if:**

- `@vueuse/core` or `@vueuse/nuxt` is in package.json, OR
- User explicitly asks about VueUse or requests suggestions for utility libraries

**Avoid:**

- Force VueUse if not installed
- Suggest VueUse for simple one-off logic that doesn't need a composable
