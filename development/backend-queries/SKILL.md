---
name: Backend Queries
description: Write efficient and secure database queries following best practices for SQL injection prevention, N+1 query optimization, and performance for PostgreSQL (Bun.sql, Prisma, Supabase) and Firestore. Use this skill when writing or modifying database queries, implementing data fetching logic, working with ORMs (Prisma, TypeORM, Entity Framework), using Bun.sql native driver, querying Firestore collections, or implementing caching strategies. Apply when working on service files (services/*.ts, repositories/*.ts, *Service.cs), query builder implementations, data access layers, or any code that fetches or manipulates data. This skill ensures parameterized queries to prevent SQL injection (never interpolate user input), eager loading to prevent N+1 problems, selective column fetching (no SELECT *), strategic indexing on WHERE/JOIN/ORDER BY columns, transactions for related operations, query timeouts for performance, caching expensive queries, prepared statements with Bun.sql for repeated queries, and query-driven modeling for Firestore to avoid complex OR queries.
---

# Backend Queries

## When to use this skill:

- When writing new database queries or data fetching operations
- When working with ORM query builders (Prisma, TypeORM, Sequelize, Entity Framework)
- When using Bun.sql native PostgreSQL driver for high-performance queries
- When implementing service layer methods that query databases
- When working on repository pattern implementations
- When writing raw SQL queries for complex operations
- When optimizing slow queries or addressing N+1 query problems
- When implementing eager loading or query joins
- When adding database indexes to improve query performance
- When wrapping related operations in database transactions
- When implementing caching strategies for frequently-accessed data
- When setting query timeouts to prevent long-running queries
- When working on files that contain data access logic (services/*.ts, repositories/*.ts, *Service.cs, models/*.py)
- When querying Firestore collections and designing queries based on data model
- When using prepared statements for repeated queries in Bun.sql

This Skill provides Claude Code with specific guidance on how to adhere to coding standards as they relate to how it should handle backend queries.

## Instructions

For details, refer to the information provided in this file:
[backend queries](../../../agent-os/standards/backend/queries.md)
