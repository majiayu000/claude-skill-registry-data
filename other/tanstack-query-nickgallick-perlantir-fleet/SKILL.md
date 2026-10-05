---
name: tanstack-query
description: TanStack Query (React Query) — data fetching, caching, mutations, optimistic updates, infinite queries.
---

# TanStack Query (React Query) Reference

> Local repo: `repos/tanstack-query`
> Packages: `repos/tanstack-query/packages/react-query/src/`
> Docs: `repos/tanstack-query/docs/`

---

## 1. Setup

```bash
npm install @tanstack/react-query
```

### QueryClientProvider

```typescript
// app/providers.tsx
'use client'
import { QueryClient, QueryClientProvider } from '@tanstack/react-query'
import { ReactQueryDevtools } from '@tanstack/react-query-devtools'
import { useState } from 'react'

export function Providers({ children }: { children: React.ReactNode }) {
  const [queryClient] = useState(
    () =>
      new QueryClient({
        defaultOptions: {
          queries: {
            staleTime: 60 * 1000,       // 1 minute before data is "stale"
            gcTime: 5 * 60 * 1000,      // 5 minutes before unused cache is garbage collected
            retry: 1,                    // retry failed queries once
            refetchOnWindowFocus: false, // disable refetch on tab focus (optional)
          },
        },
      })
  )

  return (
    <QueryClientProvider client={queryClient}>
      {children}
      <ReactQueryDevtools initialIsOpen={false} />
    </QueryClientProvider>
  )
}
```

```typescript
// app/layout.tsx
import { Providers } from './providers'

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html>
      <body>
        <Providers>{children}</Providers>
      </body>
    </html>
  )
}
```

---

## 2. useQuery

### Basic Usage

```typescript
import { useQuery } from '@tanstack/react-query'
import { createClient } from '@/lib/supabase/client'

function PostsList() {
  const supabase = createClient()

  const { data, isLoading, isError, error, isFetching } = useQuery({
    queryKey: ['posts'],
    queryFn: async () => {
      const { data, error } = await supabase
        .from('posts')
        .select('*')
        .order('created_at', { ascending: false })

      if (error) throw error
      return data
    },
  })

  if (isLoading) return <div>Loading...</div>
  if (isError) return <div>Error: {error.message}</div>

  return (
    <ul>
      {data.map((post) => (
        <li key={post.id}>{post.title}</li>
      ))}
    </ul>
  )
}
```

### Query Key Conventions

```typescript
// Simple list
queryKey: ['posts']

// Filtered list
queryKey: ['posts', { status: 'published', author: userId }]

// Single item
queryKey: ['posts', postId]

// Nested resource
queryKey: ['posts', postId, 'comments']

// With pagination
queryKey: ['posts', { page: 1, limit: 20 }]
```

Query keys are hierarchical — invalidating `['posts']` also invalidates
`['posts', postId]` and `['posts', { status: 'published' }]`.

### Advanced Options

```typescript
const { data } = useQuery({
  queryKey: ['posts', postId],
  queryFn: () => fetchPost(postId),

  // Only run when postId is truthy
  enabled: !!postId,

  // Transform data before caching
  select: (data) => data.filter((post) => post.is_published),

  // Show while loading (doesn't affect isLoading state like initialData does)
  placeholderData: previousData, // or keepPreviousData for pagination

  // Data is fresh for 5 minutes
  staleTime: 5 * 60 * 1000,

  // Refetch every 30 seconds
  refetchInterval: 30 * 1000,

  // Stop refetching when tab is not visible
  refetchIntervalInBackground: false,
})
```

---

## 3. useMutation

### Basic Mutation

```typescript
import { useMutation, useQueryClient } from '@tanstack/react-query'

function CreatePostForm() {
  const supabase = createClient()
  const queryClient = useQueryClient()

  const createPost = useMutation({
    mutationFn: async (newPost: { title: string; content: string }) => {
      const { data, error } = await supabase
        .from('posts')
        .insert(newPost)
        .select()
        .single()

      if (error) throw error
      return data
    },

    onSuccess: (data) => {
      // Invalidate and refetch posts list
      queryClient.invalidateQueries({ queryKey: ['posts'] })

      // Or add the new post directly to cache
      // queryClient.setQueryData(['posts', data.id], data)
    },

    onError: (error) => {
      console.error('Failed to create post:', error)
      toast.error('Failed to create post')
    },

    onSettled: () => {
      // Runs after success OR error — good for cleanup
    },
  })

  return (
    <form
      onSubmit={(e) => {
        e.preventDefault()
        const formData = new FormData(e.currentTarget)
        createPost.mutate({
          title: formData.get('title') as string,
          content: formData.get('content') as string,
        })
      }}
    >
      <input name="title" required />
      <textarea name="content" required />
      <button type="submit" disabled={createPost.isPending}>
        {createPost.isPending ? 'Creating...' : 'Create Post'}
      </button>
    </form>
  )
}
```

