---
name: cloudflare-d1
description: >
  Cloudflare D1 SQLite database - prepared statements, batch operations, Drizzle ORM essentials.
  Trigger: When working with D1 database, SQLite queries, Drizzle ORM, database bindings.
license: Apache-2.0
metadata:
  author: gentleman-programming
  version: "1.0"
---

## Critical Patterns

### Setup Binding

```toml
# wrangler.toml
[[d1_databases]]
binding = "DB"
database_name = "my-database"
database_id = "your-database-id"
```

```typescript
export interface Env {
  DB: D1Database
}
```

### Prepared Statements (REQUIRED)

```typescript
// ✅ ALWAYS use prepared statements
const stmt = env.DB.prepare(
  "SELECT * FROM Users WHERE email = ?"
).bind(userEmail)

const result = await stmt.first()

// ❌ NEVER do this - SQL injection!
const result = await env.DB.prepare(
  `SELECT * FROM Users WHERE email = '${userEmail}'`
).run()
```

### Return Methods

```typescript
// INSERT/UPDATE/DELETE
const result = await env.DB.prepare(
  "INSERT INTO Users (name, email) VALUES (?, ?)"
).bind("John", "john@example.com").run()

console.log(result.meta.last_row_id)   // New ID
console.log(result.meta.rows_written)  // Rows affected

// SELECT all rows
const { results } = await env.DB.prepare(
  "SELECT * FROM Users"
).all()

// SELECT single row
const user = await env.DB.prepare(
  "SELECT * FROM Users WHERE id = ?"
).bind(userId).first()

// SELECT single value
const count = await env.DB.prepare(
  "SELECT COUNT(*) as total FROM Users"
).first("total")
```

### Batch Operations

```typescript
// All succeed or all fail (atomic)
const [userResult, ordersResult] = await env.DB.batch([
  env.DB.prepare("SELECT * FROM Users WHERE id = ?").bind(1),
  env.DB.prepare("SELECT * FROM Orders WHERE user_id = ?").bind(1)
])

// Bulk inserts
await env.DB.batch([
  env.DB.prepare("INSERT INTO Users (name) VALUES (?)").bind("User 1"),
  env.DB.prepare("INSERT INTO Users (name) VALUES (?)").bind("User 2"),
  env.DB.prepare("INSERT INTO Users (name) VALUES (?)").bind("User 3")
])
```

### Drizzle ORM

```typescript
import { drizzle } from 'drizzle-orm/d1'
import { sqliteTable, text, integer } from 'drizzle-orm/sqlite-core'
import { eq } from 'drizzle-orm'

// Define schema
export const users = sqliteTable('users', {
  id: integer('id').primaryKey({ autoIncrement: true }),
  name: text('name').notNull(),
  email: text('email').notNull().unique(),
  createdAt: integer('created_at', { mode: 'timestamp' })
})

// Use in worker
export default {
  async fetch(request: Request, env: Env) {
    const db = drizzle(env.DB)
    
    // SELECT
    const allUsers = await db.select().from(users).all()
    const activeUsers = await db.select().from(users)
      .where(eq(users.active, true))
      .all()
    
    // INSERT
    const newUser = await db.insert(users).values({
      name: "John Doe",
      email: "john@example.com",
      createdAt: new Date()
    }).returning()
    
    // UPDATE
    await db.update(users)
      .set({ name: "Jane Doe" })
      .where(eq(users.id, userId))
    
    // DELETE
    await db.delete(users).where(eq(users.id, userId))
    
    return Response.json(allUsers)
  }
}
```

## Performance Tips

```typescript
// ✅ Batch queries (single round trip)
const [user, orders] = await env.DB.batch([
  env.DB.prepare("SELECT * FROM Users WHERE id = ?").bind(1),
  env.DB.prepare("SELECT * FROM Orders WHERE user_id = ?").bind(1)
])

// ❌ Multiple queries (slow)
const user = await env.DB.prepare("SELECT * FROM Users WHERE id = ?").bind(1).first()
const orders = await env.DB.prepare("SELECT * FROM Orders WHERE user_id = ?").bind(1).all()

// ✅ Use .first() for single rows
const user = await env.DB.prepare("SELECT * FROM Users WHERE id = ?").bind(1).first()

// ❌ Wasteful
const users = await env.DB.prepare("SELECT * FROM Users WHERE id = ?").bind(1).all()
const user = users.results[0]

// ✅ Always LIMIT large queries
const users = await env.DB.prepare(
  "SELECT * FROM Users ORDER BY created_at DESC LIMIT 100"
).all()
```

## Error Handling

```typescript
try {
  const user = await env.DB.prepare(
    "SELECT * FROM Users WHERE id = ?"
  ).bind(userId).first()
  
  if (!user) {
    return new Response("User not found", { status: 404 })
  }
  
  return Response.json(user)
} catch (error) {
  console.error("Database error:", error)
  return new Response("Database error", { status: 500 })
}
```

## Commands

```bash
# Create database
wrangler d1 create my-database

# Execute SQL
wrangler d1 execute my-database --local --command="SELECT * FROM Users"

# Drizzle migrations
pnpm drizzle-kit generate
pnpm drizzle-kit push
pnpm drizzle-kit studio
```

## Resources

- **Docs**: [developers.cloudflare.com/d1](https://developers.cloudflare.com/d1)
- **Drizzle**: [orm.drizzle.team](https://orm.drizzle.team)
