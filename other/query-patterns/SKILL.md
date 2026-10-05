---
name: TanStack Query Patterns
description: >-
  Auto-enforce TanStack Query best practices with factory key pattern. Activates
  when creating queries, mutations, managing server state, or implementing data
  fetching in React applications.
version: 1.0.0
---

# TanStack Query Patterns

This skill enforces TanStack Query best practices for server state management in React applications.

## Query Key Factory Pattern

The factory pattern provides type-safe, hierarchical query keys:

```typescript
// lib/query-keys.ts
export const queryKeys = {
  posts: {
    all: () => ['posts'] as const,
    lists: () => [...queryKeys.posts.all(), 'list'] as const,
    list: (filters: PostFilters) => [...queryKeys.posts.lists(), filters] as const,
    details: () => [...queryKeys.posts.all(), 'detail'] as const,
    detail: (id: string) => [...queryKeys.posts.details(), id] as const,
    comments: (id: string) => [...queryKeys.posts.detail(id), 'comments'] as const,
  },
  users: {
    all: () => ['users'] as const,
    detail: (id: string) => [...queryKeys.users.all(), id] as const,
    profile: () => [...queryKeys.users.all(), 'profile'] as const,
  },
  auth: {
    session: () => ['auth', 'session'] as const,
  },
} as const
```

## Query Options Factory

Define reusable query options for consistency:

```typescript
// features/posts/queries/postQueries.ts
import { queryOptions } from '@tanstack/react-query'
import { queryKeys } from '@/lib/query-keys'
import { postApi } from '@/features/posts/api'

export const postQueryOptions = (postId: string) =>
  queryOptions({
    queryKey: queryKeys.posts.detail(postId),
    queryFn: () => postApi.getPost(postId),
    staleTime: 5 * 60 * 1000, // 5 minutes
  })

export const postsQueryOptions = (filters: PostFilters = {}) =>
  queryOptions({
    queryKey: queryKeys.posts.list(filters),
    queryFn: () => postApi.getPosts(filters),
    staleTime: 1 * 60 * 1000, // 1 minute
  })

export const postCommentsQueryOptions = (postId: string) =>
  queryOptions({
    queryKey: queryKeys.posts.comments(postId),
    queryFn: () => postApi.getPostComments(postId),
    enabled: Boolean(postId),
  })
```

## Query Client Setup

```typescript
// lib/query-client.ts
import { QueryClient } from '@tanstack/react-query'

export function createQueryClient() {
  return new QueryClient({
    defaultOptions: {
      queries: {
        staleTime: 60 * 1000, // 1 minute
        gcTime: 5 * 60 * 1000, // 5 minutes (formerly cacheTime)
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

## Using Queries in Components

### With useSuspenseQuery (Recommended with Router)
```typescript
import { useSuspenseQuery } from '@tanstack/react-query'
import { postQueryOptions } from '@/features/posts/queries'

function PostDetail({ postId }: { postId: string }) {
  // Data guaranteed by route loader, suspense handles loading
  const { data: post } = useSuspenseQuery(postQueryOptions(postId))

  return <article>{post.title}</article>
}
```

### With useQuery (Manual Loading States)
```typescript
import { useQuery } from '@tanstack/react-query'
import { postsQueryOptions } from '@/features/posts/queries'

function PostList({ filters }: { filters: PostFilters }) {
  const { data, isLoading, error } = useQuery(postsQueryOptions(filters))

  if (isLoading) return <Skeleton />
  if (error) return <Error error={error} />

  return (
    <ul>
      {data.map(post => (
        <PostCard key={post.id} post={post} />
      ))}
    </ul>
  )
}
```

## Mutations

### Basic Mutation Hook
```typescript
// features/posts/hooks/useCreatePost.ts
import { useMutation, useQueryClient } from '@tanstack/react-query'
import { queryKeys } from '@/lib/query-keys'
import { postApi } from '@/features/posts/api'

export function useCreatePost() {
  const queryClient = useQueryClient()

  return useMutation({
    mutationFn: postApi.createPost,
    onSuccess: () => {
      // Invalidate all post lists
      queryClient.invalidateQueries({ queryKey: queryKeys.posts.lists() })
    },
  })
}
```

### Optimistic Updates
```typescript
// features/posts/hooks/useUpdatePost.ts
import { useMutation, useQueryClient } from '@tanstack/react-query'
import { queryKeys } from '@/lib/query-keys'
import type { Post, UpdatePostInput } from '@/features/posts/types'

