---
name: nuxt
description: "Covers Nuxt across supported versions (3.x and 4.x): the Nitro server engine, auto-imports, file-based routing, data fetching (useFetch, useAsyncData, $fetch), hybrid rendering (SSR/SSG/ISR/SPA), modules ecosystem, server routes with H3, runtime config, TypeScript, Nuxt DevTools, and migration strategies. Use for \"Nuxt\", \"nuxt\", \"Nitro\", \"useFetch\", \"useAsyncData\", \"Nuxt 3\", \"Nuxt 4\", \"nuxt.config\", \"Nuxt modules\", \"server routes Nuxt\" questions."
license: MIT
---

# Nuxt

This skill covers Nuxt across all supported versions (3.x and 4.x), including:

- Nitro server engine: H3 event handlers, server routes, server middleware, deployment presets (15+ targets), `routeRules` for hybrid rendering
- Auto-imports: components, composables, utils, Vue core, Nuxt core -- scan directories, extend/disable
- File-based routing: dynamic params, catch-all, optional, route groups (v4), nested layouts, route middleware
- Data fetching: `useFetch`, `useAsyncData`, `$fetch`, SSR deduplication, `pick`/`transform`, lazy mode, parallel fetches
- Hybrid rendering: SSR, SSG (`nuxi generate`), ISR, SPA mode, per-route `routeRules`
- Modules ecosystem: `@nuxt/image`, `@nuxt/content`, `@nuxt/ui`, `@pinia/nuxt`, `@nuxtjs/i18n`, `defineNuxtModule`
- Runtime config: server-only vs public, environment variables, type safety
- TypeScript: strict mode, auto-generated types, separate tsconfig (v4)
- Nuxt DevTools: pages, components, imports, payload, runtime config, performance panels
- SSR: streaming, hydration, `<ClientOnly>`, `useState` for SSR-safe state
- Deployment: Node.js, Docker, Vercel, Netlify, Cloudflare, AWS Lambda, Deno, Bun

When a question is version-specific, read the matching file under `references/versions/`. When the version is unknown, give general guidance and note where behavior differs.

## How to Approach Tasks

When you receive a request:

1. **Classify** the request type:
   - **Troubleshooting** -- Load `references/diagnostics.md`
   - **Data Fetching** -- Load `references/patterns/data-fetching.md`
   - **Server Routes / API** -- Load `references/patterns/server-routes.md`
   - **Architecture / Design** -- Load `references/architecture.md`
   - **Deployment / Performance** -- Load `references/best-practices.md`
   - **Configuration** -- Reference `assets/nuxt.config.ts`

2. **Identify version** -- Determine whether the user is on Nuxt 3.x or 4.x. Key differences: `app/` directory structure, `shared/` folder, `shallowRef` default, separate TypeScript configs. If unclear, ask.

3. **Load context** -- Read the relevant reference file for deep knowledge.

4. **Analyze** -- Apply Nuxt-specific reasoning. Consider SSR implications, auto-import behavior, Nitro server context, and hybrid rendering modes.

5. **Recommend** -- Provide actionable guidance with code examples. Prefer idiomatic Nuxt patterns (`useFetch` over raw `$fetch` in setup, `useState` over `ref` for SSR state).

6. **Verify** -- Suggest validation steps (Nuxt DevTools payload panel, `nuxi prepare`, build logs).

## Core Expertise

### Nitro Server Engine

Nitro compiles server code into a single deployable output with zero external runtime dependencies (`.output/`), portable across 15+ hosting targets. Every handler is an H3 event handler.

```ts
// server/api/hello.get.ts
export default defineEventHandler(async (event) => {
  const query = getQuery(event)
  const body = await readBody(event)
  return { message: `Hello ${query.name}` }
})
```

Server routes are auto-registered from `server/api/` and `server/routes/`. HTTP method is inferred from filename suffix (`.get.ts`, `.post.ts`, `.delete.ts`).

### Hybrid Rendering with routeRules

Mix SSR, SSG, ISR, and SPA per route:

```ts
routeRules: {
  '/':             { prerender: true },      // SSG at build time
  '/blog/**':      { isr: 60 },              // ISR every 60 seconds
  '/dashboard/**': { ssr: true },            // always SSR
  '/account/**':   { ssr: false },           // SPA (client-only)
  '/api/**':       { cors: true, headers: { 'cache-control': 's-maxage=60' } },
}
```

### Auto-Imports

Nuxt scans specific directories and makes exports globally available:

| Source | What is imported |
|---|---|
| `components/` | Vue SFCs as components |
| `composables/` | All named/default exports |
| `utils/` | All named/default exports |
| Nuxt core | `useFetch`, `useState`, `useRoute`, `navigateTo`, etc. |
| Vue core | `ref`, `reactive`, `computed`, `watch`, `onMounted`, etc. |

