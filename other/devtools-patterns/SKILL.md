---
name: TanStack DevTools Patterns
description: >-
  TanStack DevTools patterns for debugging and development. Activates when
  setting up development tools, debugging queries, or configuring developer
  experience in React applications.
version: 1.0.0
---

# TanStack DevTools Patterns

This skill covers TanStack DevTools setup and usage for debugging React applications.

## React Query DevTools

### Installation
```bash
bun add -D @tanstack/react-query-devtools
```

### Basic Setup
```typescript
// main.tsx
import { QueryClientProvider } from '@tanstack/react-query'
import { ReactQueryDevtools } from '@tanstack/react-query-devtools'
import { createQueryClient } from '@/lib/query-client'

const queryClient = createQueryClient()

function App() {
  return (
    <QueryClientProvider client={queryClient}>
      <RouterProvider router={router} />
      <ReactQueryDevtools initialIsOpen={false} />
    </QueryClientProvider>
  )
}
```

### Production Lazy Loading
```typescript
// Only load devtools in development
import { lazy, Suspense } from 'react'

const ReactQueryDevtools = lazy(() =>
  import('@tanstack/react-query-devtools').then((d) => ({
    default: d.ReactQueryDevtools,
  }))
)

function App() {
  return (
    <QueryClientProvider client={queryClient}>
      <RouterProvider router={router} />
      {import.meta.env.DEV && (
        <Suspense fallback={null}>
          <ReactQueryDevtools />
        </Suspense>
      )}
    </QueryClientProvider>
  )
}
```

### DevTools Configuration
```typescript
<ReactQueryDevtools
  initialIsOpen={false}
  position="bottom-right"
  buttonPosition="bottom-right"
  toggleButtonProps={{
    style: {
      marginBottom: '4rem', // Avoid overlapping with other UI
    },
  }}
/>
```

### Embedded DevTools
```typescript
import { ReactQueryDevtoolsPanel } from '@tanstack/react-query-devtools'

function AdminDashboard() {
  const [isOpen, setIsOpen] = useState(false)

  return (
    <div>
      <button onClick={() => setIsOpen(!isOpen)}>
        Toggle Query Inspector
      </button>
      {isOpen && (
        <div className="devtools-panel">
          <ReactQueryDevtoolsPanel />
        </div>
      )}
    </div>
  )
}
```

## Router DevTools

### Installation
```bash
bun add -D @tanstack/router-devtools
```

### Setup
```typescript
// routes/__root.tsx
import { TanStackRouterDevtools } from '@tanstack/router-devtools'

export const Route = createRootRouteWithContext<RouterContext>()({
  component: () => (
    <>
      <Outlet />
      {import.meta.env.DEV && <TanStackRouterDevtools position="bottom-left" />}
    </>
  ),
})
```

### Lazy Loading Router DevTools
```typescript
import { lazy, Suspense } from 'react'

const TanStackRouterDevtools = import.meta.env.DEV
  ? lazy(() =>
      import('@tanstack/router-devtools').then((d) => ({
        default: d.TanStackRouterDevtools,
      }))
    )
  : () => null

export const Route = createRootRouteWithContext<RouterContext>()({
  component: () => (
    <>
      <Outlet />
      <Suspense fallback={null}>
        <TanStackRouterDevtools />
      </Suspense>
    </>
  ),
})
```

## Combined DevTools Layout

```typescript
// routes/__root.tsx
import { lazy, Suspense } from 'react'

const ReactQueryDevtools = lazy(() =>
  import('@tanstack/react-query-devtools').then((d) => ({
    default: d.ReactQueryDevtools,
  }))
)

const TanStackRouterDevtools = lazy(() =>
  import('@tanstack/router-devtools').then((d) => ({
    default: d.TanStackRouterDevtools,
  }))
)

export const Route = createRootRouteWithContext<RouterContext>()({
  component: () => (
    <>
      <Outlet />
      {import.meta.env.DEV && (
        <Suspense fallback={null}>
          <ReactQueryDevtools position="bottom-right" />
          <TanStackRouterDevtools position="bottom-left" />
        </Suspense>
      )}
    </>
  ),
})
```

## Query Logging

### Development Logger
```typescript
// lib/query-client.ts
import { QueryClient } from '@tanstack/react-query'

export function createQueryClient() {
  return new QueryClient({
    defaultOptions: {
      queries: {
        // ... other options
      },
    },
    ...(import.meta.env.DEV && {
      logger: {
        log: console.log,
        warn: console.warn,
        error: console.error,
      },
    }),
  })
}
```

