---
name: stripe-migration-pattern
description: Resumable zero-downtime migrations for Convex schema changes. 6-phase pattern with checkpoint tracking, cursor-based backfill, dual-write transitions. Triggers on "migration", "backfill", "resumable", "checkpoint", "dual-write".
---

# Stripe Migration Pattern

Zero-downtime migrations for large Convex datasets. Stripe-inspired 6-phase pattern with resumability.

## Core Pattern: 6 Phases

```
1. SCHEMA    → Add new tables, keep old fields optional
2. BACKFILL  → Migrate existing data (cursor-based, resumable)
3. DUAL-WRITE → Write to both old + new locations
4. DUAL-READ  → Read from new first, fallback to old
5. CLEANUP    → Remove old data from documents
6. COMPLETE   → Remove old fields from schema
```

**Critical**: Wait 7-30 days between phases 5 and 6 for rollback safety.

## Migration State Tracking

Track progress in `migrations` table:

```typescript
// From convex/schema.ts:1290-1332
migrations: defineTable({
  migrationId: v.string(),
  name: v.string(),
  phase: v.union(
    v.literal("schema"),
    v.literal("backfill"),
    v.literal("dual-write"),
    v.literal("dual-read"),
    v.literal("cleanup"),
    v.literal("complete")
  ),
  status: v.union(
    v.literal("pending"),
    v.literal("running"),
    v.literal("completed"),
    v.literal("failed"),
    v.literal("rolled-back")
  ),
  checkpoint: v.optional(
    v.object({
      cursor: v.optional(v.string()),
      processedCount: v.number(),
      successCount: v.number(),
      errorCount: v.number(),
      lastProcessedId: v.optional(v.string()),
    })
  ),
  processedRecords: v.number(),
  startedAt: v.optional(v.number()),
  completedAt: v.optional(v.number()),
})
  .index("by_migration_id", ["migrationId"])
  .index("by_status", ["status"])
```

## Cursor-Based Backfill Pattern

Handles millions of records, survives 10min Convex action timeout.

```typescript
// From convex/migrations/001_normalize_message_attachments.ts:18-148
export const backfillBatch = internalMutation({
  args: {
    cursor: v.union(v.string(), v.null()),
    batchSize: v.number(),
  },
  handler: async (ctx, { cursor, batchSize }) => {
    // Paginate with cursor (NOT offset - doesn't scale)
    const result = await ctx.db
      .query("messages")
      .order("desc")
      .paginate({ cursor, numItems: batchSize });

    let attachmentsCreated = 0;

    for (const msg of result.page) {
      // Skip if already migrated (idempotent)
      const existing = await ctx.db
        .query("attachments")
        .withIndex("by_message", (q) => q.eq("messageId", msg._id))
        .first();

      if (existing) {
        continue;
      }

      // Migrate attachments
      if ((msg as any).attachments?.length) {
        for (const att of (msg as any).attachments) {
          await ctx.db.insert("attachments", {
            messageId: msg._id,
            conversationId: msg.conversationId,
            userId: msg.userId!,
            type: att.type,
            storageId: att.storageId as Id<"_storage">,
            // ... more fields
            createdAt: msg.createdAt,
          });
          attachmentsCreated++;
        }
      }
    }

    // Update checkpoint after each batch
    await ctx.db
      .query("migrations")
      .withIndex("by_migration_id", (q) => q.eq("migrationId", MIGRATION_ID))
      .first()
      .then(async (migration) => {
        if (migration) {
          await ctx.db.patch(migration._id, {
            processedRecords: migration.processedRecords + result.page.length,
            checkpoint: {
              cursor: result.continueCursor,
              processedCount: migration.processedRecords + result.page.length,
              successCount: (migration.checkpoint?.successCount || 0) + attachmentsCreated,
              errorCount: migration.checkpoint?.errorCount || 0,
              lastProcessedId: result.page[result.page.length - 1]?._id,
            },
            updatedAt: Date.now(),
          });
        }
      });

    return {
      done: result.isDone,
      nextCursor: result.continueCursor,
      processed: result.page.length,
      attachmentsCreated,
    };
  },
});
```

**Key points**:
- Use `.paginate()` with cursor, NOT offset
- Make idempotent (check if already migrated)
- Update checkpoint after each batch
- Return cursor for next batch

## Orchestrator Action Pattern

Loops through batches until done. Survives timeout by resuming from checkpoint.

```typescript
// From convex/migrations/001_normalize_message_attachments.ts:151-244
export const migrate = internalAction({
  handler: async (ctx) => {
    const startTime = Date.now();

    // Create or resume migration record
    let migration = (await (ctx.runQuery as any)(
      // @ts-ignore - TypeScript recursion limit with 94+ Convex modules
      internal.migrations["001_normalize_message_attachments"].getMigrationState,
      {},
    )) as Doc<"migrations"> | null;

    if (!migration) {
      // Initialize new migration
      migration = (await (ctx.runMutation as any)(
        // @ts-ignore - TypeScript recursion limit
        internal.migrations["001_normalize_message_attachments"].initializeMigration,
        {},
      )) as Doc<"migrations">;
    } else if (migration.status === "completed") {
      logger.warn("Migration already completed");
      return;
    } else {
      logger.info("Resuming migration from checkpoint");
    }

    // Run backfill in batches
    let cursor: string | null = migration.checkpoint?.cursor ?? null;
    let batchCount = 0;

    do {
      const result = (await (ctx.runMutation as any)(
        // @ts-ignore - TypeScript recursion limit
        internal.migrations["001_normalize_message_attachments"].backfillBatch,
        { cursor, batchSize: 100 },
      )) as {
        done: boolean;
        nextCursor?: string;
        processed: number;
        attachmentsCreated: number;
      };

      cursor = result.nextCursor ?? null;
      batchCount++;

      logger.info("Batch processed", {
        tag: "Migration",
        batchCount,
        processed: result.processed,
      });

      if (result.done) {
        // Mark complete
        await (ctx.runMutation as any)(
          // @ts-ignore - TypeScript recursion limit
          internal.migrations["001_normalize_message_attachments"].completeMigration,
          {},
        );
        break;
      }
    } while (cursor);

    const duration = ((Date.now() - startTime) / 1000).toFixed(2);
    logger.info("Migration complete", {
      tag: "Migration",
      durationSec: duration,
    });
  },
});
```

