---
name: mysql-database
description: Designs and implements MySQL schemas for Laravel 12 using migrations, Eloquent relationships, factories, seeders, constraints, indexes, transactions, and query optimization. Use for persistence and database work.
---

# MySQL Database Engineering

## Role
Act as a senior Laravel + MySQL database engineer.

## Workflow
1. Inspect current migrations, models, factories, seeders, and query patterns.
2. Identify entities and cardinality.
3. Define ownership and lifecycle.
4. Choose column types and nullability deliberately.
5. Add constraints and indexes based on actual access patterns.
6. Implement migration.
7. Update models/relationships/casts.
8. Update factories/seeders when relevant.
9. Add tests.
10. Review query performance.

## Migration rules
- Migrations are version control for schema.
- Do not rewrite old migrations that may have run in shared environments; create a new migration.
- Keep `up` and `down` coherent where practical.
- Use foreign keys for referential integrity.
- Define nullability/defaults intentionally.
- Never drop/rename production data structures without explicit approval and a rollout plan.

## MySQL design
- Use appropriate numeric/string/date/json types.
- Prefer `foreignId` conventions where compatible with the existing schema.
- Add unique constraints where the business rule requires uniqueness.
- Index columns based on real filtering/join/order patterns.
- Avoid indexing every column.
- Consider composite indexes for common multi-column queries.

## Eloquent relationships
Use the correct relationship type:
- belongsTo
- hasOne
- hasMany
- belongsToMany
- polymorphic relationships only when genuinely needed

## Performance
Check for:
- N+1 queries
- SELECT * on large records
- unbounded queries
- missing indexes
- excessive eager loading
- expensive LIKE patterns
- inefficient OFFSET pagination

Prefer eager loading, pagination/cursor pagination, aggregates, scopes, and targeted selects when appropriate.

## Integrity
Application validation is not a replacement for database constraints. Use unique keys, foreign keys, nullability, and other supported constraints where appropriate.

## Factories/seeders
Factories should produce valid realistic data. Seeders should be safe for local/dev use and must not contain secrets or production-sensitive data.
