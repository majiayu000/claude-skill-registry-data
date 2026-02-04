---
name: bel-crm-sql-rules
description: |
  CRITICAL: PostgreSQL MCP Server SQL limitations and correct patterns.
  This skill MUST be consulted before writing any SQL for the CRM database.
  Documents what works and what DOES NOT work with mcp__postgresql__ tools.
---

# BEL CRM SQL Rules

## CRITICAL: PostgreSQL MCP Server Limitations

The `mcp__postgresql__` tools have specific limitations. **Violating these rules causes SQL errors.**

---

## FORBIDDEN SQL Patterns (WILL FAIL)

### 1. RETURNING Clause - FORBIDDEN

```sql
-- FORBIDDEN - WILL FAIL with syntax error
INSERT INTO person (name, email) VALUES ('John', 'john@example.com') RETURNING id;

-- FORBIDDEN - WILL FAIL
UPDATE company_site SET name = 'New Name' WHERE id = 1 RETURNING *;

-- FORBIDDEN - WILL FAIL
DELETE FROM event WHERE id = 5 RETURNING id;
```

**Why:** The `write_query` tool parses SQL and rejects `RETURNING` clauses.

### 2. ON CONFLICT (UPSERT) - FORBIDDEN

```sql
-- FORBIDDEN - WILL FAIL with "Only INSERT, UPDATE, or DELETE operations are allowed"
INSERT INTO company_site (name) VALUES ('Acme')
ON CONFLICT (name) DO UPDATE SET updated_at = CURRENT_TIMESTAMP;

-- FORBIDDEN - Even if column HAD a unique constraint
INSERT INTO person (email) VALUES ('test@example.com')
ON CONFLICT (email) DO NOTHING;
```

**Why:** The `write_query` tool does not support `ON CONFLICT` syntax.

**Additional Note:** The CRM tables do NOT have UNIQUE constraints on `name` columns anyway!
- `company_site.name` is NOT unique
- `person.name` is NOT unique
- `sales_opportunity.title` is NOT unique

### 3. Multiple Statements - FORBIDDEN

```sql
-- FORBIDDEN - WILL FAIL
INSERT INTO company_site (name) VALUES ('A'); INSERT INTO company_site (name) VALUES ('B');
```

**Why:** Execute one statement per tool call.

### 4. Transaction Commands - FORBIDDEN

```sql
-- FORBIDDEN
BEGIN; INSERT INTO...; COMMIT;
```

---

## CORRECT SQL Patterns (USE THESE)

### Pattern 1: Simple INSERT (No RETURNING)

```sql
-- CORRECT - Simple INSERT
INSERT INTO company_site (name, address_city, created_at, updated_at)
VALUES ('Neue Firma GmbH', 'Berlin', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP);
```

**To get the ID after insert:**
```sql
-- CORRECT - Query for the ID in a SEPARATE read_query call
SELECT id FROM company_site WHERE name = 'Neue Firma GmbH' ORDER BY created_at DESC LIMIT 1;
```

### Pattern 2: Check-Then-Insert (Instead of UPSERT)

**Step 1: Check if exists (read_query)**
```sql
SELECT id, name FROM company_site WHERE name ILIKE '%Acme%' LIMIT 1;
```

**Step 2a: If found - UPDATE (write_query)**
```sql
UPDATE company_site SET updated_at = CURRENT_TIMESTAMP, notes = 'Updated info' WHERE id = 5;
```

**Step 2b: If not found - INSERT (write_query)**
```sql
INSERT INTO company_site (name, address_city, created_at, updated_at)
VALUES ('Acme GmbH', 'Munich', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP);
```

### Pattern 3: Simple UPDATE

```sql
-- CORRECT
UPDATE person SET job_title = 'CEO', updated_at = CURRENT_TIMESTAMP WHERE id = 42;
```

### Pattern 4: Simple DELETE

```sql
-- CORRECT
DELETE FROM event WHERE id = 123;
```

### Pattern 5: Get ID After Insert

**Two-step process:**

```sql
-- Step 1: INSERT (write_query)
INSERT INTO person (name, email, company_site_id, created_at, updated_at)
VALUES ('Max Mustermann', 'max@example.com', 5, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP);

-- Step 2: GET ID (read_query) - execute AFTER insert succeeds
SELECT id FROM person WHERE email = 'max@example.com' ORDER BY created_at DESC LIMIT 1;
```

---

## Tool Selection Guide

| Operation | Tool | Notes |
|-----------|------|-------|
| SELECT | `read_query` | All SELECT statements |
| INSERT | `write_query` | No RETURNING, no ON CONFLICT |
| UPDATE | `write_query` | No RETURNING |
| DELETE | `write_query` | No RETURNING |
| Get ID after INSERT | `read_query` | Separate call after INSERT |

---

## Common Mistakes and Fixes

### Mistake 1: Using RETURNING to get ID
```sql
-- WRONG
INSERT INTO person (name) VALUES ('John') RETURNING id;
```

**Fix:**
```sql
-- Step 1: write_query
INSERT INTO person (name, created_at, updated_at) VALUES ('John', now(), now());

-- Step 2: read_query
SELECT id FROM person WHERE name = 'John' ORDER BY created_at DESC LIMIT 1;
```

### Mistake 2: Using ON CONFLICT for upsert
```sql
-- WRONG
INSERT INTO company_site (name) VALUES ('Test')
ON CONFLICT (name) DO UPDATE SET updated_at = now();
```

**Fix:**
```sql
-- Step 1: read_query - Check existence
SELECT id FROM company_site WHERE name ILIKE '%Test%' LIMIT 1;

-- Step 2: write_query - INSERT if not found, UPDATE if found
-- If not found:
INSERT INTO company_site (name, created_at, updated_at) VALUES ('Test', now(), now());
-- If found (id=5):
UPDATE company_site SET updated_at = now() WHERE id = 5;
```

### Mistake 3: Using now() vs CURRENT_TIMESTAMP
```sql
-- BOTH WORK - now() and CURRENT_TIMESTAMP are equivalent in PostgreSQL
INSERT INTO event (type, description, event_date, created_at)
VALUES ('call', 'Called customer', now(), CURRENT_TIMESTAMP);
```

---

## Summary Checklist

Before executing SQL with `write_query`:

- [ ] No `RETURNING` clause
- [ ] No `ON CONFLICT` clause
- [ ] Single statement only
- [ ] No transaction commands (BEGIN/COMMIT)
- [ ] If you need the inserted ID: plan a follow-up `read_query`

---

## Reference for Other Skills

This skill should be referenced by:
- `bel-crm-db` - Main CRM database skill
- `bel-crm-schema-write-db` - Schema and SQL examples
- `bel-insert-file-to-crm-and-link-it` - File insertion
- `bel-download-file-from-crm-db` - File retrieval
- Any other skill that writes to the PostgreSQL CRM database
