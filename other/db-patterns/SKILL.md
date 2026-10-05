---
name: TanStack DB Patterns (Beta)
description: >-
  TanStack DB patterns for client-first reactive data stores. Activates when
  implementing offline-first apps, local-first data, or reactive client databases.
  NOTE: Beta library - API may change.
version: 1.0.0
---

# TanStack DB Patterns (Beta)

> **Beta Library**: TanStack DB is in beta. APIs may change between versions.

TanStack DB provides a client-first reactive data store with optional sync to remote sources.

## Core Concepts

- **Collections**: Named groups of documents (like tables)
- **Documents**: Individual records with unique IDs
- **Queries**: Reactive queries that update when data changes
- **Transactions**: Atomic operations across multiple documents
- **Sync**: Optional sync to remote backends

## Basic Setup

```typescript
// lib/db.ts
import { createDB, createCollection } from '@tanstack/db'

// Define document types
interface Post {
  id: string
  title: string
  content: string
  authorId: string
  published: boolean
  createdAt: number
  updatedAt: number
}

interface User {
  id: string
  name: string
  email: string
}

// Create database
export const db = createDB({
  collections: {
    posts: createCollection<Post>(),
    users: createCollection<User>(),
  },
})
```

## CRUD Operations

### Create
```typescript
import { db } from '@/lib/db'

// Insert a single document
const newPost = await db.posts.insert({
  id: crypto.randomUUID(),
  title: 'My Post',
  content: 'Post content...',
  authorId: 'user-1',
  published: false,
  createdAt: Date.now(),
  updatedAt: Date.now(),
})

// Insert multiple documents
await db.posts.insertMany([
  { id: '1', title: 'Post 1', ... },
  { id: '2', title: 'Post 2', ... },
])
```

### Read
```typescript
// Get by ID
const post = await db.posts.get('post-id')

// Query with filters
const publishedPosts = await db.posts.findMany({
  where: { published: true },
  orderBy: { createdAt: 'desc' },
  limit: 10,
})

// Query with complex filters
const userPosts = await db.posts.findMany({
  where: {
    authorId: 'user-1',
    published: true,
  },
})
```

### Update
```typescript
// Update by ID
await db.posts.update('post-id', {
  title: 'Updated Title',
  updatedAt: Date.now(),
})

// Update with function
await db.posts.update('post-id', (post) => ({
  ...post,
  viewCount: post.viewCount + 1,
  updatedAt: Date.now(),
}))

// Update many
await db.posts.updateMany(
  { where: { authorId: 'user-1' } },
  { published: false }
)
```

### Delete
```typescript
// Delete by ID
await db.posts.delete('post-id')

// Delete many
await db.posts.deleteMany({
  where: { published: false },
})
```

## Reactive Queries in React

```typescript
import { useQuery } from '@tanstack/db-react'
import { db } from '@/lib/db'

function PostList() {
  // Reactive query - updates when data changes
  const posts = useQuery(
    db.posts.query({
      where: { published: true },
      orderBy: { createdAt: 'desc' },
    })
  )

  return (
    <ul>
      {posts.map((post) => (
        <PostCard key={post.id} post={post} />
      ))}
    </ul>
  )
}

function PostDetail({ postId }: { postId: string }) {
  // Single document query
  const post = useQuery(db.posts.get(postId))

  if (!post) return <NotFound />

  return <article>{post.title}</article>
}
```

## Transactions

```typescript
import { db } from '@/lib/db'

async function transferPost(postId: string, newAuthorId: string) {
  await db.transaction(async (tx) => {
    // Get current post
    const post = await tx.posts.get(postId)
    if (!post) throw new Error('Post not found')

    // Update post author
    await tx.posts.update(postId, {
      authorId: newAuthorId,
      updatedAt: Date.now(),
    })

    // Update user post counts (if tracking)
    await tx.users.update(post.authorId, (user) => ({
      ...user,
      postCount: user.postCount - 1,
    }))

    await tx.users.update(newAuthorId, (user) => ({
      ...user,
      postCount: user.postCount + 1,
    }))
  })
}
```

