---
name: firestore-data-modeling-patterns
description: |
  Firestore data modeling best practices including subcollections vs root collections, document structure,
  relationships, query optimization, composite indexes, and atomic operations (transactions vs batches).
  Keywords: "subcollection", "root collection", "data model", "relationship", "index", "transaction", "batch"
---

# Firestore Data Modeling Patterns

## Overview

Firestore is a NoSQL document database that requires careful modeling to optimize for query patterns, scalability, and cost. This skill provides patterns for structuring data effectively.

## Subcollections vs. Root Collections

### When to Use Subcollections

**Pattern**: `users/{userId}/orders/{orderId}`

**Use When**:
- Data is tightly coupled to a parent (orders belong to a specific user)
- Child data is always accessed via parent
- You don't need to query children globally across all parents
- Document hierarchy makes semantic sense

**Example**:
```typescript
// User's private sessions (accessed only via user)
users/{userId}/sessions/{sessionId}

// User's notification preferences
users/{userId}/settings/notifications
```

**Critical Limitation**: Deleting a parent document **does NOT** delete subcollections. You must implement cleanup logic (e.g., Cloud Function).

### When to Use Root Collections

**Pattern**: Separate `users` and `posts` collections with reference fields

**Use When**:
- Need to query data globally (e.g., "all posts across all users")
- Data has many-to-many relationships
- Want simpler deletion semantics (no orphaned data risk)
- Need flexibility for future access patterns

**Example**:
```typescript
// posts collection
{
  id: "post1",
  authorId: "user123",  // Reference to users collection
  title: "...",
  createdAt: Timestamp
}

// Query all posts by a user
postsRef.where('authorId', '==', 'user123').get()

// Query all posts globally
postsRef.orderBy('createdAt', 'desc').limit(10).get()
```

**Decision Matrix**:

| Criterion | Subcollection | Root Collection |
|-----------|--------------|-----------------|
| Query across parents | ❌ Requires Collection Group Query | ✅ Simple query |
| Deletion cascade | ❌ Manual cleanup needed | ✅ Independent lifecycle |
| Document limit (1MB) | ✅ Spreads data | ⚠️ Risk if embedding arrays |
| Semantic hierarchy | ✅ Clear parent-child | ⚠️ Relies on references |

## Document Structure Best Practices

### Embedding vs. Referencing

**Embed When**:
- Data is small and frequently accessed together
- 1-to-1 or 1-to-few relationships
- Data doesn't change frequently

```typescript
// User profile with embedded address
{
  id: "user1",
  name: "Alice",
  address: {
    street: "123 Main St",
    city: "NYC",
    zip: "10001"
  }
}
```

**Reference When**:
- Data is large or changes frequently
- 1-to-many or many-to-many relationships
- Need to query the related data independently

```typescript
// Post references author
{
  id: "post1",
  title: "My Post",
  authorId: "user1", // Reference
  categoryIds: ["cat1", "cat2"] // Many-to-many
}
```

### Document Size Limits

- **Max Document Size**: 1MB
- **Max Array Size**: 20,000 elements (but practical limit is much lower for performance)
- **Max Nesting Depth**: 20 levels

**Anti-Pattern**:
```typescript
// ❌ BAD: Embedding large comment array
{
  postId: "post1",
  comments: [ /* 1000s of comments */ ] // Will exceed 1MB!
}
```

**Solution**:
```typescript
// ✅ GOOD: Comments as separate collection
posts/post1
comments/comment1 { postId: "post1", ... }
comments/comment2 { postId: "post1", ... }
```

## Query Optimization and Indexes

### Single-Field Indexes

Firestore automatically creates single-field indexes. No action needed for:
```typescript
// Automatic indexes
postsRef.where('status', '==', 'published').get()
postsRef.orderBy('createdAt', 'desc').get()
```

### Composite Indexes

**Required For**:
- Multiple `where` clauses
- Combining `where` and `orderBy` on different fields
- Array-contains with other filters

**Example Requiring Index**:
```typescript
// Query: Published posts sorted by creation date
postsRef
  .where('status', '==', 'published')
  .orderBy('createdAt', 'desc')
  .get()
```

