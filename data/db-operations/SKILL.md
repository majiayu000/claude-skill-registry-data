---
name: db-operations
description: PostgreSQL database operations specialist using Drizzle ORM for schema management, queries, and migrations
---

# Database Operations Specialist

## Instructions
When working with PostgreSQL and Drizzle ORM:

1. **Schema Management**
   - Define tables in `src/db/schema.ts`
   - Use `npm run db:generate` to create migrations
   - Apply migrations with `npm run db:migrate`
   - Use `npm run db:push` for quick schema updates

2. **Database Queries**
   - Import `db` from `src/db`
   - Use Drizzle's select() with table references
   - Implement proper joins for related data
   - Add indexes for performance optimization

3. **User Preferences**
   - Use `user_preferences` table for liked content
   - Use `user_dislikes` for content to exclude
   - Use `user_people` for favorite actors/directors
   - Always include user ID in queries

4. **Performance**
   - Add indexes on frequently queried columns
   - Use `explain()` to analyze query performance
   - Implement pagination for large result sets
   - Consider caching for frequently accessed data

## Examples

**Creating a new table:**
```typescript
import { pgTable, serial, text, timestamp } from 'drizzle-orm/pg-core'

export const newTable = pgTable('new_table', {
  id: serial('id').primaryKey(),
  name: text('name').notNull(),
  createdAt: timestamp('created_at').defaultNow(),
})
```

**Querying user preferences:**
```typescript
import { db, userPreferences } from '@/db'
import { eq } from 'drizzle-orm'

const preferences = await db.select()
  .from(userPreferences)
  .where(eq(userPreferences.userId, userId))
```

**Running migration:**
```bash
npm run db:generate  # Generate migration file
npm run db:migrate   # Apply migration
npm run db:studio    # Open Drizzle Studio
```