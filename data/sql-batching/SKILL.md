---
name: sql-batching
description: Prevent D1 "too many SQL variables" errors when using Drizzle ORM. Use this skill whenever writing database queries with `inArray()`, bulk inserts/updates, or any query with dynamic arrays. Critical for queries where array size is unbounded (user teams, registrations, IDs from prior queries).
---

# SQL Batching Pattern

**CRITICAL: D1 has a 100 bound parameter limit per query** (NOT 999 like standard SQLite).
See: https://developers.cloudflare.com/d1/platform/limits/

Use `@/utils/batch-query.ts` utilities to batch queries.

## The 100 Parameter Limit

D1's limit is **100 bound parameters per query**, not SQLite's typical 999. This affects:
- `inArray()` queries: each ID = 1 param
- Bulk inserts: each column value = 1 param (including auto-generated columns!)
- Combined queries: all WHERE conditions + array items must be < 100

**Error message**: `D1_ERROR: too many SQL variables at offset N: SQLITE_ERROR`

## When to Batch

**Always batch when:**
- Using `inArray()` with arrays from user data or prior queries
- Array size is unbounded (team memberships, registrations, results)
- Bulk inserts with dynamic row counts
- Any operation where total params could exceed 100

**Safe to skip when:**
- Array is hardcoded/constant AND small (< 50 items to leave headroom)
- Single-row inserts
- Array has guaranteed small upper bound AND you've calculated total params

## Usage

```typescript
import { autochunk, autochunkFirst } from "@/utils/batch-query"

// findMany - returns flattened results
const results = await autochunk(
  { items: ids, otherParametersCount: 1 }, // count other WHERE params
  async (chunk) => db.query.table.findMany({
    where: and(
      eq(table.field, value), // this counts as 1 param
      inArray(table.id, chunk),
    ),
  }),
)

// findFirst - stops on first match
const result = await autochunkFirst(
  { items: ids },
  async (chunk) => db.query.table.findFirst({
    where: inArray(table.id, chunk),
  }),
)
```

## For Parallel Execution

Use `chunk()` + `Promise.all` when parallel is preferred:

```typescript
import { chunk, SQL_BATCH_SIZE } from "@/utils/batch-query"

const results = (await Promise.all(
  chunk(ids, SQL_BATCH_SIZE).map((batch) =>
    db.select().from(table).where(inArray(table.id, batch))
  )
)).flat()
```

## Parameters

- `items`: Array to batch (IDs, objects)
- `otherParametersCount`: Number of other bound params in query (eq conditions, etc.)
- `SQL_BATCH_SIZE`: 100 (D1's actual limit)

## For Bulk Inserts

For bulk inserts, Drizzle includes ALL columns (including auto-generated ones). You MUST count every column in the table schema, not just the fields you're explicitly setting.

### Counting Columns

Check the table schema and count:
1. `commonColumns` (if used): `createdAt`, `updatedAt`, `updateCounter` = 3 columns
2. All explicit columns: `id`, `fieldA`, `fieldB`, etc.
3. Even nullable columns without defaults get a param (Drizzle sends `null`)

### Calculate Batch Size

```typescript
// Formula: floor(100 / totalColumns)
// Always subtract 1-2 for safety margin

// Example: judgeHeatAssignmentsTable has 12 columns
// commonColumns (3) + id, heatId, membershipId, rotationId, versionId, 
// laneNumber, position, instructions, isManualOverride (9) = 12 total
// Max rows: floor(100 / 12) = 8 rows
const INSERT_BATCH_SIZE = 8

const chunks: Item[][] = []
for (let i = 0; i < items.length; i += INSERT_BATCH_SIZE) {
  chunks.push(items.slice(i, i + INSERT_BATCH_SIZE))
}

for (const chunk of chunks) {
  await db.insert(table).values(chunk.map(item => ({ ... })))
}
```

### Real-World Examples from Codebase

| Table | Columns | Max Batch Size |
|-------|---------|----------------|
| `judgeHeatAssignmentsTable` | 12 | 8 rows |
| `competitionHeatsTable` | 12 | 8 rows |
| `workoutMovements` | 6 | 16 rows |
| `scoreRoundsTable` | 9 | 11 rows |

### Common Gotchas

1. **Don't trust old comments**: Previous code assumed 999 limit - always verify
2. **Nullable columns still count**: Even if you don't set them, Drizzle may send `null`
3. **Auto-generated columns count**: `$defaultFn()` columns still use a param slot
4. **The error is cryptic**: `too many SQL variables at offset N` means you hit 100

### Debugging

If you hit the limit, count params in the SQL output:
```
Query: insert into "table" ("col1", "col2", ...) values (?, ?, ...), (?, ?, ...)
```
Count the `?` marks - that's your actual param count.