export function useUpdatePost() {
  const queryClient = useQueryClient()

  return useMutation({
    mutationFn: postApi.updatePost,
    onMutate: async (newPost: UpdatePostInput) => {
      // Cancel outgoing refetches
      await queryClient.cancelQueries({
        queryKey: queryKeys.posts.detail(newPost.id)
      })

      // Snapshot previous value
      const previous = queryClient.getQueryData<Post>(
        queryKeys.posts.detail(newPost.id)
      )

      // Optimistically update
      queryClient.setQueryData(
        queryKeys.posts.detail(newPost.id),
        (old: Post | undefined) => old ? { ...old, ...newPost } : undefined
      )

      return { previous }
    },
    onError: (err, newPost, context) => {
      // Rollback on error
      if (context?.previous) {
        queryClient.setQueryData(
          queryKeys.posts.detail(newPost.id),
          context.previous
        )
      }
    },
    onSettled: (data, error, variables) => {
      // Always refetch after error or success
      queryClient.invalidateQueries({
        queryKey: queryKeys.posts.detail(variables.id)
      })
    },
  })
}
```

### Delete with Optimistic Update
```typescript
export function useDeletePost() {
  const queryClient = useQueryClient()

  return useMutation({
    mutationFn: postApi.deletePost,
    onMutate: async (postId: string) => {
      await queryClient.cancelQueries({ queryKey: queryKeys.posts.lists() })

      const previousLists = queryClient.getQueriesData<Post[]>({
        queryKey: queryKeys.posts.lists()
      })

      // Remove from all lists optimistically
      queryClient.setQueriesData<Post[]>(
        { queryKey: queryKeys.posts.lists() },
        (old) => old?.filter(post => post.id !== postId)
      )

      return { previousLists }
    },
    onError: (err, postId, context) => {
      context?.previousLists.forEach(([queryKey, data]) => {
        queryClient.setQueryData(queryKey, data)
      })
    },
    onSettled: () => {
      queryClient.invalidateQueries({ queryKey: queryKeys.posts.all() })
    },
  })
}
```

## Prefetching

### In Route Loaders
```typescript
// routes/posts.tsx
export const Route = createFileRoute('/posts')({
  loader: ({ context: { queryClient } }) =>
    queryClient.ensureQueryData(postsQueryOptions()),
})
```

### On Hover/Focus
```typescript
import { useQueryClient } from '@tanstack/react-query'
import { Link } from '@tanstack/react-router'
import { postQueryOptions } from '@/features/posts/queries'

function PostLink({ postId, title }: { postId: string; title: string }) {
  const queryClient = useQueryClient()

  const prefetch = () => {
    queryClient.prefetchQuery(postQueryOptions(postId))
  }

  return (
    <Link
      to="/posts/$postId"
      params={{ postId }}
      onMouseEnter={prefetch}
      onFocus={prefetch}
    >
      {title}
    </Link>
  )
}
```

## Infinite Queries

```typescript
import { useInfiniteQuery } from '@tanstack/react-query'

export function useInfinitePosts(filters: PostFilters) {
  return useInfiniteQuery({
    queryKey: queryKeys.posts.list({ ...filters, infinite: true }),
    queryFn: ({ pageParam = 1 }) =>
      postApi.getPosts({ ...filters, page: pageParam }),
    getNextPageParam: (lastPage, pages) =>
      lastPage.hasMore ? pages.length + 1 : undefined,
    initialPageParam: 1,
  })
}
```

## Dependent Queries

```typescript
function PostWithAuthor({ postId }: { postId: string }) {
  const { data: post } = useQuery(postQueryOptions(postId))

  const { data: author } = useQuery({
    ...userQueryOptions(post?.authorId ?? ''),
    enabled: Boolean(post?.authorId),
  })

  if (!post) return <Skeleton />

  return (
    <article>
      <h1>{post.title}</h1>
      {author && <p>By {author.name}</p>}
    </article>
  )
}
```

## Conventions to Enforce

1. **Factory pattern for keys** - All query keys through `queryKeys` factory
2. **Query options factories** - Define in `features/*/queries/` directories
3. **Invalidate by hierarchy** - Use `queryKeys.posts.lists()` to invalidate all lists
4. **Optimistic updates** - Always include rollback logic
5. **Enable conditional queries** - Use `enabled` option for dependent queries
6. **Proper staleTime** - Set based on data freshness requirements
7. **Use gcTime not cacheTime** - Renamed in v5

## Anti-Patterns to Block

```typescript
// ❌ WRONG: String query keys
useQuery({ queryKey: ['posts', postId] })

// ✅ CORRECT: Factory pattern
useQuery(postQueryOptions(postId))

// ❌ WRONG: Inline query function
useQuery({
  queryKey: queryKeys.posts.detail(postId),
  queryFn: async () => {
    const res = await fetch(`/api/posts/${postId}`)
    return res.json()
  }
})

// ✅ CORRECT: Extracted to API layer
useQuery(postQueryOptions(postId))

// ❌ WRONG: Manual cache updates without invalidation
onSuccess: (newPost) => {
  queryClient.setQueryData(['posts', newPost.id], newPost)
}

// ✅ CORRECT: Invalidate to refetch
onSuccess: () => {
  queryClient.invalidateQueries({ queryKey: queryKeys.posts.all() })
}

// ❌ WRONG: Using cacheTime (deprecated)
useQuery({ cacheTime: 5000 })

// ✅ CORRECT: Use gcTime
useQuery({ gcTime: 5000 })
```