## Sync with Remote Backend

```typescript
// lib/db.ts
import { createDB, createCollection, createSyncProvider } from '@tanstack/db'

const syncProvider = createSyncProvider({
  // Pull changes from server
  pull: async (collection, lastSync) => {
    const response = await fetch(`/api/${collection}/sync?since=${lastSync}`)
    return response.json()
  },

  // Push changes to server
  push: async (collection, changes) => {
    await fetch(`/api/${collection}/sync`, {
      method: 'POST',
      body: JSON.stringify(changes),
    })
  },
})

export const db = createDB({
  collections: {
    posts: createCollection<Post>(),
    users: createCollection<User>(),
  },
  sync: syncProvider,
})

// Trigger sync
await db.sync()

// Auto-sync on interval
setInterval(() => db.sync(), 30000)
```

## Offline-First Pattern

```typescript
import { useQuery, useMutation } from '@tanstack/db-react'
import { db } from '@/lib/db'

function CreatePostForm() {
  const createPost = useMutation(db.posts.insert)

  const handleSubmit = async (data: PostInput) => {
    // Immediately available locally
    await createPost.mutate({
      id: crypto.randomUUID(),
      ...data,
      createdAt: Date.now(),
      updatedAt: Date.now(),
      _pending: true, // Mark as pending sync
    })

    // Sync will happen in background when online
    if (navigator.onLine) {
      db.sync()
    }
  }

  return <form onSubmit={handleSubmit}>{/* form fields */}</form>
}

// Show pending items differently
function PostCard({ post }: { post: Post }) {
  return (
    <div className={post._pending ? 'opacity-50' : ''}>
      {post.title}
      {post._pending && <span>Syncing...</span>}
    </div>
  )
}
```

## Integration with TanStack Query

```typescript
// Hybrid approach: DB for offline, Query for server sync
import { useQuery as useReactQuery } from '@tanstack/react-query'
import { useQuery as useDBQuery } from '@tanstack/db-react'
import { db } from '@/lib/db'

function PostList() {
  // Local DB for immediate data
  const localPosts = useDBQuery(
    db.posts.query({ where: { published: true } })
  )

  // Server query for sync
  const { data: serverPosts } = useReactQuery({
    queryKey: ['posts', 'published'],
    queryFn: () => postApi.getPosts({ published: true }),
    onSuccess: (posts) => {
      // Update local DB with server data
      db.posts.upsertMany(posts)
    },
  })

  // Use local data (always available, even offline)
  return (
    <ul>
      {localPosts.map((post) => (
        <PostCard key={post.id} post={post} />
      ))}
    </ul>
  )
}
```

## When to Use TanStack DB

| Scenario | Solution |
|----------|----------|
| Standard server data | TanStack Query |
| Offline-first app | TanStack DB |
| Local-first with sync | TanStack DB + sync |
| Real-time collaboration | TanStack DB + WebSocket sync |
| Complex client state | TanStack DB or Store |

## Conventions

1. **Type your collections** - Always define document interfaces
2. **Use transactions** - For multi-document operations
3. **Handle offline** - Design for offline-first
4. **Sync strategy** - Define clear sync patterns
5. **Combine with Query** - Use Query for pure server data

## Anti-Patterns

```typescript
// ❌ WRONG: Not using transactions for related updates
await db.posts.delete(postId)
await db.comments.deleteMany({ where: { postId } }) // Could fail leaving orphans

// ✅ CORRECT: Use transaction
await db.transaction(async (tx) => {
  await tx.posts.delete(postId)
  await tx.comments.deleteMany({ where: { postId } })
})

// ❌ WRONG: Using DB for pure server data without offline need
const posts = useDBQuery(db.posts.query({}))

// ✅ CORRECT: Use Query for server data
const { data: posts } = useQuery(postsQueryOptions())
```
