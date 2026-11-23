---
name: check-query-safety
description: >
  Review database queries in a file or module for N+1 patterns, unbounded
  scans, SQL injection risks, and over-fetching. Use during code review or
  before a performance-sensitive release. Trigger on "is this query safe",
  "check for N+1 queries", "could this cause a SQL injection", "will this
  query scale", or "review my database queries". This is the deep,
  query-focused audit — review-changes only flags query issues in passing
  during a general review; use this skill when queries need dedicated
  scrutiny.
---

# check-query-safety

## You are a database query safety reviewer. Your job is to find query problems that cause production incidents: injection vulnerabilities, N+1 query patterns, unbounded result sets, and over-fetching. Be specific — report the exact file, function, and line.

## Step 1 — Detect the ORM and query builder

Identify what data-access technology the project uses:

Look for imports of:

- **Prisma**: `@prisma/client`
- **TypeORM**: `typeorm`
- **Drizzle**: `drizzle-orm`
- **Knex**: `knex`
- **Sequelize**: `sequelize`
- **SQLAlchemy**: `sqlalchemy`
- **Django ORM**: `from django.db import models`
- **ActiveRecord**: Rails conventions
- **database/sql**: Go stdlib
- **Raw SQL**: template literals, `query()`, `execute()`, `db.raw()`

**NestJS.** If the project uses NestJS (`@nestjs/core` in `package.json`), also apply the framework checks in [references/nestjs.md](references/nestjs.md), covering writes under concurrent requests, constraint violations, network calls inside transactions and values that come back as strings. A documented convention still wins over them.

---

## Step 2 — Check for SQL injection

Search for any query construction that involves string concatenation or interpolation of user-controlled values:

**High-risk patterns:**

```typescript
// Direct string interpolation in query
db.query(`SELECT * FROM users WHERE id = ${userId}`);
db.raw(`WHERE name = '${name}'`);
knex.raw(`SELECT * FROM orders WHERE status = '${status}'`);
```

```python
cursor.execute(f"SELECT * FROM users WHERE id = {user_id}")
cursor.execute("DELETE FROM sessions WHERE token = '" + token + "'")
```

```go
db.Query("SELECT * FROM users WHERE id = " + userId)
```

**Safe patterns (parameterized):**

```typescript
db.query("SELECT * FROM users WHERE id = $1", [userId]);
prisma.user.findUnique({ where: { id: userId } });
knex("users").where({ id: userId });
```

For each injection risk found:

- file path and line number
- the vulnerable pattern
- the user-controlled input source (request param, body field, header)
- the parameterized equivalent

---

## Step 3 — Detect N+1 query patterns

Search for loops or iteration that contains database queries:

**Pattern 1: query inside a loop**

```typescript
// N+1: one query per order
for (const order of orders) {
  const items = await db.orderItem.findMany({ where: { orderId: order.id } });
}
```

**Pattern 2: calling a function with a query inside a map/forEach**

```typescript
const ordersWithItems = await Promise.all(
  orders.map((order) => this.orderItemService.findByOrderId(order.id)), // N queries
);
```

**Pattern 3: missing include/join in the initial fetch**

```typescript
// Fetches orders without items, then queries items one by one elsewhere
const orders = await prisma.order.findMany(); // missing: include: { items: true }
```

For each N+1 found:

- the location of the loop and the query inside it
- the count of queries that would execute (if determinable)
- the batched/joined alternative (`include`, `findMany` with `in` filter, DataLoader pattern)

---

## Step 4 — Identify unbounded queries

Find queries that could return unbounded result sets:

**Missing `take`/`limit`:**

```typescript
// Could return millions of rows
await prisma.event.findMany();
await db("events").select("*");
```

**Missing `where` on a large or growing table:**

```typescript
await prisma.auditLog.findMany(); // audit logs grow indefinitely
```

**Count queries on large tables without an index filter:**

```sql
SELECT COUNT(*) FROM events -- full table scan if no index
```

For each unbounded query:

- file, line, and table name
- estimated growth rate if visible from schema or naming
- suggested `take`/`limit` or `where` filter

---

## Step 5 — Detect over-fetching

Find queries that load significantly more data than they use:

**Loading full records when only one or two fields are needed:**

```typescript
// Loads the entire User object to get just the email
const user = await prisma.user.findUnique({ where: { id } });
return user.email; // only this field is used

// Better:
const user = await prisma.user.findUnique({
  where: { id },
  select: { email: true },
});
```

**Selecting all columns in a raw query:**

```sql
SELECT * FROM users WHERE id = $1  -- when only name and email are needed
```

Flag instances where the fetched object has more than ~5 fields but only 1–2 are used downstream.

---

## Step 6 — Check for missing transaction boundaries

Find sequences of writes that should be atomic but are not wrapped in a transaction:

```typescript
// Vulnerable to partial failure
await prisma.order.create({ data: orderData });
await prisma.inventory.update({
  where: { id },
  data: { quantity: { decrement: 1 } },
});
// If the second fails, inventory is not decremented but the order was created
```

Flag write sequences involving two or more related tables with no `$transaction` or equivalent.

---

## Step 7 — Report findings

```text
Query safety review: <target>
──────────────────────────────────────────────────

SQL injection risks (N)
1. [high] String interpolation in raw query — src/path/file.ts:42
   db.query(`SELECT * FROM users WHERE id = ${req.params.id}`)
   Input source: req.params.id (route parameter, user-controlled)
   Fix: db.query('SELECT * FROM users WHERE id = $1', [req.params.id])

N+1 patterns (N)
1. [medium] Query inside loop — src/path/file.ts:88
   findMany called for each order in a loop of N orders
   Fix: add include: { items: true } to the initial order query

Unbounded queries (N)
1. [medium] findMany without take — src/path/file.ts:115
   prisma.event.findMany() on a table with no result limit
   Fix: add take: 100 (or the appropriate page size) and pagination

Over-fetching (N)
1. [low] Full user record loaded for email only — src/path/file.ts:200
   Fix: add select: { email: true }

Missing transactions (N)
1. [medium] Multi-table write without transaction — src/path/file.ts:250
   order.create + inventory.update not wrapped in $transaction
   Fix: wrap both in prisma.$transaction([...])

Summary
  <overall verdict: no issues / minor issues / issues requiring immediate attention>
```
