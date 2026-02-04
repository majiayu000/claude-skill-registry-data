---
name: preventing-sql-injection
description: Prevent SQL injection by using $queryRaw tagged templates instead of $queryRawUnsafe. Use when writing raw SQL queries or dynamic queries.
allowed-tools: Read, Write, Edit, Grep
---

# SQL Injection Prevention in Prisma 6

## Overview

SQL injection is one of the most critical security vulnerabilities in database applications. In Prisma 6, raw SQL queries must be written using `$queryRaw` tagged templates for automatic parameterization. **NEVER use `$queryRawUnsafe` with user input.**

## Critical Rules

### 1. ALWAYS Use $queryRaw Tagged Templates

```typescript
const email = userInput;

const users = await prisma.$queryRaw`
  SELECT * FROM "User" WHERE email = ${email}
`;
```

Prisma automatically parameterizes `${email}` to prevent SQL injection.

### 2. NEVER Use $queryRawUnsafe with User Input

```typescript
const email = userInput;

const users = await prisma.$queryRawUnsafe(
  `SELECT * FROM "User" WHERE email = '${email}'`
);
```

**VULNERABLE TO SQL INJECTION** - attacker can inject: `' OR '1'='1`

### 3. Use Prisma.sql for Dynamic Queries

```typescript
import { Prisma } from '@prisma/client';

const conditions: Prisma.Sql[] = [];

if (email) {
  conditions.push(Prisma.sql`email = ${email}`);
}

if (status) {
  conditions.push(Prisma.sql`status = ${status}`);
}

const where = conditions.length > 0
  ? Prisma.sql`WHERE ${Prisma.join(conditions, ' AND ')}`
  : Prisma.empty;

const users = await prisma.$queryRaw`
  SELECT * FROM "User" ${where}
`;
```

## Attack Vectors and Prevention

### Vector 1: String Concatenation in WHERE Clause

**VULNERABLE:**
```typescript
const searchTerm = req.query.search;

const results = await prisma.$queryRawUnsafe(
  `SELECT * FROM "Product" WHERE name LIKE '%${searchTerm}%'`
);
```

**Attack:** `'; DELETE FROM "Product"; --`

**SAFE:**
```typescript
const searchTerm = req.query.search;

const results = await prisma.$queryRaw`
  SELECT * FROM "Product" WHERE name LIKE ${'%' + searchTerm + '%'}
`;
```

### Vector 2: Dynamic Column Names

**VULNERABLE:**
```typescript
const sortColumn = req.query.sortBy;

const users = await prisma.$queryRawUnsafe(
  `SELECT * FROM "User" ORDER BY ${sortColumn}`
);
```

**Attack:** `email; DROP TABLE "User"; --`

**SAFE:**
```typescript
const sortColumn = req.query.sortBy;
const allowedColumns = ['email', 'name', 'createdAt'];

if (!allowedColumns.includes(sortColumn)) {
  throw new Error('Invalid sort column');
}

const users = await prisma.$queryRawUnsafe(
  `SELECT * FROM "User" ORDER BY ${sortColumn}`
);
```

**Note:** Column names cannot be parameterized, so use allowlist validation.

### Vector 3: Dynamic Table Names

**VULNERABLE:**
```typescript
const tableName = req.params.table;

const data = await prisma.$queryRawUnsafe(
  `SELECT * FROM "${tableName}"`
);
```

**Attack:** `User" WHERE 1=1; DROP TABLE "Session"; --`

**SAFE:**
```typescript
const tableName = req.params.table;
const allowedTables = ['User', 'Product', 'Order'];

if (!allowedTables.includes(tableName)) {
  throw new Error('Invalid table name');
}

const data = await prisma.$queryRawUnsafe(
  `SELECT * FROM "${tableName}"`
);
```

### Vector 4: IN Clause with Arrays

**VULNERABLE:**
```typescript
const ids = req.body.ids.join(',');

const users = await prisma.$queryRawUnsafe(
  `SELECT * FROM "User" WHERE id IN (${ids})`
);
```

**Attack:** `1) OR 1=1; --`

