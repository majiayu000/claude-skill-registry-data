---
name: nuxt
description: Nuxt auto-imports, file-based routing, server routes, data fetching (useFetch/useAsyncData), modules ecosystem, hybrid rendering, SEO with useHead, and auto-imported composables. Use when building Nuxt applications.
---

## nuxt

Nuxt simplifies Vue development with conventions and auto-imports.

### Core Concepts
- Auto-imports: components/, composables/, utils/ files are auto-imported
- File-based routing: pages/ directory mirrors routes automatically
- Hybrid rendering: SSR, SSG, SWR per page with route rules

### Common Patterns
- useFetch for data fetching with SSR support and deduplication
- useAsyncData for fine-grained control over fetch strategy
- server/ directory for API routes and middleware

### Best Practices
- Leverage auto-imports instead of manual imports
- Use Nuxt modules for auth, content, SEO, and more
- Configure routeRules for per-page rendering strategy

### Common Code Patterns
- useHead for per-page meta tags and SEO metadata
- pages/index.vue as home route, pages/[id].vue for dynamic routes
- Server routes in server/api/ return JSON automatically
