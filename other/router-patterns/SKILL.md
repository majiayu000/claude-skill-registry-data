---
name: TanStack Router Patterns
description: >-
  Auto-enforce TanStack Router file-based routing conventions. Activates when
  creating routes, configuring navigation, handling route params, or working
  with search params in React SPA applications.
version: 1.0.0
---

# TanStack Router Patterns

This skill enforces TanStack Router best practices for file-based routing in React SPA applications.

## Route File Naming Conventions

| Pattern | Example | URL Path | Purpose |
|---------|---------|----------|---------|
| `__root.tsx` | `routes/__root.tsx` | - | Root layout, wraps all routes |
| `index.tsx` | `routes/index.tsx` | `/` | Index route |
| `about.tsx` | `routes/about.tsx` | `/about` | Static segment |
| `posts.tsx` | `routes/posts.tsx` | `/posts` | Layout route (has `<Outlet />`) |
| `posts.index.tsx` | `routes/posts.index.tsx` | `/posts` | Posts index (nested in layout) |
| `posts.$postId.tsx` | `routes/posts.$postId.tsx` | `/posts/:postId` | Dynamic parameter |
| `posts_.$postId.edit.tsx` | `routes/posts_.$postId.edit.tsx` | `/posts/:postId/edit` | Pathless parent layout |
| `_auth.tsx` | `routes/_auth.tsx` | - | Pathless layout (no URL segment) |
| `_auth.login.tsx` | `routes/_auth.login.tsx` | `/login` | Child of pathless layout |
| `(marketing)/` | `routes/(marketing)/about.tsx` | `/about` | Route group (organization only) |
| `$.tsx` | `routes/$.tsx` | `/*` | Catch-all/splat route |

## Route File Structure

### Basic Route
```typescript
// routes/about.tsx
import { createFileRoute } from '@tanstack/react-router'

export const Route = createFileRoute('/about')({
  component: AboutPage,
})

function AboutPage() {
  return <div>About Page</div>
}
```

### Route with Loader
```typescript
// routes/posts.$postId.tsx
import { createFileRoute } from '@tanstack/react-router'
import { postQueryOptions } from '@/features/posts/queries'

export const Route = createFileRoute('/posts/$postId')({
  loader: ({ context: { queryClient }, params }) =>
    queryClient.ensureQueryData(postQueryOptions(params.postId)),
  component: PostDetailPage,
})

function PostDetailPage() {
  const { postId } = Route.useParams()
  const post = Route.useLoaderData()

  return <PostDetail post={post} />
}
```

### Route with Search Params
```typescript
// routes/posts.tsx
import { createFileRoute } from '@tanstack/react-router'
import { z } from 'zod'

const postsSearchSchema = z.object({
  page: z.number().default(1),
  sort: z.enum(['newest', 'oldest', 'popular']).default('newest'),
  search: z.string().optional(),
})

export const Route = createFileRoute('/posts')({
  validateSearch: postsSearchSchema,
  component: PostsPage,
})

function PostsPage() {
  const { page, sort, search } = Route.useSearch()
  const navigate = Route.useNavigate()

  const setPage = (newPage: number) => {
    navigate({ search: (prev) => ({ ...prev, page: newPage }) })
  }

  return <PostList page={page} sort={sort} search={search} onPageChange={setPage} />
}
```

### Root Route with Context
```typescript
// routes/__root.tsx
import { createRootRouteWithContext, Outlet } from '@tanstack/react-router'
import type { QueryClient } from '@tanstack/react-query'

interface RouterContext {
  queryClient: QueryClient
}

export const Route = createRootRouteWithContext<RouterContext>()({
  component: RootComponent,
  beforeLoad: async ({ context }) => {
    // Auth check, theme loading, etc.
    return { user: await getUser() }
  },
})

function RootComponent() {
  return (
    <div>
      <Header />
      <Outlet />
      <Footer />
    </div>
  )
}
```

### Pathless Layout Route
```typescript
// routes/_auth.tsx
import { createFileRoute, Outlet, redirect } from '@tanstack/react-router'

export const Route = createFileRoute('/_auth')({
  beforeLoad: async ({ context }) => {
    if (!context.user) {
      throw redirect({ to: '/login' })
    }
  },
  component: AuthLayout,
})

function AuthLayout() {
  return (
    <div className="authenticated-layout">
      <Sidebar />
      <main>
        <Outlet />
      </main>
    </div>
  )
}
```

## Navigation Patterns

### Declarative Navigation
```typescript
import { Link } from '@tanstack/react-router'

// Basic link
<Link to="/about">About</Link>

// With params
<Link to="/posts/$postId" params={{ postId: '123' }}>
  View Post
</Link>

// With search params
<Link to="/posts" search={{ page: 2, sort: 'newest' }}>
  Page 2
</Link>

// Active styling
<Link
  to="/posts"
  activeProps={{ className: 'active' }}
  inactiveProps={{ className: 'inactive' }}
>
  Posts
</Link>
```

