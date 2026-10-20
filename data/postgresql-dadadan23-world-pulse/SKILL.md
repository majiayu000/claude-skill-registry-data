---
name: "postgresql"
description: 'Develop PostgreSQL databases with JSONB, arrays, full-text search, and performance optimization. Use when writing PostgreSQL queries, using JSONB operations, implementing full-text search, optimizing query performance with indexes, or configuring row-level security.'
metadata:
 author: "AgentX"
 version: "1.0.0"
 created: "2025-01-15"
 updated: "2025-01-15"
compatibility:
 languages: ["sql", "plpgsql"]
 platforms: ["windows", "linux", "macos"]
---

# PostgreSQL Database Development

> **Purpose**: Production-ready PostgreSQL development for high-performance, scalable applications. 
> **Audience**: Backend engineers and database administrators working with PostgreSQL. 
> **Standard**: Follows [github/awesome-copilot](https://github.com/github/awesome-copilot) PostgreSQL patterns.

---

## When to Use This Skill

- Writing PostgreSQL queries with JSONB or array operations
- Implementing full-text search in PostgreSQL
- Optimizing PostgreSQL query performance with indexes
- Using window functions and CTEs
- Configuring row-level security (RLS)

## Prerequisites

- PostgreSQL 14+ installed or accessible
- psql or pgAdmin client

## Quick Reference

| Need | Solution | Pattern |
|------|----------|---------|
| **JSONB query** | Containment operator | `WHERE data @> '{"status": "active"}'::jsonb` |
| **Array operations** | ANY operator | `WHERE id = ANY(ARRAY[1,2,3])` |
| **Full-text search** | GIN index + tsvector | `CREATE INDEX ON posts USING gin(to_tsvector('english', content))` |
| **Window functions** | ROW_NUMBER, RANK | `ROW_NUMBER() OVER (PARTITION BY category ORDER BY created_at DESC)` |
| **Upsert** | INSERT ... ON CONFLICT | `ON CONFLICT (id) DO UPDATE SET ...` |
| **JSON aggregation** | jsonb_agg | `SELECT jsonb_agg(row_to_json(t)) FROM ...` |

---

## PostgreSQL Version

**Current**: PostgreSQL 16+ 
**Minimum**: PostgreSQL 14+

---

## Common Pitfalls

| Issue | Problem | Solution |
|-------|---------|----------|
| **N+1 queries** | Loading relations one by one | Use JOINs or array_agg |
| **Missing indexes** | Slow queries | Add indexes on WHERE, JOIN, ORDER BY columns |
| **OFFSET pagination** | Slow for large offsets | Use cursor-based pagination |
| **SELECT *** | Unnecessary data transfer | Select only needed columns |
| **Unparameterized queries** | SQL injection risk | Always use parameterized queries |
| **No connection pooling** | Too many connections | Use pgBouncer or application pooling |

---

## Resources

- **PostgreSQL Docs**: [postgresql.org/docs](https://www.postgresql.org/docs/)
- **pgAdmin**: GUI tool for PostgreSQL
- **pg_stat_statements**: Query performance monitoring
- **EXPLAIN Visualizer**: [explain.depesz.com](https://explain.depesz.com)
- **Awesome Copilot**: [github.com/github/awesome-copilot](https://github.com/github/awesome-copilot)

---

**See Also**: [Skills.md](../../../../Skills.md) - [AGENTS.md](../../../../AGENTS.md) - [Database Skill](../../architecture/database/SKILL.md)

**Last Updated**: January 27, 2026

## Troubleshooting

| Issue | Solution |
|-------|----------|
| Slow JSONB queries | Create GIN index on JSONB column |
| Full-text search not matching | Check tsvector configuration matches query language, rebuild indexes |
| Deadlock detected | Access tables in consistent order across transactions, keep transactions short |

## References

- [Postgres Data Types](references/postgres-data-types.md)
- [Postgres Query Patterns](references/postgres-query-patterns.md)
- [Postgres Advanced](references/postgres-advanced.md)