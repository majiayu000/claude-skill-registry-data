---
name: nuxt-nitro-api
description: Build type-safe Nuxt 3 applications with Nitro API patterns. Covers validation, fetch patterns, auth, SSR, composables, background tasks, and real-time features.
---

# Nuxt 3 / Nitro API Patterns

This skill provides patterns for building type-safe Nuxt 3 applications with Nitro backends.

## When to Use This Skill

Use this skill when:
- Working in a Nuxt 3 project with TypeScript
- Building API endpoints with Nitro
- Implementing authentication with nuxt-auth-utils
- Handling SSR + client-side state
- Creating background tasks or real-time features

## Reference Files

For detailed patterns, see these topic-focused reference files:

- [validation.md](./validation.md) - Zod validation with h3, Standard Schema, error handling
- [fetch-patterns.md](./fetch-patterns.md) - useFetch vs $fetch vs useAsyncData
- [auth-patterns.md](./auth-patterns.md) - nuxt-auth-utils, OAuth, WebAuthn, middleware
- [page-structure.md](./page-structure.md) - Keep pages thin, components do the work
- [composables-utils.md](./composables-utils.md) - When to use composables vs utils
- [ssr-client.md](./ssr-client.md) - SSR + localStorage, hydration, VueUse
- [deep-linking.md](./deep-linking.md) - URL params sync with filters and useFetch
- [nitro-tasks.md](./nitro-tasks.md) - Background jobs, scheduled tasks, job queues
- [sse.md](./sse.md) - Server-Sent Events for real-time streaming
- [server-services.md](./server-services.md) - Third-party service integration patterns

## Example Files

Working examples from a Nuxt project:

- [validation-endpoint.ts](./examples/validation-endpoint.ts) - API endpoint with Zod validation
- [auth-middleware.ts](./examples/auth-middleware.ts) - Server auth middleware
- [auth-utils.ts](./examples/auth-utils.ts) - Reusable auth helpers
- [deep-link-page.vue](./examples/deep-link-page.vue) - URL params sync with filters
- [sse-endpoint.ts](./examples/sse-endpoint.ts) - SSE streaming endpoint
- [service-util.ts](./examples/service-util.ts) - Server-side service pattern

## Core Principles

1. **Let Nitro infer types** - Never add manual type params to `$fetch<Type>()` or `useFetch<Type>()`
2. **Use h3 validation** - `getValidatedQuery()`, `readValidatedBody()` with Zod schemas
3. **Composables for context, utils for pure functions** - Composables access Nuxt context, utils are pure
4. **SSR-safe code** - Guard browser APIs with `import.meta.client` or `onMounted`
5. **Keep pages thin** - Pages = layout + route params + components. Components own data fetching and logic.

## Auto-Imports Quick Reference

### Server-side (`/server` directory)

All h3 utilities auto-imported:
- `defineEventHandler`, `createError`, `getQuery`, `getValidatedQuery`
- `readBody`, `readValidatedBody`, `getRouterParams`, `getValidatedRouterParams`
- `getCookie`, `setCookie`, `deleteCookie`, `getHeader`, `setHeader`

From nuxt-auth-utils:
- `getUserSession`, `setUserSession`, `clearUserSession`, `requireUserSession`
- `hashPassword`, `verifyPassword`
- `defineOAuth*EventHandler` (Google, GitHub, etc.)

**Need to import:** `z` from "zod", `fromZodError` from "zod-validation-error"

### Client-side

All auto-imported:
- Vue: `ref`, `computed`, `watch`, `onMounted`, etc.
- VueUse: `refDebounced`, `useLocalStorage`, `useUrlSearchParams`, etc.
- Nuxt: `useFetch`, `useAsyncData`, `useRoute`, `useRouter`, `useState`, `navigateTo`

### Shared (`/shared` directory - Nuxt 3.14+)

Code auto-imported on both client AND server. Use for:
- Types and interfaces
- Pure utility functions
- Constants

## Quick Patterns

### Validation (h3 v2+ with Standard Schema)

```typescript
// Pass Zod schema directly (h3 v2+)
const query = await getValidatedQuery(event, z.object({
  search: z.string().optional(),
  page: z.coerce.number().default(1),
}));

const body = await readValidatedBody(event, z.object({
  email: z.string().email(),
  name: z.string().min(1),
}));
```

### $fetch Type Inference

```typescript
// Template literals preserve type inference (fixed late 2024)
const userId = "123";  // Literal type "123"
const result = await $fetch(`/api/users/${userId}`);
// result is typed from the handler's return type

// NEVER do this - defeats type inference
const result = await $fetch<User>("/api/users/123");  // WRONG
```

### useFetch for Page Data

