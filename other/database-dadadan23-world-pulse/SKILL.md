---
name: "database"
description: 'Design database operations including migrations, indexing strategies, transactions, connection pooling, and ORM best practices. Use when creating database schemas, writing migrations, optimizing slow queries, configuring connection pools, or choosing between ORM frameworks.'
metadata:
 author: "AgentX"
 version: "1.0.0"
 created: "2025-01-15"
 updated: "2025-01-15"
---

# Database

> **Purpose**: Efficient, reliable database operations with migrations, indexes, and transactions. 
> **Focus**: ORM patterns, query optimization, data integrity. 
> **Note**: For database-specific details, see [PostgreSQL](../../development/postgresql/SKILL.md) or [SQL Server](../../development/sql-server/SKILL.md).

---

## When to Use This Skill

- Creating database schemas or migrations
- Optimizing slow database queries
- Configuring connection pooling
- Choosing between ORM frameworks
- Implementing data integrity constraints

## Prerequisites

- SQL fundamentals
- Access to a relational database

## Decision Tree

```
Database operation?
+- Schema change?
| +- New table/column? -> Migration (up + down)
| +- Rename/drop? -> Migration + verify no dependents
| - Index needed? -> CREATE INDEX CONCURRENTLY (avoid locks)
+- Query performance?
| +- Slow query? -> EXPLAIN ANALYZE -> add index or rewrite
| +- N+1 problem? -> Use eager loading / JOIN
| - Large result set? -> Pagination (cursor-based preferred)
+- Data integrity?
| +- Multiple writes? -> Use transaction
| - Concurrent access? -> Optimistic concurrency (version column)
- Connection management?
 - Always use connection pooling, never open/close per query
```

## Performance Best Practices

### Database Optimization Checklist

- [ ] Add indexes on foreign keys
- [ ] Add indexes on columns in WHERE/JOIN/ORDER BY
- [ ] Use composite indexes for multi-column queries
- [ ] Analyze query execution plans
- [ ] Fix N+1 queries with eager loading
- [ ] Use connection pooling
- [ ] Cache frequently accessed data
- [ ] Denormalize for read-heavy workloads
- [ ] Partition large tables
- [ ] Archive old data
- [ ] Monitor slow query logs

### Query Analysis

**Analyze Query Performance:**
```sql
-- PostgreSQL
EXPLAIN ANALYZE
SELECT * FROM users WHERE email = 'test@example.com';

-- MySQL
EXPLAIN
SELECT * FROM users WHERE email = 'test@example.com';
```

**Look for:**
- **Seq Scan** - Table scan (bad for large tables)
- **Index Scan** - Uses index (good)
- **Nested Loop** - Join method (can be slow)
- **Hash Join** - Better for large datasets

---

## Common Pitfalls

| Issue | Problem | Solution |
|-------|---------|----------|
| **N+1 queries** | Loading relations one by one | Use eager loading, JOINs |
| **Missing indexes** | Slow queries | Add indexes on WHERE/JOIN columns |
| **SELECT *** | Loading unnecessary data | Select only needed columns |
| **No connection pooling** | Too many connections | Implement connection pooling |
| **Large transactions** | Locks held too long | Keep transactions short |
| **No query timeout** | Queries run forever | Set query timeout limits |

---

## ORM Frameworks

**Popular ORMs:**
- **.NET**: Entity Framework Core, Dapper, NHibernate
- **Python**: SQLAlchemy, Django ORM, Peewee
- **Node.js**: Sequelize, TypeORM, Prisma
- **Java**: Hibernate, JPA, MyBatis
- **PHP**: Doctrine, Eloquent (Laravel)
- **Ruby**: ActiveRecord (Rails)

---

## Resources

**Database Docs:**
- [PostgreSQL Documentation](https://www.postgresql.org/docs/)
- [MySQL Documentation](https://dev.mysql.com/doc/)
- [SQL Server Documentation](https://learn.microsoft.com/sql/)

**Tools:**
- **Query Optimization**: EXPLAIN ANALYZE, query plan visualizers
- **Monitoring**: pg_stat_statements, slow query logs
- **Migration Tools**: Flyway, Liquibase, Alembic

---

**See Also**: [Skills.md](../../../../Skills.md) - [AGENTS.md](../../../../AGENTS.md) - [PostgreSQL](../../development/postgresql/SKILL.md) - [SQL Server](../../development/sql-server/SKILL.md)

**Last Updated**: January 27, 2026

## Scripts

| Script | Purpose | Usage |
|--------|---------|-------|
| [`scaffold-migration.py`](scripts/scaffold-migration.py) | Generate migration scaffold (SQL/EF Core/Alembic) | `python scripts/scaffold-migration.py --type sql --name add_users_table` |

## Troubleshooting

| Issue | Solution |
|-------|----------|
| Slow query performance | Check EXPLAIN plan, add missing indexes, avoid SELECT * |
| Connection pool exhaustion | Increase pool size, ensure connections are properly disposed/returned |
| Migration conflicts | Use sequential numbering, resolve merge conflicts in migration order |

## References

- [Migrations Indexing Queries](references/migrations-indexing-queries.md)
- [Transactions Pooling Orm](references/transactions-pooling-orm.md)