---
name: cascade-deletes
description: Normalized schema cascade delete patterns. Handles junction tables, parent-child ordering, nullify vs delete strategies. Triggers on "cascade", "delete", "cleanup", "junction", "related records", "deleteConversation", "deleteUser".
---

# Cascade Delete Patterns

Normalized schema requires explicit cascade deletes. Convex has no foreign key constraints or automatic cascades - must handle manually.

## Why Cascade Deletes Needed

Normalized schema separates related data into multiple tables. Deleting a conversation must also delete:
- Junction tables (projectConversations, conversationParticipants)
- Child records (messages, attachments, toolCalls, sources)
- Dependent entities (bookmarks, shares, canvasDocuments)

Leaving orphaned records wastes storage, breaks queries, violates data integrity.

## Core Strategy

1. **Parallel queries**: Fetch all related records with `Promise.all`
2. **Batch deletions**: Delete independent tables in parallel
3. **Sequential for dependencies**: Delete children before parents when order matters
4. **Nullify reusable entities**: Files/memories can exist without conversation

## Conversation Cascade Delete

From `packages/backend/convex/lib/utils/cascade.ts`:

```typescript
export async function cascadeDeleteConversation(
  ctx: MutationCtx,
  conversationId: Id<"conversations">,
  options?: { deleteMessages?: boolean; deleteConversation?: boolean },
): Promise<void> {
  const deleteMessages = options?.deleteMessages ?? true;
  const deleteConversation = options?.deleteConversation ?? true;

  // Step 1: Parallel queries for all related records
  const [
    bookmarks,
    shares,
    files,
    memories,
    junctions,
    participants,
    tokenUsage,
    attachments,
    toolCalls,
    sources,
    canvasDocs,
  ] = await Promise.all([
    ctx.db
      .query("bookmarks")
      .withIndex("by_conversation", (q) =>
        q.eq("conversationId", conversationId),
      )
      .collect(),
    ctx.db
      .query("shares")
      .withIndex("by_conversation", (q) =>
        q.eq("conversationId", conversationId),
      )
      .collect(),
    // ... more queries
  ]);

  // Step 2: Parallel deletions for independent tables
  await Promise.all([
    ...bookmarks.map((b) => ctx.db.delete(b._id)),
    ...shares.map((s) => ctx.db.delete(s._id)),
    ...junctions.map((j) => ctx.db.delete(j._id)),
    ...participants.map((p) => ctx.db.delete(p._id)),
    ...tokenUsage.map((t) => ctx.db.delete(t._id)),
    ...attachments.map((a) => ctx.db.delete(a._id)),
    ...toolCalls.map((tc) => ctx.db.delete(tc._id)),
    ...sources.map((src) => ctx.db.delete(src._id)),
  ]);

  // Step 3: Nullify files/memories (can exist independently)
  await Promise.all([
    ...files.map((f) => ctx.db.patch(f._id, { conversationId: undefined })),
    ...memories.map((m) => ctx.db.patch(m._id, { conversationId: undefined })),
  ]);

  // Step 4: Handle parent-child relationships (history before documents)
  for (const doc of canvasDocs) {
    const history = await ctx.db
      .query("canvasHistory")
      .withIndex("by_document", (q) => q.eq("documentId", doc._id))
      .collect();
    await Promise.all(history.map((h) => ctx.db.delete(h._id)));
    await ctx.db.delete(doc._id);
  }

  // Step 5: Delete messages (optional)
  if (deleteMessages) {
    const messages = await ctx.db
      .query("messages")
      .withIndex("by_conversation", (q) =>
        q.eq("conversationId", conversationId),
      )
      .collect();
    await Promise.all(messages.map((msg) => ctx.db.delete(msg._id)));
  }

  // Step 6: Delete conversation itself (optional)
  if (deleteConversation) await ctx.db.delete(conversationId);
}
```

Usage in mutations:

```typescript
export const deleteConversation = mutation({
  args: { conversationId: v.id("conversations") },
  handler: async (ctx, args) => {
    const user = await getCurrentUserOrCreate(ctx);
    const conv = await ctx.db.get(args.conversationId);
    if (!conv || conv.userId !== user._id) throw new Error("Not found");

    await cascadeDeleteConversation(ctx, args.conversationId);
  },
});
```

## Junction Table Cleanup

Junction tables represent many-to-many relationships. Must delete before parent entities.

```typescript
// ✅ CORRECT: Delete junction first
const junctions = await ctx.db
  .query("projectConversations")
  .withIndex("by_conversation", (q) =>
    q.eq("conversationId", conversationId),
  )
  .collect();

await Promise.all(junctions.map((j) => ctx.db.delete(j._id)));
```

