---
name: debugging-orm-queries
description: Converts ORM calls to raw SQL and analyzes query performance. Detects N+1 queries, missing indexes, and other anti-patterns. Use when debugging slow queries, tracing ORM-generated SQL, or optimizing database performance for Sequelize, Prisma, TypeORM (Node.js), GORM, sqlc, sqlx, ent (Go), or SQLAlchemy, Django ORM, Peewee (Python).
---

# Debugging ORM Queries

## References

| Language | ORMs | Reference |
|----------|------|-----------|
| Node.js | Sequelize, Prisma, TypeORM | [references/nodejs.md](references/nodejs.md) |
| Go | GORM, sqlc, sqlx, ent | [references/golang.md](references/golang.md) |
| Python | SQLAlchemy, Django, Peewee | [references/python.md](references/python.md) |
| Anti-patterns | N+1, indexes, pagination | [references/anti_patterns.md](references/anti_patterns.md) |

## Scripts

```bash
# Pretty-print SQL
python scripts/sql_formatter.py "SELECT..."

# Detect N+1, missing WHERE, duplicates from log file
python scripts/query_analyzer.py queries.log [--json]

# Parse EXPLAIN output (PostgreSQL or MySQL)
psql -c "EXPLAIN ANALYZE ..." | python scripts/explain_parser.py --postgres
mysql -e "EXPLAIN FORMAT=JSON ..." | python scripts/explain_parser.py --mysql

# Node.js request-scoped query tracking (see script for setup)
# Integrates with Sequelize, Prisma, TypeORM
```

## Quick Patterns

**Enable logging**: Check reference for ORM-specific config (usually `logging: true` or `echo=True`)

**ORM → SQL**: Enable logging, run query, capture output

**SQL → ORM**: Map clauses to methods:
- `SELECT columns` → specify fields/attributes
- `WHERE` → `where/filter` with operators
- `JOIN` → `include/preload/prefetch_related`
- `ORDER BY` → `order/orderBy`
- `LIMIT/OFFSET` → `limit/offset` or cursor-based

**Performance issues**: Run `query_analyzer.py` on logs, check `anti_patterns.md` for solutions
