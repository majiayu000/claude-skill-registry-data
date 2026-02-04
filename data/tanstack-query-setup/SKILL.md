---
name: tanstack-query-setup
description: TanStack Query setup for data fetching and caching. Use when implementing server state management.
---

# TanStack Query Setup Skill

This skill covers TanStack Query (React Query) for server state management.

## When to Use

Use this skill when:
- Fetching data from APIs
- Implementing caching strategies
- Handling mutations with optimistic updates
- Managing server state

## Core Principle

**SERVER STATE IS DIFFERENT** - Server state is async, cached, and can become stale. TanStack Query handles this complexity.

## Installation & Setup

```bash
npm install @tanstack/react-query
```

```typescript
// app/providers.tsx
'use client';

import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import { ReactQueryDevtools } from '@tanstack/react-query-devtools';
import { useState } from 'react';

export function Providers({ children }: { children: React.ReactNode }): React.ReactElement {
  const [queryClient] = useState(
    () =>
      new QueryClient({
        defaultOptions: {
          queries: {
            staleTime: 60 * 1000, // 1 minute
            gcTime: 5 * 60 * 1000, // 5 minutes (formerly cacheTime)
            retry: 1,
            refetchOnWindowFocus: false,
          },
        },
      })
  );

  return (
    <QueryClientProvider client={queryClient}>
      {children}
      <ReactQueryDevtools initialIsOpen={false} />
    </QueryClientProvider>
  );
}
```

## Query Keys Factory

```typescript
// lib/queryKeys.ts
export const userKeys = {
  all: ['users'] as const,
  lists: () => [...userKeys.all, 'list'] as const,
  list: (filters: UserFilters) => [...userKeys.lists(), filters] as const,
  details: () => [...userKeys.all, 'detail'] as const,
  detail: (id: string) => [...userKeys.details(), id] as const,
};

export const postKeys = {
  all: ['posts'] as const,
  lists: () => [...postKeys.all, 'list'] as const,
  list: (filters: PostFilters) => [...postKeys.lists(), filters] as const,
  details: () => [...postKeys.all, 'detail'] as const,
  detail: (id: string) => [...postKeys.details(), id] as const,
  byUser: (userId: string) => [...postKeys.all, 'user', userId] as const,
};
```

## Basic Query

```typescript
import { useQuery } from '@tanstack/react-query';
import { userKeys } from '@/lib/queryKeys';

interface User {
  id: string;
  name: string;
  email: string;
}

async function fetchUser(id: string): Promise<User> {
  const response = await fetch(`/api/users/${id}`);
  if (!response.ok) {
    throw new Error('Failed to fetch user');
  }
  return response.json();
}

export function useUser(userId: string) {
  return useQuery({
    queryKey: userKeys.detail(userId),
    queryFn: () => fetchUser(userId),
    staleTime: 5 * 60 * 1000, // 5 minutes
    enabled: !!userId, // Only fetch if userId exists
  });
}

// Usage in component
function UserProfile({ userId }: { userId: string }): React.ReactElement {
  const { data: user, isLoading, error } = useUser(userId);

  if (isLoading) return <Loading />;
  if (error) return <Error message={error.message} />;
  if (!user) return <NotFound />;

  return <div>{user.name}</div>;
}
```

## Query with Parameters

```typescript
interface UserFilters {
  page: number;
  limit: number;
  search?: string;
}

interface UsersResponse {
  users: User[];
  total: number;
  page: number;
}

async function fetchUsers(filters: UserFilters): Promise<UsersResponse> {
  const params = new URLSearchParams({
    page: String(filters.page),
    limit: String(filters.limit),
    ...(filters.search && { search: filters.search }),
  });

  const response = await fetch(`/api/users?${params}`);
  if (!response.ok) throw new Error('Failed to fetch users');
  return response.json();
}

export function useUsers(filters: UserFilters) {
  return useQuery({
    queryKey: userKeys.list(filters),
    queryFn: () => fetchUsers(filters),
    placeholderData: (previousData) => previousData, // Keep previous data while fetching
  });
}
```

## Mutations

### Basic Mutation

```typescript
import { useMutation, useQueryClient } from '@tanstack/react-query';

interface CreateUserInput {
  name: string;
  email: string;
}

async function createUser(input: CreateUserInput): Promise<User> {
  const response = await fetch('/api/users', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(input),
  });
  if (!response.ok) throw new Error('Failed to create user');
  return response.json();
}

export function useCreateUser() {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: createUser,
    onSuccess: () => {
      // Invalidate and refetch users list
      queryClient.invalidateQueries({ queryKey: userKeys.lists() });
    },
  });
}

// Usage
function CreateUserForm(): React.ReactElement {
  const createUser = useCreateUser();

  const handleSubmit = (e: FormEvent<HTMLFormElement>): void => {
    e.preventDefault();
    const formData = new FormData(e.currentTarget);
    createUser.mutate({
      name: formData.get('name') as string,
      email: formData.get('email') as string,
    });
  };

  return (
    <form onSubmit={handleSubmit}>
      <input name="name" required />
      <input name="email" type="email" required />
      <button type="submit" disabled={createUser.isPending}>
        {createUser.isPending ? 'Creating...' : 'Create'}
      </button>
      {createUser.error && <p>{createUser.error.message}</p>}
    </form>
  );
}
```

