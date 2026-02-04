---
name: Backend Migrations
description: Create and manage database migrations following best practices for reversibility, zero-downtime deployments, and version control. Use this skill when creating migration files, modifying database schemas, adding or removing tables/columns, managing indexes, or performing data transformations. Apply when working on migration files (migrations/*.ts, migrations/*.sql, *_migration.py), Prisma schema changes, Supabase migrations, or any database evolution tasks. This skill ensures reversible migrations with rollback/down methods, small focused single-change migrations, zero-downtime deployment compatibility, separated schema and data migrations, safe concurrent index creation on large tables, clear descriptive naming conventions, and proper version control practices (never modify deployed migrations).
---

# Backend Migrations

## When to use this skill:

- When creating new database migration files
- When modifying existing database schemas (adding/removing tables or columns)
- When working on migration files (migrations/*.ts, migrations/*.sql, *_migration.py)
- When adding or modifying database indexes for performance
- When performing data migrations or transformations
- When implementing rollback/down methods for migrations
- When ensuring zero-downtime deployment strategies
- When managing schema versioning and migration order
- When separating schema changes from data migrations
- When working with Prisma migrate, Supabase migrations, or Entity Framework migrations
- When creating indexes on large PostgreSQL tables using concurrent options
- When planning backwards-compatible schema changes for high-availability systems

This Skill provides Claude Code with specific guidance on how to adhere to coding standards as they relate to how it should handle backend migrations.

## Instructions

For details, refer to the information provided in this file:
[backend migrations](../../../agent-os/standards/backend/migrations.md)