### Delete Mutation

```typescript
const deletePost = useMutation({
  mutationFn: async (postId: string) => {
    const { error } = await supabase
      .from('posts')
      .delete()
      .eq('id', postId)

    if (error) throw error
  },
  onSuccess: () => {
    queryClient.invalidateQueries({ queryKey: ['posts'] })
  },
})

// Usage: deletePost.mutate(postId)
```

---

## 4. Optimistic Updates

```typescript
const updatePost = useMutation({
  mutationFn: async ({ id, title }: { id: string; title: string }) => {
    const { data, error } = await supabase
      .from('posts')
      .update({ title })
      .eq('id', id)
      .select()
      .single()

    if (error) throw error
    return data
  },

  onMutate: async (newData) => {
    // Cancel outgoing refetches so they don't overwrite our optimistic update
    await queryClient.cancelQueries({ queryKey: ['posts', newData.id] })

    // Snapshot previous value
    const previousPost = queryClient.getQueryData(['posts', newData.id])

    // Optimistically update cache
    queryClient.setQueryData(['posts', newData.id], (old: Post) => ({
      ...old,
      title: newData.title,
    }))

    // Return context with snapshot for rollback
    return { previousPost }
  },

  onError: (err, newData, context) => {
    // Rollback on error
    queryClient.setQueryData(
      ['posts', newData.id],
      context?.previousPost
    )
    toast.error('Failed to update post')
  },

  onSettled: (data, error, variables) => {
    // Always refetch to ensure server state
    queryClient.invalidateQueries({ queryKey: ['posts', variables.id] })
  },
})
```

### Optimistic Update on List

```typescript
onMutate: async (newPost) => {
  await queryClient.cancelQueries({ queryKey: ['posts'] })

  const previousPosts = queryClient.getQueryData<Post[]>(['posts'])

  queryClient.setQueryData<Post[]>(['posts'], (old) => {
    if (!old) return [newPost]
    return [{ ...newPost, id: 'temp-id' }, ...old]
  })

  return { previousPosts }
},

onError: (err, newPost, context) => {
  queryClient.setQueryData(['posts'], context?.previousPosts)
},
```

---

## 5. Infinite Queries (Pagination)

### Cursor-Based Pagination

```typescript
import { useInfiniteQuery } from '@tanstack/react-query'

function InfinitePostsList() {
  const supabase = createClient()

  const {
    data,
    fetchNextPage,
    hasNextPage,
    isFetchingNextPage,
    isLoading,
  } = useInfiniteQuery({
    queryKey: ['posts', 'infinite'],
    queryFn: async ({ pageParam }) => {
      const limit = 20
      let query = supabase
        .from('posts')
        .select('*')
        .order('created_at', { ascending: false })
        .limit(limit)

      if (pageParam) {
        query = query.lt('created_at', pageParam)
      }

      const { data, error } = await query
      if (error) throw error
      return data
    },
    initialPageParam: null as string | null,
    getNextPageParam: (lastPage) => {
      if (lastPage.length < 20) return undefined // no more pages
      return lastPage[lastPage.length - 1].created_at
    },
  })

  const allPosts = data?.pages.flatMap((page) => page) ?? []

  return (
    <div>
      {allPosts.map((post) => (
        <PostCard key={post.id} post={post} />
      ))}

      {hasNextPage && (
        <button
          onClick={() => fetchNextPage()}
          disabled={isFetchingNextPage}
        >
          {isFetchingNextPage ? 'Loading more...' : 'Load More'}
        </button>
      )}
    </div>
  )
}
```

### Offset-Based Pagination

```typescript
const { data, fetchNextPage, hasNextPage } = useInfiniteQuery({
  queryKey: ['posts', 'paginated'],
  queryFn: async ({ pageParam }) => {
    const limit = 20
    const offset = pageParam * limit

    const { data, error, count } = await supabase
      .from('posts')
      .select('*', { count: 'exact' })
      .order('created_at', { ascending: false })
      .range(offset, offset + limit - 1)

    if (error) throw error
    return { data, count }
  },
  initialPageParam: 0,
  getNextPageParam: (lastPage, allPages) => {
    const totalFetched = allPages.length * 20
    if (totalFetched >= (lastPage.count ?? 0)) return undefined
    return allPages.length
  },
})
```

