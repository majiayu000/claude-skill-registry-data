---
name: database-engineering
description: >-
  Domain specialist for data persistence, database design, query optimization, and data modeling.
  Scope: SQL injection prevention, indexing strategies, normalization, migrations, scaling, backup/recovery, ORM patterns, N+1 query detection, query optimization, relationship mapping.
  Excludes: API design, business logic, infrastructure, frontend, security beyond database.
  Triggers: "database", "SQL", "query", "index", "schema", "migration", "sharding", "replication", "backup", "N+1", "ORM", "Eloquent", "Django", "query optimization", "slow query", "relationship", "foreign key", "join".
---

# DATABASE_ENGINEERING

## DOMAIN EXPERTISE
- **Common Attacks**: SQL injection (union-based, boolean-based, blind), NoSQL injection, privilege escalation, data exfiltration
- **Common Issues**: Missing indexes, lack of constraints, poor normalization, N+1 queries, inefficient joins, no query timeouts, connection leaks
- **Common Mistakes**: N+1 query problem in loops, missing foreign keys, lack of transactions, no pagination on large datasets, using SELECT *, not using query parameterization
- **Related Patterns**: Normalization, denormalization strategies, indexing patterns, connection pooling, caching strategies, query optimization
- **Problematic Patterns**: God query, magic queries, lack of idempotency, missing rollbacks, monolithic databases
- **Injection Flaws**: SQL injection (parameterized queries needed), NoSQL injection
- **Database-Specific Vulnerabilities**: ORACLE/MYSQL/MSSQL specific issues, NoSQL-specific issues (document injection in MongoDB)
- **Performance Issues**: N+1 query patterns, missing indexes, inefficient algorithms, connection pool exhaustion
- **ORM Patterns**: Eloquent/Django ORM patterns, model discovery, relationship mapping, eager/lazy loading
- **Migration Patterns**: Idempotent migrations, rollback strategies, zero-downtime deployments

## MODE DETECTION
- **WRITE Mode**: Keywords: ["create", "generate", "write", "build", "implement", "add", "new", "design schema", "create migration", "add index", "optimize query"]
- **REVIEW Mode**: Keywords: ["review", "analyze", "audit", "check", "find issues", "query analysis", "performance review", "database review", "schema review"]

## LOADING STRATEGY
### Write Mode (Progressive)
Load patterns based on database requirements:
- Schema questions -> Load `@design/DATABASE-DESIGN.md`
- Query questions -> Load `@relational/SQL-INJECTION.md`, `@relational/INDEXING.md`
- Performance concerns -> Load `@performance/query-optimization.md`
- ORM usage -> Load `@discovery/MODEL-DISCOVERY.md`, `@design/RELATIONSHIP-MAPPING.md`
- Migrations -> Load `@migrations/MIGRATION-BEST-PRACTICES.md`

### Review Mode (Exhaustive)
Load comprehensive checklists:
- IF query review requested -> Load `@relational/NPLUS1.md`, `@relational/INDEXING.md`
- IF schema review requested -> Load `@design/DATABASE-DESIGN.md`
- IF performance review requested -> Load `@performance/query-optimization.md`

### Progressive Loading (Write Mode)
- **IF** request mentions "SQL injection", "parameterized query" -> READ FILE: `@relational/SQL-INJECTION.md`
- **IF** request mentions "index", "slow query", "optimization" -> READ FILE: `@relational/INDEXING.md`, `@connections/CONNECTION-PATTERNS.md`
- **IF** request mentions "schema", "normalization", "design" -> READ FILE: `@design/DATABASE-DESIGN.md`
- **IF** request mentions "N+1", "loop query" -> READ FILE: `@relational/NPLUS1.md`
- **IF** request mentions "migration", "schema change" -> READ FILE: `@migrations/MIGRATION-BEST-PRACTICES.md`
- **IF** request mentions "Eloquent", "Django", "ORM" -> READ FILE: `@discovery/MODEL-DISCOVERY.md`
- **IF** request mentions "relationship", "foreign key", "one-to-many" -> READ FILE: `@design/RELATIONSHIP-MAPPING.md`
- **IF** request mentions "sharding", "replication", "scale" -> READ FILES: `@scaling/SHARDING.md`, `@scaling/REPLICATION.md`
- **IF** request mentions "backup", "recovery", "restore" -> READ FILE: `@backup/BACKUP-RECOVERY.md`
- **IF** request mentions "MongoDB", "NoSQL", "document" -> READ FILE: `@nosql/MONGODB.md`

### Comprehensive Loading (Review Mode)
- **IF** request mentions "review", "analyze", "audit" -> READ FILES: `@relational/SQL-INJECTION.md`, `@relational/INDEXING.md`, `@relational/NPLUS1.md`, `@design/DATABASE-DESIGN.md`


### Write Mode Output
```markdown
## Database Implementation: [Component]

### Platform
[Detected database platform: PostgreSQL/MySQL/MongoDB/etc.]

### Implementation
```sql
-- SQL example for detected platform
```

### ORM Implementation (if applicable)
```language
[Language-specific ORM code]
```

### Performance Considerations
- [Indexing strategy]
- [Query optimization]
- [Connection management]

### Related Patterns
@relational/[specific-pattern].md
```

### Review Mode Output
```markdown
## Database Review Report

### Critical Issues
1. **[Issue Name]**: [Location: file:line]
   - Severity: CRITICAL
   - OWASP Category: [A03:2021-Injection]
   - Description: [Issue details]
   - Impact: [Data exfiltration, unauthorized access]
   - Fix: [Recommended action: parameterized queries, prepared statements]
   - Reference: @relational/SQL-INJECTION.md

### High Priority Issues
1. **[N+1 Query Problem]**: [Location: file:line]
   - Severity: HIGH
   - Description: [Query in loop causing N+1 queries]
   - Impact: [Performance degradation]
   - Fix: [Recommended action: eager loading, JOIN]
   - Reference: @relational/NPLUS1.md

### Medium Priority Issues
[Same format]

### Low Priority Issues
[Same format]
```
