---
name: grey-haven-tanstack-patterns
description: "Apply Grey Haven's TanStack ecosystem patterns - Router file-based routing, Query data fetching with staleTime, and Start server functions. Use when building React applications with TanStack Start. Triggers: 'TanStack', 'TanStack Start', 'TanStack Query', 'TanStack Router', 'React Query', 'file-based routing', 'server functions'."
# v2.0.43: Skills to auto-load for TanStack development
skills:
  - grey-haven-code-style
  - grey-haven-react-tanstack-testing
  - grey-haven-api-design-standards
# v2.0.74: Restrict tools for development work
allowed-tools:
  - Read
  - Write
  - MultiEdit
  - Bash
  - Grep
  - Glob
  - TodoWrite
  - WebFetch
  - mcp__context7__*
---

# Grey Haven TanStack Patterns

Follow Grey Haven Studio's patterns for TanStack Start, Router, and Query in React 19 applications.

## TanStack Stack Overview

Grey Haven uses the complete TanStack ecosystem:
- **TanStack Start**: Full-stack React framework with server functions
- **TanStack Router**: Type-safe file-based routing with loaders
- **TanStack Query**: Server state management with caching
- **TanStack Table** (optional): Data grids and tables
- **TanStack Form** (optional): Type-safe form handling

## Critical Patterns

### 1. File-Based Routing Structure

```
src/routes/
├── __root.tsx              # Root layout (wraps all routes)
├── index.tsx               # Homepage (/)
├── _authenticated/         # Protected routes group (underscore prefix)
│   ├── _layout.tsx        # Auth layout wrapper
│   ├── dashboard.tsx      # /dashboard
│   └── settings/
│       └── index.tsx      # /settings
└── users/
    ├── index.tsx          # /users
    └── $userId.tsx        # /users/:userId (dynamic param)
```

**Key conventions**:
- `__root.tsx` - Root layout with QueryClient provider
- `_authenticated/` - Protected route groups (underscore prefix)
- `_layout.tsx` - Layout wrapper for route groups
- `$param.tsx` - Dynamic route parameters

### 2. TanStack Query Defaults

```typescript
const queryClient = new QueryClient({
  defaultOptions: {
    queries: {
      staleTime: 60000, // 1 minute default
      retry: 1,
      refetchOnWindowFocus: false,
    },
  },
});
```

### 3. Query Key Patterns

```typescript
// ✅ CORRECT - Specific to general
queryKey: ["user", userId]
queryKey: ["users", { tenantId, page: 1 }]
queryKey: ["organizations", orgId, "teams"]

// ❌ WRONG
queryKey: [userId]                    // Missing resource type
queryKey: ["getUser", userId]        // Don't include function name
queryKey: [{ id: userId }]           // Object first is confusing
```

### 4. Server Functions with Multi-Tenant

```typescript
// ALWAYS include tenant_id parameter
export const getUserById = createServerFn("GET", async (
  userId: string,
  tenantId: string
) => {
  const user = await db.query.users.findFirst({
    where: and(
      eq(users.id, userId),
      eq(users.tenant_id, tenantId) // Multi-tenant isolation!
    ),
  });

  if (!user) throw new Error("User not found");
  return user;
});
```

### 5. Route Loaders

```typescript
export const Route = createFileRoute("/_authenticated/dashboard")({
  // Loader fetches data on server before rendering
  loader: async ({ context }) => {
    const tenantId = context.session.tenantId;
    return await getDashboardData(tenantId);
  },
  component: DashboardPage,
});

function DashboardPage() {
  const data = Route.useLoaderData(); // Type-safe loader data
  return <div>...</div>;
}
```

### 6. Mutations with Cache Invalidation

```typescript
const mutation = useMutation({
  mutationFn: (data: UserUpdate) => updateUser(userId, data),
  // Always invalidate queries after mutation
  onSuccess: () => {
    queryClient.invalidateQueries({ queryKey: ["user", userId] });
  },
});
```

## Caching Strategy

Grey Haven uses these staleTime defaults:

| Data Type | staleTime | Use Case |
|-----------|-----------|----------|
| Auth data | 5 minutes | User sessions, tokens |
| User profiles | 1 minute | User details |
| Lists | 1 minute | Data tables, lists |
| Static/config | 10 minutes | Settings, configs |
| Realtime | 0 (always refetch) | Notifications |

```typescript
const STALE_TIMES = {
  auth: 5 * 60 * 1000,        // 5 minutes
  user: 1 * 60 * 1000,        // 1 minute
  list: 1 * 60 * 1000,        // 1 minute
  static: 10 * 60 * 1000,     // 10 minutes
  realtime: 0,                // Always refetch
};
```

## Supporting Documentation

All supporting files are under 500 lines per Anthropic best practices:

- **[examples/](examples/)** - Complete code examples
  - [router-patterns.md](examples/router-patterns.md) - File-based routing, layouts, navigation
  - [query-patterns.md](examples/query-patterns.md) - Queries, mutations, infinite queries
  - [server-functions.md](examples/server-functions.md) - Creating and using server functions
  - [advanced-patterns.md](examples/advanced-patterns.md) - Dependent queries, parallel queries, custom hooks
  - [INDEX.md](examples/INDEX.md) - Examples navigation

- **[reference/](reference/)** - Configuration references
  - [router-config.md](reference/router-config.md) - Router setup and configuration
  - [query-config.md](reference/query-config.md) - QueryClient configuration
  - [caching-strategy.md](reference/caching-strategy.md) - Detailed caching patterns
  - [multi-tenant.md](reference/multi-tenant.md) - Multi-tenant patterns with RLS
  - [INDEX.md](reference/INDEX.md) - Reference navigation

- **[templates/](templates/)** - Copy-paste ready templates
  - [root-route.tsx](templates/root-route.tsx) - Root layout template
  - [auth-layout.tsx](templates/auth-layout.tsx) - Protected layout template
  - [page-route.tsx](templates/page-route.tsx) - Basic page route template
  - [server-function.ts](templates/server-function.ts) - Server function template
  - [custom-hook.ts](templates/custom-hook.ts) - Custom query hook template

- **[checklists/](checklists/)** - Pre-PR validation
  - [tanstack-checklist.md](checklists/tanstack-checklist.md) - TanStack patterns checklist

## When to Apply This Skill

Use this skill when:
- Building TanStack Start applications
- Implementing routing with TanStack Router
- Managing server state with TanStack Query
- Creating server functions for data fetching
- Optimizing query performance with caching
- Implementing multi-tenant data access
- Setting up authentication flows with route protection
- Building data-heavy React applications

## Template Reference

These patterns are from Grey Haven's production template:
- **cvi-template**: TanStack Start + Router + Query + React 19

## Critical Reminders

1. **staleTime**: Default 60000ms (1 minute) for queries
2. **Query keys**: Specific to general (["user", userId], not [userId])
3. **Server functions**: Always include tenant_id parameter
4. **Multi-tenant**: Filter by tenant_id in all server functions
5. **Loaders**: Use for server-side data fetching before render
6. **Mutations**: Invalidate queries after successful mutation
7. **Prefetching**: Use for performance on hover/navigation
8. **Error handling**: Always handle error state in queries
9. **RLS**: Server functions use RLS-enabled database connection
10. **File-based routing**: Underscore prefix (_) for route groups/layouts
