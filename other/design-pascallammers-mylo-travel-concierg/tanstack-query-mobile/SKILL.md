---
name: tanstack-query-mobile
description: TanStack Query for React Native data fetching. Use when implementing server state.
---

# TanStack Query Mobile Skill

This skill covers TanStack Query for React Native apps.

## When to Use

Use this skill when:
- Fetching data from APIs
- Caching server data
- Synchronizing server state
- Implementing pagination
- Optimistic updates

## Core Principle

**SERVER STATE** - TanStack Query manages server state. Use Zustand for client state.

## Installation

```bash
npm install @tanstack/react-query
```

## Setup

```typescript
// app/_layout.tsx
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';

const queryClient = new QueryClient({
  defaultOptions: {
    queries: {
      staleTime: 1000 * 60 * 5, // 5 minutes
      gcTime: 1000 * 60 * 30,   // 30 minutes (formerly cacheTime)
      retry: 2,
      refetchOnWindowFocus: false, // Disable for mobile
    },
  },
});

export default function RootLayout(): React.ReactElement {
  return (
    <QueryClientProvider client={queryClient}>
      <Stack />
    </QueryClientProvider>
  );
}
```

## Basic Query

```typescript
import { useQuery } from '@tanstack/react-query';

interface User {
  id: string;
  name: string;
  email: string;
}

async function fetchUser(id: string): Promise<User> {
  const response = await fetch(`/api/users/${id}`);
  if (!response.ok) throw new Error('Failed to fetch user');
  return response.json();
}

function UserProfile({ userId }: { userId: string }): React.ReactElement {
  const { data: user, isLoading, isError, error } = useQuery({
    queryKey: ['user', userId],
    queryFn: () => fetchUser(userId),
  });

  if (isLoading) {
    return <ActivityIndicator />;
  }

  if (isError) {
    return <Text>Error: {error.message}</Text>;
  }

  return (
    <View>
      <Text>{user.name}</Text>
      <Text>{user.email}</Text>
    </View>
  );
}
```

## Query with Authentication

```typescript
import { useQuery } from '@tanstack/react-query';
import { useAuthStore } from '@/store/authStore';

function useUserPosts() {
  const token = useAuthStore((state) => state.token);

  return useQuery({
    queryKey: ['posts', 'user'],
    queryFn: async () => {
      const response = await fetch('/api/posts', {
        headers: {
          Authorization: `Bearer ${token}`,
        },
      });
      if (!response.ok) throw new Error('Failed to fetch posts');
      return response.json();
    },
    enabled: !!token, // Only fetch when authenticated
  });
}
```

## Mutations

```typescript
import { useMutation, useQueryClient } from '@tanstack/react-query';

interface CreatePostInput {
  title: string;
  content: string;
}

function useCreatePost() {
  const queryClient = useQueryClient();
  const token = useAuthStore((state) => state.token);

  return useMutation({
    mutationFn: async (input: CreatePostInput) => {
      const response = await fetch('/api/posts', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          Authorization: `Bearer ${token}`,
        },
        body: JSON.stringify(input),
      });
      if (!response.ok) throw new Error('Failed to create post');
      return response.json();
    },
    onSuccess: () => {
      // Invalidate posts query to refetch
      queryClient.invalidateQueries({ queryKey: ['posts'] });
    },
  });
}

// Usage
function CreatePostForm(): React.ReactElement {
  const { mutate, isPending } = useCreatePost();

  const handleSubmit = (data: CreatePostInput) => {
    mutate(data, {
      onSuccess: () => {
        // Navigate or show success
      },
      onError: (error) => {
        // Show error toast
      },
    });
  };

  return (
    <Button onPress={() => handleSubmit({ title, content })} disabled={isPending}>
      {isPending ? 'Creating...' : 'Create Post'}
    </Button>
  );
}
```

## Optimistic Updates

```typescript
function useLikePost() {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: (postId: string) =>
      fetch(`/api/posts/${postId}/like`, { method: 'POST' }),

    onMutate: async (postId) => {
      // Cancel outgoing refetches
      await queryClient.cancelQueries({ queryKey: ['posts'] });

      // Snapshot previous value
      const previousPosts = queryClient.getQueryData(['posts']);

      // Optimistically update
      queryClient.setQueryData(['posts'], (old: Post[]) =>
        old.map((post) =>
          post.id === postId
            ? { ...post, likes: post.likes + 1, isLiked: true }
            : post
        )
      );

      return { previousPosts };
    },

    onError: (err, postId, context) => {
      // Rollback on error
      queryClient.setQueryData(['posts'], context?.previousPosts);
    },

    onSettled: () => {
      // Refetch after error or success
      queryClient.invalidateQueries({ queryKey: ['posts'] });
    },
  });
}
```

## Infinite Queries (Pagination)

```typescript
import { useInfiniteQuery } from '@tanstack/react-query';
import { FlashList } from '@shopify/flash-list';

interface PostsResponse {
  posts: Post[];
  nextCursor: string | null;
}

function useInfinitePosts() {
  return useInfiniteQuery({
    queryKey: ['posts', 'infinite'],
    queryFn: async ({ pageParam }) => {
      const response = await fetch(
        `/api/posts?cursor=${pageParam ?? ''}&limit=20`
      );
      return response.json() as Promise<PostsResponse>;
    },
    initialPageParam: null as string | null,
    getNextPageParam: (lastPage) => lastPage.nextCursor,
  });
}

function PostsList(): React.ReactElement {
  const {
    data,
    fetchNextPage,
    hasNextPage,
    isFetchingNextPage,
  } = useInfinitePosts();

  const posts = data?.pages.flatMap((page) => page.posts) ?? [];

  return (
    <FlashList
      data={posts}
      renderItem={({ item }) => <PostCard post={item} />}
      estimatedItemSize={100}
      onEndReached={() => {
        if (hasNextPage && !isFetchingNextPage) {
          fetchNextPage();
        }
      }}
      onEndReachedThreshold={0.5}
      ListFooterComponent={
        isFetchingNextPage ? <ActivityIndicator /> : null
      }
    />
  );
}
```

## Pull to Refresh

```typescript
import { RefreshControl } from 'react-native';

function PostsList(): React.ReactElement {
  const { data, isLoading, refetch, isRefetching } = usePosts();

  return (
    <FlashList
      data={data}
      renderItem={renderItem}
      estimatedItemSize={100}
      refreshControl={
        <RefreshControl
          refreshing={isRefetching}
          onRefresh={refetch}
        />
      }
    />
  );
}
```

## Query Hooks Pattern

```typescript
// hooks/queries/usePosts.ts
export function usePosts() {
  return useQuery({
    queryKey: ['posts'],
    queryFn: fetchPosts,
  });
}

export function usePost(id: string) {
  return useQuery({
    queryKey: ['posts', id],
    queryFn: () => fetchPost(id),
    enabled: !!id,
  });
}

// hooks/mutations/usePostMutations.ts
export function useCreatePost() {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: createPost,
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['posts'] });
    },
  });
}

export function useDeletePost() {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: deletePost,
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['posts'] });
    },
  });
}
```

## API Client

```typescript
// lib/api.ts
import axios from 'axios';
import * as SecureStore from 'expo-secure-store';

const api = axios.create({
  baseURL: process.env.EXPO_PUBLIC_API_URL,
});

api.interceptors.request.use(async (config) => {
  const token = await SecureStore.getItemAsync('authToken');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

export default api;
```

## Notes

- Use queryKey for cache identification
- Invalidate queries after mutations
- Use enabled for conditional fetching
- Implement optimistic updates for better UX
- Use infinite queries for pagination
- Create custom hooks for reusability
