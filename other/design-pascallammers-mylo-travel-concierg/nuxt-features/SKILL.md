---
name: nuxt-features
description: Feature module pattern organizing domain logic into queries, mutations, and actions. Use when implementing data fetching with filters, API mutations with loading states, business logic with UI feedback, or organizing domain-specific code.
---

# Nuxt Features

Domain-based feature modules with three-layer pattern: queries, mutations, actions.

## Core Concepts

**[queries.md](references/queries.md)** - Reactive data fetching with filters
**[mutations.md](references/mutations.md)** - Pure API operations with loading states
**[actions.md](references/actions.md)** - Business logic with UI feedback

## Pattern Flow

```
Component → Action → Mutation → Repository → API
              ↓
         Query (reactive data fetching)
```

## Directory Structure

```
features/{domain}/
├── queries/
│   ├── get-posts-query.ts      # List with filters
│   └── get-post-query.ts       # Single item
├── mutations/
│   ├── create-post-mutation.ts
│   ├── update-post-mutation.ts
│   └── delete-post-mutation.ts
└── actions/
    ├── create-post-action.ts
    ├── update-post-action.ts
    └── delete-post-action.ts
```

## Quick Examples

**Query** - Reactive data fetching:
```typescript
export default function getPostsQueryFactory() {
  const postApi = useRepository('posts')
  return (filters: MaybeRef<GetPostsFilters>) => {
    return useFilterQuery('posts', () => postApi.list(params), filters)
  }
}
```

**Mutation** - Pure API call:
```typescript
export default function createPostMutationFactory() {
  const postApi = useRepository('posts')
  const { start, stop, waitingFor } = useWait()
  return async (data: CreatePostData) => {
    start(waitingFor.posts.creating)
    try { return (await postApi.create(data)).data }
    finally { stop(waitingFor.posts.creating) }
  }
}
```

**Action** - Business logic + UI:
```typescript
export default function createPostActionFactory() {
  const createPost = createPostMutationFactory()
  const flash = useFlash()
  return async (data: CreatePostData) => {
    const post = await createPost(data)
    flash.success('Post created!')
    return post
  }
}
```
