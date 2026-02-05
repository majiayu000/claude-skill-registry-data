---
name: database-management
description: Specialized skill for database operations with Drizzle ORM and Neon PostgreSQL. Use when working with schema definitions, queries, migrations, or database optimization.
---

# Database Management Skill

This skill provides expertise in managing the Artiefy database using Drizzle ORM with Neon PostgreSQL.

## When to Use This Skill

- Creating or modifying database schemas
- Writing complex queries or transactions
- Running migrations and schema changes
- Optimizing query performance
- Setting up new database connections

## Key Technologies

- **Drizzle ORM**: Type-safe SQL queries and schema definitions
- **Neon PostgreSQL**: Serverless PostgreSQL database
- **Migrations**: Version-controlled schema changes

## Patterns and Conventions

### Schema Definition

- Schemas in `drizzle/` directory
- Use Drizzle's schema API with proper types
- Define relations and constraints

### Queries

- Place in `src/server/queries/`
- Use prepared statements for performance
- Handle transactions for multi-step operations

### Migrations

- Run `npm run db:generate` to create migrations
- Run `npm run db:migrate` to apply changes
- Use `npm run db:studio` for visual schema management

## Examples

### Schema Definition

```ts
// drizzle/schema.ts
import { pgTable, serial, text, timestamp } from 'drizzle-orm/pg-core';

export const users = pgTable('users', {
  id: serial('id').primaryKey(),
  name: text('name').notNull(),
  email: text('email').notNull().unique(),
  createdAt: timestamp('created_at').defaultNow(),
});
```

### Query with Drizzle

```ts
// src/server/queries/getUsers.ts
import { db } from '@/server/db';
import { users } from '@/drizzle/schema';

export async function getUsers() {
  return await db.select().from(users);
}
```

### Migration Script

```sql
-- migrations/001_create_users.sql
CREATE TABLE users (
  id SERIAL PRIMARY KEY,
  name TEXT NOT NULL,
  email TEXT NOT NULL UNIQUE,
  created_at TIMESTAMP DEFAULT NOW()
);
```

## Performance Optimization

- Use indexes on frequently queried columns
- Implement connection pooling with Neon
- Monitor slow queries with `EXPLAIN ANALYZE`

## Resources

- [Drizzle Documentation](https://orm.drizzle.team/)
- [Neon Documentation](https://neon.tech/docs)
- Project config: `drizzle.config.ts`
- Environment: `src/env.ts`
