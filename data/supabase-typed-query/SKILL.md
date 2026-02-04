---
name: supabase-typed-query
description: Help developers use supabase-typed-query for type-safe Supabase queries. Use this skill when building queries with the Query API, working with Entity/PartitionedEntity patterns, handling TaskOutcome errors, or implementing soft deletes and multi-tenancy.
---

# supabase-typed-query User Guide

## Overview

supabase-typed-query is a type-safe query builder and entity pattern library for Supabase. It provides:

- Fully typed queries leveraging your database schema
- Two complementary APIs: Query API (functional, chainable) and Entity API (CRUD patterns)
- Built on functype for robust error handling with `TaskOutcome`
- Support for soft deletes, multi-tenancy, and complex queries with OR conditions

## When to Use This Skill

Trigger this skill when users:

- Build queries using `query()` function
- Work with `Entity()` or `PartitionedEntity()` patterns
- Handle `TaskOutcome` or use `OrThrow` methods
- Implement soft deletes or multi-tenancy
- Look up comparison operators or API methods
- Debug query issues

## Quick Start

### Installation

```bash
npm install supabase-typed-query
# or
pnpm add supabase-typed-query
```

### Generate Database Types

```bash
npx supabase gen types typescript --project-id your-project-id > database.types.ts
```

### Core Imports

```typescript
import { query, Entity, PartitionedEntity } from "supabase-typed-query"
import { createClient } from "@supabase/supabase-js"
import type { Database } from "./database.types"

const client = createClient<Database>(url, key)
```

## Query API

The Query API provides chainable, functional queries with OR support.

### Basic Query

```typescript
import { query } from "supabase-typed-query"

// Simple query with type-safe conditions
const user = await query<"users", Database>(client, "users", { id: "123" }).oneOrThrow()

// Query with comparison operators
const recentPosts = await query<"posts", Database>(client, "posts", {
  created_at: { gte: new Date("2024-01-01") },
}).manyOrThrow()
```

### OR Chaining

```typescript
// Multiple OR conditions
const results = await query<"users", Database>(client, "users", { role: "admin" })
  .or({ role: "moderator" })
  .or({ role: "editor", active: true })
  .manyOrThrow()
// SQL: WHERE role = 'admin' OR role = 'moderator' OR (role = 'editor' AND active = true)
```

### Functional Operations

```typescript
// Map: transform each result
const titles = await query<"posts", Database>(client, "posts", { status: "published" })
  .map((post) => post.title)
  .manyOrThrow()

// Filter: client-side filtering after fetch
const activeUsers = await query<"users", Database>(client, "users", {})
  .filter((user) => user.active === true && user.age > 18)
  .manyOrThrow()

// Chain map + filter
const adultNames = await query<"users", Database>(client, "users", {})
  .filter((user) => user.age >= 18)
  .map((user) => user.name)
  .manyOrThrow()
```

### Execution Methods

| Method            | Returns                  | Description                  |
| ----------------- | ------------------------ | ---------------------------- |
| `.one()`          | `TaskOutcome<Option<T>>` | Expects 0-1 results          |
| `.many()`         | `TaskOutcome<List<T>>`   | Expects 0+ results           |
| `.first()`        | `TaskOutcome<Option<T>>` | Gets first if multiple       |
| `.oneOrThrow()`   | `Promise<T>`             | Throws if not found or error |
| `.manyOrThrow()`  | `Promise<List<T>>`       | Throws on error              |
| `.firstOrThrow()` | `Promise<T>`             | Throws if not found or error |

### Comparison Operators

```typescript
type ComparisonOperators<V> = {
  gte?: V // Greater than or equal
  gt?: V // Greater than
  lte?: V // Less than or equal
  lt?: V // Less than
  neq?: V // Not equal (use NOT operator for null)
  like?: string // LIKE pattern
  ilike?: string // Case-insensitive LIKE
  in?: V[] // IN array
  is?: null | boolean // IS NULL/TRUE/FALSE
}

// Examples
const results = await query<"posts", Database>(client, "posts", {
  view_count: { gte: 100, lte: 1000 },
  title: { ilike: "%guide%" },
  tags: { in: ["typescript", "supabase"] },
  published_at: { is: null }, // Find unpublished
}).manyOrThrow()
```

