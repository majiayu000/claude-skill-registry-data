---
name: database-optimizer
version: "2.0"
trigger: database optimization, query performance, index tuning, PostgreSQL
description: Database optimization, query tuning, indexing strategies, migration management, and performance monitoring for PostgreSQL with Drizzle ORM. Use when optimizing slow queries, designing schemas, creating migrations, or setting up database monitoring.
---

# Database Optimizer

## Query Optimization

### Index Strategies
```typescript
// Add index for frequent queries
export const users = pgTable('users', {
  id: uuid('id').primaryKey(),
  email: varchar('email', { length: 255 }).notNull().unique(),
  tier: integer('tier').notNull().default(1),
  createdAt: timestamp('created_at').defaultNow(),
}, (table) => ({
  emailIdx: index('email_idx').on(table.email),
  tierIdx: index('tier_idx').on(table.tier),
  createdAtIdx: index('created_at_idx').on(table.createdAt),
}));
```

### Composite Indexes
```typescript
export const agentExecutions = pgTable('agent_executions', {
  userId: uuid('user_id').references(() => users.id),
  agentId: varchar('agent_id', { length: 100 }),
  status: varchar('status', { length: 50 }),
  createdAt: timestamp('created_at'),
}, (table) => ({
  // Composite index for common query pattern
  userAgentIdx: index('user_agent_idx').on(table.userId, table.agentId),
  // Partial index for active executions
  activeIdx: index('active_idx').on(table.createdAt).where(eq(table.status, 'running')),
}));
```

## Query Patterns

### Efficient Joins
```typescript
// Use select instead of include for specific fields
const usersWithPosts = await db
  .select({
    user: { id: users.id, name: users.name },
    postCount: count(posts.id),
    lastPost: max(posts.createdAt)
  })
  .from(users)
  .leftJoin(posts, eq(users.id, posts.authorId))
  .groupBy(users.id);
```

### Pagination with Cursor
```typescript
async function getPaginatedResults(cursor?: string) {
  return db
    .select()
    .from(posts)
    .where(cursor ? lt(posts.createdAt, cursor) : undefined)
    .orderBy(desc(posts.createdAt))
    .limit(20);
}
```

## Migration Management

### Safe Migrations
```typescript
// Always make migrations reversible
export async function up(db: DB) {
  await db.schema
    .alterTable('users')
    .addColumn('tier', 'integer', (col) => col.defaultTo(1))
    .execute();
    
  // Backfill data
  await db.updateTable('users')
    .set({ tier: 1 })
    .where('tier', 'is', null)
    .execute();
}

export async function down(db: DB) {
  await db.schema
    .alterTable('users')
    .dropColumn('tier')
    .execute();
}
```

## Protocol

1. **Assess** — Understand the specific requirement and context
2. **Plan** — Determine the approach based on the guidance above
3. **Execute** — Apply the database optimizer methodology
4. **Verify** — Validate the output against expected standards
5. **Report** — Document results and any issues encountered