**SAFE:**
```typescript
const ids = req.body.ids;

const users = await prisma.$queryRaw`
  SELECT * FROM "User" WHERE id IN (${Prisma.join(ids)})
`;
```

### Vector 5: LIMIT and OFFSET Injection

**VULNERABLE:**
```typescript
const limit = req.query.limit;
const offset = req.query.offset;

const users = await prisma.$queryRawUnsafe(
  `SELECT * FROM "User" LIMIT ${limit} OFFSET ${offset}`
);
```

**Attack:** `10; DELETE FROM "User"; --`

**SAFE:**
```typescript
const limit = parseInt(req.query.limit, 10);
const offset = parseInt(req.query.offset, 10);

if (isNaN(limit) || isNaN(offset)) {
  throw new Error('Invalid pagination parameters');
}

const users = await prisma.$queryRaw`
  SELECT * FROM "User" LIMIT ${limit} OFFSET ${offset}
`;
```

## Dynamic Query Building Patterns

### Pattern 1: Optional Filters

```typescript
import { Prisma } from '@prisma/client';

interface SearchFilters {
  email?: string;
  status?: string;
  minAge?: number;
}

async function searchUsers(filters: SearchFilters) {
  const conditions: Prisma.Sql[] = [];

  if (filters.email) {
    conditions.push(Prisma.sql`email LIKE ${'%' + filters.email + '%'}`);
  }

  if (filters.status) {
    conditions.push(Prisma.sql`status = ${filters.status}`);
  }

  if (filters.minAge !== undefined) {
    conditions.push(Prisma.sql`age >= ${filters.minAge}`);
  }

  const where = conditions.length > 0
    ? Prisma.sql`WHERE ${Prisma.join(conditions, ' AND ')}`
    : Prisma.empty;

  return prisma.$queryRaw`
    SELECT * FROM "User" ${where}
  `;
}
```

### Pattern 2: Dynamic Sorting

```typescript
type SortColumn = 'email' | 'name' | 'createdAt';
type SortOrder = 'ASC' | 'DESC';

async function getUsers(sortBy: SortColumn, order: SortOrder) {
  const allowedColumns: SortColumn[] = ['email', 'name', 'createdAt'];
  const allowedOrders: SortOrder[] = ['ASC', 'DESC'];

  if (!allowedColumns.includes(sortBy) || !allowedOrders.includes(order)) {
    throw new Error('Invalid sort parameters');
  }

  return prisma.$queryRawUnsafe(
    `SELECT * FROM "User" ORDER BY ${sortBy} ${order}`
  );
}
```

### Pattern 3: Complex JOIN with Dynamic Conditions

```typescript
async function searchOrdersWithProducts(
  userId?: number,
  productName?: string,
  minTotal?: number
) {
  const conditions: Prisma.Sql[] = [];

  if (userId !== undefined) {
    conditions.push(Prisma.sql`o."userId" = ${userId}`);
  }

  if (productName) {
    conditions.push(Prisma.sql`p.name LIKE ${'%' + productName + '%'}`);
  }

  if (minTotal !== undefined) {
    conditions.push(Prisma.sql`o.total >= ${minTotal}`);
  }

  const where = conditions.length > 0
    ? Prisma.sql`WHERE ${Prisma.join(conditions, ' AND ')}`
    : Prisma.empty;

  return prisma.$queryRaw`
    SELECT o.*, p.name as "productName"
    FROM "Order" o
    INNER JOIN "Product" p ON o."productId" = p.id
    ${where}
    ORDER BY o."createdAt" DESC
  `;
}
```

### Pattern 4: Batch Operations with Safe Arrays

```typescript
async function updateUserStatuses(
  userIds: number[],
  newStatus: string
) {
  if (userIds.length === 0) {
    return [];
  }

  return prisma.$queryRaw`
    UPDATE "User"
    SET status = ${newStatus}, "updatedAt" = NOW()
    WHERE id IN (${Prisma.join(userIds)})
    RETURNING *
  `;
}
```

## When $queryRawUnsafe is Acceptable

`$queryRawUnsafe` is ONLY acceptable when:

1. **No user input involved** (static queries only)
2. **Identifiers from allowlist** (column/table names validated)
3. **Generated by type-safe builder** (internal tools, not user data)

```typescript
async function getTableSchema(tableName: 'User' | 'Product' | 'Order') {
  return prisma.$queryRawUnsafe(`
    SELECT column_name, data_type
    FROM information_schema.columns
    WHERE table_name = '${tableName}'
  `);
}
```

**Still requires:** TypeScript literal type or runtime validation against allowlist.

## Migration from $queryRawUnsafe

### Before:
```typescript
const status = req.query.status;
const minAge = req.query.minAge;

const users = await prisma.$queryRawUnsafe(
  `SELECT * FROM "User" WHERE status = '${status}' AND age >= ${minAge}`
);
```

### After:
```typescript
const status = req.query.status;
const minAge = parseInt(req.query.minAge, 10);

const users = await prisma.$queryRaw`
  SELECT * FROM "User"
  WHERE status = ${status} AND age >= ${minAge}
`;
```

## Testing for SQL Injection

### Test Case 1: Authentication Bypass
```typescript
const maliciousEmail = "' OR '1'='1";

const user = await prisma.$queryRaw`
  SELECT * FROM "User" WHERE email = ${maliciousEmail}
`;
```

**Expected:** Returns empty array (no match for literal string)

### Test Case 2: Comment Injection
```typescript
const maliciousInput = "test'; --";

const users = await prisma.$queryRaw`
  SELECT * FROM "User" WHERE name = ${maliciousInput}
`;
```

**Expected:** Searches for exact string `test'; --`, doesn't comment out rest of query

### Test Case 3: Union-Based Attack
```typescript
const maliciousId = "1 UNION SELECT password FROM Admin";

const user = await prisma.$queryRaw`
  SELECT * FROM "User" WHERE id = ${maliciousId}
`;
```

**Expected:** Type error or no results (string cannot match integer id column)

## Detection and Remediation

### Detection Patterns

Use grep to find vulnerable code:

```bash
grep -r "\$queryRawUnsafe" --include="*.ts"
grep -r "queryRawUnsafe.*\${" --include="*.ts"
grep -r "queryRawUnsafe.*req\." --include="*.ts"
```

### Automated Detection

```typescript
import { ESLint } from 'eslint';

const dangerousPatterns = [
  /\$queryRawUnsafe\s*\([^)]*\$\{/,
  /queryRawUnsafe\s*\([^)]*req\./,
  /queryRawUnsafe\s*\([^)]*params\./,
  /queryRawUnsafe\s*\([^)]*query\./,
  /queryRawUnsafe\s*\([^)]*body\./,
];
```

### Remediation Checklist

- [ ] Replace all `$queryRawUnsafe` with `$queryRaw` where user input exists
- [ ] Use `Prisma.sql` for dynamic query building
- [ ] Validate column/table names against allowlists
- [ ] Parameterize all user inputs
- [ ] Parse numeric inputs before use
- [ ] Use `Prisma.join()` for array parameters
- [ ] Add SQL injection test cases
- [ ] Run security audit tools

## Related Skills

**Security Best Practices:**

- If sanitizing user inputs before database operations, use the sanitizing-user-inputs skill from typescript for input sanitization patterns

## Resources

- [Prisma Raw Database Access Docs](https://www.prisma.io/docs/orm/prisma-client/queries/raw-database-access)
- [OWASP SQL Injection Prevention Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/SQL_Injection_Prevention_Cheat_Sheet.html)
- [Prisma Security Best Practices](https://www.prisma.io/docs/orm/prisma-client/queries/raw-database-access#sql-injection)

## Summary

- **ALWAYS** use `$queryRaw` tagged templates for user input
- **NEVER** use `$queryRawUnsafe` with untrusted data
- **USE** `Prisma.sql` and `Prisma.join()` for dynamic queries
- **VALIDATE** column/table names against allowlists
- **TEST** for common SQL injection attack vectors
- **AUDIT** codebase regularly for `$queryRawUnsafe` usage