### NOT Operator

The `not` operator follows Supabase conventions for negating IS and IN conditions:

```typescript
// IS NOT NULL - find posts with external_id set
const linkedPosts = await query<"posts", Database>(client, "posts", {
  not: { is: { external_id: null } },
}).manyOrThrow()

// IS NOT TRUE / IS NOT FALSE
const nonFeatured = await query<"posts", Database>(client, "posts", {
  not: { is: { featured: true } },
}).manyOrThrow()

// NOT IN - exclude specific values
const activePosts = await query<"posts", Database>(client, "posts", {
  not: { in: { status: ["draft", "archived", "spam"] } },
}).manyOrThrow()

// Entity API supports NOT as well
const items = await PostEntity.getItems({
  where: { status: "published" },
  not: { is: { external_id: null } },
}).manyOrThrow()
```

> **Note**: `neq: null` is deprecated. Use `not: { is: { field: null } }` instead for IS NOT NULL checks.

## RPC (Stored Procedures)

The `rpc()` function provides type-safe invocation of PostgreSQL functions/stored procedures.

### Basic RPC Call

```typescript
import { rpc } from "supabase-typed-query"

// Call a function that returns a single value
const stats = await rpc<"get_user_stats", Database>(client, "get_user_stats", {
  user_id: "123",
}).oneOrThrow()

// Call a function that returns multiple rows
const results = await rpc<"search_products", Database>(client, "search_products", {
  query: "laptop",
  limit: 10,
}).manyOrThrow()
```

### RPC Execution Methods

| Method           | Returns                  | Description                   |
| ---------------- | ------------------------ | ----------------------------- |
| `.one()`         | `TaskOutcome<Option<T>>` | Expects single result or none |
| `.many()`        | `TaskOutcome<List<T>>`   | Expects 0+ results as a list  |
| `.oneOrThrow()`  | `Promise<T>`             | Throws if not found or error  |
| `.manyOrThrow()` | `Promise<List<T>>`       | Throws on error               |

### RPC with Options

```typescript
// With count option for pagination info
const results = await rpc<"search_items", Database>(
  client,
  "search_items",
  { query: "test" },
  { count: "exact" },
).manyOrThrow()
```

### Type Safety

RPC return types are inferred from your database schema. Your Database type should include Functions definitions:

```typescript
interface Database {
  public: {
    Tables: {
      /* ... */
    }
    Functions: {
      get_user_stats: {
        Args: { user_id: string }
        Returns: { total: number; active: number }
      }
      search_products: {
        Args: { query: string; limit?: number }
        Returns: { id: string; name: string; price: number }[]
      }
    }
  }
}
```

### Error Handling with RPC

```typescript
// Using TaskOutcome
const result = await rpc<"risky_function", Database>(client, "risky_function", {}).one()

if (result.isOk()) {
  const maybeData = result.orThrow()
  if (maybeData.isSome()) {
    console.log("Data:", maybeData.orElse(null))
  }
} else {
  console.error("RPC failed:", result.error)
}

// Using OrThrow
try {
  const data = await rpc<"risky_function", Database>(client, "risky_function", {}).oneOrThrow()
} catch (error) {
  console.error("Error:", error)
}
```

## Entity API

The Entity API provides consistent CRUD patterns.

### Standard Entity

