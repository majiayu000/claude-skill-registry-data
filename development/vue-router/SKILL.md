---
name: vue-router
description: Master Vue Router - Navigation, Guards, Lazy Loading, Meta Fields, History Modes
sasmp_version: "1.3.0"
bonded_agent: 04-vue-router
bond_type: PRIMARY_BOND
version: "2.0.0"
last_updated: "2025-01"
---

# Vue Router Skill

Production-grade skill for mastering Vue Router and building robust navigation systems.

## Purpose

**Single Responsibility:** Teach Vue Router configuration, navigation patterns, route guards, lazy loading, and advanced routing techniques.

## Parameter Schema

```typescript
interface VueRouterParams {
  topic: 'config' | 'guards' | 'lazy-loading' | 'meta' | 'navigation' | 'all';
  level: 'beginner' | 'intermediate' | 'advanced';
  context?: {
    auth_required?: boolean;
    app_type?: 'spa' | 'ssr';
  };
}
```

## Learning Modules

### Module 1: Router Setup & Configuration
```
Prerequisites: vue-fundamentals
Duration: 2 hours
Outcome: Configure Vue Router
```

| Topic | Concept | Exercise |
|-------|---------|----------|
| Installation | Vue Router setup | Basic config |
| Routes array | Route definitions | Multi-page app |
| History modes | Hash vs HTML5 | Production setup |
| Router-view | Outlet component | Layout system |
| Router-link | Navigation links | Navigation menu |

### Module 2: Dynamic & Nested Routes
```
Prerequisites: Module 1
Duration: 2-3 hours
Outcome: Build complex route structures
```

| Pattern | Example | Exercise |
|---------|---------|----------|
| Dynamic params | `/user/:id` | User profile |
| Optional params | `/user/:id?` | Optional filters |
| Catch-all | `/:pathMatch(.*)*` | 404 page |
| Nested routes | `/dashboard/settings` | Admin layout |
| Named views | Multiple outlets | Dashboard widgets |

### Module 3: Navigation Guards
```
Prerequisites: Modules 1-2
Duration: 3-4 hours
Outcome: Secure routes with guards
```

| Guard Type | Scope | Use Case |
|------------|-------|----------|
| beforeEach | Global | Auth check |
| beforeEnter | Per-route | Role check |
| beforeRouteEnter | Component | Data prefetch |
| beforeRouteUpdate | Component | Param change |
| beforeRouteLeave | Component | Unsaved changes |
| afterEach | Global | Analytics |

**Guard Composition:**
```typescript
router.beforeEach(async (to, from) => {
  // Auth check
  if (to.meta.requiresAuth && !isAuthenticated()) {
    return { name: 'Login', query: { redirect: to.fullPath } }
  }

  // Role check
  if (to.meta.roles && !hasRole(to.meta.roles)) {
    return { name: 'Unauthorized' }
  }

  return true
})
```

### Module 4: Lazy Loading & Code Splitting
```
Prerequisites: Module 3
Duration: 2 hours
Outcome: Optimize route loading
```

| Technique | Implementation | Benefit |
|-----------|----------------|---------|
| Basic lazy | `() => import()` | Smaller bundles |
| Named chunks | webpackChunkName | Grouped loading |
| Prefetching | router.afterEach | Faster navigation |
| Loading states | Async components | Better UX |

### Module 5: Advanced Patterns
```
Prerequisites: Modules 1-4
Duration: 3 hours
Outcome: Expert routing techniques
```

| Pattern | Use Case | Exercise |
|---------|----------|----------|
| Route meta | Page metadata | SEO, auth, layout |
| Scroll behavior | Scroll position | Saved positions |
| Transitions | Page animations | Enter/leave effects |
| Route modules | Large apps | Feature-based routes |

## Validation Checkpoints

### Beginner Checkpoint
- [ ] Set up router with basic routes
- [ ] Use router-link and router-view
- [ ] Create dynamic route with params
- [ ] Access route params in component

### Intermediate Checkpoint
- [ ] Implement auth guard
- [ ] Create nested route layout
- [ ] Add lazy loading to routes
- [ ] Use route meta for titles

### Advanced Checkpoint
- [ ] Build full auth flow with guards
- [ ] Implement route-based code splitting
- [ ] Create route transition animations
- [ ] Design modular route structure

## Retry Logic

```typescript
const skillConfig = {
  maxAttempts: 3,
  backoffMs: [1000, 2000, 4000],
  onFailure: 'provide_simpler_route'
}
```

## Observability

```yaml
tracking:
  - event: route_configured
    data: [route_count, guards_count]
  - event: navigation_pattern_learned
    data: [pattern_name, complexity]
  - event: skill_completed
    data: [routes_built, auth_implemented]
```

## Troubleshooting

### Common Issues

| Issue | Cause | Solution |
|-------|-------|----------|
| Route not matching | Wrong path order | Specific before generic |
| Guard infinite loop | Guard → same route | Check target route |
| Lazy load fails | Wrong import path | Verify file exists |
| Params undefined | Missing props: true | Enable props |

### Debug Steps

1. Check Vue Devtools router tab
2. Verify route order (specific first)
3. Console.log in guards
4. Check router.getRoutes()

## Unit Test Template

```typescript
import { describe, it, expect, beforeEach } from 'vitest'
import { createRouter, createWebHistory } from 'vue-router'
import { routes } from './routes'

describe('Router', () => {
  let router: Router

  beforeEach(() => {
    router = createRouter({
      history: createWebHistory(),
      routes
    })
  })

  it('redirects to login when not authenticated', async () => {
    await router.push('/dashboard')
    expect(router.currentRoute.value.name).toBe('Login')
  })

  it('allows access to public routes', async () => {
    await router.push('/about')
    expect(router.currentRoute.value.name).toBe('About')
  })
})
```

## Usage

```
Skill("vue-router")
```

## Related Skills

- `vue-fundamentals` - Prerequisite
- `vue-pinia` - Auth state for guards
- `vue-nuxt` - File-based routing alternative

## Resources

- [Vue Router Documentation](https://router.vuejs.org/)
- [Navigation Guards](https://router.vuejs.org/guide/advanced/navigation-guards.html)
- [Lazy Loading](https://router.vuejs.org/guide/advanced/lazy-loading.html)
