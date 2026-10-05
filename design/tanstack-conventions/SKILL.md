---
name: TanStack Conventions
description: >-
  Auto-enforce cross-cutting TanStack conventions and import patterns. Activates
  on all TanStack development to ensure consistent project structure, imports,
  and integration patterns across Router, Query, Form, Table, and Virtual.
version: 1.0.0
---

# TanStack Conventions

This skill enforces cross-cutting conventions across all TanStack libraries for consistent, maintainable React SPA development.

## Project Structure

### Feature-Based Organization
```
src/
├── features/
│   ├── posts/
│   │   ├── components/
│   │   │   ├── PostList.tsx
│   │   │   ├── PostCard.tsx
│   │   │   ├── PostForm.tsx
│   │   │   └── index.ts          # Barrel export
│   │   ├── hooks/
│   │   │   ├── useCreatePost.ts
│   │   │   ├── useUpdatePost.ts
│   │   │   ├── useDeletePost.ts
│   │   │   └── index.ts
│   │   ├── queries/
│   │   │   ├── postQueries.ts    # Query options factories
│   │   │   └── index.ts
│   │   ├── api/
│   │   │   └── postApi.ts        # API client functions
│   │   ├── types.ts              # Feature-specific types
│   │   └── index.ts              # Feature barrel export
│   └── users/
│       └── ...
├── routes/
│   ├── __root.tsx
│   ├── index.tsx
│   ├── posts.tsx
│   ├── posts.index.tsx
│   └── posts.$postId.tsx
├── lib/
│   ├── query-client.ts           # Query client setup
│   ├── query-keys.ts             # Query key factory
│   └── router.ts                 # Router setup
├── components/
│   └── ui/                       # Shared UI components
├── hooks/                        # Shared hooks
├── types/                        # Global types
└── main.tsx
```

## Import Conventions

### Always Use Path Aliases
```typescript
// ✅ CORRECT: Path aliases
import { PostList } from '@/features/posts/components'
import { useCreatePost } from '@/features/posts/hooks'
import { postQueryOptions } from '@/features/posts/queries'
import { queryKeys } from '@/lib/query-keys'
import { Button } from '@/components/ui'

// ❌ WRONG: Relative imports across features
import { User } from '../../users/types'
import { queryClient } from '../../../lib/query-client'

// ❌ WRONG: Deep imports bypassing barrels
import { PostCard } from '@/features/posts/components/PostCard'
```

### Barrel Export Pattern
```typescript
// features/posts/components/index.ts
export { PostList } from './PostList'
export { PostCard } from './PostCard'
export { PostForm } from './PostForm'

// features/posts/index.ts
export * from './components'
export * from './hooks'
export * from './queries'
export * from './types'
```

### Import Order
```typescript
// 1. React and external libraries
import { useState, useRef } from 'react'
import { useQuery, useMutation } from '@tanstack/react-query'
import { Link, useNavigate } from '@tanstack/react-router'

// 2. Internal aliases (@/)
import { PostCard } from '@/features/posts/components'
import { queryKeys } from '@/lib/query-keys'
import { Button } from '@/components/ui'

// 3. Relative imports (same feature only)
import { postSchema } from './schemas'
import type { PostFormData } from './types'
```

## TypeScript Configuration

### tsconfig.json Path Aliases
```json
{
  "compilerOptions": {
    "strict": true,
    "noUncheckedIndexedAccess": true,
    "baseUrl": ".",
    "paths": {
      "@/*": ["./src/*"]
    }
  }
}
```

### Vite Configuration
```typescript
// vite.config.ts
import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'
import { TanStackRouterVite } from '@tanstack/router-plugin/vite'
import tsconfigPaths from 'vite-tsconfig-paths'

export default defineConfig({
  plugins: [
    TanStackRouterVite(),
    react(),
    tsconfigPaths(),
  ],
})
```

## App Setup

### Main Entry Point
```typescript
// main.tsx
import { StrictMode } from 'react'
import { createRoot } from 'react-dom/client'
import { QueryClientProvider } from '@tanstack/react-query'
import { ReactQueryDevtools } from '@tanstack/react-query-devtools'
import { RouterProvider } from '@tanstack/react-router'
import { createQueryClient } from '@/lib/query-client'
import { router } from '@/lib/router'

const queryClient = createQueryClient()

createRoot(document.getElementById('root')!).render(
  <StrictMode>
    <QueryClientProvider client={queryClient}>
      <RouterProvider router={router} context={{ queryClient }} />
      <ReactQueryDevtools />
    </QueryClientProvider>
  </StrictMode>
)
```

### Router Setup
```typescript
// lib/router.ts
import { createRouter } from '@tanstack/react-router'
import { routeTree } from '@/routeTree.gen'
import type { QueryClient } from '@tanstack/react-query'

export interface RouterContext {
  queryClient: QueryClient
}

export const router = createRouter({
  routeTree,
  context: {
    queryClient: undefined!, // Set in main.tsx
  },
  defaultPreload: 'intent',
  defaultPreloadStaleTime: 0,
})

declare module '@tanstack/react-router' {
  interface Register {
    router: typeof router
  }
}
```