### Optimistic Updates

```typescript
export function useUpdateUser() {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: updateUser,
    onMutate: async (newUser) => {
      // Cancel outgoing refetches
      await queryClient.cancelQueries({ queryKey: userKeys.detail(newUser.id) });

      // Snapshot previous value
      const previousUser = queryClient.getQueryData<User>(
        userKeys.detail(newUser.id)
      );

      // Optimistically update
      queryClient.setQueryData(userKeys.detail(newUser.id), newUser);

      // Return context with snapshot
      return { previousUser };
    },
    onError: (_err, newUser, context) => {
      // Rollback on error
      if (context?.previousUser) {
        queryClient.setQueryData(
          userKeys.detail(newUser.id),
          context.previousUser
        );
      }
    },
    onSettled: (_data, _error, newUser) => {
      // Refetch to ensure consistency
      queryClient.invalidateQueries({ queryKey: userKeys.detail(newUser.id) });
    },
  });
}
```

## Infinite Queries

```typescript
import { useInfiniteQuery } from '@tanstack/react-query';

interface PostsPage {
  posts: Post[];
  nextCursor: string | null;
}

async function fetchPosts(cursor?: string): Promise<PostsPage> {
  const params = cursor ? `?cursor=${cursor}` : '';
  const response = await fetch(`/api/posts${params}`);
  return response.json();
}

export function useInfinitePosts() {
  return useInfiniteQuery({
    queryKey: postKeys.lists(),
    queryFn: ({ pageParam }) => fetchPosts(pageParam),
    initialPageParam: undefined as string | undefined,
    getNextPageParam: (lastPage) => lastPage.nextCursor ?? undefined,
  });
}

// Usage
function PostList(): React.ReactElement {
  const {
    data,
    fetchNextPage,
    hasNextPage,
    isFetchingNextPage,
  } = useInfinitePosts();

  return (
    <div>
      {data?.pages.map((page, i) => (
        <React.Fragment key={i}>
          {page.posts.map((post) => (
            <PostCard key={post.id} post={post} />
          ))}
        </React.Fragment>
      ))}

      <button
        onClick={() => fetchNextPage()}
        disabled={!hasNextPage || isFetchingNextPage}
      >
        {isFetchingNextPage ? 'Loading...' : hasNextPage ? 'Load More' : 'No more'}
      </button>
    </div>
  );
}
```

## Prefetching

```typescript
import { useQueryClient } from '@tanstack/react-query';

function UserList(): React.ReactElement {
  const queryClient = useQueryClient();

  const prefetchUser = (userId: string): void => {
    queryClient.prefetchQuery({
      queryKey: userKeys.detail(userId),
      queryFn: () => fetchUser(userId),
      staleTime: 5 * 60 * 1000,
    });
  };

  return (
    <ul>
      {users.map((user) => (
        <li
          key={user.id}
          onMouseEnter={() => prefetchUser(user.id)}
        >
          <Link to={`/users/${user.id}`}>{user.name}</Link>
        </li>
      ))}
    </ul>
  );
}
```

## Dependent Queries

```typescript
function useUserPosts(userId: string | undefined) {
  const userQuery = useUser(userId ?? '');

  return useQuery({
    queryKey: postKeys.byUser(userId ?? ''),
    queryFn: () => fetchUserPosts(userId!),
    enabled: !!userId && userQuery.isSuccess,
  });
}
```

## Error Handling

```typescript
const queryClient = new QueryClient({
  defaultOptions: {
    queries: {
      retry: (failureCount, error) => {
        // Don't retry on 4xx errors
        if (error instanceof Response && error.status >= 400 && error.status < 500) {
          return false;
        }
        return failureCount < 3;
      },
    },
    mutations: {
      onError: (error) => {
        // Global error handling
        console.error('Mutation error:', error);
      },
    },
  },
});
```

## Best Practices

1. **Use query key factories** - Consistent, type-safe keys
2. **Set staleTime** - Prevent unnecessary refetches
3. **Use selectors** - `select` option for derived data
4. **Prefetch** - Improve perceived performance
5. **Optimistic updates** - Better UX for mutations
6. **Error boundaries** - Handle query errors gracefully

## TanStack Query vs Zustand

| Use Case | Tool |
|----------|------|
| API data | TanStack Query |
| User authentication state | Zustand |
| Shopping cart | Zustand |
| Theme/settings | Zustand |
| Form state | React Hook Form |

## Notes

- gcTime (formerly cacheTime) is how long inactive data stays in cache
- staleTime is how long data is considered fresh
- Use React Query DevTools for debugging
- Works with Server Components via initial data