```typescript
// Basic - types inferred from Nitro
const { data, status, refresh } = await useFetch("/api/users");

// Reactive query params - auto-refetch on change
const search = ref("");
const debouncedSearch = refDebounced(search, 300);  // Auto-imported
const { data } = await useFetch("/api/users", {
  query: computed(() => ({
    ...(debouncedSearch.value ? { search: debouncedSearch.value } : {}),
  })),
});

// Dynamic URL with getter
const userId = ref("123");
const { data } = await useFetch(() => `/api/users/${userId.value}`);

// New options (Nuxt 3.14+)
const { data } = await useFetch("/api/data", {
  retry: 3,          // Retry on failure
  retryDelay: 1000,  // Wait between retries
  dedupe: "cancel",  // Cancel previous request
  delay: 300,        // Debounce the request
});
```

### $fetch for Event Handlers

```typescript
// ONLY use $fetch in event handlers (onClick, onSubmit)
const handleSubmit = async () => {
  const result = await $fetch("/api/users", {
    method: "POST",
    body: { name: "Test" },
  });
};
```

### Auth Check in API

```typescript
// In server/utils/auth.ts
export async function getAuthenticatedUser(event: H3Event) {
  const session = await getUserSession(event);
  if (!session?.user) {
    throw createError({ statusCode: 401, statusMessage: "Unauthorized" });
  }
  return session.user;
}

// In API handler
export default defineEventHandler(async (event) => {
  const user = await getAuthenticatedUser(event);
  // user is typed and guaranteed to exist
});
```

### SSR-Safe localStorage

```typescript
// Option 1: import.meta.client guard
watch(preference, (value) => {
  if (import.meta.client) {
    localStorage.setItem("pref", value);
  }
});

// Option 2: onMounted
onMounted(() => {
  const saved = localStorage.getItem("pref");
  if (saved) preference.value = saved;
});

// Option 3: VueUse (SSR-safe)
const theme = useLocalStorage("theme", "light");
```

### Composable vs Util Decision

```
Needs Nuxt/Vue context (useRuntimeConfig, useRoute, refs)?
├─ YES → COMPOSABLE in /composables/use*.ts
└─ NO → UTIL in /utils/*.ts (client) or /server/utils/*.ts (server)
```

## Key Gotchas

1. **Don't use `$fetch` at top level** - Causes double-fetch (SSR + client). Use `useFetch`.
2. **Debounce search inputs** - Use `refDebounced` to avoid excessive API calls.
3. **Reset pagination on filter change** - Or users see empty page 5 with new filters.
4. **Guard browser APIs** - Use `import.meta.client`, `onMounted`, or `<ClientOnly>`.
5. **Nitro tasks are single-instance** - Can't run same task twice concurrently. Use DB job queue.
6. **useRouteQuery needs Nuxt composables** - Pass `route` and `router` explicitly.
7. **Input types aren't auto-generated** - Export Zod schemas for client use.
8. **Cookie size limit is 4096 bytes** - Store only essential session data.
9. **Ambiguous routes need type assertion** - See below.
10. **Never use generic type params with useFetch/$fetch** - See below.

### Ambiguous Route Type Inference

Nuxt generates types in `.nuxt/types/nitro-routes.d.ts` with an `InternalApi` object keyed by route paths. When routes overlap, Nuxt can't infer types from template literals:

```typescript
// Routes: GET /api/projects and GET /api/projects/:id
// If route.params.id is "", the path matches BOTH routes
const { data } = await useFetch(`/api/projects/${route.params.id}`);
// data type: unknown (ambiguous)

// Fix: Assert the specific route pattern
const { data } = await useFetch(`/api/projects/${route.params.id}` as '/api/projects/:id');
// data type: correctly inferred from /api/projects/:id handler
```

### Extracting Types from useFetch (Never Use Generic Params)

Never pass type parameters to `useFetch` or `$fetch`:

```typescript
// WRONG - Lies to type checker, breaks when endpoint changes
const { data } = await useFetch<Project[]>('/api/projects');

// RIGHT - Let Nuxt infer from the actual endpoint
const { data: projects } = await useFetch('/api/projects');
```

To use the inferred type elsewhere in your component:

```typescript
const { data: projects } = await useFetch('/api/projects');

// Get the full ref type (Ref<Project[] | null>)
type ProjectsRef = typeof projects;

// Get a single item type from an array response
type Project = NonNullable<typeof projects.value>[number];

// Use in functions/computeds
function formatProject(project: Project) {
  return `${project.name} - ${project.status}`;
}

const activeProjects = computed(() =>
  projects.value?.filter(p => p.status === 'active') ?? []
);
```

This ensures your frontend types stay in sync with your API - if the endpoint return type changes, TypeScript will catch mismatches.
