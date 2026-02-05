---
name: firebase-operations
description: Performs Firebase Firestore operations. Use when querying collections, creating/updating/deleting documents, using batch writes, or working with Timestamps. Includes pagination, transactions, and security rules patterns.
---

# Firebase Operations Skill

## Instructions

1. Import `getAdminDb, COLLECTIONS` from `@/lib/firebase-admin`
2. Use `Timestamp.now()` for timestamps
3. Convert to ISO string for API responses: `createdAt.toDate().toISOString()`
4. Use batch writes for multiple operations (max 500)
5. Use transactions for atomic operations

## Quick Reference

```typescript
import { getAdminDb, COLLECTIONS } from '@/lib/firebase-admin'
import { Timestamp, FieldValue } from 'firebase-admin/firestore'

// Get document
const doc = await db.collection(COLLECTIONS.PROJECTS).doc(id).get()

// Create with timestamps
const now = Timestamp.now()
await docRef.set({ ...data, createdAt: now, updatedAt: now })

// Update
await docRef.update({ field: value, updatedAt: Timestamp.now() })

// Increment counter
await docRef.update({ likes: FieldValue.increment(1) })
```

For complete operations (batch writes, transactions, pagination, queries), see [reference.md](reference.md).