---

## 6. Prefetching & SSR

### Prefetch in Server Components (Next.js App Router)

```typescript
// app/posts/page.tsx (Server Component)
import {
  dehydrate,
  HydrationBoundary,
  QueryClient,
} from '@tanstack/react-query'
import { createClient } from '@/lib/supabase/server'
import { PostsList } from './posts-list'

export default async function PostsPage() {
  const queryClient = new QueryClient()
  const supabase = await createClient()

  await queryClient.prefetchQuery({
    queryKey: ['posts'],
    queryFn: async () => {
      const { data, error } = await supabase
        .from('posts')
        .select('*')
        .order('created_at', { ascending: false })

      if (error) throw error
      return data
    },
  })

  return (
    <HydrationBoundary state={dehydrate(queryClient)}>
      <PostsList />
    </HydrationBoundary>
  )
}
```

```typescript
// app/posts/posts-list.tsx (Client Component)
'use client'
import { useQuery } from '@tanstack/react-query'

export function PostsList() {
  // This will use the prefetched data — no loading state on first render
  const { data } = useQuery({
    queryKey: ['posts'],
    queryFn: fetchPosts,
  })

  return <ul>{data?.map((p) => <li key={p.id}>{p.title}</li>)}</ul>
}
```

### Prefetch on Hover

```typescript
function PostLink({ postId }: { postId: string }) {
  const queryClient = useQueryClient()

  return (
    <Link
      href={`/posts/${postId}`}
      onMouseEnter={() => {
        queryClient.prefetchQuery({
          queryKey: ['posts', postId],
          queryFn: () => fetchPost(postId),
          staleTime: 60 * 1000,
        })
      }}
    >
      View Post
    </Link>
  )
}
```

---

## 7. Supabase Integration Patterns

### Realtime Invalidation

```typescript
'use client'
import { useEffect } from 'react'
import { useQueryClient } from '@tanstack/react-query'
import { createClient } from '@/lib/supabase/client'

export function RealtimeInvalidator({ table }: { table: string }) {
  const queryClient = useQueryClient()
  const supabase = createClient()

  useEffect(() => {
    const channel = supabase
      .channel(`${table}-changes`)
      .on(
        'postgres_changes',
        { event: '*', schema: 'public', table },
        () => {
          queryClient.invalidateQueries({ queryKey: [table] })
        }
      )
      .subscribe()

    return () => {
      supabase.removeChannel(channel)
    }
  }, [table, supabase, queryClient])

  return null
}

// Usage in layout:
// <RealtimeInvalidator table="posts" />
```

### Typed Query Function Factory

```typescript
// lib/queries.ts
import { createClient } from '@/lib/supabase/client'
import type { Database } from '@/types/database.types'

type Tables = Database['public']['Tables']

export function createQueryFn<T extends keyof Tables>(table: T) {
  return async () => {
    const supabase = createClient()
    const { data, error } = await supabase.from(table).select('*')
    if (error) throw error
    return data
  }
}

// Usage:
// useQuery({ queryKey: ['posts'], queryFn: createQueryFn('posts') })
```

---

## 8. Common Patterns & Tips

### Query Invalidation After Related Mutations

```typescript
// When creating a comment, invalidate both comments and the parent post
onSuccess: () => {
  queryClient.invalidateQueries({ queryKey: ['posts', postId, 'comments'] })
  queryClient.invalidateQueries({ queryKey: ['posts', postId] }) // comment count changed
}
```

### Dependent Queries

```typescript
// Fetch user first, then their posts
const { data: user } = useQuery({
  queryKey: ['user'],
  queryFn: fetchUser,
})

const { data: posts } = useQuery({
  queryKey: ['posts', { userId: user?.id }],
  queryFn: () => fetchUserPosts(user!.id),
  enabled: !!user?.id, // only runs when user is loaded
})
```

### Global Error Handler

```typescript
const queryClient = new QueryClient({
  defaultOptions: {
    queries: {
      retry: (failureCount, error) => {
        // Don't retry on 401/403
        if (error instanceof Error && error.message.includes('401')) return false
        return failureCount < 2
      },
    },
    mutations: {
      onError: (error) => {
        toast.error(error.message)
      },
    },
  },
})
```
