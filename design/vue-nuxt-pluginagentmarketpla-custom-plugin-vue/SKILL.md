---
name: vue-nuxt
description: Master Nuxt.js - SSR, SSG, Nitro Server, Modules, Auto-imports, Deployment
sasmp_version: "1.3.0"
bonded_agent: 05-vue-nuxt
bond_type: PRIMARY_BOND
version: "2.0.0"
last_updated: "2025-01"
---

# Vue Nuxt Skill

Production-grade skill for mastering Nuxt 3 and building full-stack Vue applications.

## Purpose

**Single Responsibility:** Teach Nuxt 3 architecture including SSR/SSG, Nitro server, modules, auto-imports, and deployment strategies.

## Parameter Schema

```typescript
interface NuxtParams {
  topic: 'config' | 'ssr' | 'ssg' | 'api' | 'modules' | 'deploy' | 'all';
  level: 'beginner' | 'intermediate' | 'advanced';
  context?: {
    hosting?: 'vercel' | 'netlify' | 'cloudflare' | 'node';
    rendering?: 'ssr' | 'ssg' | 'hybrid';
  };
}
```

## Learning Modules

### Module 1: Nuxt Fundamentals
```
Prerequisites: vue-fundamentals, vue-composition-api
Duration: 3-4 hours
Outcome: Set up and configure Nuxt 3
```

| Topic | Concept | Exercise |
|-------|---------|----------|
| Installation | nuxi create | New project |
| Config | nuxt.config.ts | Basic setup |
| Directory | pages/, components/ | Structure app |
| Auto-imports | No manual imports | Use composables |
| Dev tools | Nuxt DevTools | Debugging |

### Module 2: File-Based Routing
```
Prerequisites: Module 1
Duration: 2 hours
Outcome: Master Nuxt routing conventions
```

| Pattern | File | Route |
|---------|------|-------|
| Static | `pages/about.vue` | `/about` |
| Dynamic | `pages/user/[id].vue` | `/user/:id` |
| Catch-all | `pages/[...slug].vue` | `/*` |
| Optional | `pages/[[optional]].vue` | `/:optional?` |
| Nested | `pages/dashboard/settings.vue` | `/dashboard/settings` |

**Page Metadata:**
```vue
<script setup>
definePageMeta({
  layout: 'admin',
  middleware: ['auth'],
  title: 'Dashboard'
})
</script>
```

### Module 3: Data Fetching
```
Prerequisites: Module 2
Duration: 3-4 hours
Outcome: Fetch data correctly in Nuxt
```

| Composable | Use Case | Example |
|------------|----------|---------|
| useFetch | Simple fetching | API calls |
| useAsyncData | Full control | Transform data |
| useLazyFetch | Non-blocking | Secondary data |
| $fetch | Server-side | API routes |

**Fetching Patterns:**
```typescript
// Block navigation
const { data } = await useFetch('/api/user')

// Non-blocking
const { data, pending } = useLazyFetch('/api/posts')

// With transform
const { data } = await useAsyncData('user',
  () => $fetch('/api/user'),
  { transform: (d) => d.user }
)
```

### Module 4: Server API (Nitro)
```
Prerequisites: Module 3
Duration: 3-4 hours
Outcome: Build server API routes
```

| Topic | Location | Exercise |
|-------|----------|----------|
| GET | `server/api/users.get.ts` | List users |
| POST | `server/api/users.post.ts` | Create user |
| Dynamic | `server/api/users/[id].ts` | Get by ID |
| Middleware | `server/middleware/` | Auth check |
| Utils | `server/utils/` | Shared code |

**API Route Example:**
```typescript
// server/api/users/[id].get.ts
export default defineEventHandler(async (event) => {
  const id = getRouterParam(event, 'id')

  if (!id) {
    throw createError({ statusCode: 400, message: 'ID required' })
  }

  const user = await db.user.findUnique({ where: { id } })

  if (!user) {
    throw createError({ statusCode: 404, message: 'Not found' })
  }

  return user
})
```

### Module 5: Rendering & Deployment
```
Prerequisites: Modules 1-4
Duration: 3 hours
Outcome: Deploy Nuxt applications
```

| Mode | Config | Use Case |
|------|--------|----------|
| SSR | `ssr: true` | Dynamic content |
| SSG | `routeRules: { prerender }` | Static content |
| SPA | `ssr: false` | Client-only |
| Hybrid | `routeRules` per route | Mixed content |

**Deployment Targets:**
| Platform | Preset | Config |
|----------|--------|--------|
| Vercel | `vercel` | Zero-config |
| Netlify | `netlify` | netlify.toml |
| Cloudflare | `cloudflare-pages` | wrangler.toml |
| Node | `node-server` | Docker |

## Validation Checkpoints

### Beginner Checkpoint
- [ ] Create Nuxt app with pages
- [ ] Use auto-imported composables
- [ ] Fetch data with useFetch
- [ ] Create basic API route

### Intermediate Checkpoint
- [ ] Build dynamic routes with params
- [ ] Implement middleware
- [ ] Create CRUD API routes
- [ ] Use layouts and error pages

### Advanced Checkpoint
- [ ] Configure hybrid rendering
- [ ] Implement auth with middleware
- [ ] Deploy to production
- [ ] Optimize performance

## Retry Logic

```typescript
const skillConfig = {
  maxAttempts: 3,
  backoffMs: [1000, 2000, 4000],
  onFailure: 'simplify_config'
}
```

## Observability

```yaml
tracking:
  - event: project_created
    data: [template, modules]
  - event: api_route_built
    data: [method, path]
  - event: deployed
    data: [platform, render_mode]
```

## Troubleshooting

### Common Issues

| Issue | Cause | Solution |
|-------|-------|----------|
| Hydration mismatch | SSR/client diff | Use `<ClientOnly>` |
| Auto-import fails | Wrong directory | Check naming |
| API 500 error | Server error | Check server logs |
| Build fails | Config error | Validate nuxt.config |

### Debug Steps

1. Check Nuxt DevTools
2. Review server/api logs
3. Verify nuxt.config.ts
4. Test API routes directly

## Unit Test Template

```typescript
import { describe, it, expect } from 'vitest'
import { setup, $fetch } from '@nuxt/test-utils'

describe('API Routes', async () => {
  await setup({ server: true })

  it('returns users', async () => {
    const users = await $fetch('/api/users')
    expect(Array.isArray(users)).toBe(true)
  })

  it('returns 404 for missing user', async () => {
    const response = await $fetch('/api/users/999', {
      ignoreResponseError: true
    })
    expect(response.statusCode).toBe(404)
  })
})
```

## Usage

```
Skill("vue-nuxt")
```

## Related Skills

- `vue-composition-api` - Prerequisite
- `vue-testing` - Testing Nuxt apps
- `vue-typescript` - Type-safe Nuxt

## Resources

- [Nuxt 3 Documentation](https://nuxt.com/docs)
- [Nitro Documentation](https://nitro.unjs.io/)
- [Nuxt Modules](https://nuxt.com/modules)