### Custom Query Logger
```typescript
const queryClient = new QueryClient({
  queryCache: new QueryCache({
    onError: (error, query) => {
      if (import.meta.env.DEV) {
        console.error(`Query Error [${query.queryKey}]:`, error)
      }
    },
    onSuccess: (data, query) => {
      if (import.meta.env.DEV) {
        console.log(`Query Success [${query.queryKey}]:`, data)
      }
    },
  }),
  mutationCache: new MutationCache({
    onError: (error, variables, context, mutation) => {
      if (import.meta.env.DEV) {
        console.error(`Mutation Error:`, error, variables)
      }
    },
  }),
})
```

## Performance Monitoring

### Query Timing
```typescript
const queryClient = new QueryClient({
  queryCache: new QueryCache({
    onSuccess: (data, query) => {
      if (import.meta.env.DEV) {
        const timing = query.state.dataUpdatedAt - query.state.fetchFailureCount
        console.log(`[${query.queryKey}] fetched in ${timing}ms`)
      }
    },
  }),
})
```

### React Profiler Integration
```typescript
import { Profiler } from 'react'

function App() {
  const onRender = (
    id: string,
    phase: 'mount' | 'update',
    actualDuration: number
  ) => {
    if (import.meta.env.DEV && actualDuration > 16) {
      console.warn(`Slow render: ${id} (${phase}) - ${actualDuration.toFixed(2)}ms`)
    }
  }

  return (
    <Profiler id="App" onRender={onRender}>
      <QueryClientProvider client={queryClient}>
        <RouterProvider router={router} />
      </QueryClientProvider>
    </Profiler>
  )
}
```

## Debug Utilities

### Query State Inspector Hook
```typescript
import { useQueryClient } from '@tanstack/react-query'

function useQueryInspector() {
  const queryClient = useQueryClient()

  return {
    getQueryState: (queryKey: unknown[]) =>
      queryClient.getQueryState(queryKey),

    getQueriesData: () =>
      queryClient.getQueriesData({ type: 'all' }),

    invalidateAll: () =>
      queryClient.invalidateQueries(),

    clearAll: () =>
      queryClient.clear(),
  }
}

// Usage in development
function DevPanel() {
  const inspector = useQueryInspector()

  return (
    <div>
      <button onClick={() => console.log(inspector.getQueriesData())}>
        Log All Queries
      </button>
      <button onClick={inspector.invalidateAll}>
        Invalidate All
      </button>
      <button onClick={inspector.clearAll}>
        Clear Cache
      </button>
    </div>
  )
}
```

### Route State Inspector
```typescript
import { useRouter, useMatches } from '@tanstack/react-router'

function RouteInspector() {
  const router = useRouter()
  const matches = useMatches()

  if (!import.meta.env.DEV) return null

  return (
    <div className="fixed bottom-20 left-4 bg-black/90 text-white p-4 rounded text-xs">
      <pre>
        {JSON.stringify(
          {
            pathname: router.state.location.pathname,
            search: router.state.location.search,
            matches: matches.map((m) => m.routeId),
          },
          null,
          2
        )}
      </pre>
    </div>
  )
}
```

## Vite Configuration

```typescript
// vite.config.ts
import { defineConfig } from 'vite'

export default defineConfig({
  define: {
    // Strip devtools from production
    'process.env.NODE_ENV': JSON.stringify(process.env.NODE_ENV),
  },
  build: {
    rollupOptions: {
      // Exclude devtools from production bundle
      external: import.meta.env.PROD
        ? ['@tanstack/react-query-devtools', '@tanstack/router-devtools']
        : [],
    },
  },
})
```

## Conventions

1. **Lazy load devtools** - Always lazy load to reduce bundle size
2. **Environment check** - Only render in development
3. **Position wisely** - Avoid overlapping with app UI
4. **Production strip** - Ensure devtools are excluded from prod
5. **Custom logging** - Add meaningful logging in development

## Anti-Patterns

```typescript
// ❌ WRONG: DevTools in production bundle
import { ReactQueryDevtools } from '@tanstack/react-query-devtools'

function App() {
  return (
    <>
      <Main />
      <ReactQueryDevtools /> {/* Always included! */}
    </>
  )
}

// ✅ CORRECT: Conditional and lazy loaded
const ReactQueryDevtools = lazy(() =>
  import('@tanstack/react-query-devtools').then((d) => ({
    default: d.ReactQueryDevtools,
  }))
)

function App() {
  return (
    <>
      <Main />
      {import.meta.env.DEV && (
        <Suspense fallback={null}>
          <ReactQueryDevtools />
        </Suspense>
      )}
    </>
  )
}

// ❌ WRONG: No position configuration (overlapping)
<ReactQueryDevtools />
<TanStackRouterDevtools />

// ✅ CORRECT: Different positions
<ReactQueryDevtools position="bottom-right" />
<TanStackRouterDevtools position="bottom-left" />
```