```typescript
import { Entity } from "supabase-typed-query"

const PostEntity = Entity<"posts", Database>(client, "posts", { softDelete: true })

// Get single item
const post = await PostEntity.getItem({ id: "123" }).oneOrThrow()

// Get multiple items
const posts = await PostEntity.getItems({
  where: { status: "published" },
  order: ["created_at", { ascending: false }],
}).manyOrThrow()

// Add items
const created = await PostEntity.addItems({
  items: [{ title: "New Post", status: "draft" }],
}).executeOrThrow()

// Update single item
const updated = await PostEntity.updateItem({
  where: { id: "123" },
  data: { status: "published" },
}).executeOrThrow()

// Update multiple items
const bulkUpdated = await PostEntity.updateItems({
  where: { status: "draft" },
  data: { status: "archived" },
}).executeOrThrow()

// Upsert items
const upserted = await PostEntity.upsertItems({
  items: [{ id: "123", title: "Updated Title" }],
  identity: "id",
}).executeOrThrow()

// Delete single item (soft delete when softDelete: true)
const deleted = await PostEntity.deleteItem({
  where: { id: "123" },
}).executeOrThrow()

// Delete multiple items
const deletedMany = await PostEntity.deleteItems({
  where: { status: "archived" },
}).executeOrThrow()
```

**Note:** When `softDelete: true`, delete methods set the `deleted` timestamp instead of physically removing rows. When `softDelete: false`, rows are permanently removed.

### PartitionedEntity (Multi-Tenancy)

```typescript
import { PartitionedEntity } from "supabase-typed-query"

const TenantPostEntity = PartitionedEntity<"posts", string, Database>(client, "posts", {
  partitionField: "tenant_id",
  softDelete: true,
})

// All queries automatically include partition filter
const tenantPosts = await TenantPostEntity.getItems(tenantId, {
  where: { status: "published" },
}).manyOrThrow()
// SQL: WHERE tenant_id = 'tenantId' AND status = 'published' AND deleted IS NULL
```

### ViewEntity (Read-Only Views)

Database views are read-only in Supabase and only have a `Row` type (no `Insert` or `Update`). Use `ViewEntity` for type-safe querying of views.

```typescript
import { ViewEntity } from "supabase-typed-query"

// Create a read-only view entity
const AuthUsersView = ViewEntity<"auth_users_view", Database, "agent_gate">(client, "auth_users_view", {
  schema: "agent_gate",
})

// Query the view - only getItem and getItems are available
const user = await AuthUsersView.getItem({ id: "123" }).oneOrThrow()
const activeUsers = await AuthUsersView.getItems({
  where: { is_active: true },
  order: ["created_at", { ascending: false }],
}).manyOrThrow()
```

**Key differences from Entity:**

- Only `getItem()` and `getItems()` methods available (no write operations)
- No `softDelete` configuration (views are read-only snapshots)
- Uses `ViewNames` and `ViewRow` types instead of `TableNames` and `TableRow`

### PartitionedViewEntity (Multi-Tenant Views)

For views that require partition-based access control:

```typescript
import { PartitionedViewEntity } from "supabase-typed-query"

const TenantStatsView = PartitionedViewEntity<"tenant_stats_view", string, Database>(client, "tenant_stats_view", {
  partitionField: "tenant_id",
})

// Partition key is required for all queries
const stats = await TenantStatsView.getItems(tenantId, {
  where: { period: "monthly" },
}).manyOrThrow()
```

## Error Handling

### TaskOutcome Pattern (Explicit)

```typescript
import { Ok, Err } from "functype"

const result = await query<"users", Database>(client, "users", { id: userId }).one()

if (result.isOk()) {
  const maybeUser = result.getOrThrow() // Option<User>
  if (maybeUser.isSome()) {
    const user = maybeUser.getOrThrow()
    console.log(user)
  }
} else {
  console.error("Query failed:", result.error)
}
```

### OrThrow Methods (Simple)

```typescript
try {
  const user = await query<"users", Database>(client, "users", { id: userId }).oneOrThrow()
  console.log("User:", user)
} catch (error) {
  if (error instanceof SupabaseError) {
    console.log(error.code) // PostgreSQL error code
    console.log(error.details) // Additional details
    console.log(error.hint) // Hint for fixing
  }
}
```

## Custom Schema Support

PostgreSQL supports multiple schemas beyond the default `public` schema. Both Entity and Query APIs support querying from custom schemas.

### Entity with Custom Schema

```typescript
// Query from a custom schema (e.g., "inventory" schema)
const InventoryEntity = Entity<"items", Database>(client, "items", {
  softDelete: false,
  schema: "inventory", // Uses client.schema("inventory").from("items")
})

// All queries will target the "inventory" schema
const items = await InventoryEntity.getItems({ where: { active: true } }).manyOrThrow()
```

