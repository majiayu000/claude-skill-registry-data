---
name: sql-orm-safety
description: Prevents ambiguous column errors and silent data bugs from raw SQL in ORM templates.
---

# SQL ORM Safety Skill

## Problem it solves

ORMs like Drizzle, Sequelize, and TypeORM let you write raw SQL inside template literals. When these fragments appear in subqueries or complex joins, the developer must manually qualify all column references — the ORM can't resolve unqualified column names in raw SQL context. This creates ambiguous column errors that are invisible during development (single-table queries work fine) and only appear when joins or subqueries involve multiple tables with overlapping column names like `id`, `name`, or `created_at`.

## Detection triggers

Activate when:
- Error says `ambiguous column name: <column>` in a query using ORM raw SQL
- Using `sql()` template literals (Drizzle), `sequelize.literal()`, or `QueryInterface.sequelize.literal()`
- A query works on one table but breaks after adding a second table with shared column names
- Raw SQL returns unexpected data after adding a new table or join
- ORM aggregates produce wrong results when nested inside larger queries

## Protocol

### 1. Identify raw SQL in ORM templates

Search for raw SQL patterns in the codebase:
```bash
# Drizzle
grep -rn "sql\`" src/ --include="*.ts"

# Sequelize
grep -rn "\.literal(" src/ --include="*.ts"

# TypeORM
grep -rn "createQueryBuilder\|\.query(" src/ --include="*.ts"
```

### 2. Check for missing table qualifiers

In any raw SQL fragment that references columns from multiple tables, every column must be qualified:
```sql
-- BAD — ambiguous when joined
SELECT id, name, total FROM (SELECT ...)

-- GOOD — fully qualified
SELECT inventory.id, inventory.name, SUM(stock_movements.quantity) AS total
FROM inventory
JOIN stock_movements ON stock_movements.inventory_id = inventory.id
```

### 3. Replace correlated subqueries with separate aggregates

ORM `sql()` template fragments inside subqueries require manual qualification of every column reference. Instead of embedding complex subqueries, run separate queries and join in application code:
```typescript
// BAD — sql() template strips table qualification inside subquery
const items = await db.select({
  id: inventory.id,
  totalSpend: sql`(SELECT SUM(amount) FROM purchases WHERE purchases.inventory_id = ${inventory.id})`
}).from(inventory);

// GOOD — separate aggregate query + Map join
const spends = await db.select({
  inventoryId: purchases.inventoryId,
  total: sql<number>`SUM(${purchases.amount})`
}).from(purchases).groupBy(purchases.inventoryId);

const spendMap = new Map(spends.map(s => [s.inventoryId, s.total]));
const items = await db.select().from(inventory);
// Join in application code
```

### 4. Verify with a multi-table smoke test

After fixing, test with a query that joins the tables involved:
```sql
-- This should NOT produce "ambiguous column name"
SELECT * FROM table_a JOIN table_b ON table_a.id = table_b.ref_id;
```

If it crashes, there are still unqualified columns.

### 5. Watch for legacy NOT NULL columns

When adding a foreign key to an existing table, legacy display columns (e.g., `purchases.supplier` as text) remain `NOT NULL`. Every insert/update must backfill the legacy column from the new FK:
```typescript
// When creating with supplierId, also populate legacy supplier column
const supplier = await db.query.suppliers.findFirst({
  where: eq(suppliers.id, input.supplierId)
});
await db.insert(purchases).values({
  ...input,
  supplier: supplier.name,  // backfill legacy NOT NULL column
});
```

## When NOT to use

- Simple single-table queries with no joins
- ORM methods that handle qualification automatically (`.select()`, `.where()`)
- Read-only queries against views with pre-qualified columns

## Cross-references

- **safe-code-modifications** — When adding FKs, verify legacy columns are backfilled before removing old code paths.
- **debugging-and-error-recovery** — Apply structured debugging when ambiguous column errors appear in production but not development.

## Lessons learned

Real bugs caught by this skill:
1. Raw SQL fragments in ORM subqueries require manual column qualification — missing qualifiers cause "ambiguous column name" errors only after adding a second table
2. Legacy `NOT NULL` display columns must be backfilled from new FK on every write path — missing one creates constraint violations
3. Separate aggregate queries + application-code Map joins are more reliable than correlated subqueries in ORM templates