**Generate Index** (`firestore.indexes.json`):
```json
{
  "indexes": [
    {
      "collectionGroup": "posts",
      "queryScope": "COLLECTION",
      "fields": [
        { "fieldPath": "status", "order": "ASCENDING" },
        { "fieldPath": "createdAt", "order": "DESCENDING" }
      ]
    }
  ]
}
```

**Deploy**:
```bash
firebase deploy --only firestore:indexes
```

**Development Tip**: Firestore returns an error with a direct link to create the index in the Firebase Console during development.

### Collection Group Queries

To query across subcollections with the same name:

```typescript
// Query all comments across all posts
db.collectionGroup('comments')
  .where('authorId', '==', 'user1')
  .get()
```

**Requires**: Collection Group index (created automatically or via console)

## Atomic Operations

### Transactions (Read-Modify-Write)

**Use When**: Write depends on current document state

**Example**: Increment a counter
```typescript
import { runTransaction } from 'firebase/firestore';

await runTransaction(db, async (transaction) => {
  const postRef = doc(db, 'posts', 'post1');
  const postDoc = await transaction.get(postRef);

  if (!postDoc.exists()) {
    throw new Error('Post does not exist');
  }

  const newViewCount = postDoc.data().viewCount + 1;
  transaction.update(postRef, { viewCount: newViewCount });
});
```

**Characteristics**:
- ✅ Reads must precede writes
- ✅ Automatic retries on conflicts
- ❌ Fails if offline
- ❌ Limited to 500 documents

### Batched Writes (Write-Only)

**Use When**: Multiple independent write operations need atomicity

**Example**: Create user + settings document
```typescript
import { writeBatch } from 'firebase/firestore';

const batch = writeBatch(db);

const userRef = doc(db, 'users', 'user1');
batch.set(userRef, {
  name: 'Alice',
  email: 'alice@example.com',
  createdAt: serverTimestamp(),
});

const settingsRef = doc(db, 'users', 'user1', 'settings', 'notifications');
batch.set(settingsRef, {
  emailNotifications: true,
  pushNotifications: false,
});

await batch.commit(); // All succeed or all fail
```

**Characteristics**:
- ✅ Faster than transactions
- ✅ Works offline (queued)
- ✅ Up to 500 operations
- ❌ No reads allowed

**Decision Rule**: Default to batched writes (simpler, faster). Use transactions only when reads are required.

## Data Relationships

### One-to-Many

**Option 1: Subcollection** (Parent → Children)
```typescript
users/user1
users/user1/orders/order1
users/user1/orders/order2
```

**Option 2: Root Collection with Reference** (More flexible)
```typescript
users/user1
orders/order1 { userId: "user1" }
orders/order2 { userId: "user1" }
```

### Many-to-Many

**Pattern**: Store array of IDs or use join collection

**Option 1: Array of IDs** (Best for small, stable lists)
```typescript
// Post with categories
posts/post1 {
  categoryIds: ["cat1", "cat2", "cat3"]
}

// Query posts in category
postsRef.where('categoryIds', 'array-contains', 'cat1').get()
```

**Option 2: Join Collection** (Best for large or dynamic relationships)
```typescript
users/user1
courses/course1
enrollments/enroll1 { userId: "user1", courseId: "course1" }
```

## Best Practices Summary

✅ **Do**:
- Denormalize data for read-heavy applications
- Use root collections for flexibility
- Create composite indexes for complex queries
- Use batched writes for atomic multi-document updates
- Keep documents under 1MB

❌ **Don't**:
- Embed large arrays or frequently-changing data
- Use subcollections without cleanup strategy
- Create excessive indexes (storage cost + write latency)
- Assume parent deletion cascades to subcollections
- Use transactions when batches suffice

## Query Performance Tips

1. **Limit Result Sets**: Always use `.limit()` for lists
2. **Paginate**: Use `.startAfter()` for cursor-based pagination
3. **Index Overhead**: Each index adds ~1ms write latency
4. **Denormalize for Reads**: Copy frequently-accessed data (e.g., author name in post)

---

**Related Skills**: `zod-firestore-type-safety`, `firebase-nextjs-integration-strategies`
**Token Estimate**: ~1,200 tokens