## Helper Mutations

Always include these for state management:

```typescript
// From convex/migrations/001_normalize_message_attachments.ts:248-300
export const getMigrationState = internalQuery({
  handler: async (ctx) => {
    return await ctx.db
      .query("migrations")
      .withIndex("by_migration_id", (q) => q.eq("migrationId", MIGRATION_ID))
      .first();
  },
});

export const initializeMigration = internalMutation({
  handler: async (ctx) => {
    const id = await ctx.db.insert("migrations", {
      migrationId: MIGRATION_ID,
      name: MIGRATION_NAME,
      phase: "backfill",
      status: "running",
      processedRecords: 0,
      checkpoint: {
        processedCount: 0,
        successCount: 0,
        errorCount: 0,
      },
      startedAt: Date.now(),
      executedBy: "system",
      createdAt: Date.now(),
      updatedAt: Date.now(),
    });

    return await ctx.db.get(id);
  },
});

export const completeMigration = internalMutation({
  handler: async (ctx) => {
    const migration = await ctx.db
      .query("migrations")
      .withIndex("by_migration_id", (q) => q.eq("migrationId", MIGRATION_ID))
      .first();

    if (migration) {
      await ctx.db.patch(migration._id, {
        status: "completed",
        phase: "complete",
        completedAt: Date.now(),
        updatedAt: Date.now(),
      });
    }
  },
});
```

## Type Conversion Patterns

Handle schema changes during migration:

```typescript
// String → Id conversion
storageId: att.storageId as Id<"_storage">

// JSON parsing (old stringified → new native)
args: tc.arguments ? JSON.parse(tc.arguments) : {}

// Optional field handling
metadata: att.metadata
  ? {
      width: (att.metadata as any).width,
      height: (att.metadata as any).height,
    }
  : undefined
```

## Batch Size Guidelines

From production experience (834 messages in 6.13s = 136 msg/sec):

- **Small records**: 100-200 per batch
- **Large records**: 50-100 per batch
- **With relations**: 25-50 per batch

Adjust based on mutation complexity and document size.

## Verification Queries

Always include post-migration verification:

```typescript
// From convex/migrations/001_normalize_message_attachments.ts:303-327
export const verifyAttachments = internalQuery({
  handler: async (ctx) => {
    const attachments = await ctx.db.query("attachments").collect();
    return {
      count: attachments.length,
      sample: attachments.slice(0, 3),
    };
  },
});

export const verifyToolCalls = internalQuery({
  handler: async (ctx) => {
    const toolCalls = await ctx.db.query("toolCalls").collect();
    const byPartial = {
      complete: toolCalls.filter((tc) => !tc.isPartial).length,
      partial: toolCalls.filter((tc) => tc.isPartial).length,
    };
    return {
      total: toolCalls.length,
      byPartial,
      sample: toolCalls.slice(0, 3),
    };
  },
});
```

Run verification BEFORE moving to cleanup phase.

## Common Gotchas

### 1. Cursor Invalidation

**Problem**: Cursor invalidated if table modified during migration.

**Solution**: Run migrations during low-traffic periods. If cursor fails, migration restarts from beginning (idempotent).

### 2. Data Cleanup Required First

**Error**: `Schema validation failed: Field 'attachments' exists in documents but not in schema`

**Solution**: Two-step cleanup:
```typescript
// Step 1: Remove data
await ctx.db.patch(msg._id, {
  attachments: undefined,
  toolCalls: undefined,
});

// Step 2: Remove from schema (separate deployment)
```

### 3. TypeScript Type Depth

All migration files hit type depth limits (94+ Convex modules).

**Pattern**: Use type assertions with `@ts-ignore`:
```typescript
const result = (await (ctx.runMutation as any)(
  // @ts-ignore - TypeScript recursion limit with 94+ Convex modules
  internal.migrations.backfillBatch,
  { cursor, batchSize: 100 }
)) as { done: boolean; nextCursor?: string };
```

### 4. Race Conditions During Dual-Write

**Problem**: Concurrent updates to old + new locations.

**Solution**: Update in order:
1. New table (source of truth)
2. Old field (backward compat)

If crash occurs, new table has data. Next read uses dual-read pattern (new first, fallback to old).

## File Organization

```
convex/migrations/
├── 001_normalize_message_attachments.ts  # Main migration
├── 002_cleanup_deprecated_fields.ts      # Cleanup step
└── verify_dual_write.ts                  # Verification
```

Name migrations with numeric prefix for ordering.

## Key Reference Files

- Migration table schema: `convex/schema.ts:1290-1332`
- Real example: `convex/migrations/001_normalize_message_attachments.ts`
- Architecture doc: `docs/architecture/schema-normalization.md`
- Completed phases: `docs/migrations/phase1-complete.md`, `phase2-complete.md`

## When to Use This Pattern

**Use when**:
- Migrating 1000+ records
- Schema changes affect critical tables
- Zero downtime required
- Rollback capability needed

**Don't use when**:
- Small dataset (<100 records) - just write a simple mutation
- Dev environment - can destroy and recreate tables
- Non-breaking additive changes - just add field and populate lazily