### Query Client Setup
```typescript
// lib/query-client.ts
import { QueryClient } from '@tanstack/react-query'

export function createQueryClient() {
  return new QueryClient({
    defaultOptions: {
      queries: {
        staleTime: 60 * 1000,
        gcTime: 5 * 60 * 1000,
        retry: 1,
        refetchOnWindowFocus: false,
      },
      mutations: {
        retry: 0,
      },
    },
  })
}
```

## Error Handling

### API Error Type
```typescript
// types/api.ts
export interface ApiError {
  message: string
  code: string
  status: number
  details?: Record<string, string[]>
}

export function isApiError(error: unknown): error is ApiError {
  return (
    typeof error === 'object' &&
    error !== null &&
    'message' in error &&
    'status' in error
  )
}
```

### Query Error Handler
```typescript
// lib/query-client.ts
import { QueryClient } from '@tanstack/react-query'
import { toast } from '@/components/ui/toast'

export function createQueryClient() {
  return new QueryClient({
    defaultOptions: {
      queries: {
        retry: (failureCount, error) => {
          if (isApiError(error) && error.status === 404) return false
          return failureCount < 2
        },
      },
      mutations: {
        onError: (error) => {
          if (isApiError(error)) {
            toast.error(error.message)
          }
        },
      },
    },
  })
}
```

### Route Error Boundaries
```typescript
// routes/__root.tsx
export const Route = createRootRouteWithContext<RouterContext>()({
  component: RootComponent,
  errorComponent: ({ error }) => (
    <div className="error-page">
      <h1>Something went wrong</h1>
      <p>{error.message}</p>
      <Link to="/">Go home</Link>
    </div>
  ),
  notFoundComponent: () => (
    <div className="not-found-page">
      <h1>404 - Page not found</h1>
      <Link to="/">Go home</Link>
    </div>
  ),
})
```

## Loading States

### Route Pending
```typescript
export const Route = createFileRoute('/posts/$postId')({
  loader: ({ context: { queryClient }, params }) =>
    queryClient.ensureQueryData(postQueryOptions(params.postId)),
  pendingComponent: () => <PostDetailSkeleton />,
  pendingMinMs: 200,
  component: PostDetailPage,
})
```

### Query Loading
```typescript
function PostList() {
  const { data, isLoading, error } = useQuery(postsQueryOptions())

  if (isLoading) return <PostListSkeleton />
  if (error) return <ErrorMessage error={error} />

  return (
    <ul>
      {data.map((post) => (
        <PostCard key={post.id} post={post} />
      ))}
    </ul>
  )
}
```

## API Client Pattern

```typescript
// features/posts/api/postApi.ts
import { apiClient } from '@/lib/api-client'
import type { Post, CreatePostInput, UpdatePostInput } from '../types'

export const postApi = {
  getPosts: async (filters?: PostFilters): Promise<Post[]> => {
    const response = await apiClient.get('/posts', { params: filters })
    return response.data
  },

  getPost: async (id: string): Promise<Post> => {
    const response = await apiClient.get(`/posts/${id}`)
    return response.data
  },

  createPost: async (input: CreatePostInput): Promise<Post> => {
    const response = await apiClient.post('/posts', input)
    return response.data
  },

  updatePost: async ({ id, ...input }: UpdatePostInput): Promise<Post> => {
    const response = await apiClient.patch(`/posts/${id}`, input)
    return response.data
  },

  deletePost: async (id: string): Promise<void> => {
    await apiClient.delete(`/posts/${id}`)
  },
}
```

## Type Definitions

```typescript
// features/posts/types.ts
export interface Post {
  id: string
  title: string
  content: string
  authorId: string
  published: boolean
  createdAt: string
  updatedAt: string
}

export interface CreatePostInput {
  title: string
  content: string
  published?: boolean
}

export interface UpdatePostInput extends Partial<CreatePostInput> {
  id: string
}

export interface PostFilters {
  page?: number
  pageSize?: number
  search?: string
  authorId?: string
  published?: boolean
}
```

## Bun Commands

```bash
# Install dependencies
bun install

# Add TanStack packages
bun add @tanstack/react-router @tanstack/react-query @tanstack/react-form @tanstack/react-table @tanstack/react-virtual
bun add -D @tanstack/router-plugin @tanstack/react-query-devtools

# Dev server
bun run dev

# Build
bun run build

# Type check
bun run typecheck

# Generate routes
bun run routes:generate
```

## Package Scripts

```json
{
  "scripts": {
    "dev": "vite",
    "build": "tsc -b && vite build",
    "preview": "vite preview",
    "typecheck": "tsc --noEmit",
    "routes:generate": "tsr generate"
  }
}
```

## Conventions Summary

1. **Feature-based structure** - Group by feature, not by type
2. **Path aliases** - Always use `@/` for imports
3. **Barrel exports** - Export through index.ts files
4. **Query key factory** - Centralized in `lib/query-keys.ts`
5. **Type safety** - Strict TypeScript, no `any`
6. **Error boundaries** - Route and component level
7. **Loading states** - Skeletons, not spinners
8. **Bun runtime** - Use bun for all commands