### PartitionedEntity with Custom Schema

```typescript
// Multi-tenant data in a custom schema
const TenantItemsEntity = PartitionedEntity<"items", string, Database>(client, "items", {
  partitionField: "tenant_id",
  softDelete: true,
  schema: "tenant_data", // Custom schema
})

// Queries target the custom schema with partition filter
const items = await TenantItemsEntity.getItems(tenantId).manyOrThrow()
```

### Query API with Custom Schema

```typescript
import { query } from "supabase-typed-query"

// Use the 7th parameter for schema
const results = await query<"items", Database>(
  client,
  "items",
  { active: true },
  undefined, // is conditions
  undefined, // wherein conditions
  undefined, // order
  "inventory", // schema
).manyOrThrow()
```

### Default Behavior

- If no schema is specified, queries use the default `public` schema (via `client.from()`)
- When a schema is specified, queries use `client.schema(name).from(table)`

## Soft Delete

### Configuration

The `softDelete` configuration affects both queries AND delete operations:

```typescript
// Entity with soft deletes enabled
const UserEntity = Entity<"users", Database>(client, "users", { softDelete: true })
// - Queries automatically filter: WHERE deleted IS NULL
// - deleteItem/deleteItems set deleted timestamp (soft delete)

// Entity without soft deletes
const AllUsersEntity = Entity<"users", Database>(client, "users", { softDelete: false })
// - Queries include all records (no automatic filtering)
// - deleteItem/deleteItems permanently remove rows (hard delete)
```

### Per-Query Override

```typescript
// Override for specific queries
const allUsers = await UserEntity.getItems().includeDeleted().many()
const deletedOnly = await UserEntity.getItems().onlyDeleted().many()
const activeOnly = await UserEntity.getItems().excludeDeleted().many()

// Works with query() too
const all = await query<"users", Database>(client, "users", {}).includeDeleted().many()
```

## Common Patterns

### Safe Data Fetching

```typescript
import { Option } from "functype"

async function getUserEmail(userId: string): Promise<Option<string>> {
  const result = await query<"users", Database>(client, "users", { id: userId }).one()
  return result.map((maybeUser) => maybeUser.flatMap((user) => Option(user.email))).orElse(Option.none())
}
```

### Batch Operations

```typescript
// Add multiple items
const posts = await PostEntity.addItems({
  items: [
    { title: "Post 1", status: "draft" },
    { title: "Post 2", status: "draft" },
  ],
}).executeOrThrow()

// Update all matching items
const archived = await PostEntity.updateItems({
  where: { status: "draft" },
  data: { status: "archived" },
}).executeOrThrow()
```

### Complex Queries

```typescript
// Combining operators
const results = await query<"posts", Database>(client, "posts", {
  created_at: { gte: startDate, lte: endDate },
  status: { in: ["published", "featured"] },
  view_count: { gt: 100 },
})
  .or({ is_pinned: true })
  .limit(20)
  .manyOrThrow()
```

## Debugging Tips

### Common Issues

**"Type 'X' is not assignable to type 'Y'"**

- Ensure you're passing the Database type as a generic: `query<"users", Database>(...)`
- Check that your database types are up-to-date with `npx supabase gen types`

**"Property 'X' does not exist"**

- Verify table name matches your database schema
- Regenerate types if you've added new columns

**Empty results when expecting data**

- Check soft delete configuration: `{ softDelete: true }` filters out deleted records
- Use `.includeDeleted()` to see all records

**OrThrow throwing unexpectedly**

- Use explicit `TaskOutcome` methods (`.one()`, `.many()`) for debugging
- Check `result.isOk()` and inspect `result.error` for details

## Resources

### references/

- `quick-reference.md` - API cheat sheet
- `common-patterns.md` - Usage patterns and recipes

### External Links

- **GitHub**: https://github.com/jordanburke/supabase-typed-query
- **NPM**: https://www.npmjs.com/package/supabase-typed-query
- **functype**: https://github.com/jordanburke/functype