Junction tables to handle:
- `projectConversations` - projects ↔ conversations
- `projectNotes` - projects ↔ notes
- `projectFiles` - projects ↔ files
- `conversationParticipants` - users ↔ conversations
- `bookmarkTags`, `snippetTags`, `noteTags`, `taskTags` - tags ↔ entities

## Nullify vs Delete Strategy

**Delete** - Entity only exists for this parent:
- `attachments` - message-specific files
- `toolCalls` - execution results tied to message
- `sources` - citations for specific message
- `bookmarks` - reference to message in conversation
- `shares` - share link for conversation

**Nullify** - Entity can exist independently:
- `files` - user uploads, can be reused across conversations
- `memories` - extracted facts, retain even after conversation deleted

```typescript
// Nullify pattern - preserve entity, remove association
await Promise.all([
  ...files.map((f) => ctx.db.patch(f._id, { conversationId: undefined })),
  ...memories.map((m) => ctx.db.patch(m._id, { conversationId: undefined })),
]);
```

## Parent-Child Ordering

When parent-child relationship exists, delete children first to avoid orphans.

**Example**: `canvasDocuments` (parent) → `canvasHistory` (child)

```typescript
// ❌ WRONG: Delete parent first, orphans children
await ctx.db.delete(doc._id);
const history = await ctx.db
  .query("canvasHistory")
  .withIndex("by_document", (q) => q.eq("documentId", doc._id))
  .collect();
await Promise.all(history.map((h) => ctx.db.delete(h._id))); // Already orphaned

// ✅ CORRECT: Delete children first
for (const doc of canvasDocs) {
  const history = await ctx.db
    .query("canvasHistory")
    .withIndex("by_document", (q) => q.eq("documentId", doc._id))
    .collect();
  await Promise.all(history.map((h) => ctx.db.delete(h._id)));
  await ctx.db.delete(doc._id);
}
```

Other parent-child relationships:
- `messages` (parent) → `attachments`, `toolCalls`, `sources` (children)
- `knowledgeSources` (parent) → `knowledgeChunks` (children)
- `files` (parent) → `fileChunks` (children)

## GDPR User Data Deletion

From `packages/backend/convex/lib/utils/cascade.ts`, 5-phase approach:

```typescript
export async function cascadeDeleteUserData(
  ctx: MutationCtx,
  userId: Id<"users">,
): Promise<void> {
  // Phase 1: Delete junction tables (many-to-many)
  const [bookmarkTags, snippetTags, noteTags, taskTags, ...] = await Promise.all([
    ctx.db.query("bookmarkTags").withIndex("by_user", (q) => q.eq("userId", userId)).collect(),
    // ...
  ]);
  await Promise.all([
    ...bookmarkTags.map((r) => ctx.db.delete(r._id)),
    // ...
  ]);

  // Phase 2: Delete child records (have FKs to parents deleted later)
  const [toolCalls, sources, attachments, ...] = await Promise.all([
    ctx.db.query("toolCalls").withIndex("by_user", (q) => q.eq("userId", userId)).collect(),
    // ...
  ]);
  await Promise.all([...toolCalls.map((r) => ctx.db.delete(r._id)), ...]);

  // Phase 3: Delete parent records (messages, canvasDocuments, knowledgeSources)
  const [messages, canvasDocuments, knowledgeSources] = await Promise.all([
    ctx.db.query("messages").withIndex("by_user", (q) => q.eq("userId", userId)).collect(),
    // ...
  ]);
  await Promise.all([...messages.map((r) => ctx.db.delete(r._id)), ...]);

  // Phase 4: Delete main content entities
  const [conversations, bookmarks, snippets, notes, tasks, ...] = await Promise.all([
    ctx.db.query("conversations").withIndex("by_user", (q) => q.eq("userId", userId)).collect(),
    // ...
  ]);
  await Promise.all([...conversations.map((r) => ctx.db.delete(r._id)), ...]);

  // Phase 5: Delete user config/metadata
  const [userPreferences, userOnboarding, usageRecords, ...] = await Promise.all([
    ctx.db.query("userPreferences").withIndex("by_user", (q) => q.eq("userId", userId)).collect(),
    // ...
  ]);
  await Promise.all([...userPreferences.map((r) => ctx.db.delete(r._id)), ...]);
}
```

Usage:

```typescript
export const deleteMyData = mutation({
  args: { confirmationText: v.string() },
  handler: async (ctx, { confirmationText }) => {
    if (confirmationText !== "DELETE MY DATA") {
      throw new Error('Please type "DELETE MY DATA" to confirm');
    }

    const identity = await ctx.auth.getUserIdentity();
    if (!identity) throw new Error("Unauthorized");

    const user = await ctx.db
      .query("users")
      .withIndex("by_clerk_id", (q) => q.eq("clerkId", identity.subject))
      .first();

    if (!user) throw new Error("User not found");

    await cascadeDeleteUserData(ctx, user._id);

    return { success: true };
  },
});
```

## Performance Optimization

**Parallel queries** - Fetch all related records at once:

```typescript
// ✅ GOOD: Single round-trip, parallel execution
const [bookmarks, shares, files] = await Promise.all([
  ctx.db.query("bookmarks").collect(),
  ctx.db.query("shares").collect(),
  ctx.db.query("files").collect(),
]);

// ❌ BAD: Sequential, 3x latency
const bookmarks = await ctx.db.query("bookmarks").collect();
const shares = await ctx.db.query("shares").collect();
const files = await ctx.db.query("files").collect();
```

**Parallel deletions** - Delete independent records simultaneously:

```typescript
// ✅ GOOD: All deletions in parallel
await Promise.all([
  ...bookmarks.map((b) => ctx.db.delete(b._id)),
  ...shares.map((s) => ctx.db.delete(s._id)),
  ...attachments.map((a) => ctx.db.delete(a._id)),
]);

// ❌ BAD: Sequential deletions
for (const b of bookmarks) await ctx.db.delete(b._id);
for (const s of shares) await ctx.db.delete(s._id);
```

**Index usage** - Always use indexed queries for related records:

```typescript
// ✅ GOOD: Uses index, fast lookup
ctx.db
  .query("messages")
  .withIndex("by_conversation", (q) => q.eq("conversationId", conversationId))
  .collect()

// ❌ BAD: Full table scan
ctx.db
  .query("messages")
  .filter((q) => q.eq(q.field("conversationId"), conversationId))
  .collect()
```

## Key Files

- `packages/backend/convex/lib/utils/cascade.ts` - Cascade delete utilities
- `packages/backend/convex/conversations.ts` - Conversation deletion
- `packages/backend/convex/users.ts` - GDPR user data deletion

## Common Patterns

**Full cascade delete**:
```typescript
await cascadeDeleteConversation(ctx, conversationId);
```

**Preserve conversation, delete messages only**:
```typescript
await cascadeDeleteConversation(ctx, conversationId, {
  deleteMessages: true,
  deleteConversation: false,
});
```

**GDPR compliance**:
```typescript
await cascadeDeleteUserData(ctx, userId); // Keeps user account
await ctx.db.delete(userId); // Full account deletion
```

## Anti-Patterns

**Don't use nested promises**:
```typescript
// ❌ BAD: Nested promises, hard to reason about
await Promise.all(
  bookmarks.map(async (b) => {
    const tags = await ctx.db.query("tags").collect();
    await ctx.db.delete(b._id);
  })
);

// ✅ GOOD: Flat structure, clear dependencies
const bookmarks = await ctx.db.query("bookmarks").collect();
const tags = await ctx.db.query("tags").collect();
await Promise.all([
  ...bookmarks.map((b) => ctx.db.delete(b._id)),
  ...tags.map((t) => ctx.db.delete(t._id)),
]);
```

**Don't skip indexes**:
```typescript
// ❌ BAD: Filter scans entire table
const messages = await ctx.db
  .query("messages")
  .filter((q) => q.eq(q.field("userId"), userId))
  .collect();

// ✅ GOOD: Index lookup, O(log n)
const messages = await ctx.db
  .query("messages")
  .withIndex("by_user", (q) => q.eq("userId", userId))
  .collect();
```

**Don't forget junction tables**:
```typescript
// ❌ BAD: Orphans projectConversations records
await ctx.db.delete(conversationId);

// ✅ GOOD: Clean up junction first
const junctions = await ctx.db
  .query("projectConversations")
  .withIndex("by_conversation", (q) => q.eq("conversationId", conversationId))
  .collect();
await Promise.all(junctions.map((j) => ctx.db.delete(j._id)));
await ctx.db.delete(conversationId);
```

**Don't delete parents before children**:
```typescript
// ❌ BAD: Orphans canvasHistory
await ctx.db.delete(doc._id);

// ✅ GOOD: Delete history first
const history = await ctx.db
  .query("canvasHistory")
  .withIndex("by_document", (q) => q.eq("documentId", doc._id))
  .collect();
await Promise.all(history.map((h) => ctx.db.delete(h._id)));
await ctx.db.delete(doc._id);
```