### Imperative Navigation
```typescript
import { useNavigate } from '@tanstack/react-router'

function PostCard({ post }) {
  const navigate = useNavigate()

  const handleClick = () => {
    navigate({
      to: '/posts/$postId',
      params: { postId: post.id },
      search: { tab: 'comments' }
    })
  }

  return <div onClick={handleClick}>{post.title}</div>
}
```

### Programmatic Redirect
```typescript
import { redirect } from '@tanstack/react-router'

export const Route = createFileRoute('/admin')({
  beforeLoad: async ({ context }) => {
    if (!context.user?.isAdmin) {
      throw redirect({ to: '/', search: { error: 'unauthorized' } })
    }
  },
})
```

## Error Handling

### Route Error Boundary
```typescript
export const Route = createFileRoute('/posts/$postId')({
  loader: async ({ params }) => {
    const post = await getPost(params.postId)
    if (!post) {
      throw new Error('Post not found')
    }
    return post
  },
  errorComponent: ({ error }) => (
    <div className="error">
      <h2>Error loading post</h2>
      <p>{error.message}</p>
    </div>
  ),
  component: PostPage,
})
```

### Pending Component
```typescript
export const Route = createFileRoute('/posts')({
  pendingComponent: () => <div>Loading posts...</div>,
  pendingMinMs: 500, // Show pending after 500ms
  pendingMs: 1000,   // Minimum pending display time
  component: PostsPage,
})
```

## TanStack Start Fullstack SSR Patterns

TanStack Start extends TanStack Router into a full-stack SSR framework powered by Nitro.

### Server Functions (`createServerFn`)

Define type-safe RPC endpoints callable from loaders, hooks, or actions:

```typescript
// server/posts.ts
import { createServerFn } from '@tanstack/start'
import { z } from 'zod'
import { db } from './db'

export const getPost = createServerFn({ method: 'GET' })
  .validator((d: string) => z.string().parse(d))
  .handler(async ({ data: postId }) => {
    // Executes strictly on the server
    const post = await db.post.findUnique({ where: { id: postId } })
    if (!post) throw new Error('Not found')
    return post
  })

export const createPost = createServerFn({ method: 'POST' })
  .validator((d: { title: string; content: string }) =>
    z.object({ title: z.string().min(1), content: z.string() }).parse(d)
  )
  .handler(async ({ data }) => {
    return await db.post.create({ data })
  })
```

### SSR Loaders with Server Functions

Loaders run on the server during initial SSR and hydrate seamlessly on the client:

```typescript
// routes/posts.$postId.tsx
import { createFileRoute } from '@tanstack/react-router'
import { getPost } from '@/server/posts'

export const Route = createFileRoute('/posts/$postId')({
  loader: async ({ params }) => {
    return await getPost({ data: params.postId })
  },
  component: PostComponent,
})

function PostComponent() {
  const post = Route.useLoaderData()
  return (
    <main>
      <h1>{post.title}</h1>
      <div>{post.content}</div>
    </main>
  )
}
```

### Nitro Universal Deployment Configuration

TanStack Start utilizes Nitro for zero-config deployments to Bun, Node, Cloudflare Workers, or Vercel:

```typescript
// app.config.ts
import { defineConfig } from '@tanstack/start/config'
import tsConfigPaths from 'vite-tsconfig-paths'

export default defineConfig({
  vite: {
    plugins: [tsConfigPaths()],
  },
  server: {
    preset: process.env.NITRO_PRESET || 'node-server', // 'bun', 'cloudflare-pages', 'vercel', etc.
  },
})
```

## Conventions to Enforce

1. **Always use `createFileRoute`** - Never manual route configuration
2. **Type-safe params** - Use `Route.useParams()` for full type inference
3. **Validate search params** - Use Zod schemas with `validateSearch`
4. **Loaders for data** - Prefetch with `ensureQueryData`, not direct fetches
5. **Context for shared data** - Auth, theme, queryClient in root context
6. **Error boundaries** - Always provide `errorComponent` for data routes
7. **Pathless layouts** - Use `_` prefix for auth guards, feature layouts

## Anti-Patterns to Block

```typescript
// ❌ WRONG: Manual route definition
const router = createRouter({
  routes: [{ path: '/posts', component: Posts }]
})

// ✅ CORRECT: File-based routes
// routes/posts.tsx with createFileRoute

// ❌ WRONG: useParams from react-router-dom
import { useParams } from 'react-router-dom'

// ✅ CORRECT: Route-specific useParams
const { postId } = Route.useParams()

// ❌ WRONG: Unvalidated search params
const search = new URLSearchParams(window.location.search)

// ✅ CORRECT: Validated with Zod
const { page, sort } = Route.useSearch()

// ❌ WRONG: Direct fetch in loader
loader: async () => {
  const response = await fetch('/api/posts')
  return response.json()
}

// ✅ CORRECT: Use query client
loader: ({ context: { queryClient } }) =>
  queryClient.ensureQueryData(postsQueryOptions())
```
