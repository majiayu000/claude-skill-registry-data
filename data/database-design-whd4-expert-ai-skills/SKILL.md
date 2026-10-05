---
name: database-design
description: Database design principles and decision-making. Schema design, indexing strategy, ORM selection, serverless databases.
allowed-tools: Read, Write, Edit, Glob, Grep
---

# Database Design

> **Learn to THINK, not copy SQL patterns.**

## 🎯 Selective Reading Rule

**Read ONLY files relevant to the request!** Check the content map, find what you need.

| File | Description | When to Read |
|------|-------------|--------------|
| `database-selection.md` | PostgreSQL vs Neon vs Turso vs SQLite | Choosing database |
| `orm-selection.md` | Drizzle vs Prisma vs Kysely | Choosing ORM |
| `schema-design.md` | Normalization, PKs, relationships | Designing schema |
| `indexing.md` | Index types, composite indexes | Performance tuning |
| `optimization.md` | N+1, EXPLAIN ANALYZE | Query optimization |
| `migrations.md` | Safe migrations, serverless DBs | Schema changes |

## ⚡ Indexing Strategy (Cheatsheet)

**Default to B-Tree. Know when to switch.**

| Index Type | Use Case | Example |
|------------|----------|---------|
| **B-Tree** | Equality (`=`), Range (`<`, `>`), Sorting (`ORDER BY`) | `WHERE age > 21` |
| **Hash** | Exact equality ONLY (Faster than B-Tree, but limited) | `WHERE uuid = '...'` |
| **GIN** | JSONB, Full Text Search, Arrays | `WHERE data @> '{"tag": "urgent"}'` |
| **GiST** | Geo-spatial, Nearest Neighbor | `WHERE location <@ box` |

**Composite Index Rule:** Order matters! `(last_name, first_name)` helps `WHERE last_name='Bond'`, but DOES NOT help `WHERE first_name='James'`. (**Leftmost Prefix Rule**)

## ⚖️ Scaling: Partitioning vs Sharding

| Strategy | What is it? | Complexity | When to use? |
|----------|-------------|------------|--------------|
| **Partitioning** | Splitting one table into chunks on the **SAME** server. | Medium | Table > 100GB. Need to delete old data fast (`DROP PARTITION`). |
| **Sharding** | Splitting data across **DIFFERENT** servers. | Extreme | Write QPS > Single Node limit. Massive scale (Petabytes). |

## 🔌 Connection Pooling (Serverless)

**Serverless Apps + Postgres = Disaster.**
Lambda scales to 1,000 instances -> 1,000 DB connections -> DB Crashes.

**Solution:** Use **PgBouncer** (or AWS RDS Proxy / Supabase Pooler).

- Function connects to Proxy (TCP).
- Proxy holds small pool of persistent connections to DB.
- **Transactional Mode:** Connection matches to DB only for duration of transaction. Best for serverless.

---

## ⚠️ Core Principle

- ASK user for database preferences when unclear
- Choose database/ORM based on CONTEXT
- Don't default to PostgreSQL for everything

---

## Decision Checklist

Before designing schema:

- [ ] Asked user about database preference?
- [ ] Chosen database for THIS context?
- [ ] Considered deployment environment?
- [ ] Planned index strategy?
- [ ] Defined relationship types?

---

## Anti-Patterns

❌ Default to PostgreSQL for simple apps (SQLite may suffice)
❌ Skip indexing
❌ Use SELECT * in production
❌ Store JSON when structured data is better
❌ Ignore N+1 queries