Component naming: `components/base/Button.vue` becomes `<BaseButton>` (path flattened to PascalCase).

### Data Fetching

Three options with different SSR behaviors:

| | `useFetch` | `useAsyncData` | `$fetch` |
|---|---|---|---|
| SSR dedup | Yes | Yes | No |
| Reactive key | URL string (auto) | Explicit key arg | N/A |
| Best for | Simple URL fetches | Custom async logic | Mutations, event handlers |

```ts
// useFetch -- simple, SSR-safe
const { data, status, error, refresh } = await useFetch('/api/users', {
  pick: ['id', 'name'],
  transform: (res) => res.users,
  watch: [currentPage],
})

// useAsyncData -- custom logic, explicit key
const { data: user } = await useAsyncData(
  'user-profile',
  () => $fetch(`/api/users/${userId.value}`),
  { watch: [userId] }
)

// $fetch -- event handlers and mutations only
async function submitForm() {
  await $fetch('/api/contact', { method: 'POST', body: formData.value })
}
```

### File-Based Routing

```
pages/
  index.vue              -> /
  about.vue              -> /about
  blog/[slug].vue        -> /blog/:slug
  blog/[...path].vue     -> /blog/* (catch-all)
  [[...opt]].vue         -> optional catch-all
```

Route middleware:
```ts
// middleware/auth.ts
export default defineNuxtRouteMiddleware((to) => {
  const user = useSupabaseUser()
  if (!user.value) return navigateTo('/login')
})
```

### Runtime Config

```ts
// nuxt.config.ts
runtimeConfig: {
  databaseUrl: process.env.DATABASE_URL,     // server-only
  jwtSecret: process.env.JWT_SECRET,
  public: {                                  // exposed to client
    apiBase: process.env.NUXT_PUBLIC_API_BASE || '/api',
  }
}

// Usage in composable
const config = useRuntimeConfig()
config.databaseUrl        // server-only (throws on client)
config.public.apiBase     // available everywhere
```

### Nuxt DevTools

Enable with `devtools: { enabled: true }`. Panels: Pages, Components, Imports, Payload, Runtime Config, Performance, Terminal. Component inspector overlay shows source file, props, and slots on hover.

## Common Pitfalls

**1. Double-fetch in SSR**
Using `$fetch` in `onMounted` fetches on server AND client. Always use `useFetch`/`useAsyncData` in `<script setup>` for SSR-safe data.

**2. Using `ref` instead of `useState` for SSR state**
`ref` initializes independently on server and client. `useState` transfers state via SSR payload, preventing hydration mismatches.

**3. Key collisions in useAsyncData**
Two calls with the same key share data (intentional for caching, bug if accidental). Use unique keys.

**4. Pending forever with server: false + lazy: false**
`lazy: false` blocks SSR; `server: false` means no server fetch. Together they block indefinitely. Use `lazy: true` with `server: false`.

**5. Body in GET requests**
`readBody` is for POST/PUT/PATCH. Use `getQuery` for GET parameters.

**6. Hydration mismatches**
`Date.now()`, `localStorage`, `window` in `<script setup>` cause mismatches. Wrap in `onMounted` or `if (import.meta.client)`.

**7. Missing auto-imports**
Files must be in scanned directories (`components/`, `composables/`, `utils/`). Run `nuxi prepare` to regenerate `.nuxt/types/`.

**8. Static definePageMeta**
`definePageMeta` is hoisted and statically analyzed at build time. Avoid dynamic values (computed refs, conditionals). Use `useRoute()` at runtime.

**9. Stale data on re-navigation**
`useFetch` with a static key does not re-fetch by default. Add `watch` option or call `refresh()`.

**10. Deploying to wrong preset**
Nitro auto-detects some platforms. For explicit control, set `nitro: { preset: 'cloudflare-pages' }`.

## Version-Specific Guidance

| Version | Reference | What's version-specific |
|---|---|---|
| 3 | `references/versions/3.md` | Nuxt 3 features, compatibility version flag, migration to 4 |
| 4 | `references/versions/4.md` | `app/` directory, `shared/` folder, separate TypeScript configs, `shallowRef` default, useId, useRouteAnnouncer |

## Reference Files

- `references/architecture.md` -- Nitro, auto-imports, routing, data fetching, modules, DevTools. Read for "how does X work" questions.
- `references/best-practices.md` -- Data fetching patterns, server routes, deployment strategies, module development. Read for design and quality questions.
- `references/diagnostics.md` -- Build errors, hydration mismatches, data fetching gotchas. Read when troubleshooting.

## Configuration References

- `assets/nuxt.config.ts` -- Annotated Nuxt 4 configuration with all major options

## Pattern Guides

- `references/patterns/data-fetching.md` -- useFetch vs useAsyncData vs $fetch decision tree, SSR patterns
- `references/patterns/server-routes.md` -- Nitro API routes with validation, auth, typed responses
